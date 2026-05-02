import evaluate
from model import SummarizerModel
from data_loader import load_cnn_dailymail

def run_evaluation():
    # Load ROUGE metric
    rouge = evaluate.load("rouge")
    
    # Load model (prefer locally trained one if exists, otherwise base)
    model_path = "./trained_model"
    summarizer = SummarizerModel()
    
    try:
        summarizer.load_model(model_path)
    except:
        print("Trained model not found. Using default base model for evaluation.")
        summarizer.load_model("facebook/bart-base")

    # Load test data (small subset for speed)
    dataset = load_cnn_dailymail()
    test_data = dataset["test"].select(range(10))

    predictions = []
    references = []

    print("Generating summaries for evaluation...")
    for item in test_data:
        pred = summarizer.generate_summary(item["article"])
        predictions.append(pred)
        references.append(item["highlights"])

    # Compute scores
    results = rouge.compute(predictions=predictions, references=references)
    
    print("\n--- ROUGE Evaluation Scores ---")
    for key, value in results.items():
        print(f"{key}: {value:.4f}")

if __name__ == "__main__":
    run_evaluation()
