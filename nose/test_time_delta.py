# Give the correct context for the tests relative to the module itself
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from classify import *
import pandas as pd


a = pd.to_datetime('2016-01-02')
b = pd.to_datetime('2016-01-01')

#def test_time_delta():

def time_delta(x,y):
    
    # Expects datetime objects

    delta = x - y
    delta = delta.astype('timedelta64[s]')
    delta = normalise(delta.astype('int'))
    return(delta)

def normalise(x):
    
    x = (x - np.mean(x)) / np.std(x)
    return(x)
