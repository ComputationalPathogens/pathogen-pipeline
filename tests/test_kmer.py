import pytest
import os
import sys
import pandas as pd
from pyfiles import kmer as km
datadir = os.path.abspath(os.path.dirname(__file__)) + '/test_data'

def test_kmer():
    filepth = datadir + '/processed_data/cleanwcounts.csv'
    cmppth = datadir + '/processed_data/cleanwcountscomp.csv'
    km.count_kmer(datadir, filename = '/processed_data/cleancomp.csv')
    colnames = ['id', 'assembly', 'genus', 'species', 'seqfile', 'cntfile','meta']
    data = pd.read_csv(filepth, names=colnames)
    compare = pd.read_csv(cmppth, names=colnames)
    assert data.equals(compare)