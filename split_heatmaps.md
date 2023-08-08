## Split heatmap

The split heatmap, a data visualisation developed by us, underpins GeneFEAST (see figure, below). Using this visualisation, we can simultaneously depict term-gene and FEA-gene relationships, 
as well as gene level quantitative data, for communities of terms and their contributing genes. Crucially, the format can show multiple FEA results simultaneously, if required. Ordering genes based on 
hierarchical clustering of their quantitative data highlights global gene data centric patterns contributing to enrichments (Figure A). Alternatively, ordering genes by their term annotation counts and term annotation patterns 
highlights gene sets contributing to multiple enrichments; within these gene sets, genes are again ordered based on quantitative data, thus highlighting gene set specific, gene data centric patterns contributing to enrichments (Figure B).

(Back to [User Guide](user_guide.md))

![Split heatmap](https://avigailtaylor.github.io/GeneFEAST/split_heatmap.png)

**Split heatmap.** (A) A pair of heatmaps, sharing a common x-axis of genes, are drawn one on top of the other. In the top heatmap, genes (G1 to G20) are coloured yellow when they are annotated by a term (T1 to T5), otherwise grey. In the bottom heatmap, genes are coloured to depict the gene level quantitative data from the experiments which were analysed using FEA; in this case log2 fold change from two RNA-Seq experiments (FEA1 and FEA2); grey genes were not identified as genes of interest in the underlying experiment. The genes are ordered based on hierarchical clustering of their quantitative data. (B) As for (A), but genes are ordered first by their term annotation count, then by term annotation pattern, and lastly by their quantitative data.

(Back to [User Guide](user_guide.md))
