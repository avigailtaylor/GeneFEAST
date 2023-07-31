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
import pandas as pd
import yaml
from bs4 import BeautifulSoup
from goatools import obo_parser
from goatools.gosubdag.gosubdag import GoSubDag
from networkx.algorithms.community import greedy_modularity_communities

from genefeast import gf_base as gfb
from genefeast import gf_classes as gfc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mif_path")
    parser.add_argument("output_dir")
    parser.add_argument("cfg_yaml_path")
    args = parser.parse_args()
    
    gf(args.mif_path, args.output_dir, args.cfg_yaml_path)


def gf(mif_path, output_dir, cfg_yaml_path):
    # MAIN PROGRAM ****************************************************************
    # 0. CHECK PYTHON VERSION *****************************************************
    if(not(sys.version_info.major==3 and sys.version_info.minor==7)):
        print('GeneFEAST requires Python 3.7. Please make sure you have a compliant version installed.')
        sys.exit()
    
    # 1. SET UP I/O FILES AND DIRECTORIES *****************************************
    
    (status, message, mi_dict, exp_ids) = gfb.get_meta_info(mif_path) # mi short for meta input
    print(message)
    if(status > 0):
        sys.exit()
    
    # These three variables are synonyms of each other - the different names lend
    # clarity to code downstream, when they are used in different contexts.
    exp_id = exp_ids[0]
    info_string = exp_id
    summary_id = info_string
    
    ora_file_path , gene_qd_file_path , input_img_dir_path = mi_dict[info_string]
    
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
    with open(cfg_yaml_path, "r") as ymlfile:
        cfg_yaml = yaml.safe_load(ymlfile)
        
    print(cfg_yaml)
    
    QUANT_DATA_TYPE = cfg_yaml['QUANT_DATA_TYPE']
    
    DOTPLOTS = cfg_yaml['DOTPLOTS']
    
    MIN_NUM_GENES = cfg_yaml['MIN_NUM_GENES']
    
    MAX_DCNT = cfg_yaml['MAX_DCNT']
    MIN_LEVEL = cfg_yaml['MIN_LEVEL']
    
    TT_OVERLAP_MEASURE = cfg_yaml['TT_OVERLAP_MEASURE']
    MIN_WEIGHT_TT_EDGE = cfg_yaml['MIN_WEIGHT_TT_EDGE']
    
    SC_BC_OVERLAP_MEASURE = cfg_yaml['SC_BC_OVERLAP_MEASURE']
    MIN_WEIGHT_SC_BC = cfg_yaml['MIN_WEIGHT_SC_BC']
    
    BC_BC_OVERLAP_MEASURE = cfg_yaml['BC_BC_OVERLAP_MEASURE']
    MIN_WEIGHT_BC_BC = cfg_yaml['MIN_WEIGHT_BC_BC']
    
    MAX_CLUSTER_SIZE_THRESH = cfg_yaml['MAX_CLUSTER_SIZE_THRESH']
    MAX_META_COMMUNITY_SIZE_THRESH = cfg_yaml['MAX_META_COMMUNITY_SIZE_THRESH']
    
    COMBINE_TERM_TYPES = cfg_yaml['COMBINE_TERM_TYPES']
    
    HEATMAP_WIDTH_MIN = cfg_yaml['HEATMAP_WIDTH_MIN']
    HEATMAP_HEIGHT_MIN = cfg_yaml['HEATMAP_HEIGHT_MIN']
    
    HEATMAP_MIN = cfg_yaml['HEATMAP_MIN']
    HEATMAP_MAX = cfg_yaml['HEATMAP_MAX']
                            
    if(not(cfg_yaml['SEARCH_WORDS'])):
        SEARCH_WORDS = []
    else:
        SEARCH_WORDS = cfg_yaml['SEARCH_WORDS']
                 
    GENE_INDEX = cfg_yaml['GENE_INDEX'] 
    QD_INDEX = cfg_yaml['QD_INDEX']
    
    EA_FILE = cfg_yaml['EA_FILE']
    
    # *****************************************************************************
    
    # 3. DEFINE CONSTANTS *********************************************************
    # Populate the data structures required for plotting GO hierarchies and for
    # storing GO term stats (required for making decions on term inclusion.)
    if(not(cfg_yaml['OBO_FILE'])):
        OBO_FILE = os.path.dirname(__file__) + "/go-basic.obo"
    else:
        OBO_FILE = cfg_yaml['OBO_FILE']
        
    GO_DAG = obo_parser.GODag(obo_file=OBO_FILE)
    GO_SUBDAG = GoSubDag(GO_DAG.keys(), GO_DAG, tcntobj=None, children=True, prt=sys.stdout)
    
    _GO_term_stats = {}
    my_go_statsGetter = gfc.go_statsGetter(GO_SUBDAG.go2obj, GO_SUBDAG.go2nt)
    for goid in ['GO:0008150', 'GO:0003674', 'GO:0005575']:
          my_go_statsGetter.get_go_stats(goid, _GO_term_stats)
    
    # We also need to load the html tables for any MSigDB terms we might want to show 
    # - best to keep this a constant, I think...
    
    if(not(cfg_yaml['MSIGDB_HTML'])):
        MSIGDB_HTML = os.path.dirname(__file__) + "/msigdb_v7.2.filtered.html"
    else:
        MSIGDB_HTML = cfg_yaml['MSIGDB_HTML']
        
    print(MSIGDB_HTML)
        
    msigdb_file = open(MSIGDB_HTML, "r")
    msigdb_contents = msigdb_file.read()
    msigdb_html_soup = BeautifulSoup(msigdb_contents, features="lxml")
    
    #And this is where we read in any extra gene annotations provided by the user.
    (status, message, _extra_annotations_dict, _num_extra_annotations) = gfb.make_extra_annotations_dict(EA_FILE)
    
    # These are constants for rendering HTML report
    NEW_H = 350
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
    log_f.write("MAX_CLUSTER_SIZE_THRESH: " + str(MAX_CLUSTER_SIZE_THRESH) + "\n")
    log_f.write("MAX_META_COMMUNITY_SIZE_THRESH: " + str(MAX_META_COMMUNITY_SIZE_THRESH) + "\n")
    log_f.write("COMBINE_TERM_TYPES: " + str(COMBINE_TERM_TYPES) + "\n")
    log_f.write("SEARCH_WORDS: " + str(SEARCH_WORDS))
    log_f.close()
    
    # *****************************************************************************
    
    # 5 READ IN DATA FOR SUMMARISING HERE*****************************
    
    # Store input image directory and extensions
    _exp_img_dir_paths_dict = {}
    _exp_img_dir_paths_dict[exp_id] = input_img_dir_path
    _exp_img_extension_dict = {}
    _exp_img_extension_dict[exp_id] = IMG_EXTENSION
    
    
    # Read in the ORA/ GSEA data
    (status, message, _term_types_dict, _term_defs_dict, exp_term_genes_dict, _exp_term_dotplot_dict, _) = \
            gfb.read_in_ora_data(ora_file_path, exp_id, MIN_LEVEL, MAX_DCNT, DOTPLOTS, _GO_term_stats)
    print(message)
    if(status > 0):
        sys.exit()
    
    # Store quantitative data (qd) values (usually log2 FC) for genes
    (status, message, _exp_gene_qd_dict) = gfb.make_gene_qd_dict(gene_qd_file_path, exp_id, GENE_INDEX, QD_INDEX)
    print(message)
    if(status > 0):
        sys.exit()
    
    # Make the dataframe that contains the quantitative data (usually log2 FC) for each gene, in each experiment
    _exp_gene_qd = pd.DataFrame.from_records([(e, g, v) for ((e, g), v) in list(_exp_gene_qd_dict.items())], 
                                                columns = ['Experiment', 'Gene', 'QD']).set_index(['Experiment', 'Gene'])
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
        big_community_term_sets = gfb.get_big_community_term_sets(terms_graph, MAX_CLUSTER_SIZE_THRESH, TT_OVERLAP_MEASURE, MIN_WEIGHT_TT_EDGE, MAX_DCNT, _term_types_dict, _GO_term_stats, _term_genes_dict)
    
    else:
        big_community_term_sets = []
        type_2_term_dict_keys = list(type_2_term_dict.keys())
        type_2_term_dict_keys.sort()
        
        for type_2_term_dict_key in type_2_term_dict_keys:
            sub_terms_list = type_2_term_dict[type_2_term_dict_key]
            sub_terms_graph = gfb.build_terms_graph(sub_terms_list, _term_genes_dict, TT_OVERLAP_MEASURE, MIN_WEIGHT_TT_EDGE)
            
            # find 'big' communities of terms. Here 'big' just means not singleton ********
            sub_big_community_term_sets = gfb.get_big_community_term_sets(sub_terms_graph, MAX_CLUSTER_SIZE_THRESH, TT_OVERLAP_MEASURE, MIN_WEIGHT_TT_EDGE, MAX_DCNT, _term_types_dict, _GO_term_stats, _term_genes_dict)
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
        
                
    # *****************************************************************************
    
    # 7. GENERATE HTML REPORT *****************************************************
    my_summaryPrinter = gfc.summaryPrinter(summary_id, summary_id, output_dir, info_string + '_report.html', meta_communities, singleton_meta_communities, singleton_communities)
    my_summaryPrinter.print_html()
    
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
    html_f.write("  padding: 5;\n")
    html_f.write("  border: none;\n")
    html_f.write("  font: inherit;\n")
    html_f.write("  color: white;\n")
    html_f.write("  cursor: pointer;\n")
    html_f.write("  background-color: dodgerblue;\n")
    html_f.write("  border-radius: 20px;\n")
    html_f.write("  transition-duration: 0.1s;\n")
    html_f.write("}\n")
        
    html_f.write(".view-button:hover {\n")
    html_f.write("  background-color: crimson;\n")
    html_f.write("  color: white;\n")
    html_f.write("}\n")
    
    html_f.write(".disabled-view-button {\n")
    html_f.write("  padding: 5;\n")
    html_f.write("  border: none;\n")
    html_f.write("  font: inherit;\n")
    html_f.write("  color: white;\n")
    html_f.write("  background-color: dodgerblue;\n")
    html_f.write("  border-radius: 20px;\n")
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
    
    #***********************************
    
    html_f.write(".grid-container2 {\n")
    html_f.write("  display: grid;\n")
    html_f.write("  grid-template-areas:\n")
    html_f.write("    'members2 heatmap2 heatmap2 heatmap2 heatmap2 heatmap2'\n")
    html_f.write("    'spacer2a plot_buttons2 plot_buttons2 plot_buttons2 plot_buttons2 plot_buttons2'\n")
    html_f.write("    'spacer2b upset2 upset2 upset2 upset2 upset2';\n")
    html_f.write("  grid-gap: 10px;\n")
    html_f.write("  background-color: #DC143C;\n")
    html_f.write("  padding: 10px;\n")
    html_f.write("}\n\n")
    
    html_f.write(".members2 { grid-area: members2; }\n")
    html_f.write(".heatmap2 { grid-area: heatmap2;\n") 
    html_f.write("          overflow: scroll;}\n")
    html_f.write(".spacer2a{ grid-area: spacer2a;}\n")
    html_f.write(".plot_buttons2{ grid-area: plot_buttons2; }\n")
    html_f.write(".spacer2b{ grid-area: spacer2b;}\n")
    html_f.write(".upset2 { grid-area: upset2;\n")  
    html_f.write("          overflow: scroll;}\n")
    html_f.write("\n") 
        
    html_f.write(".grid-container2 > div {\n")
    html_f.write("  max-height: "+ str(NEW_H + 30) +"px;\n")
    html_f.write("  overflow: scroll;\n")
    html_f.write("  background-color: rgba(255, 255, 255, 0.8);\n")
    html_f.write("  text-align: left;\n")
    html_f.write("  padding: 15px;\n")
    html_f.write("  font-size: small;\n")
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
    
    html_f.write("</style>\n")
    html_f.write("</head>\n")
    
    
    html_f.write("<body>\n")
    
    for mc in meta_communities:
        mc.print_html(html_f, summary_id + '_communities_summary.html')
        
        for bc in mc.communities:
            bc.print_html(html_f, summary_id + '_communities_summary.html')
            
    for bc in singleton_meta_communities:
        bc.print_html(html_f, summary_id + '_communities_summary.html')
        
    for sc in singleton_communities:
        sc.print_html(html_f, summary_id + '_communities_summary.html')
       
    
    html_f.write("</body>\n")
    html_f.write("</html>\n")
    html_f.close()
    
    csv_f = open(output_dir + '/' + info_string + '_report.csv', 'w')
    for mc in meta_communities:
        for bc in mc.communities:
            bc.print_csv(csv_f)
            
    for bc in singleton_meta_communities:
        bc.print_csv(csv_f)
        
    for sc in singleton_communities:
        sc.print_csv(csv_f)
        
    csv_f.close()

if __name__ == "__main__":
    main()