#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: avigailtaylor
"""

# IMPORTS *********************************************************************

import collections
import os
import sys
import argparse

import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns
import yaml
from bs4 import BeautifulSoup
from goatools import obo_parser
from goatools.gosubdag.gosubdag import GoSubDag
from matplotlib import pyplot
from networkx.algorithms.community import greedy_modularity_communities
from sklearn.metrics import silhouette_samples, silhouette_score
from upsetplot import from_contents

from genefeast import gf_base as gfb
from genefeast import gf_classes as gfc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mif_path")
    parser.add_argument("output_dir")
    parser.add_argument("cfg_yaml_path")
    args = parser.parse_args()
    
    gf_multi(args.mif_path, args.output_dir, args.cfg_yaml_path)


def gf_multi(mif_path, output_dir, cfg_yaml_path):
    # MAIN PROGRAM ****************************************************************
    # 0. CHECK PYTHON VERSION *****************************************************
    if(not(sys.version_info.major==3 and sys.version_info.minor==7)):
        print('GeneFEAST requires Python 3.7. Please make sure you have a compliant version installed.')
        sys.exit()
    
    # 1. SET UP I/O FILES AND DIRECTORIES *****************************************
    
    (status, message, _mi_dict, _exp_ids) = gfb.get_meta_info(mif_path) # mi short for meta input
    print(message)
    if(status > 0):
        sys.exit()
        
    _info_string = '_'.join(_exp_ids)
    
    
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
    (_rel_images_dir, _abs_images_dir) = gfb.generate_images_dirs(_info_string, output_dir)
    os.mkdir(_abs_images_dir)
    
    # Also need to store the file name for the main HTML page - this is auto-generated and should not be part of the config file.
    MAIN_HYPERLINK = output_dir + '/' + _info_string + '_main.html'
    
    # *****************************************************************************
    
    # 2. IMPORT VARIABLES FROM CONFIG FILE ****************************************
    with open(cfg_yaml_path, "r") as ymlfile:
        cfg_yaml = yaml.safe_load(ymlfile)
    
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
    
    MAX_COMMUNITY_SIZE_THRESH = cfg_yaml['MAX_COMMUNITY_SIZE_THRESH']
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
    # storing GO term stats (required for making decisions on term inclusion.)
    if(not(cfg_yaml['OBO_FILE'])):
        OBO_FILE = os.path.dirname(__file__) + "/go-basic.obo"
    else:
        OBO_FILE = cfg_yaml['OBO_FILE']
    
    GO_DAG = obo_parser.GODag(obo_file=OBO_FILE)
    GO_SUBDAG = GoSubDag(GO_DAG.keys(), GO_DAG, tcntobj=None, children=True, prt=sys.stdout)
    
    _GO_term_stats = {}
    my_go_statsGetter = gfc.go_statsGetter(GO_SUBDAG.go2obj , GO_SUBDAG.go2nt)
    for goid in ['GO:0008150', 'GO:0003674', 'GO:0005575']:
          my_go_statsGetter.get_go_stats(goid, _GO_term_stats)
    
    # We also need to load the html tables for any MSigDB terms we might want to show - best to keep this a constant, I think...
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
    #NEW_H_SINGLETON = 325
    NEW_H_SINGLETON_ADJUSTMENT = 25
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
    
    # 5 READ IN ORA OR EA OUTPUTS FOR SUMMARISING HERE*****************************
    
    _exp_img_dir_paths_dict = {}
    _exp_img_extension_dict = {}
    
    _term_types_dict = {}
    _term_defs_dict = {}
    _exp_terms_dict = collections.OrderedDict()
    _exp_term_genes_dict = {}
    _exp_term_dotplot_dict = {}
    
    _exp_gene_qd_dict = {}
    
    
    for exp_id in _mi_dict.keys():   
        my_ora_file_path, my_gene_qd_file_path, my_input_img_dir_path = _mi_dict[exp_id]
        
        
        # Store input image directory and extensions
        _exp_img_dir_paths_dict[exp_id] = my_input_img_dir_path
        _exp_img_extension_dict[exp_id] = IMG_EXTENSION
        
        
        # Read in the ORA/ GSEA data
        (status, message, term_types_dict_sub, term_defs_dict_sub, exp_term_genes_dict_sub, exp_term_dotplot_dict_sub, exp_terms) = \
            gfb.read_in_ora_data(my_ora_file_path, exp_id, MIN_LEVEL, MAX_DCNT, DOTPLOTS, _GO_term_stats)
        print(message)
        if(status > 0):
            sys.exit()
        
        _term_types_dict.update(term_types_dict_sub)
        _term_defs_dict.update(term_defs_dict_sub)
        _exp_terms_dict[exp_id] = exp_terms
        _exp_term_genes_dict.update(exp_term_genes_dict_sub)
        _exp_term_dotplot_dict.update(exp_term_dotplot_dict_sub)
        
    
        # Store quantitative data (qd) values (usually log2 FC) for genes
        (status, message, exp_gene_qd_dict_sub) = gfb.make_gene_qd_dict(my_gene_qd_file_path, exp_id, GENE_INDEX, QD_INDEX)
        print(message)
        if(status > 0):
            sys.exit()
    
        _exp_gene_qd_dict.update(exp_gene_qd_dict_sub)
                
    
    # Remove terms that do not have more than MIN_NUM_GENES total gene annotations across all experiments
    (_, terms_to_remove) = gfb.find_terms_to_remove(_exp_term_genes_dict, MIN_NUM_GENES)
    for del_term in terms_to_remove:
        del _term_types_dict[del_term]
        del _term_defs_dict[del_term]
        for exp_id in _mi_dict.keys():
            if del_term in _exp_terms_dict[exp_id]:
                _exp_terms_dict[exp_id].remove(del_term)
            if(exp_id, del_term) in _exp_term_genes_dict:
                del _exp_term_genes_dict[(exp_id,del_term)]
            if(DOTPLOTS):
                if((exp_id, del_term) in _exp_term_dotplot_dict):
                    del _exp_term_dotplot_dict[(exp_id, del_term)]
    
    
    # Make the dataframe that contains the quantitative data (usually log2 FC) for each gene, in each experiment
    _exp_gene_qd = pd.DataFrame.from_records([(e, g, v) for ((e, g), v) in list(_exp_gene_qd_dict.items())], 
                                                columns = ['Experiment', 'Gene', 'QD']).set_index(['Experiment', 'Gene'])
    # Sort the indices for faster access later on...
    _exp_gene_qd = _exp_gene_qd.sort_index()
     
    # *****************************************************************************
    
    # 6. MAKE OVERALL UPSET DF ****************************************************
    exp_term_upset_df = from_contents(_exp_terms_dict)
    
    exp_term_upset_for_image_df = exp_term_upset_df.reorder_levels(_exp_ids[:: -1]) 
    ud_for_img = gfc.upsetDrawer_app2(_info_string, "recurring_terms", exp_term_upset_for_image_df, NEW_H, _abs_images_dir, _rel_images_dir, basic_upset=False)
    (upset_img_path, upset_img_width) = ud_for_img.draw_upset_plot() 
    
    num_exp_counts = np.array([sum(exp_term_upset_df.index[x]) for x in range(len(exp_term_upset_df.index))])  
    exp_term_upset_final_df = exp_term_upset_df[(num_exp_counts > 1)]
    ud = gfc.upsetDrawer_app2(_info_string, "recurring_terms", exp_term_upset_final_df, NEW_H, _abs_images_dir, _rel_images_dir, basic_upset=False)
    
    
    # *****************************************************************************
    
    # 7. GO THROUGH EACH SET OF TERMS, GROUPED TOGETHER BECAUSE THEY ARE OVER-REPRESENTED,
    # IN THE SAME SET OF EXPERIMENTS, AND CLUSTER THEM BY GENE-SET OVERLAP.
    exp_term_upset_grouped = exp_term_upset_final_df.groupby(level=list(range(exp_term_upset_final_df.index.nlevels)))
    etgContainers = []
    
    for key_i in range(len(ud.upset.intersections.keys())):
        key = ud.upset.intersections.keys()[key_i]
        exp_term_group = exp_term_upset_grouped.get_group(key)
        _etg_exp_ids = [exp_term_group.index.names[i] for i in range(len(exp_term_group.index.names)) if key[i]]
        etg_terms = [t[0] for t in exp_term_group.values] # etg is short for exp_term_group # CHECK FOR BUG - WHY IS IT t[0] ??? Does .values always return numpy arrays, or is it something to do with upset?
        
        if(key_i+1 < 10):
            _key_i_str = "0" + str(key_i + 1)
        else:
            _key_i_str = str(key_i + 1)
            
        _etg_name = "ETSI " + _key_i_str # (ETSI stands for Experiment term-set intersection)
        _etg_info_string = '__' + '__'.join(_etg_exp_ids) + '__'
        #_etg_text_details = ', '.join(_etg_exp_ids) ', '.join(_etg_exp_ids[0:-1]) + ' and ' + _etg_exp_ids[-1]
        _etg_text_details = ', '.join(_etg_exp_ids[0:-1]) + ' and ' + _etg_exp_ids[-1]
       
        _term_genes_dict = {}
        for etg_eid in _etg_exp_ids:
            for etg_t in etg_terms:
                if(etg_t in _term_genes_dict):
                    _term_genes_dict[etg_t] = _term_genes_dict[etg_t].union(_exp_term_genes_dict[(etg_eid, etg_t)])
                else:
                    _term_genes_dict[etg_t] = _exp_term_genes_dict[(etg_eid, etg_t)]
        
        type_2_term_dict = {}
        
        for t in etg_terms:
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
            terms_graph = gfb.build_terms_graph(etg_terms, _term_genes_dict, TT_OVERLAP_MEASURE, MIN_WEIGHT_TT_EDGE)
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
        
        (_big_communities, _singleton_communities, _meta_communities, _singleton_meta_communities) = \
        gfb.build_all_communities_lists(etg_terms, big_community_term_sets, 
                                          _etg_name + '_community ', _etg_name + '_meta community ', 
                                          SC_BC_OVERLAP_MEASURE, MIN_WEIGHT_SC_BC,
                                          BC_BC_OVERLAP_MEASURE, MIN_WEIGHT_BC_BC,
                                          MAX_META_COMMUNITY_SIZE_THRESH,
                                          QUANT_DATA_TYPE, _exp_gene_qd, _etg_exp_ids, 
                                          _term_types_dict, _term_defs_dict, 
                                          _term_genes_dict, _exp_term_dotplot_dict, 
                                          _abs_images_dir, _rel_images_dir, 
                                          _extra_annotations_dict, _num_extra_annotations,
                                          NEW_H, HEATMAP_WIDTH_MIN, HEATMAP_HEIGHT_MIN,
                                          HEATMAP_MIN, HEATMAP_MAX, SEARCH_WORDS, 
                                          _etg_info_string, msigdb_html_soup, GO_DAG, 
                                          _exp_img_dir_paths_dict, _exp_img_extension_dict, 
                                          new_h_singleton_adjustment=NEW_H_SINGLETON_ADJUSTMENT)
        
        
        # TODO: Add preconditions for silhoutte coefficient to work... Will need to make sure that an empty figure is created when
        # conditions are not met, as front page will need to be printed either way
        # Trim and annotate community names - DONE
        # Add to gf.py
        
        _term_community_pairs = gfb.get_big_community_labels_for_terms(_big_communities)
        
        if((len(_big_communities) >= 2) & (len(_big_communities) <= (len(_term_community_pairs)-1))):
            _terms_distance_matrix = gfb.build_terms_distance_matrix(_term_community_pairs, _term_genes_dict, TT_OVERLAP_MEASURE)
            gfb.make_silhouette_plot(_terms_distance_matrix, np.array([c for (t,c) in _term_community_pairs]), _big_communities, _term_genes_dict, _abs_images_dir)

        # Now run analysis to plot out how clustering looks when varying two thresholds: MIN_WEIGHT_TT_EDGE and MAX_COMMUNITY_SIZE_THRESH
        # TODO: check this works when multiple FEA databases are used and database agglomeration is off!
        
        min_weight_tt_edge_trials = sorted(set([x/10 for x in list(range(2,9,2))] + [MIN_WEIGHT_TT_EDGE]))
        max_community_size_thresh_trials = sorted(set([10,15,20,MAX_COMMUNITY_SIZE_THRESH]))
        
        fig, axes = pyplot.subplots(len(min_weight_tt_edge_trials), len(max_community_size_thresh_trials), figsize=(16, 10))
        #fig.tight_layout()
        
        #for min_weight_tt_edge_try in min_weight_tt_edge_trials:
        for min_weight_tt_edge_try_i in range(len(min_weight_tt_edge_trials)):
            
            min_weight_tt_edge_try = min_weight_tt_edge_trials[min_weight_tt_edge_try_i]
            
            sub_terms_graphs_try = []
            if(COMBINE_TERM_TYPES or len(type_2_term_dict.keys())==1):
                sub_terms_graphs_try.append(gfb.build_terms_graph(etg_terms, _term_genes_dict, TT_OVERLAP_MEASURE, min_weight_tt_edge_try))
            else:
                type_2_term_dict_keys = list(type_2_term_dict.keys())
                type_2_term_dict_keys.sort()
                for type_2_term_dict_key in type_2_term_dict_keys:
                    sub_terms_list = type_2_term_dict[type_2_term_dict_key]
                    sub_terms_graphs_try.append(gfb.build_terms_graph(sub_terms_list, _term_genes_dict, TT_OVERLAP_MEASURE, min_weight_tt_edge_try))
                
            #for max_community_size_thresh_try in max_community_size_thresh_trials:
            for max_community_size_thresh_try_i in range(len(max_community_size_thresh_trials)):
                
                max_community_size_thresh_try = max_community_size_thresh_trials[max_community_size_thresh_try_i]
                print(min_weight_tt_edge_try)
                print(max_community_size_thresh_try)
                big_community_term_sets_try = []
                for sub_terms_graph_try in sub_terms_graphs_try:
                    big_community_term_sets_try = big_community_term_sets_try + gfb.get_big_community_term_sets(sub_terms_graph_try, max_community_size_thresh_try,
                                                                                                                TT_OVERLAP_MEASURE, min_weight_tt_edge_try, 
                                                                                                                MAX_DCNT, _term_types_dict, _GO_term_stats, 
                                                                                                                _term_genes_dict)
                    
                num_big_communities_try = len(big_community_term_sets_try)
                
                term_community_pairs_try = gfb.get_big_community_labels_for_terms_from_term_sets(big_community_term_sets_try)
                term_community_labels_try = np.array([c for (t,c) in term_community_pairs_try])
                prop_try = gfb.calc_prop_terms_in_big_communities(term_community_labels_try, _term_genes_dict)
                
                if((num_big_communities_try >= 2) & (num_big_communities_try <= (len(term_community_pairs_try)-1))):
                    if((min_weight_tt_edge_try == MIN_WEIGHT_TT_EDGE) & (max_community_size_thresh_try==MAX_COMMUNITY_SIZE_THRESH)):
                        axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].set_facecolor("yellow")
                    
                    terms_distance_matrix_try = gfb.build_terms_distance_matrix(term_community_pairs_try, _term_genes_dict, TT_OVERLAP_MEASURE)
                    silhouette_avg_try = silhouette_score(terms_distance_matrix_try, term_community_labels_try, metric="precomputed")
                    sample_silhouette_values_try = silhouette_samples(terms_distance_matrix_try, term_community_labels_try, metric="precomputed")
                    
                    sample_silhouette_values_try_data = {'Community': term_community_labels_try,
                                                         'Silhouette Score': sample_silhouette_values_try} 
                    
                    sample_silhouette_values_try_df = pd.DataFrame(sample_silhouette_values_try_data)
                    
        
#                    _color_palette = sns.color_palette("Greens")
#                    _color_index = int(prop_try * (len(_color_palette)-1))
                    
#                    sns.violinplot(ax=axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i], data=sample_silhouette_values_try_df,
#                                                                                                       y='Score', x='Community',
#                                                                                                       color=_color_palette[_color_index],
#                                                                                                       saturation=1, inner=None, cut=0)
#                    axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].set_xticklabels([])
#                    axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].set_ylim([-1,1])
                    
                    
                    community_cum_prop_of_total_df = sample_silhouette_values_try_df.groupby('Community').size().cumsum().reset_index()
                    community_cum_prop_of_total_df['cum prop of total terms'] = [(x/len(_term_genes_dict))*100 for x in sample_silhouette_values_try_df.groupby('Community').size().cumsum()]
                
                    ax_twin = axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].twinx()
                    ax_twin.bar(community_cum_prop_of_total_df['Community'], community_cum_prop_of_total_df['cum prop of total terms'], alpha=0.25)
                    ax_twin.set_ylim([0,100])
                    if(max_community_size_thresh_try_i == (len(max_community_size_thresh_trials)-1)):
                        ax_twin.yaxis.tick_right()
                        ax_twin.set_ylabel("Cum. % terms")
                    
                    
                    sns.violinplot(ax=axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i], data=sample_silhouette_values_try_df,
                                                                                                       y='Silhouette Score', x='Community',
                                                                                                       color="red",inner=None, cut=0)
                    
                    axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].axhline(y = 0, color = 'k', linestyle = '-')
                    axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].axhline(y = 0.5, color = 'darkgrey', linestyle = '--')
                    axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].axhline(y = silhouette_avg_try, color = 'r', linestyle = ':')
                    
                    
                    #axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].set_xticklabels([]])
                    axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].set_ylim([-1.1,1.1])
                    
                    if(max_community_size_thresh_try_i > 0 ):
                        axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].set_ylabel("")
                    if(min_weight_tt_edge_try_i < (len(min_weight_tt_edge_trials)-1)):
                        axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].set_xlabel("")
                        
                    axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].set_title(str(min_weight_tt_edge_try) + ", " + str(max_community_size_thresh_try))
                   
        pyplot.subplots_adjust(hspace=0.7)            
        pyplot.savefig(_abs_images_dir + "sil_ violinplots.svg", bbox_inches="tight")
        pyplot.close()
    
        # ***************************************************************************** 
        relative_main_html = _info_string + '_main.html'
        etgContainers.append( gfc.etgContainer( _etg_name , _etg_text_details , _key_i_str , output_dir , relative_main_html  , _rel_images_dir, _meta_communities , _singleton_meta_communities , _singleton_communities , NEW_H ) )
        
    
    # 8. GENERATE HTML REPORT *****************************************************
    
    html_f = open( MAIN_HYPERLINK , 'w')
    html_f.write("<!DOCTYPE html>\n")
    html_f.write("<html>\n")
    
    html_f.write("<head>\n")
    
    html_f.write("<style>\n")
    
    html_f.write(".title {\n")
    html_f.write("  margin: 5px;\n")
    html_f.write("}\n")
    
    
    html_f.write(".grid-container {\n")
    html_f.write("display: grid;\n")
    html_f.write("grid-template-areas:\n")
    html_f.write("'blank'\n")
    html_f.write("'figure';\n")
    html_f.write("grid-gap: 10px;\n")
    html_f.write("background-color: #0aa8a8;\n")
    html_f.write("padding: 10px;\n")
    html_f.write("}\n")
    
    html_f.write(".blank{ grid-area: blank; }\n")
    html_f.write(".figure { grid-area: figure;\n")
    html_f.write("overflow: scroll;}\n")
    
    html_f.write(".grid-container > div {\n")
    html_f.write("  max-height: "+ str((NEW_H + 30) * 2) +"px;\n")
    html_f.write("  overflow: scroll;\n")
    html_f.write("  background-color: rgba(255, 255, 255, 0.8);\n")
    html_f.write("  text-align: left;\n")
    html_f.write("  padding: 15px;\n")
    html_f.write("  font-size: small;\n")
    html_f.write("  margin: 0;\n")
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
    html_f.write("overflow: hidden;\n")
    html_f.write("background-color: #088F8F;\n")
    html_f.write("top: 0; left: 0; width: 100%; height: 55px; z-index:1;")
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
    html_f.write("   text-decoration:underline;\n")
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
    html_f.write('<li><a href="' + relative_main_html + '" class="navactive">Experiment term-set intersections</a></li>\n')
    html_f.write('<li class="dropdown">\n')
    html_f.write('<button class="dropbtn">Reports\n')
    html_f.write('</button>\n')
    html_f.write('<div class="dropdown-content">\n')
    for etgContainer in etgContainers:
        html_f.write('<a href="' + etgContainer.get_summary_hyperlink() + '">' + etgContainer.name + ': ' + etgContainer.text_details + '</a>\n')
    html_f.write('</div>\n')
    html_f.write('</li>\n')
    html_f.write('</ul>\n')
    html_f.write('</div>\n')
    
    
    html_f.write('<div>\n')
    html_f.write('<ul class="subnav">\n')
    html_f.write('<li class="rightlink"><a style="color:white;">Experiment term-set intersections for ' + ', '.join(_exp_ids[0:-1]) + ' and ' + _exp_ids[-1] + '</a></li>\n')
    html_f.write('</ul>\n')
    html_f.write('</div>\n')
    html_f.write('</div>\n')
    html_f.write('<div class="subtitlebanner">\n')
    html_f.write('  <li><a style="color:black;">UpSet plot</a></li>\n')
    html_f.write('</div>\n')
    html_f.write('<div class="grid-container">\n')
    html_f.write('<div class="figure">\n')
    html_f.write('<img src="' + upset_img_path + '" width="' + str(upset_img_width)  + '" height="' + str(NEW_H) + '">\n')
    html_f.write('</div>\n')
    html_f.write('</div>\n')
    
    html_f.write("</body>\n")
    html_f.write("</html>\n")
    html_f.close()
    
    for etgContainer in etgContainers:
        etgContainer.print_html( etgContainers )
    
    for etgContainer in etgContainers:
        etgContainer.print_csv()


if __name__ == "__main__":
    main()
