# CodeT5: A Pre-trained Encoder-Decoder Transformer for Code Understanding and Generation

### Paper link: https://arxiv.org/pdf/2109.00859
### Github link: https://github.com/salesforce/CodeT5

## Overview
- Most current models rely on either encoder-only or decoder-only pre-training, which is suboptimal for generation.
- Many models process code similarly to natural language rather than as a programming language.
- CodeT5 is a pre-trained encoder-decoder transformer that supports both code understanding and code generation tasks.

## Key Features
- The model distinguishes code tokens that are identifiers, unlike prior work that treats code as natural language.
- Developers often use informative identifiers (e.g., `binarySearch`) to improve code clarity.
- CodeT5 integrates identifier information into a seq2seq model via:
  - Identifier tagging
  - Identifier prediction tasks
- Captures rich semantic information from code better than previous methods.
- Uses both code and accompanying comments to improve natural language - programming language (NL-PL) alignment.

## Shortcomings of Existing Approaches
- Conventional NLP pre-training techniques treat code as a plain sequence of tokens, ignoring its rich structural information.

## Architecture & Pre-training
- CodeT5 builds on the T5 architecture, using denoising sequence-to-sequence pre-training:
  - Corrupts the source input and requires the decoder to recover them.
  - Shown to benefit generation tasks in natural language.
  - Extended to programming languages for code-specific tasks.

## Evaluation & Applications
- Evaluated for tasks such as:
  - Error detection
  - Code generation
- Outperforms prior methods in:
  - Code defect detection
  - Clone detection
- Fine-tuned on CodeXGLUE benchmark for:
  - Code defect detection
  - Clone detection
  - Code summarization
  - Code generalization
  - Code translation

## Training Data
- Pre-trained on CodeSearchNet, which includes both:
  - Unimodal (PL-only) data
  - Bimodal (PL-NL) data
- Covers six programming languages:
  - Ruby
  - JavaScript
  - Go
  - Python
  - Java
  - PHP
- Additional data collection from Google BigQuery:
  - C/C#
- Total dataset size: 8.35 million instances for pre-training.

## Input Processing
- Supports:
  - PL input only
  - PL and NL input combined, joined with a separator token.
- Improves code understanding by:
  - Identifying identifiers and converting code into a tree structure.
  - Assigning a binary label to each code token to indicate if it’s an identifier or not.

## Tokenization
- Uses a specialized Byte-Pair Encoding (BPE) tokenizer trained for code.
- Vocabulary size: 32,000 tokens
- Includes special tokens: `[CLS]`, `[SEP]`, `[MASK0-99]`
- Filters out rare and non-printable characters.
- Reduces tokenized code length by 30%-45%, improving:
  - Training efficiency
  - Handling of code symbols (e.g., `{}`)
- Fixes issues in T5’s default tokenizer, which misprocesses code symbols.

## Limitations
- Training data consists of open-source GitHub repositories with user-written comments:
  - Not tied to any specific application.
  - May contain stereotypes from:
    - Text comments
    - Source code (e.g., variable, function, and class names)
- Generated functions may appear correct but fail to align with developer intent.
- Generation outputs should only be used as references and require:
  - Domain experts for correctness checks.
  - Security validation.
