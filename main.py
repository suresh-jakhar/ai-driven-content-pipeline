import argparse
from scraper.scraper import scrape_url
from ai_pipeline.writer import rewrite_chapter
from ai_pipeline.reviewer import review_chapter
from ai_pipeline.evaluator import evaluate_quality
from human_review.feedback import get_human_feedback
from storage.version_tracker import create_version_record
from storage.chroma_db import ChapterDB
from utils.helpers import setup_logging, clean_text, generate_chapter_id
from tqdm import tqdm
import time
import sys
import httpx

logger = setup_logging()

def print_step(step_num, step_name):
    print(f"\n\033[1mSTEP {step_num}: {step_name.upper()}\033[0m")
    print("-" * 50)

def print_success(message):
    print(f"\033[92m✓ {message}\033[0m")

def print_warning(message):
    print(f"\033[93m⚠ {message}\033[0m")

def print_error(message):
    print(f"\033[91m✗ {message}\033[0m")

def print_info(message):
    print(f"\033[94mℹ {message}\033[0m")

def get_user_url():
    while True:
        url = input("\n\033[1mEnter the URL of the book chapter:\033[0m ").strip()
        if url.startswith(('http://', 'https://')):
            return url
        print_error("Invalid URL. Please enter a valid URL starting with http:// or https://")

def main(enable_voice=False):
    print("\033[1m" + "="*50)
    print("AUTOMATED BOOK PUBLICATION PIPELINE")
    print("="*50 + "\033[0m")
    
    url = get_user_url()
    
    try:
        # Step 1: Scraping
        print_step(1, "Scraping Content")
        with tqdm(total=100, desc="Progress", ncols=100) as pbar:
            scrape_data = scrape_url(url)
            pbar.update(50)
            time.sleep(0.5)  # Simulate processing
            pbar.update(50)
        
        if not scrape_data.get("scrape_success"):
            print_error(f"Scraping failed: {scrape_data.get('error')}")
            print_info("Please check the URL and try again.")
            return
        
        print_success(f"Successfully scraped {len(scrape_data['original_text'])} characters")
        print_success(f"Screenshot saved to: {scrape_data['screenshot_path']}")

        # Step 2: AI Rewriting
        print_step(2, "AI Rewriting")
        print_info("Rewriting chapter with LLM...")
        with tqdm(total=100, desc="Processing", ncols=100) as pbar:
            rewritten = rewrite_chapter(scrape_data["original_text"])
            pbar.update(100)
        
        print_success("Chapter rewritten successfully!")
        print(f"\n\033[1mOriginal Text Sample:\033[0m\n{scrape_data['original_text'][:200]}...")
        print(f"\n\033[1mRewritten Text Sample:\033[0m\n{rewritten[:200]}...")

        # Step 3: AI Review
        print_step(3, "AI Review")
        print_info("Reviewing and refining the chapter...")
        with tqdm(total=100, desc="Reviewing", ncols=100) as pbar:
            reviewed = review_chapter(scrape_data["original_text"], rewritten)
            pbar.update(100)
        
        print_success("Chapter reviewed and polished!")

        # Step 4: Evaluation
        print_step(4, "Quality Evaluation")
        evaluation = evaluate_quality(scrape_data["original_text"], reviewed)
        print(f"\n\033[1mEvaluation Results:\033[0m")
        print(f"Total Score: \033[1m{evaluation['total_score']}/50\033[0m")
        for cat, score in evaluation["scores"].items():
            print(f"{cat.capitalize()}: {score}/10")
        
        if evaluation["total_score"] >= 30:
            print_success("Chapter meets quality standards!")
        else:
            print_warning("Chapter quality is below optimal threshold")

        # Step 5: Human Review
        print_step(5, "Human Review")
        print_info("Please review the AI-generated content:")
        feedback = get_human_feedback(scrape_data["original_text"], reviewed, evaluation)
        
        if feedback["status"] == "rejected":
            print_error("Chapter rejected. Process terminated.")
            return
        elif feedback["status"] == "edited":
            print_success("Chapter edited and accepted!")
        else:
            print_success("Chapter accepted without changes!")

        # Step 6: Versioning
        print_step(6, "Version Control")
        chapter_data = {
            **scrape_data,
            "rewritten_text": rewritten,
            "reviewed_text": reviewed,
            "evaluation": evaluation,
            "human_feedback": feedback,
            "final_text": feedback["edited_text"],
            "status": feedback["status"]
        }
        
        record_path = create_version_record(url, chapter_data)
        print_success(f"Version record saved to: {record_path}")

        # Step 7: Storage
        print_step(7, "Database Storage")
        if feedback["status"] in ["accepted", "edited"]:
            try:
                db = ChapterDB()
                chapter_id = generate_chapter_id(url)
                db.add_chapter(
                    chapter_id=chapter_id,
                    text=feedback["edited_text"],
                    metadata={
                        "url": url,
                        "score": evaluation["total_score"],
                        "status": feedback["status"]
                    }
                )
                print_success(f"Chapter stored in database with ID: {chapter_id}")
            except httpx.ReadTimeout:
                print_error("Your connection timed out while downloading the embedding model. Please check your internet and try again.")
            except Exception as e:
                print_error(f"An error occurred during database storage: {str(e)}")

        # Step 8: Voice Narration (Optional)
        if enable_voice and feedback["status"] in ["accepted", "edited"]:
            print_step(8, "Voice Narration")
            from utils.voice import text_to_speech
            print_info("Generating audio narration...")
            audio_path = text_to_speech(feedback["edited_text"])
            print_success(f"Audio narration saved to: {audio_path}")

        print("\n\033[1;92m" + "="*50)
        print("PROCESSING COMPLETE!")
        print("="*50 + "\033[0m")

    except Exception as e:
        print_error(f"An unexpected error occurred: {str(e)}")
        logger.exception("Pipeline error")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated Book Publication Pipeline")
    parser.add_argument("--voice", action="store_true", help="Enable voice narration")
    args = parser.parse_args()
    
    main(args.voice)