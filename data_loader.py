from datasets import load_dataset

def load_cnn_dailymail():
    """
    Loads the CNN/DailyMail dataset from HuggingFace.
    Returns the dataset object.
    """
    print("Loading CNN/DailyMail dataset...")
    # Using version 3.0.0 which is the standard version on HuggingFace
    dataset = load_dataset("cnn_dailymail", "3.0.0")
    print("Dataset loaded successfully!")
    return dataset

if __name__ == "__main__":
    # Test the loader
    data = load_cnn_dailymail()
    print(f"Train size: {len(data['train'])}")
    print(f"Sample article: {data['train'][0]['article'][:100]}...")
