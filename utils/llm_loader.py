from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

MODEL_CACHE = {}

def load_model(model_name):
    """Load and cache LLM models"""
    if model_name not in MODEL_CACHE:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )
        MODEL_CACHE[model_name] = (model, tokenizer)
    return MODEL_CACHE[model_name]