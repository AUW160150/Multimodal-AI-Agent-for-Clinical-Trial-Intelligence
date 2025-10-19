# src/analyzers/pdf_analyzer.py
"""Extract data from clinical trial PDFs using Gemini Vision"""

import json
from pathlib import Path
from src.utils.gemini_wrapper import get_gemini_model
from config.settings import USE_MOCK_GEMINI, GEMINI_MODEL, PDF_STORAGE_PATH

try:
    from PIL import Image
    import io
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False
    print("⚠️ PIL not available - vision features limited")

class PDFAnalyzer:
    def __init__(self, use_mock=USE_MOCK_GEMINI):
        self.model = get_gemini_model(GEMINI_MODEL, use_mock=use_mock)
        self.use_mock = use_mock
    
    def analyze_survival_curve(self, image_path):
        """
        Extract survival data from Kaplan-Meier curve
        
        Args:
            image_path: Path to survival curve image
        """
        if self.use_mock:
            # Return mock data for development
            return {
                "median_survival_treatment": 24.8,
                "median_survival_control": 11.2,
                "hazard_ratio": 0.42,
                "confidence_interval": "0.31-0.58",
                "p_value": "< 0.0001",
                "analysis": "Treatment shows significant survival benefit over control",
                "data_quality": "High - clear separation of curves"
            }
        
        # Real vision analysis (when not using mock)
        if not VISION_AVAILABLE:
            return {"error": "Vision libraries not available"}
        
        try:
            img = Image.open(image_path)
            
            prompt = """Analyze this Kaplan-Meier survival curve and extract:

1. Median survival time for treatment group (months)
2. Median survival time for control group (months)
3. Hazard ratio (HR)
4. 95% Confidence interval
5. P-value
6. Brief analysis of clinical significance

Provide output in JSON format:
{
  "median_survival_treatment": number,
  "median_survival_control": number,
  "hazard_ratio": number,
  "confidence_interval": "string",
  "p_value": "string",
  "analysis": "string",
  "data_quality": "High/Medium/Low"
}"""
            
            response = self.model.generate_content([prompt, img])
            text = response.text.strip()
            
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0].strip()
            
            return json.loads(text)
            
        except Exception as e:
            print(f"❌ Error analyzing survival curve: {e}")
            return {"error": str(e)}
    
    def analyze_adverse_events_table(self, image_path):
        """
        Extract adverse events data from table
        
        Args:
            image_path: Path to AE table image
        """
        if self.use_mock:
            return {
                "grade_3_plus_treatment": 68,
                "grade_3_plus_control": 42,
                "most_common_ae": "Cytokine release syndrome",
                "most_common_ae_rate": 32,
                "serious_aes": [
                    {"event": "Cytokine release syndrome", "rate": 32},
                    {"event": "Neutropenia", "rate": 24},
                    {"event": "Infection", "rate": 18}
                ],
                "analysis": "Safety profile manageable with standard interventions"
            }
        
        # Real analysis when available
        return {"error": "Real vision analysis - implement when needed"}
    
    def extract_trial_results(self, pdf_path):
        """
        Extract key results from full trial result PDF
        
        Args:
            pdf_path: Path to PDF file
        """
        if self.use_mock:
            return {
                "primary_endpoint_met": True,
                "primary_endpoint": "Overall Survival",
                "primary_result": "HR 0.42 (95% CI: 0.31-0.58), p<0.0001",
                "secondary_endpoints": [
                    {
                        "endpoint": "Progression-Free Survival",
                        "result": "HR 0.35, p<0.0001"
                    },
                    {
                        "endpoint": "Objective Response Rate",
                        "result": "72% vs 45%, p<0.001"
                    }
                ],
                "safety_summary": "Adverse events consistent with known profile",
                "conclusion": "Treatment demonstrates significant clinical benefit"
            }
        
        return {"error": "Full PDF analysis - implement when needed"}