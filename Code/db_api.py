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
    def add_plant(self, user_id, species_id, nickname=""):
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
    def get_all_plants(self, user_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM User_Plant WHERE user_id = ?", (user_id,))

            # Fetch all rows... and convert them into a list of dicts
            return [dict(row) for row in cursor.fetchall()]


    # Fetch a users plant
    def get_plant(self, user_id, plant_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM User_Plant WHERE user_id = ? AND plant_id = ?", 
                           (user_id, plant_id))
            row = cursor.fetchone()

            # Convert the row into a dict
            return dict(row) if row else None

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

    
    # User Queries--------------------------------------------------------------------
    def get_audience_level(self, user_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT audience_level FROM App_User WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            return row['audience_level'] if row else 'beginner'

    # adds the user if they don't exist, updates their level
    def save_audience_level(self, user_id, level):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO App_User (user_id, audience_level)
                VALUES (?, ?)
            ''', (user_id, level))
    
    # LLM Logging---------------------------------------------------------------------
    def save_llm_response(self, plant_id, species_id, audience_level, sensors, species_thresholds, alerts, history, recommendation_text, recommendation_source, timestamp):
        log_id = str(uuid.uuid4())
        if not timestamp:
            timestamp = datetime.utcnow().isoformat()

        # Serialize to a more structured format for storage
        sensors_json = json.dumps(sensors)
        thresholds_json = json.dumps(species_thresholds)
        alerts_json = json.dumps(alerts)
        history_json = json.dumps(history)

        # Dump it
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                           INSERT INTO LLM_Response_Log
                           (log_id, plant_id, species_id, audience_level, sensors, species_thresholds, alerts, history, recommendation_text, recommendation_source, timestamp)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (log_id, plant_id, species_id, audience_level, sensors_json, thresholds_json, alerts_json, history_json, recommendation_text, recommendation_source, timestamp))
    
    def get_llm_responses(self, plant_id, time_start=None, time_end=None):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM LLM_Response_Log WHERE plant_id = ?"
            params = [plant_id]

            # Optional timestamp filtering
            if time_start:
                query += " AND timestamp >= ?"
                params.append(time_start)
            if time_end:
                query += " AND timestamp <= ?"
                params.append(time_end)
            
            # run the query
            query += " ORDER BY timestamp DESC"
            cursor.execute(query, tuple(params))
            results = []
            
            # filter the results
            for row in cursor.fetchall():
                d = dict(row)
                d['sensors'] = json.loads(d['sensors'])
                d['species_thresholds'] = json.loads(d['species_thresholds'])
                d['alerts'] = json.loads(d['alerts'])
                d['history'] = json.loads(d['history'])
                results.append(d)
            
            # pass them back
            return results
                