#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: avigailtaylor
"""

import os

# Configuration file for gf.py and gfmulti.py

QUANT_DATA_TYPE = 'log2 FC' # This will be the label under the colour bar on all heatmaps

DOTPLOTS = True

MIN_NUM_GENES = 10

MAX_DCNT = 50
MIN_LEVEL = 5

TT_OVERLAP_MEASURE = 'OC'
MIN_WEIGHT_TT_EDGE = 0.5

SC_BC_OVERLAP_MEASURE = 'OC'
MIN_WEIGHT_SC_BC = 0.25

BC_BC_OVERLAP_MEASURE = 'J'
MIN_WEIGHT_BC_BC = 0.1

MAX_CLUSTER_SIZE_THRESH = 15
MAX_META_COMMUNITY_SIZE_THRESH = 15

COMBINE_TERM_TYPES = False

HEATMAP_WIDTH_MIN = 10 # These default values are set so that images render at a good size on
HEATMAP_HEIGHT_MIN = 5 # a 15 inch monitor
               
HEATMAP_MIN = -4 # These default values are set to reflect the typical range of
HEATMAP_MAX = 4  # log2 FC data.
         
SEARCH_WORDS = []
             
GENE_INDEX = 7   # These constants are set so that they match the column indices of the expected DEG output
QD_INDEX = 2     # file from the R package enrichR. These can be changed if input file format is different.

MSIGDB_HTML = os.path.dirname(__file__) + "/msigdb_v7.2.filtered.html" # WARNING. THIS SHOULD BE CONSIDERED AS A CONSTANT. ONLY EDIT AFTER READING DOCS.
OBO_FILE = os.path.dirname(__file__) + "/go-basic.obo" # WARNING. THIS SHOULD BE CONSIDERED AS A CONSTANT. ONLY EDIT AFTER READING DOCS.

EA_FILE_PATH = ''
