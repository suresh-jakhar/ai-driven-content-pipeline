import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SCREENSHOTS_DIR = DATA_DIR / "screenshots"
VERSIONS_DIR = DATA_DIR / "versions"
AUDIO_DIR = DATA_DIR / "audio"

# Create directories if missing
for d in [SCREENSHOTS_DIR, VERSIONS_DIR, AUDIO_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# LLM Configuration
LLM_SETTINGS = {
    "writer_model": "distilgpt2",
    "reviewer_model": "distilgpt2",
    "max_new_tokens": 1024,
    "temperature": 0.7
}

# Scoring weights
SCORE_WEIGHTS = {
    "grammar": 0.25,
    "clarity": 0.20,
    "structure": 0.15,
    "faithfulness": 0.25,
    "fluency": 0.15
}