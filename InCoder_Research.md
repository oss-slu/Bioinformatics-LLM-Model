## InCoder: A Generative Model for Code Infilling and Synthesis

### Paper link: [https://arxiv.org/pdf/2204.05999v3](https://arxiv.org/pdf/2204.05999v3)
### Model page: [https://sites.google.com/view/incoder-code-models/](https://sites.google.com/view/incoder-code-models/)

## Overview
- Most existing code models generate code left-to-right, limiting their ability to edit and refine existing code.
- InCoder is a unified generative model that can both synthesize code (left-to-right generation) and edit code (via masking and infilling).
- Trained on a large corpus of permissively licensed code, using a causal masking objective to learn infilling.

## Key Features
- Supports both code generation and code editing by predicting masked code spans with access to bidirectional context.
- Unlike previous models, InCoder enables arbitrary region infilling, making it useful for tasks like:
  - Bug fixing
  - Comment generation
  - Variable renaming
  - Code completion
- Achieves competitive performance on standard left-to-right program synthesis benchmarks while outperforming prior models on infilling tasks.

## Shortcomings of Existing Approaches
- Traditional models treat code as natural language, ignoring the structured nature of programming.
- Left-to-right models lack the ability to edit existing code efficiently.
- Most pre-trained models are optimized for generation, not code refinement.

## Architecture & Pre-training
- Based on a decoder-only Transformer architecture.
- Uses a causal masking training objective:
  - Randomly masks spans of code and moves them to the end of the sequence.
  - Trains the model to predict these spans, improving infilling ability.
- Pre-trained on 159GB of permissively licensed code from GitHub and GitLab across 28 programming languages.
- StackOverflow content is also referenced.

## Evaluation & Applications
- Evaluated on various zero-shot infilling tasks:
  - Type inference: Predicts missing type annotations.
  - Comment generation: Generates meaningful docstrings based on function bodies.
  - Variable renaming: Suggests more meaningful names for variables.
  - Code completion: Fills in missing lines of code in incomplete programs.
- Outperforms left-to-right models on HumanEval and CodeXGLUE benchmarks for infilling tasks.

## Training Data
- Includes both code-only data and StackOverflow discussions for a more holistic understanding.
- Filtered for quality, deduplicated to remove redundancy, and cleaned for evaluation integrity.
- Primary language of use is Python 

## Input Processing
- Supports:
  - Standard left-to-right code generation
  - Code infilling with bidirectional context
- Uses causal masking to allow flexible code completion and refinement.

## Tokenization
- Uses a byte-level BPE tokenizer optimized for code.
- Reduces tokenized sequence length by 30-45%, improving efficiency.
- Handles code symbols and identifiers better than standard NLP tokenizers.

## Limitations
- Trained only on open-source repositories which may not generalize to proprietary codebases.
- Predictions require human verification to ensure correctness and security.
- Code completions may appear syntactically correct but need validation for logic and intent.

### Summary
InCoder is a powerful code generation and editing model designed to fill in missing code spans efficiently. 
It surpasses traditional left-to-right models in code infilling and refinement while maintaining strong performance on standard code synthesis tasks.
