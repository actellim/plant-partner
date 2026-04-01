from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()


class OpenRouterExplainer:
    def __init__(self):
        # Connect to OpenRouter using your OpenRouter API key
        # OpenRouter works with the OpenAI SDK if you change the base URL
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"]
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
        plant = data.get("plant", "Unknown Plant")
        sensor_values = data.get("sensor_values", {})
        ideal_ranges = data.get("ideal_ranges", {})
        decision = data.get("decision", "No decision was provided.")
        audience_level = data.get("audience_level", "beginner")

        audience_instruction = self._get_audience_instruction(audience_level)

        prompt = f"""
You are a plant-care assistant.

Plant: {plant}
Current sensor values: {sensor_values}
Ideal ranges: {ideal_ranges}
Backend decision: {decision}

Rules:
- Do not make a new decision.
- Only explain the backend decision.
- Keep the explanation accurate and based only on the provided data.
- Keep the tone calm, professional, and helpful.
- Give a practical recommendation if appropriate.
- Avoid exaggerated wording.

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
        
            return response.choices[0].message.content.strip()

        # If anything goes wrong with OpenRouter, catch the error and return a simple backend decision explanation instead of crashing
        except Exception as e:
            print("OpenRouter ERROR:", e)
            return self.fallback(data)
