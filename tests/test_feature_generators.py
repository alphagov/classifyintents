import nose.tools as nt
import os, sys
import pandas as pd
from classifyintents import *
import numpy as np

class TestFeatureGenerators:
    
    # Would be run before each class method

    #def setup(self):

    # To run after each class method

    #def teardown(self):
    
    # To run when the class is instantiated.

    @classmethod
    def setup_class(self):
                
        print('Testing functions which clean and create new features')
        
        self.test_case = pd.Series([
        '-', ' ', 'none,','What is my purpose?','You pass butter'
        ])

        self.expected_str_len = pd.Series([
        -0.400000,-0.452632,-0.031579,0.547368,0.336842
        ])      

    # No teardown required
    #@classmethod
    #def teardown_class(cls):
    #    print ("teardown_class() after any methods in this class")

    # Test whether it works on a single instance


    def test_string_len__works_as_expected(self):

        actual_str_len = string_len(self.test_case)
        
        print(actual_str_len)
        
        nt.assert_true(
            all(np.isclose(self.expected_str_len, actual_str_len))
            )

