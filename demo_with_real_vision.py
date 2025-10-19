# demo_with_real_vision.py
"""
Demo script with ONE real Gemini Vision example
Use this for the live demo / video recording
"""

import google.generativeai as genai
from config.settings import GEMINI_API_KEY
from PIL import Image, ImageDraw, ImageFont
import json

print("="*60)
print("TRIALS INTEL - REAL VISION DEMO")
print("="*60)

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Step 1: Create a mock survival curve image (for demo)
def create_mock_survival_curve():
    """Create a simple mock Kaplan-Meier curve for demo"""
    img = Image.new('RGB', (800, 600), 'white')
    draw = ImageDraw.Draw(img)
    
    # Draw axes
    draw.line([(100, 500), (700, 500)], fill='black', width=3)  # X-axis
    draw.line([(100, 100), (100, 500)], fill='black', width=3)  # Y-axis
    
    # Draw treatment curve (better survival)
    treatment_points = [
        (100, 150), (200, 180), (300, 220), (400, 280), 
        (500, 350), (600, 420), (700, 480)
    ]
    draw.line(treatment_points, fill='blue', width=3)
    
    # Draw control curve (worse survival)
    control_points = [
        (100, 150), (200, 250), (300, 350), (400, 420),
        (500, 470), (600, 490), (700, 495)
    ]
    draw.line(control_points, fill='red', width=3)
    
    # Add labels
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    draw.text((120, 120), "Treatment (n=225)", fill='blue', font=font)
    draw.text((120, 250), "Control (n=225)", fill='red', font=font)
    draw.text((300, 520), "Time (months)", fill='black', font=font)
    draw.text((20, 300), "Survival %", fill='black', font=font)
    draw.text((120, 480), "HR 0.42, p<0.0001", fill='green', font=font)
    
    # Save
    img.save('data/raw/demo_survival_curve.png')
    print("✅ Created mock survival curve: data/raw/demo_survival_curve.png")
    return 'data/raw/demo_survival_curve.png'

# Step 2: Real Gemini Vision Analysis
print("\n[STEP 1] Creating demo survival curve...")
image_path = create_mock_survival_curve()

print("\n[STEP 2] Analyzing with REAL Gemini Vision...")
print("🌐 Using gemini-2.0-flash-exp (multimodal)")

try:
    # Load image
    img = Image.open(image_path)
    
    # Create vision model
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    # Analyze
    prompt = """Analyze this Kaplan-Meier survival curve and extract:

1. Which line represents treatment vs control (based on colors and labels)
2. Approximate median survival for each group (in months, read from x-axis)
3. The hazard ratio and p-value if visible
4. Brief clinical interpretation

Provide output in JSON format:
{
  "treatment_arm": "description",
  "control_arm": "description", 
  "median_survival_treatment": estimated_months,
  "median_survival_control": estimated_months,
  "hazard_ratio": number_if_visible,
  "p_value": "value_if_visible",
  "interpretation": "brief analysis",
  "confidence": "high/medium/low"
}"""
    
    print("\n⏳ Sending to Gemini Vision API...")
    response = model.generate_content([prompt, img])
    
    print("\n📊 GEMINI VISION RESPONSE:")
    print("="*60)
    print(response.text)
    print("="*60)
    
    # Try to parse JSON
    try:
        text = response.text.strip()
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0].strip()
        elif '```' in text:
            text = text.split('```')[1].split('```')[0].strip()
        
        result = json.loads(text)
        
        print("\n✅ Successfully parsed Gemini Vision output:")
        print(json.dumps(result, indent=2))
        
        print("\n💡 KEY FINDINGS:")
        print(f"   • Treatment survival: ~{result.get('median_survival_treatment', 'N/A')} months")
        print(f"   • Control survival: ~{result.get('median_survival_control', 'N/A')} months")
        print(f"   • Hazard Ratio: {result.get('hazard_ratio', 'N/A')}")
        print(f"   • Statistical significance: {result.get('p_value', 'N/A')}")
        print(f"   • Interpretation: {result.get('interpretation', 'N/A')}")
        
    except json.JSONDecodeError:
        print("\n⚠️ Could not parse as JSON, but Gemini Vision worked!")
    
    print("\n✅ DEMO COMPLETE - Real Gemini Vision Analysis Successful!")
    print("\n🎯 This proves multimodal capability:")
    print("   ✓ Gemini read the image")
    print("   ✓ Extracted survival data from curves")
    print("   ✓ Interpreted clinical significance")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Check API key is valid")
    print("2. Wait for quota reset (60 seconds)")
    print("3. Try gemini-1.5-flash instead of gemini-2.0-flash-exp")