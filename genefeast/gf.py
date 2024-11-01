#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: avigailtaylor
"""
# IMPORTS *********************************************************************

import os
import sys
import argparse

import networkx as nx
import numpy as np
import pandas as pd
import warnings
import yaml
from bs4 import BeautifulSoup
from goatools import obo_parser
from goatools.gosubdag.gosubdag import GoSubDag
from matplotlib import pyplot
from networkx.algorithms.community import greedy_modularity_communities

from genefeast import gf_base as gfb
from genefeast import gf_classes as gfc
from genefeast import gf_multi

def main():
    warnings.filterwarnings("ignore", category=FutureWarning)
    parser = argparse.ArgumentParser()
#    parser.add_argument("mif_path")
#    parser.add_argument("output_dir")
#    parser.add_argument("cfg_yaml_path")
#    args = parser.parse_args()
#    
#    gf(args.mif_path, args.output_dir, args.cfg_yaml_path)
    
    parser.add_argument("setup_yaml_path")
    parser.add_argument("output_dir")
    args = parser.parse_args()
    
#    with open(args.setup_yaml_path, "r") as ymlfile:
#        setup = yaml.safe_load(ymlfile)
        
    #gf(args.setup_yaml_path, args.output_dir, setup["cfg_yaml_path"])
    (status, message, _mi_dict, _exp_ids) = gfb.get_meta_info_from_setup(args.setup_yaml_path) # mi short for meta input
    if(status > 0):
        print(message)
        sys.exit()
        
    if(len(_exp_ids)>1):
        print("**********\nMultiple FEAs detected. Proceeding with multi FEA report generation.\n**********")
        gf_multi.gf_multi(args.setup_yaml_path, args.output_dir)
    else:
        print("**********\nSingle FEA detected. Proceeding with single FEA report generation.\n**********")
        gf(args.setup_yaml_path, args.output_dir)
    


#def gf(mif_path, output_dir, cfg_yaml_path):
#def gf(setup_yaml_path, output_dir, cfg_yaml_path):
def gf(setup_yaml_path, output_dir):
    # MAIN PROGRAM ****************************************************************
    # 0. CHECK PYTHON VERSION *****************************************************
    if(not(sys.version_info.major==3 and sys.version_info.minor==12)):
        print('GeneFEAST requires Python 3.12. Please make sure you have a compliant version installed.')
        sys.exit()
    
    # 1. SET UP I/O FILES AND DIRECTORIES *****************************************
    print("\nSetting up I/O files and directories")
    #(status, message, mi_dict, exp_ids) = gfb.get_meta_info(mif_path) # mi short for meta input
    (status, message, mi_dict, exp_ids) = gfb.get_meta_info_from_setup(setup_yaml_path) # mi short for meta input
    print(message)
    if(status > 0):
        sys.exit()
    
    # These three variables are synonyms of each other - the different names lend
    # clarity to code downstream, when they are used in different contexts.
    exp_id = exp_ids[0]
    info_string = exp_id
    summary_id = info_string
    
    ora_file_path , gene_qd_file_path , input_img_dir = mi_dict[info_string]
    
    (status, message) = gfb.get_output_dir_status(output_dir)
    print(message)
    if(status == 1):
        sys.exit()
    elif(status == 2):
        sys.exit()
    elif(status == 3):
        os.makedirs(output_dir)
    
    # Make images output directory -- The name of the output directory is a variable (output_dir),
    # however the name of the images directory, placed inside the output directory, is auto-generated
    (rel_images_dir, abs_images_dir) = gfb.generate_images_dirs(info_string, output_dir)
    os.mkdir(abs_images_dir)
    
    # *****************************************************************************
    
    # 2. IMPORT VARIABLES FROM CONFIG FILE ****************************************
    #with open(cfg_yaml_path, "r") as ymlfile:
    #    cfg_yaml = yaml.safe_load(ymlfile)
    print("\nConfiguring variables for report generation")    
    
    with open(setup_yaml_path, "r") as ymlfile:
        setup = yaml.safe_load(ymlfile)
    
#   QUANT_DATA_TYPE = cfg_yaml['QUANT_DATA_TYPE']
    if(setup.get("QUANT_DATA_TYPE") is None):
        QUANT_DATA_TYPE = "log2 FC"
    else:
        QUANT_DATA_TYPE = setup.get("QUANT_DATA_TYPE")

#    DOTPLOTS = cfg_yaml['DOTPLOTS']
    
    if(setup.get("ENRICHR") is None):
        ENRICHR = False
    else:
        ENRICHR = setup.get("ENRICHR")
    
    
    if(setup.get("DOTPLOTS") is None):
        DOTPLOTS = False
    else:
        DOTPLOTS = setup.get("DOTPLOTS")
        
    if(DOTPLOTS and not(ENRICHR)):
        print('*** ERROR: DOTPLOTS is set to True, but ENRICHR is set to False. '
              'Dotplots can only be plotted if ORA/ GSEA results are in Enrichr format (see docs). '
              'Please ensure that ORA/ GSEA results are in Enrichr format, and explicitly set ENRICHR to True in '
              'setup YAML file. (The default value for ENRICHR is False if not given in the setup '
              'YAML file.) ***')
        sys.exit()
    
#    MIN_NUM_GENES = cfg_yaml['MIN_NUM_GENES']
    if(setup.get("MIN_NUM_GENES") is None):
        MIN_NUM_GENES = 10
    else:
        MIN_NUM_GENES = setup.get("MIN_NUM_GENES")
    
#    MAX_DCNT = cfg_yaml['MAX_DCNT']
    if(setup.get("MAX_DCNT") is None):
        MAX_DCNT = 50
    else:
        MAX_DCNT = setup.get("MAX_DCNT")
        
#    MIN_LEVEL = cfg_yaml['MIN_LEVEL']
    if(setup.get("MIN_LEVEL") is None):
        MIN_LEVEL = 3
    else:
        MIN_LEVEL = setup.get("MIN_LEVEL")

#    TT_OVERLAP_MEASURE = cfg_yaml['TT_OVERLAP_MEASURE']
    if(setup.get("TT_OVERLAP_MEASURE") is None):
        TT_OVERLAP_MEASURE = "OC"
    else:
        TT_OVERLAP_MEASURE = setup.get("TT_OVERLAP_MEASURE")

#    MIN_WEIGHT_TT_EDGE = cfg_yaml['MIN_WEIGHT_TT_EDGE']
    if(setup.get("MIN_WEIGHT_TT_EDGE") is None):
        MIN_WEIGHT_TT_EDGE = 0.5
    else:
        MIN_WEIGHT_TT_EDGE = setup.get("MIN_WEIGHT_TT_EDGE")
    
#    SC_BC_OVERLAP_MEASURE = cfg_yaml['SC_BC_OVERLAP_MEASURE']
    if(setup.get("SC_BC_OVERLAP_MEASURE") is None):
        SC_BC_OVERLAP_MEASURE = "OC"
    else:
        SC_BC_OVERLAP_MEASURE = setup.get("SC_BC_OVERLAP_MEASURE")

#    MIN_WEIGHT_SC_BC = cfg_yaml['MIN_WEIGHT_SC_BC']
    if(setup.get("MIN_WEIGHT_SC_BC") is None):
        MIN_WEIGHT_SC_BC = 0.25
    else:
        MIN_WEIGHT_SC_BC = setup.get("MIN_WEIGHT_SC_BC")

#    BC_BC_OVERLAP_MEASURE = cfg_yaml['BC_BC_OVERLAP_MEASURE']
    if(setup.get("BC_BC_OVERLAP_MEASURE") is None):
        BC_BC_OVERLAP_MEASURE = "JI"
    else:
        BC_BC_OVERLAP_MEASURE = setup.get("BC_BC_OVERLAP_MEASURE")

#    MIN_WEIGHT_BC_BC = cfg_yaml['MIN_WEIGHT_BC_BC']
    if(setup.get("MIN_WEIGHT_BC_BC") is None):
        MIN_WEIGHT_BC_BC = 0.1
    else:
        MIN_WEIGHT_BC_BC = setup.get("MIN_WEIGHT_BC_BC")
   
#    MAX_COMMUNITY_SIZE_THRESH = cfg_yaml['MAX_COMMUNITY_SIZE_THRESH']
    if(setup.get("MAX_COMMUNITY_SIZE_THRESH") is None):
        MAX_COMMUNITY_SIZE_THRESH = 15
    else:
        MAX_COMMUNITY_SIZE_THRESH = setup.get("MAX_COMMUNITY_SIZE_THRESH")
        
#    MAX_META_COMMUNITY_SIZE_THRESH = cfg_yaml['MAX_META_COMMUNITY_SIZE_THRESH']
    if(setup.get("MAX_META_COMMUNITY_SIZE_THRESH") is None):
        MAX_META_COMMUNITY_SIZE_THRESH = 15
    else:
        MAX_META_COMMUNITY_SIZE_THRESH = setup.get("MAX_META_COMMUNITY_SIZE_THRESH")
    
#    COMBINE_TERM_TYPES = cfg_yaml['COMBINE_TERM_TYPES']
    if(setup.get("COMBINE_TERM_TYPES") is None):
        COMBINE_TERM_TYPES = False
    else:
        COMBINE_TERM_TYPES = setup.get("COMBINE_TERM_TYPES")    
    
    
#    HEATMAP_WIDTH_MIN = cfg_yaml['HEATMAP_WIDTH_MIN']
    if(setup.get("HEATMAP_WIDTH_MIN") is None):
        HEATMAP_WIDTH_MIN = 10
    else:
        HEATMAP_WIDTH_MIN = setup.get("HEATMAP_WIDTH_MIN")  

#    HEATMAP_HEIGHT_MIN = cfg_yaml['HEATMAP_HEIGHT_MIN']
    if(setup.get("HEATMAP_HEIGHT_MIN") is None):
        HEATMAP_HEIGHT_MIN = 6.5
    else:
        HEATMAP_HEIGHT_MIN = setup.get("HEATMAP_HEIGHT_MIN")  
    
#    HEATMAP_MIN = cfg_yaml['HEATMAP_MIN']
    if(setup.get("HEATMAP_MIN") is None):
        HEATMAP_MIN = -4
    else:
        HEATMAP_MIN = setup.get("HEATMAP_MIN")  

#    HEATMAP_MAX = cfg_yaml['HEATMAP_MAX']
    if(setup.get("HEATMAP_MAX") is None):
        HEATMAP_MAX = 4
    else:
        HEATMAP_MAX = setup.get("HEATMAP_MAX")  
                            
#    if(not(cfg_yaml['SEARCH_WORDS'])):
#        SEARCH_WORDS = []
#    else:
#        SEARCH_WORDS = cfg_yaml['SEARCH_WORDS']
    if(setup.get("SEARCH_WORDS") is None):
        SEARCH_WORDS = []
    else:
        SEARCH_WORDS = setup.get("SEARCH_WORDS")  

                 
#    GENE_INDEX = cfg_yaml['GENE_INDEX'] 
    if(setup.get("GENE_INDEX") is None):
        GENE_INDEX = 0
    else:
        GENE_INDEX = setup.get("GENE_INDEX")  

#    QD_INDEX = cfg_yaml['QD_INDEX']
    if(setup.get("QD_INDEX") is None):
        QD_INDEX = 1
    else:
        QD_INDEX = setup.get("QD_INDEX")  
    
#    EA_FILE = cfg_yaml['EA_FILE']
    EA_FILE = setup.get("EA_FILE")

        
    
    # *****************************************************************************
    
    # 3. DEFINE CONSTANTS *********************************************************
    # Populate the data structures required for plotting GO hierarchies and for
    # storing GO term stats (required for making decions on term inclusion.)
#    if(not(cfg_yaml['OBO_FILE'])):
#        OBO_FILE = os.path.dirname(__file__) + "/go-basic.obo"
#    else:
#        OBO_FILE = cfg_yaml['OBO_FILE']

    print("\nReading in OBO file")
    if(setup.get("OBO_FILE") is None):
        OBO_FILE = os.path.dirname(__file__) + "/go-basic.obo"
    else:
        OBO_FILE = setup.get("OBO_FILE")  
    
        
    GO_DAG = obo_parser.GODag(obo_file=OBO_FILE)
    GO_SUBDAG = GoSubDag(GO_DAG.keys(), GO_DAG, tcntobj=None, children=True, prt=sys.stdout)
    
    _GO_term_stats = {}
    my_go_statsGetter = gfc.go_statsGetter(GO_SUBDAG.go2obj, GO_SUBDAG.go2nt)
    for goid in ['GO:0008150', 'GO:0003674', 'GO:0005575']:
          my_go_statsGetter.get_go_stats(goid, _GO_term_stats)
    
    # We also need to load the html tables for any MSigDB terms we might want to show 
    # - best to keep this a constant, I think...
    
#    if(not(cfg_yaml['MSIGDB_HTML'])):
#        MSIGDB_HTML = os.path.dirname(__file__) + "/msigdb_v7.2.filtered.html"
#    else:
#        MSIGDB_HTML = cfg_yaml['MSIGDB_HTML']
     
    print("\nReading in MSigDB file")  
    if(setup.get("MSIGDB_HTML") is None):
        MSIGDB_HTML = os.path.dirname(__file__) + "/msigdb_v7.2.filtered.html"
    else:
        MSIGDB_HTML = setup.get("MSIGDB_HTML")      
        
    msigdb_file = open(MSIGDB_HTML, "r", encoding='UTF8')
    msigdb_contents = msigdb_file.read()
    msigdb_html_soup = BeautifulSoup(msigdb_contents, features="lxml")
    
    #And this is where we read in any extra gene annotations provided by the user.
    (status, message, _extra_annotations_dict, _num_extra_annotations) = gfb.make_extra_annotations_dict(EA_FILE)
    
    # These are constants for rendering HTML report
    NEW_H = 300
    IMG_EXTENSION = '.png'
    # Notes on IMG_EXTENSION: At the moment, the only file format available for 
    # external, extra, images is png. However, this might change in future releases.
    # To make this extension as easy as possible, IMG_EXTENSION is a constant here,
    # but it is seen as a variable in the classes to which it is passed.
    
    # *****************************************************************************
    
    
    # 4. WRITE LOG FILE ***********************************************************
    log_f = open(output_dir + '/log.txt', 'w')
    log_f.write("MIN_NUM_GENES: " + str(MIN_NUM_GENES) + "\n")
    log_f.write("MAX_DCNT: " + str(MAX_DCNT) + "\n")
    log_f.write("MIN_LEVEL: " + str(MIN_LEVEL) + "\n")
    log_f.write("TT_OVERLAP_MEASURE: " + TT_OVERLAP_MEASURE + "\n")
    log_f.write("MIN_WEIGHT_TT_EDGE: " + str(MIN_WEIGHT_TT_EDGE) + "\n")
    log_f.write("SC_BC_OVERLAP_MEASURE: " + SC_BC_OVERLAP_MEASURE + "\n")
    log_f.write("MIN_WEIGHT_SC_BC: " + str(MIN_WEIGHT_SC_BC) + "\n")
    log_f.write("BC_BC_OVERLAP_MEASURE: " + BC_BC_OVERLAP_MEASURE + "\n")
    log_f.write("MIN_WEIGHT_BC_BC: " + str(MIN_WEIGHT_BC_BC) + "\n")
    log_f.write("MAX_COMMUNITY_SIZE_THRESH: " + str(MAX_COMMUNITY_SIZE_THRESH) + "\n")
    log_f.write("MAX_META_COMMUNITY_SIZE_THRESH: " + str(MAX_META_COMMUNITY_SIZE_THRESH) + "\n")
    log_f.write("COMBINE_TERM_TYPES: " + str(COMBINE_TERM_TYPES) + "\n")
    log_f.write("SEARCH_WORDS: " + str(SEARCH_WORDS))
    log_f.close()
    
    # *****************************************************************************
    
    # 5 READ IN DATA FOR SUMMARISING HERE*****************************
    print("\nReading in FEA for summarization")
    # Store input image directory and extensions
    _exp_img_dir_paths_dict = {}
    _exp_img_dir_paths_dict[exp_id] = input_img_dir
    _exp_img_extension_dict = {}
    _exp_img_extension_dict[exp_id] = IMG_EXTENSION
    
    
    # Read in the ORA/ GSEA data
    (status, message, _term_types_dict, _term_defs_dict, exp_term_genes_dict, _exp_term_dotplot_dict, _) = \
            gfb.read_in_ora_data(ora_file_path, exp_id, MIN_LEVEL, MAX_DCNT, ENRICHR, DOTPLOTS, _GO_term_stats)
    print(message)
    if(status > 0):
        sys.exit()
    
    # Store quantitative data (qd) values (usually log2 FC) for genes
    (status, message, _exp_gene_qd_dict) = gfb.make_gene_qd_dict(gene_qd_file_path, exp_id, GENE_INDEX, QD_INDEX)
    print(message)
    if(status > 0):
        sys.exit()
    
    # Make the dataframe that contains the quantitative data (usually log2 FC) for each gene, in each FEA
    _exp_gene_qd = pd.DataFrame.from_records([(e, g, v) for ((e, g), v) in list(_exp_gene_qd_dict.items())], 
                                                columns = ['FEA', 'Gene', 'QD']).set_index(['FEA', 'Gene'])
    # Sort the indices for faster access later on...
    _exp_gene_qd = _exp_gene_qd.sort_index()
    
    
    # Remove terms that do not have more than MIN_NUM_GENES gene annotations
    (_term_genes_dict, terms_to_remove) = gfb.find_terms_to_remove(exp_term_genes_dict, MIN_NUM_GENES)
    for del_term in terms_to_remove:
        del _term_types_dict[del_term]    
        del _term_defs_dict[del_term]    
        del _term_genes_dict[del_term]    
        if(DOTPLOTS):
            del _exp_term_dotplot_dict[(exp_id, del_term)]
    
    # *****************************************************************************
    
    # 6. CLUSTER TERMS BY THEIR GENE-SET OVERLAP **********************************
    print("\nFinding communities of terms")
    
    # create network of terms - terms are connected by edges if their overlap 
    # weight exceeds a certain threshold. *****************************************
    
    terms_list = list(_term_genes_dict.keys())
    type_2_term_dict = {}
        
    for t in terms_list:
        if _term_types_dict[t].lower() in type_2_term_dict:
            type_2_term_dict[_term_types_dict[t].lower()].append(t)
        else:
            type_2_term_dict[_term_types_dict[t].lower()] = [t]
        
        # For the purposes of combining term types, we have recorded any 
        # GO subtype information in type_2_term_dict. Now this has been done, 
        # we only need to take forward the fact that this is a GO term.
        if _term_types_dict[t].lower()[0 : 2] == "go":
            _term_types_dict[t] = "GO"
    
    
    if(COMBINE_TERM_TYPES or len(type_2_term_dict.keys())==1):    
        terms_graph = gfb.build_terms_graph(terms_list, _term_genes_dict, TT_OVERLAP_MEASURE, MIN_WEIGHT_TT_EDGE)    
        # find 'big' communities of terms. Here 'big' just means not singleton ********
        big_community_term_sets = gfb.get_big_community_term_sets(terms_graph, MAX_COMMUNITY_SIZE_THRESH, TT_OVERLAP_MEASURE, MIN_WEIGHT_TT_EDGE, MAX_DCNT, _term_types_dict, _GO_term_stats, _term_genes_dict)
    
    else:
        big_community_term_sets = []
        type_2_term_dict_keys = list(type_2_term_dict.keys())
        type_2_term_dict_keys.sort()
        
        for type_2_term_dict_key in type_2_term_dict_keys:
            sub_terms_list = type_2_term_dict[type_2_term_dict_key]
            sub_terms_graph = gfb.build_terms_graph(sub_terms_list, _term_genes_dict, TT_OVERLAP_MEASURE, MIN_WEIGHT_TT_EDGE)
            
            # find 'big' communities of terms. Here 'big' just means not singleton ********
            sub_big_community_term_sets = gfb.get_big_community_term_sets(sub_terms_graph, MAX_COMMUNITY_SIZE_THRESH, TT_OVERLAP_MEASURE, MIN_WEIGHT_TT_EDGE, MAX_DCNT, _term_types_dict, _GO_term_stats, _term_genes_dict)
            big_community_term_sets = big_community_term_sets + sub_big_community_term_sets
    
    (big_communities, singleton_communities, meta_communities, singleton_meta_communities) = \
        gfb.build_all_communities_lists(terms_list, big_community_term_sets, 
                                          'community ', 'meta community ', 
                                          SC_BC_OVERLAP_MEASURE, MIN_WEIGHT_SC_BC,
                                          BC_BC_OVERLAP_MEASURE, MIN_WEIGHT_BC_BC,
                                          MAX_META_COMMUNITY_SIZE_THRESH,
                                          QUANT_DATA_TYPE, _exp_gene_qd, exp_ids, 
                                          _term_types_dict, _term_defs_dict, 
                                          _term_genes_dict, _exp_term_dotplot_dict, 
                                          abs_images_dir, rel_images_dir, 
                                          _extra_annotations_dict, _num_extra_annotations,
                                          NEW_H, HEATMAP_WIDTH_MIN, HEATMAP_HEIGHT_MIN,
                                          HEATMAP_MIN, HEATMAP_MAX, SEARCH_WORDS, 
                                          info_string, msigdb_html_soup, GO_DAG, 
                                          _exp_img_dir_paths_dict, _exp_img_extension_dict)
        
    
    term_community_pairs = gfb.get_big_community_labels_for_terms(big_communities)
        
    TEST = False
    if(not(TEST) and (len(big_communities) >= 2) & (len(big_communities) <= (len(term_community_pairs)-1))):
        terms_distance_matrix = gfb.build_terms_distance_matrix(term_community_pairs, _term_genes_dict, TT_OVERLAP_MEASURE)
        print("\nGenerating silhouette plot for communities detected with chosen parameters")
        ( silplot_img_path , silplot_img_width, silplot_img_height ) = gfb.make_silhouette_plot(terms_distance_matrix, np.array([c for (t,c) in term_community_pairs]), big_communities, _term_genes_dict, 
                                                                                                abs_images_dir, rel_images_dir, '', NEW_H * 2.5)
    else:
        # preconditions for silhouette coefficient not met, so generate empty figure.
        pyplot.figure(figsize=(10, 10))
        pyplot.savefig(abs_images_dir + "_sil_plot.png", bbox_inches="tight")
        pyplot.close()
        silplot_img_path = rel_images_dir + "_sil_plot.png"
        silplot_img_width = NEW_H * 2.5
        silplot_img_height = NEW_H * 2.5
    
        # Now run analysis to plot out how clustering looks when varying two thresholds: MIN_WEIGHT_TT_EDGE and MAX_COMMUNITY_SIZE_THRESH
        # TODO: check this works when multiple FEA databases are used and database agglomeration is off!
    
    print("\nGenerating community detection quality comparison plot for grid search of community detection parameters")
    ( comparisonplot_oc_img_path , comparisonplot_oc_img_width, comparisonplot_oc_img_height ) = gfb.make_sil_violinplots(MIN_WEIGHT_TT_EDGE, MAX_COMMUNITY_SIZE_THRESH, COMBINE_TERM_TYPES, type_2_term_dict,
                                                                                                                 terms_list, _term_genes_dict, 'OC', TT_OVERLAP_MEASURE,
                                                                                                                 MAX_DCNT, _term_types_dict, _GO_term_stats, 
                                                                                                                 abs_images_dir, rel_images_dir, '', NEW_H * 2.5)
    

    ( comparisonplot_ji_img_path , comparisonplot_ji_img_width, comparisonplot_ji_img_height ) = gfb.make_sil_violinplots(MIN_WEIGHT_TT_EDGE, MAX_COMMUNITY_SIZE_THRESH, COMBINE_TERM_TYPES, type_2_term_dict,
                                                                                                                 terms_list, _term_genes_dict, 'JI', TT_OVERLAP_MEASURE,
                                                                                                                 MAX_DCNT, _term_types_dict, _GO_term_stats, 
                                                                                                                 abs_images_dir, rel_images_dir, '', NEW_H * 2.5)
            
    # *****************************************************************************
    
    # 7. GENERATE HTML REPORT *****************************************************
    print("\nGenerating HTML report")
    my_summaryPrinter = gfc.summaryPrinter(summary_id, summary_id, output_dir, info_string + '_report.html', rel_images_dir, meta_communities, singleton_meta_communities, singleton_communities,
                                           silplot_img_path, silplot_img_width, silplot_img_height, 
                                           comparisonplot_oc_img_path, comparisonplot_oc_img_width, comparisonplot_oc_img_height,
                                           comparisonplot_ji_img_path, comparisonplot_ji_img_width, comparisonplot_ji_img_height)
    my_summaryPrinter.print_html()
    my_summaryPrinter.print_html('communities_silhouette')
    my_summaryPrinter.print_html('communities_paramcomparison_oc')
    my_summaryPrinter.print_html('communities_paramcomparison_ji')
    
    html_f = open(output_dir + '/' + info_string + '_report.html', 'w')
    html_f.write("<!DOCTYPE html>\n")
    html_f.write("<html>\n")
    
    html_f.write("<head>\n")
    
    jSPrinter = gfc.javaScriptPrinter()
    jSPrinter.print_html( html_f )
    
    html_f.write("<style>\n")
    
    html_f.write(".title {\n")
    html_f.write("  margin: 5px;\n")
    html_f.write("}\n")
    
    html_f.write(".view-button {\n")
    html_f.write("  background-color: inherit;\n")
    html_f.write("  float: left;\n")
    html_f.write("  border: none;\n")
    html_f.write("  outline: none;\n")
    html_f.write("  cursor: pointer;\n")
    html_f.write("  padding: 4px 6px;\n")
    html_f.write("  transition: 0.1s;\n")
    html_f.write("  font-size: 16pxs;\n")
    html_f.write("  margin: 2px;\n")
    html_f.write("}\n")
        
    html_f.write(".view-button:hover {\n")
    html_f.write("  background-color: #0aa8a8;\n")
    html_f.write("  color: white;\n")
    html_f.write("}\n")
    
    html_f.write(".disabled-view-button {\n")
    html_f.write("  background-color: inherit;\n")
    html_f.write("  float: left;\n")
    html_f.write("  border: none;\n")
    html_f.write("  outline: none;\n")
    html_f.write("  padding: 4px 6px;\n")
    html_f.write("  font-size: 16pxs;\n")
    html_f.write("  opacity: 0.3;\n")
    html_f.write("}\n")
    
    html_f.write(".grid-container {\n")
    html_f.write("  display: grid;\n")
    html_f.write("  grid-template-areas:\n")
    html_f.write("    'terms plotbox plotbox plotbox plotbox plotbox'\n")
    html_f.write("    'spacer plot_buttons plot_buttons plot_buttons plot_buttons plot_buttons'\n")
    html_f.write("    'meta extra extra extra extra extra';\n")
    html_f.write("  grid-gap: 10px;\n")
    html_f.write("  background-color: #2196F3;\n")
    html_f.write("  padding: 10px;\n")
    html_f.write("}\n\n")
    
    html_f.write(".terms { grid-area: terms; }\n")
    html_f.write(".plotbox { grid-area: plotbox;\n") 
    html_f.write("          overflow: scroll;}\n")
    html_f.write(".spacer{ grid-area: spacer;}\n")
    html_f.write(".plot_buttons{ grid-area: plot_buttons; }\n")
    html_f.write(".extra { grid-area: extra;\n")  
    html_f.write("          overflow: scroll;}\n")
    html_f.write(".meta { grid-area: meta; }\n") 
    html_f.write("\n")  
    
    html_f.write(".grid-container > div {\n")
    html_f.write("  max-height: "+ str(NEW_H + 30) +"px;\n")
    html_f.write("  overflow: scroll;\n")
    html_f.write("  background-color: rgba(255, 255, 255, 0.8);\n")
    html_f.write("  text-align: left;\n")
    html_f.write("  padding: 15px;\n")
    html_f.write("  font-size: small;\n")
    html_f.write("}\n\n")
        
    html_f.write(".collapsible {\n")
    html_f.write("  background-color: rgba(33, 150, 243, 0.8);\n")
    html_f.write("  color: white;\n")
    html_f.write("  cursor: pointer;\n")
    html_f.write("  padding: 5px;\n")
    html_f.write("  width: 100%;\n")
    html_f.write("  border: none;\n")
    html_f.write("  text-align: left;\n")
    html_f.write("  outline: none;\n")
    html_f.write("  font-size: 15px;\n")
    html_f.write("}\n")
        
    html_f.write(".active, .collapsible:hover {\n")
    html_f.write("  background-color: #2196F3;\n")
    html_f.write("}\n\n")
    
    #***********************************
    
#    html_f.write(".grid-container2 {\n")
#    html_f.write("  display: grid;\n")
#    html_f.write("  grid-template-areas:\n")
#    html_f.write("    'members2 upset2 upset2 upset2 upset2 upset2'\n")
#    html_f.write("    'spacer2a plot_buttons2 plot_buttons2 plot_buttons2 plot_buttons2 plot_buttons2'\n")
#    html_f.write("    'spacer2b heatmap2 heatmap2 heatmap2 heatmap2 heatmap2';\n")
#    html_f.write("  grid-gap: 10px;\n")
#    html_f.write("  background-color: #DC143C;\n")
#    html_f.write("  padding: 10px;\n")
#    html_f.write("}\n\n")

    html_f.write(".grid-container2 {\n")
    html_f.write("  display: grid;\n")
    html_f.write("  grid-template-areas:\n")
    html_f.write("    'members2 upset2 upset2 upset2 upset2 upset2'\n")
    html_f.write("    'spacer2 plot_buttons2 plot_buttons2 plot_buttons2 plot_buttons2 plot_buttons2';\n")
    html_f.write("  grid-gap: 10px;\n")
    html_f.write("  background-color: #DC143C;\n")
    html_f.write("  padding: 10px;\n")
    html_f.write("}\n\n")
    
    
#    html_f.write(".members2 { grid-area: members2; }\n")
#    html_f.write(".heatmap2 { grid-area: heatmap2;\n") 
#    html_f.write("          overflow: scroll;}\n")
#    html_f.write(".spacer2a{ grid-area: spacer2a;}\n")
#    html_f.write(".plot_buttons2{ grid-area: plot_buttons2; }\n")
#    html_f.write(".spacer2b{ grid-area: spacer2b;}\n")
#    html_f.write(".upset2 { grid-area: upset2;\n")  
#    html_f.write("          overflow: scroll;}\n")
#    html_f.write("\n")
        
    html_f.write(".members2 { grid-area: members2;\n")
    html_f.write("          overflow: scroll;}\n")
    html_f.write(".spacer2{ grid-area: spacer2;}\n")
    html_f.write(".plot_buttons2{ grid-area: plot_buttons2; }\n")
    html_f.write(".upset2 { grid-area: upset2;\n")  
    html_f.write("          overflow: scroll;}\n")
    html_f.write("\n") 
        
    
#    html_f.write(".grid-container2 > div {\n")
#    html_f.write("  max-height: "+ str(NEW_H + 30) +"px;\n")
#    html_f.write("  overflow: scroll;\n")
#    html_f.write("  background-color: rgba(255, 255, 255, 0.8);\n")
#    html_f.write("  text-align: left;\n")
#    html_f.write("  padding: 15px;\n")
#    html_f.write("  font-size: small;\n")
#    html_f.write("}\n\n")
    
    html_f.write(".grid-container2 > div {\n")
    #html_f.write("  max-height: "+ str((NEW_H*2) + (30*3)) +"px;\n")
    html_f.write("  max-height: "+ str(NEW_H + 160 + 80) +"px;\n")
    html_f.write("  overflow: scroll;\n")
    html_f.write("  background-color: rgba(255, 255, 255, 0.8);\n")
    html_f.write("  text-align: left;\n")
    html_f.write("  padding: 15px;\n")
    html_f.write("  font-size: small;\n")
    html_f.write("}\n\n")
        
    html_f.write(".collapsible2 {\n")
    html_f.write("  background-color: rgba(220, 20, 60, 0.8);\n")
    html_f.write("  color: white;\n")
    html_f.write("  cursor: pointer;\n")
    html_f.write("  padding: 5px;\n")
    html_f.write("  width: 100%;\n")
    html_f.write("  border: none;\n")
    html_f.write("  text-align: left;\n")
    html_f.write("  outline: none;\n")
    html_f.write("  font-size: 15px;\n")
    html_f.write("}\n")
        
    html_f.write(".active, .collapsible2:hover {\n")
    html_f.write("  background-color: #DC143C;\n")
    html_f.write("}\n\n")
    
    #***********************************
    
    html_f.write(".grid-container3 {\n")
    html_f.write("  display: grid;\n")
    html_f.write("  grid-template-areas:\n")
    html_f.write("    'overlaps3 heatmap3 heatmap3 heatmap3 heatmap3 heatmap3'\n")
    html_f.write("    'spacer3a plot_buttons3 plot_buttons3 plot_buttons3 plot_buttons3 plot_buttons3'\n")
    html_f.write("    'spacer3b extra3 extra3 extra3 extra3 extra3';\n")
    html_f.write("  grid-gap: 10px;\n")
    html_f.write("  background-color: #FFD700;\n")
    html_f.write("  padding: 10px;\n")
    html_f.write("}\n\n")
    
    html_f.write(".overlaps3 { grid-area: overlaps3; }\n")
    html_f.write(".heatmap3 { grid-area: heatmap3;\n") 
    html_f.write("          overflow: scroll;}\n")
    html_f.write(".spacer3a{ grid-area: spacer3a;}\n")
    html_f.write(".plot_buttons3{ grid-area: plot_buttons3; }\n")
    html_f.write(".spacer3b{ grid-area: spacer3b;}\n")
    html_f.write(".extra3 { grid-area: extra3;\n")  
    html_f.write("          overflow: scroll;}\n")
    html_f.write("\n")  
    
    html_f.write(".grid-container3 > div {\n")
    html_f.write("  max-height: "+ str(NEW_H + 30) +"px;\n")
    html_f.write("  overflow: scroll;\n")
    html_f.write("  background-color: rgba(255, 255, 255, 0.8);\n")
    html_f.write("  text-align: left;\n")
    html_f.write("  padding: 15px;\n")
    html_f.write("  font-size: small;\n")
    html_f.write("}\n\n")
        
    html_f.write(".collapsible3a {\n")
    html_f.write("  background-color: rgba(255, 215, 0, 0.8);\n")
    html_f.write("  color: white;\n")
    html_f.write("  cursor: pointer;\n")
    html_f.write("  padding: 5px;\n")
    html_f.write("  width: 100%;\n")
    html_f.write("  border: none;\n")
    html_f.write("  text-align: left;\n")
    html_f.write("  outline: none;\n")
    html_f.write("  font-size: 15px;\n")
    html_f.write("}\n")
        
    html_f.write(".active, .collapsible3a:hover {\n")
    html_f.write("  background-color: #FFD700;\n")
    html_f.write("}\n\n")
            
    html_f.write(".collapsible3b {\n")
    html_f.write("  background-color: rgba(255, 215, 0, 0.8);\n")
    html_f.write("  color: white;\n")
    html_f.write("  cursor: pointer;\n")
    html_f.write("  padding: 5px;\n")
    html_f.write("  width: 100%;\n")
    html_f.write("  border: none;\n")
    html_f.write("  text-align: left;\n")
    html_f.write("  outline: none;\n")
    html_f.write("  font-size: 15px;\n")
    html_f.write("}\n")
        
    html_f.write(".active, .collapsible3b:hover {\n")
    html_f.write("  background-color: #FFD700;\n")
    html_f.write("}\n\n")
            
#    html_f.write(".content {\n")
#    html_f.write("display: none;\n")
#    html_f.write("}\n")
    
    html_f.write(".content {\n")
    html_f.write("display: grid;\n")
    html_f.write("background-color: #FFD700;\n")
    html_f.write("padding-left: 10px;\n")
    html_f.write("padding-top: 10px;\n")
    html_f.write("}\n")
    
    html_f.write(".navgrid-container {\n")
    html_f.write("display: grid;\n")
    html_f.write("grid-template-columns: auto;\n")
    html_f.write("position: fixed; top: 0; left: 0; width:100%; height: 55px; z-index:1;\n")
    html_f.write("}\n")

    html_f.write("ul {\n")
    html_f.write("list-style-type: none;\n")
    html_f.write("margin: 0;\n")
    html_f.write("padding: 0;\n")
    html_f.write("background-color: #088F8F;\n")
    html_f.write("top: 0; left: 0; width: 100%; height: 55px; z-index:1;\n")
    html_f.write("}\n")

    html_f.write("li {\n")
    html_f.write("  float: left;\n")
    html_f.write("}\n")


    html_f.write("li a {\n")
    html_f.write("  display: block;\n")
    html_f.write("  color: white;\n")
    html_f.write("  font-weight: bold;\n")
    html_f.write("  text-align: center;\n")
    html_f.write("  padding: 14px 16px;\n")
    html_f.write("  text-decoration: none;\n")
    html_f.write("}\n")

    #html_f.write("li a:hover:not(.navactive) {\n")
    #html_f.write("  color: black;\n")
    #html_f.write("}\n")

    html_f.write(".navactive {\n")
    html_f.write("  text-decoration:underline;\n")
    html_f.write("}\n")

    html_f.write(".logo {\n")
    html_f.write("  display: block;\n")
    html_f.write("  color: yellow;\n")
    html_f.write("  text-align: center;\n")
    html_f.write("  text-decoration: none;\n")
    html_f.write("  padding: 9px 16px;\n")
    html_f.write("  padding-right: 75px;\n")
    html_f.write("  font-family: arial black, sans-serif;\n") 
    html_f.write("  font-size: 18px;\n")
    html_f.write("}\n")

    html_f.write(".rightlink {\n")
    html_f.write("  float: right;\n")
    html_f.write("}\n")
    
    html_f.write(".subnav {\n")
    html_f.write("  list-style-type: none;\n")
    html_f.write("  margin: 0;\n")
    html_f.write("  padding: 0;\n")
    html_f.write("  overflow: hidden;\n")
    html_f.write("  background-color: #0aa8a8;\n")
    html_f.write("}\n")
    
    html_f.write(".dropdown {\n")
    html_f.write("  float: left;\n")
    html_f.write("  overflow: hidden;\n")
    html_f.write("}\n")
    
    html_f.write(".dropdown .dropbtn {\n")
    html_f.write("  font-size: 16px;\n")  
    html_f.write("  border: none;\n")
    html_f.write("  outline: none;\n")
    html_f.write("  color: white;\n")
    html_f.write("  font-weight: bold;\n")
    html_f.write("  padding: 14px 16px;\n")
    html_f.write("  background-color: inherit;\n")
    html_f.write("  font-family: inherit;\n")
    html_f.write("  margin: 0;\n")
    html_f.write("}\n")
    
    html_f.write(".dropbtnactive {\n")
    html_f.write("  font-size: 16px;\n")  
    html_f.write("  border: none;\n")
    html_f.write("  outline: none;\n")
    html_f.write("  color: white;\n")
    html_f.write("  text-decoration:underline;\n")
    html_f.write("  font-weight: bold;\n")
    html_f.write("  padding: 14px 16px;\n")
    html_f.write("  background-color: inherit;\n")
    html_f.write("  font-family: inherit;\n")
    html_f.write("  margin: 0;\n")
    html_f.write("}\n")

    #html_f.write(".navbar a:hover, .dropdown:hover .dropbtn {\n")
    #html_f.write("  color: black;\n")
    #html_f.write("}\n")

    html_f.write(".dropdown-content {\n")
    html_f.write("  display: none;\n")
    html_f.write("  position: absolute;\n")
    html_f.write("  background-color: #0aa8a8;\n")
    html_f.write("  min-width: 160px;\n")
    html_f.write("  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);\n")
    html_f.write("}\n")

    html_f.write(".dropdown-content a {\n")
    html_f.write("  float: none;\n")
    html_f.write("  color: white;\n")
    html_f.write("  padding: 12px 16px;\n")
    html_f.write("  text-decoration: none;\n")
    html_f.write("  display: block;\n")
    html_f.write("  text-align: left;\n")
    html_f.write("  font-size: small;\n")
    html_f.write("}\n")

    html_f.write(".dropdown-content a:hover {\n")
    html_f.write("  background-color: #088F8F;\n")
    html_f.write("}\n")
        
    html_f.write(".dropdown:hover .dropdown-content {\n")
    html_f.write("  display: block;\n")
    html_f.write("  position:fixed;\n")
    html_f.write("  z-index: 9999;\n")
    html_f.write("}\n")
    html_f.write("\n")

    html_f.write(".dropdownsub {\n")
    html_f.write("  float: left;\n")
    html_f.write("  overflow: hidden;\n")
    html_f.write("}\n")
    html_f.write("\n")

    html_f.write(".dropdown-content .dropdownsub {\n")
    html_f.write("  float: none;\n")
    html_f.write("  text-decoration: none;\n")
    html_f.write("  display: block;\n")
    html_f.write("  text-align: left;\n")
    html_f.write("}\n")
    html_f.write("\n")


    html_f.write(".dropdownsub-content{\n")
    html_f.write("  display: none;\n")
    html_f.write("  position: absolute;\n")
    html_f.write("  background-color: #0aa8a8;\n")
    html_f.write("  min-width: 160px;\n")
    html_f.write("  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);\n")
    html_f.write("}\n")
    html_f.write("\n")


    html_f.write(".dropdownsub-content a {\n")
    html_f.write("  float: none;\n")
    html_f.write("  color: white;\n")
    html_f.write("  padding: 12px 16px;\n")
    html_f.write("  text-decoration: none;\n")
    html_f.write("  display: block;\n")
    html_f.write("  text-align: left;\n")
    html_f.write("  font-size: small;\n")
    html_f.write("}\n")
    html_f.write("\n")


    html_f.write(".dropdownsub:hover .dropdownsub-content {\n")
    html_f.write("  display: block;\n")
    html_f.write("  position:absolute;\n")
    html_f.write("  z-index: 9999;\n")
    html_f.write("  left: 50%;\n")
    html_f.write("}\n")
    html_f.write("\n")


    html_f.write(".dropdownsubsub {\n")
    html_f.write("  float: left;\n")
    html_f.write("  overflow: hidden;\n")
    html_f.write("}\n")
    html_f.write("\n")

    html_f.write(".dropdownsub-content .dropdownsubsub {\n")
    html_f.write("  float: none;\n")
    html_f.write("  text-decoration: none;\n")
    html_f.write("  display: block;\n")
    html_f.write("  text-align: left;\n")
    html_f.write("}\n")
    html_f.write("\n")


    html_f.write(".dropdownsubsub-content{\n")
    html_f.write("  display: none;\n")
    html_f.write("  position: absolute;\n")
    html_f.write("  background-color: #0aa8a8;\n")
    html_f.write("  min-width: 160px;\n")
    html_f.write("  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);\n")
    html_f.write("}\n")
    html_f.write("\n")


    html_f.write(".dropdownsubsub-content a {\n")
    html_f.write("  float: none;\n")
    html_f.write("  color: white;\n")
    html_f.write("  padding: 12px 16px;\n")
    html_f.write("  text-decoration: none;\n")
    html_f.write("  display: block;\n")
    html_f.write("  text-align: left;\n")
    html_f.write("  font-size: small;\n")
    html_f.write("}\n")
    html_f.write("\n")


    html_f.write(".dropdownsubsub:hover .dropdownsubsub-content {\n")
    html_f.write("  display: block;\n")
    html_f.write("  position:absolute;\n")
    html_f.write("  z-index: 9999;\n")
    html_f.write("  left: 50%;\n")
    html_f.write("}\n")
    html_f.write("\n")


    html_f.write(".subtitlebanner {\n")
    html_f.write("  list-style-type: none;\n")
    html_f.write("  margin: 0;\n")
    html_f.write("  padding: 0;\n")
    html_f.write("  overflow: hidden;\n")
    html_f.write("  background-color: #0aa8a8;\n")
    html_f.write("  margin-top:110px;\n")
    html_f.write("  z-index:1\n")
    html_f.write("}\n\n")
    
    html_f.write("</style>\n")
    html_f.write("</head>\n")
    
    
    html_f.write('<body style="background-color:#0aa8a8; font-family: arial, sans-serif;">\n')
        
        
    html_f.write('<div class="navgrid-container">\n')
    html_f.write('<div>\n')
    html_f.write('<ul>\n')
    html_f.write('<li class="logo">GeneFEAST</li>\n')
    html_f.write('</ul>\n')
    html_f.write('</div>\n')
        
    html_f.write('<div>\n')
    html_f.write('<ul class="subnav">\n')
    html_f.write('<li class="dropdown">\n')
    html_f.write('<button class="dropbtn" onclick="document.location=\'' + summary_id + '_communities_summary.html\'">Communities overview</button>\n')
    html_f.write('<div class="dropdown-content">\n')
    html_f.write('<a href="' + summary_id + '_communities_summary.html">List of communities</a>\n')
    html_f.write('<a href="' + summary_id + '_communities_silhouette.html">Silhouette plot</a>\n')
    
    
    #html_f.write('<a href="' + summary_id + '_communities_paramcomparison.html">Graphical grid search of community detection parameters</a>\n')
    html_f.write('<div class="dropdownsub" style="width:450px">\n')
    html_f.write('<a href="javascript:;">Graphical grid search of community detection parameters</a>\n')
    html_f.write('<div class="dropdownsub-content" style="width:450px">\n')
    html_f.write('<a href="' + summary_id + '_communities_paramcomparison_oc.html">Graphical grid search of community detection parameters (OC)</a>\n')
    html_f.write('<a href="' + summary_id + '_communities_paramcomparison_ji.html">Graphical grid search of community detection parameters (JI)</a>\n')
    html_f.write('</div>\n')
    html_f.write('</div>\n')
    
    
    html_f.write('</div>\n')
    html_f.write('</li> \n')   
        
        
    html_f.write('<li class="dropdown">\n')
    html_f.write('<button class="dropbtnactive" onclick="document.location=\'' + info_string + '_report.html' + '\'">Full report</button>\n')
    html_f.write('<div class="dropdown-content">\n')    
        
    
    if(len(meta_communities)==0):
        html_f.write('<a href="#">Meta communities</a>\n')
    else:
        html_f.write('<div class="dropdownsub" style="width:300px">\n')
        html_f.write('<a href="' + info_string + '_report.html' + '#' + meta_communities[0].name + '">Meta communities</a>\n')
        html_f.write('<div class="dropdownsub-content">\n')
                     
        for mg in meta_communities:
            html_f.write('<div class="dropdownsubsub" style="width:300px">\n')
            html_f.write('<a href="' + info_string + '_report.html' + '#' + mg.name + '">' + mg.name + '</a>\n' )
            
            html_f.write('<div class="dropdownsubsub-content" style="width:600px;max-height:200px;overflow:scroll;">\n')
            for bc in mg.communities:
                html_f.write('<a href="' + info_string + '_report.html' + '#' + bc.name + '">' + bc.name + ' ' + bc.top_term + '</a>\n')
            
            html_f.write('</div>\n')
                
            html_f.write('</div>\n')
        
        html_f.write('</div>\n')
        html_f.write('</div>\n')
    
    
    if(len(singleton_meta_communities)==0):
        html_f.write('<a href="javascript:;">Communities</a>\n')
    else:
        html_f.write('<div class="dropdownsub" style="width:300px">\n')
        html_f.write('<a href="' + info_string + '_report.html' + '#' + singleton_meta_communities[0].name + '">Communities</a>\n')
        html_f.write('<div class="dropdownsub-content" style="width:600px;max-height:200px;overflow:scroll;">\n')
        for bc in singleton_meta_communities:
            html_f.write('<a href="' + info_string + '_report.html' + '#' + bc.name + '">' + bc.name + ' ' + bc.top_term + '</a>\n')
        
        html_f.write('</div>\n')
        html_f.write('</div>\n')         
    
    if(len(singleton_communities)==0):
        html_f.write('<a href="#">Terms</a>\n')
    else:
        html_f.write('<div class="dropdownsub" style="width:300px">\n')
        html_f.write('<a href="' + info_string + '_report.html' + '#' + singleton_communities[0].name + '">Terms</a>\n')
        html_f.write('<div class="dropdownsub-content" style="width:600px;max-height:200px;overflow:scroll;">\n')
        for sc in singleton_communities:
            if( sc.name == sc.all_term_defs_dict[ sc.name ] ):
                html_f.write('<a href="' + info_string + '_report.html' + '#' + sc.name + '">' + sc.name + '</a>\n' )
            else:
                html_f.write('<a href="' + info_string + '_report.html' + '#' + sc.name + '">' + sc.name + ' - ' + sc.all_term_defs_dict[ sc.name ]  + '</a>\n' )
        html_f.write('</div>\n')
        html_f.write('</div>\n')  
    
    html_f.write('</div>\n')
    html_f.write('</li>\n')
    
        
    html_f.write('<li class="rightlink"><a style="color:white;">' + summary_id + '</a></li>\n')
    html_f.write('</ul>\n')
    html_f.write('</div>\n')
    html_f.write('</div>\n')    
        
    
    first_print = True
    for mc in meta_communities:
        mc.print_html(html_f, summary_id + '_communities_summary.html', first_print)
        first_print = False
        
        for bc in mc.communities:
            bc.print_html(html_f, summary_id + '_communities_summary.html', first_print)
            
    for bc in singleton_meta_communities:
        bc.print_html(html_f, summary_id + '_communities_summary.html', first_print)
        first_print = False
        
    for sc in singleton_communities:
        sc.print_html(html_f, summary_id + '_communities_summary.html', first_print)
        first_print = False
       
    
    jSPrinter.print_html_for_event_listeners( html_f )
    
    html_f.write("</body>\n")
    html_f.write("</html>\n")
    html_f.close()
    
    print("\nGenerating csv files")
    csv_f = open(output_dir + '/' + info_string + '_report.csv', 'w')
    for mc in meta_communities:
        for bc in mc.communities:
            bc.print_csv(csv_f)
            
    for bc in singleton_meta_communities:
        bc.print_csv(csv_f)
        
    for sc in singleton_communities:
        sc.print_csv(csv_f)
        
    csv_f.close()
    
    print("\nDONE!\n")

if __name__ == "__main__":
    main()