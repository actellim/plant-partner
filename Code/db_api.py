import sqlite3
import json
import uuid                
from datetime import datetime


class PlantDatabase:
    def __init__(self, db_path='db/plant_partner.sqlite'):
        self.db_path = db_path

    # Create a connection and set up the factory
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    
    # Species Queries----------------------------------------------------------------
    def get_species(self, species_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Consolidated_Plant WHERE id = ?", 
                           (species_id,))
            row = cursor.fetchone()

            # Convert the row into a dict
            if row:
                species = dict(row)
                species['usda_traits'] = json.loads(species['usda_traits'])
                species['pfaf_traits'] = json.loads(species['pfaf_traits'])
                species['pfaf_descriptions'] = json.loads(species['pfaf_descriptions'])
                species['attributions'] = json.loads(species['attributions'])
                return species
            return None


    # Plant Queries-------------------------------------------------------------------
    # Let users add their own plants
    def add_plant(self, species_id, nickname=""):
        plant_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO User_Plant (plant_id, species_id, nickname, created_at)
                VALUES (?, ?, ?, ?)
            ''', (plant_id, species_id, nickname, created_at))
            # return the plant_id that was just created.
            return plant_id


    # Get all the user's plants
    def get_all_plants(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM User_Plant")

            # Fetch all rows... and convert them into a list of dicts
            return [dict(row) for row in cursor.fetchall()]


    # Fetch a users plant
    def get_plant(self, plant_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM User_Plant WHERE plant_id = ?", 
                           (plant_id,))
            row = cursor.fetchone()

            # Convert the row into a dict
            if row:
                return dict(row)
            return None
    

    # Update a users plant
    def update_plant(self, plant_id, nickname):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE User_Plant
                SET nickname = ?
                WHERE plant_id = ?
            ''', (nickname, plant_id))
    

    # Delete for full CRUD of user plants
    def delete_plant(self, plant_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # remove associated sensor readings
            cursor.execute("DELETE FROM Sensor_Reading WHERE plant_id = ?", (plant_id, ))

            # delete the plant
            cursor.execute("DELETE FROM User_Plant WHERE plant_id = ?", (plant_id,))
    
    

    # Sensor Queries------------------------------------------------------------------
    # Save a sensor reading
    def save_sensor_reading(self, plant_id, moisture, temperature, humidity, light, 
                            timestamp = None):
        reading_id = str(uuid.uuid4())
        if not timestamp:
            timestamp = datetime.utcnow().isoformat()

        # with auto commits here, don't call the commit method manually
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Sensor_Reading
                (reading_id, plant_id, moisture, temperature, humidity, light, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', 
            (reading_id, plant_id, moisture, temperature, humidity, light, timestamp))
    
    # Get the most recent sensor reading
    def get_current_sensor_data(self, plant_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM Sensor_Reading
                WHERE plant_id = ?
                ORDER BY timestamp DESC
                LIMIT 1
            ''', (plant_id, ))
            
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
    

    # Fetches history for the last days days
    def get_sensor_history(self, plant_id, days):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Utilize sqlite datetime modifiers
            cursor.execute('''
                SELECT * FROM Sensor_Reading
                WHERE plant_id = ?
                AND timestamp >= datetime('now', ?)
                ORDER BY timestamp ASC
            ''', (plant_id, f'-{days} days'))
            
            # Convert them to dicts
            return [dict(row) for row in cursor.fetchall()]

    

    
    
    

