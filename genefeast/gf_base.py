#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: avigailtaylor
"""

# IMPORTS *********************************************************************
import os
import collections
import csv
import math
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns
import yaml

from PIL import Image
from fractions import Fraction
from networkx.algorithms.community import greedy_modularity_communities
from matplotlib import pyplot
from sklearn.metrics import silhouette_samples, silhouette_score
from upsetplot import from_contents

from genefeast import gf_classes as gfc

# FUNCTIONS *******************************************************************

def get_output_dir_status(output_dir):

    status = 0
    message = ''
    
    if os.path.exists( output_dir ):
        if( os.path.isdir( output_dir ) ):
            if( len( os.listdir( output_dir ) ) == 0 ):
                message = ( 'Output directory already exists and is empty. '
                            'Proceeding with analysis now...' )
            else:
                status = 1
                message = ( '*** ERROR: Output directory is not empty. '
                            'Please delete the contents of the directory before '
                            'running this program again. Alternatively, provide '
                            'the name of an empty directory. ***' )
        else:
            status = 2
            message = ( '*** ERROR: A file exists with the same name as your '
                        'output directory. Please delete the file before running '
                        'this program again. ***' )
    else:
        status = 3
        message = ( 'Output directory does not exist... Creating directory now, '
                    'and then proceeding with analysis...' )
    
    return (status, message)
        
    
def get_meta_info(mif_path):
    status = 0
    message = ''
    mi_dict = collections.OrderedDict() # mi short for meta input
    exp_ids = []
    
    if os.stat(mif_path).st_size > 0:
    
        with open( mif_path ) as mf:
            csvreader_mf = csv.reader( mf )
            for line in csvreader_mf:
                if(len(line) > 4):                
                    status = 1
                    message = ('*** ERROR: There are more fields than expected in '
                                   'the meta input file. Please check the file format '
                                   'against the docs. ***')
                    return(status, message, collections.OrderedDict(), [])
                    
                elif(len(line) < 4):
                    status = 2
                    message = ('*** ERROR: Meta input file not formatted correctly. Check the number '
                               'of fields in each line and that there are no empty lines. ***')
                    return(status, message, collections.OrderedDict(), [])
                    
                else:
                    exp_id , ora_file_path , gene_qd_file_path , input_img_dir_path = line
                    if(exp_id in mi_dict):
                        status = 3
                        message = ('*** ERROR: Two or more experiments have the same ID. '
                                   'Please check your meta input file for repeated '
                                   'lines and/ or naming errors. ***')
                        return(status, message, collections.OrderedDict(), [])
                    else:
                        mi_dict[ exp_id ] = [ora_file_path, gene_qd_file_path, input_img_dir_path]
                        exp_ids.append( exp_id )
        
        return(status, message, mi_dict, exp_ids)
    
    else:
        status = 2
        message = ('*** ERROR: Meta input file not formatted correctly. Check the number '
                               'of fields in each line and that there are no empty lines. ***')
        return(status, message, collections.OrderedDict(), [])
        
def get_meta_info_from_setup(setup_yaml_path):
    status = 0
    message = ''
    mi_dict = collections.OrderedDict() # mi short for meta input
    exp_ids = []
    
    if os.stat(setup_yaml_path).st_size > 0:
        with open(setup_yaml_path, "r") as ymlfile:
            setup = yaml.safe_load(ymlfile)
            
            if(setup.get("FEAs") is None):
                status = 2
                message = ('*** ERROR: No FEAs have been listed in setup YAML file. ***')
                return(status, message, collections.OrderedDict(), [])
            else:
                mi_list = setup.get("FEAs")
                for exp_mi in mi_list:
                    if(not("id" in exp_mi.keys()) 
                        or not("goi_file" in exp_mi.keys()) 
                        or not("fea_file" in exp_mi.keys())):
                        
                        status = 3
                        message = ('*** ERROR: One of the FEAs listed in setup YAML file is '
                                   'missing one or more of "id", "goi_file", or "fea_file." ***')
                        return(status, message, collections.OrderedDict(), [])
                    else:
                        if("input_img_dir" in exp_mi.keys()):
                            input_img_dir = exp_mi["input_img_dir"]
                        else:
                            input_img_dir = ""
                        
                        
                        exp_id = exp_mi["id"]
                        gene_qd_file_path = exp_mi["goi_file"]
                        ora_file_path = exp_mi["fea_file"]
                        
                        if(exp_id in mi_dict):
                            status = 4
                            message = ('*** ERROR: Two or more FEAs have the same ID. '
                                       'Please check your meta input file for repeated '
                                       'lines and/ or naming errors. ***')
                            return(status, message, collections.OrderedDict(), [])
                        
                        else:
                            mi_dict[ exp_id ] = [ora_file_path, gene_qd_file_path, input_img_dir]
                            exp_ids.append( exp_id )
                            
                return(status, message, mi_dict, exp_ids)

    else:
        status = 1
        message = ('*** ERROR: Setup YAML file is empty. ***')
        return(status, message, collections.OrderedDict(), [])
        
def generate_images_dirs(info_string, output_dir):
    rel_images_dir = 'images_' + info_string + '_AUTO/'
    abs_images_dir = output_dir + '/' + rel_images_dir
    
    return(rel_images_dir, abs_images_dir)

def is_number_str(number_string):
    try:
        float(number_string)
    except ValueError:
        return False
    else:
        return True
    
def is_fraction_str(fraction_string):
    try:
        Fraction(fraction_string)
    except ValueError:
        return False
    else:
        return True
        
def read_in_ora_data(ora_file_path, exp_id, min_level, max_dcnt, enrichr_format, dotplots, GO_term_stats):
    status = 0
    message = ''
    term_types_dict = {}
    term_defs_dict = {}
    exp_terms = []
    exp_term_genes_dict = {}
    exp_term_dotplot_dict = {}
    
    seen_exp_term_pairs = []
    
    if os.stat(ora_file_path).st_size > 0:
        with open(ora_file_path) as f:    
            csvreader = csv.reader(f)
            next( csvreader )
            lines_read = 0
            for line in csvreader:
                lines_read += 1
                
                
                if(enrichr_format):
                    if(len(line) < 10):
                        status = 1
                        message = ('*** ERROR: ORA (or GSEA) file not formatted correctly. '
                                   'Enrichr format is expected, but has not been supplied. '
                                   'If your ORA file is in basic csv format with four columns '
                                   '(Type, Term, Definition, Genes), then '
                                   'please check that variable ENRICHR is set to False in the setup YAML file, '
                                   'and then run again. (Note that the default value for ENRICHR is False if not '
                                   'given in the setup YAML file.) '
                                   'Otherwise, please check that your ORA file is '
                                   'in the expected Enrichr format and matches the description in the docs. '
                                   'Also, check the number of fields in each line and that there '
                                   'are no empty lines. ***')
                        return(status, message, {}, {}, {}, {}, [])
                        
                    else:
                        term = line[1]
                        genes = set(line[ len(line) - 2 ].split("/"))
                        ttype = line[0].upper()
                        
                        len_diff = len( line ) - 10
                        definition = ','.join( line[ 2 : ( 2 + len_diff + 1 ) ] )
                else:
                    if(len(line) != 4):
                        status = 1
                        message = ('*** ERROR: ORA (or GSEA) file not formatted correctly. '
                                   'Basic format is expected, but has not been supplied. '
                                   'If your ORA file is in Enrichr format (see docs), then '
                                   'please check that variable ENRICHR is set to True in the setup YAML, '
                                   'and then run again. (Note that the default value for ENRICHR is False if not '
                                   'given in the setup YAML file.) Otherwise, please check that your ORA file is '
                                   'in basic csv format with four columns (Type, Term, Definition, Genes). '
                                   'Also, check the number of fields in each line and that there '
                                   'are no empty lines. ***')
                        return(status, message, {}, {}, {}, {}, [])
                        
                    else:
                        len_diff = len( line ) - 4
                        
                        ttype = line[0].upper()
                        term = line[1]
                        definition = ','.join( line[ 2 : ( 2 + len_diff + 1 ) ] )
                        genes = set(line[ len(line) - 1 ].split("/"))
                
                
                if((exp_id, term) in seen_exp_term_pairs):
                    print("This term is repeated " + term)
                    status = 2
                    message = ('*** ERROR: Term repeated in ORA (or GSEA) file in '
                               ' experiment with ID: ' + exp_id + '. ***')
                    return(status, message, {}, {}, {}, {}, [])
                else:
                    seen_exp_term_pairs.append((exp_id, term))
                
                
                add_term = True
                
                if ttype[0:2] == "GO":
                    if term in GO_term_stats.keys():
                        t_dcnt , t_level = GO_term_stats[ term ]
                        add_term = ( t_level >= min_level and t_dcnt <= max_dcnt )
                    else:
                        add_term = False
                
                if( add_term ):
                    exp_term_genes_dict[ ( exp_id , term ) ] = genes
                    
                    if( not( term in term_types_dict ) ):
                        term_types_dict[ term ] = ttype
                    
                    if( not( term in term_defs_dict ) ):
                        term_defs_dict[ term ] = definition
                        
                    if( dotplots ):
                        
                        if(not(enrichr_format)):
                            status = 3
                            message = ( '*** ERROR: DOTPLOTS is True, but ORA/ GSEA file is not in the Enrichr format '
                                       'required for dotplots. To fix this, set DOTPLOTS to False in the setup YAML file. '
                                       'Alternatively, set ENRICHR '
                                       'to True in the setup YAML file (if not given, the default value is False), '
                                       'and supply ORA/ GSEA results in the Enrichr format (see docs). ***')
                            return(status, message, {}, {}, {}, {}, [])
                            
                        else:
                        
                            gene_ratio_string = line[ len(line) - 7 ]
                            bg_ratio_string = line[ len(line) - 6 ]
                            padj_string = line[len(line) - 4]
                            count_string = line[len(line) - 1]
                            
                            if(not(is_fraction_str(gene_ratio_string)) or \
                               not(is_fraction_str(bg_ratio_string)) or \
                               not(is_number_str(padj_string)) or \
                               not(is_number_str(count_string))):
                                
                                
                                status = 3
                                message = ( '*** ERROR: Data for dotplots is not formatted as expected in ORA/ GSEA file. '
                                            'Please refer to documentation for expected column order and content. '
                                            'If you do not have dotplot data to plot, or if you want to omit dotplots '
                                            'for whatever reason, then you can set DOTPLOTS to False in the config file. '
                                            'NOTE, however, that your ORA/ GSEA file still has to have the expected '
                                            'column order (see docs). ***' )
                                return(status, message, {}, {}, {}, {}, [])
                            else:
                                gene_ratio_Fraction = Fraction( gene_ratio_string )
                                gene_ratio = round( gene_ratio_Fraction.numerator/gene_ratio_Fraction.denominator , 3 )
                                neg_log10_padj = round( -1 * math.log10(float(padj_string)), 1)
                                count = int(count_string)
                                exp_term_dotplot_dict[ ( exp_id , term ) ] = [ gene_ratio , neg_log10_padj , count , gene_ratio_string , bg_ratio_string ]
                
                    
                    
                    exp_terms.append(term)
        
            if(lines_read==0):
                status = 4 
                message = ('*** ERROR: ORA (or GSEA) file not formatted correctly. '
                           'In particular, it only has one row, which is assumed '
                           'to be the header row and has been skipped. Please add '
                           'either a header row or data rows to the file. ***')
                return(status, message, {}, {}, {}, {}, [])
            else:
                return(status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, exp_term_dotplot_dict, exp_terms)
    else:
        status = 5
        message = ('*** ERROR: ORA/ GSEA file is empty. ***')
        return(status, message, {}, {}, {}, {}, [])
                    

def make_extra_annotations_dict(ea_file_path):
    status = 0
    message = ''
    extra_annotations_dict = {}
    num_extra_annotations = 0
    
    if(ea_file_path):
        if os.stat(ea_file_path).st_size > 0:
            with open(ea_file_path) as f:    
                tsv_reader = csv.reader(f)
                for row in tsv_reader:
                    if(len(row) != 2):
                        status = 1
                        message = ('*** ERROR: Extra annotation file is not formatted correctly. '
                                   'In particular, one of the rows does not have two columns. ***')
                        return(status, message, extra_annotations_dict, num_extra_annotations)
                    
                    else:
                        (annotation, genes_string) = row
                    
                        if annotation in extra_annotations_dict.keys():
                            status = 2
                            message = ('*** ERROR: Extra annotation file is not formatted correctly. '
                                       'In particular, an extra annotation has been repeated. ***')
                            return(status, message, extra_annotations_dict, num_extra_annotations)
                        else:
                            extra_annotations_dict[annotation] = genes_string.split('/')
                            num_extra_annotations +=1
                
    
    return(status, message, extra_annotations_dict, num_extra_annotations)
                

def make_gene_qd_dict(gene_qd_file_path, exp_id, gene_index, qd_index):
    status = 0
    message = ''
    gene_qd_dict = {}
    
    if os.stat(gene_qd_file_path).st_size > 0:
        with open(gene_qd_file_path) as f:
            csvreader = csv.reader(f)
            next( csvreader )
            lines_read = 0
            for line in csvreader:
                lines_read += 1
                if((len(line) < (max(gene_index, qd_index) + 1)) 
                                    or not(is_number_str(line[qd_index]))):
                    status = 1
                    message = ('*** ERROR: Gene quantitative data file (usually gene '
                               'expression/ log2 FC) not formatted correctly. '
                               'Check the number of fields in each line, and compare '
                               'this to GENE_INDEX and QD_INDEX in appx_config.py. '
                               'Also check that the quantitative data column contains '
                               'numbers only, and that there are no empty lines. ***')
                    return(status, message, {})
                    
                else:
                    (gene, qd) = line[gene_index],float(line[qd_index])
                    if((exp_id, gene) in gene_qd_dict):
                        status = 2
                        message = ('*** ERROR: Gene repeated in gene quantitative data '
                                   'file for experiment with ID: ' + exp_id + '. ***')
                        return(status, message, {})
                        
                    else:
                        gene_qd_dict[(exp_id, gene)] = qd
            
            if(lines_read == 0):
                status = 3
                message = ('*** ERROR: Gene quantitative data file (usually gene '
                          'expression/ log2 FC) not formatted correctly. '
                          'In particular, it only has one row, which is assumed '
                          'to be the header row and has been skipped. Please add '
                          'either a header row or data rows to the file. ***')
                return(status, message, {})
            else:
                return(status, message, gene_qd_dict)
    else:
        status = 4
        message = ('*** ERROR: Gene quantitative data file (usually gene '
                   'expression/ log2 FC) is empty. ***')
        return(status, message, {})


def find_terms_to_remove_old(exp_terms_dict, exp_term_genes_dict, min_num_genes):
    exp_term_upset_df_TEMP = from_contents(exp_terms_dict)
    ud_TEMP = gfc.upsetDrawer_app2( '' , "TEMP" , exp_term_upset_df_TEMP , 350, '' , '' , basic_upset = False )
    exp_term_upset_TEMP_grouped = exp_term_upset_df_TEMP.groupby( level = list( range( exp_term_upset_df_TEMP.index.nlevels ) ) )
    
    terms_to_remove = []
    
    for temp_key_i in range( len( ud_TEMP.upset.intersections.keys() ) ):
        temp_key = ud_TEMP.upset.intersections.keys()[ temp_key_i ]
        exp_term_group_TEMP = exp_term_upset_TEMP_grouped.get_group( temp_key )
        etg_expids_TEMP = [ exp_term_group_TEMP.index.names[ i ] for i in range( len( exp_term_group_TEMP.index.names ) ) if temp_key[i] ]
        etg_terms_TEMP = [ t[0] for t in exp_term_group_TEMP.values ]
        
        term_genes_dict_TEMP = {}
        for etg_eid_TEMP in etg_expids_TEMP:
            for etg_t_TEMP in etg_terms_TEMP:
                if( etg_t_TEMP in term_genes_dict_TEMP ):
                    term_genes_dict_TEMP[ etg_t_TEMP ] = term_genes_dict_TEMP[ etg_t_TEMP ].union( exp_term_genes_dict[ ( etg_eid_TEMP , etg_t_TEMP ) ] )
                else:
                    term_genes_dict_TEMP[ etg_t_TEMP ] = exp_term_genes_dict[ ( etg_eid_TEMP , etg_t_TEMP ) ]
                    
        for etg_t_TEMP in etg_terms_TEMP:
            if( len( term_genes_dict_TEMP[ etg_t_TEMP ] ) < min_num_genes ):
                terms_to_remove.append( etg_t_TEMP )
                
    return(terms_to_remove)
    


def find_terms_to_remove_aux(term_genes_dict, min_num_genes):
    terms_to_remove = []
    
    for t in term_genes_dict:
        if(len(term_genes_dict[t]) < min_num_genes):
            terms_to_remove.append(t)
            
    return terms_to_remove


def find_terms_to_remove(exp_term_genes_dict, min_num_genes):
    term_genes_dict = {}
    
    for (e, t) in exp_term_genes_dict:
        
        if t in term_genes_dict:
            term_genes_dict[t] = term_genes_dict[t].union(exp_term_genes_dict[(e, t)])
        else:
            term_genes_dict[t] = exp_term_genes_dict[(e, t)]

            
    terms_to_remove = find_terms_to_remove_aux(term_genes_dict, min_num_genes)
                
    return(term_genes_dict, terms_to_remove)
    

def build_terms_graph(terms_list, term_genes_dict, tt_overlap_measure, min_weight_tt_edge):
    terms_graph = nx.Graph()
    t_index = 0
    
    my_terms_list = sorted(terms_list)
    
    for t1 in my_terms_list[0:len(my_terms_list)-1]:
        for t2 in my_terms_list[ t_index+1 : len(my_terms_list) ]:       
    
            t1_genes = term_genes_dict[ t1 ] 
            t2_genes = term_genes_dict[ t2 ]
                    
            weight = 0
            
            if( tt_overlap_measure == 'OC' ):
                weight = len( set.intersection( t1_genes , t2_genes ) )/ min( len( t1_genes ) , len( t2_genes ) )
            if( tt_overlap_measure == 'JI' ):
                weight = len( set.intersection( t1_genes , t2_genes ) )/ len( set.union( t1_genes , t2_genes ) )
            
            
            if weight >= min_weight_tt_edge:
                terms_graph.add_edges_from( [ ( t1 , t2 , { 'w' : weight } ) ] )
        
        t_index += 1
        
    return(terms_graph)


def adaptive_big_community_find_aux( xl_terms , max_community_size_thresh , tt_overlap_measure , min_weight_tt_edge , term_genes_dict ):
    xl_terms_graph = nx.Graph()
    xl_t_index = 0

    my_xl_terms = sorted(xl_terms)
    for xl_t1 in my_xl_terms[0:len(my_xl_terms)-1]:
        for xl_t2 in my_xl_terms[ xl_t_index+1 : len( my_xl_terms ) ]:       

            xl_t1_genes = term_genes_dict[ xl_t1 ]
            xl_t2_genes = term_genes_dict[ xl_t2 ]
                
            weight = 0
        
            if( tt_overlap_measure == 'OC' ):
                weight = len( set.intersection( xl_t1_genes , xl_t2_genes ) )/ min( len( xl_t1_genes ) , len( xl_t2_genes ) )
            if( tt_overlap_measure == 'JI' ):
                weight = len( set.intersection( xl_t1_genes , xl_t2_genes ) )/ len( set.union( xl_t1_genes , xl_t2_genes ) )
        
        
            if weight >= min_weight_tt_edge:
                xl_terms_graph.add_edges_from( [ ( xl_t1 , xl_t2 , { 'w' : weight } ) ] )
    
        xl_t_index += 1
        
    
    community_term_sets = []
    if( len( xl_terms_graph.edges  )>0 ):
        community_term_sets = list( greedy_modularity_communities( xl_terms_graph ) )

    big_community_term_sets_aux = [ community_term_set for community_term_set in community_term_sets if ( ( len( community_term_set ) > 1 ) and ( len( community_term_set ) <= max_community_size_thresh ) ) ]
        
    XL_community_term_sets_aux = [ community_term_set for community_term_set in community_term_sets if len( community_term_set ) > max_community_size_thresh ]
    
    return( big_community_term_sets_aux , XL_community_term_sets_aux )


def adaptive_big_community_find( xl , max_community_size_thresh , tt_overlap_measure , min_weight_tt_edge , max_dcnt , term_types_dict , GO_term_stats , term_genes_dict ):
    # PRE-CONDITION: Function only called on sets of terms that are allowed to be clustered, 
    # so if COMBINE_TERM_TYPES is FALSE, we assume that only terms of one type have been passed
    # in a call to this function... We do not check the validity of this assumption here.
    # Similarly we assume that MIN_NUM_GENES is exceeded for each term, too, etc.
    my_xl = xl
    
    my_min_weight_tt_edge = min_weight_tt_edge
    my_max_dcnt = max_dcnt
    
    big_community_term_sets = []
    
    
    while( len( my_xl ) > 0 and ( ( my_min_weight_tt_edge <= 0.9 ) or ( my_max_dcnt >= 10 ) ) ):
        
        putative_xl_terms = [ term for xl_term_set in my_xl for term in xl_term_set ]
        my_max_dcnt = my_max_dcnt - 5
        
        my_xl_terms = []
        
        for xl_t in putative_xl_terms:
            if not( term_types_dict[ xl_t ].lower() == "go" ):
                my_xl_terms.append( xl_t )
            else:
                xl_t_dcnt , xl_t_level = GO_term_stats[ xl_t ]
                if( xl_t_dcnt <= my_max_dcnt ):
                    my_xl_terms.append( xl_t )
         
        ( big_community_term_sets_aux , my_xl ) = adaptive_big_community_find_aux( my_xl_terms , max_community_size_thresh , tt_overlap_measure , my_min_weight_tt_edge , term_genes_dict )
         
        big_community_term_sets = big_community_term_sets + big_community_term_sets_aux
        
        if( len( my_xl ) > 0 ):
            my_xl_terms = [ term for xl_term_set in my_xl for term in xl_term_set ]
            my_min_weight_tt_edge = my_min_weight_tt_edge + 0.1
            ( big_community_term_sets_aux , my_xl ) = adaptive_big_community_find_aux( my_xl_terms , max_community_size_thresh , tt_overlap_measure , my_min_weight_tt_edge , term_genes_dict )
            
            big_community_term_sets = big_community_term_sets + big_community_term_sets_aux
            
    return big_community_term_sets + my_xl    



def get_big_community_term_sets(terms_graph, max_community_size_thresh, tt_overlap_measure, min_weight_tt_edge, max_dcnt, term_types_dict, GO_term_stats, term_genes_dict):
    community_term_sets = []
    big_community_term_sets_aux = []
    XL_community_term_sets = []
    adapted_big_community_term_sets = []
    big_community_term_sets = []
        
    if( len( terms_graph.edges  )>0 ):
        community_term_sets = list( greedy_modularity_communities( terms_graph ) )

    big_community_term_sets_aux = [ community_term_set for community_term_set in community_term_sets if ( ( len( community_term_set ) > 1 ) and ( len( community_term_set ) <= max_community_size_thresh ) ) ]
    XL_community_term_sets = [ community_term_set for community_term_set in community_term_sets if len( community_term_set ) > max_community_size_thresh ]
    adapted_big_community_term_sets = adaptive_big_community_find( XL_community_term_sets , max_community_size_thresh , tt_overlap_measure , min_weight_tt_edge , max_dcnt , term_types_dict , GO_term_stats , term_genes_dict )
    big_community_term_sets = big_community_term_sets_aux + adapted_big_community_term_sets
    big_community_term_sets.sort( key=len , reverse=True )
    
    return big_community_term_sets

def build_big_communities_list(big_community_term_sets, big_community_stub,
                                quant_data_type, exp_gene_qd, exp_ids, 
                                term_types_dict, term_defs_dict, 
                                term_genes_dict, exp_term_dotplot_dict, 
                                abs_images_dir, rel_images_dir,  
                                extra_annotations_dict, num_extra_annotations,
                                new_h, heatmap_width_min, heatmap_height_min,
                                heatmap_min, heatmap_max, search_words, 
                                info_string, msigdb_html_soup, go_dag, 
                                exp_img_dir_paths_dict, exp_img_extension_dict):
    
    big_communities = []
    bc_index = 1
    for community_term_set in big_community_term_sets:
        
        if(bc_index < 10):
            bc_name = big_community_stub + "0" + str(bc_index)
        else:
            bc_name = big_community_stub + str(bc_index)
        
        big_communities.append(gfc.bigCommunity(bc_name, list(community_term_set), 
                                                  quant_data_type, exp_gene_qd, 
                                                  exp_ids, term_types_dict, 
                                                  term_defs_dict, term_genes_dict, 
                                                  exp_term_dotplot_dict, abs_images_dir, 
                                                  rel_images_dir,  
                                                  extra_annotations_dict, num_extra_annotations,
                                                  new_h, heatmap_width_min, heatmap_height_min,
                                                  heatmap_min, heatmap_max, search_words, 
                                                  info_string, msigdb_html_soup, go_dag, 
                                                  exp_img_dir_paths_dict, exp_img_extension_dict))
        
        bc_index += 1
    return big_communities

def build_singleton_communities_list(terms_list, big_community_term_sets,
                                quant_data_type, exp_gene_qd, exp_ids, 
                                term_types_dict, term_defs_dict, 
                                term_genes_dict, exp_term_dotplot_dict, 
                                abs_images_dir, rel_images_dir,  
                                extra_annotations_dict, num_extra_annotations,
                                new_h,heatmap_width_min, heatmap_height_min,
                                heatmap_min, heatmap_max, search_words, 
                                info_string, msigdb_html_soup, go_dag, 
                                exp_img_dir_paths_dict, exp_img_extension_dict,
                                new_h_singleton_adjustment):
    
    terms_in_big_communities = set([term for community_term_set \
                                    in big_community_term_sets for term in community_term_set])
    
    terms_remaining = list( set(terms_list) - terms_in_big_communities )

    terms_remaining_sorted = [st for (st, st_type) in sorted([(t, term_types_dict[t]) for t in terms_remaining], key = lambda x: (x[1], x[0]))]
    
    singleton_communities = []

    for remaining_term in terms_remaining_sorted:
        singleton_communities.append(gfc.singletonCommunity(remaining_term, 
                                                              [remaining_term], 
                                                              quant_data_type, exp_gene_qd, 
                                                              exp_ids, term_types_dict, term_defs_dict, 
                                                              term_genes_dict, exp_term_dotplot_dict, 
                                                              abs_images_dir, rel_images_dir,  
                                                              extra_annotations_dict, num_extra_annotations,
                                                              new_h - new_h_singleton_adjustment, 
                                                              heatmap_width_min, heatmap_height_min, heatmap_min, heatmap_max, 
                                                              search_words, info_string, msigdb_html_soup, go_dag, 
                                                              exp_img_dir_paths_dict, exp_img_extension_dict))
        
    return singleton_communities
        

def get_big_community_labels_for_terms(big_communities):
    term_community_pairs = []
    for bc in big_communities:
        term_community_pairs = term_community_pairs + [(term, bc.name) for term in bc.terms]

    return term_community_pairs

def get_big_community_labels_for_terms_from_term_sets(big_community_term_sets):
    term_community_pairs = []
    for bc_index in range(len(big_community_term_sets)):
        term_community_pairs = term_community_pairs + [(term, str(bc_index+1)) for term in big_community_term_sets[bc_index]]

    return term_community_pairs


def build_terms_distance_matrix(term_community_pairs, term_genes_dict, tt_overlap_measure):
    
    terms_ordered_by_community = [t for (t,c) in term_community_pairs]
    terms_distance_matrix = np.zeros((len(terms_ordered_by_community), len(terms_ordered_by_community))) 
    
    for t_index in range(len(terms_ordered_by_community)-1):
        
        t1 = terms_ordered_by_community[t_index]
        t1_genes = term_genes_dict[ t1 ] 
        
        for t_index2 in range(t_index+1, len(terms_ordered_by_community)):
            
            t2 = terms_ordered_by_community[t_index2]
            t2_genes = term_genes_dict[ t2 ]
    
            similarity = 0
            if( tt_overlap_measure == 'OC' ):
                similarity = len( set.intersection( t1_genes , t2_genes ) )/ min( len( t1_genes ) , len( t2_genes ) )
            if( tt_overlap_measure == 'JI' ):
                similarity = len( set.intersection( t1_genes , t2_genes ) )/ len( set.union( t1_genes , t2_genes ) )
                
            distance = 1 - similarity
            terms_distance_matrix[t_index,t_index2] = distance
            terms_distance_matrix[t_index2,t_index] = distance
    
    return(terms_distance_matrix)
    
def calc_prop_terms_in_big_communities(term_community_labels, term_genes_dict):
    return(len(term_community_labels)/len(term_genes_dict))    
    
def make_silhouette_plot(terms_distance_matrix, term_community_labels, big_communities, term_genes_dict, abs_images_dir, rel_images_dir, etg_name, new_h):
    
    silhouette_avg = silhouette_score(terms_distance_matrix, term_community_labels, metric="precomputed")
    sample_silhouette_values = silhouette_samples(terms_distance_matrix, term_community_labels, metric="precomputed")
    prop_terms_in_big_communities = calc_prop_terms_in_big_communities(term_community_labels, term_genes_dict)
    num_big_communities = len(big_communities)
    
    fig, ax = pyplot.subplots()
    
    ax.set_xlim([min(0,min(sample_silhouette_values))-0.1, 1])
    ax.set_ylim([0, len(terms_distance_matrix) + (num_big_communities + 2) * 10])
    
    ax.fill_betweenx(
            np.arange(10,12),
            0,
            [prop_terms_in_big_communities, prop_terms_in_big_communities],
            facecolor='g',
            edgecolor='g',
            alpha=0.7
    )
    
    ax.text(-0.05, 11, "proportion terms in big communities" , fontsize='xx-small')
    ax.axhspan(0, 20, facecolor='0.5', alpha=0.25)
    
    y_lower = 22
    
    for i in range(num_big_communities-1,-1,-1):
    
        # Aggregate the silhouette scores for samples belonging to
        # cluster i, and sort them
        ith_cluster_silhouette_values = sample_silhouette_values[term_community_labels == big_communities[i].name]

        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        #color = pyplot.cm.nipy_spectral(float(i) / num_big_communities)
        color = pyplot.cm.cool(float(i) / num_big_communities)
        ax.fill_betweenx(
            np.arange(y_lower, y_upper),
            0,
            ith_cluster_silhouette_values,
            facecolor=color,
            edgecolor=color,
            alpha=0.7,
        )

        # Label the silhouette plots with their cluster numbers at the middle
        ax.text(-0.05, y_lower + 0.5 * size_cluster_i, gfc.trim_term(big_communities[i].name), fontsize='xx-small')

        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples

    # add blank text to stretch the plot vertically
    #ax.set_title("Silhouette plot for communities", fontsize='x-small')
    ax.set_xlabel("silhouette coefficient", fontsize='xx-small')
    ax.tick_params(axis='x', labelsize=6)

    # The vertical line for average silhouette score of all the values
    ax.axvline(x=silhouette_avg, color="red", linestyle="--")

    ax.set_yticks([])  # Clear the yaxis labels / ticks
    #ax.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])
    pyplot.savefig(abs_images_dir + etg_name  + "_sil_plot.png", bbox_inches="tight", dpi=300)
    pyplot.close()
    
    image = Image.open(abs_images_dir + etg_name  + "_sil_plot.png")
    w,h = image.size
    new_w = int(new_h * w/h)
    image.close()
            
    return (rel_images_dir + etg_name + "_sil_plot.png", new_w, new_h)


def make_sil_violinplots(min_weight_tt_edge, max_community_size_thresh, combine_term_types, type_2_term_dict,
                                 etg_terms, term_genes_dict, tested_overlap_measure, tt_overlap_measure,
                                 max_dcnt, term_types_dict, GO_term_stats, 
                                 abs_images_dir, rel_images_dir, etg_name, new_h):
    
    
    min_weight_tt_edge_trials = sorted(set([x/10 for x in list(range(2,9,2))] + [min_weight_tt_edge]))
    max_community_size_thresh_trials = sorted(set([10,15,20,max_community_size_thresh]))
    
    fig, axes = pyplot.subplots(len(min_weight_tt_edge_trials), len(max_community_size_thresh_trials), figsize=(16, 10))
    #fig.tight_layout()
    
    #for min_weight_tt_edge_try in min_weight_tt_edge_trials:
    for min_weight_tt_edge_try_i in range(len(min_weight_tt_edge_trials)):
        
        min_weight_tt_edge_try = min_weight_tt_edge_trials[min_weight_tt_edge_try_i]
        
        sub_terms_graphs_try = []
        if(combine_term_types or len(type_2_term_dict.keys())==1):
            sub_terms_graphs_try.append(build_terms_graph(etg_terms, term_genes_dict, tested_overlap_measure, min_weight_tt_edge_try))
        else:
            type_2_term_dict_keys = list(type_2_term_dict.keys())
            type_2_term_dict_keys.sort()
            for type_2_term_dict_key in type_2_term_dict_keys:
                sub_terms_list = type_2_term_dict[type_2_term_dict_key]
                sub_terms_graphs_try.append(build_terms_graph(sub_terms_list, term_genes_dict, tested_overlap_measure, min_weight_tt_edge_try))
            
        #for max_community_size_thresh_try in max_community_size_thresh_trials:
        for max_community_size_thresh_try_i in range(len(max_community_size_thresh_trials)):
            
            max_community_size_thresh_try = max_community_size_thresh_trials[max_community_size_thresh_try_i]
            big_community_term_sets_try = []
            for sub_terms_graph_try in sub_terms_graphs_try:
                big_community_term_sets_try = big_community_term_sets_try + get_big_community_term_sets(sub_terms_graph_try, max_community_size_thresh_try,
                                                                                                            tested_overlap_measure, min_weight_tt_edge_try, 
                                                                                                            max_dcnt, term_types_dict, GO_term_stats, 
                                                                                                            term_genes_dict)
            
            
                
            num_big_communities_try = len(big_community_term_sets_try)
           
            
            
            term_community_pairs_try = get_big_community_labels_for_terms_from_term_sets(big_community_term_sets_try)
            term_community_labels_try = np.array([c for (t,c) in term_community_pairs_try])
            #prop_try = gfb.calc_prop_terms_in_big_communities(term_community_labels_try, term_genes_dict)
            
            
            
            if((num_big_communities_try >= 2) & (num_big_communities_try <= (len(term_community_pairs_try)-1))):
                if((tested_overlap_measure == tt_overlap_measure) & 
                   (min_weight_tt_edge_try == min_weight_tt_edge) & 
                   (max_community_size_thresh_try==max_community_size_thresh)):
                    axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].set_facecolor("yellow")
                
                
                terms_distance_matrix_try = build_terms_distance_matrix(term_community_pairs_try, term_genes_dict, tested_overlap_measure)
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
                
                
                community_cum_prop_of_total_df = sample_silhouette_values_try_df.groupby('Community', sort=False).size().cumsum().reset_index()
                community_cum_prop_of_total_df['cum prop of total terms'] = [(x/len(term_genes_dict))*100 for x in sample_silhouette_values_try_df.groupby('Community', sort=False).size().cumsum()]
            

                axis = axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i]
                ax_twin = axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].twinx()
                ax_twin.bar(community_cum_prop_of_total_df['Community'], community_cum_prop_of_total_df['cum prop of total terms'], alpha=0.25)
                ax_twin.set_ylim([0,100])
                if(max_community_size_thresh_try_i == (len(max_community_size_thresh_trials)-1)):
                    ax_twin.yaxis.tick_right()
                    ax_twin.set_ylabel("Cum. % terms")
                
                
                sns.violinplot(ax=axis, data=sample_silhouette_values_try_df,y='Silhouette Score', x='Community', color="red",inner=None, cut=0)
                
                axis.axhline(y = 0, color = 'k', linestyle = '-')
                axis.axhline(y = 0.5, color = 'darkgrey', linestyle = '--')
                axis.axhline(y = silhouette_avg_try, color = 'r', linestyle = ':')
                
                
                #axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].set_xticklabels([]])
                axis.set_ylim([-1.1,1.1])
                
                if(max_community_size_thresh_try_i > 0 ):
                    axis.set_ylabel("")
                if(min_weight_tt_edge_try_i < (len(min_weight_tt_edge_trials)-1)):
                    axis.set_xlabel("")
                
                
                if(len(axis.get_xticks()) > 5):
                    axis.set_xticks(axis.get_xticks()[::2])
                
                axis.set_title("OM=" + tested_overlap_measure + ", GSO=" + str(min_weight_tt_edge_try) + ", MCS=" + str(max_community_size_thresh_try))
            else:
                axis = axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i]
                ax_twin = axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].twinx()
                ax_twin.set_ylim([0,100])
                if(max_community_size_thresh_try_i == (len(max_community_size_thresh_trials)-1)):
                    ax_twin.yaxis.tick_right()
                    ax_twin.set_ylabel("Cum. % terms")
                
                
                axis.axhline(y = 0, color = 'k', linestyle = '-')
                axis.axhline(y = 0.5, color = 'darkgrey', linestyle = '--')
                
                
                #axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].set_xticklabels([]])
                axis.set_ylim([-1.1,1.1])
                
                if(max_community_size_thresh_try_i == 0 ):
                    axis.set_ylabel("Silhouette Score")
                if(min_weight_tt_edge_try_i == (len(min_weight_tt_edge_trials)-1)):
                    axis.set_xlabel("Community")
                
                
                axis.set_xticks([])
                
                axis.set_title("OM=" + tested_overlap_measure + ", GSO=" + str(min_weight_tt_edge_try) + ", MCS=" + str(max_community_size_thresh_try))
            
                
                
                
                
#                sns.violinplot(ax=axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i], data=sample_silhouette_values_try_df,
#                                                                                                   y='Silhouette Score', x='Community',
#                                                                                                   color="red",inner=None, cut=0)
#                
#                axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].axhline(y = 0, color = 'k', linestyle = '-')
#                axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].axhline(y = 0.5, color = 'darkgrey', linestyle = '--')
#                axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].axhline(y = silhouette_avg_try, color = 'r', linestyle = ':')
#                
#                
#                #axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].set_xticklabels([]])
#                axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].set_ylim([-1.1,1.1])
#                
#                if(max_community_size_thresh_try_i > 0 ):
#                    axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].set_ylabel("")
#                if(min_weight_tt_edge_try_i < (len(min_weight_tt_edge_trials)-1)):
#                    axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].set_xlabel("")
#                    
#                axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].set_title(str(min_weight_tt_edge_try) + ", " + str(max_community_size_thresh_try))
#                
#                axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].set_xticklabels(axes[min_weight_tt_edge_try_i, max_community_size_thresh_try_i].get_xticklabels(), rotation=45, ha='right', va='top')
#               
    pyplot.subplots_adjust(hspace=0.7)            
    pyplot.savefig(abs_images_dir + etg_name + "_sil_violinplots_" + tested_overlap_measure + ".png", bbox_inches="tight")
    pyplot.close()
    image = Image.open(abs_images_dir + etg_name + "_sil_violinplots_" + tested_overlap_measure + ".png")
    w,h = image.size
    new_w = int(new_h * w/h)
    image.close()
            
    return (rel_images_dir + etg_name + "_sil_violinplots_" + tested_overlap_measure + ".png", new_w, new_h)
    
def build_big_communities_tracker_and_graph(big_communities, bc_bc_overlap_measure, min_weight_bc_bc):
    big_communities_tracker_dict = {}
    big_communities_graph = nx.Graph()
    bc_1_index = 0
    for bc_1 in big_communities[0:len(big_communities)-1]:
        for bc_2 in big_communities[(bc_1_index + 1):len(big_communities)]:
            
            weight = bc_1.calc_overlap(bc_2, bc_bc_overlap_measure)
            
            if weight > min_weight_bc_bc:
                big_communities_graph.add_edges_from([(bc_1.name, bc_2.name, {'w':weight})])
                big_communities_tracker_dict[bc_1.name] = bc_1
                big_communities_tracker_dict[bc_2.name] = bc_2
        bc_1_index += 1
        
    return(big_communities_tracker_dict, big_communities_graph)
    


def adaptive_big_meta_community_find_aux(xl_communities, max_meta_community_size_thresh, bc_bc_overlap_measure, min_weight_bc_bc):
    xl_big_communities_graph = nx.Graph()
    bc_1_index = 0
    
    for bc_1 in xl_communities[0:len(xl_communities)-1]:
        for bc_2 in xl_communities[(bc_1_index + 1):len(xl_communities)]:
            
            weight = bc_1.calc_overlap(bc_2, bc_bc_overlap_measure)
            
            if weight > min_weight_bc_bc:
                xl_big_communities_graph.add_edges_from([(bc_1.name, bc_2.name, {'w':weight})])
        bc_1_index += 1

        
    meta_community_community_sets = []
    if( len( xl_big_communities_graph.edges  )>0 ):
        meta_community_community_sets = list(greedy_modularity_communities(xl_big_communities_graph))
        
    big_meta_community_community_sets_aux = [ meta_community_community_set for meta_community_community_set in meta_community_community_sets 
                                             if ((len(meta_community_community_set) > 1) and (len(meta_community_community_set) <=  max_meta_community_size_thresh))]
    XL_meta_community_community_sets_aux = [ meta_community_community_set for meta_community_community_set in meta_community_community_sets 
                                        if len(meta_community_community_set) > max_meta_community_size_thresh]
    
    return( big_meta_community_community_sets_aux , XL_meta_community_community_sets_aux )


def adaptive_big_meta_community_find(xl, big_communities_tracker_dict, max_meta_community_size_thresh, bc_bc_overlap_measure, min_weight_bc_bc):
    
    my_xl = xl
    
    my_min_weight_bc_bc = min_weight_bc_bc
    
    big_meta_community_community_sets = []
    
    
    while(len(my_xl) > 0 and (my_min_weight_bc_bc <= 0.9)):
        
        my_xl_communities = [ big_communities_tracker_dict[community] for xl_meta_community_community_set in my_xl for community in xl_meta_community_community_set ]
        
        my_min_weight_bc_bc = my_min_weight_bc_bc + 0.1
        (big_meta_community_community_sets_aux, my_xl) = adaptive_big_meta_community_find_aux(my_xl_communities, max_meta_community_size_thresh, bc_bc_overlap_measure, min_weight_bc_bc)
            
        big_meta_community_community_sets = big_meta_community_community_sets + big_meta_community_community_sets_aux
            
    return big_meta_community_community_sets + my_xl 




def get_big_meta_community_community_sets(big_communities_graph, big_communities_tracker_dict, max_meta_community_size_thresh, bc_bc_overlap_measure, min_weight_bc_bc):
    meta_community_community_sets = []
    big_meta_community_community_sets_aux = []
    XL_meta_community_community_sets = []
    adapted_big_meta_community_community_sets = []
    big_meta_community_community_sets = []
        
    if( len( big_communities_graph.edges  )>0 ):
        meta_community_community_sets = list(greedy_modularity_communities(big_communities_graph))

    big_meta_community_community_sets_aux = [ meta_community_community_set for meta_community_community_set in meta_community_community_sets 
                                             if ((len(meta_community_community_set) > 1) and (len(meta_community_community_set) <=  max_meta_community_size_thresh))]
    XL_meta_community_community_sets = [ meta_community_community_set for meta_community_community_set in meta_community_community_sets 
                                        if len(meta_community_community_set) > max_meta_community_size_thresh]
    adapted_big_meta_community_community_sets = adaptive_big_meta_community_find(XL_meta_community_community_sets, big_communities_tracker_dict, max_meta_community_size_thresh, bc_bc_overlap_measure, min_weight_bc_bc)
    big_meta_community_community_sets = big_meta_community_community_sets_aux + adapted_big_meta_community_community_sets
    big_meta_community_community_sets.sort( key=len , reverse=True )
    
    return big_meta_community_community_sets


def build_meta_communities_list(big_communities, meta_community_stub,
                                bc_bc_overlap_measure, min_weight_bc_bc,
                                max_meta_community_size_thresh,
                                quant_data_type, exp_gene_qd, exp_ids,
                                abs_images_dir, rel_images_dir,  
                                extra_annotations_dict, num_extra_annotations,
                                new_h, heatmap_width_min, heatmap_height_min,
                                heatmap_min, heatmap_max, search_words,
                                info_string):
    
    (big_communities_tracker_dict, big_communities_graph) = \
                                build_big_communities_tracker_and_graph(big_communities, 
                                                                        bc_bc_overlap_measure, 
                                                                        min_weight_bc_bc)                           
#    meta_community_community_sets = []
#    if( len(big_communities_graph.edges) > 0 ):
#        meta_community_community_sets = list(greedy_modularity_communities(big_communities_graph))
#    
#    big_meta_community_community_sets = \
#        [meta_community_community_set for meta_community_community_set in \
#         meta_community_community_sets if len(meta_community_community_set) > 1]
        
    
    big_meta_community_community_sets = get_big_meta_community_community_sets(big_communities_graph, big_communities_tracker_dict, max_meta_community_size_thresh, bc_bc_overlap_measure, min_weight_bc_bc)
    
    meta_communities = []
    mg_index = 1
    for meta_community_community_set in big_meta_community_community_sets:
        if( mg_index < 10 ):
            mg_name = meta_community_stub + "0" + str(mg_index)
        else:
            mg_name = meta_community_stub + str(mg_index)
        
        # make the meta group
        meta_communities.append(gfc.metaGroup(mg_name, 
                                          [big_communities_tracker_dict[bc_name] \
                                               for bc_name in list(meta_community_community_set)], 
                                          quant_data_type, exp_gene_qd, exp_ids, 
                                          abs_images_dir, rel_images_dir,  
                                          extra_annotations_dict, num_extra_annotations,
                                          new_h, heatmap_width_min, heatmap_height_min,
                                          heatmap_min, heatmap_max, search_words, 
                                          info_string))
        mg_index +=1
        
        # link each community in the meta group back to the meta group name, and also to its meta group siblings
        for bc_name in list(meta_community_community_set):
            big_communities_tracker_dict[bc_name].set_meta_community_name(mg_name)
            big_communities_tracker_dict[bc_name].set_meta_community_siblings([big_communities_tracker_dict[bcn] \
                                                                              for bcn in list(meta_community_community_set - {bc_name})])
            
    # finally, identify those big communities that are not members of a meta 
    #community, these are singleton meta communities
    singleton_meta_communities = [bc for bc in big_communities if not(bc.meta_community_name)]
    
    return(meta_communities, singleton_meta_communities)

                                
    
def build_all_communities_lists(terms_list, big_community_term_sets, 
                                big_community_stub, meta_community_stub, 
                                sc_bc_overlap_measure, min_weight_sc_bc,
                                bc_bc_overlap_measure, min_weight_bc_bc,
                                max_meta_community_size_thresh,
                                quant_data_type, exp_gene_qd, exp_ids, 
                                term_types_dict, term_defs_dict, 
                                term_genes_dict, exp_term_dotplot_dict, 
                                abs_images_dir, rel_images_dir,  
                                extra_annotations_dict, num_extra_annotations,
                                new_h, heatmap_width_min, heatmap_height_min,
                                heatmap_min, heatmap_max, search_words, 
                                info_string, msigdb_html_soup, go_dag, 
                                exp_img_dir_paths_dict, exp_img_extension_dict,
                                new_h_singleton_adjustment=0):
    
    big_communities = build_big_communities_list(big_community_term_sets, 
                                                  big_community_stub,
                                                  quant_data_type, exp_gene_qd, exp_ids, 
                                                  term_types_dict, term_defs_dict, 
                                                  term_genes_dict, exp_term_dotplot_dict, 
                                                  abs_images_dir, rel_images_dir,  
                                                  extra_annotations_dict, num_extra_annotations,
                                                  new_h, heatmap_width_min, heatmap_height_min, 
                                                  heatmap_min, heatmap_max, search_words, 
                                                  info_string, msigdb_html_soup, go_dag, 
                                                  exp_img_dir_paths_dict, exp_img_extension_dict)
    
    singleton_communities = build_singleton_communities_list(terms_list, big_community_term_sets,
                                                        quant_data_type, exp_gene_qd, exp_ids, 
                                                        term_types_dict, term_defs_dict, 
                                                        term_genes_dict, exp_term_dotplot_dict, 
                                                        abs_images_dir, rel_images_dir,  
                                                        extra_annotations_dict, num_extra_annotations,
                                                        new_h,heatmap_width_min, heatmap_height_min,
                                                        heatmap_min, heatmap_max, search_words, 
                                                        info_string, msigdb_html_soup, go_dag, 
                                                        exp_img_dir_paths_dict, exp_img_extension_dict,
                                                        new_h_singleton_adjustment)
    
    # find overlapping communities - their individual terms did not cluster, but there is still some
    # overlap between aggregates **************************************************

    for bc in big_communities:
        for sc in singleton_communities:
            if bc.calc_overlap( sc , sc_bc_overlap_measure ) > min_weight_sc_bc:
                bc.add_overlapping_singleton_community_name( sc.name )
                sc.add_overlapping_big_community( bc )
                
    
    (meta_communities, singleton_meta_communities) = \
        build_meta_communities_list(big_communities, meta_community_stub,
                                bc_bc_overlap_measure, min_weight_bc_bc,
                                max_meta_community_size_thresh,
                                quant_data_type, exp_gene_qd, exp_ids,
                                abs_images_dir, rel_images_dir, 
                                extra_annotations_dict, num_extra_annotations,
                                new_h, heatmap_width_min, heatmap_height_min,
                                heatmap_min, heatmap_max, search_words,
                                info_string)
        
    return(big_communities, singleton_communities, meta_communities, singleton_meta_communities)

    
    
    
    
    
    
    
    
    
    
