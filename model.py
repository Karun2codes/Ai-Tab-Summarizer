import torch
from transformers import BartForConditionalGeneration, BartTokenizer

class SummarizerModel:
    def __init__(self, model_name="facebook/bart-base"):
        """
        Initializes the model wrapper with a specific BART variant.
        """
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.tokenizer = None

    def load_model(self, path=None):
        """
        Loads the model and tokenizer. If path is provided, loads from local disk.
        Otherwise, downloads from HuggingFace.
        """
        load_path = path if path else self.model_name
        print(f"Loading model from {load_path}...")
        
        self.tokenizer = BartTokenizer.from_pretrained(load_path)
        self.model = BartForConditionalGeneration.from_pretrained(load_path).to(self.device)
        print("Model loaded successfully.")

    def generate_summary(self, text, max_length=250, min_length=80):
        """
        Generates a summary for the given input text.
        """
        if self.model is None or self.tokenizer is None:
            raise Exception("Model not loaded. Call load_model() first.")

        # Tokenize input
        inputs = self.tokenizer([text], max_length=1024, return_tensors="pt", truncation=True).to(self.device)

        # Generate summary IDs
        summary_ids = self.model.generate(
            inputs["input_ids"], 
            num_beams=4, 
            max_length=max_length, 
            min_length=min_length,
            early_stopping=True
        )

        # Decode and return string
        return [self.tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids][0]

if __name__ == "__main__":
    # Quick test
    summarizer = SummarizerModel()
    summarizer.load_model()
    test_text = "The quick brown fox jumps over the lazy dog. This is a classic pangram used to test typefaces and scripts. It contains every letter of the English alphabet."
    print(f"Summary: {summarizer.generate_summary(test_text)}")
