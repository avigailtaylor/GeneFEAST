# GeneFEAST

GeneFEAST, implemented in Python, is a gene-centric functional enrichment analysis summarisation and visualisation tool that can be applied to large functional enrichment analysis (FEA) results arising from any upstream FEA pipeline. It produces a systematic, navigable HTML report, making it easy to identify sets of genes putatively driving multiple enrichments and to explore gene-level quantitative data first used to identify input genes. Further, GeneFEAST can compare FEA results from multiple studies, making it possible to, for example, highlight patterns of gene expression amongst genes commonly differentially expressed in two sets of conditions, and giving rise to shared enrichments under those conditions. GeneFEAST offers a novel, effective way to address the complexities of linking up many, overlapping FEA results to their underlying genes and data; advancing gene-centric hypotheses, and providing pivotal information for downstream validation experiments.

## Installation

We **strongly recommend** installing GeneFEAST in a **virtual environment** because the library has several requirements:

- python == 3.7
- matplotlib == 3.3.3
- numpy == 1.17.2
- pandas == 0.25.2
- upsetplot == 0.4.1
- goatools == 1.0.14
- scipy == 1.3.2
- networkx == 2.5
- lxml == 4.4.1
- beautifulsoup4 == 4.8.0
- pillow == 6.2.0
- PyYAML == 5.1.2


> Please follow the instructions at the top of **[this guide](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)** to create and activate a virtual environment. Please only follow the instructions to the end of section **Activating a virtual environment** and then **come back here**.


> **IMPORTANT**
> If you do not have Python 3.7 installed on your computer, you will need to install it first, ***before*** creating a virtual environment.
> 
> (As an example, to install Python 3.7 on Ubuntu you would follow **[these instructions](https://vegastack.com/tutorials/how-to-install-python-3-7-on-ubuntu-20-04)**.)
>
> Once this is done, make sure to create the virtual environment using Python 3.7 explicitly (i.e. not just the default Python used by your computer).


Once you have created and activated your virtual environment, you can install the library using pip:

> $ pip install genefeast

## Usage

#### To run GeneFEAST you will need:
- **FEA results file**: A comma-delimited file containing the results of a functional enrichment analysis (FEA). GeneFEAST expects a file containing the following ten columns, in this order:
  - Type (**Required**. This refers to the the type of the term and can be, e.g., GO, KEGG, MSIGDB, etc.)
  - ID (**Required**)
  - Description (**Required**)
  - GeneRatio (Required only when dot plots are switched on)
  - BgRatio (Required only when dot plots are switched on)
  - pvalue (Optional; field can be empty) 
  - p.adjust (Required only when dot plots are switched on)
  - qvalue (Optional; field can be empty)
  - geneID (**Required**. This should be a "/" delimited list of gene IDs. The gene IDs ***must match*** those used in the genes of interest file (see next))
  - count (Required only when dot plots are switched on. This is the number of genes of interest annotated with the term. This should match the length of the list of genes given in the geneID column.)
    
- **Genes of interest file**: A file containing a list of genes of interest, one per line, each with their corresponding quantitative data (eg log2 fold change from an RNASeq analyses). Please note:
  - Genes of intersest ***must*** be listed using ***IDs that match those used in the FEA results file***.
  - There can be other columns in the file - these will be ignored.
  - You will use the [config file](config_template.yml) to tell GeneFEAST which column contains gene IDs, and which column contains quantitative data.
  - If you do not have quantitative data, you can just provide a dummy column with the same *numerical* value entered for each gene.
 
- **A YAML config file**. You can create one using [this template](config_template.yml).

#### In addition, you can also provide GeneFEAST with:
- Pre-made PNG images for significantly enriched/ over-represented terms. One example might be KEGG pathway images generated as part of the FEA.
  - For each FEA being summarised you have the option of providing a directory (folder) containing at most one image for each enriched/ over-represented term identified in that FEA.
  - The path for this directory will be given along with the FEA results and genes of interest files (described above), when the main call to GeneFEAST is made. Note that these paths will be provided in a simple **meta input** file which you will need to compose prior to running GeneFEAST. Instructions for writing this file are in the next section, below.
  - > **IMPORTANT**
    > - GeneFEAST automatically generates a GO heirarchy for all terms with a Type string starting "GO" (or "go", "Go", and "gO"; case is ignored). So if you provide a corresponding image for such a term, this will be ignored. The work around here is to change the Type field in the FEA file to be something other than a string starting with "GO" (or "go", "Go", and "gO").
    > - Similarly, for MSIGDB terms, GeneFEAST will always try to include an HTML tabular description of the term, and any provided image will be ignored. As for GO terms, the work around here is to change the Type field in the FEA file to be something other than a string starting with "MSIGDB" (or any other case variant).
- Extra annotations for genes.
  - Sometimes, you may wish to keep track of an *a priori* set of interesting genes, for example those that are members of a particular biological signature, throughout the GeneFEAST report. To do this, you can provide GeneFEAST with an extra annotation (EA) file. The EA file is a headerless, comma delimited file with one extra annotation per row, and two columns: The first column is the extra annotation name, and the second column is a "/" delimited list of genes annotated with the extra annotation.
  - Each extra annotation will be displayed as an additional row at the top of the term-gene heatmap panel in the split heatmap that is created for each community of terms (similarly for each meta-community of communities).
  - In order for GeneFEAST to use the EA file, you need to provide a path to it in the  [config file](config_template.yml).
- A GO OBO file
  - GeneFEAST ships with a GO OBO file, but if you want to provide more up-to-date version of this yourself you can provide a path to this file in the [config file](config_template.yml).
- MSIGDB HTML file.
  - GeneFEAST ships with an MSIGDB HTML file containing an HTML tabular summary of each MSIGDB term, but if you want to provide a more up-to-date version of this yourself, you can provide a path to this file in the [config file](config_template.yml).

#### Finally, before running GeneFEAST, create a meta input file:
- Headerless, comma delimited file.
- One row per FEA to be summarised.
- Four fields per row:
  - FEA name/ identifier. You choose this. Must be unique. (**Required**)
  - Path to FEA results file. (**Required**)
  - Path to Genes of interest file. (**Requried**)
  - Path to additional images directory. (Optional. You can leave this field blank.)
