import json
import re
import os
from thefuzz import fuzz, process

USDA_FILE = 'usda_data.jsonl'
PFAF_FILE = 'pfaf_data.jsonl'
OUTPUT_FILE = 'merged_plants.jsonl'
DEBUG_FILE = 'match_debug.json'

# Thresholds for calibration
GENUS_THRESHOLD = 90
SPECIES_THRESHOLD_BASE = 90

# Near-miss logging thresholds
GENUS_NEAR_MISS = 85
SPECIES_NEAR_MISS = 80

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
    usda_records = [r for r in usda_records if not (r.get('not_found') or r.get('error'))]
    
    print(f"Loaded {len(usda_records)} USDA and {len(pfaf_records)} PFAF records.")
    
    pfaf_lookup = {}
    pfaf_genera_map = {}
    for p in pfaf_records:
        cleaned = clean_scientific_name(p['scientific_name']).lower()
        pfaf_lookup[cleaned] = p
        genus = cleaned.split()[0]
        if genus not in pfaf_genera_map: pfaf_genera_map[genus] = []
        pfaf_genera_map[genus].append(cleaned)

    pfaf_genera_list = list(pfaf_genera_map.keys())
    merged_results = []
    pfaf_merged_keys = set()
    match_debug = []
    
    stats = {"exact": 0, "hierarchical": 0, "fuzzy": 0, "none": 0}

    print(f"Merging records (Prefix Guard active)...")
    
    for usda in usda_records:
        original_name = usda['scientificName']
        cleaned_name = clean_scientific_name(original_name).lower()
        base_species = get_base_species(cleaned_name).lower()
        usda_parts = cleaned_name.split()
        usda_genus = usda_parts[0] if usda_parts else ""
        
        match = None
        match_type = None
        match_score = 100
        
        if cleaned_name in pfaf_lookup:
            match = pfaf_lookup[cleaned_name]
            match_type = "exact"
        elif base_species in pfaf_lookup:
            match = pfaf_lookup[base_species]
            match_type = "hierarchical"
        elif usda_genus:
            best_genera_res = process.extract(usda_genus, pfaf_genera_list, scorer=fuzz.ratio, limit=3)
            valid_genera_res = [res for res in best_genera_res if res[1] >= GENUS_THRESHOLD]
            
            if valid_genera_res:
                candidates = []
                for g, g_score in valid_genera_res:
                    candidates.extend(pfaf_genera_map[g])
                
                if candidates:
                    best_match, score = process.extractOne(cleaned_name, candidates, scorer=fuzz.token_sort_ratio)
                    
                    is_valid_fuzzy = False
                    if score >= SPECIES_THRESHOLD_BASE:
                        pfaf_parts = best_match.split()
                        if len(usda_parts) >= 2 and len(pfaf_parts) >= 2:
                            u_epithet = usda_parts[1]
                            p_epithet = pfaf_parts[1]
                            # PREFIX GUARD: Most valid spelling variations share the first 3 characters.
                            # This correctly filters cana/cina (c match only) and rigida/frigida (r vs f).
                            u_pref = u_epithet[:3]
                            p_pref = p_epithet[:3]
                            if u_pref == p_pref:
                                is_valid_fuzzy = True
                            # Fallback for very short species names (identical match)
                            elif len(u_epithet) <= 3 and u_epithet == p_epithet:
                                is_valid_fuzzy = True
                        else:
                            is_valid_fuzzy = True # Genus-only matches or hybrids
                    
                    if is_valid_fuzzy:
                        match = pfaf_lookup[best_match]
                        match_type = "fuzzy"
                        match_score = score
                    else:
                        match_type = "none"
                        if score >= SPECIES_NEAR_MISS:
                            match_debug.append({"type": "rejected_species_fuzzy", "score": score, "usda_name": original_name, "pfaf_match": pfaf_lookup[best_match]['scientific_name']})
                else: match_type = "none"
            else: match_type = "none"
        else: match_type = "none"

        stats[match_type] += 1
        if match:
            match_debug.append({"type": match_type, "score": match_score, "usda_name": original_name, "pfaf_match": match['scientific_name']})
            pfaf_merged_keys.add(clean_scientific_name(match['scientific_name']).lower())

        consolidated = {
            "scientific_name_primary": original_name,
            "common_name_primary": usda.get('commonName'),
            "usda_traits": usda.get('traits'),
            "pfaf_traits": match.get("traits") if match else None,
            "pfaf_descriptions": match.get("descriptions") if match else None,
            "attributions": [{
                "source": "USDA PLANTS",
                "license": "Public Domain",
                "url": f"https://plants.usda.gov/home/plantProfile?symbol={usda.get('symbol')}",
                "original_scientific_name": original_name
            }]
        }
        if match:
            pfaf_attr = match["attributions"][0].copy()
            if match_type == "hierarchical": pfaf_attr["note"] = f"Inherited from parent species: {match['scientific_name']}"
            elif match_type == "fuzzy": pfaf_attr["note"] = f"Fuzzy match (score: {match_score}) with: {match['scientific_name']}"
            consolidated["attributions"].append(pfaf_attr)
            if not consolidated["common_name_primary"]: consolidated["common_name_primary"] = match.get("common_name")
        merged_results.append(consolidated)

    orphan_count = 0
    for cleaned_name, p in pfaf_lookup.items():
        if cleaned_name not in pfaf_merged_keys:
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
        for r in merged_results: f.write(json.dumps(r) + '\n')
    with open(DEBUG_FILE, 'w', encoding='utf-8') as f:
        json.dump(match_debug, f, indent=2)

    print(f"\n--- Merge Summary ---")
    print(f"Exact: {stats['exact']} | Hierarchical: {stats['hierarchical']} | Fuzzy: {stats['fuzzy']} | No Match: {stats['none']}")
    print(f"Total Joins: {stats['exact'] + stats['hierarchical'] + stats['fuzzy']}")
    print(f"Standalone PFAF: {orphan_count} | Total Records: {len(merged_results)}")

if __name__ == "__main__":
    merge_datasets()
