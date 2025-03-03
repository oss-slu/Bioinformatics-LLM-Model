import requests
import json
import time

# List of top 100 Bioconductor package names
package_names = [
    "BiocVersion", "BiocGenerics", "GenomeInfoDb", "S4Vectors", "zlibbioc", "IRanges", "XVector", 
    "Biobase", "Biostrings", "GenomicRanges", "DelayedArray", "BiocParallel", "MatrixGenerics", 
    "S4Arrays", "SparseArray", "SummarizedExperiment", "AnnotationDbi", "KEGGREST", "limma", 
    "UCSC.utils", "BiocFileCache", "Rhtslib", "edgeR", "Rsamtools", "GenomicAlignments", "Rhdf5lib", 
    "DESeq2", "ggtree", "biomaRt", "treeio", "rhdf5", "rtracklayer", "clusterProfiler", "enrichplot", 
    "rhdf5filters", "BiocIO", "DOSE", "graph", "fgsea", "GOSemSim", "GenomicFeatures", "qvalue", 
    "annotate", "SingleCellExperiment", "DelayedMatrixStats", "beachmat", "BSgenome", "ComplexHeatmap", 
    "sparseMatrixStats", "HDF5Array", "preprocessCore", "BiocSingular", "ScaledMatrix", "multtest", 
    "genefilter", "VariantAnnotation", "AnnotationHub", "ProtGenerics", "BiocNeighbors", 
    "AnnotationFilter", "impute", "ensembldb", "GEOquery", "scuttle", "RBGL", "Rgraphviz", "GSEABase", 
    "affyio", "affy", "ExperimentHub", "sva", "GSVA", "scater", "BiocBaseUtils", "MultiAssayExperiment", 
    "ShortRead", "bluster", "BiocStyle", "biomformat", "interactiveDisplayBase", "phyloseq", 
    "KEGGgraph", "pcaMethods", "biovizBase", "EnhancedVolcano", "DNAcopy", "pwalign", "vsn", "glmGamPoi", 
    "geneplotter", "metapod", "DirichletMultinomial", "scran", "pathview", "SpatialExperiment", 
    "biocViews", "TCGAbiolinks", "SingleR", "batchelor", "assorthead", "seqLogo", "ResidualMatrix", 
    "apeglm", "MsCoreUtils", "TFBSTools", "tximport", "CNEr", "basilisk", "Gviz", "txdbmaker", "monocle", 
    "dir.expiry", "mzR", "basilisk.utils", "siggenes", "graphite", "MSnbase", "mzID", 
    "ConsensusClusterPlus", "alabaster.base", "alabaster.matrix", "illuminaio", "OrganismDbi", "topGO", 
    "DECIPHER", "EBImage", "alabaster.ranges", "flowCore", "ReactomePA", "alabaster.se", "bumphunter", 
    "mixOmics", "RProtoBufLib", "cytolib", "alabaster.schemas", "QFeatures", "AUCell", "maftools", 
    "gypsum", "DropletUtils", "dada2", "minfi", "Rsubread", "gdsfmt", "snpStats", "AnnotationForge", 
    "MAST", "TreeSummarizedExperiment", "ChIPseeker", "ggbio", "InteractionSet", "TrajectoryUtils", 
    "marray", "aroma.light", "PSMatch", "regioneR", "Spectra", "msa", "MetaboCoreUtils", "globaltest", 
    "microbiome", "BiocCheck", "EDASeq", "SNPRelate", "MassSpecWavelet", "Category", "oligo", "decontam", 
    "oligoClasses", "scDblFinder", "xcms", "metagenomeSeq", "Wrench", "affxparser", "slingshot", 
    "methylumi", "UCell", "GOstats", "zellkonverter", "bsseq", "singscore", "mia", "DEXSeq", "goseq", 
    "MsFeatures", "tkWidgets", "widgetTools", "dittoSeq", "DynDoc", "Mfuzz", "motifmatchr", 
    "MsExperiment", "densvis", "STRINGdb", "survcomp", "GENIE3", "GenomicFiles", "Nebulosa", "ANCOMBC", 
    "PCAtools", "lumi", "systemPipeR", "ALDEx2", "decoupleR", "plyranges", "chromVAR", "MultiDataSet", 
    "gcrma", "ropls", "infercnv", "flowWorkspace", "ROC", "DiffBind", "ggtreeExtra", "ncdfFlow", 
    "RcisTarget", "FlowSOM", "DMRcate", "ChIPpeakAnno", "missMethyl", "Glimma", "GenomicDataCommons", 
    "bamsignals", "GreyListChIP", "tximeta", "flowViz", "affyPLM", "GlobalAncova", "MungeSumstats", 
    "alabaster.sce", "Maaslin2", "simplifyEnrichment", "variancePartition", "SeqArray", "lpsymphony", 
    "RUVSeq", "RCy3", "universalmotif", "zinbwave", "wateRmelon", "gage", "ggcyto", "RaggedExperiment", 
    "ChemmineR", "sangerseqR", "karyoploteR", "sesame", "DSS", "fastseg", "seqPattern", "celda", 
    "flowClust", "minet", "viper", "TCGAutils", "motifStack", "OmnipathR", "ChAMP", "IHW", "genomation", 
    "EpiDISH", "destiny", "beadarray", "GenomicScores", "rGREAT", "methylKit", "safe", "chipseq", 
    "quantsmooth", "R4RNA", "openCyto", "TSCAN", "GWASTools", "gwascat", "trackViewer", "NOISeq", 
    "DEGreport", "LoomExperiment", "LEA", "scRepertoire", "SPIA", "EnrichedHeatmap", "M3C", "MotifDb", 
    "M3Drop", "GeneOverlap", "ReportingTools", "CATALYST", "DEP", "ballgown", "BeadDataPackR", "flowAI", 
    "csaw", "tradeSeq", "derfinder", "derfinderHelper", "EnrichmentBrowser", "ggmsa", "MSstats", "AnVIL", 
    "rrvgo", "muscat", "MOFA2", "lefser", "RTCGAToolbox", "quantiseqr", "iSEE", "MicrobiotaProcess", 
    "ggkegg", "scMerge", "Heatplus", "baySeq", "Rbowtie", "scds", "BumpyMatrix", "annotatr", "CAMERA", 
    "flowStats", "RTCGA", "MSstatsConvert", "arrayQualityMetrics", "diffcyt", "progeny", "UniProt.ws", 
    "MsBackendMgf", "piano", "SeqVarTools", "TCseq", "SRAdb", "CytoML", "splatter", "TOAST", "rols", 
    "cmapR", "Rdisop", "ArrayExpress", "MLInterfaces", "escape", "Icens", "GenomicInteractions", 
    "iClusterPlus", "CGHbase", "miloR", "Organism.dplyr", "scde", "affycoretools", 
    "InteractiveComplexHeatmap", "pcaExplorer", "qusage", "ATACseqQC", "GeomxTools", "recount", 
    "NanoStringNCTools", "CGHcall", "EBSeq", "rWikiPathways", "soGGi", "cBioPortalData", "ChIPQC", 
    "mbkmeans", "eds", "supraHex", "AIMS", "GENESIS", "muscle", "QuasR", "rGADEM", "microbiomeMarker", 
    "AnnotationHubData"
]

