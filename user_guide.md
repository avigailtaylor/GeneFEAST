# User Guide

## Installation

We **strongly recommend** installing GeneFEAST in a **virtual environment** because the library has several dependencies and requirements:

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

```$ pip install genefeast```

## Usage

#### To run GeneFEAST you will need:
- **FEA results file**. This is a comma-separated file containing the results of a functional enrichment analysis (FEA) that has been run on a list of genes of interest (GoI) identified via a high-throughput 'omics experiment. (For example, an RNA-Seq experiment used to identify the set of genes differentially expressed between an experimental condition and a control condition).  GeneFEAST expects a file containing the following ten columns, in this order:
  - Type (**Required**. This refers to the type of the term and can be, e.g., GO, KEGG, MSIGDB, etc.)
  - ID (**Required**)
  - Description (**Required**)
  - GeneRatio (Required only when dot plots are switched on)
  - BgRatio (Required only when dot plots are switched on)
  - pvalue (Optional; field can be empty) 
  - p.adjust (Required only when dot plots are switched on)
  - qvalue (Optional; field can be empty)
  - geneID (**Required**. This should be a list of gene IDs separated using the "/" symbol. The gene IDs ***must match*** those used in the genes of interest file (see next))
  - count (Required only when dot plots are switched on. This is the number of genes of interest annotated with the term. This should match the length of the list of genes given in the geneID column.)
    
- **Genes of interest file**: A file containing the list of GoI that were the input for the FEA being summarised. The file should contain one GoI per line, each with its corresponding quantitative data measured in the high-throughput 'omics experiment in which the GoI were identified. For example, in an RNA-Seq experiment this could be the log2 fold change observed between an experimental condition and a control condition. Please note: 
  - GoI ***must*** be listed using ***IDs that match those used in the FEA results file***.
  - You will use the [config file](config_template.yml) to tell GeneFEAST which column contains gene IDs, and which column contains quantitative data.
  - If you do not have quantitative data, you can just provide a dummy column with the same *numerical* value entered for each gene.
  - There can be other columns in the file - these will be ignored.
 
- **A YAML config file**. You can create one using [this template](config_template.yml).

#### In addition, you can also provide GeneFEAST with:
- Pre-made PNG images for significantly enriched/ over-represented terms. One example might be KEGG pathway images generated as part of the FEA.
  - For each FEA being summarised you have the option of providing a directory (folder) containing at most one image for each enriched/ over-represented term identified in that FEA.
  - The path for this directory will be given along with the FEA results and genes of interest files (described above), when the main call to GeneFEAST is made. Note that these paths will be provided in a simple **meta-input** file which you will need to compose prior to running GeneFEAST. Instructions for writing this file are in the next section, below.
  - > **IMPORTANT**
    > - GeneFEAST automatically generates a GO hierarchy for all terms with a Type string starting "GO" (or "go", "Go", and "gO"; case is ignored). So, if you provide a corresponding image for such a term, this will be ignored. The work around here, should you wish to provide alternative images for GO terms, is to change their Type field in the FEA file to be something other than a string starting with "GO" (or "go", "Go", and "gO").
    > - Similarly, for MSIGDB terms, GeneFEAST will always try to include an HTML tabular description of the term, and any provided image will be ignored. As for GO terms, the work around here is to change the Type field in the FEA file to be something other than a string starting with "MSIGDB" (or any other case variant).
- Extra annotations for genes.
  - Sometimes, you may wish to keep track of an *a priori* set of genes relevant to your study, for example those that are members of a particular biological signature, throughout the GeneFEAST report. To do this, you can provide GeneFEAST with an extra annotation (EA) file. The EA file is a headerless, comma-separated file with one extra annotation per row, and two columns: The first column is the extra annotation name, and the second column is the list of genes to be labelled with the extra annotation. Note that this list must be delimited using the "/" symbol.
  - Each extra annotation will be displayed as an additional row at the top of the term-GoI heatmap panel in the [split heatmap](split_heatmaps.md) created for each community of terms (similarly for each meta community of communities).
  - In order for GeneFEAST to use the EA file, you need to provide a path to it in the  [config file](config_template.yml).
- A GO OBO file
  - GeneFEAST ships with a GO OBO file, but if you want to provide a more recent version of this yourself, you can provide a path to this file in the [config file](config_template.yml).
- MSIGDB HTML file.
  - GeneFEAST ships with an MSIGDB HTML file containing an HTML tabular summary of each MSIGDB term, but if you want to provide a more recent version of this yourself, you can provide a path to this file in the [config file](config_template.yml).

#### Finally, before running GeneFEAST, create a meta-input file:
- Headerless, comma-separated file.
- One row per FEA to be summarised.
- Four fields per row:
  - FEA name/ identifier. (**Required**)
    - This should **match**, or somehow make reference to, the **'omics experiment** used to identify the GoI that were input into the FEA. **Must be unique**.
  - Path to FEA results file. (**Required**)
  - Path to Genes of interest file. (**Required**)
  - Path to additional images directory. (Optional. You can leave this field blank.)

