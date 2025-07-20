from config import AUDIO_DIR
from gtts import gTTS
import hashlib
from datetime import datetime
from tqdm import tqdm

def text_to_speech(text, lang='en'):
    """Enhanced TTS function with progress feedback"""
    print("\nInitializing text-to-speech engine...")
    
    if len(text) > 5000:
        print("  Text too long, truncating to 5000 characters")
        text = text[:5000] + " [truncated]"
    
    text_hash = hashlib.md5(text.encode()).hexdigest()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"narration_{text_hash}_{timestamp}.mp3"
    filepath = AUDIO_DIR / filename
    
    print("  Generating audio...")
    with tqdm(total=100, desc="Processing", ncols=100) as pbar:
        tts = gTTS(text=text, lang=lang, slow=False)
        pbar.update(50)
        tts.save(str(filepath))
        pbar.update(50)
    
    print("\nAudio generation complete!")
    return filepath