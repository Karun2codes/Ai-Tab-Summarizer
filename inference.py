from model import SummarizerModel
import os

class InferenceEngine:
    def __init__(self, model_dir="./trained_model"):
        """
        Inference engine that automatically looks for the trained model.
        """
        self.summarizer = SummarizerModel()
        
        # Check if local model exists, else fallback to base
        if os.path.exists(model_dir):
            self.summarizer.load_model(model_dir)
        else:
            print(f"Warning: {model_dir} not found. Using default facebook/bart-base.")
            self.summarizer.load_model("facebook/bart-base")

    def summarize(self, text):
        """
        Generates summary for a single piece of text.
        """
        if not text or len(text.strip()) < 10:
            return "Text too short to summarize."
        return self.summarizer.generate_summary(text)

if __name__ == "__main__":
    # Example usage
    engine = InferenceEngine()
    text = "Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to natural intelligence displayed by animals including humans. AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals."
    print(f"Result: {engine.summarize(text)}")
