import google.generativeai as genai

def list_available_models():
    api_key = "AIzaSyCLSNHpSFgjeeeEci4Muo73og58q6VThL4"
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
