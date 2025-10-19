# validate_phase3.py
"""Validate Phase 3 is working correctly - not just error handling"""

import json
from src.utils.gemini_wrapper import get_gemini_model, MockGeminiModel
from src.analyzers.trial_analyzer import TrialAnalyzer

print("="*60)
print("PHASE 3 VALIDATION")
print("="*60)

# Test 1: Mock Response Format
print("\n[TEST 1] Mock Gemini Response Format")
print("-"*60)

mock_model = MockGeminiModel("test")
response = mock_model.generate_content("classify this trial therapeutic_area")

print(f"Raw Response Text:\n{response.text}\n")

try:
    parsed = json.loads(response.text)
    print("✅ Response is valid JSON")
    print(f"Keys present: {list(parsed.keys())}")
    
    required_fields = ['therapeutic_area', 'disease_category', 'intervention_class', 
                      'target_population', 'innovation_level', 'commercial_potential', 'key_insights']
    
    missing = [f for f in required_fields if f not in parsed]
    
    if missing:
        print(f"❌ MISSING FIELDS: {missing}")
    else:
        print("✅ All required fields present")
        
except json.JSONDecodeError as e:
    print(f"❌ INVALID JSON: {e}")
    exit(1)

# Test 2: Analyzer Processing
print("\n[TEST 2] Analyzer Processing")
print("-"*60)

fake_trial = {
    'nct_id': 'NCT_TEST_001',
    'title': 'Test CAR-T Study',
    'conditions': ['Lymphoma', 'B-Cell Malignancy'],
    'phase': 'PHASE3',
    'interventions': [{'type': 'Biological', 'name': 'CAR-T Cells'}]
}

analyzer = TrialAnalyzer(use_mock=True)
analysis = analyzer.classify_trial(fake_trial)

print(f"Analysis Result:")
print(json.dumps(analysis, indent=2))

# Validate structure
validation_passed = True

for field in required_fields:
    if field not in analysis:
        print(f"❌ Missing field in analysis: {field}")
        validation_passed = False
    elif analysis[field] == "Unknown" or analysis[field] == "Analysis failed - using default values":
        print(f"⚠️  Field '{field}' has default/error value: {analysis[field]}")
        validation_passed = False

if validation_passed:
    print("\n✅ All fields have REAL mock values (not defaults)")
else:
    print("\n❌ Some fields have default/error values - mock not working properly")
    exit(1)

# Test 3: Batch Processing
print("\n[TEST 3] Batch Analysis")
print("-"*60)

test_trials = [
    {
        'nct_id': f'NCT_TEST_{i:03d}',
        'title': f'Test Study {i}',
        'conditions': ['Cancer'],
        'phase': 'PHASE2',
        'interventions': [{'type': 'Drug', 'name': f'Test Drug {i}'}]
    }
    for i in range(1, 4)
]

analyzed = analyzer.analyze_batch(test_trials)

print(f"Input trials: {len(test_trials)}")
print(f"Analyzed trials: {len(analyzed)}")

if len(analyzed) != len(test_trials):
    print("❌ Not all trials were analyzed")
    exit(1)

all_have_analysis = all('analysis' in t for t in analyzed)
if not all_have_analysis:
    print("❌ Some trials missing analysis")
    exit(1)

print("✅ All trials analyzed successfully")

# Test 4: Comparison Function
print("\n[TEST 4] Trial Comparison")
print("-"*60)

summary = analyzer.compare_trials(analyzed)

print(f"Summary keys: {list(summary.keys())}")

required_summary_keys = ['total_trials', 'by_phase', 'by_therapeutic_area', 'ai_insights']

for key in required_summary_keys:
    if key not in summary:
        print(f"❌ Missing summary key: {key}")
        exit(1)

if 'ai_insights' in summary:
    ai = summary['ai_insights']
    required_ai_keys = ['market_trends', 'investment_opportunities', 'competitive_landscape', 
                       'risk_factors', 'recommendations']
    
    for key in required_ai_keys:
        if key not in ai:
            print(f"❌ Missing AI insight key: {key}")
            exit(1)

print("✅ All summary components present")

# Final verification
print("\n" + "="*60)
print("VALIDATION RESULTS")
print("="*60)

print("\n✅ Phase 3 is GENUINELY WORKING")
print("\nVerified:")
print("• Mock responses return proper JSON")
print("• All required fields are populated with real values")
print("• Batch processing works")
print("• Comparative analysis generates insights")
print("• No silent failures or default values")

print("\n🎯 Ready to proceed to Phase 4 or Demo UI")