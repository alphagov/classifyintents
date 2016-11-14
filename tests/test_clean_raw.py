import nose.tools as nt
import os, sys
import pandas as pd
from classify import *
import numpy as np

class TestCleanUrls:
    
    # Would be run before each class method

    #def setup(self):

    # To run after each class method

    #def teardown(self):
    
    # To run when the class is instantiated.

    @classmethod
    def setup_class(self):
                
        print('Loading test_data/raw_test_data.csv into survey class')
        print('This test dataset tests basic functionality')
        
        self.a = classify.survey()
        self.a.load('test_data/raw_test_data.csv')
        self.a.clean_raw()
        self.columns = self.a.data.columns.tolist().sort()

        # Note fillna otherwise this test will fail!

        self.clean_raw_expected_columns = pd.read_csv('test_data/data_clean_raw_expected_columns.csv',skip_blank_lines=False).fillna('')
        self.clean_raw_expected_columns = self.clean_raw_expected_columns['columns'].tolist().sort()
   
    #@classmethod
    #def teardown_class(cls):
    #    print ("teardown_class() after any methods in this class")

    # Test whether it works on a single instance

    def test_unique_pages_df(self):

        nt.assert_equal(
                self.columns, 
                self.clean_raw_expected_columns
                )

