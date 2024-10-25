# User Guide

<mark><b>October 2024: This user guide is being edited to reflect changes in GeneFEAST!! It is incomplete and cannot be used as-is. The user guide should be finished by the end of the month.</b></mark>

### Installation

#### Option 1: Don't install! Instead, download the GeneFEAST ready-to-use [docker](https://docs.docker.com/get-docker/) container!

To download the latest container from the [repository](https://github.com/avigailtaylor/GeneFEAST/pkgs/container/genefeast):
```
docker pull ghcr.io/avigailtaylor/genefeast:latest
```


#### Option 2:  Locally install the package and its dependencies

1. Install Python 3.12
2. Install Graphviz
3. [Create and activate a virtual Python environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment).
* <mark>We **strongly recommend** installing GeneFEAST in a **virtual environment** because of its [dependencies and requirements](dependencies_and_requirements.md).</mark>
* <mark>**NOTE:** Create a virtual environment using Python 3.12 explicitly, rather than your computer's default version.</mark>
4. Install the most recent version of setuptools:
* Unix/macOS: `pip install --upgrade setuptools`
* Windows: `py -m pip install --upgrade setuptools`
5. Install GeneFEAST:
* Unix/macOS: `pip install genefeast`
* Windows: `py -m pip install genefeast`


### Usage

##### To run GeneFEAST, you will need:

<details>
<summary>Functional enrichment analysis (FEA) results file</summary>

- CSV file containing the results of a functional enrichment analysis (FEA) that has been run on a list of genes of interest (GoI).
- The file should have the following four columns, in this order:

<table>
  <tr><td><b>Type</b></td><td><b>ID</b></td><td><b>Description</b></td><td><b>GeneID</b></td></tr>
</table>
  
    - Type: Term type/ originating database
    - ID: Term ID in database
    - Description: Term description
    - GeneID: "/"-separated list of gene IDs corresponding to GoIs annotated by the term

<details>
   <summary>Example</summary>
  
<table>
  <tr><td><b>Type</b></td><td><b>ID</b></td><td><b>Description</b></td><td><b>GeneID</b></td></tr>
  <tr>
    <td>"GO"</td>
    <td>"GO:0071774"</td>
    <td>"response to fibroblast growth factor"</td>
    <td>"CCN2/THBS1/EGR3/FGF2/SPRY4/<br>NDST1/CCL2/IER2/FLRT3/PRKD2/<br>CXCL8/SPRY2/FRS2/FGFR1/SPRY1/<br>RUNX2/HYAL1/KDM5B/NOG/ZFP36L1/<br>COL1A1/CASR/FGFR3/FGF1/EXT1/<br>FGFBP1/GATA3/NR4A1"</td>
  </tr>
  <tr>
    <td>"GO"</td>
    <td>"GO:0002294"</td>
    <td>"CD4-positive alpha-beta T cell differentiation involved in immune response"</td>
    <td>"RARA/BCL6/SMAD7/SOCS3/PTGER4/<br>JUNB/ZC3H12A/FOXP1/ENTPD7/NFKBIZ/<br>NLRP3/RC3H1/RORC/RIPK2/ANXA1/<br>RELB/MYB/IL6/LGALS9/GATA3"</td>
  </tr>
  <tr>
    <td>"GO"</td>
    <td>"GO:2000514"</td>
    <td>"regulation of CD4-positive alpha-beta T cell activation"</td>
    <td>"RARA/BCL6/SMAD7/JUNB/RUNX1/<br>ZC3H12A/NFKBIZ/NLRP3/RC3H1/CD274/<br>CBLB/RIPK2/ANXA1/AGER/RUNX3/<br>SOCS1/VSIR/PRKCQ/LGALS9/GATA3"</td>
  </tr>
</table>

```
Type,ID,Description,GeneID
    
"GO","GO:0071774","response to fibroblast growth factor","CCN2/THBS1/EGR3/FGF2/SPRY4/NDST1/CCL2/IER2/FLRT3/PRKD2/CXCL8/SPRY2/FRS2/FGFR1/SPRY1/RUNX2/HYAL1/KDM5B/NOG/ZFP36L1/COL1A1/CASR/FGFR3/FGF1/EXT1/FGFBP1/GATA3/NR4A1"
"GO","GO:0002294","CD4-positive alpha-beta T cell differentiation involved in immune response","RARA/BCL6/SMAD7/SOCS3/PTGER4/JUNB/ZC3H12A/FOXP1/ENTPD7/NFKBIZ/NLRP3/RC3H1/RORC/RIPK2/ANXA1/RELB/MYB/IL6/LGALS9/GATA3"
"GO","GO:2000514","regulation of CD4-positive alpha-beta T cell activation","RARA/BCL6/SMAD7/JUNB/RUNX1/ZC3H12A/NFKBIZ/NLRP3/RC3H1/CD274/CBLB/RIPK2/ANXA1/AGER/RUNX3/SOCS1/VSIR/PRKCQ/LGALS9/GATA3"
``` 

</details>
</details>


<details>
<summary>Optional/ Advanced: Format <a href="https://cran.r-project.org/web/packages/enrichR/vignettes/enrichR.html">enrichR</a> output for use with GeneFEAST</summary>
<br>
   
  - GeneRatio (Required only when dot plots are switched on)
  - BgRatio (Required only when dot plots are switched on)
  - pvalue (Optional; field can be empty) 
  - p.adjust (Required only when dot plots are switched on)
  - qvalue (Optional; field can be empty)
  - geneID (**Required**. This should be a list of gene IDs separated using the "/" symbol. The gene IDs ***must match*** those used in the genes of interest file (see next))
  - count (Required only when dot plots are switched on. This is the number of genes of interest annotated with the term. This should match the length of the list of genes given in the geneID column.)

</details>

<details>
<summary>Genes of interest (GoI) file</summary>
  
- CSV file containing the list of Genes of Interest (GoI) that were the input for the FEA being summarised. 
- The file should contain one GoI per line, each with its corresponding quantitative data as measured in the high-throughput 'omics experiment in which the GoI were identified. 
  
  <details>
   <summary>Example</summary>

   
   |GeneID|log2FC|
   |------|------|
   |PDGFB|2.845276684|
   |GTPBP4|1.396754262|
   |C12orf49|1.469143469|
   |SLC2A1|1.618759309|
   |CCN2|2.593769464|
   |CXCR4|2.528192609|
   |NCOA5|2.137989231|
   |CDKN1A|3.154969844|
   |RARA|1.444539048|

  <mark>**NOTE:**</mark>
  - <mark>GoI ***must*** be listed using ***IDs that match those used in the FEA results file***.</mark>
  - <mark>If you do not have quantitative data, you can just provide a dummy column with the same *numerical* value entered for each gene.</mark>

</details>
</details>

<details>
   <summary>A YAML setup file</summary>
   <br>
You will use your setup file to tell GeneFEAST the id(s) of the FEA(s) to summarise, the location(s) of the FEA file(s), and the location(s) of the GoI file(s).
<br>
To summarise a single FEA:

```
FEAs:
    - id: "FEA_1"
      goi_file_path: "full/file/path/to/goi_file_for_FEA_1"
      fea_file_path: "full/file/path/to/FEA_1_results_file"
```

To summarise a multiple FEAs (e.g. three FEAs):
```
FEAs:
    - id: "FEA_1"
      goi_file_path: "full/file/path/to/goi_file_for_FEA_1"
      fea_file_path: "full/file/path/to/FEA_1_results_file"

    - id: "FEA_2"
      goi_file_path: "full/file/path/to/goi_file_for_FEA_2"
      fea_file_path: "full/file/path/to/FEA_2_results_file"

    - id: "FEA_3"
      goi_file_path: "full/file/path/to/goi_file_for_FEA_3"
      fea_file_path: "full/file/path/to/FEA_3_results_file"
```
  
   You can create one using [this template](config_template.yml).
</details>

#### In addition, you can also provide GeneFEAST with:
- Pre-made PNG images for significantly enriched/ over-represented terms. One example might be KEGG pathway images generated as part of the FEA.
  - For each FEA being summarised you have the option of providing a directory (folder) containing at most one image for each enriched/ over-represented term identified in that FEA.
  - The path for this directory will be given along with the FEA results and genes of interest files (described above), when the main call to GeneFEAST is made. Note that these paths will be provided in a simple **meta-input** file which you will need to compose prior to running GeneFEAST. Instructions for writing this file are in the next section, below.
  - > **IMPORTANT**
    > - GeneFEAST automatically generates a GO hierarchy for all terms with a Type string starting "GO" (or "go", "Go", and "gO"; case is ignored). So, if you provide a corresponding image for such a term, this will be ignored. The work around here, should you wish to provide alternative images for GO terms, is to change their Type field in the FEA file to be something other than a string starting with "GO" (or "go", "Go", and "gO").
    > - Similarly, for MSIGDB terms, GeneFEAST will always try to include an HTML tabular description of the term, and any provided image will be ignored. As for GO terms, the work around here is to change the Type field in the FEA file to be something other than a string starting with "MSIGDB" (or any other case variant).
- Search terms for to be searched for alongside your GoI.
  - As part of the report generation process, GeneFEAST conducts a literature search for each GoI, via the National Center for Biotechnology Information's Gene and PubMed services (Sayers, et al., 2021). You can provide a list of search terms via the [config file](config_template.yml), and the literature search will incorporate them.
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

#### Running GeneFEAST through a ready-to-use [docker](https://docs.docker.com/get-docker/) container:

If you are running GeneFEAST through its [docker](https://docs.docker.com/get-docker/) container, then, to summarize results from a single FEA, type the following on the command line:

```bash
# assuming that the input YAML and data files are located in ${PWD}.
docker run --rm -v ${PWD}:/data -w /data ghcr.io/avigailtaylor/genefeast gf <YAML_CONFIG_FILE> <OUTPUT_DIR> 
```

Or, to summarize results from multiple FEAs, type the following on the command line:

```bash
# assuming that the input YAML and data files are located in ${PWD}.
docker run --rm -v ${PWD}:/data -w /data ghcr.io/avigailtaylor/genefeast gf_multi <YAML_CONFIG_FILE> <OUTPUT_DIR> 
```

---

#### Running an installed copy of GeneFEAST:

If you have installed GeneFEAST, then you can either run it on the command line, or you can run it from inside Python.

To use GeneFEAST to summarize results from a single FEA, type the following on the command line:

```bash
gf <YAML_CONFIG_FILE> <OUTPUT_DIR> 
```

Alternatively, in Python:

```python
from genefeast import gf

gf.gf(<YAML_CONFIG_FILE>, <OUTPUT_DIR>)
```

To use GeneFEAST to summarize results from multiple FEAs, type the following on the command line:

```bash
gf_multi <YAML_CONFIG_FILE> <OUTPUT_DIR>
```

Alternatively, in Python:

```python
from genefeast import gf_multi

gf_multi.gf_multi(<YAML_CONFIG_FILE>, <OUTPUT_DIR>)
```

***

#### Viewing the GeneFEAST report

##### Single FEA summary report
To view a GeneFEAST single FEA summary report, navigate to the output directory (specified by you in the `<OUTPUT_DIR>` parameter, above) and use a web browser to open 
file `<FEA_IDENTIFIER>_communities_summary.html`.

##### Multi FEA summary report

To view a GeneFEAST multi FEA summary report, navigate to the output directory and use a web browser to open file `<FEA_IDENTIFIERS>_main.html`.

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
- an upset plot showing the overlap between sets of genes annotated by the member terms;
- [split heatmaps](split_heatmaps.md) of the term- and experiment-GoI relationships, gene-level quantitative data and extra annotations, if supplied; 
- further information about terms, such as GO hierarchies and KEGG pathway diagrams;
- and external hyperlinks to literature searches for each gene of interest, incorporating additional search terms if you have supplied them.

Where applicable, community frames have links to their meta community and also to sibling communities in their meta community (red, solid arrows); separately, they also have a list of links to terms sharing some gene-set overlap, but which is too weak for membership of the community (red, dashed arrow). 

Term frames have similar, reduced content of community frames. In particular, they do not include upset plots and dot plots, and the term-gene heatmap element of their [split heatmap](split_heatmaps.md) is extended to highlight which genes, if any, contribute to enriched terms that have been clustered into a community; in this case the corresponding gene-community pair is depicted in the heatmap. Term frames have links back to weakly connected communities (red, dashed arrow).

Meta community frames contain: split heatmaps, wherein term annotation is replaced by gene-community membership in the top heatmap, a literature search for each gene (as described above), and an upset plot showing the overlap between sets of genes annotated by the member communities. Meta community frames have links to member communities (red, solid arrow)

Reports summarising multiple FEAs start with a 'main' page showing an upset plot of the sets of terms identified as enriched in each of the analyses (left green box). We refer to each set of terms found in two or more FEAs as an *"FEA term-set intersection"*. The main page also has an additional side panel (on the right, not shown here) displaying a list of links to separate reports for each intersection. Each of the separate reports has the structure of a report summarising a single FEA, as described above.

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
