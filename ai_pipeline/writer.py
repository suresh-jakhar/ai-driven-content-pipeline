from transformers import pipeline, AutoTokenizer
from config import LLM_SETTINGS
from utils.llm_loader import load_model
from tqdm import tqdm
import torch
import textwrap

def format_prompt(text):
    """Format the writing prompt with clear instructions"""
    return f"""
    [INSTRUCTIONS]
    You are a professional editor rewriting a book chapter in modern English.
    Your task is to:
    1. Maintain the original plot, characters, and key details
    2. Improve clarity and flow while preserving the author's voice
    3. Fix any grammatical errors
    4. Keep the same length as the original
    
    [ORIGINAL CHAPTER]
    {textwrap.fill(text, width=80)}
    
    [REWRITTEN CHAPTER]
    """

def rewrite_chapter(text):
    """Enhanced rewriting function with progress feedback"""
    print("\nInitializing AI writer...")
    model, tokenizer = load_model(LLM_SETTINGS["writer_model"])
    
    print("  Preparing text generation pipeline...")
    generator = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer
    )
    
    prompt = format_prompt(text)
    
    # Truncate the prompt to fit model's max length
    max_length = 1024
    input_ids = tokenizer.encode(prompt, add_special_tokens=False)
    if len(input_ids) > max_length:
        print(f"  Prompt too long for model, truncating to {max_length} tokens.")
        input_ids = input_ids[:max_length]
        prompt = tokenizer.decode(input_ids)

    print("  Generating rewritten content...")
    with tqdm(total=100, desc="Writing", ncols=100) as pbar:
        result = generator(
            prompt,
            max_new_tokens=LLM_SETTINGS["max_new_tokens"],
            temperature=LLM_SETTINGS["temperature"],
            do_sample=True
        )
        pbar.update(100)
    
    # Extract just the rewritten portion
    full_output = result[0]['generated_text']
    rewritten = full_output.split("[REWRITTEN CHAPTER]")[-1].strip()
    
    print("\nWriting complete!")
    print(f"Prompt length: {len(prompt)} characters")
    print(f"Rewritten length: {len(rewritten)} characters")
    
    return rewritten