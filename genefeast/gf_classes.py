#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: avigailtaylor
"""

# IMPORTS *********************************************************************

from pathlib import Path

import collections
import matplotlib as mp
import numpy as np
import pandas as pd
import pycircos
import seaborn as sns
import upsetplot as up
from PIL import Image
from collections import OrderedDict
from goatools import godag_plot
from itertools import combinations
from matplotlib import pyplot
#from matplotlib.tight_layout import get_renderer
from scipy.cluster.hierarchy import dendrogram, linkage
from upsetplot import from_contents
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
Garc = pycircos.Garc
Gcircle = pycircos.Gcircle

# GLOBAL FUNCTIONS ************************************************************
def trim_term(term, strong_trim=False):
        if term.find('community') == 0:
            if(strong_trim):
                return term.split('(')[0].split(' ')[1]
            else:
                return term.split('(')[0]
        
        elif term.find('FEATSI') == 0: #(FEATSI stands for FEA term-set intersection)
            
            if(strong_trim):
                return term.split('_')[1].split(' ')[1]
            else:
                return ' '.join(term.split('_')[1].split(' ')[0:2])
        elif(len(term) > 15):
            return term[0:15] + '...'
        else:
            return term
        
def annotate_trimmed_terms(trimmed_terms):
    annotated_trimmed_terms = [trimmed_terms[0]]
    for i in range(1, len(trimmed_terms)):
        x = trimmed_terms[0:i].count(trimmed_terms[i])
        if(x > 0):
            annotated_trimmed_terms.append(trimmed_terms[i] + str(x + 1))
        else:
            annotated_trimmed_terms.append(trimmed_terms[i])
    return annotated_trimmed_terms

def build_searches(gene, search_words):
    
    ncbi_gene_href = 'https://www.ncbi.nlm.nih.gov/gene?Db=gene&Cmd=DetailsSearch&Term=' + gene
    pubmed_gene_href = 'https://pubmed.ncbi.nlm.nih.gov/?term=' + gene + '[Title/Abstract]'
    pubmed_search_href = 'https://pubmed.ncbi.nlm.nih.gov/?term=' + gene + '[Title/Abstract] AND ' + '(' + ' OR '.join(['+'.join( sw.split()) + '[Title/Abstract]' for sw in search_words]) + ')'
    
    pubmed_print_string = ''
    if(len(search_words) > 0):
        pubmed_print_string = gene + ' AND ' + '( ' + ' OR '.join(search_words) + ' )'

    return(ncbi_gene_href, pubmed_gene_href, pubmed_search_href, pubmed_print_string)
        
# CLASSES *********************************************************************

# Helper classes
class my_UpSet(up.UpSet):
    # This is copied directly from the original - the only change is the value
    # of MAGIC_MARGIN, from 10 to 50, so that there is enough space in the 
    # plot for the FEA labels.
    def make_grid(self, fig=None):
        """Get a SubplotSpec for each Axes, accounting for label text width
        """
        
        n_cats = len(self.totals)
        n_inters = len(self.intersections)

        if fig is None:
            fig = pyplot.gcf()

        # Determine text size to determine figure size / spacing
        r = fig.canvas.get_renderer()
        t = fig.text(0, 0, '\n'.join(self.totals.index.values))
        textw = t.get_window_extent(renderer=r).width
        t.remove()

        MAGIC_MARGIN = 50  # FIXME
        figw = self._reorient(fig.get_window_extent(renderer=r)).width

        sizes = np.asarray([p['elements'] for p in self._subset_plots])

        if self._element_size is None:
            colw = (figw - textw - MAGIC_MARGIN) / (len(self.intersections) +
                                                    self._totals_plot_elements)
        else:
            fig = self._reorient(fig)
            render_ratio = figw / fig.get_figwidth()
            colw = self._element_size / 72 * render_ratio
            figw = (colw * (len(self.intersections) +
                            self._totals_plot_elements) +
                    MAGIC_MARGIN + textw)
            fig.set_figwidth(figw / render_ratio)
            fig.set_figheight((colw * (n_cats + sizes.sum())) /
                              render_ratio)

        text_nelems = int(np.ceil(figw / colw - (len(self.intersections) +
                                                 self._totals_plot_elements)))

        GS = self._reorient(mp.gridspec.GridSpec)
        gridspec = GS(*self._swapaxes(n_cats + (sizes.sum() or 0),
                                      n_inters + text_nelems +
                                      self._totals_plot_elements), hspace=1)
        if self._horizontal:
            out = {'matrix': gridspec[-n_cats:, -n_inters:],
                   'shading': gridspec[-n_cats:, :],
                   'totals': gridspec[-n_cats:, :self._totals_plot_elements],
                   'gs': gridspec}
            cumsizes = np.cumsum(sizes[:: -1])
            for start, stop, plot in zip(np.hstack([[0], cumsizes]), cumsizes,
                                         self._subset_plots[:: -1]):
                out[plot['id']] = gridspec[start:stop, -n_inters:]
        else:
            out = {'matrix': gridspec[-n_inters:, :n_cats],
                   'shading': gridspec[:, :n_cats],
                   'totals': gridspec[:self._totals_plot_elements, :n_cats],
                   'gs': gridspec}
            cumsizes = np.cumsum(sizes)
            for start, stop, plot in zip(np.hstack([[0], cumsizes]), cumsizes,
                                         self._subset_plots):
                out[plot['id']] = \
                    gridspec[-n_inters:, start + n_cats:stop + n_cats]
        return out


class upsetDrawer:
    def __init__ (self, community):
        self.community = community
    
    def draw_upset_plot(self):
        trimmed_terms = [trim_term(term) for term in self.community.terms]
        annotated_trimmed_terms = annotate_trimmed_terms(trimmed_terms)
        annotated_trimmed_term_genes_dict = {}
        for (term, annotated_trimmed_term) in zip(self.community.terms, annotated_trimmed_terms):
            annotated_trimmed_term_genes_dict[annotated_trimmed_term] = self.community.term_genes_dict[term]
        
        community_df = from_contents(annotated_trimmed_term_genes_dict)
        annotated_trimmed_terms.reverse()
        community_df = community_df.reorder_levels(annotated_trimmed_terms)
        
        my_upset = my_UpSet(community_df, sort_categories_by = None,  sort_by='-degree')
        my_upset.plot(fig=pyplot.figure(dpi = 120))
           
        pyplot.savefig(self.community.abs_images_dir + self.community.name.replace(' ', '') + "_upset.png", bbox_inches="tight")
        pyplot.close()
        image = Image.open(self.community.abs_images_dir + self.community.name.replace(' ', '') + "_upset.png")
        w,h = image.size
        image.close()

        new_w = int(self.community.new_h * w/h)
        
        return (self.community.rel_images_dir + self.community.name.replace(' ', '') + "_upset.png", new_w)
        
class upsetDrawer_app2: # an upsetDrawer for my_app_3... Requirements are quite different compared to upsetDrawer for communities in app and app_2.
    def __init__ (self, name, sets_of, upset_df, new_h, abs_images_dir, rel_images_dir, basic_upset=True, trim=False):
        self.name  = name
        self.sets_of = sets_of
        self.upset_df = upset_df.copy()
        self.new_h = new_h
        self.rel_images_dir = rel_images_dir
        self.abs_images_dir = abs_images_dir
        self.basic_upset = basic_upset
        
        if(trim):
            self.upset_df.index.rename([trim_term(term) for term in self.upset_df.index.names], inplace=True)
        
        if self.basic_upset:
            self.upset = my_UpSet(self.upset_df)
        else:
            self.upset = my_UpSet(self.upset_df, sort_categories_by=None, totals_plot_elements=5)
    
    def draw_upset_plot(self):
        self.upset.plot(fig=pyplot.figure(dpi=120))
        pyplot.savefig(self.abs_images_dir + self.name.replace(' ', '') + "_" + self.sets_of  + "_upset.png", bbox_inches="tight")
        pyplot.close()
        image = Image.open(self.abs_images_dir + self.name.replace(' ', '') + "_" + self.sets_of + "_upset.png")
        w,h = image.size
        image.close()
        
        new_w = int(self.new_h * w/h)
        
        return (self.rel_images_dir + self.name.replace(' ', '') + "_" + self.sets_of + "_upset.png", new_w)


class circosDrawer:
    def __init__ (self, etg, rows_cols, trim_terms=True, metaGroupCircosDrawer = False):
        self.etg = etg
        self.rows_cols = rows_cols
        self.trim_terms = trim_terms
        self.trimmed_term_mapping_dict = self.__build_trimmed_term_mapping_dict(metaGroupCircosDrawer)
        self.metaGroupCircosDrawer = metaGroupCircosDrawer
        self.metaGroup_barplot_dict = self.__build_metaGroup_barplot_dict()
        
    def __get_lordered_gene_exp_heatmap_fm_subset_df(self, s_cols, cluster_genes):
        
        heatmap_df = self.etg.gene_exp_heatmap_df.loc[:, s_cols]
        heatmap_fm_df = self.etg.gene_exp_heatmap_fm_df.loc[:, s_cols]
        
        
        if(len(cluster_genes) > 1):
            Z = linkage(heatmap_df.values.T, 'ward', optimal_ordering=True)# MIGHT NEED TO REMOVE optimal_ordering=True
            dn = dendrogram(Z, no_plot=True)
            heatmap_fm_df = heatmap_fm_df.reindex(columns=[cluster_genes[gi] for gi in dn['leaves']])
            return (heatmap_fm_df, Z, dn['leaves'])
        else:
            return (heatmap_fm_df, [[]], [0])
        
    
    def __build_trimmed_term_mapping_dict(self, strict_trim):
        if(self.trim_terms):
            trimmed_terms = [trim_term(term, strict_trim) for term in self.etg.terms]
            annotated_trimmed_terms = annotate_trimmed_terms(trimmed_terms)
            return dict(zip(self.etg.terms,annotated_trimmed_terms))
        else:
            return dict(zip(self.etg.terms,self.etg.terms))
        
    
    def __build_metaGroup_barplot_dict(self):
        
        metaGroup_barplot_dict = dict()
        if(self.metaGroupCircosDrawer):
            for community in self.etg.communities:
                metaGroup_barplot_dict[self.trimmed_term_mapping_dict[community.name]] = community.term_genes_dict.values()
        return metaGroup_barplot_dict
        
    def draw_circos(self):
               
        # We want to draw the circos plot to reflect the order of genes in heatmap B. So we need to do the work to build the 
        # dataframe for that heatmap first...
        (s_rows, s_cols) = self.rows_cols
        cluster_genes = [self.etg.genes_sorted[i] for i in range(len(self.etg.genes_sorted)) if s_cols.iloc[i]]
        cluster_genes_indices = [i for i in range(len(self.etg.genes_sorted)) if s_cols.iloc[i]]
        
        gene_term_heatmap_fm_subset_df = self.etg.gene_term_heatmap_fm_df.iloc[s_rows].loc[:, s_cols]    
        (rows_t, cols_g) = gene_term_heatmap_fm_subset_df.values.shape
        
        gene_term_heatmap_fm_subset_df_COPY = gene_term_heatmap_fm_subset_df.copy()
        for exponent in range(rows_t):
            gene_term_heatmap_fm_subset_df_COPY.iloc[exponent] = gene_term_heatmap_fm_subset_df.iloc[exponent] * (2**exponent)
        gene_binary_sums = gene_term_heatmap_fm_subset_df_COPY.sum().values
        
        gene_counts = gene_term_heatmap_fm_subset_df.sum().values 
        
        ordered_cluster_genes = []
        for (gc, gbs) in list(OrderedDict.fromkeys(sorted(list(zip(gene_counts, gene_binary_sums)), key=lambda x: (-x[0], -x[1])))):
            
            subset_cluster_genes = [gene for (gene, count, binary_sum) in list(zip(cluster_genes, gene_counts, gene_binary_sums)) if (count==gc and binary_sum==gbs)]
            subset_cluster_gene_indices = [gene_index for (gene_index, count, binary_sum) in list(zip(cluster_genes_indices, gene_counts, gene_binary_sums)) if (count==gc and binary_sum==gbs)]
            subset_cluster_gene_cols = [(i in subset_cluster_gene_indices) for i in range(len(s_cols))]

            if(len(subset_cluster_genes) > 1):
                (_, _, subset_leaves) = self.__get_lordered_gene_exp_heatmap_fm_subset_df(subset_cluster_gene_cols, subset_cluster_genes)
            else:
                subset_leaves = [0]
            
            ordered_cluster_genes = ordered_cluster_genes + [subset_cluster_genes[gi] for gi in subset_leaves]
        
        gene_term_heatmap_fm_subset_df = gene_term_heatmap_fm_subset_df.reindex(columns=ordered_cluster_genes).infer_objects(copy=False)
        
        gene_term_heatmap_fm_subset_df.rename(index=self.trimmed_term_mapping_dict, inplace=True)       #print(gene_term_heatmap_fm_subset_df.index)
       
        
        # Now that we have the correct heatmap df, we can make the circos plot in the same order...
        circle = Gcircle()
        circos_dict = {}
        for gtheatmap_index, gtheatmap_row in gene_term_heatmap_fm_subset_df.iterrows():
            row_values = gtheatmap_row.values
            if(not(self.metaGroupCircosDrawer)):
                circos_dict_values  = [ np.nan if np.isnan(row_values[x]) else (gtheatmap_index, int(row_values[x] + np.nansum(row_values[0:x]) -1) , int(row_values[x] + np.nansum(row_values[0:x])), 900) for x in range(0,len(row_values))]
            else:
                circos_dict_values  = [ np.nan if np.isnan(row_values[x]) else (gtheatmap_index, int(row_values[x] + np.nansum(row_values[0:x]) -1) , int(row_values[x] + np.nansum(row_values[0:x])), 750) for x in range(0,len(row_values))]
            circos_dict[gtheatmap_index] = circos_dict_values
            
            arc = Garc(arc_id=gtheatmap_index, size=np.nansum(row_values), interspace = 1, raxis_range=(950,1000), labelposition=150, label_visible=True, labelsize=16)
            circle.add_garc(arc)
        
        circle.set_garcs()
        
        
        if(self.metaGroupCircosDrawer):
            values_all = []
            arcdata_dict = collections.defaultdict(dict)
            for gtheatmap_index, gtheatmap_row in gene_term_heatmap_fm_subset_df.iterrows():
                row_values = gtheatmap_row.values
                
                arcdata_dict[gtheatmap_index]["positions"] = range(int(np.nansum(row_values)))
                arcdata_dict[gtheatmap_index]["widths"] = [1 for x in range(int(np.nansum(row_values)))]
                arcdata_dict[gtheatmap_index]["values"] = [sum([ordered_cluster_genes[x] in v for v in self.metaGroup_barplot_dict[gtheatmap_index]]) 
                                                            for x in range(0,len(row_values)) if not(np.isnan(row_values[x]))]
                values_all.append(arcdata_dict[gtheatmap_index]["values"])
            
            #print(values_all)
            #print(min(values_all))
            #print(max(values_all))
            vmin,vmax = min([value for values in values_all for value in values]), max([value for values in values_all for value in values])
            for key in arcdata_dict:
                circle.barplot(key, data=arcdata_dict[key]["values"], positions=arcdata_dict[key]["positions"],
                               width=arcdata_dict[key]["widths"], base_value=0.0, rlim=[vmin-0.05*abs(vmin), vmax+0.05*abs(vmax)],
                               raxis_range=[800,900], facecolor="b", spine=True)
                
            
        
        
        circos_df = pd.DataFrame(circos_dict).transpose()
        num_circos_segments = circos_df.shape[0]
        circos_pair_indices = list(combinations(range(num_circos_segments),2))
        
        circos_df_columns = list(circos_df)
        
        circos_chords = [ [(circos_df[c][x], circos_df[c][y]) for (x,y) in circos_pair_indices if 
                               (isinstance(circos_df[c][x],tuple) and
                                isinstance(circos_df[c][y],tuple)) ] for c in circos_df_columns ]
        
        circos_chords_flat = [ chord_tuple for col_tuples in circos_chords for chord_tuple in col_tuples]
        
        for (chord_start, chord_end) in circos_chords_flat:
            circle.chord_plot(chord_start, chord_end)
        
        circle.figure
        pyplot.savefig(self.etg.abs_images_dir + self.etg.name.replace(':', '').replace(' ', '') + "_circos.png", bbox_inches="tight", dpi=300)
        pyplot.close()

        image = Image.open(self.etg.abs_images_dir + self.etg.name.replace(':', '').replace(' ', '') + "_circos.png")
        w,h = image.size
        new_w = int(self.etg.new_h * w/h)
        image.close()

        return( self.etg.rel_images_dir + self.etg.name.replace(':', '').replace(' ', '') + "_circos.png" , new_w)
        

class heatmapDrawer:
    def __init__ (self, etg, trim_terms=True):
        self.etg = etg
        self.trim_terms = trim_terms
        self.trimmed_term_mapping_dict = self.__build_trimmed_term_mapping_dict()
        
    def __get_lordered_gene_exp_heatmap_fm_subset_df(self, s_cols, cluster_genes):
        
        heatmap_df = self.etg.gene_exp_heatmap_df.loc[:, s_cols]
        heatmap_fm_df = self.etg.gene_exp_heatmap_fm_df.loc[:, s_cols]
        
        
        if(len(cluster_genes) > 1):
            Z = linkage(heatmap_df.values.T, 'ward', optimal_ordering=True)# MIGHT NEED TO REMOVE optimal_ordering=True
            dn = dendrogram(Z, no_plot=True)
            heatmap_fm_df = heatmap_fm_df.reindex(columns=[cluster_genes[gi] for gi in dn['leaves']])
            return (heatmap_fm_df, Z, dn['leaves'])
        else:
            return (heatmap_fm_df, [[]], [0])
        
    
    def __build_trimmed_term_mapping_dict(self):
        if(self.trim_terms):
            trimmed_terms = [trim_term(term) for term in self.etg.terms]
            annotated_trimmed_terms = annotate_trimmed_terms(trimmed_terms)
            return dict(zip(self.etg.terms,annotated_trimmed_terms))
        else:
            return dict(zip(self.etg.terms,self.etg.terms))
        
    def __add_extra_annotations(self, gene_term_heatmap_df):
        if(self.etg.num_extra_annotations == 0):
            return gene_term_heatmap_df
        else:
            extra_annotation_df = pd.DataFrame()
            for annotation in self.etg.extra_annotations_dict.keys():
                #extra_annotation_df = extra_annotation_df.append(pd.DataFrame([[0.5 if a in self.etg.extra_annotations_dict[annotation] else np.nan for a in list(gene_term_heatmap_df.columns)]], columns = list(gene_term_heatmap_df.columns), index = [annotation]))
                extra_annotation_df =  pd.concat([extra_annotation_df, 
                                                  pd.DataFrame([[0.5 if a in self.etg.extra_annotations_dict[annotation] else np.nan for a in list(gene_term_heatmap_df.columns)]], columns = list(gene_term_heatmap_df.columns), index = [annotation])], 
                                                 ignore_index=False)

            #return extra_annotation_df.append(gene_term_heatmap_df)
            return pd.concat([extra_annotation_df, gene_term_heatmap_df], ignore_index=False)
        
        
    def draw_heatmaps(self, ylabel1='Term', ylabel2='FEA', postfix=''):
        
        #NOTE: The 'fm' in heatmap_fm stands for 'for masking'
        
        (s_rows, s_cols) = self.etg.rows_cols
        cluster_genes = [self.etg.genes_sorted[i] for i in range(len(self.etg.genes_sorted)) if s_cols.iloc[i]]
        cluster_genes_indices = [i for i in range(len(self.etg.genes_sorted)) if s_cols.iloc[i]]
        
        (gene_exp_heatmap_fm_subset_df, Z, leaves) = self.__get_lordered_gene_exp_heatmap_fm_subset_df(s_cols, cluster_genes)
        gene_term_heatmap_fm_subset_df = self.etg.gene_term_heatmap_fm_df.iloc[s_rows].loc[:, s_cols]
        
        gene_term_heatmap_fm_subset_df = gene_term_heatmap_fm_subset_df.reindex(columns = [cluster_genes[gi] for gi in leaves])
        gene_term_heatmap_fm_subset_df.rename(index=self.trimmed_term_mapping_dict, inplace=True)
        gene_term_heatmap_fm_subset_df = self.__add_extra_annotations(gene_term_heatmap_fm_subset_df)
        
        #print(gene_term_heatmap_fm_subset_df)
        
        gene_term_mask = gene_term_heatmap_fm_subset_df.isnull()
        
        #print(gene_term_mask)
        gene_exp_mask = gene_exp_heatmap_fm_subset_df.isnull()
        
        
        (rows_t, cols_g) = gene_term_heatmap_fm_subset_df.values.shape
        (rows_e, _) = gene_exp_heatmap_fm_subset_df.values.shape
        
        fig_width = max((cols_g * 0.6) + 4, self.etg.heatmap_width_min) * 2
        fig_height = max(((rows_t + rows_e) * 0.5) + 4, self.etg.heatmap_height_min) * 1.5 * 2 
        # fig_height = max(((rows_t + rows_e) * 0.3) + 4, self.etg.heatmap_height_min) * 1.5 * 2
    
        with sns.axes_style("dark" , {'axes.facecolor': '#686868'}):
            fig, (ax1, ax2, ax3) = pyplot.subplots(nrows=3, figsize=(fig_width, fig_height))

        with sns.axes_style("dark" , {'axes.facecolor': '#686868'}):
            sns.heatmap(gene_term_heatmap_fm_subset_df, xticklabels=True, yticklabels=True, linewidth=1, 
                            mask=gene_term_mask, cmap="spring", ax=ax1, cbar=False, vmin=0, vmax=1)


        with sns.axes_style("dark" , {'axes.facecolor': '#686868'}):
            sns.heatmap(gene_exp_heatmap_fm_subset_df, xticklabels=True, yticklabels=True,
                        linewidth=1, mask=gene_exp_mask, center=0, cmap="RdBu_r" , vmin = self.etg.heatmap_min , vmax = self.etg.heatmap_max,
                        ax=ax2, cbar=False ,zorder=10)
        
        #dn = dendrogram(Z, color_threshold = 0 , orientation = 'bottom' , no_labels = True , link_color_func=lambda k: 'white')
        if(len(cluster_genes) > 1):
            dendrogram(Z, color_threshold=0, orientation='bottom', no_labels=True)
        ax3.set_facecolor('None')
        ax3.get_xaxis().set_ticks([])
        ax3.get_yaxis().set_ticks([])
        
        cbar = fig.colorbar(ax2.collections[0], ax=ax3, location="bottom", use_gridspec=False, pad=0.5)
        cbar.ax.tick_params(labelsize=40)
        cbar.set_label(self.etg.quant_data_type, size=40)
        
        ax1.set_xlabel('')
        ax1.set_ylabel(ylabel1, fontsize=30)
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right', va='top', fontsize=40)
        ax1.set_yticklabels(ax1.get_yticklabels(), rotation=0, fontsize = 30)

        ax2.set_xlabel('')
        ax2.set_ylabel(ylabel2, fontsize=30)
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right', va='top', fontsize=40)
        ax2.set_yticklabels(ax2.get_yticklabels(), rotation=0, fontsize=30)

        pyplot.subplots_adjust(hspace=0.7)
        pyplot.savefig(self.etg.abs_images_dir + self.etg.name.replace(':', '').replace(' ', '') + "__A_heatmap_" + postfix + ".png", bbox_inches="tight")
        pyplot.close()
        
        image = Image.open(self.etg.abs_images_dir + self.etg.name.replace(':', '').replace(' ', '') + "__A_heatmap_" + postfix + ".png")
        w,h = image.size
        new_w_A = int(self.etg.new_h * w/h)
        image.close()

        
        #******************************************************************
        
        gene_term_heatmap_fm_subset_df = self.etg.gene_term_heatmap_fm_df.iloc[s_rows].loc[:, s_cols]    
        
        gene_counts = gene_term_heatmap_fm_subset_df.sum().values
        
        gene_term_heatmap_fm_subset_df_COPY = gene_term_heatmap_fm_subset_df.copy()
        for exponent in range(rows_t - self.etg.num_extra_annotations):
            gene_term_heatmap_fm_subset_df_COPY.iloc[exponent] = gene_term_heatmap_fm_subset_df.iloc[exponent] * (2**exponent)
        gene_binary_sums = gene_term_heatmap_fm_subset_df_COPY.sum().values
        
        gene_counts = gene_term_heatmap_fm_subset_df.sum().values # Why is this line repeated?
        
        ordered_cluster_genes = []
        for (gc, gbs) in list(OrderedDict.fromkeys(sorted(list(zip(gene_counts, gene_binary_sums)), key=lambda x: (-x[0], -x[1])))):
            
            subset_cluster_genes = [gene for (gene, count, binary_sum) in list(zip(cluster_genes, gene_counts, gene_binary_sums)) if (count==gc and binary_sum==gbs)]
            subset_cluster_gene_indices = [gene_index for (gene_index, count, binary_sum) in list(zip(cluster_genes_indices, gene_counts, gene_binary_sums)) if (count==gc and binary_sum==gbs)]
            subset_cluster_gene_cols = [(i in subset_cluster_gene_indices) for i in range(len(s_cols))]

            if(len(subset_cluster_genes) > 1):
                (_, _, subset_leaves) = self.__get_lordered_gene_exp_heatmap_fm_subset_df(subset_cluster_gene_cols, subset_cluster_genes)
            else:
                subset_leaves = [0]
            
            ordered_cluster_genes = ordered_cluster_genes + [subset_cluster_genes[gi] for gi in subset_leaves]
        
        gene_term_heatmap_fm_subset_df = gene_term_heatmap_fm_subset_df.reindex(columns=ordered_cluster_genes)
        
        gene_term_heatmap_fm_subset_df.rename(index=self.trimmed_term_mapping_dict, inplace=True)
        
        gene_term_heatmap_fm_subset_df = self.__add_extra_annotations(gene_term_heatmap_fm_subset_df)
        
        gene_exp_heatmap_fm_subset_df = self.etg.gene_exp_heatmap_fm_df.loc[:, s_cols]
        gene_exp_heatmap_fm_subset_df = gene_exp_heatmap_fm_subset_df.reindex(columns=ordered_cluster_genes)
        
        gene_term_mask = gene_term_heatmap_fm_subset_df.isnull()
        gene_exp_mask = gene_exp_heatmap_fm_subset_df.isnull()
    
        with sns.axes_style("dark", {'axes.facecolor': '#686868'}):
            fig, (ax1, ax2, ax3) = pyplot.subplots(nrows=3, figsize=(fig_width, fig_height))

        with sns.axes_style("dark" , {'axes.facecolor': '#686868'}):
            sns.heatmap(gene_term_heatmap_fm_subset_df, xticklabels=True, yticklabels=True, linewidth=1, 
                            mask=gene_term_mask, cmap="spring", ax=ax1, cbar=False, vmin=0, vmax = 1)

        with sns.axes_style("dark" , {'axes.facecolor': '#686868'}):
            sns.heatmap(gene_exp_heatmap_fm_subset_df, xticklabels=True, yticklabels=True,
                        linewidth=1, mask=gene_exp_mask, center=0, cmap="RdBu_r", vmin=self.etg.heatmap_min, vmax=self.etg.heatmap_max,
                        ax=ax2, cbar=False, zorder=10)
        
        if(len(cluster_genes) > 1):
            dendrogram(Z, color_threshold=0, orientation='bottom', no_labels=True, link_color_func=lambda k: 'white')
            
        ax3.set_facecolor('None')
        ax3.get_xaxis().set_ticks([])
        ax3.get_yaxis().set_ticks([])
        
        cbar = fig.colorbar(ax2.collections[0], ax=ax3, location="bottom", use_gridspec=False, pad=0.5)
        cbar.ax.tick_params(labelsize=40)
        cbar.set_label(self.etg.quant_data_type, size=40)
        
        ax1.set_xlabel('')
        ax1.set_ylabel(ylabel1, fontsize=30)
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right', va='top', fontsize=40)
        ax1.set_yticklabels(ax1.get_yticklabels(), rotation=0, fontsize=30)

        ax2.set_xlabel('')
        ax2.set_ylabel(ylabel2, fontsize=30)
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right', va='top', fontsize=40)
        ax2.set_yticklabels(ax2.get_yticklabels(), rotation=0, fontsize=30)

        pyplot.subplots_adjust(hspace=0.7)
        
        pyplot.savefig(self.etg.abs_images_dir + self.etg.name.replace(':', '').replace(' ', '') + "__B_heatmap_" + postfix + ".png", bbox_inches="tight")
        pyplot.close()

        image = Image.open(self.etg.abs_images_dir + self.etg.name.replace(':', '').replace(' ', '') + "__B_heatmap_" + postfix + ".png")
        w,h = image.size
        new_w_B = int(self.etg.new_h * w/h)
        image.close()
        
        #******************************************************************
        
        gene_term_heatmap_fm_subset_df = self.etg.gene_term_heatmap_fm_df.iloc[s_rows].loc[:, s_cols]
        
        ordered_cluster_genes = sorted(cluster_genes)
        gene_term_heatmap_fm_subset_df = gene_term_heatmap_fm_subset_df.reindex(columns=ordered_cluster_genes)
        gene_term_heatmap_fm_subset_df.rename( index = self.trimmed_term_mapping_dict , inplace = True )
        gene_term_heatmap_fm_subset_df = self.__add_extra_annotations(gene_term_heatmap_fm_subset_df)
        
        gene_exp_heatmap_fm_subset_df = self.etg.gene_exp_heatmap_fm_df.loc[:, s_cols]
        gene_exp_heatmap_fm_subset_df = gene_exp_heatmap_fm_subset_df.reindex(columns=ordered_cluster_genes)
                
        gene_term_mask = gene_term_heatmap_fm_subset_df.isnull()
        gene_exp_mask = gene_exp_heatmap_fm_subset_df.isnull()
    
        with sns.axes_style("dark" , {'axes.facecolor': '#686868'}):
            fig, (ax1, ax2, ax3) = pyplot.subplots(nrows=3, figsize=(fig_width, fig_height))

        with sns.axes_style("dark" , {'axes.facecolor': '#686868'}):
            sns.heatmap(gene_term_heatmap_fm_subset_df, xticklabels=True, yticklabels=True, linewidth=1, 
                            mask=gene_term_mask, cmap="spring", ax=ax1, cbar=False, vmin=0, vmax = 1)

        with sns.axes_style("dark" , {'axes.facecolor': '#686868'}):
            sns.heatmap(gene_exp_heatmap_fm_subset_df, xticklabels=True, yticklabels=True,
                        linewidth=1, mask=gene_exp_mask, center=0, cmap="RdBu_r", vmin=self.etg.heatmap_min, vmax=self.etg.heatmap_max,
                        ax=ax2, cbar=False, zorder=10)
        
        if(len(cluster_genes) > 1):
            dendrogram(Z, color_threshold=0, orientation='bottom', no_labels=True, link_color_func=lambda k: 'white')
        
        ax3.set_facecolor('None')
        ax3.get_xaxis().set_ticks([])
        ax3.get_yaxis().set_ticks([])
        
        cbar = fig.colorbar(ax2.collections[0], ax=ax3, location="bottom", use_gridspec=False, pad=0.5)
        cbar.ax.tick_params(labelsize=40)
        cbar.set_label(self.etg.quant_data_type, size=40)
        
        ax1.set_xlabel('')
        ax1.set_ylabel(ylabel1, fontsize=30)
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45,  ha='right', va='top', fontsize=40)
        ax1.set_yticklabels(ax1.get_yticklabels(), rotation=0, fontsize=30)

        ax2.set_xlabel('')
        ax2.set_ylabel(ylabel2, fontsize=30)
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right', va='top', fontsize=40)
        ax2.set_yticklabels(ax2.get_yticklabels(), rotation=0, fontsize=30)

        pyplot.subplots_adjust(hspace=0.7)
        
        pyplot.savefig(self.etg.abs_images_dir + self.etg.name.replace(':', '').replace(' ', '') + "__C_heatmap_" + postfix + ".png", bbox_inches="tight")
        pyplot.close()
        image = Image.open(self.etg.abs_images_dir + self.etg.name.replace(':', '').replace(' ', '') + "__C_heatmap_" + postfix + ".png")
        w,h = image.size
        new_w_C = int(self.etg.new_h * w/h)
        image.close()

        if(postfix==''):
            heatmap_titles = ["Heatmap A of " + self.etg.name, "Heatmap B of " + self.etg.name, "Heatmap C of " + self.etg.name]
        else:
            heatmap_titles = ["Heatmap A of " + self.etg.name + " ("+ postfix +")", "Heatmap B of " + self.etg.name + " ("+ postfix +")", "Heatmap C of " + self.etg.name + " ("+ postfix +")"]
            
        return( [self.etg.rel_images_dir + self.etg.name.replace(':', '').replace(' ', '') + "__A_heatmap_" + postfix + ".png" , 
                 self.etg.rel_images_dir + self.etg.name.replace(':', '').replace(' ', '') + "__B_heatmap_" + postfix + ".png",
                 self.etg.rel_images_dir + self.etg.name.replace(':', '').replace(' ', '') + "__C_heatmap_" + postfix + ".png"] , 
                [new_w_A, new_w_B, new_w_C], heatmap_titles)

class dotplotDrawer:
    def __init__ (self, community):
        self.community = community
        self.type_label = ', '.join(self.community.type_label.split(' ')) + ' term'
    
    
    def __build_dotplot_df(self, exp_id):
        trimmed_terms = [trim_term(term) for term in self.community.terms]
        annotated_trimmed_terms = annotate_trimmed_terms(trimmed_terms)
        dotplot_data = []
        for (term, annotated_trimmed_term) in zip(self.community.terms, annotated_trimmed_terms):
            dotplot_data.append([annotated_trimmed_term] + self.community.all_term_dotplot_dict[(exp_id, term)][0 : 3])
        
        dotplot_df = pd.DataFrame(dotplot_data, columns=[self.type_label, 'gene ratio', '-log10(p-adj)', 'count']) 
        dotplot_df.sort_values(by='gene ratio', inplace=True)
        
        return dotplot_df
    
    def __get_zero_entry_status(self, legend):
        
        t_index = 0
        t = legend.texts[t_index]
        in_counts_section = t.get_text() == 'count'
        
        while(not in_counts_section):
            t_index += 1
            t = legend.texts[t_index]
            in_counts_section = t.get_text() == 'count'
                
        zero_entry = False
        
        for t in legend.texts[t_index+1 : len(legend.texts)]:
            try:
                entry = float(t.get_text())
                zero_entry = zero_entry or entry == 0
            except ValueError:
                pass
 
        return zero_entry
    
    
    def draw_dotplot(self, exp_id, w_min=5, h_min=4):
        dotplot_df = self.__build_dotplot_df(exp_id)
        cmap = sns.light_palette("purple", as_cmap=True)
        
        min_count = min(dotplot_df['count'])
        max_count = max(dotplot_df['count'])
        
        fig_width = max((len(self.community.terms) * 0.5) + 2, w_min)
        fig_height = max(fig_width / 3, h_min)
        
        pyplot.figure(figsize=(fig_width, fig_height))
                
        if((len(self.community.terms)<=4) or min_count==max_count):
            g = sns.scatterplot(x=self.type_label, y="gene ratio", hue="-log10(p-adj)", size="count", palette=cmap,
                                 size_norm = (min_count, max_count),
                                 sizes = (200 * (min_count/max_count), 200), data=dotplot_df, legend='full')        
        else:
            g = sns.scatterplot(x=self.type_label, y="gene ratio", hue="-log10(p-adj)", size="count", palette=cmap,
                            size_norm = (min_count, max_count) , 
                            sizes = (200 * (min_count/max_count), 200), data=dotplot_df, legend='brief')
            
            zero_entry_exists = self.__get_zero_entry_status( g.axes.legend_ )
            
            while(zero_entry_exists):
                min_count = min_count + 1
                max_count = max(min_count, max_count)
                pyplot.close()
            
                pyplot.figure(figsize=(fig_width, fig_height))
                g = sns.scatterplot(x=self.type_label, y="gene ratio", hue="-log10(p-adj)", size="count", palette=cmap,
                            size_norm=(min_count, max_count), 
                            sizes=(200 * (min_count/max_count), 200), data=dotplot_df, legend='brief')
                
                zero_entry_exists = self.__get_zero_entry_status(g.axes.legend_)
        
        leg = g.axes.legend_
        
        for t in leg.texts:
            try:
                entry = float(t.get_text())
                if(entry == int(entry)):
                    t.set_text(str(int(entry)))
                else:
                    t.set_text(str(round(entry, 1)))
            except ValueError:
                pass    
       
        h,l = g.get_legend_handles_labels()
        g.get_legend().remove()
        
        count_index = l.index('count')
        pyplot.legend(h[count_index : len(l)], l[count_index : len(l)], bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
        pyplot.xticks(rotation=45, ha='right', va='top')
                        
        axins = inset_axes(g,
                   width="5%",  # width = 5% of parent_bbox width
                   height="50%",
                   loc='lower left',
                   bbox_to_anchor=(1.3, 0.5, 1, 1),
                   bbox_transform=g.transAxes,
                   borderpad=0,
                   )
        
        if(dotplot_df['-log10(p-adj)'].min() == dotplot_df['-log10(p-adj)'].max()):
            norm = pyplot.Normalize(dotplot_df['-log10(p-adj)'].min(), dotplot_df['-log10(p-adj)'].min() + 1)
        else:
            norm = pyplot.Normalize(dotplot_df['-log10(p-adj)'].min(), dotplot_df['-log10(p-adj)'].max())
        sm = pyplot.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar = g.figure.colorbar(sm, cax=axins)
        cbar.set_label('-log10(p-adj)')
        
        if(not(exp_id)):
            pyplot.savefig(self.community.abs_images_dir + self.community.name.replace(':', '').replace(' ', '') + "_dotplot.png", bbox_inches="tight", dpi=120)
            pyplot.close()
            
            image = Image.open(self.community.abs_images_dir + self.community.name.replace(':', '').replace(' ', '') + "_dotplot.png")
            w,h = image.size
            new_w = int(self.community.new_h * w/h)
            image.close()
            
            return (self.community.rel_images_dir + self.community.name.replace(':', '').replace(' ', '') + "_dotplot.png", new_w)
        
        else:
            pyplot.savefig(self.community.abs_images_dir + self.community.name.replace(':', '').replace(' ', '') + "_" + exp_id + "_dotplot.png", bbox_inches="tight", dpi=120)
            pyplot.close()
            
            image = Image.open(self.community.abs_images_dir + self.community.name.replace(':', '').replace(' ', '') + "_" + exp_id + "_dotplot.png")
            w,h = image.size
            new_w = int(self.community.new_h * w/h)
            image.close()
            
            return (self.community.rel_images_dir + self.community.name.replace(':', '').replace(' ', '') + "_" + exp_id  + "_dotplot.png", new_w)
        

class go_statsGetter:
    
    def __init__(self, id2obj, id2nt):
        self.id2obj = id2obj  # Contains children (and parents)
        self.id2nt = id2nt    # Contains fields for printing (optional)
        self.terms_seen = set()
        
    def get_go_stats(self, term, stats_collector, depth=1):
        if term in self.terms_seen:
            return
        
        obj = self.id2obj[term]
        ntprt = self.id2nt[term]
        dct = ntprt._asdict()
        stats_collector[dct['id']] = (dct['dcnt'], dct['level'])
        self.terms_seen.add(term)
        
        depth += 1
        for child in obj.children:
            self.get_go_stats(child.item_id, stats_collector, depth)

        
class go_hierarchyDrawer:
    def __init__ (self, community):
        self.community = community
        
    def draw_hierarchy(self):
        
        godag_plot.plot_gos(self.community.abs_images_dir + self.community.name.replace(':', '').replace(' ', '') + "_hierarchy.png",
                            self.community.go_terms, self.community.go_dag, title="", dpi=300)
        
        pyplot.close()
        
        image = Image.open(self.community.abs_images_dir + self.community.name.replace(':', '').replace(' ', '') + "_hierarchy.png")
        w,h = image.size
        new_w = (self.community.new_h * w/h)
        image.close()
        
        return (self.community.rel_images_dir + self.community.name.replace(':', '').replace(' ', '') + "_hierarchy.png", new_w)

# Community printer classes

# CSV printer        
class communityCsvPrinter():
    def __init__(self, community):
        self.community = community
    
    def print_csv(self, csv_f):
        expanded_info_df = self.community.etg_df.copy()
        expanded_info_df['Community'] = self.community.name
        expanded_info_df['Meta-community'] = self.community.meta_community_name
        expanded_info_df.to_csv(csv_f, columns=['Community', 'Meta-community', 'FEA', 'Term', 'Gene', 'QD'], index=False, header=False)
        
class singletonCommunityCsvPrinter():
    def __init__(self, singletonCommunity):
        self.singletonCommunity = singletonCommunity
    
    def print_csv(self, csv_f):
        self.singletonCommunity.singleton_etg_df.to_csv(csv_f, columns=['Community', 'Meta-community', 'FEA', 'Term', 'Gene', 'QD'], index=False, header=False)


# HTML printers
class bigBasicCommunityPrinter():
    def __init__ (self, community):
        self.community = community
    
    def _print_html_title(self, html_f, summary_html, first_print, backlink='' ):
        
        if(first_print):
            html_f.write('<div style="height:110px" id="' + self.community.name +'"></div>')
        else:
            html_f.write('<div style="height:100px" id="' + self.community.name +'"></div>')
            html_f.write('<hr>\n')
            
        html_f.write('<button type="button" class="collapsible"><table>\n')
        html_f.write('<tr><td></td></tr>\n')
        html_f.write('<tr>\n')
        
        if(self.community.meta_community_name):
            #html_f.write('<td><h5 class="title">' + self.community.name + ' ' + self.community.info_string + '   *** ' + self.community.meta_community_name + ' ***</h5></td>\n')
            html_f.write('<td><h5 class="title">' + self.community.name + ' // Member of ' + self.community.meta_community_name + '</h5></td>\n')
        else:
            #html_f.write('<td><h5 class="title">' + self.community.name + ' ' + self.community.info_string + '</h5></td>\n')
            html_f.write('<td><h5 class="title">' + self.community.name + '</h5></td>\n')
        
        #html_f.write('<td><button class="view-button" style="font-size:small;" onclick="document.location=\'' + summary_html + '\'">Communities summary</button></td>\n')
        
        #if( backlink ):
        #    html_f.write('<td><button class="view-button" style="font-size:small;" onclick="document.location=\'' + backlink + '\'">Main page</button></td>\n')
        
        html_f.write('</tr>\n')
        html_f.write('</table></button>\n')
    
    def _print_html_griditem1(self, html_f):
        html_f.write('<div class="terms">\n')
        html_f.write('<table style="font-size:small;white-space: nowrap;">\n')
        
        html_f.write('<tr>\n')
        html_f.write('<td>\n')
        html_f.write('<b>Member terms: </b>\n')
        html_f.write('</td>\n')
        html_f.write('<td>\n')
        html_f.write('</td>\n')
        html_f.write('</tr>\n')
        
        html_f.write('<tr>\n')
        html_f.write('<td>\n')
        html_f.write('</td>\n')
        html_f.write('<td>\n')
        html_f.write('</td>\n')
        html_f.write('</tr>\n')
        
        for term in self.community.terms:
            html_f.write('<tr>\n')
            html_f.write('<td>\n')
            html_f.write(term)
            if(term == self.community.top_term_id):
                html_f.write('<sup>*</sup>')
            html_f.write('</td>\n')
            html_f.write('<td>\n')
            html_f.write(self.community.all_term_defs_dict[term] + '\n') 
            html_f.write('</td>\n')
            html_f.write('</tr>\n')
    
        html_f.write('</table>\n')
        
        html_f.write('</div>\n')
        
        html_f.write('<div class="spacer">\n')
        html_f.write('</div>\n')
        
    def _print_html_griditem2(self, html_f):
        html_f.write('<div class="plotbox">\n')
        html_f.write('<div style="width: 1200px;">\n')
        html_f.write('<table><tr><td style="font-weight: bold;" id="' + self.community.name + '_plotbox_title">Circos plot</td></tr></table>\n')
        html_f.write('<img id="' + self.community.name + '_plotbox" src="' + self.community.circos_img_path + '" width="' + str(self.community.circos_img_width) + '" height="' + str(self.community.new_h) + '">\n')
        
        #html_f.write('<table><tr><td style="font-weight: bold;" id="' + self.community.name + '_plotbox_title">UpSet plot</td></tr></table>\n')
        #html_f.write('<img id="' + self.community.name + '_plotbox" src="' + self.community.upset_img_path + '" width="' + str(self.community.upset_img_width) + '" height="' + str(self.community.new_h) + '">\n')
        
        
        html_f.write('<div style="display:none;height:' + str(self.community.new_h + 3) + 'px;padding:0px;border:0px;margin:0px;" id="' +  self.community.name + '_plotbox_table_0">\n')
        html_f.write('<table style="font-size:small;white-space: nowrap;">\n')
        html_f.write('<tr>\n')
        html_f.write('<td>\n')
        html_f.write('<b>Gene</b>\n')
        html_f.write('</td>\n')
        html_f.write('<td>\n')
        html_f.write('<b>NCBI: Gene database</b>\n')
        html_f.write('</td>\n')
        html_f.write('<td>\n')
        html_f.write('<b>NCBI: PubMed database (Gene only)</b>\n')
        html_f.write('</td>\n')
        
        if(len(self.community.search_words) > 0):
            html_f.write('<td>\n')
            html_f.write('<b>NCBI: PubMed database (Gene and keywords)</b>\n')
            html_f.write('</td>\n')
        
        html_f.write('</tr>\n')
        
        for inc_gene in self.community.included_genes:
            (ncbi_gene_href, pubmed_gene_href, pubmed_search_href, pubmed_print_string) = build_searches(inc_gene, self.community.search_words)
            html_f.write('<tr>\n')
            
            html_f.write('<td>\n')
            html_f.write(inc_gene + '\n') 
            html_f.write('</td>\n')
            
            html_f.write('<td>\n')
            html_f.write('<a href = "' + ncbi_gene_href + '" target="_blank">' + inc_gene + ' (NCBI: Gene)</a>\n') 
            html_f.write('</td>\n')
            
#            html_f.write('<td>\n')
#            html_f.write('<a href = "' + ensembl_gene_href + '" target="_blank">' + inc_gene + ' (ENSEMBL)</a>\n') 
#            html_f.write('</td>\n')
            
            html_f.write('<td>\n')
            html_f.write('<a href = "' + pubmed_gene_href + '" target="_blank">' + inc_gene + ' (NCBI: PubMed)</a>\n') 
            html_f.write('</td>\n')
            
            if(len(self.community.search_words) > 0):
                html_f.write('<td>\n')
                html_f.write('<a href = "' + pubmed_search_href + '" target="_blank">' + pubmed_print_string + ' (NCBI: PubMed)</a>\n') 
                html_f.write('</td>\n')
            
            html_f.write('</tr>\n')
        
        html_f.write('</table>\n')
        html_f.write('<div style="height:2500px;"></div>\n')
        html_f.write('</div>\n')
        html_f.write('</div>\n')
        html_f.write('</div>\n')
        
        html_f.write('<div class="plot_buttons">\n')
        
        
        html_f.write('<button class="view-button"  onclick="changeImg( \'' + self.community.name + '\' , \'plotbox\' , \'' + self.community.circos_img_path + '\' ,' + str(self.community.new_h) + ',\'' + str(self.community.circos_img_width) + '\' ,\'Circos plot\',1)">Circos plot</button>\n')
        
        html_f.write('<button class="view-button"  onclick="changeImg( \'' + self.community.name + '\' , \'plotbox\' , \'' + self.community.upset_img_path + '\' ,' + str(self.community.new_h) + ',\'' + str(self.community.upset_img_width) + '\' ,\'UpSet plot\',1)">UpSet plot</button>\n')
        
        
        
        
        #heatmap_img_paths_array_as_str = ','.join(self.community.heatmap_img_paths_list)
        #heatmap_widths_array_as_str = ','.join(map(str, self.community.heatmap_img_widths_list))
        #heatmap_img_titles_array_as_str = ','.join(self.community.heatmap_img_titles_list)
                        
        #html_f.write('<button class="view-button"  onclick="changeImg( \'' + self.community.name + '\' , \'plotbox\'  , \'' + heatmap_img_paths_array_as_str + '\' ,' + str(self.community.new_h) + ',\'' + heatmap_widths_array_as_str + '\',\'' + heatmap_img_titles_array_as_str + '\',1)">Heatmaps</button>\n')
        
        
        if(len(self.community.heatmap_img_paths_list) == 3):
            html_f.write('<button class="view-button"  onclick="changeImg( \'' + self.community.name + '\' , \'plotbox\' , \'' + self.community.heatmap_img_paths_list[0] + '\' ,' + str(self.community.new_h) + ',\'' + str(self.community.heatmap_img_widths_list[0]) + '\' ,\'' + self.community.heatmap_img_titles_list[0] + '\',1)">Heatmap A (' + self.community.quant_data_type +')</button>\n')
            html_f.write('<button class="view-button"  onclick="changeImg( \'' + self.community.name + '\' , \'plotbox\' , \'' + self.community.heatmap_img_paths_list[1] + '\' ,' + str(self.community.new_h) + ',\'' + str(self.community.heatmap_img_widths_list[1]) + '\' ,\'' + self.community.heatmap_img_titles_list[1] + '\',1)">Heatmap B (annotations x ' + self.community.quant_data_type +')</button>\n')
            html_f.write('<button class="view-button"  onclick="changeImg( \'' + self.community.name + '\' , \'plotbox\' , \'' + self.community.heatmap_img_paths_list[2] + '\' ,' + str(self.community.new_h) + ',\'' + str(self.community.heatmap_img_widths_list[2]) + '\' ,\'' + self.community.heatmap_img_titles_list[2] + '\',1)">Heatmap C (alphabetical)</button>\n')
        else:
            heatmap_img_paths_array_as_str_A = ','.join( [self.community.heatmap_img_paths_list[x] for x in [0,3]] )
            heatmap_widths_array_as_str_A = ','.join( map( str , [self.community.heatmap_img_widths_list[x] for x in [0,3]] ) )
            heatmap_img_titles_array_as_str_A = ','.join( [self.community.heatmap_img_titles_list[x] for x in [0,3]] )
            
            heatmap_img_paths_array_as_str_B = ','.join( [self.community.heatmap_img_paths_list[x] for x in [1,4]] )
            heatmap_widths_array_as_str_B = ','.join( map( str , [self.community.heatmap_img_widths_list[x] for x in [1,4]] ) )
            heatmap_img_titles_array_as_str_B = ','.join( [self.community.heatmap_img_titles_list[x] for x in [1,4]] )
            
            heatmap_img_paths_array_as_str_C = ','.join( [self.community.heatmap_img_paths_list[x] for x in [2,5]] )
            heatmap_widths_array_as_str_C = ','.join( map( str , [self.community.heatmap_img_widths_list[x] for x in [2,5]] ) )
            heatmap_img_titles_array_as_str_C = ','.join( [self.community.heatmap_img_titles_list[x] for x in [2,5]] )
            
            html_f.write( '<button class="view-button"  onclick="changeImg( \'' + self.community.name + '\' , \'plotbox\' , \'' + heatmap_img_paths_array_as_str_A + '\' ,' + str( self.community.new_h ) + ',\'' + heatmap_widths_array_as_str_A + '\',\'' + heatmap_img_titles_array_as_str_A + '\',1)">Heatmap A (' + self.community.quant_data_type +')</button>\n' )
            html_f.write( '<button class="view-button"  onclick="changeImg( \'' + self.community.name + '\' , \'plotbox\' , \'' + heatmap_img_paths_array_as_str_B + '\' ,' + str( self.community.new_h ) + ',\'' + heatmap_widths_array_as_str_B + '\',\'' + heatmap_img_titles_array_as_str_B + '\',1)">Heatmap B (annotations x ' + self.community.quant_data_type +')</button>\n' )
            html_f.write( '<button class="view-button"  onclick="changeImg( \'' + self.community.name + '\' , \'plotbox\' , \'' + heatmap_img_paths_array_as_str_C + '\' ,' + str( self.community.new_h ) + ',\'' + heatmap_widths_array_as_str_C + '\',\'' + heatmap_img_titles_array_as_str_C + '\',1)">Heatmap C (alphabetical)</button>\n' )
        
        
        
        
        if(self.community.all_term_dotplot_dict):
            dotplot_img_paths_array_as_str = ','.join(self.community.dotplot_img_paths_list)
            dotplot_widths_array_as_str = ','.join(map(str, self.community.dotplot_img_widths_list))
            dotplot_img_titles_array_as_str = ','.join(self.community.dotplot_img_titles_list)
        
            if(len(self.community.exp_ids) == 1):
                html_f.write('<button class="view-button"  onclick="changeImg( \'' + self.community.name + '\' , \'plotbox\' , \'' + dotplot_img_paths_array_as_str + '\' ,' + str(self.community.new_h) + ',\'' + dotplot_widths_array_as_str + '\',\'' + dotplot_img_titles_array_as_str + '\',1)">Dot plot</button>\n')
            else:
                html_f.write('<button class="view-button"  onclick="changeImg( \'' + self.community.name + '\' , \'plotbox\' , \'' + dotplot_img_paths_array_as_str + '\' ,' + str(self.community.new_h) + ',\'' + dotplot_widths_array_as_str + '\',\'' + dotplot_img_titles_array_as_str + '\',1)">Dot plots</button>\n')

        
        html_f.write('<button class="view-button"  onclick="changeTable( \'' + self.community.name + '\' , 0 , 1 ,\'plotbox\', true , \'Literature search\')">Literature search</button>\n')
        
        html_f.write('</div>\n')
        
    def _print_html_griditem3(self, html_f):
        html_f.write('<div class="extra">\n') # Empty
        html_f.write('<div style="width: 1200px;">\n')
        html_f.write('</div>\n')
        html_f.write('</div>\n')
        
    def _print_html_griditem4( self , html_f ):
        html_f.write('<div class="meta">\n')  # grid-item 4      
        html_f.write('<table style="font-size:small;white-space: nowrap;">\n')
        
        html_f.write('<tr>\n')
        html_f.write('<td>\n')
        html_f.write('<b>Extra connections: </b>\n')
        html_f.write('</td>\n')
        html_f.write('</tr>\n')
        
        html_f.write('<tr>\n')
        html_f.write('<td>\n')
        html_f.write('</td>\n')
        html_f.write('</tr>\n')
        
        if (not(self.community.meta_community_name) and len(self.community.overlapping_singleton_communities_names) == 0):
            html_f.write('<tr>\n')
            html_f.write('<td>\n')
            html_f.write('<b>None</b>\n')
            html_f.write('</td>\n')
            html_f.write('</tr>\n')
        
        else:
            if (self.community.meta_community_name):
                html_f.write('<tr>\n')
                html_f.write('<td>\n')
                html_f.write('<b>Member of:</b> <a href="#' + self.community.meta_community_name + '">' + self.community.meta_community_name + '</a>\n')
                html_f.write('</td>\n')
                html_f.write('<td>\n')
                html_f.write('</td>\n')
                html_f.write('</tr>\n')
                
                html_f.write('<tr>\n')
                html_f.write('<td>\n')
                html_f.write('</td>\n')
                html_f.write('<td>\n')
                html_f.write('</td>\n')
                html_f.write('</tr>\n')
                
                html_f.write('<tr>\n')
                html_f.write('<td>\n')
                html_f.write('<b>Meta community siblings: </b>\n')
                html_f.write('</td>\n')
                html_f.write('<td>\n')
                html_f.write('</td>\n')
                html_f.write('</tr>\n')
                
                self.community.meta_community_siblings.sort(key=lambda x: x.name)
                for sib in self.community.meta_community_siblings:
                    html_f.write('<tr>\n')
                    html_f.write('<td>\n')
                    html_f.write('<a href="#' + sib.name + '">' + sib.name + '</a>\n')
                    html_f.write('</td>\n')
                    html_f.write('<td>\n')
                    html_f.write(sib.top_term)
                    html_f.write('</td>\n')
                    html_f.write('</tr>\n')

                html_f.write('<tr>\n')
                html_f.write('<td>\n')
                html_f.write('</td>\n')
                html_f.write('</tr>\n')
                
            
            if (len(self.community.overlapping_singleton_communities_names) > 0):
                if (self.community.meta_community_name):
                    html_f.write('</table>\n') 
                    html_f.write('<table style="font-size:small;white-space: nowrap;">\n')
                
                self.community.overlapping_singleton_communities_names.sort()
                html_f.write('<tr>\n')
                html_f.write('<td>\n')
                html_f.write('<b>Other overlapping terms: </b>\n')
                html_f.write('</td>\n')
                html_f.write('<td>\n')
                html_f.write('</td>\n')
                html_f.write('</tr>\n')
                
                sc_names_sorted = [sc for (sc, sc_type) in sorted([(c, self.community.all_term_types_dict[c]) for c in self.community.overlapping_singleton_communities_names], key=lambda x: (x[1], x[0]))]
                
                for term in sc_names_sorted:
                    html_f.write('<tr>\n')
                    html_f.write('<td>\n')
                    if(term == self.community.all_term_defs_dict[term]):
                        html_f.write('<a href="#' + term + '">' + term + '</a>\n')
                    else:
                        html_f.write('<a href="#' + term + '">' + term + ' ' + self.community.all_term_defs_dict[term] + '</a>\n')
                    html_f.write('</td>\n')
                    html_f.write('<td>\n')
                    html_f.write('</td>\n')
                    html_f.write('</tr>\n')
                
                 
        html_f.write('</table>\n')        
        html_f.write('</div>\n')  
    
    
    def print_html (self, html_f, summary_html, first_print, backlink='' ):
        
        self._print_html_title(html_f, summary_html, first_print, backlink)
                
        html_f.write('<div class="grid-container">\n')
        
        self._print_html_griditem1(html_f)
        
        self._print_html_griditem2(html_f)
        
        self._print_html_griditem3(html_f)
        
        self._print_html_griditem4(html_f)
        
        html_f.write('</div>\n')
        #html_f.write('<hr>\n')
        #html_f.write('<br>\n')
        #html_f.write('<br>\n')
        #html_f.write('<br>\n')

class bigOneExtraImgCommunityPrinter(bigBasicCommunityPrinter):
    def __init__ (self, community):
        super().__init__(community)
    
    
    def _print_html_griditem3(self, html_f):
        html_f.write('<div class="extra">\n')# grid-item 3
        html_f.write('<div style="width: 1200px;">\n')
        if ('GO' in self.community.term_types):
            html_f.write('<table><tr><td style="font-weight: bold;">GO hierarchy</td></tr></table>\n')
        else:
            html_f.write('<table><tr><td style="font-weight: bold;" >' + self.community.extra_img_title + '</td></tr></table>\n')
        
        html_f.write('<img src="' + self.community.extra_img_path + '" width="' + str(self.community.extra_img_width) + '" height="' + str(self.community.new_h) + '">\n')
        html_f.write('</div>\n')
        html_f.write('</div>\n')
    
    def print_html (self, html_f, summary_html, first_print, backlink=''):     
        super()._print_html_title(html_f, summary_html, first_print, backlink )
        
        html_f.write('<div class="grid-container">\n')
        
        super()._print_html_griditem1(html_f)
        
        super()._print_html_griditem2(html_f)
        
        self._print_html_griditem3(html_f)
        
        super()._print_html_griditem4(html_f)
        
        html_f.write('</div>\n')
        #html_f.write('<hr>\n')
        #html_f.write('<br>\n')
        #html_f.write('<br>\n')
        #html_f.write('<br>\n')


class bigOneDescTableCommunityPrinter(bigBasicCommunityPrinter):
    def __init__ (self, community):
        super().__init__(community)
    
    def _print_html_griditem3(self, html_f):
        term_desc_table = self.community.msigdb_html_soup.find(id=self.community.terms_with_desc_tables[0])
        term_desc_table_html = term_desc_table.prettify()
        
        html_f.write('<div class="extra">\n')# grid-item 3
        html_f.write('<div style="width: 1200px;">\n')
        html_f.write('<div style="display:block;height:' + str(self.community.new_h + 18) + 'px;padding:0px;border:0px;margin:0px;">\n')
        html_f.write(term_desc_table_html)
        html_f.write('</div>\n')
        html_f.write('</div>\n')
        html_f.write('</div>\n')
    
    def print_html (self, html_f, summary_html, first_print, backlink=''):
        super()._print_html_title(html_f, summary_html, first_print, backlink)
        
        html_f.write('<div class="grid-container">\n')
        
        super()._print_html_griditem1(html_f)
        
        super()._print_html_griditem2(html_f)
        
        self._print_html_griditem3(html_f)
        
        super()._print_html_griditem4(html_f)
        
        html_f.write('</div>\n')
        #html_f.write('<hr>\n')
        #html_f.write('<br>\n')
        #html_f.write('<br>\n')
        #html_f.write('<br>\n')


class bigManyDescTableCommunityPrinter( bigBasicCommunityPrinter ):
    def __init__ (self, community):
        super().__init__(community)
    
    def _print_html_griditem1(self, html_f):
        html_f.write('<div class="terms">\n') 
        html_f.write('<table style="font-size:small;white-space: nowrap;">\n')
        
        html_f.write('<tr>\n')
        html_f.write('<td>\n')
        html_f.write('<b>Member terms: </b>\n')
        html_f.write('</td>\n')
        html_f.write('<td>\n')
        html_f.write('</td>\n')
        html_f.write('<td>\n')
        html_f.write('</td>\n')
        html_f.write('</tr>\n')
        
        html_f.write('<tr>\n')
        html_f.write('<td>\n')
        html_f.write('</td>\n')
        html_f.write('<td>\n')
        html_f.write('</td>\n')
        html_f.write('<td>\n')
        html_f.write('</td>\n')
        html_f.write('</tr>\n')
        
        for term in self.community.terms:
            html_f.write('<tr>\n')
            html_f.write('<td>\n')
            html_f.write(term)
            if(term == self.community.top_term_id):
                html_f.write('<sup>*</sup>')
            html_f.write('</td>\n')
            
            html_f.write('<td>\n')
            
            if term in self.community.terms_with_desc_tables:
                term_i = self.community.terms_with_desc_tables.index(term)
                html_f.write('<button class="view-button"  onclick="changeTable( \'' + self.community.name + '\' , ' + str( term_i ) + ' , ' + str(len(self.community.terms_with_desc_tables)) + ',\'extra\' , false , \'\' )">View</button>\n')
            
            html_f.write('</td>\n')
            
            html_f.write('<td>\n')
            html_f.write(self.community.all_term_defs_dict[term]) 
            html_f.write('</td>\n')
            
            html_f.write('</tr>\n')
    
        html_f.write('</table>\n')
        html_f.write('</div>\n')
        
        html_f.write('<div class="spacer">\n')
        html_f.write('</div>\n')
       
        
    def _print_html_griditem3(self, html_f):
        
        html_f.write('<div class="extra">\n') # grid-item 3
        html_f.write('<div style="width: 1200px;">\n')
        
        for term_i in range(len(self.community.terms_with_desc_tables)):
            term = self.community.terms_with_desc_tables[term_i]
            
            term_desc_table = self.community.msigdb_html_soup.find(id=term)
            term_desc_table_html = term_desc_table.prettify()
            
            if(term == self.community.first_term_to_show):
                html_f.write('<div style="display:block;height:' + str(self.community.new_h + 18) + 'px;padding:0px;border:0px;margin:0px;" id="' +  self.community.name + '_extra_table_' + str(term_i)  + '">\n')
            else:
                html_f.write('<div style="display:none;height:' + str(self.community.new_h + 18) + 'px;padding:0px;border:0px;margin:0px;" id="' +  self.community.name + '_extra_table_' + str(term_i)  + '">\n')
            html_f.write(term_desc_table_html)
            html_f.write('</div>\n')
            
        html_f.write('</div>\n')
        html_f.write('</div>\n')
    
    def print_html (self, html_f, summary_html, first_print, backlink=''):      
        super()._print_html_title(html_f, summary_html, first_print, backlink)
        
        html_f.write('<div class="grid-container">\n')
        
        self._print_html_griditem1(html_f)
        
        super()._print_html_griditem2(html_f)
        
        self._print_html_griditem3(html_f)
        
        super()._print_html_griditem4(html_f)
        
        html_f.write('</div>\n')
        #html_f.write('<hr>\n')
        #html_f.write('<br>\n')
        #html_f.write('<br>\n')
        #html_f.write('<br>\n')

      
class bigManyExtraImgCommunityPrinter(bigBasicCommunityPrinter):
    def __init__ (self, community):
        super().__init__(community)
    
    def _print_html_griditem1(self, html_f):
        html_f.write('<div class="terms">\n') 
        html_f.write('<table style="font-size:small;white-space: nowrap;">\n')
        
        html_f.write('<tr>\n')
        html_f.write('<td>\n')
        html_f.write('<b>Member terms: </b>\n')
        html_f.write('</td>\n')
        html_f.write('<td>\n')
        html_f.write('</td>\n')
        html_f.write('<td>\n')
        html_f.write('</td>\n')
        html_f.write('</tr>\n')
        
        html_f.write('<tr>\n')
        html_f.write('<td>\n')
        html_f.write('</td>\n')
        html_f.write('<td>\n')
        html_f.write('</td>\n')
        html_f.write('<td>\n')
        html_f.write('</td>\n')
        html_f.write('</tr>\n')
        
        community_terms = self.community.terms
        
        if(self.community.go_img_path and len(self.community.go_terms) > 1): #if we have more than one GO term and a corresponding Go term hierarchy...
            community_term_types = [term_type for (term, term_type) in [(t, self.community.all_term_types_dict[t]) for t in self.community.terms]]
            
            last_GO_index = len(community_term_types) - 1 - community_term_types[:: -1].index('GO')
            
            community_terms.insert(last_GO_index + 1, 'GO hierarchy')
        
        for term in community_terms:
            html_f.write('<tr>\n')
            html_f.write('<td>\n')
            
            if(not(term == 'GO hierarchy')):
                html_f.write(term)
                if(term == self.community.top_term_id):
                    html_f.write('<sup>*</sup>')
                html_f.write('</td>\n')
                
                html_f.write('<td>\n')
                
                if term in self.community.term_img_dict:
                    
                    if(not(self.community.all_term_types_dict[term]=='GO' and len(self.community.go_terms)>1)):
                        term_extra_img_paths_list, widths_list, term_extra_img_titles_list = self.community.term_img_dict[term]
                        
                        term_extra_img_paths_array_as_str = ','.join(term_extra_img_paths_list)
                        widths_array_as_str = ','.join(map(str, widths_list))
                        term_extra_img_titles_array_as_str = ','.join(term_extra_img_titles_list)
                        
                        html_f.write('<button class="view-button"  onclick="changeImg( \'' + self.community.name + '\' , \'extra\'  , \'' + term_extra_img_paths_array_as_str + '\' ,' + str(self.community.new_h) + ',\'' + widths_array_as_str + '\',\'' + term_extra_img_titles_array_as_str + '\',0)">View</button>\n')
                
                html_f.write('</td>\n')
                
                html_f.write('<td>\n')
                html_f.write(self.community.all_term_defs_dict[term]) 
                
            
            else:
                html_f.write('<button class="view-button"  onclick="changeImg( \'' + self.community.name + '\' , \'extra\'  , \'' + self.community.go_img_path + '\' ,' + str(self.community.new_h) + ',\'' + str(self.community.go_img_width) + '\',\'GO hierarchy\',0)">GO hierarchy</button>\n')
                html_f.write('</td>\n')
                html_f.write('<td>\n')
                html_f.write('</td>\n')
                html_f.write('<td>\n')
                            
            html_f.write('</td>\n')
            html_f.write('</tr>\n')
    
        html_f.write('</table>\n')
        html_f.write('</div>\n')
        
        html_f.write('<div class="spacer">\n')
        html_f.write('</div>\n')

        
    def _print_html_griditem3(self, html_f):
        html_f.write('<div class="extra">\n') # grid-item 3
        html_f.write('<div style="width: 1200px;">\n')
        html_f.write('<table><tr><td style="font-weight: bold;" id="' + self.community.name + '_extra_title">' + self.community.extra_img_title + '</td></tr></table>\n')
        html_f.write('<img id="' + self.community.name + '_extra" src="' + self.community.extra_img_path + '" width="' + str(self.community.extra_img_width)  + '" height="' + str(self.community.new_h) + '">\n')
        html_f.write('</div>\n')
        html_f.write('</div>\n')
    
    def print_html (self, html_f, summary_html, first_print, backlink=''):        
        super()._print_html_title(html_f, summary_html, first_print, backlink)
        
        html_f.write('<div class="grid-container">\n')
        
        self._print_html_griditem1(html_f)
        
        super()._print_html_griditem2(html_f)
        
        self._print_html_griditem3(html_f)
        
        super()._print_html_griditem4(html_f)
        
        html_f.write('</div>\n')
        #html_f.write('<hr>\n')
        #html_f.write('<br>\n')
        #html_f.write('<br>\n')
        #html_f.write('<br>\n')
    

class bigMixCommunityPrinter(bigBasicCommunityPrinter):
    def __init__ (self, community):
        super().__init__(community)
    
    def _print_html_griditem1(self, html_f):
        html_f.write('<div class="terms">\n') 
        html_f.write('<table style="font-size:small;white-space: nowrap;">\n')
        
        html_f.write('<tr>\n')
        html_f.write('<td>\n')
        html_f.write('<b>Member terms: </b>\n')
        html_f.write('</td>\n')
        html_f.write('<td>\n')
        html_f.write('</td>\n')
        html_f.write('<td>\n')
        html_f.write('</td>\n')
        html_f.write('</tr>\n')
        
        html_f.write('<tr>\n')
        html_f.write('<td>\n')
        html_f.write('</td>\n')
        html_f.write('<td>\n')
        html_f.write('</td>\n')
        html_f.write('<td>\n')
        html_f.write('</td>\n')
        html_f.write('</tr>\n')
        
        community_terms = self.community.terms
        
        if(self.community.go_img_path and len(self.community.go_terms)>1): #if we have more than one GO term and a corresponding Go term hierarchy...
            community_term_types = [term_type for (term, term_type) in [(t, self.community.all_term_types_dict[t]) for t in self.community.terms]]
            last_GO_index = len(community_term_types) - 1 - community_term_types[:: -1].index('GO')
            community_terms.insert(last_GO_index + 1, 'GO hierarchy')
                
        for term in community_terms:
            html_f.write('<tr>\n')
            html_f.write('<td>\n')
            
            if(not(term == 'GO hierarchy')):
                html_f.write(term)
                if(term == self.community.top_term_id):
                    html_f.write('<sup>*</sup>')
                html_f.write('</td>\n')
                
                html_f.write('<td>\n')
                
                if term in self.community.terms_with_desc_tables: # Only terms from MSIGDB can have decription tables (although we don't assume that they always do). 
                    # Note, of course, that if an MSIGDB term doesn't have a description table, this code will proceed to check for an image... But calling code
                    # will prevent any such term from having an extra image.
                    term_i = self.community.terms_with_desc_tables.index(term)
                    html_f.write('<button class="view-button"  onclick="changeTable( \'' + self.community.name + '\' , ' + str(term_i) + ' , ' + str(len(self.community.terms_with_desc_tables)) + ',\'extra\' , true , \'\' )">View</button>\n')
                
                elif term in self.community.term_img_dict:
                    if(not(self.community.all_term_types_dict[term]=='GO' and len(self.community.go_terms)>1)):
                        term_extra_img_paths_list, widths_list, term_extra_img_titles_list = self.community.term_img_dict[term]
                        
                        term_extra_img_paths_array_as_str = ','.join(term_extra_img_paths_list)
                        widths_array_as_str = ','.join(map(str, widths_list))
                        term_extra_img_titles_array_as_str = ','.join(term_extra_img_titles_list)
                        
                        html_f.write('<button class="view-button"  onclick="changeImg( \'' + self.community.name + '\' , \'extra\' , \'' + term_extra_img_paths_array_as_str + '\' ,' + str(self.community.new_h) + ',\'' + widths_array_as_str + '\',\'' + term_extra_img_titles_array_as_str + '\',' + str(len(self.community.terms_with_desc_tables)) + ')">View</button>\n')
                
                html_f.write('</td>\n')
                html_f.write('<td>\n')
                html_f.write(self.community.all_term_defs_dict[term])
                
            else:
                html_f.write('<button class="view-button"  onclick="changeImg( \'' + self.community.name + '\' , \'extra\'  , \'' + self.community.go_img_path + '\' ,' + str(self.community.new_h) + ',\'' + str(self.community.go_img_width) + '\',\'GO hierarchy\',' + str(len(self.community.terms_with_desc_tables)) + ')">GO hierarchy</button>\n')
                html_f.write('</td>\n')
                html_f.write('<td>\n')
                html_f.write('</td>\n')
                html_f.write('<td>\n')
            
            html_f.write('</td>\n')
            html_f.write('</tr>\n')
    
        html_f.write('</table>\n')
        html_f.write('</div>\n')
        html_f.write('<div class="spacer">\n')
        html_f.write('</div>\n')
       
        
    def _print_html_griditem3(self, html_f):
        html_f.write('<div class="extra">\n') # grid-item 3
        html_f.write('<div style="width: 1200px;">\n')
        
        
        first_term_shown = False
        for term_i in range(len(self.community.terms_with_desc_tables)):
            term = self.community.terms_with_desc_tables[term_i]
            term_desc_table = self.community.msigdb_html_soup.find(id=term)
            term_desc_table_html = term_desc_table.prettify()
            
            if(term == self.community.first_term_to_show):
                html_f.write('<div style="display:block;height:' + str(self.community.new_h + 18) + 'px;padding:0px;border:0px;margin:0px;" id="' +  self.community.name + '_extra_table_' + str(term_i)  + '">\n')
                first_term_shown = True
            else:
                html_f.write('<div style="display:none;height:' + str(self.community.new_h + 18) + 'px;padding:0px;border:0px;margin:0px;" id="' +  self.community.name + '_extra_table_' + str(term_i)  + '">\n')
            html_f.write(term_desc_table_html)
            html_f.write('</div>\n')
        
        
        if(first_term_shown):
            html_f.write('<table><tr><td style="font-weight: bold;" id="' + self.community.name + '_extra_title"></td></tr></table>\n')
            html_f.write('<img style="display:none;" id="' + self.community.name + '_extra" src="' + self.community.extra_img_path + '" width="' + str(self.community.extra_img_width) + '" height="' + str(self.community.new_h) + '">\n')
        else:
            html_f.write('<table><tr><td style="font-weight: bold;" id="' + self.community.name + '_extra_title">' + self.community.extra_img_title + '</td></tr></table>\n')
            html_f.write('<img style="display:inline;" id="' + self.community.name + '_extra" src="' + self.community.extra_img_path + '" width="' + str(self.community.extra_img_width)  + '" height="' + str(self.community.new_h) + '">\n')
        
        html_f.write('</div>\n')
        html_f.write('</div>\n')
    
    def print_html (self, html_f, summary_html, first_print, backlink='' ):

        super()._print_html_title(html_f, summary_html, first_print, backlink )
        
        html_f.write('<div class="grid-container">\n')
        
        self._print_html_griditem1(html_f)
        
        super()._print_html_griditem2(html_f)
        
        self._print_html_griditem3(html_f)
        
        super()._print_html_griditem4(html_f)
        
        html_f.write('</div>\n')
        #html_f.write('<hr>\n')
        #html_f.write('<br>\n')
        #html_f.write('<br>\n')
        #html_f.write('<br>\n')


# Community classes

class community:
    def __init__ (self, name, terms, quant_data_type, all_gene_qd, _exp_ids, all_term_types_dict, all_term_defs_dict, all_term_genes_dict, all_term_dotplot_dict, abs_images_dir, rel_images_dir,  extra_annotations_dict, num_extra_annotations, new_h, heatmap_width_min, heatmap_height_min, heatmap_min, heatmap_max, search_words, info_string, msigdb_html_soup, go_dag, exp_img_dir_paths_dict, exp_img_extension_dict):
        self.name = name
        self.abs_images_dir = abs_images_dir
        self.rel_images_dir = rel_images_dir
        self.extra_annotations_dict = extra_annotations_dict
        self.num_extra_annotations = num_extra_annotations
        self.new_h = new_h
        self.heatmap_width_min = heatmap_width_min
        self.heatmap_height_min = heatmap_height_min
        self.heatmap_min = heatmap_min
        self.heatmap_max = heatmap_max
        self.search_words = search_words
        self.info_string = info_string
        self.msigdb_html_soup = msigdb_html_soup
        self.go_dag = go_dag
        self.exp_img_dir_paths_dict = exp_img_dir_paths_dict
        self.exp_img_extension_dict = exp_img_extension_dict 
        
        self.quant_data_type = quant_data_type
        self.all_gene_qd = all_gene_qd
        self.exp_ids = _exp_ids
        self.all_term_types_dict = {k:v.upper() for k,v in all_term_types_dict.items()} # make sure all term types are in upper case
        self.all_term_defs_dict = all_term_defs_dict
        self.all_term_genes_dict = all_term_genes_dict
        self.all_term_dotplot_dict = all_term_dotplot_dict 
        self.terms = [term for (term, term_type) in sorted([(t, self.all_term_types_dict[t]) for t in  terms], key=lambda x: (x[1],x[0]))]
        
        
        (self.term_types, self.go_terms, self.type_label) = self.__set_term_types_info()
        self.name = self.name + ' (' + self.type_label + ')' ### Adding term type to community name
        
        self.term_genes_dict = self.__make_term_genes_dict()
        self.genes = self.__make_unique_gene_list()
        self.genes_sorted = sorted(self.genes)
        
    def __set_term_types_info(self):
        my_term_types = []
        my_go_terms = []
        
        for term in self.terms:
            #term_type = self.all_term_types_dict[ term ].upper()
            term_type = self.all_term_types_dict[term]
            
            if(term_type == "GO"):
                my_go_terms.append(term)
            
            if not(term_type in my_term_types):
                my_term_types.append(term_type)
                
        my_term_types.sort()
        
        return (my_term_types, my_go_terms, ' '.join(my_term_types))
    
    def __make_term_genes_dict(self):
        my_term_genes_dict = {}
        for term in self.terms:
            my_term_genes_dict[term] = self.all_term_genes_dict[term]
        return my_term_genes_dict
    
    def __make_unique_gene_list(self):
        my_genes = list(set([gene for gene_set in list(self.term_genes_dict.values()) for gene in gene_set]))
        return my_genes
    
    def calc_overlap(self, other_community, measure):
        if(measure == 'JI'):
            return self.calc_Jaccard(other_community)
        elif(measure == 'OC'):
            return self.calc_overlap_coeff(other_community)
        else:
            print('WARNING, measure for calculating overlap is not valid. Please choose either "JI" (for Jaccard Index) or "OC" (for Overlap Coefficient).')
            return 0
            
    def calc_Jaccard(self, other_community):
        set_1 = set(self.genes)
        set_2 = set(other_community.genes)
        return len(set.intersection(set_1, set_2)) / len(set.union(set_1, set_2))
        
    def calc_overlap_coeff(self, other_community):
        set_1 = set(self.genes)
        set_2 = set(other_community.genes)
        return len(set.intersection(set_1, set_2)) / min(len(set_1), len(set_2))
    

class bigCommunity(community):
    def __init__ (self, name, terms, quant_data_type, all_gene_qd, _exp_ids, all_term_types_dict, all_term_defs_dict, all_term_genes_dict, all_term_dotplot_dict, abs_images_dir, rel_images_dir, extra_annotations_dict, num_extra_annotations, new_h, heatmap_width_min, heatmap_height_min, heatmap_min, heatmap_max, search_words, info_string, msigdb_html_soup, go_dag, exp_img_dir_paths_dict, exp_img_extension_dict):
        super().__init__(name, terms, quant_data_type, all_gene_qd, _exp_ids, all_term_types_dict, all_term_defs_dict, all_term_genes_dict, all_term_dotplot_dict, abs_images_dir, rel_images_dir, extra_annotations_dict, num_extra_annotations, new_h, heatmap_width_min, heatmap_height_min, heatmap_min, heatmap_max, search_words, info_string, msigdb_html_soup, go_dag, exp_img_dir_paths_dict, exp_img_extension_dict )
        
        if( self.all_term_dotplot_dict ):
            et_pairs = [ ( e , t ) for e in self.exp_ids for t in self.terms ]
            self.top_term_id = [ term for ( term , term_nlog10p ) in sorted( [ ( t , self.all_term_dotplot_dict[( e , t )][1] ) for ( e , t ) in  et_pairs ], key = lambda x: (-x[1],x[0]) ) ][0]
            
        else:
            self.top_term_id = [ term for ( term , term_numgenes ) in sorted( [ ( t , len( self.term_genes_dict[t] ) ) for t in  self.terms ], key = lambda x: (-x[1],x[0]) ) ][0]
            
        top_term_def = self.all_term_defs_dict[ self.top_term_id ]
        self.top_term = self.top_term_id + ' - ' + top_term_def
            
            
        
        self.go_img_path = ''
        self.go_img_width = 0
        
        self.extra_img_path = ''
        self.extra_img_width = 0
        self.extra_img_title = ''
        
        self.terms_with_desc_tables = []
        self.term_img_dict = {}
        self.first_term_to_show = ''
        
        self.bcprinter = None
        
        self.meta_community_name = ''
        self.meta_community_siblings = []
        self.overlapping_singleton_communities_names = []
        
        # Draw UpSet plot
        my_upsetDrawer = upsetDrawer( self )
        ( self.upset_img_path , self.upset_img_width ) = my_upsetDrawer.draw_upset_plot()
        
        
        # Draw Heatmap plot
        _etg_data = []
        for _e in self.exp_ids:
            for _t in self.terms:
                for _g in sorted(self.term_genes_dict[ _t ]):
                    if( ( _e , _g ) in self.all_gene_qd.index ):
                        _etg_data.append( ( _e , _t , _g , self.all_gene_qd.loc[ ( _e , _g ) ].iloc[0] , 1 ) )
                        
        self.etg_df = pd.DataFrame.from_records( _etg_data , columns = [ 'FEA' , 'Term' , 'Gene' , 'QD' , 'Present' ] )
        
        self.gene_term_heatmap_df = self.etg_df[ [ 'Term' , 'Gene' , 'Present' ] ].drop_duplicates().pivot_table(index='Term', columns='Gene', values='Present', fill_value=0).reindex( index=self.terms, columns = self.genes_sorted )
        self.gene_term_heatmap_fm_df = self.etg_df[ [ 'Term' , 'Gene' , 'Present' ] ].drop_duplicates().pivot_table(index='Term', columns='Gene', values='Present').reindex( index=self.terms, columns = self.genes_sorted )
        self.gene_exp_heatmap_df = self.etg_df[ [ 'FEA' , 'Gene' , 'QD' ] ].drop_duplicates().pivot_table(index='FEA', columns='Gene', values='QD', fill_value=0).reindex( index=self.exp_ids, columns = self.genes_sorted )
        self.gene_exp_heatmap_fm_df = self.etg_df[ [ 'FEA' , 'Gene' , 'QD' ] ].drop_duplicates().pivot_table(index='FEA', columns='Gene', values='QD').reindex( index=self.exp_ids, columns = self.genes_sorted )
        
        self.rows_cols = ( [] , [] )
        if( len( self.genes ) > 25 and len( self.terms ) >= 4 and 
           (sum(self.gene_term_heatmap_df.sum() > 0) > sum(self.gene_term_heatmap_df.sum() > (len( self.terms )//4)))):
            self.rows_cols = ( ( range( len( self.terms ) ) , self.gene_term_heatmap_df.sum() > 0 ) )
            my_heatmapDrawer_full = heatmapDrawer( self )
            
            if( len(self.exp_ids) > 1 ):
                ( heatmap_img_paths_list_full , heatmap_img_widths_list_full  , heatmap_img_titles_list_full  ) = my_heatmapDrawer_full.draw_heatmaps( postfix='full')
            else:
                ( heatmap_img_paths_list_full , heatmap_img_widths_list_full  , heatmap_img_titles_list_full  ) = my_heatmapDrawer_full.draw_heatmaps( ylabel2='', postfix='full' )
            
            
            self.rows_cols = ( ( range( len( self.terms ) ) , self.gene_term_heatmap_df.sum() > len( self.terms )//4 ) )
            my_heatmapDrawer_truncated = heatmapDrawer( self )
            
            if( len(self.exp_ids) > 1 ):
                ( heatmap_img_paths_list_truncated , heatmap_img_widths_list_truncated , heatmap_img_titles_list_truncated ) = my_heatmapDrawer_truncated.draw_heatmaps( postfix='truncated')
            else:
                ( heatmap_img_paths_list_truncated , heatmap_img_widths_list_truncated , heatmap_img_titles_list_truncated ) = my_heatmapDrawer_truncated.draw_heatmaps( ylabel2='', postfix='truncated' )
                
                
            self.heatmap_img_paths_list = heatmap_img_paths_list_truncated + heatmap_img_paths_list_full
            self.heatmap_img_widths_list = heatmap_img_widths_list_truncated + heatmap_img_widths_list_full
            self.heatmap_img_titles_list = heatmap_img_titles_list_truncated + heatmap_img_titles_list_full
            
        else:
            self.rows_cols = ( ( range( len( self.terms ) ) , self.gene_term_heatmap_df.sum() > 0 ) )
            my_heatmapDrawer = heatmapDrawer( self )
        
            if( len(self.exp_ids) > 1 ):
                ( self.heatmap_img_paths_list , self.heatmap_img_widths_list , self.heatmap_img_titles_list ) = my_heatmapDrawer.draw_heatmaps( )
            else:
                ( self.heatmap_img_paths_list , self.heatmap_img_widths_list , self.heatmap_img_titles_list ) = my_heatmapDrawer.draw_heatmaps( ylabel2 = '' )
        
        # Before drawing the rest of the plots, extract the gene list that's shown in the heatmap:
        ( _ , s_cols ) = self.rows_cols
        self.included_genes = [ self.genes_sorted[ i ] for i in range( len( self.genes_sorted ) ) if s_cols.iloc[i]]
        
        
        #*****************************************************************************************
        # Now draw the Circos plot. This will sit with UpSet plot, but is created here because needs information from heatmap generation
        
        # Draw Circos plot
        my_circosDrawer = circosDrawer(self, rows_cols = (( range( len( self.terms ) ) , self.gene_term_heatmap_df.sum() > 0 )))
        ( self.circos_img_path , self.circos_img_width ) = my_circosDrawer.draw_circos()
        
        #*****************************************************************************************
        
        
        if( self.all_term_dotplot_dict ):
            # Draw Dotplot plot
            my_dotplotDrawer = dotplotDrawer( self )
            self.dotplot_img_paths_list = [ ]
            self.dotplot_img_widths_list = [ ]
            self.dotplot_img_titles_list = [ ]
            for e in self.exp_ids:
                ( dotplot_img_path , dotplot_img_width ) = my_dotplotDrawer.draw_dotplot(e)
                self.dotplot_img_paths_list.append( dotplot_img_path )
                self.dotplot_img_widths_list.append( dotplot_img_width )
                
                dotplot_title_extension = ''
                if(len(self.exp_ids) > 1):
                    dotplot_title_extension = ' of ' + e
                    
                self.dotplot_img_titles_list.append( 'Dot plot' + dotplot_title_extension )
        

        # Draw GO hierarchy, if GO terms present
        if( 'GO' in self.term_types ):
            my_go_hierarchyDrawer = go_hierarchyDrawer( self )
            ( self.go_img_path , self.go_img_width ) = my_go_hierarchyDrawer.draw_hierarchy()           
        
        # Any extra images...
        num_extra_images = 0
        num_desc_tables = 0
        for term in self.terms:
            
            if( not( self.all_term_types_dict[ term ][0:6] == 'MSIGDB' ) ): # To avoid confusion, MSIGDB terms cannot have associated images, so don't even
                                                                        # look for one if this is an MSIGDB term
            
                if( self.all_term_types_dict[ term ] == 'GO' ):
                    self.term_img_dict[ term ] = ( [ self.go_img_path ] , [ self.go_img_width ] , [ 'GO hierarchy' ])
                    
                    # if first term to show has not yet been set, set it now. Note
                    # that boolean value of the empty string is False.
                    if( not( self.first_term_to_show ) ): 
                        self.first_term_to_show = term
                
                else:
                    for e in self.exp_ids:
                        input_img_dir_path = self.exp_img_dir_paths_dict[ e ]
                        img_extension = self.exp_img_extension_dict[ e ]
                        
                        term_image_file = Path( input_img_dir_path + '/' + term + img_extension )
                
                        if( term_image_file.exists()):
                            num_extra_images += 1
                            term_image = Image.open( input_img_dir_path + '/' + term + img_extension )
                            
                            new_term_image_filename = ( term + '_' + e ).replace( ':' , '' ).replace( ' ' , '' ) + img_extension
                            
                            suffix = 1
                            while(Path(self.abs_images_dir + new_term_image_filename).exists()):
                                new_term_image_filename = ( term + '_' +  str(suffix) + '_' + e ).replace( ':' , '' ).replace( ' ' , '' ) + img_extension
                                suffix += 1
                            
                            #term_image.save( self.abs_images_dir + ( term + '_' + e ).replace( ':' , '' ).replace( ' ' , '' ) + img_extension )
                            term_image.save(self.abs_images_dir + new_term_image_filename)
                            w,h = term_image.size
                            new_w = ( self.new_h * w/h )
                            term_image.close()
                            
                            term_title_extension = ''
                            if(len(self.exp_ids)>1):
                                term_title_extension = '_' + e
                                
                            if( not( term in self.term_img_dict ) ):
                                #self.term_img_dict[ term ] = ( [ self.rel_images_dir + ( term + '_' + e ).replace( ':' , '' ).replace( ' ' , '' ) + img_extension ] , [ new_w ] , [ term + term_title_extension ] )
                                self.term_img_dict[term] = ([self.rel_images_dir + new_term_image_filename], [new_w], [term + term_title_extension])
                            else:
                                l1,l2,l3 = self.term_img_dict[term]
                                #self.term_img_dict[ term ] = ( l1 + [ self.rel_images_dir + ( term + '_' + e ).replace( ':' , '' ).replace( ' ' , '' ) + img_extension ] , l2 + [ new_w ] , l3 + [ term + term_title_extension ] )
                                self.term_img_dict[term] = (l1 + [self.rel_images_dir + new_term_image_filename], l2 + [new_w], l3 + [term + term_title_extension])
                            
                            # if first term to show has not yet been set, set it now. Note
                            # that boolean value of the empty string is False.
                            if( not( self.first_term_to_show ) ): 
                                self.first_term_to_show = term
                        
            else:
                if( self.msigdb_html_soup.find(id=term) != None ):
                    num_desc_tables += 1
                    self.terms_with_desc_tables.append( term )
                    # if first term to show has not yet been set, set it now. Note that boolean value of the empty string is False.
                    if( not( self.first_term_to_show ) ): 
                        self.first_term_to_show = term
                            
        # Now choose the correct printer...            
        if( num_desc_tables == 0 ):
            if ( num_extra_images == 0 ):       
                if( not ( 'GO' in self.term_types ) ):
                    self.bcprinter = bigBasicCommunityPrinter( self )    
                else:
                    self.extra_img_path  = self.go_img_path
                    self.extra_img_width  = self.go_img_width
                    self.extra_img_title = 'GO hierarchy'
                    
                    self.bcprinter = bigOneExtraImgCommunityPrinter( self )
            else: # One or more extra images
                #set extra image to be the first image in term_img_dict...
                ( self.extra_img_path , *rest ) , ( self.extra_img_width , *rest ) , ( self.extra_img_title , *rest ) = self.term_img_dict[ list(self.term_img_dict.keys())[0] ]
                
                if( ( num_extra_images == 1 ) and ( not ( 'GO' in self.term_types ) ) ): # Only one extra image, and no GO image...
                    self.bcprinter = bigOneExtraImgCommunityPrinter( self ) 
                else:
                    self.bcprinter = bigManyExtraImgCommunityPrinter( self )
        
        else: # One or more description tables
            if( num_extra_images > 0 ):
                ( self.extra_img_path , *rest ) , ( self.extra_img_width , *rest ) , ( self.extra_img_title , *rest ) = self.term_img_dict[ list(self.term_img_dict.keys())[0] ]
                self.bcprinter = bigMixCommunityPrinter( self )
            else: # No extra images except for possibly a GO image...
                if( not ( 'GO' in self.term_types ) ): # No GO image, so only need to print description tables...
                    if( num_desc_tables == 1 ):
                        self.bcprinter = bigOneDescTableCommunityPrinter( self )
                    else: # num_desc_table > 1
                        self.bcprinter = bigManyDescTableCommunityPrinter( self )
                else: # There is a GO image to include
                    self.extra_img_path  = self.go_img_path
                    self.extra_img_width  = self.go_img_width
                    self.extra_img_title = 'GO hierarchy' # ADDED TO FIX BUG THAT I HAVEN'T OBSERVED, BUT THINK EXISTS. REMOVE AND TEST, ADD BACK IN AND TEST. SEE TODO
                    
                    self.bcprinter = bigMixCommunityPrinter( self )
        
    
    def print_csv(self, csv_f):
        my_community_csv_printer = communityCsvPrinter(self)
        my_community_csv_printer.print_csv(csv_f)
    
    def print_html ( self , html_f , summary_html , first_print, backlink = '' ):
        self.bcprinter.print_html( html_f , summary_html , first_print, backlink )
          
    def set_meta_community_name ( self , meta_community_name ):
        self.meta_community_name = meta_community_name
    
    def set_meta_community_siblings ( self , meta_community_siblings ):
        self.meta_community_siblings = meta_community_siblings
    
        
    def add_overlapping_singleton_community_name ( self , overlapping_singleton_community_name ):
        self.overlapping_singleton_communities_names.append( overlapping_singleton_community_name )
   



class singletonCommunity( community ):
    def __init__ ( self , name , terms , quant_data_type , all_gene_qd , _exp_ids , all_term_types_dict , all_term_defs_dict , all_term_genes_dict , all_term_dotplot_dict , abs_images_dir , rel_images_dir , extra_annotations_dict, num_extra_annotations, new_h , heatmap_width_min, heatmap_height_min, heatmap_min , heatmap_max , search_words , info_string , msigdb_html_soup , go_dag , exp_img_dir_paths_dict , exp_img_extension_dict ):
        super().__init__( name , terms , quant_data_type , all_gene_qd , _exp_ids , all_term_types_dict , all_term_defs_dict , all_term_genes_dict , all_term_dotplot_dict , abs_images_dir , rel_images_dir , extra_annotations_dict, num_extra_annotations, new_h , heatmap_width_min, heatmap_height_min, heatmap_min , heatmap_max , search_words , info_string , msigdb_html_soup , go_dag , exp_img_dir_paths_dict , exp_img_extension_dict )
        
        self.name = name # NOTE: The superclass 'community' adds term type label to name,
                         # but this is not desirable behaviour for a singleton community,
                         # so changing it back here.
        
        # These variables are used in the heatmap and literature search for this term,
        # However, they cannot be set until *after* overlapping big communities have
        # been identified; a step which has to happen after a singletonCommunity has been
        # created. ************************************************************
        self.heatmap_img_path = ''
        self.heatmap_img_width = 0
        
        self.heatmap_img_paths_list = [] 
        self.heatmap_img_widths_list = [] 
        self.heatmap_img_titles_list = []
        
        self.overlapping_big_communities = []
        self.rows_cols = ( [] , [] )
        self.hm_y1_label = ''
        self.included_genes = []
        # *********************************************************************
        
        # Now sort out description and extra images, as required.
#        self.extra_img_path = ''
#        self.extra_img_width = 0
#        self.extra_title = ''
        
        self.extra_img_paths = []
        self.extra_img_widths = []
        self.extra_img_titles = []
        
        self.num_extra_images = 0
        self.num_desc_tables = 0
        self.term = self.terms[0]
        
        if( not( self.all_term_types_dict[ self.term ][0:6] == 'MSIGDB' ) ): # To avoid confusion, MSIGDB terms cannot have associated images, so don't even
                                                                             # look for one if this is an MSIGDB term
        
            if( 'GO' in self.term_types ):
                my_go_hierarchyDrawer = go_hierarchyDrawer( self )
#                ( self.extra_img_path , self.extra_img_width ) = my_go_hierarchyDrawer.draw_hierarchy()
#                self.extra_title = self.name
                (go_img_path, go_img_width) = my_go_hierarchyDrawer.draw_hierarchy()
                self.extra_img_paths.append(go_img_path)
                self.extra_img_widths.append(go_img_width)
                self.extra_img_titles.append(self.name)
                
                self.num_extra_images = 1
            else:
                for e in self.exp_ids:
                    input_img_dir_path = self.exp_img_dir_paths_dict[ e ]
                    img_extension = self.exp_img_extension_dict[ e ]
                    
                    term_image_file = Path( input_img_dir_path + '/' + self.term + img_extension )
            
                    if( term_image_file.exists()):
                        
                        term_image = Image.open( input_img_dir_path + '/' + self.term + img_extension )
                        
                        new_term_image_filename = ( self.term + '_' + e ).replace( ':' , '' ).replace( ' ' , '' ) + img_extension
                            
                        suffix = 1
                        while(Path(self.abs_images_dir + new_term_image_filename).exists()):
                            new_term_image_filename = ( self.term + '_' +  str(suffix) + '_' + e ).replace( ':' , '' ).replace( ' ' , '' ) + img_extension
                            suffix += 1
                        
                        #term_image.save( self.abs_images_dir + ( self.term + '_' + e ).replace( ':' , '' ).replace( ' ' , '' ) + img_extension )
                        term_image.save(self.abs_images_dir + new_term_image_filename)
                        w,h = term_image.size
                        new_w = ( self.new_h * w/h )
                        term_image.close()
                        
#                        name_title_extension = ''
#                        if(len(self.exp_ids)>1):
#                            name_title_extension = '_' + e
#                            #self.extra_img_paths.append( self.rel_images_dir + ( self.term + '_' + e ).replace( ':' , '' ).replace( ' ' , '' ) + img_extension )
#                            self.extra_img_paths.append(self.rel_images_dir + new_term_image_filename)
#                            self.extra_img_widths.append( new_w )
#                            self.extra_img_titles.append( self.name + name_title_extension )
#                        
#                        # if this is the first extra image found, then set self.extra_img_path and self.extra_img_width
#                        if( not( self.extra_img_path ) ): 
#                            self.extra_img_path = self.rel_images_dir + ( self.term + '_' + e ).replace( ':' , '' ).replace( ' ' , '' ) + img_extension
#                            self.extra_img_width = new_w
#                            self.extra_title = self.name + name_title_extension
#                            
#                        self.num_extra_images += 1
                        
                        name_title_extension = ''
                        if(len(self.exp_ids)>1):
                            name_title_extension = '_' + e
                            
                        self.extra_img_paths.append(self.rel_images_dir + new_term_image_filename)
                        self.extra_img_widths.append( new_w )
                        self.extra_img_titles.append( self.name + name_title_extension )
                            
                        self.num_extra_images += 1                    
        else:
            if( self.msigdb_html_soup.find( id = self.term ) != None ):
                self.num_desc_tables += 1
            
        
    def add_overlapping_big_community ( self , overlapping_big_community ):
        self.overlapping_big_communities.append( overlapping_big_community )
        
    
    def print_csv(self, csv_f):
        my_singleton_community_csv_printer = singletonCommunityCsvPrinter(self)
        
        _etg_data = []
        for _e in self.exp_ids:
                for _g in sorted(self.term_genes_dict[self.terms[0]]):
                    if( ( _e , _g ) in self.all_gene_qd.index ):
                        _etg_data.append( ( '', '' , _e , self.term , _g , self.all_gene_qd.loc[ ( _e , _g ) ].iloc[0] ) )
                        
        self.singleton_etg_df = pd.DataFrame.from_records( _etg_data , columns = ['Community', 'Meta-community', 'FEA', 'Term', 'Gene', 'QD'] )
        
        my_singleton_community_csv_printer.print_csv(csv_f)


    def pre_print ( self ):
        
        if( len( self.overlapping_big_communities ) > 0 ):
            
            self.hm_y1_label = 'Term/ Community'
            self.overlapping_big_communities.sort( key=lambda x: x.name )
            
            for bc in self.overlapping_big_communities:

                self.terms.append( bc.name )
                self.term_genes_dict[ bc.name ] = list( set.intersection( set( self.genes ) , set( bc.genes ) ) )
            
        self.terms[0] = 'term'
        self.term_genes_dict[ 'term' ] = self.term_genes_dict[ self.term ]
        del self.term_genes_dict[ self.term ]
            
            
        _etg_data = []
        for _e in self.exp_ids:
            for _t in self.terms:
                for _g in self.term_genes_dict[ _t ]:
                    if( ( _e , _g ) in self.all_gene_qd.index ):
                        _etg_data.append( ( _e , _t , _g , self.all_gene_qd.loc[ ( _e , _g ) ].iloc[0] , 1 ) )
                        
        _etg_df = pd.DataFrame.from_records( _etg_data , columns = [ 'FEA' , 'Term' , 'Gene' , 'QD' , 'Present' ] )
        
        self.gene_term_heatmap_df = _etg_df[ [ 'Term' , 'Gene' , 'Present' ] ].drop_duplicates().pivot_table(index='Term', columns='Gene', values='Present', fill_value=0).reindex( index=self.terms, columns = self.genes_sorted )
        self.gene_term_heatmap_fm_df = _etg_df[ [ 'Term' , 'Gene' , 'Present' ] ].drop_duplicates().pivot_table(index='Term', columns='Gene', values='Present').reindex( index=self.terms, columns = self.genes_sorted )
        self.gene_exp_heatmap_df = _etg_df[ [ 'FEA' , 'Gene' , 'QD' ] ].drop_duplicates().pivot_table(index='FEA', columns='Gene', values='QD', fill_value=0).reindex( index=self.exp_ids, columns = self.genes_sorted )
        self.gene_exp_heatmap_fm_df = _etg_df[ [ 'FEA' , 'Gene' , 'QD' ] ].drop_duplicates().pivot_table(index='FEA', columns='Gene', values='QD').reindex( index=self.exp_ids, columns = self.genes_sorted )
    
        self.rows_cols = ( ( range( len( self.terms ) ) , self.gene_term_heatmap_df.sum() > 0 ) )
            
        my_heatmapDrawer = heatmapDrawer( self )
        
        if( len(self.exp_ids) > 1 ):
            ( self.heatmap_img_paths_list , self.heatmap_img_widths_list , self.heatmap_img_titles_list ) = my_heatmapDrawer.draw_heatmaps( ylabel1 = self.hm_y1_label )
        else:
            ( self.heatmap_img_paths_list , self.heatmap_img_widths_list , self.heatmap_img_titles_list ) = my_heatmapDrawer.draw_heatmaps( ylabel1 = self.hm_y1_label , ylabel2 = '' )
        
        
        
        # Before continuing with HTML printing, extract the gene list that's shown in the heatmap:
        ( _ , s_cols ) = self.rows_cols
        self.included_genes = [ self.genes_sorted[ i ] for i in range( len( self.genes_sorted ) ) if s_cols.iloc[i]]
    
    
    def print_html ( self , html_f , summary_html , first_print, backlink = '' ):
        # get ready for printing...
        self.pre_print()
        
        if(first_print):
            html_f.write('<div style="height:110px" id="' + self.name +'"></div>\n')
        else:
            html_f.write('<div style="height:100px" id="' + self.name +'"></div>\n')
            html_f.write('<hr>\n')
        
        # gather some important data and make heatmap...
        if(self.all_term_dotplot_dict):
            html_f.write('<button type="button" class="collapsible3b">\n')
        else:
            html_f.write('<button type="button" class="collapsible3a">\n')
            
        html_f.write('<table>\n')
        html_f.write('<tr><td></td></tr>\n')
        html_f.write('<tr>\n')
        if( self.name == self.all_term_defs_dict[ self.name ] ):
            html_f.write('<td><h5 class="title">' + self.name + '</h5></td>\n')
            #html_f.write('<td><h5 class="title">' + self.name + ' ' + self.info_string + '</h5></td>\n')
        else:
            html_f.write('<td><h5 class="title">' + self.name + ' ' + self.all_term_defs_dict[ self.name ] + '</h5></td>\n')
            #html_f.write('<td><h5 class="title">' + self.name + ' ' + self.all_term_defs_dict[ self.name ] + ' ' + self.info_string + '</h5></td>\n')
        
        #html_f.write('<td><button class="view-button" style="font-size:small;" onclick="document.location=\'' + summary_html + '\'">Communities summary</button></td>\n' )
        
        #if( backlink ):
        #    html_f.write('<td><button class="view-button" style="font-size:small;" onclick="document.location=\'' + backlink + '\'">Main page</button></td>\n' )
        
        html_f.write('</tr>\n')
        html_f.write('</table></button>\n')
        
        if( self.all_term_dotplot_dict ):
            html_f.write('<table class="content" style="font-size:small;white-space: nowrap;">\n')
            if( len(self.exp_ids) == 1 ):
                gr,nlog10p,c,gr_string,bg_string = self.all_term_dotplot_dict[ (self.exp_ids[0], self.term) ]
                html_f.write('<tr><td>' + 'gene ratio: ' + gr_string + ', Bg ratio: ' +  bg_string + ', -log10(padj): ' + str( nlog10p ) + '</td></tr>')
            else:
                for e in self.exp_ids:
                    gr,nlog10p,c,gr_string,bg_string = self.all_term_dotplot_dict[ ( e , self.term ) ]
                    html_f.write('<tr><td>' + e + '</td><td>' + 'gene ratio: ' + gr_string + ', Bg ratio: ' +  bg_string + ', -log10(padj): ' + str( nlog10p ) + '</td></tr>')
            html_f.write('</table>\n')
        
            
        html_f.write('<div class="grid-container3">\n')
        html_f.write('<div class="overlaps3" style="max-height: ' + str( self.new_h + 25 ) + 'px;">\n')
        html_f.write('<table style="font-size:small;white-space: nowrap;">\n')
        
        html_f.write('<tr>\n')
        html_f.write('<td>\n')
        html_f.write('<b>Overlapping communities: </b>\n')
        html_f.write('</td>\n')
        html_f.write('<td>\n')
        html_f.write('</td>\n')
        html_f.write('</tr>\n')
        
        html_f.write('<tr>\n')
        html_f.write('<td>\n')
        html_f.write('</td>\n')
        html_f.write('<td>\n')
        html_f.write('</td>\n')
        html_f.write('</tr>\n')
        
        if( len( self.overlapping_big_communities ) > 0 ):
            
            self.overlapping_big_communities.sort( key=lambda x: x.name )
            
            
            for bc in self.overlapping_big_communities:
                html_f.write('<tr>\n')
                html_f.write('<td>\n')
                html_f.write('<a href="#' + bc.name + '">' + bc.name + '</a>\n' )
                html_f.write('</td>\n')
                html_f.write('<td>\n')
                html_f.write( bc.top_term )
                html_f.write('</td>\n')
                html_f.write('</tr>\n')
        else:
            html_f.write('<tr>\n')
            html_f.write('<td>\n')
            html_f.write('<b>None</b>\n')
            html_f.write('</td>\n')
            html_f.write('<td>\n')
            html_f.write('</td>\n')
            html_f.write('</tr>\n')
   
        html_f.write('</table>\n')
        html_f.write('</div>\n')
        
        html_f.write('<div class="spacer3a">\n')
        html_f.write('</div>\n')
        html_f.write('<div class="spacer3b">\n')
        html_f.write('</div>\n')
                
        html_f.write('<div class="heatmap3">\n')
        html_f.write('<div style="width: 1200px;">\n')
        html_f.write('<table><tr><td style="font-weight: bold;" id="' + self.name + '_heatmap_title">' + self.heatmap_img_titles_list[0] + '</td></tr></table>\n')
        html_f.write('<img id="' + self.name + '_heatmap" src="' + self.heatmap_img_paths_list[0] + '" width="' + str( self.heatmap_img_widths_list[0] )  + '" height="' + str( self.new_h ) + '">\n')
        
        
        html_f.write('<div style="display:none;height:' + str( self.new_h + 3 ) + 'px;padding:0px;border:0px;margin:0px;" id="' +  self.name + '_heatmap_table_0">\n')
        html_f.write('<table style="font-size:small;white-space: nowrap;">\n')
        html_f.write('<tr>\n')
        html_f.write('<td>\n')
        html_f.write('<b>Gene</b>\n')
        html_f.write('</td>\n')
        html_f.write('<td>\n')
        html_f.write('<b>NCBI: Gene database</b>\n')
        html_f.write('</td>\n')
        html_f.write('<td>\n')
        html_f.write('<b>NCBI: PubMed database (Gene only)</b>\n')
        html_f.write('</td>\n')
        
        if(len(self.search_words) > 0):
            html_f.write('<td>\n')
            html_f.write('<b>NCBI: PubMed database (Gene and keywords)</b>\n')
            html_f.write('</td>\n')
        
        html_f.write('</tr>\n')
        
        for inc_gene in self.included_genes:
            ( ncbi_gene_href , pubmed_gene_href , pubmed_search_href , pubmed_print_string ) = build_searches( inc_gene , self.search_words )
            html_f.write('<tr>\n')
            
            html_f.write('<td>\n')
            html_f.write(inc_gene + '\n') 
            html_f.write('</td>\n')
            
            html_f.write('<td>\n')
            html_f.write('<a href = "' + ncbi_gene_href + '" target="_blank">' + inc_gene + ' (NCBI: Gene)</a>\n') 
            html_f.write('</td>\n')
            
#            html_f.write('<td>\n')
#            html_f.write('<a href = "' + ensembl_gene_href + '" target="_blank">' + inc_gene + ' (ENSEMBL)</a>\n') 
#            html_f.write('</td>\n')
            
            html_f.write('<td>\n')
            html_f.write('<a href = "' + pubmed_gene_href + '" target="_blank">' + inc_gene + ' (NCBI: PubMed)</a>\n') 
            html_f.write('</td>\n')
            
            if(len(self.search_words) > 0):
                html_f.write('<td>\n')
                html_f.write('<a href = "' + pubmed_search_href + '" target="_blank">' + pubmed_print_string + ' (NCBI: PubMed)</a>\n') 
                html_f.write('</td>\n')
            
            html_f.write('</tr>\n')
        
        html_f.write('</table>\n')
        html_f.write('<div style="height:2500px;"></div>\n')
        html_f.write('</div>\n')
        
        
        html_f.write('</div>\n')
        html_f.write('</div>\n')
                         
        
        #heatmap_img_paths_array_as_str = ','.join( self.heatmap_img_paths_list )
        #heatmap_widths_array_as_str = ','.join( map( str , self.heatmap_img_widths_list ) )
        #heatmap_img_titles_array_as_str = ','.join( self.heatmap_img_titles_list )
        
        html_f.write('<div class="plot_buttons3">\n')
        #html_f.write('<button class="view-button"  onclick="changeImg( \'' + self.name + '\' , \'heatmap\'  , \'' + heatmap_img_paths_array_as_str + '\' ,' + str( self.new_h ) + ',\'' + heatmap_widths_array_as_str + '\',\'' + heatmap_img_titles_array_as_str + '\',1)">Heatmaps</button>\n' )
        html_f.write('<button class="view-button"  onclick="changeImg( \'' + self.name + '\' , \'heatmap\'  , \'' + self.heatmap_img_paths_list[0] + '\' ,' + str( self.new_h ) + ',\'' + str(self.heatmap_img_widths_list[0]) + '\',\'' + self.heatmap_img_titles_list[0] + '\',1)">Heatmap A (' + self.quant_data_type +')</button>\n' )
        html_f.write('<button class="view-button"  onclick="changeImg( \'' + self.name + '\' , \'heatmap\'  , \'' + self.heatmap_img_paths_list[1] + '\' ,' + str( self.new_h ) + ',\'' + str(self.heatmap_img_widths_list[1]) + '\',\'' + self.heatmap_img_titles_list[1] + '\',1)">Heatmap B (annotations x ' + self.quant_data_type +')</button>\n' )
        html_f.write('<button class="view-button"  onclick="changeImg( \'' + self.name + '\' , \'heatmap\'  , \'' + self.heatmap_img_paths_list[2] + '\' ,' + str( self.new_h ) + ',\'' + str(self.heatmap_img_widths_list[2]) + '\',\'' + self.heatmap_img_titles_list[2] + '\',1)">Heatmap C (alphabetical)</button>\n' )
        
        
        html_f.write('<button class="view-button"  onclick="changeTable( \'' + self.name + '\' , 0 , 1 ,\'heatmap\', true , \'Literature search\')">Literature search</button>\n' )
    
        if( len(self.exp_ids) > 1 and ( self.num_extra_images > 1 ) ):# only want a button to toggle through extra images if there is more than one such image... len(self.exp_ids) > 1
                                                                      # is necessary, but not sufficient for this to be the case, hence the extra check here.
            extra_img_paths_array_as_str = ','.join( self.extra_img_paths )
            widths_array_as_str = ','.join( map( str , self.extra_img_widths ) )
            extra_img_titles_array_as_str = ','.join( self.extra_img_titles )                
                
            html_f.write( '<button class="view-button"  onclick="changeImg( \'' + self.name + '\' , \'extra\'  , \'' + extra_img_paths_array_as_str + '\' ,' + str( self.new_h ) + ',\'' + widths_array_as_str + '\',\'' + extra_img_titles_array_as_str + '\',0)"><span>&#8595;</span> Toggle ' + self.name + ' figures <span>&#8595;</span></button>\n' )
        
        html_f.write('</div>\n')        
        
        html_f.write('<div class="extra3">\n')
        html_f.write('<div style="width: 1200px;">\n')
        
        # Only terms from MSIGDB can have decription tables (although we don't assume that they always do). 
        # Note, of course, that if an MSIGDB term doesn't have a description table, this code will proceed to check for an image... But code above
        # will prevent any such term from having an extra image.
        if( self.num_desc_tables == 1 ):
            
            term_desc_table = self.msigdb_html_soup.find( id = self.term )
            term_desc_table_html = term_desc_table.prettify()
            html_f.write('<div style="display:block;height:' + str( self.new_h + 3 ) + 'px;padding:0px;border:0px;margin:0px;">\n')
            html_f.write( term_desc_table_html )
            html_f.write('</div>\n')
            
        elif( self.num_extra_images >= 1 ):
#            html_f.write('<table><tr><td style="font-weight: bold;" id="' + self.name + '_extra_title">' + self.extra_title + '</td></tr></table>\n')
#            html_f.write('<img id="' + self.name + '_extra" src="' + self.extra_img_path + '" width="' + str( self.extra_img_width )  + '" height="' + str( self.new_h ) + '">\n')
            html_f.write('<table><tr><td style="font-weight: bold;" id="' + self.name + '_extra_title">' + self.extra_img_titles[0] + '</td></tr></table>\n')
            html_f.write('<img id="' + self.name + '_extra" src="' + self.extra_img_paths[0] + '" width="' + str( self.extra_img_widths[0] )  + '" height="' + str( self.new_h ) + '">\n')

        html_f.write('</div>\n')
        html_f.write('</div>\n')
        
        html_f.write('</div>\n')
        #html_f.write('<hr>\n')
        #html_f.write('<br>\n')
        #html_f.write('<br>\n')
        #html_f.write('<br>\n')

        
class metaGroup( community ):
    def __init__ ( self , name , communities , quant_data_type , all_gene_qd , _exp_ids , abs_images_dir , rel_images_dir , extra_annotations_dict, num_extra_annotations, new_h , heatmap_width_min, heatmap_height_min, heatmap_min , heatmap_max , search_words , info_string ):
        self.name = name
        self.abs_images_dir = abs_images_dir
        self.rel_images_dir = rel_images_dir
        self.extra_annotations_dict = extra_annotations_dict
        self.num_extra_annotations = num_extra_annotations
#        self.new_h = new_h
        self.new_h = new_h + 160
        self.heatmap_width_min = heatmap_width_min
        self.heatmap_height_min = heatmap_height_min
        self.heatmap_min = heatmap_min
        self.heatmap_max = heatmap_max
        self.search_words = search_words
        self.info_string = info_string
        
        self.quant_data_type = quant_data_type
        self.all_gene_qd = all_gene_qd
        self.exp_ids = _exp_ids
        self.type_label = "community"
        self.communities = communities
        self.communities.sort( key=lambda x: x.name )
        
        self.terms = [ community.name for community in communities ] # Need to have an attribute 'terms' for drawers and printers
        self.term_genes_dict = self.__make_community_genes_dict()  # Need to have an attribute 'term_genes_dict' for drawers and printers
        
        self.genes = list( set( [ gene for gene_set in [ community.genes for community in self.communities ] for gene in gene_set ] ) )
        self.genes_sorted = sorted( self.genes )
        
        
        my_upsetDrawer = upsetDrawer( self  )
        (self.upset_img_path , self.upset_img_width ) = my_upsetDrawer.draw_upset_plot()
                
        _etg_data = []
        for _e in self.exp_ids:
            for _com in self.communities:
                for _g in _com.genes:
                    if( ( _e , _g ) in self.all_gene_qd.index ):
                        _etg_data.append( ( _e , _com.name , _g , self.all_gene_qd.loc[ ( _e , _g ) ].iloc[0] , 1 ) )
                        
        _etg_df = pd.DataFrame.from_records( _etg_data , columns = [ 'FEA' , 'Community' , 'Gene' , 'QD' , 'Present' ] )
        
        # Note, we call this a gene_term_heatmap_df here, rather than a gene_community_heatmap_df, because that is what heatmapDrawer is expecting.
        self.gene_term_heatmap_df = _etg_df[ [ 'Community' , 'Gene' , 'Present' ] ].drop_duplicates().pivot_table(index='Community', columns='Gene', values='Present', fill_value=0).reindex( index=self.terms, columns = self.genes_sorted )
        self.gene_term_heatmap_fm_df = _etg_df[ [ 'Community' , 'Gene' , 'Present' ] ].drop_duplicates().pivot_table(index='Community', columns='Gene', values='Present').reindex( index=self.terms, columns = self.genes_sorted )
        self.gene_exp_heatmap_df = _etg_df[ [ 'FEA' , 'Gene' , 'QD' ] ].drop_duplicates().pivot_table(index='FEA', columns='Gene', values='QD', fill_value=0).reindex( index=self.exp_ids, columns = self.genes_sorted )
        self.gene_exp_heatmap_fm_df = _etg_df[ [ 'FEA' , 'Gene' , 'QD' ] ].drop_duplicates().pivot_table(index='FEA', columns='Gene', values='QD').reindex( index=self.exp_ids, columns = self.genes_sorted )
    
#        self.rows_cols = ( [] , [] )
#        if( len( self.genes ) > 50 and len( self.communities ) >= 3 ):
#            self.rows_cols = ( ( range( len( self.communities ) ) , self.gene_term_heatmap_df.sum() > len( self.communities )//3 ) )  
#        else:
#            self.rows_cols = ( ( range( len( self.communities ) ) , self.gene_term_heatmap_df.sum() > 1 ) )
#            
#        my_heatmapDrawer = heatmapDrawer( self )
#        
#        if( len(self.exp_ids) > 1 ):
#            (self.heatmap_img_paths_list , self.heatmap_img_widths_list , self.heatmap_img_titles_list ) = my_heatmapDrawer.draw_heatmaps(ylabel1 = 'Community')
#        else:
#            (self.heatmap_img_paths_list , self.heatmap_img_widths_list , self.heatmap_img_titles_list ) = my_heatmapDrawer.draw_heatmaps(ylabel1 = 'Community' , ylabel2 = '')
            
            
        self.rows_cols = ( [] , [] )
        if( len( self.genes ) > 50 and len( self.terms ) >= 3 and 
           (sum(self.gene_term_heatmap_df.sum() > 1) > sum(self.gene_term_heatmap_df.sum() > (len( self.communities )//3)))):
            self.rows_cols = ( ( range( len( self.communities ) ) , self.gene_term_heatmap_df.sum() > 1 ) )
            my_heatmapDrawer_full = heatmapDrawer( self )
            
            if( len(self.exp_ids) > 1 ):
                ( heatmap_img_paths_list_full , heatmap_img_widths_list_full  , heatmap_img_titles_list_full  ) = my_heatmapDrawer_full.draw_heatmaps( ylabel1='Community', postfix='full')
            else:
                ( heatmap_img_paths_list_full , heatmap_img_widths_list_full  , heatmap_img_titles_list_full  ) = my_heatmapDrawer_full.draw_heatmaps( ylabel1='Community' , ylabel2='', postfix='full' )
            
            
            self.rows_cols = ( ( range( len( self.communities ) ) , self.gene_term_heatmap_df.sum() > len( self.communities )//3 ) )  
            my_heatmapDrawer_truncated = heatmapDrawer( self )
            
            if( len(self.exp_ids) > 1 ):
                ( heatmap_img_paths_list_truncated , heatmap_img_widths_list_truncated , heatmap_img_titles_list_truncated ) = my_heatmapDrawer_truncated.draw_heatmaps( ylabel1='Community', postfix='truncated')
            else:
                ( heatmap_img_paths_list_truncated , heatmap_img_widths_list_truncated , heatmap_img_titles_list_truncated ) = my_heatmapDrawer_truncated.draw_heatmaps( ylabel1='Community', ylabel2='', postfix='truncated' )
                
                
            self.heatmap_img_paths_list = heatmap_img_paths_list_truncated + heatmap_img_paths_list_full
            self.heatmap_img_widths_list = heatmap_img_widths_list_truncated + heatmap_img_widths_list_full
            self.heatmap_img_titles_list = heatmap_img_titles_list_truncated + heatmap_img_titles_list_full
            
        else:
            self.rows_cols = ( ( range( len( self.communities ) ) , self.gene_term_heatmap_df.sum() > 1 ) )
            my_heatmapDrawer = heatmapDrawer( self )
        
            if( len(self.exp_ids) > 1 ):
                ( self.heatmap_img_paths_list , self.heatmap_img_widths_list , self.heatmap_img_titles_list ) = my_heatmapDrawer.draw_heatmaps( ylabel1 = 'Community' )
            else:
                ( self.heatmap_img_paths_list , self.heatmap_img_widths_list , self.heatmap_img_titles_list ) = my_heatmapDrawer.draw_heatmaps( ylabel1 = 'Community' , ylabel2 = '' )
            
        
        # Now extract the gene list that's shown in the heatmap:
        ( _ , s_cols ) = self.rows_cols
        self.included_genes = [ self.genes_sorted[ i ] for i in range( len( self.genes_sorted ) ) if s_cols.iloc[i]]


        #*****************************************************************************************
        # Now draw the Circos plot. This will sit with UpSet plot, but is created here because needs information from heatmap generation
        
        # Draw Circos plot
        my_circosDrawer = circosDrawer(self, rows_cols = (( range( len( self.communities ) ) , self.gene_term_heatmap_df.sum() > 0 )), metaGroupCircosDrawer = True)
        ( self.circos_img_path , self.circos_img_width ) = my_circosDrawer.draw_circos()
        
        #*****************************************************************************************                        

    def __make_community_genes_dict( self ):
        my_community_genes_dict = {}
        for community in self.communities:
            my_community_genes_dict[ community.name ] = community.genes
        return my_community_genes_dict

        
    def print_html( self , html_f , summary_html , first_print, backlink = '' ):
        
        if(first_print):
            html_f.write('<div style="height:110px" id="' + self.name +'"></div>')
        else:
            html_f.write('<div style="height:100px" id="' + self.name +'"></div>')
            html_f.write('<hr>\n')
            
        html_f.write('<button type="button" class="collapsible2"><table>\n')
        html_f.write('<tr><td></td></tr>\n')
        html_f.write('<tr>\n')
        html_f.write('<td><h5 class="title">' + self.name + '</h5></td>\n')
        #html_f.write('<td><h5 class="title">' + self.name + ' ' + self.info_string + '</h5></td>\n')
        #html_f.write('<td><button class="view-button" style="font-size:small;" onclick="document.location=\'' + summary_html + '\'">Communities summary</button></td>\n' )
        #if( backlink ):
        #    html_f.write('<td><button class="view-button" style="font-size:small;" onclick="document.location=\'' + backlink + '\'">Main page</button></td>\n' )
        html_f.write('</tr>\n')
        html_f.write('</table></button>\n')
        
        html_f.write('<div class="grid-container2">\n')
        
#        html_f.write('<div class="members2" style="max-height: ' + str( self.new_h + 25 ) + 'px;" >\n')
        html_f.write('<div class="members2" style="max-height: ' + str( self.new_h + 90 ) + 'px;" >\n')
        html_f.write('<table style="font-size:small;white-space: nowrap;">\n')
        
        if ( len( self.communities ) > 0 ):
            html_f.write('<tr>\n')
            html_f.write('<td>\n')
            html_f.write('<b>Member communities: </b>\n')
            html_f.write('</td>\n')
            html_f.write('<td>\n')
            html_f.write('</td>\n')
            html_f.write('</tr>\n')
            
            html_f.write('<tr>\n')
            html_f.write('<td>\n')
            html_f.write('</td>\n')
            html_f.write('<td>\n')
            html_f.write('</td>\n')
            html_f.write('</tr>\n')
            
            for com in self.communities:
                html_f.write('<tr>\n')
                html_f.write('<td>\n')
                html_f.write( '<a href="#' + com.name + '">' + com.name + '</a>\n' )
                html_f.write('</td>\n')
                html_f.write('<td>\n')
                html_f.write( com.top_term )
                html_f.write('</td>\n')
                html_f.write('</tr>\n')
        
        html_f.write('</table>\n')        
        html_f.write('</div>\n') 
        
        
#        html_f.write('<div class="spacer2a">\n')
#        html_f.write('</div>\n')
#        html_f.write('<div class="spacer2b">\n')
#        html_f.write('</div>\n')
        
        html_f.write('<div class="spacer2">\n')
        html_f.write('</div>\n')
        
        
#        html_f.write('<div class="heatmap2">\n')
#        html_f.write('<div style="width: 1200px;">\n')
        
#        html_f.write('<table><tr><td style="font-weight: bold;" id="' + self.name + '_heatmap_title">' + self.heatmap_img_titles_list[0]  + '</td></tr></table>\n')
#        html_f.write('<img id="' + self.name + '_heatmap" src="' + self.heatmap_img_paths_list[0] + '" width="' + str( self.heatmap_img_widths_list[0] )  + '" height="' + str( self.new_h ) + '">\n')
#        html_f.write('<div style="display:none;height:' + str( self.new_h + 3 ) + 'px;padding:0px;border:0px;margin:0px;" id="' +  self.name + '_heatmap_table_0">\n')
#        html_f.write('<table style="font-size:small;white-space: nowrap;">\n')
        
        html_f.write('<div class="upset2">\n')
        html_f.write('<div style="width: 1200px;">\n')
        html_f.write('<table><tr><td style="font-weight: bold;" id="' + self.name + '_upset_title">Circos plot</td></tr></table>\n')
        html_f.write('<img id="' + self.name + '_upset" src="' + self.circos_img_path + '" width="' + str(self.circos_img_width) + '" height="' + str(self.new_h) + '">\n')
        html_f.write('<div style="display:none;height:' + str( self.new_h + 3 ) + 'px;padding:0px;border:0px;margin:0px;" id="' +  self.name + '_upset_table_0">\n')
        html_f.write('<table style="font-size:small;white-space: nowrap;">\n')
        
        
        html_f.write('<tr>\n')
        html_f.write('<td>\n')
        html_f.write('<b>Gene</b>\n')
        html_f.write('</td>\n')
        html_f.write('<td>\n')
        html_f.write('<b>NCBI: Gene database</b>\n')
        html_f.write('</td>\n')
        html_f.write('<td>\n')
        html_f.write('<b>NCBI: PubMed database (Gene only)</b>\n')
        html_f.write('</td>\n')
        
        if(len(self.search_words) > 0):
            html_f.write('<td>\n')
            html_f.write('<b>NCBI: PubMed database (Gene and keywords)</b>\n')
            html_f.write('</td>\n')
        
        html_f.write('</tr>\n')
        
        for inc_gene in self.included_genes:
            ( ncbi_gene_href , pubmed_gene_href , pubmed_search_href , pubmed_print_string ) = build_searches( inc_gene , self.search_words )
            html_f.write('<tr>\n')
            
            html_f.write('<td>\n')
            html_f.write(inc_gene + '\n') 
            html_f.write('</td>\n')
            
            html_f.write('<td>\n')
            html_f.write('<a href = "' + ncbi_gene_href + '" target="_blank">' + inc_gene + ' (NCBI: Gene)</a>\n') 
            html_f.write('</td>\n')
            
#            html_f.write('<td>\n')
#            html_f.write('<a href = "' + ensembl_gene_href + '" target="_blank">' + inc_gene + ' (ENSEMBL)</a>\n') 
#            html_f.write('</td>\n')
            
            html_f.write('<td>\n')
            html_f.write('<a href = "' + pubmed_gene_href + '" target="_blank">' + inc_gene + ' (NCBI: PubMed)</a>\n') 
            html_f.write('</td>\n')
            
            if(len(self.search_words) > 0):
                html_f.write('<td>\n')
                html_f.write('<a href = "' + pubmed_search_href + '" target="_blank">' + pubmed_print_string + ' (NCBI: PubMed)</a>\n') 
                html_f.write('</td>\n')
            
            html_f.write('</tr>\n')
        
        
        
        html_f.write('</table>\n')
        html_f.write('<div style="height:2500px;"></div>\n')
        html_f.write('</div>\n')
        
        
        html_f.write('</div>\n')
        html_f.write('</div>\n')
        
        #heatmap_img_paths_array_as_str = ','.join( self.heatmap_img_paths_list )
        #heatmap_widths_array_as_str = ','.join( map( str , self.heatmap_img_widths_list ) )
        #heatmap_img_titles_array_as_str = ','.join( self.heatmap_img_titles_list )
        
        
        html_f.write('<div class="plot_buttons2">\n')
        
        html_f.write('<button class="view-button"  onclick="changeImg( \'' + self.name + '\' , \'upset\' , \'' + self.circos_img_path + '\' ,' + str(self.new_h) + ',\'' + str(self.circos_img_width) + '\' ,\'Circos plot\',1)">Circos plot</button>\n')
        
        html_f.write('<button class="view-button"  onclick="changeImg( \'' + self.name + '\' , \'upset\' , \'' + self.upset_img_path + '\' ,' + str(self.new_h) + ',\'' + str(self.upset_img_width) + '\' ,\'UpSet plot\',1)">UpSet plot</button>\n')
        
        
        
        if(len(self.heatmap_img_paths_list) == 3):
#            html_f.write('<button class="view-button"  onclick="changeImg( \'' + self.name + '\' , \'heatmap\' , \'' + self.heatmap_img_paths_list[0] + '\' ,' + str(self.new_h) + ',\'' + str(self.heatmap_img_widths_list[0]) + '\' ,\'' + self.heatmap_img_titles_list[0] + '\',1)">Heatmap A</button>\n')
#            html_f.write('<button class="view-button"  onclick="changeImg( \'' + self.name + '\' , \'heatmap\' , \'' + self.heatmap_img_paths_list[1] + '\' ,' + str(self.new_h) + ',\'' + str(self.heatmap_img_widths_list[1]) + '\' ,\'' + self.heatmap_img_titles_list[1] + '\',1)">Heatmap B</button>\n')
#            html_f.write('<button class="view-button"  onclick="changeImg( \'' + self.name + '\' , \'heatmap\' , \'' + self.heatmap_img_paths_list[2] + '\' ,' + str(self.new_h) + ',\'' + str(self.heatmap_img_widths_list[2]) + '\' ,\'' + self.heatmap_img_titles_list[2] + '\',1)">Heatmap C</button>\n')
        
            html_f.write('<button class="view-button"  onclick="changeImg( \'' + self.name + '\' , \'upset\' , \'' + self.heatmap_img_paths_list[0] + '\' ,' + str(self.new_h) + ',\'' + str(self.heatmap_img_widths_list[0]) + '\' ,\'' + self.heatmap_img_titles_list[0] + '\',1)">Heatmap A (' + self.quant_data_type +')</button>\n')
            html_f.write('<button class="view-button"  onclick="changeImg( \'' + self.name + '\' , \'upset\' , \'' + self.heatmap_img_paths_list[1] + '\' ,' + str(self.new_h) + ',\'' + str(self.heatmap_img_widths_list[1]) + '\' ,\'' + self.heatmap_img_titles_list[1] + '\',1)">Heatmap B (annotations x ' + self.quant_data_type +')</button>\n')
            html_f.write('<button class="view-button"  onclick="changeImg( \'' + self.name + '\' , \'upset\' , \'' + self.heatmap_img_paths_list[2] + '\' ,' + str(self.new_h) + ',\'' + str(self.heatmap_img_widths_list[2]) + '\' ,\'' + self.heatmap_img_titles_list[2] + '\',1)">Heatmap C (alphabetical)</button>\n')
        
        else:
            heatmap_img_paths_array_as_str_A = ','.join( [self.heatmap_img_paths_list[x] for x in [0,3]] )
            heatmap_widths_array_as_str_A = ','.join( map( str , [self.heatmap_img_widths_list[x] for x in [0,3]] ) )
            heatmap_img_titles_array_as_str_A = ','.join( [self.heatmap_img_titles_list[x] for x in [0,3]] )
            
            heatmap_img_paths_array_as_str_B = ','.join( [self.heatmap_img_paths_list[x] for x in [1,4]] )
            heatmap_widths_array_as_str_B = ','.join( map( str , [self.heatmap_img_widths_list[x] for x in [1,4]] ) )
            heatmap_img_titles_array_as_str_B = ','.join( [self.heatmap_img_titles_list[x] for x in [1,4]] )
            
            heatmap_img_paths_array_as_str_C = ','.join( [self.heatmap_img_paths_list[x] for x in [2,5]] )
            heatmap_widths_array_as_str_C = ','.join( map( str , [self.heatmap_img_widths_list[x] for x in [2,5]] ) )
            heatmap_img_titles_array_as_str_C = ','.join( [self.heatmap_img_titles_list[x] for x in [2,5]] )
            
#            html_f.write( '<button class="view-button"  onclick="changeImg( \'' + self.name + '\' , \'heatmap\' , \'' + heatmap_img_paths_array_as_str_A + '\' ,' + str( self.new_h ) + ',\'' + heatmap_widths_array_as_str_A + '\',\'' + heatmap_img_titles_array_as_str_A + '\',1)">Heatmap A</button>\n' )
#            html_f.write( '<button class="view-button"  onclick="changeImg( \'' + self.name + '\' , \'heatmap\' , \'' + heatmap_img_paths_array_as_str_B + '\' ,' + str( self.new_h ) + ',\'' + heatmap_widths_array_as_str_B + '\',\'' + heatmap_img_titles_array_as_str_B + '\',1)">Heatmap B</button>\n' )
#            html_f.write( '<button class="view-button"  onclick="changeImg( \'' + self.name + '\' , \'heatmap\' , \'' + heatmap_img_paths_array_as_str_C + '\' ,' + str( self.new_h ) + ',\'' + heatmap_widths_array_as_str_C + '\',\'' + heatmap_img_titles_array_as_str_C + '\',1)">Heatmap C</button>\n' )
#        
        
            html_f.write( '<button class="view-button"  onclick="changeImg( \'' + self.name + '\' , \'upset\' , \'' + heatmap_img_paths_array_as_str_A + '\' ,' + str( self.new_h ) + ',\'' + heatmap_widths_array_as_str_A + '\',\'' + heatmap_img_titles_array_as_str_A + '\',1)">Heatmap A (' + self.quant_data_type +')</button>\n')
            html_f.write( '<button class="view-button"  onclick="changeImg( \'' + self.name + '\' , \'upset\' , \'' + heatmap_img_paths_array_as_str_B + '\' ,' + str( self.new_h ) + ',\'' + heatmap_widths_array_as_str_B + '\',\'' + heatmap_img_titles_array_as_str_B + '\',1)">Heatmap B (annotations x ' + self.quant_data_type +')</button>\n')
            html_f.write( '<button class="view-button"  onclick="changeImg( \'' + self.name + '\' , \'upset\' , \'' + heatmap_img_paths_array_as_str_C + '\' ,' + str( self.new_h ) + ',\'' + heatmap_widths_array_as_str_C + '\',\'' + heatmap_img_titles_array_as_str_C + '\',1)">Heatmap C (alphabetical)</button>\n')
        
        
        html_f.write( '<button class="view-button"  onclick="changeTable( \'' + self.name + '\' , 0 , 1 ,\'upset\', true , \'Literature search\')">Literature search</button>\n' )

        html_f.write('</div>\n')
        
        
#        html_f.write('<div class="upset2">\n')
#        html_f.write('<div style="width: 1200px;">\n')
#        #html_f.write('<table><tr><td style="font-weight: bold;">UpSet plot</td></tr></table>\n')
#        #html_f.write('<img src="' + self.upset_img_path + '" width="' + str( self.upset_img_width )  + '" height="' + str( self.new_h ) + '">\n')
#        #html_f.write('<table><tr><td style="font-weight: bold;">Circos plot</td></tr></table>\n')
#        #html_f.write('<img src="' + self.circos_img_path + '" width="' + str( self.circos_img_width )  + '" height="' + str( self.new_h ) + '">\n')
#        
#        html_f.write('<table><tr><td style="font-weight: bold;" id="' + self.name + '_upset_title">Circos plot</td></tr></table>\n')
#        html_f.write('<img id="' + self.name + '_upset" src="' + self.circos_img_path + '" width="' + str(self.circos_img_width) + '" height="' + str(self.new_h) + '">\n')
#        
#        
#        html_f.write('</div>\n')
#        html_f.write('</div>\n')
        
        html_f.write('</div>\n')
        
        #html_f.write('<hr>\n')
        #html_f.write('<br>\n')
        #html_f.write('<br>\n')
        #html_f.write('<br>\n')

class etgContainer:
    def __init__( self , etg_name , etg_text_details , key_i_str ,  output_dir , relative_main_html , rel_images_dir, meta_communities , singleton_meta_communities , singleton_communities , new_h, 
                 silplot_img_path , silplot_img_width, silplot_img_height,
                 comparisonplot_oc_img_path , comparisonplot_oc_img_width, comparisonplot_oc_img_height,
                 comparisonplot_ji_img_path , comparisonplot_ji_img_width, comparisonplot_ji_img_height):
        self.name = etg_name
        self.text_details = etg_text_details
        self.key_i_str = key_i_str
        self.hyperlink = key_i_str + '_report.html'
        self.summary_hyperlink = key_i_str + '_communities_summary.html'
        self.csv_filename = key_i_str + '_report.csv'
        self.output_dir = output_dir
        self.relative_main_html = relative_main_html
        self.rel_images_dir = rel_images_dir
        self.meta_communities = meta_communities
        self.singleton_meta_communities = singleton_meta_communities
        self.singleton_communities = singleton_communities
        self.new_h = new_h
        self.silplot_img_path = silplot_img_path
        self.silplot_img_width = silplot_img_width
        self.silplot_img_height = silplot_img_height
        self.comparisonplot_oc_img_path = comparisonplot_oc_img_path
        self.comparisonplot_oc_img_width = comparisonplot_oc_img_width
        self.comparisonplot_oc_img_height = comparisonplot_oc_img_height
        self.comparisonplot_ji_img_path = comparisonplot_ji_img_path
        self.comparisonplot_ji_img_width = comparisonplot_ji_img_width
        self.comparisonplot_ji_img_height = comparisonplot_ji_img_height
        
    def print_csv(self):
        csv_f = open(self.output_dir + '/' + self.csv_filename , 'w')
        for mc in self.meta_communities:
            for bc in mc.communities:
                bc.print_csv(csv_f)
                
        for bc in self.singleton_meta_communities:
            bc.print_csv(csv_f)
            
        for sc in self.singleton_communities:
            sc.print_csv(csv_f)
            
        csv_f.close()
    
    def get_summary_hyperlink( self ):
        return self.summary_hyperlink # used by external code
    

    def print_html( self, etgContainers ):
        # Can we refactor this to pass the etgContainer object, rather than all of its attributes? The question is, how will this affect instances of summaryPrinter not called by an etgContainer?
        my_summaryPrinter = summaryPrinter( self.key_i_str , self.name + ': ' + self.text_details , self.output_dir , self.hyperlink , self.rel_images_dir, 
                                            self.meta_communities , self.singleton_meta_communities , self.singleton_communities , 
                                            self.silplot_img_path, self.silplot_img_width, self.silplot_img_height, 
                                            self.comparisonplot_oc_img_path, self.comparisonplot_oc_img_width, self.comparisonplot_oc_img_height,
                                            self.comparisonplot_ji_img_path, self.comparisonplot_ji_img_width, self.comparisonplot_ji_img_height, 
                                            self.relative_main_html, etgContainers )
        my_summaryPrinter.print_html()
        my_summaryPrinter.print_html('communities_silhouette')
        my_summaryPrinter.print_html('communities_paramcomparison_oc')
        my_summaryPrinter.print_html('communities_paramcomparison_ji')
        
        html_f = open( self.output_dir + '/' + self.hyperlink , 'w' )
        html_f.write("<!DOCTYPE html>\n")
        html_f.write("<html>\n")

        html_f.write("<head>\n")
        jSPrinter = javaScriptPrinter()
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
        html_f.write("  max-height: "+ str( self.new_h + 30 ) +"px;\n")
        html_f.write("  overflow: scroll;\n")
        html_f.write("  background-color: rgba(255, 255, 255, 0.8);\n")
        html_f.write("  text-align: left;\n")
        html_f.write("  padding: 15px;\n")
        html_f.write("  font-size: small;\n")
        html_f.write("}\n")
        
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
        
#        html_f.write(".grid-container2 {\n")
#        html_f.write("  display: grid;\n")
#        html_f.write("  grid-template-areas:\n")
#        html_f.write("    'members2 upset2 upset2 upset2 upset2 upset2'\n")
#        html_f.write("    'spacer2a plot_buttons2 plot_buttons2 plot_buttons2 plot_buttons2 plot_buttons2'\n")
#        html_f.write("    'spacer2b heatmap2 heatmap2 heatmap2 heatmap2 heatmap2';\n")
#        html_f.write("  grid-gap: 10px;\n")
#        html_f.write("  background-color: #DC143C;\n")
#        html_f.write("  padding: 10px;\n")
#        html_f.write("}\n\n")
        
        html_f.write(".grid-container2 {\n")
        html_f.write("  display: grid;\n")
        html_f.write("  grid-template-areas:\n")
        html_f.write("    'members2 upset2 upset2 upset2 upset2 upset2'\n")
        html_f.write("    'spacer2 plot_buttons2 plot_buttons2 plot_buttons2 plot_buttons2 plot_buttons2';\n")
        html_f.write("  grid-gap: 10px;\n")
        html_f.write("  background-color: #DC143C;\n")
        html_f.write("  padding: 10px;\n")
        html_f.write("}\n\n")    
#        
#        html_f.write(".members2 { grid-area: members2; }\n")
#        html_f.write(".heatmap2 { grid-area: heatmap2;\n") 
#        html_f.write("          overflow: scroll;}\n")
#        html_f.write(".spacer2a{ grid-area: spacer2a;}\n")
#        html_f.write(".plot_buttons2{ grid-area: plot_buttons2; }\n")
#        html_f.write(".spacer2b{ grid-area: spacer2b;}\n")
#        html_f.write(".upset2 { grid-area: upset2;\n")  
#        html_f.write("          overflow: scroll;}\n")
#        html_f.write("\n")
            
        html_f.write(".members2 { grid-area: members2;\n")
        html_f.write("          overflow: scroll;}\n")
        html_f.write(".spacer2{ grid-area: spacer2;}\n")
        html_f.write(".plot_buttons2{ grid-area: plot_buttons2; }\n")
        html_f.write(".upset2 { grid-area: upset2;\n")  
        html_f.write("          overflow: scroll;}\n")
        html_f.write("\n")         
                
#        html_f.write(".grid-container2 > div {\n")
#        html_f.write("  max-height: "+ str( self.new_h + 30) +"px;\n")
#        html_f.write("  overflow: scroll;\n")
#        html_f.write("  background-color: rgba(255, 255, 255, 0.8);\n")
#        html_f.write("  text-align: left;\n")
#        html_f.write("  padding: 15px;\n")
#        html_f.write("  font-size: small;\n")
#        html_f.write("}\n")
        
        html_f.write(".grid-container2 > div {\n")
        #html_f.write("  max-height: "+ str((self.new_h*2) + (30*3)) +"px;\n")
        html_f.write("  max-height: "+ str(self.new_h + 160 + 80) +"px;\n")
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
        html_f.write("  max-height: "+ str( self.new_h + 30 ) +"px;\n")
        html_f.write("  overflow: scroll;\n")
        html_f.write("  background-color: rgba(255, 255, 255, 0.8);\n")
        html_f.write("  text-align: left;\n")
        html_f.write("  padding: 15px;\n")
        html_f.write("  font-size: small;\n")
        html_f.write("}\n")
        
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
            
        #html_f.write(".content {\n")
        #html_f.write("display: none;\n")
        #html_f.write("}\n")
        
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
        
        html_f.write('<li><a href="' + self.relative_main_html + '">FEA term-set intersections</a></li>\n')
        html_f.write('<li class="dropdown">\n')
        html_f.write('<button class="dropbtnactive">Reports\n')
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
        html_f.write('<li class="dropdown">\n')
        html_f.write('<button class="dropbtn" onclick="document.location=\'' + self.key_i_str + '_communities_summary.html\'">Communities overview</button>\n')
        html_f.write('<div class="dropdown-content">\n')
        html_f.write('<a href="' + self.key_i_str + '_communities_summary.html">List of communities</a>\n')
        html_f.write('<a href="' + self.key_i_str + '_communities_silhouette.html">Silhouette plot</a>\n')
        #html_f.write('<a href="' + self.key_i_str + '_communities_paramcomparison.html">Graphical grid search of community detection parameters</a>\n')
        
        html_f.write('<div class="dropdownsub" style="width:450px">\n')
        html_f.write('<a href="javascript:;">Graphical grid search of community detection parameters</a>\n')
        html_f.write('<div class="dropdownsub-content" style="width:450px">\n')
        html_f.write('<a href="' + self.key_i_str + '_communities_paramcomparison_oc.html">Graphical grid search of community detection parameters (OC)</a>\n')
        html_f.write('<a href="' + self.key_i_str + '_communities_paramcomparison_ji.html">Graphical grid search of community detection parameters (JI)</a>\n')
        html_f.write('</div>\n')
        html_f.write('</div>\n')
        
        html_f.write('</div>\n')
        html_f.write('</li> \n')
        
        
        html_f.write('<li class="dropdown">\n')
        html_f.write('<button class="dropbtnactive" onclick="document.location=\'' + self.hyperlink + '\'">Full report</button>\n')
        html_f.write('<div class="dropdown-content">\n')
        
        if(len(self.meta_communities)==0):
            html_f.write('<a href="#">Meta communities</a>\n')
        else:
            html_f.write('<div class="dropdownsub" style="width:300px">\n')
            html_f.write('<a href="' + self.hyperlink + '#' + self.meta_communities[0].name + '">Meta communities</a>\n')
            html_f.write('<div class="dropdownsub-content">\n')
                         
            for mg in self.meta_communities:
                html_f.write('<div class="dropdownsubsub" style="width:300px">\n')
                html_f.write('<a href="' + self.hyperlink + '#' + mg.name + '">' + mg.name + '</a>\n' )
                
                html_f.write('<div class="dropdownsubsub-content" style="width:600px;max-height:200px;overflow:scroll;">\n')
                for bc in mg.communities:
                    html_f.write('<a href="' + self.hyperlink + '#' + bc.name + '">' + bc.name + ' ' + bc.top_term + '</a>\n')
                
                html_f.write('</div>\n')
                    
                html_f.write('</div>\n')
            
            html_f.write('</div>\n')
            html_f.write('</div>\n')
        
        
        if(len(self.singleton_meta_communities)==0):
            html_f.write('<a href="javascript:;">Communities</a>\n')
        else:
            html_f.write('<div class="dropdownsub" style="width:300px">\n')
            html_f.write('<a href="' + self.hyperlink + '#' + self.singleton_meta_communities[0].name + '">Communities</a>\n')
            html_f.write('<div class="dropdownsub-content" style="width:600px;max-height:200px;overflow:scroll;">\n')
            for bc in self.singleton_meta_communities:
                html_f.write('<a href="' + self.hyperlink + '#' + bc.name + '">' + bc.name + ' ' + bc.top_term + '</a>\n')
            
            html_f.write('</div>\n')
            html_f.write('</div>\n')         
        
        if(len(self.singleton_communities)==0):
            html_f.write('<a href="#">Terms</a>\n')
        else:
            html_f.write('<div class="dropdownsub" style="width:300px">\n')
            html_f.write('<a href="' + self.hyperlink + '#' + self.singleton_communities[0].name + '">Terms</a>\n')
            html_f.write('<div class="dropdownsub-content" style="width:600px;max-height:200px;overflow:scroll;">\n')
            for sc in self.singleton_communities:
                if( sc.name == sc.all_term_defs_dict[ sc.name ] ):
                    html_f.write('<a href="' + self.hyperlink + '#' + sc.name + '">' + sc.name + '</a>\n' )
                else:
                    html_f.write('<a href="' + self.hyperlink + '#' + sc.name + '">' + sc.name + ' - ' + sc.all_term_defs_dict[ sc.name ]  + '</a>\n' )
            html_f.write('</div>\n')
            html_f.write('</div>\n')  
        
        html_f.write('</div>\n')
        html_f.write('</li>\n')
        
        
        html_f.write('<li class="rightlink"><a style="color:white;">' + self.name + ': ' + self.text_details + '</a></li>\n')
        html_f.write('</ul>\n')
        html_f.write('</div>\n')
        html_f.write('</div>\n')
            
        
        first_print = True
        for mc in self.meta_communities:
            mc.print_html( html_f , self.summary_hyperlink , first_print, backlink = self.relative_main_html )
            first_print = False
            
            for bc in mc.communities:
                bc.print_html( html_f , self.summary_hyperlink , first_print, backlink = self.relative_main_html )
                
        for bc in self.singleton_meta_communities:
            bc.print_html( html_f , self.summary_hyperlink , first_print, backlink = self.relative_main_html )
            first_print = False
            
        for sc in self.singleton_communities:
            sc.print_html( html_f , self.summary_hyperlink , first_print, backlink = self.relative_main_html )
            first_print = False

        jSPrinter.print_html_for_event_listeners( html_f )
        html_f.write("</body>\n")
        html_f.write("</html>\n")
        html_f.close()


class summaryPrinter:
    #Can we refactor this? See note and query in etgContainer object...
    def __init__( self , summary_id , summary_title , output_dir , report_html , rel_images_dir, meta_communities , singleton_meta_communities , singleton_communities , 
                  silplot_img_path, silplot_img_width, silplot_img_height, 
                  comparisonplot_oc_img_path, comparisonplot_oc_img_width, comparisonplot_oc_img_height,
                  comparisonplot_ji_img_path, comparisonplot_ji_img_width, comparisonplot_ji_img_height, 
                  backlink = '' , etgContainers = [] ):
        self.summary_id = summary_id
        self.summary_title = summary_title
        self.output_dir = output_dir
        self.report_html = report_html
        self.rel_images_dir = rel_images_dir
        self.meta_communities = meta_communities
        self.singleton_meta_communities = singleton_meta_communities
        self.singleton_communities = singleton_communities
        self.silplot_img_path = silplot_img_path
        self.silplot_img_width = silplot_img_width
        self.silplot_img_height = silplot_img_height
        self.comparisonplot_oc_img_path = comparisonplot_oc_img_path
        self.comparisonplot_oc_img_width = comparisonplot_oc_img_width
        self.comparisonplot_oc_img_height = comparisonplot_oc_img_height
        self.comparisonplot_ji_img_path = comparisonplot_ji_img_path
        self.comparisonplot_ji_img_width = comparisonplot_ji_img_width
        self.comparisonplot_ji_img_height = comparisonplot_ji_img_height
        self.backlink = backlink
        self.etgContainers = etgContainers
        
    
    def print_html( self , summary_type="communities_summary" ):
        html_f = open( self.output_dir + '/' + self.summary_id + '_' + summary_type + '.html', 'w' )
        html_f.write("<!DOCTYPE html>\n")
        html_f.write("<html>\n")

        html_f.write("<head>\n")
        
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
               
        html_f.write(".grid-container {\n")
        html_f.write("  display: grid;\n")
        html_f.write("  grid-template-areas:\n")
        html_f.write("    'report_title'\n")
        html_f.write("    'meta_communities'\n")
        html_f.write("    'singleton_meta_communities'\n")
        html_f.write("    'singleton_communities';\n")
        html_f.write("  grid-gap: 10px;\n")
        html_f.write("  background-color: #0aa8a8;\n")
        html_f.write("  padding: 10px;\n")
        html_f.write("}\n")
        
        html_f.write(".report_title{ grid-area: report_title; }\n")
        html_f.write(".meta_communities { grid-area: meta_communities;\n")
        html_f.write("                    overflow: scroll;}\n")
        html_f.write(".singleton_meta_communities { grid-area: singleton_meta_communities;\n")
        html_f.write("                         overflow: scroll;}\n")
        html_f.write(".singleton_communities { grid-area: singleton_communities;\n")
        html_f.write("                              overflow: scroll;}\n")       
        
        html_f.write(".grid-container > div {\n")
        html_f.write("  max-height: 760px;\n")
        html_f.write("  overflow: scroll;\n")
        html_f.write("  background-color: rgba(255, 255, 255, 0.8);\n")
        html_f.write("  text-align: left;\n")
        html_f.write("  padding: 15px;\n")
        html_f.write("  font-size: small;\n")
        html_f.write("  margin:0;\n")
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
        if(not(self.backlink=='')):
            html_f.write('<li><a href="' + self.backlink + '">FEA term-set intersections</a></li>\n')
            html_f.write('<li class="dropdown">\n')
            html_f.write('<button class="dropbtnactive">Reports\n')
            html_f.write('</button>\n')
            html_f.write('<div class="dropdown-content">\n')
            for etgContainer in self.etgContainers:
                html_f.write('<a href="' + etgContainer.get_summary_hyperlink() + '">' + etgContainer.name + ': ' + etgContainer.text_details + '</a>\n')
            html_f.write('</div>\n')
            html_f.write('</li>\n')
        html_f.write('</ul>\n')
        html_f.write('</div>\n')
    
    
        html_f.write('<div>\n')
        html_f.write('<ul class="subnav">\n')
        html_f.write('<li class="dropdown">\n')
        html_f.write('<button class="dropbtnactive" onclick="document.location=\'' + self.summary_id + '_communities_summary.html\'">Communities overview</button>\n')
        html_f.write('<div class="dropdown-content">\n')
        html_f.write('<a href="' + self.summary_id + '_communities_summary.html">List of communities</a>\n')
        html_f.write('<a href="' + self.summary_id + '_communities_silhouette.html">Silhouette plot</a>\n')
        #html_f.write('<a href="' + self.summary_id + '_communities_paramcomparison.html">Graphical grid search of community detection parameters</a>\n')
        
        html_f.write('<div class="dropdownsub" style="width:450px">\n')
        html_f.write('<a href="javascript:;">Graphical grid search of community detection parameters</a>\n')
        html_f.write('<div class="dropdownsub-content" style="width:450px">\n')
        html_f.write('<a href="' + self.summary_id + '_communities_paramcomparison_oc.html">Graphical grid search of community detection parameters (OC)</a>\n')
        html_f.write('<a href="' + self.summary_id + '_communities_paramcomparison_ji.html">Graphical grid search of community detection parameters (JI)</a>\n')
        html_f.write('</div>\n')
        html_f.write('</div>\n')
        
        html_f.write('</div>\n')
        html_f.write('</li> \n')
        
        
        html_f.write('<li class="dropdown">\n')
        html_f.write('<button class="dropbtn" onclick="document.location=\'' + self.report_html + '\'">Full report</button>\n')
        html_f.write('<div class="dropdown-content">\n')
        
        if(len(self.meta_communities)==0):
            html_f.write('<a href="#">Meta communities</a>\n')
        else:
            html_f.write('<div class="dropdownsub" style="width:300px">\n')
            html_f.write('<a href="' + self.report_html + '#' + self.meta_communities[0].name + '">Meta communities</a>\n')
            html_f.write('<div class="dropdownsub-content">\n')
                         
            for mg in self.meta_communities:
                html_f.write('<div class="dropdownsubsub" style="width:300px">\n')
                html_f.write('<a href="' + self.report_html + '#' + mg.name + '">' + mg.name + '</a>\n' )
                
                html_f.write('<div class="dropdownsubsub-content" style="width:600px;max-height:200px;overflow:scroll;">\n')
                for bc in mg.communities:
                    html_f.write('<a href="' + self.report_html + '#' + bc.name + '">' + bc.name + ' ' + bc.top_term + '</a>\n')
                
                html_f.write('</div>\n')
                    
                html_f.write('</div>\n')
            
            html_f.write('</div>\n')
            html_f.write('</div>\n')
        
        
        if(len(self.singleton_meta_communities)==0):
            html_f.write('<a href="javascript:;">Communities</a>\n')
        else:
            html_f.write('<div class="dropdownsub" style="width:300px">\n')
            html_f.write('<a href="' + self.report_html + '#' + self.singleton_meta_communities[0].name + '">Communities</a>\n')
            html_f.write('<div class="dropdownsub-content" style="width:600px;max-height:200px;overflow:scroll;">\n')
            for bc in self.singleton_meta_communities:
                html_f.write('<a href="' + self.report_html + '#' + bc.name + '">' + bc.name + ' ' + bc.top_term + '</a>\n')
            
            html_f.write('</div>\n')
            html_f.write('</div>\n')         
        
        if(len(self.singleton_communities)==0):
            html_f.write('<a href="#">Terms</a>\n')
        else:
            html_f.write('<div class="dropdownsub" style="width:300px">\n')
            html_f.write('<a href="' + self.report_html + '#' + self.singleton_communities[0].name + '">Terms</a>\n')
            html_f.write('<div class="dropdownsub-content" style="width:600px;max-height:200px;overflow:scroll;">\n')
            for sc in self.singleton_communities:
                if( sc.name == sc.all_term_defs_dict[ sc.name ] ):
                    html_f.write('<a href="' + self.report_html + '#' + sc.name + '">' + sc.name + '</a>\n' )
                else:
                    html_f.write('<a href="' + self.report_html + '#' + sc.name + '">' + sc.name + ' - ' + sc.all_term_defs_dict[ sc.name ]  + '</a>\n' )
            html_f.write('</div>\n')
            html_f.write('</div>\n')  
        
        html_f.write('</div>\n')
        html_f.write('</li>\n')
        
        
        html_f.write('<li class="rightlink"><a style="color:white;">' + self.summary_title + '</a></li>\n')
        html_f.write('</ul>\n')
        html_f.write('</div>\n')
        html_f.write('</div>\n')
        
        
        if(summary_type == "communities_summary"):
            html_f.write('<div class="subtitlebanner">\n')
            html_f.write('<li><a style="color:black;">List of communities</a></li>\n')
            html_f.write('</div>\n')
            html_f.write('<div class="grid-container">\n')
            
            
            html_f.write('<div class="meta_communities">\n')
            html_f.write('<table>\n')
            html_f.write('<tr><td><b>Meta communities</b></td><td></td><td></td></tr>\n' )
            for mg in self.meta_communities:
                html_f.write('<tr><td><a href="' + self.report_html + '#' + mg.name + '">' + mg.name + '</a></td><td><a href="' + self.report_html + '#' + mg.communities[0].name + '">' + mg.communities[0].name + '</a></td><td>' + mg.communities[0].top_term + '</td></tr>\n' )
                
                for bc in mg.communities[ 1 : len(mg.communities) ]:
                    html_f.write('<tr><td></td><td><a href="' + self.report_html + '#' + bc.name + '">' + bc.name + '</a></td><td>' + bc.top_term + '</td></tr>\n' )
                html_f.write('<tr><td></td><td></td><td></td></tr>\n' )
                
            html_f.write('</table>\n')
            html_f.write('</div>\n')
            
            html_f.write('<div class="singleton_meta_communities">\n')
            html_f.write('<table>\n')
            html_f.write('<tr><td><b>Communities</b></td><td></td></tr>\n' )
            for bc in self.singleton_meta_communities:
                html_f.write('<tr><td><a href="' + self.report_html + '#' + bc.name + '">' + bc.name + '</a></td><td>' + bc.top_term + '</td></tr>\n' )
                html_f.write('<tr><td></td><td></td></tr>\n' )
            
            html_f.write('</table>\n')    
            html_f.write('</div>\n')
            
            html_f.write('<div class="singleton_communities">\n')
            html_f.write('<table>\n')
            html_f.write('<tr><td><b>Terms</b></td></tr>\n' )
            for sc in self.singleton_communities:
                if( sc.name == sc.all_term_defs_dict[ sc.name ] ):
                    html_f.write('<tr><td><a href="' + self.report_html + '#' + sc.name + '">' + sc.name + '</a></td></tr>\n' )
                else:
                    html_f.write('<tr><td><a href="' + self.report_html + '#' + sc.name + '">' + sc.name + ' - ' + sc.all_term_defs_dict[ sc.name ]  + '</a></td></tr>\n' )
                html_f.write('<tr><td></td></tr>\n' )
            html_f.write('</table>\n')
            html_f.write('</div>\n')
            
            html_f.write('</div>\n')
            
        elif(summary_type == "communities_paramcomparison_oc"):
            html_f.write('<div class="subtitlebanner">\n')
            html_f.write('<li><a style="color:black;">Graphical grid search of community detection parameters (OC)</a></li>\n')
            html_f.write('</div>\n')
            html_f.write('<div class="grid-container">\n')
            html_f.write('<div class="figure">\n')
            html_f.write('<img src="' + self.comparisonplot_oc_img_path + '" width="' + str(self.comparisonplot_oc_img_width) + '" height="' + str(self.comparisonplot_oc_img_height) + '">\n')
            #html_f.write('<img src="' + self.rel_images_dir + 'sil_violinplots.svg">\n')
            html_f.write('</div>\n')
            html_f.write('</div>\n')
            
        
        elif(summary_type == "communities_paramcomparison_ji"):
            html_f.write('<div class="subtitlebanner">\n')
            html_f.write('<li><a style="color:black;">Graphical grid search of community detection parameters (JI)</a></li>\n')
            html_f.write('</div>\n')
            html_f.write('<div class="grid-container">\n')
            html_f.write('<div class="figure">\n')
            html_f.write('<img src="' + self.comparisonplot_ji_img_path + '" width="' + str(self.comparisonplot_ji_img_width) + '" height="' + str(self.comparisonplot_ji_img_height) + '">\n')
            #html_f.write('<img src="' + self.rel_images_dir + 'sil_violinplots.svg">\n')
            html_f.write('</div>\n')
            html_f.write('</div>\n')
            
        elif(summary_type == "communities_silhouette"):
            html_f.write('<div class="subtitlebanner">\n')
            html_f.write('<li><a style="color:black;">Silhouette plot</a></li>\n')
            html_f.write('</div>\n')
            html_f.write('<div class="grid-container">\n')
            html_f.write('<div class="figure">\n')
            html_f.write('<img src="' + self.silplot_img_path + '" width="' + str(self.silplot_img_width) + '" height="' + str(self.silplot_img_height) + '">\n')
            html_f.write('</div>\n')
            html_f.write('</div>\n')
        
        
        html_f.write("</body>\n")
        html_f.write("</html>\n")
        html_f.close()

class javaScriptPrinter:
    def __init__(self):
        pass
    
    def print_html( self , html_f ):
        html_f.write("<script>\n")
        html_f.write("function changeImg( stub , postfix , srcfiles_str , h , widths_str , titles_str , n_tables ) {\n")
        html_f.write('  var imgID = stub + "_" + postfix\n')
        html_f.write('  var titleID = stub + "_" + postfix + "_title"\n')
        html_f.write('  var srcfiles = srcfiles_str.split(",");\n')
        html_f.write('  var widths = widths_str.split(",");\n')
        html_f.write('  var titles = titles_str.split(",");\n')
     
        html_f.write('  var srcfilenames = []; \n')
        html_f.write('  var si;\n')
        html_f.write('  for (si = 0; si < srcfiles.length; si++) {\n')
        html_f.write('      var path_as_list = srcfiles[ si ].split("/");\n')
        html_f.write('      srcfilenames.push(path_as_list[ path_as_list.length - 1 ]);\n')
        html_f.write('  }\n')
        
        html_f.write('  var current_srcfilename_path_as_list = document.getElementById(imgID).src.split("/");\n')
        html_f.write('  var current_srcfilename = current_srcfilename_path_as_list[ current_srcfilename_path_as_list.length - 1 ];\n')

        html_f.write('  var i = ( srcfilenames.indexOf( current_srcfilename ) + 1 ) % srcfiles.length;\n')        
        html_f.write('  var srcfile = srcfiles[ i ];\n')
        html_f.write('  var w = widths[ i ];\n')
        html_f.write('  var title = titles[ i ];\n')
        
        html_f.write("  document.getElementById(titleID).innerHTML = title;\n")
        html_f.write("  document.getElementById(imgID).src = srcfile;\n")
        html_f.write("  document.getElementById(imgID).height = h;\n")
        html_f.write("  document.getElementById(imgID).width = w;\n")
        html_f.write('  document.getElementById(imgID).style.display = "inline";\n')
        
        html_f.write("    var i;\n")
        html_f.write("    for (i = 0; i < n_tables; i++) {\n")
        html_f.write('      var table_ID = stub + "_" + postfix + "_table_" + i;\n')
        html_f.write('      document.getElementById(table_ID).style.display = "none";\n')
        html_f.write("    }\n")
        
        html_f.write("}\n")
        html_f.write("</script>\n")
        
        html_f.write("<script>\n")
        html_f.write("function changeTable( stub , table_i , n_tables , postfix , images , title ) {\n")
          
        html_f.write('  if( images ){\n')
        html_f.write('    var imgID = stub + "_" + postfix\n')
        html_f.write('    document.getElementById(imgID).style.display = "none";\n')
        html_f.write('    document.getElementById(imgID).src = "";\n')
        html_f.write('    var titleID = stub + "_" + postfix + "_title"\n')
        html_f.write('    document.getElementById(titleID).innerHTML = title;\n')
        html_f.write('  }\n')
              
        html_f.write("  var i;\n")
        html_f.write("  for (i = 0; i < n_tables; i++) {\n")
        html_f.write('    var table_ID = stub + "_" + postfix + "_table_" + i;\n')
            
        html_f.write("    if( i != table_i ){\n")
        html_f.write('      document.getElementById(table_ID).style.display = "none";\n') 
        html_f.write("    }\n")
        html_f.write("    else{\n")
        html_f.write('      document.getElementById(table_ID).style.display = "block";\n') 
        html_f.write("    }\n")
        html_f.write("  }\n")
        html_f.write("}\n")
        html_f.write("</script>\n")
        
    def print_html_for_event_listeners( self , html_f ):
        html_f.write("<script>\n")
        html_f.write('var coll = document.getElementsByClassName("collapsible");\n')
        html_f.write('var i;\n')
        html_f.write('for (i = 0; i < coll.length; i++) {\n')
        html_f.write('  coll[i].addEventListener("click", function() {\n')
        html_f.write('    var content = this.nextElementSibling;\n')
        html_f.write('    if (content.style.display == "grid" || content.style.display == "") {\n')
        html_f.write('      content.style.display = "none";\n')
        #html_f.write('      content.nextElementSibling.style.display = "none";\n')
        html_f.write('    } else {\n')
        html_f.write('      content.style.display = "grid";\n')
        #html_f.write('      content.nextElementSibling.style.display = "grid";\n')
        html_f.write('    }\n')
        html_f.write(' });\n')
        html_f.write('}\n')
        html_f.write("</script>\n")
        
        html_f.write("<script>\n")
        html_f.write('var coll = document.getElementsByClassName("collapsible2");\n')
        html_f.write('var i;\n')
        html_f.write('for (i = 0; i < coll.length; i++) {\n')
        html_f.write('  coll[i].addEventListener("click", function() {\n')
        html_f.write('    var content = this.nextElementSibling;\n')
        html_f.write('    if (content.style.display == "grid" || content.style.display == "") {\n')
        html_f.write('      content.style.display = "none";\n')
        #html_f.write('      content.nextElementSibling.style.display = "none";\n')
        html_f.write('    } else {\n')
        html_f.write('      content.style.display = "grid";\n')
        #html_f.write('      content.nextElementSibling.style.display = "grid";\n')
        html_f.write('    }\n')
        html_f.write(' });\n')
        html_f.write('}\n')
        html_f.write("</script>\n")
        
        html_f.write("<script>\n")
        html_f.write('var coll = document.getElementsByClassName("collapsible3a");\n')
        html_f.write('var i;\n')
        html_f.write('for (i = 0; i < coll.length; i++) {\n')
        html_f.write('  coll[i].addEventListener("click", function() {\n')
        html_f.write('    var content = this.nextElementSibling;\n')
        html_f.write('    if (content.style.display == "grid" || content.style.display == "") {\n')
        html_f.write('      content.style.display = "none";\n')
        #html_f.write('      content.nextElementSibling.style.display = "none";\n')
        html_f.write('    } else {\n')
        html_f.write('      content.style.display = "grid";\n')
        #html_f.write('      content.nextElementSibling.style.display = "grid";\n')
        html_f.write('    }\n')
        html_f.write(' });\n')
        html_f.write('}\n')
        html_f.write("</script>\n")
        
        html_f.write("<script>\n")
        html_f.write('var coll = document.getElementsByClassName("collapsible3b");\n')
        html_f.write('var i;\n')
        html_f.write('for (i = 0; i < coll.length; i++) {\n')
        html_f.write('  coll[i].addEventListener("click", function() {\n')
        #html_f.write('    var content = this.nextElementSibling.nextElementSibling;\n')
        html_f.write('    var content = this.nextElementSibling;\n')
        html_f.write('    if (content.style.display == "grid" || content.style.display == "") {\n')
        html_f.write('      content.style.display = "none";\n')
        html_f.write('      content.nextElementSibling.style.display = "none";\n')
        #html_f.write('      content.nextElementSibling.nextElementSibling.style.display = "none";\n')
        html_f.write('    } else {\n')
        html_f.write('      content.style.display = "grid";\n')
        html_f.write('      content.nextElementSibling.style.display = "grid";\n')
        #html_f.write('      content.nextElementSibling.nextElementSibling.style.display = "grid";\n')
        html_f.write('    }\n')
        html_f.write(' });\n')
        html_f.write('}\n')
        html_f.write("</script>\n")
        


# END CLASSES *****************************************************************


# EXTRA CLASS ***************************************************************
# This class enables use of the heatmapDrawer without having to first construct
# a community. This is useful for when user wants to draw a split heatmap ouside
# of the context of summarising enrichment results.
        
class heatmapDrawerUser:
    
    def __init__ (self, name, terms, quant_data_type, all_gene_qd, exp_ids, term_genes_dict, ylabel1, ylabel2, 
                  extra_annotations_dict, num_extra_annotations, new_h, heatmap_width_min, heatmap_height_min, heatmap_min, heatmap_max,
                  abs_images_dir='', rel_images_dir=''):
        self.name = name
        self.terms = terms
        self.quant_data_type = quant_data_type
        self.all_gene_qd = all_gene_qd
        self.exp_ids = exp_ids
        self.term_genes_dict = term_genes_dict
        self.ylabel1 = ylabel1
        self.ylabel2 = ylabel2
        self.extra_annotations_dict = extra_annotations_dict
        self.num_extra_annotations = num_extra_annotations
        self.genes = self.__make_unique_gene_list()
        self.genes_sorted = sorted(self.genes)
        self.new_h = new_h
        self.heatmap_width_min = heatmap_width_min
        self.heatmap_height_min = heatmap_height_min
        self.heatmap_min = heatmap_min
        self.heatmap_max = heatmap_max
        self.abs_images_dir = abs_images_dir
        self.rel_images_dir = rel_images_dir
        
        _etg_data = []
        for _e in self.exp_ids:
            for _t in self.terms:
                for _g in sorted(self.term_genes_dict[ _t ]):
                    if( ( _e , _g ) in self.all_gene_qd.index ):
                        _etg_data.append( ( _e , _t , _g , self.all_gene_qd.loc[ ( _e , _g ) ][0] , 1 ) )
                        
        self.etg_df = pd.DataFrame.from_records( _etg_data , columns = [ 'FEA' , 'Term' , 'Gene' , 'QD' , 'Present' ] )
        
        self.gene_term_heatmap_df = self.etg_df[ [ 'Term' , 'Gene' , 'Present' ] ].drop_duplicates().pivot_table(index='Term', columns='Gene', values='Present', fill_value=0).reindex( index=self.terms, columns = self.genes_sorted )
        self.gene_term_heatmap_fm_df = self.etg_df[ [ 'Term' , 'Gene' , 'Present' ] ].drop_duplicates().pivot_table(index='Term', columns='Gene', values='Present').reindex( index=self.terms, columns = self.genes_sorted )
        self.gene_exp_heatmap_df = self.etg_df[ [ 'FEA' , 'Gene' , 'QD' ] ].drop_duplicates().pivot_table(index='FEA', columns='Gene', values='QD', fill_value=0).reindex( index=self.exp_ids, columns = self.genes_sorted )
        self.gene_exp_heatmap_fm_df = self.etg_df[ [ 'FEA' , 'Gene' , 'QD' ] ].drop_duplicates().pivot_table(index='FEA', columns='Gene', values='QD').reindex( index=self.exp_ids, columns = self.genes_sorted )
        
        self.rows_cols = ( [] , [] )
        
    def __make_unique_gene_list(self):
        my_genes = list(set([gene for gene_set in list(self.term_genes_dict.values()) for gene in gene_set]))
        return my_genes
    

    def drawHeatmap(self, condense_heatmap=False, trim_labels=True):
        
#        # Draw Heatmap plot
#        _etg_data = []
#        for _e in self.exp_ids:
#            for _t in self.terms:
#                for _g in sorted(self.term_genes_dict[ _t ]):
#                    if( ( _e , _g ) in self.all_gene_qd.index ):
#                        _etg_data.append( ( _e , _t , _g , self.all_gene_qd.loc[ ( _e , _g ) ][0] , 1 ) )
#                        
#        self.etg_df = pd.DataFrame.from_records( _etg_data , columns = [ 'Experiment' , 'Term' , 'Gene' , 'QD' , 'Present' ] )
#        
#        self.gene_term_heatmap_df = self.etg_df[ [ 'Term' , 'Gene' , 'Present' ] ].drop_duplicates().pivot( 'Term' , 'Gene' , 'Present' ).fillna( 0 ).reindex( index=self.terms, columns = self.genes_sorted )
#        self.gene_term_heatmap_fm_df = self.etg_df[ [ 'Term' , 'Gene' , 'Present' ] ].drop_duplicates().pivot( 'Term' , 'Gene' , 'Present' ).reindex( index=self.terms, columns = self.genes_sorted )
#        self.gene_exp_heatmap_df = self.etg_df[ [ 'Experiment' , 'Gene' , 'QD' ] ].drop_duplicates().pivot( 'Experiment' , 'Gene' , 'QD' ).fillna( 0 ).reindex( index=self.exp_ids, columns = self.genes_sorted )
#        self.gene_exp_heatmap_fm_df = self.etg_df[ [ 'Experiment' , 'Gene' , 'QD' ] ].drop_duplicates().pivot( 'Experiment' , 'Gene' , 'QD' ).reindex( index=self.exp_ids, columns = self.genes_sorted )
#        
#        self.rows_cols = ( [] , [] )
        if(condense_heatmap):
            if( len( self.genes ) > 25 and len( self.terms ) >= 4 ):
                self.rows_cols = ( ( range( len( self.terms ) ) , self.gene_term_heatmap_df.sum() > len( self.terms )//4 ) )  
            else:
                self.rows_cols = ( ( range( len( self.terms ) ) , self.gene_term_heatmap_df.sum() > 0 ) )
        else:
            self.rows_cols = ( ( range( len( self.terms ) ) , self.gene_term_heatmap_df.sum() > 0 ) )
            
        my_heatmapDrawer = heatmapDrawer(self, trim_terms=trim_labels)
        
        (self.heatmap_img_paths_list, self.heatmap_img_widths_list, self.heatmap_img_titles_list) = my_heatmapDrawer.draw_heatmaps(ylabel1=self.ylabel1, ylabel2=self.ylabel2)
        
        