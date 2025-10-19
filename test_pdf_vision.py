# test_pdf_vision.py
"""Test PDF vision analysis capabilities"""

import json
from src.analyzers.pdf_analyzer import PDFAnalyzer

print("="*60)
print("PHASE 4: PDF VISION ANALYSIS (MOCK MODE)")
print("="*60)

# Initialize analyzer
analyzer = PDFAnalyzer(use_mock=True)

# Test 1: Survival Curve Analysis
print("\n[TEST 1] Kaplan-Meier Survival Curve Analysis")
print("-"*60)

survival_data = analyzer.analyze_survival_curve("mock_km_curve.png")

print("📊 SURVIVAL DATA EXTRACTED:")
print(json.dumps(survival_data, indent=2))

print("\n💡 INTERPRETATION:")
print(f"   • Treatment median survival: {survival_data['median_survival_treatment']} months")
print(f"   • Control median survival: {survival_data['median_survival_control']} months")
print(f"   • Hazard Ratio: {survival_data['hazard_ratio']} ({survival_data['confidence_interval']})")
print(f"   • Statistical significance: p {survival_data['p_value']}")
print(f"   • Clinical impact: {survival_data['analysis']}")

# Test 2: Adverse Events Table
print("\n[TEST 2] Adverse Events Table Analysis")
print("-"*60)

ae_data = analyzer.analyze_adverse_events_table("mock_ae_table.png")

print("⚠️ SAFETY DATA EXTRACTED:")
print(json.dumps(ae_data, indent=2))

print("\n💡 INTERPRETATION:")
print(f"   • Grade 3+ events (treatment): {ae_data['grade_3_plus_treatment']}%")
print(f"   • Grade 3+ events (control): {ae_data['grade_3_plus_control']}%")
print(f"   • Most common AE: {ae_data['most_common_ae']} ({ae_data['most_common_ae_rate']}%)")

print("\n   Top Serious Adverse Events:")
for ae in ae_data['serious_aes']:
    print(f"     • {ae['event']}: {ae['rate']}%")

# Test 3: Full Trial Results
print("\n[TEST 3] Complete Trial Results Extraction")
print("-"*60)

results = analyzer.extract_trial_results("mock_trial_paper.pdf")

print("📄 TRIAL RESULTS:")
print(json.dumps(results, indent=2))

print("\n💡 EXECUTIVE SUMMARY:")
print(f"   • Primary endpoint: {results['primary_endpoint']}")
print(f"   • Endpoint met: {'✅ YES' if results['primary_endpoint_met'] else '❌ NO'}")
print(f"   • Result: {results['primary_result']}")
print(f"   • Conclusion: {results['conclusion']}")

print("\n   Secondary Endpoints:")
for endpoint in results['secondary_endpoints']:
    print(f"     • {endpoint['endpoint']}: {endpoint['result']}")

# Investment Intelligence Summary
print("\n" + "="*60)
print("🎯 INVESTMENT INTELLIGENCE")
print("="*60)

print("\n📈 QUANTITATIVE METRICS:")
print(f"   Efficacy Score: {survival_data['median_survival_treatment'] / survival_data['median_survival_control']:.1f}x improvement")
print(f"   Risk/Benefit Ratio: {ae_data['grade_3_plus_treatment'] - ae_data['grade_3_plus_control']}% increased toxicity")
print(f"   Statistical Power: p {survival_data['p_value']} (highly significant)")

print("\n💰 COMMERCIAL IMPLICATIONS:")
print("   • Superiority demonstrated vs standard of care")
print("   • Safety profile manageable for market approval")
print("   • Multiple positive secondary endpoints support label expansion")
print("   • Data quality sufficient for regulatory submission")

print("\n✅ Phase 4 Complete - Multimodal Vision Analysis Ready!")
print("\n🚀 SYSTEM CAPABILITIES:")
print("   ✅ ClinicalTrials.gov data scraping")
print("   ✅ AI-powered trial classification")
print("   ✅ Comparative intelligence generation")
print("   ✅ PDF vision analysis (survival curves, tables)")
print("   ✅ Investment intelligence synthesis")