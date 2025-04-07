import json
import torch
from torch.utils.data import DataLoader
from transformers import RobertaTokenizer, RobertaForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset

# Load your custom dataset from JSON
with open('/masking/fixed_masked_training_data.json', 'r') as f:
    data = json.load(f)


dataset = Dataset.from_dict({
    'input': [example['input'] for example in data],
    'output': [example['output'] for example in data]
})

tokenizer = RobertaTokenizer.from_pretrained("Salesforce/codet5-small")

# Define the preprocessing function
def preprocess_data(examples):
    inputs = [f"Summarize R: {code}" for code in examples['input']]
    model_inputs = tokenizer(inputs, padding="max_length", truncation=True, max_length=256)

    # Tokenize labels and handle padding tokens with -100
    labels = tokenizer(examples['output'], padding="max_length", truncation=True, max_length=128).input_ids
    labels = [[label if label != 0 else -100 for label in label_example] for label_example in labels]

    model_inputs["labels"] = labels
    return model_inputs

dataset = dataset.map(preprocess_data, batched=True)



# Initialize the model
model = RobertaForSequenceClassification.from_pretrained("Salesforce/codet5-small")

# Set up TrainingArguments
training_args = TrainingArguments(
    output_dir='./results',          
    evaluation_strategy="epoch",     
    learning_rate=2e-5,              
    per_device_train_batch_size=8,   
    per_device_eval_batch_size=8,    
    num_train_epochs=3,              
    weight_decay=0.01,               
    logging_dir='./logs',           
    logging_steps=10,                
)

trainer = Trainer(
    model=model,                         
    args=training_args,                 
    train_dataset=dataset,               
    eval_dataset=dataset,             
)

trainer.train()

# Save the model after training
model.save_pretrained('./final_model')
tokenizer.save_pretrained('./final_model')
