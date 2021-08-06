import pytest
import os
import sys
import numpy as np
datadir = os.path.abspath(os.path.dirname(__file__)) + '/test_data'
from pyfiles import matrix as m

def test_matrix():
    filepth = datadir + '/processed_data/features.npy'
    cmppth = datadir + '/processed_data/featurescomp.npy'
    
    #if __name__ == '__main__':
    m.build_matrix(datadir, filename = '/processed_data/cleanwcountscomp.csv')
    data = np.load(filepth)
    comp = np.load(cmppth)
    check = data == comp
    assert check.all()
        