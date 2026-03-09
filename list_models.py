import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def list_available_models():
    api_key = os.getenv("MARO_GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    print("\n--- Available Models for this API Key ---")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Model: {m.name} | Display Name: {m.display_name}")
    except Exception as e:
        print(f"Error fetching models: {e}")

if __name__ == "__main__":
    list_available_models()
