## Split heatmap

The split heatmap, a data visualisation developed by us, underpins GeneFEAST (see figure, below). Using this visualisation, we can simultaneously depict term-gene and FEA-gene relationships, as well as gene-level quantitative data, for communities of terms and their contributing genes. Crucially, the format can show multiple FEA results simultaneously, if required. Hierarchical clustering of genes based on their quantitative data highlights global gene-data patterns contributing to enrichments (Figure A). Alternatively, first ordering genes by the number of annotations that they have, and then by their annotation pattern, highlights subsets of genes contributing to multiple enrichments. Within these subsets, genes are also hierarchicaly clustered based on their quantitative data, thus highlighting local gene-data patterns contributing to enrichments that are specific to the subsets (Figure B).

(Back to [User Guide](user_guide.md))

![Split heatmap](https://avigailtaylor.github.io/GeneFEAST/split_heatmap.png)

**Split heatmap.** (A) A pair of heatmaps, sharing a common x-axis of genes, are drawn one on top of the other. In the top heatmap, genes (G1 to G20) are coloured yellow when they are annotated by a term (T1 to T5), otherwise grey. In the bottom heatmap, genes are coloured to depict gene-level quantitative data; in this case log2 fold change from two RNA-Seq experiments whose genes of interest, i.e. differentially expressed genes, were analysed using a FEA (FEA1 and FEA2). Grey genes were not identified as genes of interest in the underlying experiment. The genes are ordered based on hierarchical clustering of their quantitative data. (B) As for (A), but genes are ordered first by their annotation count, then by annotation pattern, and lastly by their quantitative data.

(Back to [User Guide](user_guide.md))
