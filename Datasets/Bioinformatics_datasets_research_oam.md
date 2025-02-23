## BioCoder Python and Rosalind Datasets

### Description:
Several Github repositories were parsed and functions were selected from them. It consists of real-world Python and Java functions from bioinformatics repositories and problem-solving challenges from the Rosalind Project. For our focus I have selected only the Python functions and Rosalind solutions.

The dataset can be found at this link:
[BioCoder Dataset](https://github.com/gersteinlab/BioCoder/tree/main/datasets)

### Format:
After the functions were extracted, the output was a JSON format. The functions were then processed. This included filtering out functions that were too short, too long, or had too many parameters. It also included filtering out functions that were too similar to each other. The function sets I focused on are:

- **python_hidden.json**: A JSON of the 1026 Python functions that make up the Python part of the "hidden" dataset of the benchmark
- **python_public.json**: A JSON of the 50 Python functions that make up the Python part of the "public" dataset of the benchmark
- **python_simlar.json**: A JSON of the 50 Python functions that make up the Python part of the "similar" dataset of the benchmark
- **rosalind.json**: A JSON of the 253 Rosalind functions that make up the Rosalind part of the "public" dataset of the benchmark

### Example Python function:
```python
def parse_contig_file_name(ref_names, taxon_names, contig_file):
    """Extract the reference & taxon names from the contig file name."""
    sep = '[_. ]'
    ref_names = [(x, re.sub(sep, sep, x) + sep) for x in ref_names]
    ref_names = sorted(ref_names, key=lambda x: (len(x[1]), x), reverse=True)
    taxon_names = [(x, re.sub(sep, sep, x) + sep) for x in taxon_names]
    taxon_names = sorted(taxon_names, key=lambda x: (len(x[1]), x), reverse=True)
    ref_name = [x[0] for x in ref_names if re.search(x[1], contig_file)]
    taxon_name = [x[0] for x in taxon_names if re.search(x[1], contig_file)]
    ref_name += [None]
    taxon_name += [None]
    return ref_name[0], taxon_name[0]
```

### Example Rosalind problem/solution:
**Finding a Spliced Motif**

```python
from .helpers import Parser

def matches(s1, s2):
    i, j = 0, 0
    while j < len(s2):
        if s2[j] == s1[i]:
            yield i + 1
            j += 1
        i += 1

def main(file):
    s1, s2 = [x.seq for x in Parser(file).fastas()]
    print(*list(matches(s1, s2)))
```

---

## Bioinfo_R_Scripts

### Description:
Bioinfo_R_Scripts is a well-organized GitHub repository featuring useful command-line scripts for bioinformatics. These scripts are written in R (version 3.6 or later) and have been tested on Linux systems. The repository is open-source and freely available for use, modification, and contributions from the community.

The dataset can be found at this link:
[Bioinfo_R_Scripts](https://github.com/rajanbit/Bioinfo_R_Scripts?tab=readme-ov-file)

### Format:
There are two folders in this repository:
- **RNA-Seq_Data_Analysis_Scripts**: Contains R scripts related to RNA-Seq data analysis tasks.
- **Basic_plots**: Contains R scripts for basic plotting tasks.

---

## Biocode

### Description:
This is a collection of bioinformatics scripts many have found useful and code modules which make writing new ones a lot faster. Biocode is a curated repository of general-use utility scripts.

The dataset can be found at this link:
[Biocode](https://github.com/jorvis/biocode)

### Format:
The majority of the scripts are Python with some Perl scripts. The scripts are categorized into the following groupings:
- **blast** - If it uses, massages, or just reformats BLAST output, it goes here.
- **chado** - Scripts that are tied into the chado schema (gmod.org) should be found here.
- **fasta** - Filtering, converting, size distribution plots, etc.
- **fastq** - Utilities for FASTQ format.
- **genbank** - Anything related to the GenBank Flat File Format.
- **general** - Utility scripts that may not fit in any other existing directory.
- **gff** - Extractions, conversions, and manipulations of files in Generic Feature Format.
- **gtf** - Scripts focused on GTF format from Ensembl/WashU.
- **hmm** - Merging, manipulating, or reading HMM libraries.
- **sam_bam** - Analysis of and parsing SAM/BAM files.
- **taxonomy** - Anything related to taxonomic analysis.

---

## Seq-N-Slide: Sequencing Data Analysis Pipelines

### Description:
Seq-N-Slide is a set of streamlined analysis workflows for common genomic sequencing assays, such as RNA-seq, ATAC-seq, ChIP-seq, WGS/WES, and WGBS/RRBS.

The dataset can be found at this link:
[Seq-N-Slide](https://github.com/igordot/sns?tab=readme-ov-file)

### Format:
The dataset consists of shell scripts, R scripts, and Perl scripts that address various sequencing workflows.

---

## Genomics

### Description:
A collection of scripts and notes related to genomics and bioinformatics.

The dataset can be found at this link:
[Genomics](https://github.com/igordot/genomics)

### Format:
The dataset consists of R scripts, shell scripts, and Perl scripts that address various genomics and bioinformatics-related tasks. The scripts folder contains complete scripts for specific tasks. The **scripts-bigpurple** and **scripts-phoenix** folders contain scripts optimized for a specific cluster.
