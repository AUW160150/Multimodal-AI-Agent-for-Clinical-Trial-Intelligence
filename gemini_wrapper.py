# src/utils/gemini_wrapper.py
"""Gemini wrapper with mock mode for development"""

import os
from config.settings import GEMINI_API_KEY

class MockGeminiResponse:
    def __init__(self, text):
        self.text = text

class MockGeminiModel:
    def __init__(self, model_name):
        self.model_name = model_name
    
    def generate_content(self, prompt):
        # Mock intelligent responses based on prompt
        if isinstance(prompt, list):
            prompt_text = str(prompt[0]) if prompt else ""
        else:
            prompt_text = str(prompt)
        
        prompt_lower = prompt_text.lower()
        
        # Trial comparison/summary - check FIRST (more specific)
        if any(word in prompt_lower for word in ['summary', 'strategic insights', 'investor', 'market trends', 'investment opportunities']):
            return MockGeminiResponse("""{
  "market_trends": [
    "Rapid expansion of CAR-T therapies beyond hematologic malignancies",
    "Increasing focus on solid tumor applications",
    "Growing number of Phase 3 trials indicating market maturity"
  ],
  "investment_opportunities": [
    "Next-generation CAR-T platforms with improved safety profiles",
    "Combination therapies pairing CAR-T with checkpoint inhibitors",
    "Manufacturing automation to reduce production costs"
  ],
  "competitive_landscape": "The CAR-T market is dominated by established players with 5-6 approved therapies, but significant opportunity exists in underserved indications and improved manufacturing approaches. Clinical trial activity shows 40% YoY growth.",
  "risk_factors": [
    "High manufacturing costs limiting market penetration",
    "Safety concerns around cytokine release syndrome",
    "Reimbursement challenges in certain markets"
  ],
  "recommendations": [
    "Focus on trials targeting solid tumors for differentiation",
    "Monitor manufacturing innovation for cost reduction opportunities",
    "Track real-world evidence for approved CAR-T therapies"
  ]
}""")
        
        # Clinical trial classification - check SECOND
        elif any(word in prompt_lower for word in ['classify', 'therapeutic_area', 'analyze this clinical trial']):
            return MockGeminiResponse("""{
  "therapeutic_area": "Oncology",
  "disease_category": "Hematologic Malignancy",
  "intervention_class": "Biological - CAR-T Cell Therapy",
  "target_population": "Adults with relapsed/refractory B-cell lymphoma",
  "innovation_level": "Novel",
  "commercial_potential": "High",
  "key_insights": [
    "CAR-T therapy represents breakthrough approach for blood cancers",
    "Strong market potential with limited competition in this indication",
    "Phase 3 data suggests significant efficacy improvements over standard care"
  ]
}""")
        
        # Default response
        return MockGeminiResponse(f'{{"analysis": "Mock response for: {prompt_text[:50]}..."}}')

def get_gemini_model(model_name="gemini-2.0-flash", use_mock=True):
    """
    Get Gemini model - mock or real
    
    Args:
        model_name: Gemini model to use
        use_mock: If True, use mock (for development without API quota)
    """
    if use_mock:
        print(f"🔧 Using MOCK Gemini ({model_name})")
        return MockGeminiModel(model_name)
    else:
        print(f"🌐 Using REAL Gemini ({model_name})")
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        return genai.GenerativeModel(model_name)