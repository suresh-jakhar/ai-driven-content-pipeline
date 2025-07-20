import json
from datetime import datetime
from config import VERSIONS_DIR
import hashlib

def create_version_record(url, data):
    """Create versioned JSON record"""
    url_hash = hashlib.md5(url.encode()).hexdigest()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chapter_{url_hash}_{timestamp}.json"
    filepath = VERSIONS_DIR / filename
    
    record = {
        "metadata": {
            "url": url,
            "timestamp": timestamp,
            "status": data.get("status", "pending"),
            "chapter_id": f"chapter_{url_hash}",
            "version": timestamp
        },
        "content": {
            "original_text": data.get("original_text", ""),
            "rewritten_text": data.get("rewritten_text", ""),
            "reviewed_text": data.get("reviewed_text", ""),
            "final_text": data.get("final_text", ""),
            "screenshot_path": data.get("screenshot_path", "")
        },
        "evaluation": data.get("evaluation", {}),
        "human_feedback": data.get("human_feedback", {})
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    
    return filepath