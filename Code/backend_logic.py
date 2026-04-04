
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

# MOCK DATA (for testing without database)

MOCK_PLANTS = {
    'plant_1': {
        'uuid': 'plant_1',
        'plant_name': 'My Office Pothos',
        'species_id': 'pothos',
        'location': 'Office',
        'image_url': 'images/plant1.jpg',
        'date_added': '2026-03-01'
    },
    'plant_2': {
        'uuid': 'plant_2',
        'plant_name': 'Bedroom Snake Plant',
        'species_id': 'snake_plant',
        'location': 'Bedroom',
        'image_url': 'images/plant2.jpg',
        'date_added': '2026-03-05'
    }
}

MOCK_SPECIES = {
    'pothos': {
        'species_id': 'pothos',
        'common_name': 'Pothos',
        'scientific_name': 'Epipremnum aureum',
        'thresholds': {
            'moisture': {'min': 30, 'max': 70},
            'temperature': {'min': 18, 'max': 26},
            'humidity': {'min': 40, 'max': 60},
            'light': {'min': 200, 'max': 800}
        },
        'care_info': {
            'watering_frequency': 'Every 7-10 days',
            'difficulty': 'Easy'
        }
    },
    'snake_plant': {
        'species_id': 'snake_plant',
        'common_name': 'Snake Plant',
        'scientific_name': 'Sansevieria trifasciata',
        'thresholds': {
            'moisture': {'min': 20, 'max': 50},
            'temperature': {'min': 15, 'max': 30},
            'humidity': {'min': 30, 'max': 70},
            'light': {'min': 100, 'max': 1000}
        },
        'care_info': {
            'watering_frequency': 'Every 2-3 weeks',
            'difficulty': 'Very Easy'
        }
    }
}

MOCK_CURRENT_SENSORS = {
    'plant_1': {
        'moisture': 25,      # LOW
        'temperature': 22,   # OK
        'humidity': 45,      # OK
        'light': 150,        # LOW
        'timestamp': '2026-04-03 19:30:00'
    },
    'plant_2': {
        'moisture': 35,      # OK
        'temperature': 21,   # OK
        'humidity': 50,      # OK
        'light': 300,        # OK
        'timestamp': '2026-04-03 19:30:00'
    }
}

MOCK_HISTORY = {
    'plant_1': [
        {'date': '2026-03-27', 'moisture': 28, 'temperature': 21, 'humidity': 43, 'light': 180, 'timestamp': '2026-03-27 10:00:00'},
        {'date': '2026-03-28', 'moisture': 25, 'temperature': 22, 'humidity': 45, 'light': 195, 'timestamp': '2026-03-28 10:00:00'},
        {'date': '2026-03-29', 'moisture': 23, 'temperature': 22, 'humidity': 44, 'light': 160, 'timestamp': '2026-03-29 10:00:00'},
        {'date': '2026-03-30', 'moisture': 26, 'temperature': 23, 'humidity': 46, 'light': 170, 'timestamp': '2026-03-30 10:00:00'},
        {'date': '2026-03-31', 'moisture': 24, 'temperature': 24, 'humidity': 47, 'light': 155, 'timestamp': '2026-03-31 10:00:00'},
        {'date': '2026-04-01', 'moisture': 22, 'temperature': 24, 'humidity': 48, 'light': 165, 'timestamp': '2026-04-01 10:00:00'},
        {'date': '2026-04-02', 'moisture': 25, 'temperature': 25, 'humidity': 49, 'light': 150, 'timestamp': '2026-04-02 10:00:00'},
    ],
    'plant_2': [
        {'date': '2026-03-27', 'moisture': 35, 'temperature': 20, 'humidity': 50, 'light': 300, 'timestamp': '2026-03-27 10:00:00'},
        {'date': '2026-03-28', 'moisture': 34, 'temperature': 20, 'humidity': 49, 'light': 310, 'timestamp': '2026-03-28 10:00:00'},
        {'date': '2026-03-29', 'moisture': 36, 'temperature': 21, 'humidity': 51, 'light': 295, 'timestamp': '2026-03-29 10:00:00'},
        {'date': '2026-03-30', 'moisture': 35, 'temperature': 21, 'humidity': 50, 'light': 305, 'timestamp': '2026-03-30 10:00:00'},
        {'date': '2026-03-31', 'moisture': 37, 'temperature': 21, 'humidity': 52, 'light': 290, 'timestamp': '2026-03-31 10:00:00'},
        {'date': '2026-04-01', 'moisture': 36, 'temperature': 20, 'humidity': 50, 'light': 300, 'timestamp': '2026-04-01 10:00:00'},
        {'date': '2026-04-02', 'moisture': 35, 'temperature': 21, 'humidity': 50, 'light': 300, 'timestamp': '2026-04-02 10:00:00'},
    ]
}


