from transformers import pipeline, AutoTokenizer
from config import LLM_SETTINGS
from utils.llm_loader import load_model

def review_chapter(original, rewritten):
    """Review and refine rewritten chapter"""
    model, tokenizer = load_model(LLM_SETTINGS["reviewer_model"])
    generator = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer
    )
    
    prompt = f"""
    Original Chapter:
    {original}
    
    Rewritten Chapter:
    {rewritten}
    
    As a professional proofreader, review the rewritten chapter for:
    1. Grammar and spelling errors
    2. Clarity and readability
    3. Consistent tone and style
    4. Faithfulness to original meaning
    
    Provide your refined version:
    """

    # Truncate the prompt to fit model's max length
    max_length = 1024
    input_ids = tokenizer.encode(prompt, add_special_tokens=False)
    if len(input_ids) > max_length:
        print(f"  Review prompt too long for model, truncating to {max_length} tokens.")
        input_ids = input_ids[:max_length]
        prompt = tokenizer.decode(input_ids)

    result = generator(
        prompt,
        max_new_tokens=LLM_SETTINGS["max_new_tokens"],
        temperature=LLM_SETTINGS["temperature"] * 0.7,  # Lower temperature for refinement
        do_sample=True
    )
    
    return result[0]['generated_text'].split("Provide your refined version:")[-1].strip()