# R-Based Datasets

## GEN242  

**Link:** [GEN242 Tutorials](https://girke.bioinformatics.ucr.edu/GEN242/tutorials/rprogramming/rprogramming/)  

**Description:**  
This website contains a plethora of online tutorials on R programming, data analysis techniques, and bioinformatics workflows such as RNA-Seq and ChIP-Seq. It also covers automation, interactive applications (Shiny), and package development, making it a valuable resource for gathering data on structured and domain-specific R coding. Since these examples are organized in a textbook/tutorial format, we can also mine code-text pairs to better guide the fine-tuning process.

**Code Example:**  
```r
appendStep(sal) <- LineWise(code = { 
    bampaths <- getColumn(sal, step = "bwa_alignment", "outfiles", 
        column = "samtools_sort_bam") 
    fqpaths <- getColumn(sal, step = "bwa_alignment", "targetsWF", 
        column = "FileName1") 
    read_statsDF <- alignStats(args = bampaths, fqpaths = fqpaths, 
        pairEnd = TRUE) 
    write.table(read_statsDF, "results/alignStats.xls", row.names = FALSE, 
        quote = FALSE, sep = "\t") 
}, step_name = "align_stats", dependency = "bwa_alignment", run_step = "optional")
```

---

## Ebits  

**Link:** [Ebits Repository](https://github.com/mschubert/ebits?utm_source=chatgpt.com)  

**Description:**  
The ebits repository is a collection of R code modules designed to make bioinformatics workflows easier. It includes tools for handling data frames, working with arrays, and performing high-speed computing tasks. Since the code is modular and covers key bioinformatics functions, we can use it to fine-tune a bioinformatics-focused LLM by providing examples that improve its ability to understand computation-focused code in bioinformatics.

**Code Example:**  
```r
gene.matrix = function(obj, to, from=.guess$id_type(narray::dimnames(obj, along=1)), 
                       dset=.guess$dset(narray::dimnames(obj, along=1)), summarize=mean) { 
    if (to %in% c("hgnc_symbol", "mgi_symbol")) 
        to = "external_gene_name" 
 
    lookup = .gene_table(dset) 
    df = na.omit(data.frame(from = as.character(lookup[[from]]), 
                            to = as.character(lookup[[to]]))) 
    df = df[!duplicated(df),] 
 
    # remove versions of gene ids 
    if (from == "ensembl_gene_id") { 
        if (is.array(obj)) 
            dimnames(obj)[[1]] = sub("\\.[0-9]+$", "", dimnames(obj)[[1]]) 
        else 
            names(obj) = sub("\\.[0-9]+$", "", dimnames(obj)[[1]]) 
    } 
 
    narray::translate(obj, along=1, from=df$from, to=df$to, FUN=summarize) 
}
```

---

## Bioinformatics Workshop Gitbook  

**Link:** [Bioinformatics Workshop Gitbook](https://corytophanes.github.io/BIO_BIT_Bioinformatics_209/getting-started-with-r.html)  

**Description:**  
This book includes R coding tutorials on working with protein and nucleotide sequences, covering tasks such as importing sequences, translating nucleotides to amino acids, and analyzing protein properties. These structured examples provide code-text pairs that can be used to fine-tune an R-based LLM, helping it better understand bioinformatics workflows. By training on these scenarios, the model can generate more accurate R code for sequence analysis and protein-related computations.

**Code Example:**  
```r
## Translating DNA/RNA: 
my_aa_translated_Biostrings_set <- Biostrings::translate(my_nuc_Biostrings_set, genetic.code= 
SGC1, no.init.codon=FALSE) 
my_aa_translated_Biostrings_set 
```

---

## ClustAssess  

**Link:** [ClustAssess Repository](https://github.com/Core-Bioinformatics/ClustAssess/tree/main)  

**Description:**  
The ClustAssess repository provides an R package for checking how reliable clustering results are, especially in single-cell RNA sequencing data. It includes tools to see if data points consistently group together, helping researchers find the most stable clusters. Using this repository to fine-tune an LLM would improve its ability to aid in clustering analysis in bioinformatics.

**Code Example:**  
```r
seurat_clustering <- function(object, resolution, seed, algorithm = 3, num_start = 10, num_iter = 
10, ...) { 
    if (algorithm != 4) { 
        cluster_result <- Seurat::FindClusters( 
            object, 
            resolution = resolution, 
            random.seed = seed, 
            algorithm = algorithm, 
            n.start = num_start, 
            n.iter = num_iter, 
            ... 
        ) 
        return(as.integer(cluster_result[[colnames(cluster_result)[1]]])) 
    } 
 
    if (!(inherits(object, "igraph"))) { 
        object <- Seurat::as.sparse(object) 
        is_nn <- all(object@x == 1) 
        if (is_nn) { 
            object <- igraph::graph_from_adjacency_matrix( 
                adjmatrix = object, 
                mode = "directed" 
            ) 
        } else { 
            object <- igraph::graph_from_adjacency_matrix( 
                adjmatrix = object, 
                mode = "undirected", 
                weighted = TRUE 
            ) 
        } 
    } 
 
    cluster_result <- leiden::leiden( 
        object = object, 
        weights = igraph::E(object)$weight, 
        resolution = resolution, 
        n_iterations = num_iter, 
        seed = seed, 
        ... 
    ) 
    return(cluster_result) 
}
```

---

## bulkAnalyseR  

**Link:** [bulkAnalyseR Repository](https://github.com/Core-Bioinformatics/bulkAnalyseR/tree/main)  

**Description:**  
The bulkAnalyseR repository provides an R package that helps create interactive web apps for analyzing and sharing bulk sequencing data, like mRNA and sRNA sequencing. It allows users to run standard analyses, visualize results, and explore data using customizable Shiny apps, making bioinformatics workflows more accessible and reproducible. Fine-tuning an R-based LLM with this repository would improve its ability to generate code for interactive data analysis in bioinformatics.

**Code Example:**  
```r
DEplotPanelApp <- function(){ 
  shinyApp( 
    ui = navbarPage("DE", tabPanel("", tabsetPanel(DEpanelUI('RNA'), 
DEplotPanelUI('RNA')))), 
    server = function(input, output, session){ 
      DEresults <- DEpanelServer('RNA') 
      DEplotPanelServer('RNA', DEresults) 
    } 
  ) 
}
