import pytest
import os
import pandas as pd
datadir = os.path.abspath(os.path.dirname(__file__)) + '/test_data'
from pyfiles import trainmodel as tm

def test_modeleval():
    prediction = [0, 0, 1, 1, 2]
    actual = [0, 2, 1, 1, 2]
    
    acc = tm.model_eval(prediction, actual)
    assert acc == 0.8
    
def test_loaddata():
    comppth = datadir + '/processed_data/featurescomp.pkl'
    data, labels_enc, label_classes = tm.load_data(datadir, filenamenp = '/processed_data/featurescomp.pkl', filenamecsv = '/processed_data/cleanwcountscomp.csv')
    
    comp = pd.read_pickle(comppth)
    check = data.equals(comp)
    assert check
    
    enccheck = [0,1,1,0,0]
    check = labels_enc == enccheck
    assert check.all()
    
    classescheck = ['testone','testtwo']
    check = label_classes == classescheck
    assert check.all()
    
    
    