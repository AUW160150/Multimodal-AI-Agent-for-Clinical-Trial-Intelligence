# src/scrapers/clinical_trials.py
"""Fetch clinical trial data from ClinicalTrials.gov"""

import requests
import json
from tqdm import tqdm
from config.settings import CLINICAL_TRIALS_BASE_URL, MAX_TRIALS_TO_FETCH

class ClinicalTrialsScraper:
    def __init__(self):
        self.base_url = CLINICAL_TRIALS_BASE_URL
    
    def search_trials(self, condition, max_results=20):
        """
        Search for clinical trials by condition
        
        Args:
            condition: Disease/condition to search for
            max_results: Maximum number of trials to return
        """
        print(f"\n🔍 Searching for trials: {condition}")
        
        params = {
            'query.cond': condition,
            'filter.overallStatus': 'RECRUITING|ACTIVE_NOT_RECRUITING|COMPLETED',
            'pageSize': min(max_results, 100),
            'format': 'json'
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            studies = data.get('studies', [])
            print(f"✅ Found {len(studies)} trials")
            
            return self._parse_studies(studies[:max_results])
            
        except Exception as e:
            print(f"❌ Error fetching trials: {e}")
            return []
    
    def _parse_studies(self, studies):
        """Parse study data into clean format"""
        parsed = []
        
        for study in tqdm(studies, desc="Parsing trials"):
            try:
                protocol = study.get('protocolSection', {})
                id_module = protocol.get('identificationModule', {})
                status_module = protocol.get('statusModule', {})
                design_module = protocol.get('designModule', {})
                conditions_module = protocol.get('conditionsModule', {})
                interventions_module = protocol.get('armsInterventionsModule', {})
                
                trial_data = {
                    'nct_id': id_module.get('nctId', 'Unknown'),
                    'title': id_module.get('briefTitle', 'No title'),
                    'official_title': id_module.get('officialTitle', ''),
                    'status': status_module.get('overallStatus', 'Unknown'),
                    'phase': design_module.get('phases', ['N/A'])[0] if design_module.get('phases') else 'N/A',
                    'conditions': conditions_module.get('conditions', []),
                    'interventions': [
                        {
                            'type': i.get('type', 'Unknown'),
                            'name': i.get('name', 'Unknown')
                        }
                        for i in interventions_module.get('interventions', [])
                    ],
                    'enrollment': design_module.get('enrollmentInfo', {}).get('count', 'Unknown'),
                    'start_date': status_module.get('startDateStruct', {}).get('date', 'Unknown'),
                    'completion_date': status_module.get('completionDateStruct', {}).get('date', 'Unknown'),
                    'url': f"https://clinicaltrials.gov/study/{id_module.get('nctId', '')}"
                }
                
                parsed.append(trial_data)
                
            except Exception as e:
                print(f"⚠️ Error parsing study: {e}")
                continue
        
        return parsed
    
    def save_trials(self, trials, filename):
        """Save trials to JSON file"""
        filepath = f"data/raw/{filename}"
        with open(filepath, 'w') as f:
            json.dump(trials, f, indent=2)
        print(f"💾 Saved {len(trials)} trials to {filepath}")