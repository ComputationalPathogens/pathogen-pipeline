import itertools
import os
import csv
import Bio
import pandas as pd
from Bio import Seq, SeqIO
import numpy as np
from numpy import save, savetxt, load, loadtxt
from concurrent.futures import ProcessPoolExecutor

def get_file_names(filepth):

    colnames = ['id', 'assembly', 'genus', 'species', 'seqfile']
    data = pd.read_csv(filepth, names=colnames)
    files = data.seqfile.tolist()
    return files


def get_kmer_counts(filename, num_cols, col_index):

    genome_row = num_cols*[0]

    id = 0
    #Same method as used in acheron, nothing else tried was fast enough
    with open(filename) as f:
        for record in SeqIO.parse(f, 'fasta'):
            kmercount = record.id
            kmercount = int(kmercount)
            seq = record.seq
            seq = str(seq)
            index = col_index[seq]
            genome_row[index] = kmercount


    return genome_row

def build_matrix(datadir):
    cols = {}
    rows = {}
    chars = "ACGT"
    files_path = datadir + '/processed_data/clean.csv'
    i = 0
    files = get_file_names(files_path)
    #taken from acheron, again best way to do it I could find

    for seq in itertools.product(chars, repeat=11):
        dna = "".join(seq)
        rev = Seq.reverse_complement(dna)
        if dna > rev:
            dna = rev
        if not dna in cols:
            cols[dna] = i
            i += 1

    x = np.asarray(files)
    numcols = i
    numrows = len(x)
    kmer_matrix = np.zeros((numrows,numcols), dtype=np.ubyte)
    rowindex = 0
    with ProcessPoolExecutor(max_workers=None) as ppe:
        for row in ppe.map(get_kmer_counts, files, itertools.repeat(numcols), itertools.repeat(cols)):
            rows[rowindex] = rowindex
            kmer_matrix[rowindex,:] = row
            rowindex += 1

    saves = datadir + '/processed_data/features.npy'
    save(saves, kmer_matrix)
    return datadir


