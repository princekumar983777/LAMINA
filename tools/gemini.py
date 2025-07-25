import os
from dotenv import load_dotenv
import sys
import json
from google import genai
from google.genai import types
from tools.utils.prompt import system_instruction
# from Project.tools.utils.prompt import system_instruction



class Gemini:
    def __init__(self, model="gemini-2.0-flash"):
        load_dotenv()
        GEN_API_KEY = os.getenv("GEN_API_KEY")
        if not GEN_API_KEY:
            print("GEN_API_KEY not found in environment. Please set it in a .env file.")
            sys.exit(1)
        else:
            print("Loaded the Gemini Key ...")
        self.client = genai.Client(api_key=GEN_API_KEY)
        print("Connected to gemini ...")
    
    def query_gemini(self , user_input):
        print("Querying Gemini...")
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_input,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            ),
        )
        # Try to extract JSON from response
        try:
            # Remove markdown if present
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            data = json.loads(text)
        except Exception as e:
            print("Error parsing Gemini response:", e)
            print("Raw response:", response.text)
            data = {"reply": response.text, "task": None, "param": {}}
        return data

# sample uses 
if __name__ == "__main__":
    obj = Gemini()
    data = obj.query_gemini("can you play the song Sahiba on youtube.")
    print(data)

