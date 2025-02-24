# Extracting Bioconductor Code Snippets for CodeT5 Fine-Tuning

## Overview
This is an overview of the data that the Bioconductor website holds.Some of the data that Bioconductor provides is vignettes, reference manuals, and GitHub repositories containing code that can be used for model training.

Link to all software packages: https://bioconductor.org/packages/devel/BiocViews.html#___Software

## Finding Bioconductor Code Snippets

### A. Package Vignettes 
This is best for Workflows & Examples

- **Example: DESeq2 Vignette**
  - [DESeq2 Vignette](https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.R)
  - This contains tutorials with code snippets for differential gene expression analysis.

### B. Reference Manuals (Best for Function Documentation)
- URL Format:
  ```
  https://bioconductor.org/packages/release/bioc/manuals/{package_name}/man/{package_name}.pdf
  ```
- **Example: DESeq2 Manual**
  - [DESeq2 Manual](https://bioconductor.org/packages/release/bioc/manuals/DESeq2/man/DESeq2.pdf)
  - This includes function descriptions and usage examples.

### C. GitHub Repositories 
Many Bioconductor packages are also present on GitHub.

This would be best for Source Code & Scripts. 

- **Example: DESeq2 GitHub Repository**
  - [DESeq2 Source Code](https://github.com/thelovelab/DESeq2)
  - Look in the `R/` folder for function definitions.

## Extracting Code for Fine-Tuning CodeT5

We can try to use datascraping to download vignettes/manuals and extract relevant R code blocks. We could scrape just the R scripts from packages that have scripts available. For the one's that do not have a script available, there is more likely than not going to be a pdf manual which will have the different functions along with the descriptions present. For packages that have Git repositories, we can go directly there and scrape to get each and every script seperately instead of taking one file that has all of the scripts. It would allow for cleaner data. 