import sqlite3
import json
import os

DB_PATH = 'pfaf_full_repo/data.sqlite'
OUTPUT_FILE = 'pfaf_data.jsonl'

def extract_pfaf():
    if not os.path.exists(DB_PATH):
        print(f"Error: {DB_PATH} not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Fetching PFAF plants...")
    # Get all columns from plants table
    cursor.execute("PRAGMA table_info(plants)")
    columns = [row[1] for row in cursor.fetchall()]
    
    cursor.execute("SELECT * FROM plants")
    plants = cursor.fetchall()

    print(f"Processing {len(plants)} plants...")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for p in plants:
            plant_dict = dict(zip(columns, p))
            latin_name = plant_dict['latin_name']
            
            # Fetch care requirements from join table
            cursor.execute("""
                SELECT care FROM plant_care 
                WHERE plant = ?
            """, (latin_name,))
            care_reqs = [row[0] for row in cursor.fetchall()]
            
            # Structure for merged output
            record = {
                "scientific_name": latin_name,
                "common_name": plant_dict.get('common_name'),
                "family": plant_dict.get('family'),
                "traits": {
                    "hardiness_zone": plant_dict.get('hardiness'),
                    "moisture": plant_dict.get('moisture'),
                    "shade": plant_dict.get('shade'),
                    "growth_rate": plant_dict.get('growth'),
                    "care_requirements": care_reqs
                },
                "descriptions": {
                    "summary": plant_dict.get('summary'),
                    "habitats": plant_dict.get('habitats'),
                    "cultivation": plant_dict.get('cultivation_details'),
                    "edible_uses": plant_dict.get('edible_uses'),
                    "medicinal_uses": plant_dict.get('medicinal_uses')
                },
                "attributions": [
                    {
                        "source": "PFAF (Plants For A Future)",
                        "license": "CC-BY 4.0",
                        "url": f"https://pfaf.org/user/Plant.aspx?LatinName={latin_name.replace(' ', '+')}",
                        "original_name": latin_name
                    }
                ]
            }
            
            f.write(json.dumps(record) + '\n')

    conn.close()
    print(f"Successfully extracted {len(plants)} records to {OUTPUT_FILE}")

if __name__ == "__main__":
    extract_pfaf()