# CORE MONITORING LOGIC

class PlantMonitor:

    def __init__(self, llm=None, database=None):
        """
        Initialize monitor.

        Args:
            llm: LLM class instance
            database: Database class instance 
        """
        self.llm = llm
        self.db = database
        self.use_mock_db = (database is None)  # Use mock data if no database


    # DATABASE ACCESS LAYER (using mock data, will be integrated later)

    def _get_plant_data(self, plant_id: str) -> Dict:
        """Get plant data from database (for now its mock)"""
        if self.use_mock_db:
            # will be replaced with database call when ready
            return MOCK_PLANTS.get(plant_id)
        else:
            return self.db.get_plant(plant_id)


    def _get_species_data(self, species_id: str) -> Dict:
        """Get species data from database (for now its mock)"""
        if self.use_mock_db:
            # will be replaced with database call when ready
            return MOCK_SPECIES.get(species_id)
        else:
            return self.db.get_species(species_id)

    def _get_current_sensors(self, plant_id: str) -> Dict:
        """Get current sensor readings from database (for now its mock)"""
        if self.use_mock_db:
            return MOCK_CURRENT_SENSORS.get(plant_id)
        else:
            return
            

    def _get_sensor_history(self, plant_id: str, days: int = 7) -> List[Dict]:
        """Get historical sensor data from database (for now its mock)"""
        if self.use_mock_db:
            # will be replaced with database call when ready
            return MOCK_HISTORY.get(plant_id, [])
        else:
            return self.db.get_sensor_history(plant_id, days=days)
        
    
    def _log_sensor_reading(self, plant_id: str, sensors: Dict) -> None:
        """
        Save the current sensor reading to history.

        For now this calls the database method when database is connected.
        While we're still using mock data, this does nothing.
        """
        if self.use_mock_db:
            # will be replaced with database call when ready
            return

        # save_sensor_reading(plant_id, moisture, temperature, humidity, light, timestamp) (this is just a mock method for database.py class)
        self.db.save_sensor_reading(
            plant_id=plant_id,
            moisture=sensors.get("moisture"),
            temperature=sensors.get("temperature"),
            humidity=sensors.get("humidity"),
            light=sensors.get("light"),
            timestamp=sensors.get("timestamp") or datetime.now().isoformat(),
        )


    # 1. THRESHOLD CHECKING ALGORITHM

    def check_thresholds(self, sensors: Dict, species_thresholds: Dict) -> List[Dict]:
        """
        Check if sensor values violate optimal ranges.
        """
        alerts = []

        sensor_names = {
            'moisture': 'Soil Moisture',
            'temperature': 'Temperature',
            'humidity': 'Humidity',
            'light': 'Light Level'
        }

        for sensor, threshold in species_thresholds.items():
            value = sensors.get(sensor, 0)
            name = sensor_names.get(sensor, sensor)

            if value < threshold['min']:
                alerts.append({
                    'type': 'threshold',
                    'severity': 'high' if sensor == 'moisture' else 'medium',
                    'sensor': name,
                    'message': f"{name} is too low ({value})",
                    'current_value': value,
                    'expected_range': f"{threshold['min']}-{threshold['max']}",
                    'action': self._get_action_recommendation(sensor, 'low')
                })

            elif value > threshold['max']:
                alerts.append({
                    'type': 'threshold',
                    'severity': 'high' if sensor == 'moisture' else 'medium',
                    'sensor': name,
                    'message': f"{name} is too high ({value})",
                    'current_value': value,
                    'expected_range': f"{threshold['min']}-{threshold['max']}",
                    'action': self._get_action_recommendation(sensor, 'high')
                })

        return alerts


    def _get_action_recommendation(self, sensor: str, direction: str) -> str:
        """Rule-based action recommendations"""
        actions = {
            'moisture_low': 'Water your plant now',
            'moisture_high': 'Reduce watering frequency and check drainage',
            'temperature_low': 'Move to a warmer location away from drafts',
            'temperature_high': 'Move to a cooler location or increase ventilation',
            'humidity_low': 'Mist leaves daily or use a humidifier nearby',
            'humidity_high': 'Improve air circulation or reduce watering',
            'light_low': 'Move closer to window or add grow light',
            'light_high': 'Move away from direct sunlight or add shading'
        }
        return actions.get(f'{sensor}_{direction}', 'Monitor this reading closely')

    # 2. HEALTH SCORING ALGORITHM

    def calculate_health_score(self, alerts: List[Dict], trends: List[Dict]) -> Tuple[str, int]:
        """
        Calculate overall plant health status and score.
        """
        score = 100

        for alert in alerts:
            if alert['severity'] == 'high':
                score -= 30
            elif alert['severity'] == 'medium':
                score -= 15

        score -= len(trends) * 5
        score = max(0, score)

        if score == 100:
            status = 'healthy'
        elif score >= 80:
            status = 'good'
        elif score >= 60:
            status = 'fair'
        elif score >= 40:
            status = 'needs_attention'
        else:
            status = 'critical'

        return status, score



    # 3. LLM INTEGRATION - Generate Recommendations

    def generate_recommendation(
        self,
        plant_name: str,
        species_name: str,
        sensors: Dict,
        species_thresholds: Dict,
        alerts: List[Dict],
        trends: List[Dict],
        history: Optional[List[Dict]] = None,
        audience_level: str = "beginner",
    ) -> Dict:
        """
        Generate care recommendations using LLM or simple logic.

        LLM integration:
        - We send current sensors, ideal ranges, a textual decision summary,
          and the raw history list so the LLM can analyze trends itself.
        """

        # CASE 1: Everything is fine
        if len(alerts) == 0 and len(trends) == 0:
            return {
                "text": f"Your {species_name} is healthy! All sensor readings are within optimal ranges. Keep up the good care!",
                "priority": "none",
                "source": "system",
            }

        # CASE 2: Single simple problem - use rule (no LLM call needed)
        if len(alerts) == 1 and len(trends) == 0:
            return {
                "text": alerts[0]["action"],
                "priority": alerts[0]["severity"],
                "source": "rule_based",
            }

        # CASE 3: Use LLM for more complex situations
        if self.llm is not None:
            try:
                # Build decision summary for LLM (current issues + any backend trends)
                decision_parts = []
                for alert in alerts:
                    decision_parts.append(f"{alert['message']} - {alert['action']}")
                for trend in trends:
                    decision_parts.append(f"Pattern: {trend['message']}")

                decision_summary = " | ".join(decision_parts) if decision_parts else "Current state was provided."

                # Prepare data in format expected by LLM's generate_explanation method
                llm_data = {
                    "plant": f"{plant_name} ({species_name})",
                    "sensor_values": {
                        "moisture": sensors.get("moisture"),
                        "temperature": sensors.get("temperature"),
                        "humidity": sensors.get("humidity"),
                        "light": sensors.get("light"),
                    },
                    "ideal_ranges": {
                        "moisture": f"{species_thresholds['moisture']['min']}-{species_thresholds['moisture']['max']}%",
                        "temperature": f"{species_thresholds['temperature']['min']}-{species_thresholds['temperature']['max']}°C",
                        "humidity": f"{species_thresholds['humidity']['min']}-{species_thresholds['humidity']['max']}%",
                        "light": f"{species_thresholds['light']['min']}-{species_thresholds['light']['max']} lux",
                    },
                    "decision": decision_summary,
                    "audience_level": audience_level,  # 'beginner', 'intermediate', or 'expert'
                }

                # give the raw history to the LLM so it can analyze trends
                if history is not None:
                    llm_data["history"] = history

                # Call LLM's generate_explanation method
                recommendation_text = self.llm.generate_explanation(llm_data)
                priority = "high" if any(a["severity"] == "high" for a in alerts) else "medium"

                return {
                    "text": recommendation_text,
                    "priority": priority,
                    "source": "llm",
                }

            except Exception as e:
                print(f"LLM error: {e}")
                # Fall through to rule-based fallback

        # CASE 4: Fallback - combine all actions if LLM is unavailable or fails
        actions = [a["action"] for a in alerts]
        recommendation_text = f"Your {species_name} needs attention. " + " ".join(actions)
        
        priority = "high" if any(a["severity"] == "high" for a in alerts) else "medium"

        return {
            "text": recommendation_text,
            "priority": priority,
            "source": "rule_based_fallback",
        }


    # 4. MAIN MONITORING FUNCTION

    def get_plant_status(self, plant_id: str, audience_level: str = "beginner") -> Dict:
        """
        MAIN FUNCTION: Get complete plant health status.

        Args:
            plant_id: UUID of the plant
            audience_level: 'beginner', 'intermediate', or 'expert' (for LLM)

        Returns:
            Complete status dictionary with all monitoring data
        """

        # Step 1: Get plant and species data (using mock or database)
        plant = self._get_plant_data(plant_id)
        if not plant:
            raise ValueError(f"Plant {plant_id} not found")

        species = self._get_species_data(plant["species_id"])

        # Step 2: Get current sensor readings
        sensors = self._get_current_sensors(plant_id)

        # Step 2.5: Log this reading to history (DB later, mock now)
        self._log_sensor_reading(plant_id, sensors)

        # Step 3: Run threshold checking (current problems)
        alerts = self.check_thresholds(sensors, species["thresholds"])

        # Step 4: Fetch history for LLM (no backend trend analysis)
        history = self._get_sensor_history(plant_id, days=7)
        trends: List[Dict] = []  # trend analysis is delegated to the LLM

        # Step 5: Calculate health score (based only on alerts for now)
        health_status, health_score = self.calculate_health_score(alerts, trends)

        # Step 6: Generate recommendation (LLM uses history to find trends)
        recommendation = self.generate_recommendation(
            plant["plant_name"],
            species["common_name"],
            sensors,
            species["thresholds"],
            alerts,
            trends,
            history=history,
            audience_level=audience_level,
        )

        # Step 7: Return complete status
        return {
            "plant_id": plant_id,
            "plant_name": plant["plant_name"],
            "species": species["common_name"],
            "location": plant["location"],
            "timestamp": datetime.now().isoformat(),
            "sensors": sensors,
            "alerts": alerts,
            "trends": trends,  # still here, but empty for now
            "health_status": health_status,
            "health_score": health_score,
            "recommendation": recommendation,
            "alert_count": len(alerts),
            "trend_count": len(trends),
        }


    # HELPER FUNCTIONS

    def get_all_plants(self) -> List[Dict]:
        """Get list of all plants"""
        if self.use_mock_db:
            # will be replaced with database call when ready
            return list(MOCK_PLANTS.values())
        else:
            return self.db.get_all_plants()


    def get_sensor_history(self, plant_id: str, days: int = 7) -> List[Dict]:
        """Get historical sensor data"""
        return self._get_sensor_history(plant_id, days=days)
    
    # any other methods needed for frontend or anything can be added here
