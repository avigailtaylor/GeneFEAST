# Example input data and output reports

> The gene expression data used in this example is from: 
>
> Pinto SM, Subbannayya Y, Kim H, Hagen L, Górna MW, Nieminen AI, Bjørås M, Espevik T, Kainov D, Kandasamy RK. Multi-OMICs landscape of SARS-CoV-2-induced host responses in human lung epithelial cells. iScience. 2023 Jan 20;26(1):105895. doi: 10.1016/j.isci.2022.105895. Epub 2022 Dec 28. PMID: 36590899; PMCID: PMC9794516.

### Download the following example input and meta-input files:

Example FEA results file, [GO_BP_3h_0.001_4GF.csv](https://avigailtaylor.github.io/GeneFEAST/GO_BP_3h_0.001_4GF.csv)
Example Genes of interest file, [mmc2_goi_3h.csv](https://avigailtaylor.github.io/GeneFEAST/mmc2_goi_3h.csv)
Example config file, [mmc2_3h_config.yml](https://avigailtaylor.github.io/GeneFEAST/mmc2_3h_config.yml)

### Download the following example meta-input file:

Example meta input file, [meta_3h.txt](https://avigailtaylor.github.io/GeneFEAST/meta_3h.txt)

> !IMPORTANT! Now open this file and put in the full path to your downloaded copies of GO_BP_3h_0.001_4GF.csv and mmc2_goi_3h.csv.


### Now run GeneFEAST in one of the following three ways:

If you are running GeneFEAST through its [docker](https://docs.docker.com/get-docker/) container:
```
docker run --volume $HOME:$HOME --workdir $(pwd) ghcr.io/avigailtaylor/genefeast:latest gf <full/path/to/meta_3h.txt> <OUTPUT_DIR> <full/path/to/mmc2_3h_config.yml>
```

If you are running GeneFEAST through the command line
```
    $ gf <full/path/to/meta_3h.txt> \
         <OUTPUT_DIR> \
         <full/path/to/mmc2_3h_config.yml>
```

Alternatively, in Python:

```python
from genefeast import gf

gf.gf(<full/path/to/meta_3h.txt>, <OUTPUT_DIR>, <full/path/to/mmc2_3h_config.yml>)
```
> In all three of these examples, <OUTPUT_DIR> can be whatever you want it to be, so long as it does not already exist.

---
### Comparing your output to the example output

Once you have run GeneFEAST, you can compare your output to [this example output](https://avigailtaylor.github.io/GeneFEAST/mmc2_3h_output.zip)
