import re
from transformers import BartTokenizer

# Load the tokenizer for the BART model
tokenizer = BartTokenizer.from_pretrained("facebook/bart-base")

def clean_text(text):
    """
    Performs basic text cleaning: removing extra whitespaces, 
    special characters, and normalizing casing.
    """
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces/newlines
    text = re.sub(r'[^\w\s.,!?-]', '', text)  # Remove special characters except punctuation
    return text.strip()

def preprocess_function(examples):
    """
    Tokenizes the input articles and the target highlights (summaries).
    """
    inputs = [clean_text(doc) for doc in examples["article"]]
    
    # Tokenize inputs
    model_inputs = tokenizer(inputs, max_length=1024, truncation=True, padding="max_length")

    # Tokenize targets using text_target (modern way, replaces as_target_tokenizer)
    labels = tokenizer(text_target=examples["highlights"], max_length=128, truncation=True, padding="max_length")

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

if __name__ == "__main__":
    # Test cleaning
    sample = "Hello!!!   This is a   TEST article... with some @#$ symbols."
    print(f"Original: {sample}")
    print(f"Cleaned: {clean_text(sample)}")
