import os
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments, BartForConditionalGeneration, BartTokenizer
from data_loader import load_cnn_dailymail
from preprocess import preprocess_function
import torch

def train():
    # 1. Load Dataset
    dataset = load_cnn_dailymail()
    
    # Use a larger subset for better accuracy
    train_dataset = dataset["train"].select(range(5000)) 
    val_dataset = dataset["validation"].select(range(500))

    # 2. Preprocess
    print("Preprocessing data...")
    tokenized_train = train_dataset.map(preprocess_function, batched=True)
    tokenized_val = val_dataset.map(preprocess_function, batched=True)

    # 3. Load Model
    model_name = "facebook/bart-base"
    model = BartForConditionalGeneration.from_pretrained(model_name)
    tokenizer = BartTokenizer.from_pretrained(model_name)

    # 4. Define Training Arguments
    training_args = Seq2SeqTrainingArguments(
        output_dir="./results",
        eval_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        weight_decay=0.01,
        save_total_limit=3,
        num_train_epochs=10,
        predict_with_generate=True,
        fp16=torch.cuda.is_available(),
    )

    # 5. Initialize Trainer
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_val,
        processing_class=tokenizer, # Updated from 'tokenizer' for newer versions
    )

    # 6. Start Training
    print("Starting training loop...")
    trainer.train()

    # 7. Save Model
    print("Saving model to ./trained_model...")
    trainer.save_model("./trained_model")
    tokenizer.save_pretrained("./trained_model")

if __name__ == "__main__":
    train()
