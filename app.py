# app.py
"""Trials Intel - Demo Web Application"""

from flask import Flask, render_template, jsonify, request
import json
from pathlib import Path
from src.scrapers.clinical_trials import ClinicalTrialsScraper
from src.analyzers.trial_analyzer import TrialAnalyzer
from src.analyzers.pdf_analyzer import PDFAnalyzer
from config.settings import USE_MOCK_GEMINI

app = Flask(__name__)

# Initialize components
scraper = ClinicalTrialsScraper()
analyzer = TrialAnalyzer(use_mock=USE_MOCK_GEMINI)
pdf_analyzer = PDFAnalyzer(use_mock=USE_MOCK_GEMINI)

# Cache for demo
cached_trials = None
cached_analysis = None

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search_trials():
    """Search for clinical trials"""
    global cached_trials
    
    data = request.json
    condition = data.get('condition', 'CAR-T Cell Therapy')
    max_results = data.get('max_results', 10)
    
    print(f"\n🔍 Searching for: {condition}")
    
    trials = scraper.search_trials(condition, max_results)
    cached_trials = trials
    
    return jsonify({
        'success': True,
        'trials': trials,
        'count': len(trials)
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_trials():
    """Analyze trials with Gemini"""
    global cached_trials, cached_analysis
    
    if not cached_trials:
        return jsonify({'success': False, 'error': 'No trials to analyze'})
    
    print(f"\n🧠 Analyzing {len(cached_trials)} trials...")
    
    # Analyze trials
    analyzed = analyzer.analyze_batch(cached_trials[:5])  # Limit for demo
    
    # Generate comparison
    summary = analyzer.compare_trials(analyzed)
    
    cached_analysis = {
        'trials': analyzed,
        'summary': summary
    }
    
    return jsonify({
        'success': True,
        'analysis': cached_analysis
    })

@app.route('/api/vision-demo', methods=['GET'])
def vision_demo():
    """Demonstrate PDF vision capabilities"""
    
    print("\n👁️ Running vision analysis demo...")
    
    # Mock vision analysis (for demo)
    survival_data = pdf_analyzer.analyze_survival_curve("demo_km_curve.png")
    ae_data = pdf_analyzer.analyze_adverse_events_table("demo_ae_table.png")
    
    return jsonify({
        'success': True,
        'survival_analysis': survival_data,
        'safety_analysis': ae_data
    })

@app.route('/api/status', methods=['GET'])
def status():
    """System status"""
    return jsonify({
        'status': 'online',
        'gemini_mode': 'mock' if USE_MOCK_GEMINI else 'real',
        'cached_trials': len(cached_trials) if cached_trials else 0,
        'has_analysis': cached_analysis is not None
    })

if __name__ == '__main__':
    print("="*60)
    print("🚀 TRIALS INTEL - DEMO SERVER")
    print("="*60)
    print(f"\nMode: {'MOCK (development)' if USE_MOCK_GEMINI else 'REAL GEMINI'}")
    print("\n📍 Open: http://localhost:5000")
    print("\n" + "="*60)
    
    app.run(debug=True, port=5000)