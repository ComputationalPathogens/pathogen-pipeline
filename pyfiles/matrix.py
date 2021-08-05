import itertools
import pandas as pd
from Bio import Seq, SeqIO
import numpy as np
from numpy import save
from concurrent.futures import ProcessPoolExecutor

def get_file_names(filepth):
    """
    Parameters
    ----------
    filepth : Path to clean data .csv to pull kmer count file paths

    Returns
    -------
    files : List of file paths for counted kmers

    """

    colnames = ['id', 'assembly', 'genus', 'species', 'seqfile', 'cntfile']
    data = pd.read_csv(filepth, names=colnames)
    files = data.cntfile.tolist()
    return files


def get_kmer_counts(filename, num_cols, col_index, datadir):
    """
    Parameters
    ----------
    filename : Path to file of counted kmers
    num_cols : Amount of features
    col_index : Dictionary mapping of Kmer:Count for building feature row

    Returns
    -------
    genome_row : Completed feature row of kmer counts for input sample

    """

    genome_row = num_cols*[0]
    append = datadir + filename
    #Same method used in Computational-pathogens/acheron
    with open(append) as f:
        for record in SeqIO.parse(f, 'fasta'):
            kmercount = record.id
            kmercount = int(kmercount)
            seq = record.seq
            seq = str(seq)
            if len(seq) < 11:
                print("Invalid key: %s" % (seq))
                print(filename)
            index = col_index[seq]
            genome_row[index] = kmercount


    return genome_row

def build_matrix(datadir, filename = '/processed_data/cleanwcounts.csv'):
    """
    Parameters
    ----------
    datadir : Base directory of nextflow execution

    Returns
    -------
    datadir : Base directory of nextflow execution
    
    Desc
    ----
    Builds feature matrix of [NumSamples]*[NumFeatures] size and saves it 
    to features.npy
    
    """
    cols = {}
    rows = {}
    chars = "ACGT"
    files_path = datadir + filename
    i = 0
    files = get_file_names(files_path)

    #Same method used in Computational-pathogens/acheron
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
        for row in ppe.map(get_kmer_counts, files, itertools.repeat(numcols), itertools.repeat(cols), itertools.repeat(datadir)):
            rows[rowindex] = rowindex
            kmer_matrix[rowindex,:] = row
            rowindex += 1

    saves = datadir + '/processed_data/features.npy'
    save(saves, kmer_matrix)
    return datadir


