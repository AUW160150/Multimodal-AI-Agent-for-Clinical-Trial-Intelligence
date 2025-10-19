# test_gemini.py
import google.generativeai as genai
from config.settings import GEMINI_API_KEY
import os

print("Testing Gemini API connection...\n")

# Check if API key exists
if not GEMINI_API_KEY:
    print("❌ ERROR: GEMINI_API_KEY not found in .env file!")
    print("Please add: GEMINI_API_KEY=your_key_here")
    exit(1)

print(f"API Key found: {GEMINI_API_KEY[:20]}...")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# List all available models
print("\n📋 Listing available models...")
try:
    models = genai.list_models()
    available_models = []
    
    for m in models:
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)
            print(f"  ✅ {m.name}")
    
    if not available_models:
        print("❌ No models available for content generation!")
        exit(1)
    
    # Use the first available model
    model_name = available_models[0]
    print(f"\n🎯 Using model: {model_name}")
    
    # Test generation
    model = genai.GenerativeModel(model_name)
    response = model.generate_content("Say 'Gemini is working!' if you can read this.")
    
    print("\n💬 Gemini Response:")
    print(response.text)
    print("\n✅ Gemini API is configured correctly!")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nTroubleshooting:")
    print("1. Check your API key at: https://aistudio.google.com/app/apikey")
    print("2. Make sure the key is valid and active")
    print("3. Check if you have quota/billing enabled")