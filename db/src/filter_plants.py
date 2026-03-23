import json
import os

INPUT_FILE = 'merged_plants.jsonl'
OUTPUT_FILE = 'merged_plants_optimized.jsonl'

def has_data(record):
    usda = record.get('usda_traits') or {}
    pfaf = record.get('pfaf_traits') or {}
    
    # Check Moisture (USDA or PFAF)
    has_moisture = (
        usda.get('moistureUse') is not None or 
        usda.get('precipitationMin') is not None or 
        usda.get('precipitationMax') is not None or
        (pfaf.get('moisture') is not None and pfaf.get('moisture') != "")
    )
    
    # Check Temperature (USDA or PFAF)
    has_temp = (
        usda.get('minTempF') is not None or 
        (pfaf.get('hardiness_zone') is not None and pfaf.get('hardiness_zone') != "")
    )
    
    # Check Light (USDA or PFAF)
    has_light = (
        usda.get('shadeTolerance') is not None or 
        (pfaf.get('shade') is not None and pfaf.get('shade') != "")
    )
                
    # MUST HAVE ALL THREE
    return has_moisture and has_temp and has_light

def filter_records():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    count_before = 0
    count_after = 0
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as f_in, \
         open(OUTPUT_FILE, 'w', encoding='utf-8') as f_out:
        
        for line in f_in:
            if not line.strip():
                continue
            count_before += 1
            record = json.loads(line)
            
            if has_data(record):
                f_out.write(json.dumps(record) + '\n')
                count_after += 1
                
    print(f"Filtering complete (Strict AND criteria).")
    print(f"Records before: {count_before}")
    print(f"Records after:  {count_after}")
    print(f"Removed:        {count_before - count_after}")
    print(f"Optimized version saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    filter_records()
