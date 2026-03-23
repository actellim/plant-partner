import json
import re
import os
from thefuzz import fuzz, process

USDA_FILE = 'usda_data.jsonl'
PFAF_FILE = 'pfaf_data.jsonl'
OUTPUT_FILE = 'merged_plants.jsonl'
DEBUG_FILE = 'match_debug.json'

# Tune this based on log review.
FUZZY_THRESHOLD = 95

def clean_scientific_name(name):
    """Strips authors and HTML tags to get the base botanical name."""
    if not name: return ""
    name = re.sub(r'<[^>]*>', '', name)
    name = re.sub(r'\(.*?\)', '', name)
    tokens = [t for t in name.split() if t.strip()]
    if len(tokens) < 2: return name.strip()
    genus, species = tokens[0], tokens[1]
    base_name = f"{genus} {species}"
    infraspecific = ""
    for i, token in enumerate(tokens):
        if token in ['var.', 'ssp.', 'subsp.', 'f.']:
            if i + 1 < len(tokens):
                infraspecific = f" {token} {tokens[i+1]}"
                break
    return (base_name + infraspecific).strip()

def get_base_species(cleaned_name):
    """Returns just the Genus and Species."""
    tokens = cleaned_name.split()
    return f"{tokens[0]} {tokens[1]}" if len(tokens) >= 2 else cleaned_name

def load_jsonl(filepath):
    data = []
    if not os.path.exists(filepath): return data
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try: data.append(json.loads(line))
                except: pass
    return data

def merge_datasets():
    print("Loading datasets...")
    usda_records = load_jsonl(USDA_FILE)
    pfaf_records = load_jsonl(PFAF_FILE)
    
    # Pre-filter USDA records
    usda_records = [r for r in usda_records if not (r.get('not_found') or r.get('error'))]
    
    print(f"Loaded {len(usda_records)} USDA and {len(pfaf_records)} PFAF records.")
    
    pfaf_lookup = {}
    pfaf_cleaned_names = []
    for p in pfaf_records:
        cleaned = clean_scientific_name(p['scientific_name']).lower()
        pfaf_lookup[cleaned] = p
        pfaf_cleaned_names.append(cleaned)

    merged_results = []
    pfaf_merged_keys = set()
    match_debug = []
    
    stats = {
        "exact": 0,
        "hierarchical": 0,
        "fuzzy": 0,
        "none": 0
    }

    print(f"Merging records (Threshold: {FUZZY_THRESHOLD})...")
    
    for usda in usda_records:
        original_name = usda['scientificName']
        cleaned_name = clean_scientific_name(original_name).lower()
        base_species = get_base_species(cleaned_name).lower()
        
        match = None
        match_type = None
        match_score = 100
        
        # 1. Exact Match
        if cleaned_name in pfaf_lookup:
            match = pfaf_lookup[cleaned_name]
            match_type = "exact"
        # 2. Hierarchical Match
        elif base_species in pfaf_lookup:
            match = pfaf_lookup[base_species]
            match_type = "hierarchical"
        # 3. Fuzzy Match
        else:
            best_match, score = process.extractOne(cleaned_name, pfaf_cleaned_names, scorer=fuzz.token_sort_ratio)
            
            # Token-length guard: If the species epithet is short, a 1-2 letter difference
            # (like 'rigida' vs 'frigida') yields a high score but is a different species.
            # We require a higher score (e.g., 98) for short words, or we reject if the 
            # absolute difference in characters is too impactful.
            is_valid_fuzzy = False
            if score >= FUZZY_THRESHOLD:
                # Compare the specific epithets (second word)
                usda_parts = cleaned_name.split()
                pfaf_parts = best_match.split()
                
                if len(usda_parts) >= 2 and len(pfaf_parts) >= 2:
                    usda_epithet = usda_parts[1]
                    pfaf_epithet = pfaf_parts[1]
                    
                    # If it's a very short epithet, a 1-character change is too risky
                    if len(usda_epithet) <= 7 or len(pfaf_epithet) <= 7:
                        # Require a near-perfect match for short epithets
                        if score >= 98:
                            is_valid_fuzzy = True
                    else:
                        # For longer epithets, the 95 threshold is generally safe
                        is_valid_fuzzy = True
                else:
                    # Single word genus matches (rare, but just in case)
                    is_valid_fuzzy = True

            if is_valid_fuzzy:
                match = pfaf_lookup[best_match]
                match_type = "fuzzy"
                match_score = score
            else:
                match_type = "none"

        stats[match_type] += 1

        if match:
            match_debug.append({
                "type": match_type,
                "score": match_score,
                "usda_name": original_name,
                "pfaf_match": match['scientific_name']
            })

        consolidated = {
            "scientific_name_primary": original_name,
            "common_name_primary": usda.get('commonName'),
            "usda_traits": usda.get('traits'),
            "pfaf_traits": None,
            "pfaf_descriptions": None,
            "attributions": [{
                "source": "USDA PLANTS",
                "license": "Public Domain",
                "url": f"https://plants.usda.gov/home/plantProfile?symbol={usda.get('symbol')}",
                "original_scientific_name": original_name
            }]
        }

        if match:
            match_key = clean_scientific_name(match['scientific_name']).lower()
            pfaf_merged_keys.add(match_key)
            consolidated["pfaf_traits"] = match.get("traits")
            consolidated["pfaf_descriptions"] = match.get("descriptions")
            
            pfaf_attr = match["attributions"][0].copy()
            if match_type == "hierarchical":
                pfaf_attr["note"] = f"Inherited from parent species: {match['scientific_name']}"
            elif match_type == "fuzzy":
                pfaf_attr["note"] = f"Fuzzy match (score: {match_score}) with: {match['scientific_name']}"
            
            consolidated["attributions"].append(pfaf_attr)
            if not consolidated["common_name_primary"]:
                consolidated["common_name_primary"] = match.get("common_name")

        merged_results.append(consolidated)

    # Add orphans
    orphan_count = 0
    for cleaned_name in pfaf_cleaned_names:
        if cleaned_name not in pfaf_merged_keys:
            p = pfaf_lookup[cleaned_name]
            merged_results.append({
                "scientific_name_primary": p['scientific_name'],
                "common_name_primary": p.get('common_name'),
                "usda_traits": None,
                "pfaf_traits": p.get('traits'),
                "pfaf_descriptions": p.get('descriptions'),
                "attributions": p.get('attributions', [])
            })
            orphan_count += 1

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for r in merged_results:
            f.write(json.dumps(r) + '\n')
            
    with open(DEBUG_FILE, 'w', encoding='utf-8') as f:
        json.dump(match_debug, f, indent=2)

    print(f"\n--- Merge Summary (USDA -> PFAF) ---")
    print(f"Exact Matches:        {stats['exact']}")
    print(f"Hierarchical Matches:  {stats['hierarchical']}")
    print(f"Fuzzy Matches:         {stats['fuzzy']}")
    print(f"No Match:              {stats['none']}")
    print(f"------------------------------------")
    print(f"Total Joins:           {stats['exact'] + stats['hierarchical'] + stats['fuzzy']}")
    print(f"Standalone PFAF:       {orphan_count}")
    print(f"Total Final Records:   {len(merged_results)}")
    print(f"\nOutput: {OUTPUT_FILE}")
    print(f"Review all matches in: {DEBUG_FILE}")

if __name__ == "__main__":
    merge_datasets()
