# test_scraper.py
"""Test ClinicalTrials.gov scraper"""

from src.scrapers.clinical_trials import ClinicalTrialsScraper

# Initialize scraper
scraper = ClinicalTrialsScraper()

# Test search
trials = scraper.search_trials("CAR-T Cell Therapy", max_results=10)

# Display results
print(f"\n📊 Retrieved {len(trials)} trials\n")

for trial in trials[:3]:
    print(f"🔬 {trial['title']}")
    print(f"   NCT ID: {trial['nct_id']}")
    print(f"   Phase: {trial['phase']}")
    print(f"   Status: {trial['status']}")
    print(f"   URL: {trial['url']}")
    print()

# Save results
scraper.save_trials(trials, 'cart_trials.json')

print("✅ Phase 2 Complete!")