---

#### Running GeneFEAST. What you need to do:

To use GeneFEAST to summarize results from a single FEA, type the following on the command line:

```
    $ gf META_INPUT_FILE \
         OUTPUT_DIR \
         YAML_CONFIG_FILE
```

Alternatively, in Python:

```python
from genefeast import gf

gf.gf(META_INPUT_FILE, OUTPUT_DIR, YAML_CONFIG_FILE)
```

To use GeneFEAST to summarize results from multiple FEAs, type the following on the command line:

```
    $ gf_multi META_INPUT_FILE \
               OUTPUT_DIR \
               YAML_CONFIG_FILE
```

Alternatively, in Python:

```python
from genefeast import gf_multi

gf_multi.gf_multi(META_INPUT_FILE, OUTPUT_DIR, YAML_CONFIG_FILE)
```
***

#### Viewing the GeneFEAST report

##### Single FEA summary report
To view a GeneFEAST single FEA summary report, navigate to the output directory (specified by you in the OUTPUT_DIR parameter, above) and use a web browser to open 
file *<FEA_IDENTIFIER>_communities_summary.html*.

##### Multi FEA summary report

To view a GeneFEAST multi FEA summary report, navigate to the output directory and use a web browser to open file *<FEA_IDENTIFIERS>_main.html*.

> **IMPORTANT**
> Viewing the HTML output report requires a web-browser with HTML5 and JavaScript 1.6 support.

> **IMPORTANT**
> Please make sure to keep all the output generated by GeneFEAST in the output directory; the HTML report uses relative links to images, and will break if the relative directory structure is broken.

***
#### Navigating the GeneFEAST report

The figure below summarises the structure of HTML reports generated by GeneFEAST:

![GeneFEAST Report structure](https://avigailtaylor.github.io/GeneFEAST/report_structure.png)

Reports summarising one FEA have a 'Communities summary' homepage (green box, top centre) that has links (black, solid arrows) to each meta community (red boxes), with a separate link to each member community therein (blue boxes); the homepage also has links to communities of enriched terms that did not form part of a larger meta community (isolated blue box, right), and links to terms that did not form part of an enriched-term community (yellow box). Every meta community, community and term has a frame of information, implemented in HTML and CSS, which can be scaled to fit your monitor. Within each frame, JavaScript enables toggling of content. 

For each community of enriched terms, GeneFEAST reports: 

- member terms;
- a dot plot summary of member term’s FEA results; 
- an upset plot (Lex, et al., 2014) showing the overlap between sets of genes annotated by the member terms;
- [split heatmaps](split_heatmaps.md) of the term- and experiment-GoI relationships, gene-level quantitative data and extra annotations, if supplied; 
- further information about terms, such as GO hierarchies and KEGG pathway diagrams;
- and external hyperlinks to literature searches for each gene of interest, via the National Center for Biotechnology Information's Gene and PubMed services (Sayers, et al., 2021), incorporating additional search terms if the user has supplied them.

Where applicable, community frames have links back to their meta community and also to sibling communities in their meta community (red, solid arrows); separately, they also have a list of links to terms sharing some gene-set overlap, but which is too weak for membership of the community (red, dashed arrows). 

Term frames have similar, reduced content of community frames. In particular, they do not include upset plots and dot plots, and the term-gene heatmap element of their [split heatmap](split_heatmaps.md) is extended to highlight which genes, if any, contribute to enriched terms that have been clustered into a community; in this case the corresponding gene-community pair is depicted in the heatmap.

Meta community frames have: links to member communities (red, solid arrows), [split heatmaps](split_heatmaps.md), wherein term annotation is replaced by gene-community membership in the top heatmap, a literature search for each gene (as described above), and an upset plot showing the overlap between sets of genes annotated by the member communities.

Reports summarising multiple FEAs start with a 'main' page showing an upset plot of the sets of terms identified as enriched in each of the analyses (left green box). We refer to the sets of terms found in two or more FEAs as *"FEA term-set intersections"*. On the right side panel of this main page (not shown here) is a list of links to separate reports for each intersection, each of which has the structure of a report summarising a single FEA, as described above.

***

#### Additional GeneFEAST output

Term-community membership, term- and experiment-GoI relationships are also output in comma-separated value format, for input into downstream programs. The columns are:

- Community (will be empty if a term is not part of a community)
- Meta community (will be empty if a community is not part of a meta community)
- FEA/experiment identifier
- Term
- Gene
- Quantitative data for gene

> **NOTE**
> This table structure is necessarily repetitive, with possible multiple entries per gene. In particular, each gene has one entry per FEA/experiment-term pair where:
> - the gene was identified as a GoI in the experiment that underwent FEA,
> - the gene is annotated by the term,
> - and the term has been identified as significantly enriched in the FEA.
