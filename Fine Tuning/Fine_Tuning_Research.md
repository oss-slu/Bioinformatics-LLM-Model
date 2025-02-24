# Fine-Tuning CodeT5 for Bioinformatics Datasets

## Overview
This document outlines the process for fine-tuning the CodeT5 model using bioinformatics datasets. It includes dataset preprocessing, training setup, hyperparameter tuning, and evaluation.

---

## 1. Preprocessing the Dataset
### 1.1 Data Collection
- We have to gather all the different bioinformatics repositories from github that contain Python or R code. 
- We have to ensure the dataset contains code snippets relevant to bioinformatics workflows.

### 1.2 Data Cleaning
- Remove unnecessary symbols, comments, and non-relevant lines.
- Ensure text encoding and format consistency.
- Ensure the dataset is free from corrupt or incomplete code snippets


#### Example Code for Cleaning:

For python code: 

```python
import re

def clean_code(code_snippet):
    # Remove comments
    code_snippet = re.sub(r'#.*', '', code_snippet)  # Remove Python-style comments
    code_snippet = re.sub(r'//.*', '', code_snippet)  # Remove C-style comments
    code_snippet = re.sub(r'/\*.*?\*/', '', code_snippet, flags=re.DOTALL)  # Remove multi-line comments
    
    # Trim excess whitespace
    code_snippet = "\n".join([line.strip() for line in code_snippet.split("\n") if line.strip()])
    
    return code_snippet

# Example usage
raw_code = """
# This is a comment
import numpy as np  // Importing numpy
/* Multi-line 
   comment */
print("Hello, world!")
"""
cleaned_code = clean_code(raw_code)
print(cleaned_code)
```

For R code:

```r
clean_bioinformatics_code <- function(code_snippet) {
  # Remove comments
  code_snippet <- gsub("#.*", "", code_snippet)  # Remove R-style comments
  
  # Remove hardcoded file paths (e.g., "/Users/.../data.csv" or "C:/Users/.../data.csv")
  code_snippet <- gsub("\"[A-Za-z]:?/.+?\\.(csv|txt|fasta|fa|tsv)\"", "\"data_file\"", code_snippet)
  
  # Standardize package loading (ensure "library()" calls are formatted correctly)
  code_snippet <- gsub("library\\s*\\(\\s*([A-Za-z0-9_]+)\\s*\\)", "library(\\1)", code_snippet)
  
  # Ensure consistent spacing and formatting
  code_lines <- unlist(strsplit(code_snippet, "\n"))
  code_lines <- trimws(code_lines)  # Trim whitespace
  code_lines <- code_lines[nchar(code_lines) > 0]  # Remove empty lines
  
  return(paste(code_lines, collapse = "\n"))
}

# Example usage
raw_code <- "
# Load necessary library
  library( Biostrings )   # Used for DNA sequences
seq <- DNAString(\"ATGC\") # Creating a sequence
file_path <- \"/Users/ompatel/data/sequence_data.fasta\"

# Print sequence
print(seq)
"
cleaned_code <- clean_bioinformatics_code(raw_code)
cat(cleaned_code)
```

### 1.3 Formatting and Tokenization
- CodeT5 uses a code-specific **BPE tokenizer** trained using the Hugging Face `RobertaTokenizer`.
- The dataset must be tokenized correctly before training.
- For bioinformatics-specific processing, we ensure:
    - Preservation of FASTA/VCF file structures during tokenization.
    - Custom token recognition for common bioinformatics functions and libraries.
    - Handling multi-line sequences and ensuring correct splitting for model training.

#### Example Code for Tokenization:
```python
from transformers import RobertaTokenizer

tokenizer = RobertaTokenizer.from_pretrained("Salesforce/codet5-base")

def preprocess_function(examples):
    return tokenizer(examples["code"], padding="max_length", truncation=True)

tokenized_datasets = dataset.map(preprocess_function, batched=True)
```

---

## 2. Training Setup
### 2.1 Model Initialization
- Load the CodeT5 model with a sequence-to-sequence objective.
- We have to ensure the model is compatible with bioinformatics code structures, more specifically the libraries being used. 

#### Example Code:
```python
from transformers import AutoModelForSeq2SeqLM

model = AutoModelForSeq2SeqLM.from_pretrained("Salesforce/codet5-base")
```

### 2.2 Training Arguments
- Define parameters such as batch size, learning rate, and weight decay.
- Adjust the learning rates to prevent overfitting on smaller bioinformatics datasets

#### Example Code:
```python
from transformers import TrainingArguments

training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    save_total_limit=2,
)
```

### 2.3 Training Execution
 - We can utlize a Trainer API for efficient model training
 - Ensure compatability with training when working with larger bioinformatics dataset
#### Example Code:
```python
from transformers import Trainer

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
)

trainer.train()
```

---

## 3. Hyperparameter Tuning
- Experiment with different values for:
  - Batch size
  - Learning rate
  - Weight decay
- Use **grid search** or **Optuna** for hyperparameter optimization.
- Log the results with Weights and Biases to better understand the performance

Example Code for Hyperparameter Tuning with Optuna:
```python
import optuna

def objective(trial):
    learning_rate = trial.suggest_loguniform("learning_rate", 1e-5, 5e-4)
    batch_size = trial.suggest_categorical("batch_size", [4, 8, 16])
    weight_decay = trial.suggest_uniform("weight_decay", 0.01, 0.1)
    
    training_args = TrainingArguments(
        output_dir="./results",
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=3,
        weight_decay=weight_decay,
        learning_rate=learning_rate,
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["test"],
    )
    
    result = trainer.train()
    return result.training_loss

study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=10)
print("Best hyperparameters:", study.best_params)
```
---

## 4. Evaluation
### 4.1 Metrics
- Since the Hugging Face description does not provide built-in evaluation results, we define our own:
  - **BLEU Score** (for code generation accuracy)
  - **ROUGE Score** (for text-based similarity)
  - **Exact Match Accuracy** (for code completion correctness)
  - **Task-Specific Metrics** (e.g., API call correctness in bioinformatics workflows)
  - **Execution-based Metric** (for the correctness of generated code snippets when executed in an R or Python)


### Expected Results for Metrics
| Metric  | Good Score Range |
|---------|-----------------|
| BLEU    | 30-60           |
| ROUGE-L | 50-80           |
| Exact Match Accuracy | 60-90%  |
| Execution-Based Metrics | 80-95% |

### 4.2 Evaluation Code
#### Example Code:
```python
import evaluate

metric = evaluate.load("bleu")

def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
    return metric.compute(predictions=decoded_preds, references=decoded_labels)
```

---