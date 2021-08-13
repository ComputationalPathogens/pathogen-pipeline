import pytest
import os
import pandas as pd
datadir = os.path.abspath(os.path.dirname(__file__)) + '/test_data'
from pyfiles import matrix as m

def test_matrix():
    filepth = datadir + '/processed_data/features.pkl'
    cmppth = datadir + '/processed_data/featurescomp.pkl'
    
    #if __name__ == '__main__':
    m.build_matrix(datadir, filename = '/processed_data/cleanwcountscomp.csv')
    data = pd.read_pickle(filepth)
    comp = pd.read_pickle(cmppth)
    check = data.equals(comp)
    assert check
        