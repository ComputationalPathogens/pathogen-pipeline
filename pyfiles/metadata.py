import csv
import numpy as np
import pandas as pd
import os
from collections import Counter


def build_metadata(datadir):
    filename = datadir + '/processed_data/metadata.csv'
    datapth = datadir + '/refseq/bacteria/'
    f = open(filename, 'w', newline='')
    writer = csv.writer(f)
    id = -1
    #change over to use pandas write_csv
    for subdir, dirs, files in os.walk(datapth):
        dirs.sort()
        files.sort()
        pth, assembly, organism, genus, species, cnt = '', '', '', '', '', ''
        for file in files:
            ext = os.path.splitext(file)[-1].lower()
            if ext == ".fna":
                filename = os.path.splitext(file)[0]
                pth = subdir + '/' + filename + '.fna'
            if ext == ".fa":
                filename = os.path.splitext(file)[0]
                cnt = subdir + '/' + filename + '.fa'
            if ext == ".gz":
                filename = os.path.splitext(file)[0]
                fastapth = subdir + '/' + filename
                pth = subdir + '/' + filename + '.fna'
                cmd = 'gunzip ' + fastapth
                os.system(cmd)
            if ext == ".txt":
                fp = subdir + '/' + file
                with open(fp, 'r') as f:
                    lines = f.readlines()
                count = 0
                for line in lines:
                    #change to lines[0] and lines[1] directly grabbing?
                    count += 1
                    if count == 1:
                        assembly = line
                        assembly = assembly[18:]
                    if count == 2:
                        #safer way of parsing this text later?
                        organism = line
                        organism = organism[18:]
                        species = organism.split(" ")
                        genus = species[0]
                        species = species[1]
                        if species == 'sp.':
                            species = "unknown"
                    if count == 3:
                        break
        if id > -1:
            writer.writerow([id, assembly, genus, species, pth, cnt])
        id += 1

    return datadir

def clean_outliers(k, datadir):
    """
    k - the amount of folds for cross fold validation, will remove any classes
    with less than k occurences for stratified k-fold
    """
    k = int(k)
    colnames = ['id', 'assembly', 'genus', 'species', 'seqfile', 'cntfile']
    csvpth = datadir + '/processed_data/metadata.csv'
    data2 = pd.read_csv(csvpth, names=colnames)
    species = data2.species.tolist()
    labels = np.asarray(species)
    count = Counter(labels)
    for index, row in data2.iterrows():
        if count[row['species']] < k:
            data2.drop(index, axis=0, inplace=True)

    cleanpth = datadir + '/processed_data/clean.csv'
    data2.to_csv(cleanpth, index=False, header=False)
    return datadir
