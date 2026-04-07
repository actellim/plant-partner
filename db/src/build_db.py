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

    # 1. Create the test user
    test_user_id = "test_user"
    cursor.execute("INSERT OR IGNORE INTO App_User (user_id, audience_level) VALUES (?, ?)", (test_user_id, 'beginner'))

    # 2. Find or create species IDs to satisfy Foreign Key constraints
    # Search for pothos
    cursor.execute("SELECT id FROM Consolidated_Plant WHERE scientific_name_primary LIKE '%Epipremnum aureum%' LIMIT 1")
    pothos_row = cursor.fetchone()
    pothos_id = pothos_row[0] if pothos_row else "mock_pothos_id"
    
    if not pothos_row:
        # insert a dummy species if it wasn't found 
        cursor.execute("INSERT OR IGNORE INTO Consolidated_Plant (id, scientific_name_primary, common_name_primary) VALUES (?, ?, ?)", 
                       (pothos_id, "Epipremnum aureum", "Pothos"))

    # Search for Snake Plant
    cursor.execute("SELECT id FROM Consolidated_Plant WHERE scientific_name_primary LIKE '%Sansevieria trifasciata%' OR scientific_name_primary LIKE '%Dracaena trifasciata%' LIMIT 1")
    snake_row = cursor.fetchone()
    snake_id = snake_row[0] if snake_row else "mock_snake_id"
    
    if not snake_row:
        cursor.execute("INSERT OR IGNORE INTO Consolidated_Plant (id, scientific_name_primary, common_name_primary) VALUES (?, ?, ?)", 
                       (snake_id, "Sansevieria trifasciata", "Snake Plant"))

    # 3. Insert the User Plants
    cursor.execute('''
        INSERT OR REPLACE INTO User_Plant (plant_id, user_id, species_id, nickname, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', ('plant_1', test_user_id, pothos_id, 'My Office Pothos', '2026-03-01T00:00:00'))

    cursor.execute('''
        INSERT OR REPLACE INTO User_Plant (plant_id, user_id, species_id, nickname, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', ('plant_2', test_user_id, snake_id, 'Bedroom Snake Plant', '2026-03-05T00:00:00'))

    # 4. Insert Sensor History
    mock_history = [
        # plant_1 (Office Pothos)
        ('plant_1', 28, 21, 43, 180, '2026-03-27T10:00:00'),
        ('plant_1', 25, 22, 45, 195, '2026-03-28T10:00:00'),
        ('plant_1', 23, 22, 44, 160, '2026-03-29T10:00:00'),
        ('plant_1', 26, 23, 46, 170, '2026-03-30T10:00:00'),
        ('plant_1', 24, 24, 47, 155, '2026-03-31T10:00:00'),
        ('plant_1', 22, 24, 48, 165, '2026-04-01T10:00:00'),
        ('plant_1', 25, 25, 49, 150, '2026-04-02T10:00:00'),
        ('plant_1', 25, 22, 45, 150, '2026-04-03T19:30:00'), # Current
        
        # plant_2 (Bedroom Snake Plant)
        ('plant_2', 35, 20, 50, 300, '2026-03-27T10:00:00'),
        ('plant_2', 34, 20, 49, 310, '2026-03-28T10:00:00'),
        ('plant_2', 36, 21, 51, 295, '2026-03-29T10:00:00'),
        ('plant_2', 35, 21, 50, 305, '2026-03-30T10:00:00'),
        ('plant_2', 37, 21, 52, 290, '2026-03-31T10:00:00'),
        ('plant_2', 36, 20, 50, 300, '2026-04-01T10:00:00'),
        ('plant_2', 35, 21, 50, 300, '2026-04-02T10:00:00'),
        ('plant_2', 35, 21, 50, 300, '2026-04-03T19:30:00')  # Current
    ]

    for h in mock_history:
        reading_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT OR REPLACE INTO Sensor_Reading 
            (reading_id, plant_id, moisture, temperature, humidity, light, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (reading_id, h[0], h[1], h[2], h[3], h[4], h[5]))        

    # Commit the inserts
    conn.commit()
    conn.close()
    print("Database built successfully!")

if __name__ == "__main__":
    build_database()