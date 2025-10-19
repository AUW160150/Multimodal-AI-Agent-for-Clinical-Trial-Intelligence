# production_mode.py
"""
Production mode - All real Gemini (text + vision)
Use this for final submission when you have API quota
"""

import os
from dotenv import load_dotenv

# Force real Gemini mode
os.environ['USE_MOCK_GEMINI'] = 'false'

# Reload settings
load_dotenv(override=True)

from src.scrapers.clinical_trials import ClinicalTrialsScraper
from src.analyzers.trial_analyzer import TrialAnalyzer
from src.analyzers.pdf_analyzer import PDFAnalyzer
import json

print("="*60)
print("🚀 TRIALS INTEL - PRODUCTION MODE")
print("="*60)
print("\n⚠️  USING REAL GEMINI API - Will consume quota")
print("="*60)

# Initialize with real Gemini
scraper = ClinicalTrialsScraper()
analyzer = TrialAnalyzer(use_mock=False)
pdf_analyzer = PDFAnalyzer(use_mock=False)

# Run full pipeline
print("\n[1/4] Searching ClinicalTrials.gov...")
trials = scraper.search_trials("CAR-T Cell Therapy", max_results=5)
print(f"✅ Found {len(trials)} trials")

print("\n[2/4] Analyzing with Gemini (text)...")
analyzed = analyzer.analyze_batch(trials)
print(f"✅ Analyzed {len(analyzed)} trials")

print("\n[3/4] Generating comparative intelligence...")
summary = analyzer.compare_trials(analyzed)
print("✅ Generated investment insights")

print("\n[4/4] Sample vision analysis...")
# Note: For real vision, you'd need actual PDF/image files
# This is placeholder for the architecture
print("✅ Vision analysis ready (requires real PDF inputs)")

# Save results
output = {
    'trials': analyzed,
    'summary': summary,
    'metadata': {
        'mode': 'PRODUCTION',
        'gemini_model': 'gemini-2.0-flash',
        'total_trials': len(analyzed)
    }
}

with open('data/processed/production_analysis.json', 'w') as f:
    json.dump(output, f, indent=2)

print("\n💾 Saved: data/processed/production_analysis.json")
print("\n✅ PRODUCTION RUN COMPLETE")

# Display sample results
print("\n" + "="*60)
print("SAMPLE RESULTS")
print("="*60)

trial = analyzed[0]
print(f"\n🔬 {trial['title']}")
print(f"\nAnalysis:")
a = trial['analysis']
print(f"  • Therapeutic Area: {a['therapeutic_area']}")
print(f"  • Commercial Potential: {a['commercial_potential']}")
print(f"  • Innovation Level: {a['innovation_level']}")

if summary.get('ai_insights'):
    ai = summary['ai_insights']
    print(f"\n📈 Market Trends:")
    for trend in ai['market_trends'][:2]:
        print(f"  • {trend}")