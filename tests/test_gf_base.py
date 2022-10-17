#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: avigailtaylor
"""

import math
import os
import shutil
import unittest
from fractions import Fraction

from genefeast import gf_base


def compare_dicts(dict1, dict2):
    return (set(dict1.keys()) == set(dict2.keys())) and all([dict1[k] == dict2[k] for k in dict1.keys()])

class TestBaseFunctions(unittest.TestCase):

    def setUp(self):
        try:
            os.remove('test')
        except:
            pass
        
        try:
            shutil.rmtree('test')
        except:
            pass
        
        
    def test_get_output_dir_status_0(self):
        os.makedirs('test')
        
        (status, message) = gf_base.get_output_dir_status('test')
        self.assertEqual(status, 0)
        
        shutil.rmtree('test')
        

    def test_get_output_dir_message_0(self):
        os.makedirs('test')
        
        (status, message) = gf_base.get_output_dir_status('test')
        self.assertEqual(message, 'Output directory already exists and is empty. '
                            'Proceeding with analysis now...')
        
        shutil.rmtree('test')
    

    def test_get_output_dir_status_1(self):
        os.makedirs('test/sub_test')
        
        (status, message) = gf_base.get_output_dir_status('test')
        self.assertEqual(status, 1)
        
        shutil.rmtree('test')

        
    def test_get_output_dir_message_1(self):
        os.makedirs('test/sub_test')
        
        (status, message) = gf_base.get_output_dir_status('test')
        self.assertEqual(message, '*** ERROR: Output directory is not empty. '
                            'Please delete the contents of the directory before '
                            'running this program again. Alternatively, provide '
                            'the name of an empty directory. ***')
        
        shutil.rmtree('test')

    
    def test_get_output_dir_status_2(self):
        f = open('test', 'a')
        f.close()
        
        (status, message) = gf_base.get_output_dir_status('test')
        self.assertEqual(status, 2)
        
        os.remove('test')


    def test_get_output_dir_message_2(self):
        f = open('test', 'a')
        f.close()
        
        (status, message) = gf_base.get_output_dir_status('test')
        self.assertEqual(message, '*** ERROR: A file exists with the same name as your '
                        'output directory. Please delete the file before running '
                        'this program again. ***')
        
        os.remove('test')        

    
    def test_get_output_dir_status_3(self):
        (status, message) = gf_base.get_output_dir_status('test')
        self.assertEqual(status, 3)
        
    
    def test_get_output_dir_message_3(self):
        (status, message) = gf_base.get_output_dir_status('test')
        self.assertEqual(message,'Output directory does not exist... Creating directory now, '
                    'and then proceeding with analysis...')

    #**************************************************************************

    def test_get_meta_info_status_0_1(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 0)
        os.remove('test')

    def test_get_meta_info_message_0_1(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '')
        os.remove('test')

    def test_get_meta_info_dict_0_1(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        tester_dict['a'] = ['b', 'c', 'd']
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_0_1(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, ['a'])
        os.remove('test')
        
    def test_get_meta_info_status_0_1b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.write('a,b,c,d') 
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 0)
        os.remove('test')

    def test_get_meta_info_message_0_1b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.write('a,b,c,d')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '')
        os.remove('test')

    def test_get_meta_info_dict_0_1b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.write('a,b,c,d') # no \n
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        tester_dict['a'] = ['b', 'c', 'd']
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_0_1b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.write('a,b,c,d')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, ['a'])
        os.remove('test')       
    
    def test_get_meta_info_status_0_2(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 0)
        os.remove('test')
        
    def test_get_meta_info_message_0_2(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '')
        os.remove('test')

    def test_get_meta_info_dict_0_2(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        tester_dict['a'] = ['b', 'c', 'd']
        tester_dict['e'] = ['f', 'g', 'h']
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_0_2(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, ['a', 'e'])
        os.remove('test')

    
    def test_get_meta_info_status_1_1(self):
        f = open('test', 'a')
        f.write('a,b,c,d,e\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 1)
        os.remove('test')
        
    def test_get_meta_info_message_1_1(self):
        f = open('test', 'a')
        f.write('a,b,c,d,e\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '*** ERROR: There are more fields than expected in '
                                   'the meta input file. Please check the file format '
                                   'against the docs. ***')
        os.remove('test')

    def test_get_meta_info_dict_1_1(self):
        f = open('test', 'a')
        f.write('a,b,c,d,e\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_1_1(self):
        f = open('test', 'a')
        f.write('a,b,c,d,e\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, [])
        os.remove('test')


        
    def test_get_meta_info_status_1_1b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.write('a,b,c,d,e')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 1)
        os.remove('test')
        
    def test_get_meta_info_message_1_1b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.write('a,b,c,d,e')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '*** ERROR: There are more fields than expected in '
                                   'the meta input file. Please check the file format '
                                   'against the docs. ***')
        os.remove('test')

    def test_get_meta_info_dict_1_1b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.write('a,b,c,d,e')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_1_1b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.write('a,b,c,d,e')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, [])
        os.remove('test')


    def test_get_meta_info_status_1_2(self):
        f = open('test', 'a')
        f.write('a,b,c,d,e\n')
        f.write('e,f,g,h,i\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 1)
        os.remove('test')
        
    def test_get_meta_info_message_1_2(self):
        f = open('test', 'a')
        f.write('a,b,c,d,e\n')
        f.write('e,f,g,h,i\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '*** ERROR: There are more fields than expected in '
                                   'the meta input file. Please check the file format '
                                   'against the docs. ***')
        os.remove('test')

    def test_get_meta_info_dict_1_2(self):
        f = open('test', 'a')
        f.write('a,b,c,d,e\n')
        f.write('e,f,g,h,i\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_1_2(self):
        f = open('test', 'a')
        f.write('a,b,c,d,e\n')
        f.write('e,f,g,h,i\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, [])
        os.remove('test')


    def test_get_meta_info_status_1_3(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('e,f,g,h,i\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 1)
        os.remove('test')
        
    def test_get_meta_info_message_1_3(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('e,f,g,h,i\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '*** ERROR: There are more fields than expected in '
                                   'the meta input file. Please check the file format '
                                   'against the docs. ***')
        os.remove('test')

    def test_get_meta_info_dict_1_3(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('e,f,g,h,i\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_1_3(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('e,f,g,h,i\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, [])
        os.remove('test')

    def test_get_meta_info_status_1_4(self):
        f = open('test', 'a')
        f.write('a,b,c,d,e\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 1)
        os.remove('test')
        
    def test_get_meta_info_message_1_4(self):
        f = open('test', 'a')
        f.write('a,b,c,d,e\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '*** ERROR: There are more fields than expected in '
                                   'the meta input file. Please check the file format '
                                   'against the docs. ***')
        os.remove('test')

    def test_get_meta_info_dict_1_4(self):
        f = open('test', 'a')
        f.write('a,b,c,d,e\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_1_4(self):
        f = open('test', 'a')
        f.write('a,b,c,d,e\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, [])
        os.remove('test')

    def test_get_meta_info_status_1_5(self):
        f = open('test', 'a')
        f.write('l,m,n,o\n')
        f.write('a,b,c,d,e\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 1)
        os.remove('test')
        
    def test_get_meta_info_message_1_5(self):
        f = open('test', 'a')
        f.write('l,m,n,o\n')
        f.write('a,b,c,d,e\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '*** ERROR: There are more fields than expected in '
                                   'the meta input file. Please check the file format '
                                   'against the docs. ***')
        os.remove('test')

    def test_get_meta_info_dict_1_5(self):
        f = open('test', 'a')
        f.write('l,m,n,o\n')
        f.write('a,b,c,d,e\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_1_5(self):
        f = open('test', 'a')
        f.write('l,m,n,o\n')
        f.write('a,b,c,d,e\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, [])
        os.remove('test')


    def test_get_meta_info_status_2_1(self):
        f = open('test', 'a')
        f.write('a,b,c\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 2)
        os.remove('test')
        
    def test_get_meta_info_message_2_1(self):
        f = open('test', 'a')
        f.write('a,b,c\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '*** ERROR: Meta input file not formatted correctly. Check the number '
                               'of fields in each line and that there are no empty lines. ***')
        os.remove('test')

    def test_get_meta_info_dict_2_1(self):
        f = open('test', 'a')
        f.write('a,b,c\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_2_1(self):
        f = open('test', 'a')
        f.write('a,b,c\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, [])
        os.remove('test')
        
    def test_get_meta_info_status_2_1b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.write('a,b,c')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 2)
        os.remove('test')
        
    def test_get_meta_info_message_2_1b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.write('a,b,c')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '*** ERROR: Meta input file not formatted correctly. Check the number '
                               'of fields in each line and that there are no empty lines. ***')
        os.remove('test')

    def test_get_meta_info_dict_2_1b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.write('a,b,c')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_2_1b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.write('a,b,c')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, [])
        os.remove('test')


    def test_get_meta_info_status_2_2(self):
        f = open('test', 'a')
        f.write('a,b,c\n')
        f.write('e,f,g\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 2)
        os.remove('test')
        
    def test_get_meta_info_message_2_2(self):
        f = open('test', 'a')
        f.write('a,b,c\n')
        f.write('e,f,g\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '*** ERROR: Meta input file not formatted correctly. Check the number '
                               'of fields in each line and that there are no empty lines. ***')
        os.remove('test')

    def test_get_meta_info_dict_2_2(self):
        f = open('test', 'a')
        f.write('a,b,c\n')
        f.write('e,f,g\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_2_2(self):
        f = open('test', 'a')
        f.write('a,b,c\n')
        f.write('e,f,g\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, [])
        os.remove('test')


    def test_get_meta_info_status_2_3(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('e,f,g\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 2)
        os.remove('test')
        
    def test_get_meta_info_message_2_3(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('e,f,g\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '*** ERROR: Meta input file not formatted correctly. Check the number '
                               'of fields in each line and that there are no empty lines. ***')
        os.remove('test')

    def test_get_meta_info_dict_2_3(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('e,f,g\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_2_3(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('e,f,g\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, [])
        os.remove('test')

    def test_get_meta_info_status_2_4(self):
        f = open('test', 'a')
        f.write('a,b,c\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 2)
        os.remove('test')
        
    def test_get_meta_info_message_2_4(self):
        f = open('test', 'a')
        f.write('a,b,c\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '*** ERROR: Meta input file not formatted correctly. Check the number '
                               'of fields in each line and that there are no empty lines. ***')
        os.remove('test')

    def test_get_meta_info_dict_2_4(self):
        f = open('test', 'a')
        f.write('a,b,c\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_2_4(self):
        f = open('test', 'a')
        f.write('a,b,c\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, [])
        os.remove('test')

    def test_get_meta_info_status_2_5(self):
        f = open('test', 'a')
        f.write('l,m,n,o\n')
        f.write('a,b,c\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 2)
        os.remove('test')
        
    def test_get_meta_info_message_2_5(self):
        f = open('test', 'a')
        f.write('l,m,n,o\n')
        f.write('a,b,c\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '*** ERROR: Meta input file not formatted correctly. Check the number '
                               'of fields in each line and that there are no empty lines. ***')
        os.remove('test')

    def test_get_meta_info_dict_2_5(self):
        f = open('test', 'a')
        f.write('l,m,n,o\n')
        f.write('a,b,c\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_2_5(self):
        f = open('test', 'a')
        f.write('l,m,n,o\n')
        f.write('a,b,c\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, [])
        os.remove('test')


    def test_get_meta_info_status_2b_1(self):
        f = open('test', 'a')
        f.write('\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 2)
        os.remove('test')
        
    def test_get_meta_info_message_2b_1(self):
        f = open('test', 'a')
        f.write('\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '*** ERROR: Meta input file not formatted correctly. Check the number '
                               'of fields in each line and that there are no empty lines. ***')
        os.remove('test')

    def test_get_meta_info_dict_2b_1(self):
        f = open('test', 'a')
        f.write('\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_2b_1(self):
        f = open('test', 'a')
        f.write('\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, [])
        os.remove('test')
        
    def test_get_meta_info_status_2b_1b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 2)
        os.remove('test')
        
    def test_get_meta_info_message_2b_1b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '*** ERROR: Meta input file not formatted correctly. Check the number '
                               'of fields in each line and that there are no empty lines. ***')
        os.remove('test')

    def test_get_meta_info_dict_2b_1b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_2b_1b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, [])
        os.remove('test')


    def test_get_meta_info_status_2b_2(self):
        f = open('test', 'a')
        f.write('\n')
        f.write('e,f,g\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 2)
        os.remove('test')
        
    def test_get_meta_info_message_2b_2(self):
        f = open('test', 'a')
        f.write('\n')
        f.write('e,f,g\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '*** ERROR: Meta input file not formatted correctly. Check the number '
                               'of fields in each line and that there are no empty lines. ***')
        os.remove('test')

    def test_get_meta_info_dict_2b_2(self):
        f = open('test', 'a')
        f.write('\n')
        f.write('e,f,g\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_2b_2(self):
        f = open('test', 'a')
        f.write('\n')
        f.write('e,f,g\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, [])
        os.remove('test')


    def test_get_meta_info_status_2b_3(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 2)
        os.remove('test')
        
    def test_get_meta_info_message_2b_3(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '*** ERROR: Meta input file not formatted correctly. Check the number '
                               'of fields in each line and that there are no empty lines. ***')
        os.remove('test')

    def test_get_meta_info_dict_2b_3(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_2b_3(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, [])
        os.remove('test')

    def test_get_meta_info_status_2b_4(self):
        f = open('test', 'a')
        f.write('\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 2)
        os.remove('test')
        
    def test_get_meta_info_message_2b_4(self):
        f = open('test', 'a')
        f.write('\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '*** ERROR: Meta input file not formatted correctly. Check the number '
                               'of fields in each line and that there are no empty lines. ***')
        os.remove('test')

    def test_get_meta_info_dict_2b_4(self):
        f = open('test', 'a')
        f.write('\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_2b_4(self):
        f = open('test', 'a')
        f.write('\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, [])
        os.remove('test')

    def test_get_meta_info_status_2b_5(self):
        f = open('test', 'a')
        f.write('l,m,n,o\n')
        f.write('\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 2)
        os.remove('test')
        
    def test_get_meta_info_message_2b_5(self):
        f = open('test', 'a')
        f.write('l,m,n,o\n')
        f.write('\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '*** ERROR: Meta input file not formatted correctly. Check the number '
                               'of fields in each line and that there are no empty lines. ***')
        os.remove('test')

    def test_get_meta_info_dict_2b_5(self):
        f = open('test', 'a')
        f.write('l,m,n,o\n')
        f.write('\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_2b_5(self):
        f = open('test', 'a')
        f.write('l,m,n,o\n')
        f.write('\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, [])
        os.remove('test')

    def test_get_meta_info_status_3_1(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('a,e,f,g\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 3)
        os.remove('test')
        
    def test_get_meta_info_message_3_1(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('a,e,f,g\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '*** ERROR: Two or more experiments have the same ID. '
                                  'Please check your meta input file for repeated '
                                  'lines and/ or naming errors. ***')
        os.remove('test')

    def test_get_meta_info_dict_3_1(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('a,e,f,g\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_3_1(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('a,e,f,g\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, [])
        os.remove('test')
        
    def test_get_meta_info_status_3_1b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('a,e,f,g')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 3)
        os.remove('test')
        
    def test_get_meta_info_message_3_1b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('a,e,f,g')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '*** ERROR: Two or more experiments have the same ID. '
                                  'Please check your meta input file for repeated '
                                  'lines and/ or naming errors. ***')
        os.remove('test')

    def test_get_meta_info_dict_3_1b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('a,e,f,g')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_3_1b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('a,e,f,g')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, [])
        os.remove('test')


    def test_get_meta_info_status_3_2(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('a,e,f,g\n')
        f.write('x,b,c,d\n')
        f.write('x,e,f,g\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 3)
        os.remove('test')
        
    def test_get_meta_info_message_3_2(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('a,e,f,g\n')
        f.write('x,b,c,d\n')
        f.write('x,e,f,g\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '*** ERROR: Two or more experiments have the same ID. '
                                  'Please check your meta input file for repeated '
                                  'lines and/ or naming errors. ***')
        os.remove('test')

    def test_get_meta_info_dict_3_2(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('a,e,f,g\n')
        f.write('x,b,c,d\n')
        f.write('x,e,f,g\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_3_2(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('a,e,f,g\n')
        f.write('x,b,c,d\n')
        f.write('x,e,f,g\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, [])
        os.remove('test')


    def test_get_meta_info_status_3_3(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('x,b,c,d\n')
        f.write('x,e,f,g\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 3)
        os.remove('test')
        
    def test_get_meta_info_message_3_3(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('x,b,c,d\n')
        f.write('x,e,f,g\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '*** ERROR: Two or more experiments have the same ID. '
                                  'Please check your meta input file for repeated '
                                  'lines and/ or naming errors. ***')
        os.remove('test')

    def test_get_meta_info_dict_3_3(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('x,b,c,d\n')
        f.write('x,e,f,g\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_3_3(self):
        f = open('test', 'a')
        f.write('a,b,c,d\n')
        f.write('x,b,c,d\n')
        f.write('x,e,f,g\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, [])
        os.remove('test')

    def test_get_meta_info_status_3_4(self):
        f = open('test', 'a')
        f.write('x,b,c,d\n')
        f.write('x,e,f,g\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 3)
        os.remove('test')
        
    def test_get_meta_info_message_3_4(self):
        f = open('test', 'a')
        f.write('x,b,c,d\n')
        f.write('x,e,f,g\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '*** ERROR: Two or more experiments have the same ID. '
                                  'Please check your meta input file for repeated '
                                  'lines and/ or naming errors. ***')
        os.remove('test')

    def test_get_meta_info_dict_3_4(self):
        f = open('test', 'a')
        f.write('x,b,c,d\n')
        f.write('x,e,f,g\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_3_4(self):
        f = open('test', 'a')
        f.write('x,b,c,d\n')
        f.write('x,e,f,g\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, [])
        os.remove('test')

    def test_get_meta_info_status_3_5(self):
        f = open('test', 'a')
        f.write('l,m,n,o\n')
        f.write('x,b,c,d\n')
        f.write('x,e,f,g\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(status, 3)
        os.remove('test')
        
    def test_get_meta_info_message_3_5(self):
        f = open('test', 'a')
        f.write('l,m,n,o\n')
        f.write('x,b,c,d\n')
        f.write('x,e,f,g\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(message, '*** ERROR: Two or more experiments have the same ID. '
                                  'Please check your meta input file for repeated '
                                  'lines and/ or naming errors. ***')
        os.remove('test')

    def test_get_meta_info_dict_3_5(self):
        f = open('test', 'a')
        f.write('l,m,n,o\n')
        f.write('x,b,c,d\n')
        f.write('x,e,f,g\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        tester_dict = {}
        self.assertEqual(compare_dicts(mi_dict, tester_dict), 1)
        os.remove('test')

    def test_get_meta_info_ids_3_5(self):
        f = open('test', 'a')
        f.write('l,m,n,o\n')
        f.write('x,b,c,d\n')
        f.write('x,e,f,g\n')
        f.write('e,f,g,h\n')
        f.close()
        (status, message, mi_dict, exp_ids) = gf_base.get_meta_info('test')
        self.assertEqual(exp_ids, [])
        os.remove('test')


    def test_generate_images_dirs_1(self):
        info_string = 'info'
        output_dir = 'test'
        (rel_images_dir, abs_images_dir) = gf_base.generate_images_dirs(info_string, output_dir)
        self.assertEqual(rel_images_dir, 'images_info_AUTO/')
        
    def test_generate_images_dirs_2(self):
        info_string = 'info'
        output_dir = 'test'
        (rel_images_dir, abs_images_dir) = gf_base.generate_images_dirs(info_string, output_dir)
        self.assertEqual(abs_images_dir, 'test/images_info_AUTO/')
        
    
    
    def test_read_in_ora_data_status_0_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_0_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_0_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_0_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_0_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(exp_term_genes_dict, {})
    
    
    def test_read_in_ora_data_exp_term_dotplot_dict_0_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_0_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(exp_terms, [])
        
    
    def test_read_in_ora_data_status_0_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_0_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_0_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_0_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_0_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(exp_term_genes_dict, {})


    def test_read_in_ora_data_exp_term_dotplot_dict_0_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_0_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(exp_terms, [])



    def test_read_in_ora_data_status_0_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_0_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_0_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_0_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_0_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(exp_term_genes_dict, {})

    
    def test_read_in_ora_data_exp_term_dotplot_dict_0_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_0_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(exp_terms, [])



    def test_read_in_ora_data_status_0_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_0_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_0_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_0_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_0_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(exp_term_genes_dict, {})

    
    def test_read_in_ora_data_exp_term_dotplot_dict_0_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_0_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(exp_terms, [])


    def test_read_in_ora_data_status_0_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_0_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_0_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_0_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_0_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(exp_term_genes_dict, {})


    def test_read_in_ora_data_exp_term_dotplot_dict_0_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_0_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(exp_terms, [])




    def test_read_in_ora_data_status_0_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_0_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_0_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_0_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_0_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(exp_term_genes_dict, {})


    def test_read_in_ora_data_exp_term_dotplot_dict_0_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_0_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(exp_terms, [])



    def test_read_in_ora_data_status_0_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_0_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_0_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_0_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_0_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(exp_term_genes_dict, {})


    def test_read_in_ora_data_exp_term_dotplot_dict_0_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_0_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(exp_terms, [])


    def test_read_in_ora_data_status_0_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_0_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_0_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_0_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_0_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(exp_term_genes_dict, {})


    def test_read_in_ora_data_exp_term_dotplot_dict_0_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_0_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(exp_terms, [])



    def test_read_in_ora_data_status_0_9(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_0_9(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_0_9(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_0_9(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol biosynthetic process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_0_9(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)

    def test_read_in_ora_data_exp_term_dotplot_dict_0_9(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_term_dotplot_dict,{})
        
    
    def test_read_in_ora_data_exp_terms_0_9(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(exp_terms, ['GO:0016126'])




    
    def test_read_in_ora_data_status_0_10(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_0_10(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_0_10(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_0_10(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol biosynthetic process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_0_10(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)

    def test_read_in_ora_data_exp_term_dotplot_dict_0_10(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        gene_ratio_string = '20/1383'
        gene_ratio_Fraction = Fraction( gene_ratio_string )
        gene_ratio = round( gene_ratio_Fraction.numerator/gene_ratio_Fraction.denominator , 3 )
        bg_ratio_string = '52/23210'
        neg_log10_padj = round( -1 * math.log10( float( '3e-08' ) ) , 1 )
        count = 20
        
        test_exp_term_dotplot_dict = {}
        test_exp_term_dotplot_dict[('test_id','GO:0016126')] = [ gene_ratio , neg_log10_padj , count , gene_ratio_string , bg_ratio_string ]
        
        self.assertEqual(compare_dicts(exp_term_dotplot_dict, test_exp_term_dotplot_dict), 1)
        
    
    def test_read_in_ora_data_exp_terms_0_10(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(exp_terms, ['GO:0016126'])




    def test_read_in_ora_data_status_0_11(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_0_11(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_0_11(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_0_11(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol biosynthetic process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_0_11(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)

    def test_read_in_ora_data_exp_term_dotplot_dict_0_11(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_term_dotplot_dict,{})
        
    
    def test_read_in_ora_data_exp_terms_0_11(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(exp_terms, ['GO:0016126'])




    
    def test_read_in_ora_data_status_0_12(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_0_12(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_0_12(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_0_12(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol biosynthetic process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_0_12(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)

    def test_read_in_ora_data_exp_term_dotplot_dict_0_12(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        gene_ratio_string = '20/1383'
        gene_ratio_Fraction = Fraction( gene_ratio_string )
        gene_ratio = round( gene_ratio_Fraction.numerator/gene_ratio_Fraction.denominator , 3 )
        bg_ratio_string = '52/23210'
        neg_log10_padj = round( -1 * math.log10( float( '3e-08' ) ) , 1 )
        count = 20
        
        test_exp_term_dotplot_dict = {}
        test_exp_term_dotplot_dict[('test_id','GO:0016126')] = [ gene_ratio , neg_log10_padj , count , gene_ratio_string , bg_ratio_string ]
        
        self.assertEqual(compare_dicts(exp_term_dotplot_dict, test_exp_term_dotplot_dict), 1)
        
    
    def test_read_in_ora_data_exp_terms_0_12(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(exp_terms, ['GO:0016126'])


    def test_read_in_ora_data_status_0_13(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_0_13(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_0_13(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_0_13(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol biosynthetic process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_0_13(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)

    def test_read_in_ora_data_exp_term_dotplot_dict_0_13(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_term_dotplot_dict,{})
        
    
    def test_read_in_ora_data_exp_terms_0_13(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(exp_terms, ['GO:0016126'])




    
    def test_read_in_ora_data_status_0_14(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_0_14(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_0_14(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_0_14(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol biosynthetic process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_0_14(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)

    def test_read_in_ora_data_exp_term_dotplot_dict_0_14(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        gene_ratio_string = '20/1383'
        gene_ratio_Fraction = Fraction( gene_ratio_string )
        gene_ratio = round( gene_ratio_Fraction.numerator/gene_ratio_Fraction.denominator , 3 )
        bg_ratio_string = '52/23210'
        neg_log10_padj = round( -1 * math.log10( float( '3e-08' ) ) , 1 )
        count = 20
        
        test_exp_term_dotplot_dict = {}
        test_exp_term_dotplot_dict[('test_id','GO:0016126')] = [ gene_ratio , neg_log10_padj , count , gene_ratio_string , bg_ratio_string ]
        
        self.assertEqual(compare_dicts(exp_term_dotplot_dict, test_exp_term_dotplot_dict), 1)
        
    
    def test_read_in_ora_data_exp_terms_0_14(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(exp_terms, ['GO:0016126'])








    def test_read_in_ora_data_status_0_15(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_0_15(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_0_15(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        test_term_types_dict['GO:0016127'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_0_15(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol biosynthetic process'
        test_term_defs_dict['GO:0016127'] = 'sterol biosynthetic process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_0_15(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
        test_exp_term_genes_dict[('test_id', 'GO:0016127')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)

    def test_read_in_ora_data_exp_term_dotplot_dict_0_15(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_term_dotplot_dict,{})
        
    
    def test_read_in_ora_data_exp_terms_0_15(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(exp_terms, ['GO:0016126','GO:0016127'])




    
    def test_read_in_ora_data_status_0_16(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_0_16(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_0_16(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        test_term_types_dict['GO:0016127'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_0_16(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol biosynthetic process'
        test_term_defs_dict['GO:0016127'] = 'sterol biosynthetic process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_0_16(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
        test_exp_term_genes_dict[('test_id', 'GO:0016127')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)

    def test_read_in_ora_data_exp_term_dotplot_dict_0_16(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        gene_ratio_string = '20/1383'
        gene_ratio_Fraction = Fraction( gene_ratio_string )
        gene_ratio = round( gene_ratio_Fraction.numerator/gene_ratio_Fraction.denominator , 3 )
        bg_ratio_string = '52/23210'
        neg_log10_padj = round( -1 * math.log10( float( '3e-08' ) ) , 1 )
        count = 20
        
        test_exp_term_dotplot_dict = {}
        test_exp_term_dotplot_dict[('test_id','GO:0016126')] = [ gene_ratio , neg_log10_padj , count , gene_ratio_string , bg_ratio_string ]
        test_exp_term_dotplot_dict[('test_id','GO:0016127')] = [ gene_ratio , neg_log10_padj , count , gene_ratio_string , bg_ratio_string ]
        
        self.assertEqual(compare_dicts(exp_term_dotplot_dict, test_exp_term_dotplot_dict), 1)
        
    
    def test_read_in_ora_data_exp_terms_0_16(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(exp_terms, ['GO:0016126', 'GO:0016127'])


 




    def test_read_in_ora_data_status_0_17(self):
        """extra commas in descriptions"""
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol, biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterolm biosynthetic, process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_0_17(self):
        """extra commas in descriptions"""
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterolm biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol, biosynthetic, process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_0_17(self):
        """extra commas in descriptions"""
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol, biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol, biosynthetic, process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        test_term_types_dict['GO:0016127'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_0_17(self):
        """extra commas in descriptions"""
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol, biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol, biosynthetic, process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol, biosynthetic process'
        test_term_defs_dict['GO:0016127'] = 'sterol, biosynthetic, process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_0_17(self):
        """extra commas in descriptions"""
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol, biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol, biosynthetic, process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
        test_exp_term_genes_dict[('test_id', 'GO:0016127')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)

    def test_read_in_ora_data_exp_term_dotplot_dict_0_157(self):
        """extra commas in descriptions"""
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol, biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol, biosynthetic, process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_term_dotplot_dict,{})
        
    
    def test_read_in_ora_data_exp_terms_0_17(self):
        """extra commas in descriptions"""
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol, biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol, biosynthetic, process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(exp_terms, ['GO:0016126','GO:0016127'])




    
    def test_read_in_ora_data_status_0_18(self):
        """extra commas in descriptions"""
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol, biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol, biosynthetic, process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_0_18(self):
        """extra commas in descriptions"""
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol, biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol, biosynthetic, process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_0_18(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol, biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol, biosynthetic, process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        test_term_types_dict['GO:0016127'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_0_18(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol, biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol, biosynthetic, process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol, biosynthetic process'
        test_term_defs_dict['GO:0016127'] = 'sterol, biosynthetic, process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_0_18(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol, biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol, biosynthetic, process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
        test_exp_term_genes_dict[('test_id', 'GO:0016127')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)

    def test_read_in_ora_data_exp_term_dotplot_dict_0_18(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol, biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol, biosynthetic, process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        gene_ratio_string = '20/1383'
        gene_ratio_Fraction = Fraction( gene_ratio_string )
        gene_ratio = round( gene_ratio_Fraction.numerator/gene_ratio_Fraction.denominator , 3 )
        bg_ratio_string = '52/23210'
        neg_log10_padj = round( -1 * math.log10( float( '3e-08' ) ) , 1 )
        count = 20
        
        test_exp_term_dotplot_dict = {}
        test_exp_term_dotplot_dict[('test_id','GO:0016126')] = [ gene_ratio , neg_log10_padj , count , gene_ratio_string , bg_ratio_string ]
        test_exp_term_dotplot_dict[('test_id','GO:0016127')] = [ gene_ratio , neg_log10_padj , count , gene_ratio_string , bg_ratio_string ]
        
        self.assertEqual(compare_dicts(exp_term_dotplot_dict, test_exp_term_dotplot_dict), 1)
        
    
    def test_read_in_ora_data_exp_terms_0_18(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol, biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol, biosynthetic, process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(exp_terms, ['GO:0016126', 'GO:0016127'])





    def test_read_in_ora_data_status_1_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(status, 1)
    
    
    def test_read_in_ora_data_message_1_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(message, '*** ERROR: ORA (or GSEA) file not formatted correctly. '
                                  'Check that the format matches the description in the docs. '
                                  'Also, check the number of fields in each line and that there '
                                  'are no empty lines. ***')
    
    
    def test_read_in_ora_data_term_types_dict_1_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_1_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_1_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(exp_term_genes_dict, {})
    
    
    def test_read_in_ora_data_exp_term_dotplot_dict_1_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_1_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(exp_terms, [])
        
    
    def test_read_in_ora_data_status_1_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(status, 1)
    
    
    def test_read_in_ora_data_message_1_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(message, '*** ERROR: ORA (or GSEA) file not formatted correctly. '
                                  'Check that the format matches the description in the docs. '
                                  'Also, check the number of fields in each line and that there '
                                  'are no empty lines. ***')
    
    
    def test_read_in_ora_data_term_types_dict_1_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_1_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_1_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(exp_term_genes_dict, {})


    def test_read_in_ora_data_exp_term_dotplot_dict_1_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_1_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(exp_terms, [])


    def test_read_in_ora_data_status_1_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(status, 1)
    
    
    def test_read_in_ora_data_message_1_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(message, '*** ERROR: ORA (or GSEA) file not formatted correctly. '
                                  'Check that the format matches the description in the docs. '
                                  'Also, check the number of fields in each line and that there '
                                  'are no empty lines. ***')
    
    
    def test_read_in_ora_data_term_types_dict_1_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_1_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_1_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_term_genes_dict, {})
    
    
    def test_read_in_ora_data_exp_term_dotplot_dict_1_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_1_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_terms, [])
        
    
    def test_read_in_ora_data_status_1_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(status, 1)
    
    
    def test_read_in_ora_data_message_1_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(message, '*** ERROR: ORA (or GSEA) file not formatted correctly. '
                                  'Check that the format matches the description in the docs. '
                                  'Also, check the number of fields in each line and that there '
                                  'are no empty lines. ***')
    
    
    def test_read_in_ora_data_term_types_dict_1_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_1_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_1_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_term_genes_dict, {})


    def test_read_in_ora_data_exp_term_dotplot_dict_1_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_1_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_terms, [])





    def test_read_in_ora_data_status_1_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(status, 1)
    
    
    def test_read_in_ora_data_message_1_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(message, '*** ERROR: ORA (or GSEA) file not formatted correctly. '
                                  'Check that the format matches the description in the docs. '
                                  'Also, check the number of fields in each line and that there '
                                  'are no empty lines. ***')
    
    
    def test_read_in_ora_data_term_types_dict_1_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_1_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_1_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_term_genes_dict, {})
    
    
    def test_read_in_ora_data_exp_term_dotplot_dict_1_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_1_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_terms, [])
        
    
    def test_read_in_ora_data_status_1_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(status, 1)
    
    
    def test_read_in_ora_data_message_1_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(message, '*** ERROR: ORA (or GSEA) file not formatted correctly. '
                                  'Check that the format matches the description in the docs. '
                                  'Also, check the number of fields in each line and that there '
                                  'are no empty lines. ***')
    
    
    def test_read_in_ora_data_term_types_dict_1_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_1_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_1_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_term_genes_dict, {})


    def test_read_in_ora_data_exp_term_dotplot_dict_1_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_1_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_terms, [])




    def test_read_in_ora_data_status_1_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(status, 1)
    
    
    def test_read_in_ora_data_message_1_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(message, '*** ERROR: ORA (or GSEA) file not formatted correctly. '
                                  'Check that the format matches the description in the docs. '
                                  'Also, check the number of fields in each line and that there '
                                  'are no empty lines. ***')
    
    
    def test_read_in_ora_data_term_types_dict_1_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_1_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_1_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_term_genes_dict, {})
    
    
    def test_read_in_ora_data_exp_term_dotplot_dict_1_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_1_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_terms, [])
        
    
    def test_read_in_ora_data_status_1_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(status, 1)
    
    
    def test_read_in_ora_data_message_1_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(message, '*** ERROR: ORA (or GSEA) file not formatted correctly. '
                                  'Check that the format matches the description in the docs. '
                                  'Also, check the number of fields in each line and that there '
                                  'are no empty lines. ***')
    
    
    def test_read_in_ora_data_term_types_dict_1_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_1_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_1_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_term_genes_dict, {})


    def test_read_in_ora_data_exp_term_dotplot_dict_1_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_1_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_terms, [])




    def test_read_in_ora_data_status_2_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(status, 2)
    
    
    def test_read_in_ora_data_message_2_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(message, '*** ERROR: Term repeated in ORA (or GSEA) file in '
                                  ' experiment with ID: ' + 'test_id' + '. ***')
    
    
    def test_read_in_ora_data_term_types_dict_2_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_2_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_2_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(exp_term_genes_dict, {})
    
    
    def test_read_in_ora_data_exp_term_dotplot_dict_2_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_2_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(exp_terms, [])
        
    
    def test_read_in_ora_data_status_2_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(status, 2)
    
    
    def test_read_in_ora_data_message_2_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(message, '*** ERROR: Term repeated in ORA (or GSEA) file in '
                                  ' experiment with ID: ' + 'test_id' + '. ***')
    
    
    def test_read_in_ora_data_term_types_dict_2_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_2_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_2_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(exp_term_genes_dict, {})


    def test_read_in_ora_data_exp_term_dotplot_dict_2_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_2_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(exp_terms, [])



    def test_read_in_ora_data_status_2_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(status, 2)
    
    
    def test_read_in_ora_data_message_2_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(message, '*** ERROR: Term repeated in ORA (or GSEA) file in '
                                  ' experiment with ID: ' + 'test_id' + '. ***')
    
    
    def test_read_in_ora_data_term_types_dict_2_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_2_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_2_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_term_genes_dict, {})
    
    
    def test_read_in_ora_data_exp_term_dotplot_dict_2_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_2_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_terms, [])
        
    
    def test_read_in_ora_data_status_2_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(status, 2)
    
    
    def test_read_in_ora_data_message_2_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(message, '*** ERROR: Term repeated in ORA (or GSEA) file in '
                                  ' experiment with ID: ' + 'test_id' + '. ***')
    
    
    def test_read_in_ora_data_term_types_dict_2_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_2_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_2_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_term_genes_dict, {})


    def test_read_in_ora_data_exp_term_dotplot_dict_2_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_2_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_terms, [])



    def test_read_in_ora_data_status_2_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(status, 2)
    
    
    def test_read_in_ora_data_message_2_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(message, '*** ERROR: Term repeated in ORA (or GSEA) file in '
                                  ' experiment with ID: ' + 'test_id' + '. ***')
    
    
    def test_read_in_ora_data_term_types_dict_2_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_2_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_2_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_term_genes_dict, {})
    
    
    def test_read_in_ora_data_exp_term_dotplot_dict_2_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_2_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_terms, [])
        
    
    def test_read_in_ora_data_status_2_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(status, 2)
    
    
    def test_read_in_ora_data_message_2_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(message, '*** ERROR: Term repeated in ORA (or GSEA) file in '
                                  ' experiment with ID: ' + 'test_id' + '. ***')
    
    
    def test_read_in_ora_data_term_types_dict_2_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_2_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_2_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_term_genes_dict, {})


    def test_read_in_ora_data_exp_term_dotplot_dict_2_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_2_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_terms, [])



    def test_read_in_ora_data_status_2_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(status, 2)
    
    
    def test_read_in_ora_data_message_2_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(message, '*** ERROR: Term repeated in ORA (or GSEA) file in '
                                  ' experiment with ID: ' + 'test_id' + '. ***')
    
    
    def test_read_in_ora_data_term_types_dict_2_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_2_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_2_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_term_genes_dict, {})
    
    
    def test_read_in_ora_data_exp_term_dotplot_dict_2_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_2_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_terms, [])
        
    
    def test_read_in_ora_data_status_2_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(status, 2)
    
    
    def test_read_in_ora_data_message_2_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(message, '*** ERROR: Term repeated in ORA (or GSEA) file in '
                                  ' experiment with ID: ' + 'test_id' + '. ***')
    
    
    def test_read_in_ora_data_term_types_dict_2_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_2_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_2_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_term_genes_dict, {})


    def test_read_in_ora_data_exp_term_dotplot_dict_2_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_2_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_terms, [])




    def test_read_in_ora_data_status_2_9(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(status, 2)
    
    
    def test_read_in_ora_data_message_2_9(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(message, '*** ERROR: Term repeated in ORA (or GSEA) file in '
                                  ' experiment with ID: ' + 'test_id' + '. ***')
    
    
    def test_read_in_ora_data_term_types_dict_2_9(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_2_9(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_2_9(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_term_genes_dict, {})
    
    
    def test_read_in_ora_data_exp_term_dotplot_dict_2_9(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_2_9(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_terms, [])
        
    
    def test_read_in_ora_data_status_2_10(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(status, 2)
    
    
    def test_read_in_ora_data_message_2_10(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(message, '*** ERROR: Term repeated in ORA (or GSEA) file in '
                                  ' experiment with ID: ' + 'test_id' + '. ***')
    
    
    def test_read_in_ora_data_term_types_dict_2_10(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_2_10(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_2_10(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_term_genes_dict, {})


    def test_read_in_ora_data_exp_term_dotplot_dict_2_10(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_2_10(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_terms, [])



    def test_read_in_ora_data_status_2_11(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(status, 2)
    
    
    def test_read_in_ora_data_message_2_11(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(message, '*** ERROR: Term repeated in ORA (or GSEA) file in '
                                  ' experiment with ID: ' + 'test_id' + '. ***')
    
    
    def test_read_in_ora_data_term_types_dict_2_11(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_2_11(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_2_11(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_term_genes_dict, {})
    
    
    def test_read_in_ora_data_exp_term_dotplot_dict_2_11(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_2_11(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_terms, [])
        
    
    def test_read_in_ora_data_status_2_12(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(status, 2)
    
    
    def test_read_in_ora_data_message_2_12(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(message, '*** ERROR: Term repeated in ORA (or GSEA) file in '
                                  ' experiment with ID: ' + 'test_id' + '. ***')
    
    
    def test_read_in_ora_data_term_types_dict_2_12(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_2_12(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_2_12(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_term_genes_dict, {})


    def test_read_in_ora_data_exp_term_dotplot_dict_2_12(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_2_12(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_terms, [])


    def test_read_in_ora_data_status_2_13(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(status, 2)
    
    
    def test_read_in_ora_data_message_2_13(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(message, '*** ERROR: Term repeated in ORA (or GSEA) file in '
                                  ' experiment with ID: ' + 'test_id' + '. ***')
    
    
    def test_read_in_ora_data_term_types_dict_2_13(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_2_13(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_2_13(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_term_genes_dict, {})
    
    
    def test_read_in_ora_data_exp_term_dotplot_dict_2_13(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_2_13(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_terms, [])
        
    
    def test_read_in_ora_data_status_2_14(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(status, 2)
    
    
    def test_read_in_ora_data_message_2_14(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(message, '*** ERROR: Term repeated in ORA (or GSEA) file in '
                                  ' experiment with ID: ' + 'test_id' + '. ***')
    
    
    def test_read_in_ora_data_term_types_dict_2_14(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_2_14(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_2_14(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_term_genes_dict, {})


    def test_read_in_ora_data_exp_term_dotplot_dict_2_14(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_2_14(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_terms, [])



    def test_read_in_ora_data_status_2_15(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(status, 2)
    
    
    def test_read_in_ora_data_message_2_15(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(message, '*** ERROR: Term repeated in ORA (or GSEA) file in '
                                  ' experiment with ID: ' + 'test_id' + '. ***')
    
    
    def test_read_in_ora_data_term_types_dict_2_15(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_2_15(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_2_15(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_term_genes_dict, {})
    
    
    def test_read_in_ora_data_exp_term_dotplot_dict_2_15(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_2_15(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_terms, [])
        
    
    def test_read_in_ora_data_status_2_16(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(status, 2)
    
    
    def test_read_in_ora_data_message_2_16(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(message, '*** ERROR: Term repeated in ORA (or GSEA) file in '
                                  ' experiment with ID: ' + 'test_id' + '. ***')
    
    
    def test_read_in_ora_data_term_types_dict_2_16(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_2_16(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_2_16(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_term_genes_dict, {})


    def test_read_in_ora_data_exp_term_dotplot_dict_2_16(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_2_16(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_terms, [])




    def test_read_in_ora_data_status_2_17(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(status, 2)
    
    
    def test_read_in_ora_data_message_2_17(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(message, '*** ERROR: Term repeated in ORA (or GSEA) file in '
                                  ' experiment with ID: ' + 'test_id' + '. ***')
    
    
    def test_read_in_ora_data_term_types_dict_2_17(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_2_17(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_2_17(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_term_genes_dict, {})
    
    
    def test_read_in_ora_data_exp_term_dotplot_dict_2_17(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_2_17(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_terms, [])
        
    
    def test_read_in_ora_data_status_2_18(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(status, 2)
    
    
    def test_read_in_ora_data_message_2_18(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(message, '*** ERROR: Term repeated in ORA (or GSEA) file in '
                                  ' experiment with ID: ' + 'test_id' + '. ***')
    
    
    def test_read_in_ora_data_term_types_dict_2_18(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_2_18(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_2_18(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_term_genes_dict, {})


    def test_read_in_ora_data_exp_term_dotplot_dict_2_18(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_2_18(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_terms, [])



    def test_read_in_ora_data_status_2_19(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(status, 2)
    
    
    def test_read_in_ora_data_message_2_19(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(message, '*** ERROR: Term repeated in ORA (or GSEA) file in '
                                  ' experiment with ID: ' + 'test_id' + '. ***')
    
    
    def test_read_in_ora_data_term_types_dict_2_19(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_2_19(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_2_19(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_term_genes_dict, {})
    
    
    def test_read_in_ora_data_exp_term_dotplot_dict_2_19(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_2_19(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, test_stats)
        self.assertEqual(exp_terms, [])
        
    
    def test_read_in_ora_data_status_2_20(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(status, 2)
    
    
    def test_read_in_ora_data_message_2_20(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(message, '*** ERROR: Term repeated in ORA (or GSEA) file in '
                                  ' experiment with ID: ' + 'test_id' + '. ***')
    
    
    def test_read_in_ora_data_term_types_dict_2_20(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_2_20(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_2_20(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_term_genes_dict, {})


    def test_read_in_ora_data_exp_term_dotplot_dict_2_20(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_2_20(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (2, 0)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, test_stats)
        self.assertEqual(exp_terms, [])





    def test_read_in_ora_data_status_3_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(status, 3)
    
    
    def test_read_in_ora_data_message_3_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(message, '*** ERROR: Data for dotplots is not formatted as expected in ORA/ GSEA file. '
                                  'Please refer to documentation for expected column order and content. '
                                  'If you do not have dotplot data to plot, or if you want to omit dotplots '
                                  'for whatever reason, then you can set DOTPLOTS to False in the config file. '
                                  'NOTE, however, that your ORA/ GSEA file still has to have the expected '
                                  'column order (see docs). ***')
    
    
    def test_read_in_ora_data_term_types_dict_3_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_3_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_term_genes_dict, {})

    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_3_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_terms, [])


    def test_read_in_ora_data_status_3_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(status, 3)
    
    
    def test_read_in_ora_data_message_3_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(message, '*** ERROR: Data for dotplots is not formatted as expected in ORA/ GSEA file. '
                                  'Please refer to documentation for expected column order and content. '
                                  'If you do not have dotplot data to plot, or if you want to omit dotplots '
                                  'for whatever reason, then you can set DOTPLOTS to False in the config file. '
                                  'NOTE, however, that your ORA/ GSEA file still has to have the expected '
                                  'column order (see docs). ***')
    
    
    def test_read_in_ora_data_term_types_dict_3_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_3_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_term_genes_dict, {})

    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_3_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_terms, [])






    def test_read_in_ora_data_status_3_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(status, 3)
    
    
    def test_read_in_ora_data_message_3_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(message, '*** ERROR: Data for dotplots is not formatted as expected in ORA/ GSEA file. '
                                  'Please refer to documentation for expected column order and content. '
                                  'If you do not have dotplot data to plot, or if you want to omit dotplots '
                                  'for whatever reason, then you can set DOTPLOTS to False in the config file. '
                                  'NOTE, however, that your ORA/ GSEA file still has to have the expected '
                                  'column order (see docs). ***')
    
    
    def test_read_in_ora_data_term_types_dict_3_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_3_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_term_genes_dict, {})

    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_3_3(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_terms, [])



    def test_read_in_ora_data_status_3_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(status, 3)
    
    
    def test_read_in_ora_data_message_3_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(message, '*** ERROR: Data for dotplots is not formatted as expected in ORA/ GSEA file. '
                                  'Please refer to documentation for expected column order and content. '
                                  'If you do not have dotplot data to plot, or if you want to omit dotplots '
                                  'for whatever reason, then you can set DOTPLOTS to False in the config file. '
                                  'NOTE, however, that your ORA/ GSEA file still has to have the expected '
                                  'column order (see docs). ***')
    
    
    def test_read_in_ora_data_term_types_dict_3_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_3_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_term_genes_dict, {})

    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_3_4(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_terms, [])







    def test_read_in_ora_data_status_3_1b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_3_1b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_3_1b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_3_1b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol biosynthetic process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_1b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)


    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_1b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_term_dotplot_dict,{})
        
        
    
    def test_read_in_ora_data_exp_terms_3_1b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_terms, ['GO:0016126'])





    def test_read_in_ora_data_status_3_2b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_3_2b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_3_2b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_3_2b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol biosynthetic process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_2b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)


    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_2b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_term_dotplot_dict,{})
        
        
    
    def test_read_in_ora_data_exp_terms_3_2b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_terms, ['GO:0016126'])




    def test_read_in_ora_data_status_3_3b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_3_3b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_3_3b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_3_3b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol biosynthetic process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_3b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)


    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_3b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_term_dotplot_dict,{})
        
        
    
    def test_read_in_ora_data_exp_terms_3_3b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_terms, ['GO:0016126'])



    def test_read_in_ora_data_status_3_4b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_3_4b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_3_4b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_3_4b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol biosynthetic process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_4b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)


    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_4b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_term_dotplot_dict,{})
        
        
    
    def test_read_in_ora_data_exp_terms_3_4b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_terms, ['GO:0016126'])




    def test_read_in_ora_data_status_3_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(status, 3)
    
    
    def test_read_in_ora_data_message_3_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(message, '*** ERROR: Data for dotplots is not formatted as expected in ORA/ GSEA file. '
                                  'Please refer to documentation for expected column order and content. '
                                  'If you do not have dotplot data to plot, or if you want to omit dotplots '
                                  'for whatever reason, then you can set DOTPLOTS to False in the config file. '
                                  'NOTE, however, that your ORA/ GSEA file still has to have the expected '
                                  'column order (see docs). ***')
    
    
    def test_read_in_ora_data_term_types_dict_3_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_3_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_term_genes_dict, {})

    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_3_5(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_terms, [])


    def test_read_in_ora_data_status_3_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(status, 3)
    
    
    def test_read_in_ora_data_message_3_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(message, '*** ERROR: Data for dotplots is not formatted as expected in ORA/ GSEA file. '
                                  'Please refer to documentation for expected column order and content. '
                                  'If you do not have dotplot data to plot, or if you want to omit dotplots '
                                  'for whatever reason, then you can set DOTPLOTS to False in the config file. '
                                  'NOTE, however, that your ORA/ GSEA file still has to have the expected '
                                  'column order (see docs). ***')
    
    
    def test_read_in_ora_data_term_types_dict_3_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_3_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_term_genes_dict, {})

    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_3_6(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_terms, [])






    def test_read_in_ora_data_status_3_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(status, 3)
    
    
    def test_read_in_ora_data_message_3_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(message, '*** ERROR: Data for dotplots is not formatted as expected in ORA/ GSEA file. '
                                  'Please refer to documentation for expected column order and content. '
                                  'If you do not have dotplot data to plot, or if you want to omit dotplots '
                                  'for whatever reason, then you can set DOTPLOTS to False in the config file. '
                                  'NOTE, however, that your ORA/ GSEA file still has to have the expected '
                                  'column order (see docs). ***')
    
    
    def test_read_in_ora_data_term_types_dict_3_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_3_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_term_genes_dict, {})

    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_3_7(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_terms, [])



    def test_read_in_ora_data_status_3_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(status, 3)
    
    
    def test_read_in_ora_data_message_3_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(message, '*** ERROR: Data for dotplots is not formatted as expected in ORA/ GSEA file. '
                                  'Please refer to documentation for expected column order and content. '
                                  'If you do not have dotplot data to plot, or if you want to omit dotplots '
                                  'for whatever reason, then you can set DOTPLOTS to False in the config file. '
                                  'NOTE, however, that your ORA/ GSEA file still has to have the expected '
                                  'column order (see docs). ***')
    
    
    def test_read_in_ora_data_term_types_dict_3_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_3_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_term_genes_dict, {})

    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_3_8(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_terms, [])







    def test_read_in_ora_data_status_3_5b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_3_5b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_3_5b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        test_term_types_dict['GO:0016127'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_3_5b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol biosynthetic process'
        test_term_defs_dict['GO:0016127'] = 'sterol biosynthetic process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_5b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        test_exp_term_genes_dict[('test_id', 'GO:0016127')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)


    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_5b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_term_dotplot_dict,{})
        
        
    
    def test_read_in_ora_data_exp_terms_3_5b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_terms, ['GO:0016127','GO:0016126'])





    def test_read_in_ora_data_status_3_6b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_3_6b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_3_6b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        test_term_types_dict['GO:0016127'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_3_6b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol biosynthetic process'
        test_term_defs_dict['GO:0016127'] = 'sterol biosynthetic process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_6b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        test_exp_term_genes_dict[('test_id', 'GO:0016127')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)


    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_6b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_term_dotplot_dict,{})
        
        
    
    def test_read_in_ora_data_exp_terms_3_6b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_terms, ['GO:0016127','GO:0016126'])




    def test_read_in_ora_data_status_3_7b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_3_7b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_3_7b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        test_term_types_dict['GO:0016127'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_3_7b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol biosynthetic process'
        test_term_defs_dict['GO:0016127'] = 'sterol biosynthetic process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_7b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        test_exp_term_genes_dict[('test_id', 'GO:0016127')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)


    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_7b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_term_dotplot_dict,{})
        
        
    
    def test_read_in_ora_data_exp_terms_3_7b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_terms, ['GO:0016127','GO:0016126'])



    def test_read_in_ora_data_status_3_8b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_3_8b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_3_8b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        test_term_types_dict['GO:0016127'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_3_8b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol biosynthetic process'
        test_term_defs_dict['GO:0016127'] = 'sterol biosynthetic process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_8b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
        test_exp_term_genes_dict[('test_id', 'GO:0016127')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)


    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_8b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_term_dotplot_dict,{})
        
        
    
    def test_read_in_ora_data_exp_terms_3_8b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_terms, ['GO:0016127','GO:0016126'])



    def test_read_in_ora_data_status_3_9(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(status, 3)
    
    
    def test_read_in_ora_data_message_3_9(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(message, '*** ERROR: Data for dotplots is not formatted as expected in ORA/ GSEA file. '
                                  'Please refer to documentation for expected column order and content. '
                                  'If you do not have dotplot data to plot, or if you want to omit dotplots '
                                  'for whatever reason, then you can set DOTPLOTS to False in the config file. '
                                  'NOTE, however, that your ORA/ GSEA file still has to have the expected '
                                  'column order (see docs). ***')
    
    
    def test_read_in_ora_data_term_types_dict_3_9(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_3_9(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_9(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_term_genes_dict, {})

    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_9(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_3_9(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_terms, [])


    def test_read_in_ora_data_status_3_10(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(status, 3)
    
    
    def test_read_in_ora_data_message_3_10(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(message, '*** ERROR: Data for dotplots is not formatted as expected in ORA/ GSEA file. '
                                  'Please refer to documentation for expected column order and content. '
                                  'If you do not have dotplot data to plot, or if you want to omit dotplots '
                                  'for whatever reason, then you can set DOTPLOTS to False in the config file. '
                                  'NOTE, however, that your ORA/ GSEA file still has to have the expected '
                                  'column order (see docs). ***')
    
    
    def test_read_in_ora_data_term_types_dict_3_10(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_3_10(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_10(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_term_genes_dict, {})

    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_10(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_3_10(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_terms, [])






    def test_read_in_ora_data_status_3_11(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(status, 3)
    
    
    def test_read_in_ora_data_message_3_11(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(message, '*** ERROR: Data for dotplots is not formatted as expected in ORA/ GSEA file. '
                                  'Please refer to documentation for expected column order and content. '
                                  'If you do not have dotplot data to plot, or if you want to omit dotplots '
                                  'for whatever reason, then you can set DOTPLOTS to False in the config file. '
                                  'NOTE, however, that your ORA/ GSEA file still has to have the expected '
                                  'column order (see docs). ***')
    
    
    def test_read_in_ora_data_term_types_dict_3_11(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_3_11(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_11(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_term_genes_dict, {})

    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_11(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_3_11(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_terms, [])



    def test_read_in_ora_data_status_3_12(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(status, 3)
    
    
    def test_read_in_ora_data_message_3_12(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(message, '*** ERROR: Data for dotplots is not formatted as expected in ORA/ GSEA file. '
                                  'Please refer to documentation for expected column order and content. '
                                  'If you do not have dotplot data to plot, or if you want to omit dotplots '
                                  'for whatever reason, then you can set DOTPLOTS to False in the config file. '
                                  'NOTE, however, that your ORA/ GSEA file still has to have the expected '
                                  'column order (see docs). ***')
    
    
    def test_read_in_ora_data_term_types_dict_3_12(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_3_12(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_12(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_term_genes_dict, {})

    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_12(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_3_12(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_terms, [])







    def test_read_in_ora_data_status_3_9b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_3_9b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_3_9b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_3_9b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol biosynthetic process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_9b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)


    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_9b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_term_dotplot_dict,{})
        
        
    
    def test_read_in_ora_data_exp_terms_3_9b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_terms, ['GO:0016126'])





    def test_read_in_ora_data_status_3_10b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_3_10b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_3_10b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_3_10b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol biosynthetic process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_10b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)


    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_10b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_term_dotplot_dict,{})
        
        
    
    def test_read_in_ora_data_exp_terms_3_10b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_terms, ['GO:0016126'])




    def test_read_in_ora_data_status_3_11b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_3_11b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_3_11b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_3_11b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol biosynthetic process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_11b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)


    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_11b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_term_dotplot_dict,{})
        
        
    
    def test_read_in_ora_data_exp_terms_3_11b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_terms, ['GO:0016126'])



    def test_read_in_ora_data_status_3_12b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_3_12b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_3_12b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_3_12b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol biosynthetic process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_12b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)


    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_12b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_term_dotplot_dict,{})
        
        
    
    def test_read_in_ora_data_exp_terms_3_12b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        test_stats['GO:0016127'] = (2, 0)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_terms, ['GO:0016126'])




    def test_read_in_ora_data_status_3_13(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(status, 3)
    
    
    def test_read_in_ora_data_message_3_13(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(message, '*** ERROR: Data for dotplots is not formatted as expected in ORA/ GSEA file. '
                                  'Please refer to documentation for expected column order and content. '
                                  'If you do not have dotplot data to plot, or if you want to omit dotplots '
                                  'for whatever reason, then you can set DOTPLOTS to False in the config file. '
                                  'NOTE, however, that your ORA/ GSEA file still has to have the expected '
                                  'column order (see docs). ***')
    
    
    def test_read_in_ora_data_term_types_dict_3_13(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_3_13(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_13(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_term_genes_dict, {})

    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_13(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_3_13(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_terms, [])


    def test_read_in_ora_data_status_3_14(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(status, 3)
    
    
    def test_read_in_ora_data_message_3_14(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(message, '*** ERROR: Data for dotplots is not formatted as expected in ORA/ GSEA file. '
                                  'Please refer to documentation for expected column order and content. '
                                  'If you do not have dotplot data to plot, or if you want to omit dotplots '
                                  'for whatever reason, then you can set DOTPLOTS to False in the config file. '
                                  'NOTE, however, that your ORA/ GSEA file still has to have the expected '
                                  'column order (see docs). ***')
    
    
    def test_read_in_ora_data_term_types_dict_3_14(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_3_14(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_14(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_term_genes_dict, {})

    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_14(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_3_14(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_terms, [])






    def test_read_in_ora_data_status_3_15(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(status, 3)
    
    
    def test_read_in_ora_data_message_3_15(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(message, '*** ERROR: Data for dotplots is not formatted as expected in ORA/ GSEA file. '
                                  'Please refer to documentation for expected column order and content. '
                                  'If you do not have dotplot data to plot, or if you want to omit dotplots '
                                  'for whatever reason, then you can set DOTPLOTS to False in the config file. '
                                  'NOTE, however, that your ORA/ GSEA file still has to have the expected '
                                  'column order (see docs). ***')
    
    
    def test_read_in_ora_data_term_types_dict_3_15(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_3_15(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_15(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_term_genes_dict, {})

    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_15(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_3_15(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,d,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_terms, [])



    def test_read_in_ora_data_status_3_16(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(status, 3)
    
    
    def test_read_in_ora_data_message_3_16(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        self.assertEqual(message, '*** ERROR: Data for dotplots is not formatted as expected in ORA/ GSEA file. '
                                  'Please refer to documentation for expected column order and content. '
                                  'If you do not have dotplot data to plot, or if you want to omit dotplots '
                                  'for whatever reason, then you can set DOTPLOTS to False in the config file. '
                                  'NOTE, however, that your ORA/ GSEA file still has to have the expected '
                                  'column order (see docs). ***')
    
    
    def test_read_in_ora_data_term_types_dict_3_16(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_3_16(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_16(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_term_genes_dict, {})

    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_16(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_3_16(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,e\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, True, test_stats)
        
        self.assertEqual(exp_terms, [])



    def test_read_in_ora_data_status_3_13b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_3_13b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_3_13b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_3_13b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol biosynthetic process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_13b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)


    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_13b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_term_dotplot_dict,{})
        
        
    
    def test_read_in_ora_data_exp_terms_3_13b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,a,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_terms, ['GO:0016126'])





    def test_read_in_ora_data_status_3_14b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_3_14b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_3_14b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_3_14b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol biosynthetic process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_14b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)


    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_14b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_term_dotplot_dict,{})
        
        
    
    def test_read_in_ora_data_exp_terms_3_14b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,b,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_terms, ['GO:0016126'])




    def test_read_in_ora_data_status_3_15b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_3_15b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_3_15b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_3_15b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol biosynthetic process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_15b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)


    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_15b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_term_dotplot_dict,{})
        
        
    
    def test_read_in_ora_data_exp_terms_3_15b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,c,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_terms, ['GO:0016126'])



    def test_read_in_ora_data_status_3_16b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(status, 0)
    
    
    def test_read_in_ora_data_message_3_16b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        self.assertEqual(message, '')
    
    
    def test_read_in_ora_data_term_types_dict_3_16b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_term_types_dict = {}
        test_term_types_dict['GO:0016126'] = 'GO'
        
        self.assertEqual(compare_dicts(term_types_dict, test_term_types_dict), 1)
        
    
    def test_read_in_ora_data_term_defs_dict_3_16b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        
        test_term_defs_dict = {}
        test_term_defs_dict['GO:0016126'] = 'sterol biosynthetic process'
        
        self.assertEqual(compare_dicts(term_defs_dict, test_term_defs_dict), 1)
        
    
    def test_read_in_ora_data_exp_term_genes_dict_3_16b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        test_exp_term_genes_dict = {}
        test_exp_term_genes_dict[('test_id', 'GO:0016126')] = \
                                    set(['Cyb5r1','Hsd17b7','Ebp','Nsdhl',
                                         'G6pdx','Fdps','Pmvk','Dhcr24','Cyp51',
                                         'Insig1','Por','Dhcr7','Lss','Msmo1',
                                         'Mvd','Fdft1','Hmgcr','Hmgcs1','Erg28','Sqle'])
    
        self.assertEqual(compare_dicts(exp_term_genes_dict, test_exp_term_genes_dict), 1)


    
    def test_read_in_ora_data_exp_term_dotplot_dict_3_16b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_term_dotplot_dict,{})
        
        
    
    def test_read_in_ora_data_exp_terms_3_16b(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.write('GO,GO:0016127,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,20\n')
        f.write('GO,GO:0016126,sterol biosynthetic process,20/1383,52/23210,5e-12,3e-08,8e-10,'
                'Cyb5r1/Hsd17b7/Ebp/Nsdhl/G6pdx/Fdps/Pmvk/Dhcr24/Cyp51/Insig1/Por/Dhcr7/Lss/'
                'Msmo1/Mvd/Fdft1/Hmgcr/Hmgcs1/Erg28/Sqle,d\n')
        f.close()
        
        test_stats = {}
        test_stats['GO:0016126'] = (1, 1)
        
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 1, 1, False, test_stats)
        
        self.assertEqual(exp_terms, ['GO:0016126'])



    def test_read_in_ora_data_status_4_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(status, 4)
    
    
    def test_read_in_ora_data_message_4_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(message, '*** ERROR: ORA (or GSEA) file not formatted correctly. '
                                  'In particular, it only has one row, which is assumed '
                                  'to be the header row and has been skipped. Please add '
                                  'either a header row or data rows to the file. ***')
    
    
    def test_read_in_ora_data_term_types_dict_4_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_4_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_4_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(exp_term_genes_dict, {})
    
    
    def test_read_in_ora_data_exp_term_dotplot_dict_4_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_4_1(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(exp_terms, [])
        
    
    def test_read_in_ora_data_status_4_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(status, 4)
    
    
    def test_read_in_ora_data_message_4_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(message, '*** ERROR: ORA (or GSEA) file not formatted correctly. '
                                  'In particular, it only has one row, which is assumed '
                                  'to be the header row and has been skipped. Please add '
                                  'either a header row or data rows to the file. ***')
    
    
    def test_read_in_ora_data_term_types_dict_4_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_4_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_4_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(exp_term_genes_dict, {})


    def test_read_in_ora_data_exp_term_dotplot_dict_4_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_4_2(self):
        f = open('test', 'a')
        f.write('Type,ID,Description,GeneRatio,BgRatio,pvalue,p.adjust,qvalue,geneID,Count\n')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(exp_terms, [])




    def test_read_in_ora_data_status_5_1(self):
        f = open('test', 'a')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(status, 5)
    
    
    def test_read_in_ora_data_message_5_1(self):
        f = open('test', 'a')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(message, '*** ERROR: ORA/ GSEA file is empty. ***')
    
    
    def test_read_in_ora_data_term_types_dict_5_1(self):
        f = open('test', 'a')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_5_1(self):
        f = open('test', 'a')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_5_1(self):
        f = open('test', 'a')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(exp_term_genes_dict, {})
    
    
    def test_read_in_ora_data_exp_term_dotplot_dict_5_1(self):
        f = open('test', 'a')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_5_1(self):
        f = open('test', 'a')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, False, {})
        self.assertEqual(exp_terms, [])
        
    
    def test_read_in_ora_data_status_5_2(self):
        f = open('test', 'a')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(status, 5)
    
    
    def test_read_in_ora_data_message_5_2(self):
        f = open('test', 'a')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(message, '*** ERROR: ORA/ GSEA file is empty. ***')
    
    
    def test_read_in_ora_data_term_types_dict_5_2(self):
        f = open('test', 'a')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(term_types_dict, {})
        
    
    def test_read_in_ora_data_term_defs_dict_5_2(self):
        f = open('test', 'a')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(term_defs_dict, {})
        
    
    def test_read_in_ora_data_exp_term_genes_dict_5_2(self):
        f = open('test', 'a')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(exp_term_genes_dict, {})


    def test_read_in_ora_data_exp_term_dotplot_dict_5_2(self):
        f = open('test', 'a')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(exp_term_dotplot_dict, {})
        
    
    def test_read_in_ora_data_exp_terms_5_2(self):
        f = open('test', 'a')
        f.close()
        (status, message, term_types_dict, term_defs_dict, exp_term_genes_dict, \
         exp_term_dotplot_dict, exp_terms) = \
                         gf_base.read_in_ora_data('test', 'test_id', 0, 0, True, {})
        self.assertEqual(exp_terms, [])

       
    def test_make_gene_qd_dict_status_0_1(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(status, 0)
        os.remove('test')
        
    def test_make_gene_qd_dict_message_0_1(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(message, '')
        os.remove('test')
        
    def test_make_gene_qd_dict_dict_0_1(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        tester_dict = {}
        tester_dict[('test_id', 'a')] = 1.0
        self.assertEqual(compare_dicts(gene_qd_dict, tester_dict), 1)
        os.remove('test')
        
    def test_make_gene_qd_dict_status_0_1b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(status, 0)
        os.remove('test')
        
    def test_make_gene_qd_dict_message_0_1b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(message, '')
        os.remove('test')
        
    def test_make_gene_qd_dict_dict_0_1b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        tester_dict = {}
        tester_dict[('test_id', 'a')] = 1.0
        self.assertEqual(compare_dicts(gene_qd_dict, tester_dict), 1)
        os.remove('test')

    def test_make_gene_qd_dict_status_0_2(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('b,2.0\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(status, 0)
        os.remove('test')
        
    def test_make_gene_qd_dict_message_0_2(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('b,2.0\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(message, '')
        os.remove('test')
        
    def test_make_gene_qd_dict_dict_0_2(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('b,2.0\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        tester_dict = {}
        tester_dict[('test_id', 'a')] = 1.0
        tester_dict[('test_id', 'b')] = 2.0
        self.assertEqual(compare_dicts(gene_qd_dict, tester_dict), 1)
        os.remove('test')

    def test_make_gene_qd_dict_status_0_2b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('b,2.0')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(status, 0)
        os.remove('test')
        
    def test_make_gene_qd_dict_message_0_2b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('b,2.0')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(message, '')
        os.remove('test')
        
    def test_make_gene_qd_dict_dict_0_2b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('b,2.0')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        tester_dict = {}
        tester_dict[('test_id', 'a')] = 1.0
        tester_dict[('test_id', 'b')] = 2.0
        self.assertEqual(compare_dicts(gene_qd_dict, tester_dict), 1)
        os.remove('test')
        
    def test_make_gene_qd_dict_status_0_3(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('b,-3e3\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(status, 0)
        os.remove('test')
        
    def test_make_gene_qd_dict_message_0_3(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('b,-3e3\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(message, '')
        os.remove('test')
        
    def test_make_gene_qd_dict_dict_0_3(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('b,-3e3\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        tester_dict = {}
        tester_dict[('test_id', 'a')] = 1.0
        tester_dict[('test_id', 'b')] = -3000.0
        self.assertEqual(compare_dicts(gene_qd_dict, tester_dict), 1)
        os.remove('test')

    def test_make_gene_qd_dict_status_0_3b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('b,-3e3')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(status, 0)
        os.remove('test')
        
    def test_make_gene_qd_dict_message_0_3b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('b,-3e3')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(message, '')
        os.remove('test')
        
    def test_make_gene_qd_dict_dict_0_3b(self):
        """no carriage return"""
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('b,-3e3')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        tester_dict = {}
        tester_dict[('test_id', 'a')] = 1.0
        tester_dict[('test_id', 'b')] = -3000.0
        self.assertEqual(compare_dicts(gene_qd_dict, tester_dict), 1)
        os.remove('test')


    def test_make_gene_qd_dict_status_0_4(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1,2,3,q,w\n')
        f.write('b,-3e3\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(status, 0)
        os.remove('test')
        
    def test_make_gene_qd_dict_message_0_4(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1,2,3,q,w\n')
        f.write('b,-3e3\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(message, '')
        os.remove('test')
        
    def test_make_gene_qd_dict_dict_0_4(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1,2,3,q,w\n')
        f.write('b,-3e3\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        tester_dict = {}
        tester_dict[('test_id', 'a')] = 1.0
        tester_dict[('test_id', 'b')] = -3000.0
        self.assertEqual(compare_dicts(gene_qd_dict, tester_dict), 1)
        os.remove('test')
        
        
    def test_make_gene_qd_dict_status_1_1(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(status, 1)
        os.remove('test')
        
    def test_make_gene_qd_dict_message_1_1(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(message, ('*** ERROR: Gene quantitative data file (usually gene '
                                   'expression/ log2 FC) not formatted correctly. '
                                   'Check the number of fields in each line, and compare '
                                   'this to GENE_INDEX and QD_INDEX in appx_config.py. '
                                   'Also check that the quantitative data column contains '
                                   'numbers only, and that there are no empty lines. ***'))
        os.remove('test')
        
    def test_make_gene_qd_dict_dict_1_1(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(gene_qd_dict, {})
        os.remove('test')
    
    
    def test_make_gene_qd_dict_status_1_2(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 2)
        self.assertEqual(status, 1)
        os.remove('test')
        
    def test_make_gene_qd_dict_message_1_2(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 2)
        self.assertEqual(message, ('*** ERROR: Gene quantitative data file (usually gene '
                                   'expression/ log2 FC) not formatted correctly. '
                                   'Check the number of fields in each line, and compare '
                                   'this to GENE_INDEX and QD_INDEX in appx_config.py. '
                                   'Also check that the quantitative data column contains '
                                   'numbers only, and that there are no empty lines. ***'))
        os.remove('test')
        
    def test_make_gene_qd_dict_dict_1_2(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 2)
        self.assertEqual(gene_qd_dict, {})
        os.remove('test')
        
    
    def test_make_gene_qd_dict_status_1_3(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 2, 0)
        self.assertEqual(status, 1)
        os.remove('test')
        
    def test_make_gene_qd_dict_message_1_3(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 2, 0)
        self.assertEqual(message, ('*** ERROR: Gene quantitative data file (usually gene '
                                   'expression/ log2 FC) not formatted correctly. '
                                   'Check the number of fields in each line, and compare '
                                   'this to GENE_INDEX and QD_INDEX in appx_config.py. '
                                   'Also check that the quantitative data column contains '
                                   'numbers only, and that there are no empty lines. ***'))
        os.remove('test')
        
    def test_make_gene_qd_dict_dict_1_3(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 2, 0)
        self.assertEqual(gene_qd_dict, {})
        os.remove('test')
        
    def test_make_gene_qd_dict_status_1_4(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('a\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(status, 1)
        os.remove('test')
        
    def test_make_gene_qd_dict_message_1_4(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('a\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(message, ('*** ERROR: Gene quantitative data file (usually gene '
                                   'expression/ log2 FC) not formatted correctly. '
                                   'Check the number of fields in each line, and compare '
                                   'this to GENE_INDEX and QD_INDEX in appx_config.py. '
                                   'Also check that the quantitative data column contains '
                                   'numbers only, and that there are no empty lines. ***'))
        os.remove('test')
        
    def test_make_gene_qd_dict_dict_1_4(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('a\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(gene_qd_dict, {})
        os.remove('test')
        
    def test_make_gene_qd_dict_status_1_5(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(status, 1)
        os.remove('test')
        
    def test_make_gene_qd_dict_message_1_5(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(message, ('*** ERROR: Gene quantitative data file (usually gene '
                                   'expression/ log2 FC) not formatted correctly. '
                                   'Check the number of fields in each line, and compare '
                                   'this to GENE_INDEX and QD_INDEX in appx_config.py. '
                                   'Also check that the quantitative data column contains '
                                   'numbers only, and that there are no empty lines. ***'))
        os.remove('test')
        
    def test_make_gene_qd_dict_dict_1_5(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(gene_qd_dict, {})
        os.remove('test')
        
    def test_make_gene_qd_dict_status_1_6(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,b\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(status, 1)
        os.remove('test')
        
    def test_make_gene_qd_dict_message_1_6(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,b\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(message, ('*** ERROR: Gene quantitative data file (usually gene '
                                   'expression/ log2 FC) not formatted correctly. '
                                   'Check the number of fields in each line, and compare '
                                   'this to GENE_INDEX and QD_INDEX in appx_config.py. '
                                   'Also check that the quantitative data column contains '
                                   'numbers only, and that there are no empty lines. ***'))
        os.remove('test')
        
    def test_make_gene_qd_dict_dict_1_6(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,b\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(gene_qd_dict, {})
        os.remove('test')
        
    def test_make_gene_qd_dict_status_1_7(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('a,b\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(status, 1)
        os.remove('test')
        
    def test_make_gene_qd_dict_message_1_7(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('a,b\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(message, ('*** ERROR: Gene quantitative data file (usually gene '
                                   'expression/ log2 FC) not formatted correctly. '
                                   'Check the number of fields in each line, and compare '
                                   'this to GENE_INDEX and QD_INDEX in appx_config.py. '
                                   'Also check that the quantitative data column contains '
                                   'numbers only, and that there are no empty lines. ***'))
        os.remove('test')
        
    def test_make_gene_qd_dict_dict_1_7(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('a,b\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(gene_qd_dict, {})
        os.remove('test')
        
    def test_make_gene_qd_dict_status_1_8(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,b\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(status, 1)
        os.remove('test')
        
    def test_make_gene_qd_dict_message_1_8(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,b\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(message, ('*** ERROR: Gene quantitative data file (usually gene '
                                   'expression/ log2 FC) not formatted correctly. '
                                   'Check the number of fields in each line, and compare '
                                   'this to GENE_INDEX and QD_INDEX in appx_config.py. '
                                   'Also check that the quantitative data column contains '
                                   'numbers only, and that there are no empty lines. ***'))
        os.remove('test')
        
    def test_make_gene_qd_dict_dict_1_8(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,b\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(gene_qd_dict, {})
        os.remove('test')
        
    def test_make_gene_qd_dict_status_1_9(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(status, 1)
        os.remove('test')
        
    def test_make_gene_qd_dict_message_1_9(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(message, ('*** ERROR: Gene quantitative data file (usually gene '
                                   'expression/ log2 FC) not formatted correctly. '
                                   'Check the number of fields in each line, and compare '
                                   'this to GENE_INDEX and QD_INDEX in appx_config.py. '
                                   'Also check that the quantitative data column contains '
                                   'numbers only, and that there are no empty lines. ***'))
        os.remove('test')
        
    def test_make_gene_qd_dict_dict_1_9(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(gene_qd_dict, {})
        os.remove('test')
        
    def test_make_gene_qd_dict_status_1_10(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(status, 1)
        os.remove('test')
        
    def test_make_gene_qd_dict_message_1_10(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(message, ('*** ERROR: Gene quantitative data file (usually gene '
                                   'expression/ log2 FC) not formatted correctly. '
                                   'Check the number of fields in each line, and compare '
                                   'this to GENE_INDEX and QD_INDEX in appx_config.py. '
                                   'Also check that the quantitative data column contains '
                                   'numbers only, and that there are no empty lines. ***'))
        os.remove('test')
        
    def test_make_gene_qd_dict_dict_1_10(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(gene_qd_dict, {})
        os.remove('test')
        
    def test_make_gene_qd_dict_status_1_11(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(status, 1)
        os.remove('test')
        
    def test_make_gene_qd_dict_message_1_11(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(message, ('*** ERROR: Gene quantitative data file (usually gene '
                                   'expression/ log2 FC) not formatted correctly. '
                                   'Check the number of fields in each line, and compare '
                                   'this to GENE_INDEX and QD_INDEX in appx_config.py. '
                                   'Also check that the quantitative data column contains '
                                   'numbers only, and that there are no empty lines. ***'))
        os.remove('test')
        
    def test_make_gene_qd_dict_dict_1_11(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(gene_qd_dict, {})
        os.remove('test')


    def test_make_gene_qd_dict_status_2_1(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(status, 2)
        os.remove('test')
        
    def test_make_gene_qd_dict_message_2_1(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(message, ('*** ERROR: Gene repeated in gene quantitative data '
                                   'file for experiment with ID: test_id. ***'))
        os.remove('test')
        
    def test_make_gene_qd_dict_dict_2_1(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(gene_qd_dict, {})
        os.remove('test')
        
        
    def test_make_gene_qd_dict_status_2_2(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('b,1\n')
        f.write('a,1\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(status, 2)
        os.remove('test')
        
    def test_make_gene_qd_dict_message_2_2(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('b,1\n')
        f.write('a,1\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(message, ('*** ERROR: Gene repeated in gene quantitative data '
                                   'file for experiment with ID: test_id. ***'))
        os.remove('test')
        
    def test_make_gene_qd_dict_dict_2_2(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('b,1\n')
        f.write('a,1\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(gene_qd_dict, {})
        os.remove('test')
        
    def test_make_gene_qd_dict_status_2_3(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('b,1\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(status, 2)
        os.remove('test')
        
    def test_make_gene_qd_dict_message_2_3(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('b,1\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(message, ('*** ERROR: Gene repeated in gene quantitative data '
                                   'file for experiment with ID: test_id. ***'))
        os.remove('test')
        
    def test_make_gene_qd_dict_dict_2_3(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('b,1\n')
        f.write('a,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(gene_qd_dict, {})
        os.remove('test')
        
    def test_make_gene_qd_dict_status_2_4(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('a,1\n')
        f.write('b,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(status, 2)
        os.remove('test')
        
    def test_make_gene_qd_dict_message_2_4(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('a,1\n')
        f.write('b,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(message, ('*** ERROR: Gene repeated in gene quantitative data '
                                   'file for experiment with ID: test_id. ***'))
        os.remove('test')
        
    def test_make_gene_qd_dict_dict_2_4(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.write('a,1\n')
        f.write('a,1\n')
        f.write('b,1\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(gene_qd_dict, {})
        os.remove('test')
        
    def test_make_gene_qd_dict_status_3_1(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(status, 3)
        os.remove('test')
        
    def test_make_gene_qd_dict_message_3_1(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(message, ('*** ERROR: Gene quantitative data file (usually gene '
                                   'expression/ log2 FC) not formatted correctly. '
                                   'In particular, it only has one row, which is assumed '
                                   'to be the header row and has been skipped. Please add '
                                   'either a header row or data rows to the file. ***'))
        os.remove('test')
        
    def test_make_gene_qd_dict_dict_3_1(self):
        f = open('test', 'a')
        f.write('gene,log2FC\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(gene_qd_dict, {})
        os.remove('test')

    def test_make_gene_qd_dict_status_3_2(self):
        f = open('test', 'a')
        f.write('\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(status, 3)
        os.remove('test')
        
    def test_make_gene_qd_dict_message_3_2(self):
        f = open('test', 'a')
        f.write('\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(message, ('*** ERROR: Gene quantitative data file (usually gene '
                                   'expression/ log2 FC) not formatted correctly. '
                                   'In particular, it only has one row, which is assumed '
                                   'to be the header row and has been skipped. Please add '
                                   'either a header row or data rows to the file. ***'))
        os.remove('test')
        
    def test_make_gene_qd_dict_dict_3_2(self):
        f = open('test', 'a')
        f.write('\n')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(gene_qd_dict, {})
        os.remove('test')
        
    def test_make_gene_qd_dict_status_4_1(self):
        f = open('test', 'a')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(status, 4)
        os.remove('test')
        
    def test_make_gene_qd_dict_message_4_1(self):
        f = open('test', 'a')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(message, ('*** ERROR: Gene quantitative data file (usually gene '
                                   'expression/ log2 FC) is empty. ***'))
        os.remove('test')
        
    def test_make_gene_qd_dict_dict_4_1(self):
        f = open('test', 'a')
        f.close()
        (status, message, gene_qd_dict) = gf_base.make_gene_qd_dict('test', 'test_id', 0, 1)
        self.assertEqual(gene_qd_dict, {})
        os.remove('test')

    
    def test_find_terms_to_remove_old(self):
        exp_terms_dict = {}
        exp_terms_dict['exp1'] = ['t1', 't2', 't3', 't4', 't5', 't7']
        exp_terms_dict['exp2'] = ['t2', 't3', 't6', 't7']
        exp_terms_dict['exp3'] = ['t4', 't6', 't7']
        exp_terms_dict['exp4'] = ['t8']
        
        exp_term_genes_dict = {}
        exp_term_genes_dict[('exp1', 't1')] = set(['A', 'B', 'C'])
        exp_term_genes_dict[('exp1', 't2')] = set(['E', 'F', 'G'])
        exp_term_genes_dict[('exp1', 't3')] = set(['H', 'I', 'J'])
        exp_term_genes_dict[('exp1', 't4')] = set(['K', 'L', 'M'])
        exp_term_genes_dict[('exp1', 't5')] = set(['N', 'O'])
        exp_term_genes_dict[('exp1', 't7')] = set(['Q', 'R', 'S'])
        exp_term_genes_dict[('exp2', 't2')] = set(['F', 'G', 'H'])
        exp_term_genes_dict[('exp2', 't3')] = set(['K', 'L'])
        exp_term_genes_dict[('exp2', 't6')] = set(['T', 'U', 'V'])
        exp_term_genes_dict[('exp2', 't7')] = set(['Q'])
        exp_term_genes_dict[('exp3', 't4')] = set(['M', 'N', 'O', 'P'])
        exp_term_genes_dict[('exp3', 't6')] = set(['T', 'U', 'V'])
        exp_term_genes_dict[('exp3', 't7')] = set(['S'])
        exp_term_genes_dict[('exp4', 't8')] = set(['W'])
        
        terms_to_remove = gf_base.find_terms_to_remove_old(exp_terms_dict, exp_term_genes_dict, 4)
        
        self.assertEqual(sorted(terms_to_remove), ['t1', 't5', 't6', 't7', 't8'])
        
        
    def test_find_terms_to_remove_aux(self):
        term_genes_dict = {}
        term_genes_dict['t1'] = set(['A', 'B', 'C'])
        term_genes_dict['t2'] = set(['E', 'F', 'G', 'H'])
        term_genes_dict['t3'] = set(['H', 'I', 'J', 'K', 'L'])
        term_genes_dict['t4'] = set(['K', 'L', 'M', 'N', 'O', 'P'])
        term_genes_dict['t5'] = set(['N', 'O'])
        term_genes_dict['t6'] = set(['T', 'U', 'V'])
        term_genes_dict['t7'] = set(['Q', 'R', 'S'])
        term_genes_dict['t8'] = set(['W'])
        
        terms_to_remove = gf_base.find_terms_to_remove_aux(term_genes_dict, 4)
        
        self.assertEqual(sorted(terms_to_remove), ['t1', 't5', 't6', 't7', 't8'])
        
    
    def test_find_terms_to_remove_1(self):
        exp_term_genes_dict = {}
        exp_term_genes_dict[('exp1', 't1')] = set(['A', 'B', 'C'])
        exp_term_genes_dict[('exp1', 't2')] = set(['E', 'F', 'G'])
        exp_term_genes_dict[('exp1', 't3')] = set(['H', 'I', 'J'])
        exp_term_genes_dict[('exp1', 't4')] = set(['K', 'L', 'M'])
        exp_term_genes_dict[('exp1', 't5')] = set(['N', 'O'])
        exp_term_genes_dict[('exp1', 't7')] = set(['Q', 'R', 'S'])
        exp_term_genes_dict[('exp2', 't2')] = set(['F', 'G', 'H'])
        exp_term_genes_dict[('exp2', 't3')] = set(['K', 'L'])
        exp_term_genes_dict[('exp2', 't6')] = set(['T', 'U', 'V'])
        exp_term_genes_dict[('exp2', 't7')] = set(['Q'])
        exp_term_genes_dict[('exp3', 't4')] = set(['M', 'N', 'O', 'P'])
        exp_term_genes_dict[('exp3', 't6')] = set(['T', 'U', 'V'])
        exp_term_genes_dict[('exp3', 't7')] = set(['S'])
        exp_term_genes_dict[('exp4', 't8')] = set(['W'])
        
        
        (term_genes_dict, terms_to_remove) = gf_base.find_terms_to_remove(exp_term_genes_dict, 4)
        
        tester_dict = {}
        tester_dict['t1'] = set(['A', 'B', 'C'])
        tester_dict['t2'] = set(['E', 'F', 'G', 'H'])
        tester_dict['t3'] = set(['H', 'I', 'J', 'K', 'L'])
        tester_dict['t4'] = set(['K', 'L', 'M', 'N', 'O', 'P'])
        tester_dict['t5'] = set(['N', 'O'])
        tester_dict['t6'] = set(['T', 'U', 'V'])
        tester_dict['t7'] = set(['Q', 'R', 'S'])
        tester_dict['t8'] = set(['W'])

        self.assertEqual(compare_dicts(term_genes_dict, tester_dict), 1)
   

    def test_find_terms_to_remove_2(self):
        exp_term_genes_dict = {}
        exp_term_genes_dict[('exp1', 't1')] = set(['A', 'B', 'C'])
        exp_term_genes_dict[('exp1', 't2')] = set(['E', 'F', 'G'])
        exp_term_genes_dict[('exp1', 't3')] = set(['H', 'I', 'J'])
        exp_term_genes_dict[('exp1', 't4')] = set(['K', 'L', 'M'])
        exp_term_genes_dict[('exp1', 't5')] = set(['N', 'O'])
        exp_term_genes_dict[('exp1', 't7')] = set(['Q', 'R', 'S'])
        exp_term_genes_dict[('exp2', 't2')] = set(['F', 'G', 'H'])
        exp_term_genes_dict[('exp2', 't3')] = set(['K', 'L'])
        exp_term_genes_dict[('exp2', 't6')] = set(['T', 'U', 'V'])
        exp_term_genes_dict[('exp2', 't7')] = set(['Q'])
        exp_term_genes_dict[('exp3', 't4')] = set(['M', 'N', 'O', 'P'])
        exp_term_genes_dict[('exp3', 't6')] = set(['T', 'U', 'V'])
        exp_term_genes_dict[('exp3', 't7')] = set(['S'])
        exp_term_genes_dict[('exp4', 't8')] = set(['W'])
        
        
        (term_genes_dict, terms_to_remove) = gf_base.find_terms_to_remove(exp_term_genes_dict, 4)

        self.assertEqual(sorted(terms_to_remove), ['t1', 't5', 't6', 't7', 't8'])
        
    
    def test_find_terms_to_remove_3(self):
        exp_terms_dict = {}
        exp_terms_dict['exp1'] = ['t1', 't2', 't3', 't4', 't5', 't7']
        exp_terms_dict['exp2'] = ['t2', 't3', 't6', 't7']
        exp_terms_dict['exp3'] = ['t4', 't6', 't7']
        exp_terms_dict['exp4'] = ['t8']
        
        exp_term_genes_dict = {}
        exp_term_genes_dict[('exp1', 't1')] = set(['A', 'B', 'C'])
        exp_term_genes_dict[('exp1', 't2')] = set(['E', 'F', 'G'])
        exp_term_genes_dict[('exp1', 't3')] = set(['H', 'I', 'J'])
        exp_term_genes_dict[('exp1', 't4')] = set(['K', 'L', 'M'])
        exp_term_genes_dict[('exp1', 't5')] = set(['N', 'O'])
        exp_term_genes_dict[('exp1', 't7')] = set(['Q', 'R', 'S'])
        exp_term_genes_dict[('exp2', 't2')] = set(['F', 'G', 'H'])
        exp_term_genes_dict[('exp2', 't3')] = set(['K', 'L'])
        exp_term_genes_dict[('exp2', 't6')] = set(['T', 'U', 'V'])
        exp_term_genes_dict[('exp2', 't7')] = set(['Q'])
        exp_term_genes_dict[('exp3', 't4')] = set(['M', 'N', 'O', 'P'])
        exp_term_genes_dict[('exp3', 't6')] = set(['T', 'U', 'V'])
        exp_term_genes_dict[('exp3', 't7')] = set(['S'])
        exp_term_genes_dict[('exp4', 't8')] = set(['W'])
        
        (term_genes_dict, terms_to_remove) = gf_base.find_terms_to_remove(exp_term_genes_dict, 4)
        terms_to_remove_old = gf_base.find_terms_to_remove_old(exp_terms_dict, exp_term_genes_dict, 4)
        
        self.assertEqual(sorted(terms_to_remove), sorted(terms_to_remove_old))
        
if __name__ == '__main__':
    unittest.main()