GITHUB_API_BASE = "https://api.github.com/repos/Bioconductor"
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "Mozilla/5.0"
}

# OPTIONAL: Add a GitHub token to increase API limits
GITHUB_TOKEN = ""  # Add your token here
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"

package_r_code = {}
scraped_count = 0  # Counter for successfully scraped packages
max_scrapes = 100  # Stop after 100 packages
output_file = "bioconductor_r_code.json"

def check_rate_limit():
    """Check remaining GitHub API rate limit."""
    url = "https://api.github.com/rate_limit"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        rate_info = response.json()
        remaining = rate_info["rate"]["remaining"]
        reset_time = rate_info["rate"]["reset"]
        return remaining, reset_time
    return None, None

def wait_for_rate_limit():
    """Wait until rate limit resets."""
    remaining, reset_time = check_rate_limit()
    if remaining is not None and remaining == 0:
        wait_time = 15
        print(f"Rate limit exceeded. Waiting for {wait_time:.2f} seconds...")
        time.sleep(wait_time)

def get_r_files_from_github(package_name):
    """Fetch all R files in the package's GitHub 'R/' directory."""
    api_url = f"{GITHUB_API_BASE}/{package_name}/contents/R?ref=devel"
    r_code = {}

    for _ in range(3):  # Retry up to 3 times in case of failure
        try:
            wait_for_rate_limit()
            response = requests.get(api_url, headers=HEADERS)
            if response.status_code == 403:
                print(f"⚠️ Rate limited while fetching {package_name}. Retrying...")
                time.sleep(10)
                continue
            if response.status_code != 200:
                print(f"⚠️ Could not access {package_name}/R directory (Status: {response.status_code})")
                return None

            files = response.json()
            for file in files:
                if file["type"] == "file" and file["name"].endswith(".R"):
                    file_url = file["download_url"]
                    file_content = download_file(file["name"], file_url)
                    if file_content:
                        r_code[file["name"]] = file_content
            return r_code if r_code else None

        except Exception as e:
            print(f"Error processing {package_name}: {e}")
            time.sleep(1)  # Wait before retrying
    return None

def download_file(file_name, file_url):
    """Download and return the content of an R file."""
    response = requests.get(file_url, headers=HEADERS)
    if response.status_code == 200:
        return response.text
    else:
        print(f"⚠️ Could not fetch {file_url}")
        return None

# Iterate through the packages and fetch R files
for package in package_names:
    if scraped_count >= max_scrapes:
        break  # Stop when 100 packages are scraped

    print(f"Fetching R files for {package}...")
    r_code = get_r_files_from_github(package)

    if r_code:
        package_r_code[package] = r_code
        scraped_count += 1
        print(f"Successfully scraped {package} ({scraped_count}/{max_scrapes})")
        time.sleep(1)  # Introduce delay to avoid triggering rate limits

# Save the results
if package_r_code:
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(package_r_code, f, indent=4, ensure_ascii=False)

    print(f"\nScraping complete! {scraped_count} packages successfully scraped.")
    print(f"R code saved to {output_file}")
else:
    print("\nNo R files were successfully scraped.")

print(f"\nStopped at package: {package}")