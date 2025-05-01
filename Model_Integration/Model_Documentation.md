# Fine-Tuned CodeT5 Model Training and Evaluation Documentation

## 1. Model Training Overview

- **Base Model Used:** `Salesforce/codet5-small`
- **Fine-tuned Model:** `Om368/Fine-tuned_CodeT5_Model`
- **Dataset:** Loaded from a custom JSON file `fixed_masked_training_data.json`.
  - Each entry contains:
    - `input`: masked code snippet
    - `output`: complete code snippet
- **Task Objective:** Fine-tune the model to generate R code related to bioinformatics tasks.

### Training Steps:

1. Load the custom dataset.
2. Preprocess the input and output with a tokenizer (`RobertaTokenizer` from CodeT5).
3. Train using the HuggingFace `Trainer` API.
4. Save the fine-tuned model and tokenizer to a local directory (`./final_model`).

---

## 2. Hyperparameter Configuration

| Hyperparameter              | Value             |
| ---------------------------- | ----------------- |
| Learning Rate                | 2e-5              |
| Training Batch Size          | 8                 |
| Evaluation Batch Size        | 8                 |
| Number of Training Epochs    | 3                 |
| Weight Decay (L2 Regularization) | 0.01         |
| Optimizer                    | AdamW             |
| Max Input Token Length       | 256 tokens        |
| Max Output Token Length      | 128 tokens        |
| Logging Frequency            | Every 10 steps    |

- **Loss function:** CrossEntropyLoss (automatically used inside `Trainer`).
- **Gradient Clipping:** Handled internally by HuggingFace.

---

## 3. Model Evaluation Strategy

### Current Evaluation:

- **Training and evaluation** were both done on the same dataset (initial version).
- **No separate validation set** yet, so overfitting risk exists.
- Model performance primarily monitored via **training loss**.

### Recommended Future Evaluation:

- Split data into:
  - **Training set (80%)**
  - **Validation set (20%)**
- Introduce evaluation metrics such as:
  - **ROUGE**
  - **BLEU**
  - **Exact Match**
- Use early stopping based on validation loss to prevent overfitting.

---

## 4. Future Improvements for Training on More Data

- **Larger Dataset:**
  - Expand training samples to cover more diverse examples.
  - Include edge cases, longer code snippets, and real-world codebases.

- **Hyperparameter Tuning:**
  - Experiment with different learning rates (e.g., 1e-5, 3e-5).
  - Try larger batch sizes if GPU memory allows (16, 32).
  - Use learning rate schedulers (e.g., cosine decay, linear warmup).

- **Model Scaling:**
  - Fine-tune larger models like `codet5-base` or `codet5-large` for potentially better performance.

---

# Conclusion

This document covers the fine-tuning methodology for the `Salesforce/codet5-small` model, the hyperparameters used, evaluation methods, and recommendations for future model improvement as the dataset scales.

