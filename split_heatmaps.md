## Split heatmap

GeneFEAST is underpinned by the split heatmap, a data visualisation that we developed (Figure 1). Using this visualisation, we can simultaneously depict term-GoI and experiment-GoI relationships, as well as gene-level quantitative data, for communities of terms and their associated GoI. Crucially, the format can show GoI data from multiple experiments simultaneously, thus enabling a gene-centric comparison of FEA results arising from those multiple experiments. Hierarchical clustering of genes based on their quantitative data highlights global gene-data patterns contributing to enrichments (Figure 1A). Alternatively, ordering genes first by the number of annotations that they have, and then by their annotation pattern, highlights subsets of genes contributing to multiple enrichments. Within each of these subsets, genes are then hierarchically clustered based on their quantitative data, thus highlighting local, subset-specific gene-data patterns contributing to enrichments (Figure 1B).

### Extra annotations

Sometimes, you may wish to keep track of an *a priori* set of genes relevant to your study, for example genes contributing to a particular biological signature, throughout the GeneFEAST report. In such cases, you can provide extra annotations to be added as rows to the term-GoI heatmap in all split heatmaps of the report (Figure 2). This is done *post hoc* once communities, and meta communities, and their associated GoI have been identified.

(Back to [User Guide](user_guide.md))

![Split heatmap](https://avigailtaylor.github.io/GeneFEAST/sh.png)

**Figure 1. Split heatmap.** (**A**) A pair of heatmaps, sharing a common x-axis of genes, are drawn one on top of the other. In the top heatmap, GoI (G1 to G20) are coloured yellow when they are annotated by a term (T1 to T5), otherwise grey. In the bottom heatmap, genes are coloured to depict gene-level quantitative data; in this case log2 fold change from two RNA-Seq experiments whose GoI, i.e. differentially expressed genes, were analysed using a FEA (E1 and E2). Grey genes were not identified as GoI in the underlying experiment. The genes are ordered based on hierarchical clustering of their quantitative data. (**B**) As for (**A**), but genes are ordered first by their annotation count, then by annotation pattern, and lastly by their quantitative data.

***

![Split heatmap](https://avigailtaylor.github.io/GeneFEAST/sh_EA.png)

**Figure 2. Split heatmap with extra annotation.** A split heatmap with an extra annotation (EA1) added as a row on top of the existing term-GoI heatmap. GoI labelled with the extra annotation are coloured in pink, with the remaining GoI coloured in grey.

(Back to [User Guide](user_guide.md))
