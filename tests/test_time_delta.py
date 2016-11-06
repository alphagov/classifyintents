# Give the correct context for the tests relative to the module itself

import os
import sys
sys.path.insert(0, os.path.abspath('..'))
import pandas as pd
from classify.classify import *


a = pd.to_datetime('2016-01-02')
b = pd.to_datetime('2016-01-01')

def test_time_delta():

    classify.time_delta(a,b)

    return(True)
