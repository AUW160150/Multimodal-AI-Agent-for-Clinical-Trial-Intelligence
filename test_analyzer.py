# test_analyzer.py
"""Test Gemini trial analysis"""

import json
from src.scrapers.clinical_trials import ClinicalTrialsScraper
from src.analyzers.trial_analyzer import TrialAnalyzer

print("="*60)
print("PHASE 3: GEMINI-POWERED TRIAL ANALYSIS")
print("="*60)

# Load trials (use existing or fetch new)
try:
    with open('data/raw/cart_trials.json', 'r') as f:
        trials = json.load(f)
    print(f"\n✅ Loaded {len(trials)} trials from cache")
except:
    print("\n⚠️ No cached trials, fetching new...")
    scraper = ClinicalTrialsScraper()
    trials = scraper.search_trials("CAR-T Cell Therapy", max_results=10)
    scraper.save_trials(trials, 'cart_trials.json')

# Initialize analyzer
analyzer = TrialAnalyzer(use_mock=True)  # Using mock for now

# Analyze trials
analyzed_trials = analyzer.analyze_batch(trials[:5])  # Start with 5

# Display results
print("\n" + "="*60)
print("ANALYSIS RESULTS")
print("="*60)

for trial in analyzed_trials[:3]:
    print(f"\n🔬 {trial['title']}")
    print(f"   NCT ID: {trial['nct_id']}")
    print(f"   Phase: {trial['phase']}")
    
    analysis = trial['analysis']
    print(f"\n   📊 ANALYSIS:")
    print(f"   • Therapeutic Area: {analysis['therapeutic_area']}")
    print(f"   • Disease Category: {analysis['disease_category']}")
    print(f"   • Intervention: {analysis['intervention_class']}")
    print(f"   • Innovation Level: {analysis['innovation_level']}")
    print(f"   • Commercial Potential: {analysis['commercial_potential']}")
    
    if analysis.get('key_insights'):
        print(f"   • Key Insights:")
        for insight in analysis['key_insights'][:2]:
            print(f"     - {insight}")
    print()

# Generate comparative analysis
print("\n" + "="*60)
print("COMPARATIVE INTELLIGENCE")
print("="*60)

summary = analyzer.compare_trials(analyzed_trials)

print(f"\n📈 Portfolio Overview:")
print(f"   Total Trials: {summary['total_trials']}")

print(f"\n   By Phase:")
for phase, count in summary['by_phase'].items():
    print(f"   • {phase}: {count}")

print(f"\n   By Therapeutic Area:")
for area, count in summary['by_therapeutic_area'].items():
    print(f"   • {area}: {count}")

if 'ai_insights' in summary:
    ai = summary['ai_insights']
    
    print(f"\n🎯 AI-Generated Insights:")
    
    if ai.get('market_trends'):
        print(f"\n   Market Trends:")
        for trend in ai['market_trends'][:3]:
            print(f"   • {trend}")
    
    if ai.get('investment_opportunities'):
        print(f"\n   Investment Opportunities:")
        for opp in ai['investment_opportunities'][:3]:
            print(f"   • {opp}")
    
    if ai.get('recommendations'):
        print(f"\n   Recommendations:")
        for rec in ai['recommendations'][:3]:
            print(f"   • {rec}")

# Save analyzed data
output_file = 'data/processed/analyzed_trials.json'
with open(output_file, 'w') as f:
    json.dump({
        'trials': analyzed_trials,
        'summary': summary
    }, f, indent=2)

print(f"\n💾 Saved analysis to {output_file}")
print("\n✅ Phase 3 Complete!")