# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Gemini Settings
GEMINI_MODEL = "gemini-2.0-flash"
USE_MOCK_GEMINI = os.getenv('USE_MOCK_GEMINI', 'true').lower() == 'true'

# ClinicalTrials.gov API
CLINICAL_TRIALS_BASE_URL = "https://clinicaltrials.gov/api/v2/studies"

# Processing Settings
MAX_TRIALS_TO_FETCH = 20  # Start small
PDF_STORAGE_PATH = "data/raw/pdfs"
PROCESSED_DATA_PATH = "data/processed"

# Demo Settings
DEMO_DISEASE_AREAS = [
    "CAR-T Cell Therapy",
    "Non-Small Cell Lung Cancer"
]

# Create directories
os.makedirs(PDF_STORAGE_PATH, exist_ok=True)
os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)