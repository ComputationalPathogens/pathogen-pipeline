import os
import pandas as pd

def count_kmer(rootdir):
    filepath = rootdir + '/processed_data/clean.csv'
    walkdir = rootdir + '/refseq/bacteria/'
    dumpname = 'mer_counts_dumps.fa'

    colnames = ['id', 'assembly', 'genus', 'species', 'seqfile', 'cntfile']
    data = pd.read_csv(filepath, dtype={'id':'int32','seqfile':'str'}, names=colnames)
    id = 0
    data['seqfile'] = data['seqfile'].astype('str')
    data['cntfile'] = data['cntfile'].astype('str')
    files = data.seqfile.tolist()
    files2 = data.cntfile.tolist()
    for file in files:
        ext = os.path.splitext(str(file))
        dirname = os.path.dirname(file)
        if ext[-1] == ".fna":
            merpth = dirname + '/' + 'mer_counts.jf'
            cmd = 'jellyfish count -m 11 -s 100M -C -o ' + merpth + ' ' + file
            dumppth = dirname + '/' + dumpname
            cmd2 = 'jellyfish dump ' + merpth + ' > ' + dumppth
            os.system(cmd)
            os.system(cmd2)
            data.at[id,'cntfile'] = dumppth
            id = id + 1
        else:
            dumppth = "error"
            data.at[id,'cntfile'] = dumppth
            id = id + 1


    data.to_csv(filepath, index=False, header=False)

    return rootdir


