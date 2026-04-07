from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent / ".env")
# Load API key from .env file
# load_dotenv()


class OpenRouterExplainer:
    def __init__(self):
        # Connect to OpenRouter using your OpenRouter API key
        # OpenRouter works with the OpenAI SDK if you change the base URL
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
        )

    def _get_audience_instruction(self, level: str) -> str:
        # Clean the input
        level = level.lower().strip()

        # Control how the explanation should sound depending on the audience level
        if level == "beginner":
            return (
                "Explain in very simple, friendly, easy-to-understand words. "
                "Avoid technical terms. Keep it short and clear."
            )
        elif level == "intermediate":
            return (
                "Explain clearly with some detail, assuming the user has basic plant care knowledge."
            )
        elif level == "expert":
            return (
                "Explain using more precise and technical language suitable for an experienced user."
            )
        else:
            return "Explain clearly and simply for a general user."

    def fallback(self, data: dict) -> str:
        # This runs if OpenRouter fails for any reason. Basically just returns the backend decision in a simple format
        plant = data.get("plant", "This plant")
        decision = data.get("decision", "Plant care adjustment may be needed.")
        level = data.get("audience_level", "beginner").lower().strip()
        
        if level == "beginner":
            return f"{plant}: {decision}"
        elif level == "intermediate":
            return f"{plant}: Based on current conditions, {decision}"
        elif level == "expert":
            return f"{plant}: The current readings indicate the following condition: {decision}"
        else:
            return f"{plant}: {decision}"

    # This is the main function the backend will call to get an explanation for the plant care decision
    def generate_explanation(self, data: dict) -> str:
        # Example sample input data:
        # {
        #   "plant": "Kenny's Plant",
        #   "sensor_values": {
        #       "moisture": 25,
        #       "temperature": 22,
        #       "humidity": 45,
        #       "light": 150
        #   },
        #   "ideal_ranges": {
        #       "moisture": "30-70%",
        #       "temperature": "18-26°C",
        #       "humidity": "40-60%",
        #       "light": "200-800 lux"
        #   },
        #   "decision": "Soil Moisture is too low Water your plant now!",
        #   "audience_level": "beginner",
        #   "history": [
        #       {
        #           "date": "2026-03-27",
        #           "moisture": 28,
        #           "temperature": 21,
        #           "humidity": 43,
        #           "light": 180,
        #           "timestamp": "2026-03-27 10:00:00"
        #       },
        #       ...
        #   ]
        # }

        # Get the current plant name from the backend data
        plant = data.get("plant", "Unknown Plant")

        # Get the current sensor readings
        sensor_values = data.get("sensor_values", {})

        # Get the ideal/expected ranges for this plant
        ideal_ranges = data.get("ideal_ranges", {})

        # Get the final backend decision that we want the LLM to explain
        decision = data.get("decision", "No decision was provided.")

        # Get the user level so the explanation can be adjusted
        audience_level = data.get("audience_level", "beginner")

        # Get the plant's past sensor history from the backend
        history = data.get("history", [])

        # Get the explanation style based on audience level
        audience_instruction = self._get_audience_instruction(audience_level)

        # If history exists, pass it to the prompt
        # no history exists use a simple message instead
        history_text = history if history else "No history data provided."

        # Build the prompt sent to OpenRouter
        prompt = f"""
You are a plant-care assistant.

Plant: {plant}
Current sensor values: {sensor_values}
Ideal ranges: {ideal_ranges}
Backend decision: {decision}
Sensor history: {history_text}

Rules:
- Do not make a new decision.
- Only explain the backend decision.
- Use the history only to mention simple trends if helpful.
- Keep the explanation accurate and based only on the provided data.
- Keep the tone calm, professional, and clear.
- Give a direct practical recommendation if appropriate.
- Avoid exaggerated wording.
- Do not use greeting sentences.
- Do not use conversational filler.
- Do not ask the user any questions.
- Keep beginner responses to 2–3 short, simple sentences.
- Keep intermediate responses concise (5–6 sentences max).
- Keep expert responses concise and slightly more technical (7–8 sentences max).

Audience instruction:
{audience_instruction}
"""

        try:
            # Send request to OpenRouter
            response = self.client.chat.completions.create(
                model="meta-llama/llama-3-8b-instruct",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                extra_headers={
                    "HTTP-Referer": "http://localhost",
                    "X-Title": "Plant Partner Project"
                }
            )

            # Return only the explanation text from the model response
            return response.choices[0].message.content.strip()

        # If anything goes wrong with OpenRouter, catch the error and return a simple backend decision explanation instead of crashing
        except Exception as e:
            print("OpenRouter ERROR:", e)
            return self.fallback(data)