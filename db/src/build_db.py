import sqlite3
import json
import uuid

# Connect to sqlite3
# Will create the db if it doesn't exist
def build_database():
    conn = sqlite3.connect('db/plant_partner.sqlite')
    cursor = conn.cursor()

    # Species Database
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Consolidated_Plant (
        id TEXT PRIMARY KEY,
        scientific_name_primary TEXT,
        common_name_primary TEXT,
        usda_traits TEXT,
        pfaf_traits TEXT,
        pfaf_descriptions TEXT,
        attributions TEXT
        )
    ''')
    
    # Users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS App_User (
            user_id TEXT PRIMARY KEY,
            audience_level TEXT DEFAULT 'beginner'
        )
    ''')
    
    # User Plants
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS User_Plant(
        plant_id TEXT PRIMARY KEY,
        user_id TEXT,
        species_id TEXT,
        nickname TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES App_User(user_id),
        FOREIGN KEY(species_id) REFERENCES Consolidated_Plant(id)
        )
    ''')

    # Sensor Readings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sensor_Reading(
            reading_id TEXT PRIMARY KEY,
            plant_id TEXT,
            moisture REAL,
            temperature REAL,
            humidity REAL,
            light REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(plant_id) REFERENCES User_Plant(plant_id)
            )
        ''')
    
    # LLM Logging
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS LLM_Response_Log (
            log_id TEXT PRIMARY KEY,
            plant_id TEXT,
            species_id TEXT,
            audience_level TEXT,
            sensors TEXT,
            species_thresholds TEXT,
            alerts TEXT,
            history TEXT,
            recommendation_text TEXT,
            recommendation_source TEXT,
            timestamp DATETIME,
            FOREIGN KEY(plant_id) REFERENCES User_Plant(plant_id),
            FOREIGN KEY(species_id) REFERENCES Consolidated_Plant(id) 
        ) 
    ''')

    conn.commit()

    # Parse the json lines and insert them
    file_path = 'db/artifact_archive/merged_plants.jsonl'
    
    with open(file_path, 'r', encoding='utf-8') as jsonldb:
        for line in jsonldb:
            if not line.strip(): continue

            plant = json.loads(line)

            # Generate UUID
            species_id = str(uuid.uuid4())
            sci_name = plant.get('scientific_name_primary')
            com_name = plant.get('common_name_primary')

            # Serialize to json strings and handle empty cases
            usda_traits = json.dumps(plant.get('usda_traits') or {})
            pfaf_traits = json.dumps(plant.get('pfaf_traits') or {})
            pfaf_descriptions = json.dumps(plant.get('pfaf_descriptions') or {})
            attributions = json.dumps(plant.get('attributions') or [])

            # Insert the data into the DB
            cursor.execute('''
                INSERT INTO Consolidated_Plant
                (id, scientific_name_primary, common_name_primary,
                 usda_traits, pfaf_traits, pfaf_descriptions, attributions)
                 values (?, ?, ?, ?, ?, ?, ?)
            ''', (species_id, sci_name, com_name, usda_traits, pfaf_traits, pfaf_descriptions, attributions))
        
    # Commit the inserts
    conn.commit()
    conn.close()
    print("Database built successfully!")

if __name__ == "__main__":
    build_database()