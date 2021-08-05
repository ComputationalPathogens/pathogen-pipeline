import pytest
import os
import sys
import pandas as pd
datadir = os.path.abspath(os.path.dirname(__file__)) + '/test_data'
from pyfiles import metadata as md

def test_metadata():
    filepth = datadir + '/processed_data/metadata.csv'
    cmppth = datadir + '/processed_data/metadatacomp.csv'
    md.build_metadata(datadir)
    colnames = ['id', 'assembly', 'genus', 'species', 'seqfile', 'cntfile']
    data = pd.read_csv(filepth, names=colnames)
    compare = pd.read_csv(cmppth, names=colnames)
    assert data.equals(compare)

def test_clean():
    filepth = datadir + '/processed_data/clean.csv'
    cmppth = datadir + '/processed_data/cleancomp.csv'
    md.clean_outliers(2, datadir, filename = '/processed_data/metadatacomp.csv')
    colnames = ['id', 'assembly', 'genus', 'species', 'seqfile', 'cntfile']
    data = pd.read_csv(filepth, names=colnames)
    compare = pd.read_csv(cmppth, names=colnames)
    assert data.equals(compare)


