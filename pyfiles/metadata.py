import csv
import numpy as np
import pandas as pd
import os
from collections import Counter


def build_metadata(datadir, filename = '/processed_data/metadata.csv'):

    """
    Parameters
    ----------
    datadir : Base directory of nextflow execution

    Returns
    -------
    datadir : Base directory of nextflow execution
    
    Disc
    ----
    Generates a .csv to record the Assembly#, Genus, Species and file paths
    for complete genome sequences/kmer counts

    """
    filepth = datadir + filename
    datapth = datadir + '/refseq/bacteria/'
    f = open(filepth, 'w', newline='')
    writer = csv.writer(f)
    id = -1
    #change over to use pandas write_csv
    for subdir, dirs, files in os.walk(datapth):
        dirs.sort()
        files.sort()
        pth, assembly, organism, genus, species, cnt = 'empty', 'empty', 'empty', 'empty', 'empty', 'empty'
        for file in files:
            ext = os.path.splitext(file)[-1].lower()
            if ext == ".fna":
                name = os.path.splitext(file)[0]
                pth = '/refseq/bacteria/' + name + '/' + name + '.fna'
            if ext == ".gz":
                name = os.path.splitext(file)[0]
                name = os.path.splitext(name)[0]
                fastapth = subdir + '/' + name
                pth = '/refseq/bacteria/' + name + '/' + name + '.fna'
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

def clean_outliers(k, datadir, filename = '/processed_data/metadata.csv'):
    """
    Parameters
    ----------
    k : The amount of folds for k-fold validation, will remove any classes with
    less than k occurences so stratified k-fold can be used
    
    datadir : Base directory of nextflow execution

    Returns
    -------
    datadir : Base directory of nextflow execution
    
    Disc
    ----
    'Cleans' data by removing any samples with less than k occurences so data
    can be used in stratified k-fold

    """
    k = int(k)
    colnames = ['id', 'assembly', 'genus', 'species', 'seqfile', 'cntfile']
    csvpth = datadir + filename
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
