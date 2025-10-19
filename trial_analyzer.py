# src/analyzers/trial_analyzer.py
"""Analyze clinical trials using Gemini"""

import json
from src.utils.gemini_wrapper import get_gemini_model
from config.settings import USE_MOCK_GEMINI, GEMINI_MODEL
from tqdm import tqdm

class TrialAnalyzer:
    def __init__(self, use_mock=USE_MOCK_GEMINI):
        self.model = get_gemini_model(GEMINI_MODEL, use_mock=use_mock)
        self.use_mock = use_mock
    
    def classify_trial(self, trial):
        """
        Classify trial by therapeutic area and extract key info
        
        Args:
            trial: Trial data dict
        """
        prompt = f"""Analyze this clinical trial and provide a structured classification:

Title: {trial['title']}
Conditions: {', '.join(trial['conditions'])}
Phase: {trial['phase']}
Interventions: {json.dumps(trial['interventions'], indent=2)}

Provide output in JSON format:
{{
  "therapeutic_area": "Oncology/Cardiology/Neurology/etc",
  "disease_category": "specific disease type",
  "intervention_class": "Drug/Device/Biological/etc",
  "target_population": "description",
  "innovation_level": "Novel/Incremental/Standard",
  "commercial_potential": "High/Medium/Low",
  "key_insights": ["insight1", "insight2", "insight3"]
}}"""
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Extract JSON if wrapped in markdown
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0].strip()
            elif '```' in text:
                text = text.split('```')[1].split('```')[0].strip()
            
            analysis = json.loads(text)
            
            # Validate required fields
            required_fields = ['therapeutic_area', 'disease_category', 'intervention_class', 
                             'target_population', 'innovation_level', 'commercial_potential']
            
            for field in required_fields:
                if field not in analysis:
                    analysis[field] = "Unknown"
            
            if 'key_insights' not in analysis:
                analysis['key_insights'] = []
            
            return analysis
            
        except Exception as e:
            print(f"⚠️ Error analyzing trial {trial.get('nct_id', 'Unknown')}: {e}")
            print(f"   Response was: {response.text if 'response' in locals() else 'No response'}")
            
            # Return safe default structure
            return {
                "therapeutic_area": ', '.join(trial['conditions'][:1]) if trial.get('conditions') else "Unknown",
                "disease_category": ', '.join(trial['conditions']) if trial.get('conditions') else "Unknown",
                "intervention_class": trial['interventions'][0]['type'] if trial.get('interventions') else "Unknown",
                "target_population": "Analysis failed - using default values",
                "innovation_level": "Unknown",
                "commercial_potential": "Unknown",
                "key_insights": []
            }
    
    def compare_trials(self, trials):
        """
        Compare multiple trials and generate insights
        
        Args:
            trials: List of trial dicts with analysis
        """
        # Create summary
        summary = {
            'total_trials': len(trials),
            'by_phase': {},
            'by_therapeutic_area': {},
            'by_innovation_level': {},
            'top_insights': []
        }
        
        for trial in trials:
            analysis = trial.get('analysis', {})
            
            # Count by phase
            phase = trial['phase']
            summary['by_phase'][phase] = summary['by_phase'].get(phase, 0) + 1
            
            # Count by therapeutic area
            area = analysis.get('therapeutic_area', 'Unknown')
            summary['by_therapeutic_area'][area] = summary['by_therapeutic_area'].get(area, 0) + 1
            
            # Count by innovation
            innovation = analysis.get('innovation_level', 'Unknown')
            summary['by_innovation_level'][innovation] = summary['by_innovation_level'].get(innovation, 0) + 1
            
            # Collect insights
            insights = analysis.get('key_insights', [])
            summary['top_insights'].extend(insights)
        
        # Generate AI summary
        prompt = f"""Based on this clinical trial data summary, provide strategic insights for pharma investors:

{json.dumps(summary, indent=2)}

Provide 3-5 actionable insights about:
- Market trends
- Investment opportunities
- Competitive landscape
- Risk factors

Format as JSON:
{{
  "market_trends": ["trend1", "trend2"],
  "investment_opportunities": ["opp1", "opp2"],
  "competitive_landscape": "summary",
  "risk_factors": ["risk1", "risk2"],
  "recommendations": ["rec1", "rec2"]
}}"""
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Debug print
            if self.use_mock:
                print(f"\n[DEBUG] Raw AI summary response:\n{text[:200]}...\n")
            
            # Extract JSON if wrapped in markdown
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0].strip()
            elif '```' in text:
                text = text.split('```')[1].split('```')[0].strip()
            
            ai_insights = json.loads(text)
            
            # Validate all required keys exist
            required_keys = ['market_trends', 'investment_opportunities', 'competitive_landscape', 
                           'risk_factors', 'recommendations']
            
            for key in required_keys:
                if key not in ai_insights:
                    print(f"⚠️ Missing key in AI insights: {key}")
                    ai_insights[key] = [] if key != 'competitive_landscape' else "Not available"
            
            summary['ai_insights'] = ai_insights
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error in AI insights: {e}")
            print(f"   Attempted to parse: {text[:200] if 'text' in locals() else 'No text'}")
            summary['ai_insights'] = {
                "market_trends": ["Analysis pending - JSON parse error"],
                "investment_opportunities": ["Analysis pending"],
                "competitive_landscape": "Analysis pending",
                "risk_factors": ["Analysis pending"],
                "recommendations": ["Analysis pending"]
            }
        except Exception as e:
            print(f"❌ Error generating summary insights: {e}")
            import traceback
            traceback.print_exc()
            summary['ai_insights'] = {
                "market_trends": ["Analysis pending - error"],
                "investment_opportunities": ["Analysis pending"],
                "competitive_landscape": "Analysis pending",
                "risk_factors": ["Analysis pending"],
                "recommendations": ["Analysis pending"]
            }
        
        return summary
    
    def analyze_batch(self, trials):
        """
        Analyze multiple trials
        
        Args:
            trials: List of trial dicts
        """
        print(f"\n🧠 Analyzing {len(trials)} trials with Gemini...")
        
        analyzed_trials = []
        
        for trial in tqdm(trials, desc="Analyzing"):
            trial_copy = trial.copy()
            trial_copy['analysis'] = self.classify_trial(trial)
            analyzed_trials.append(trial_copy)
        
        return analyzed_trials