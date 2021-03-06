import os
import pandas as pd

def count_kmer(rootdir, filename = '/processed_data/clean.csv'):
    """
    Parameters
    ----------
    rootdir : Base directory of nextflow execution

    Returns
    -------
    rootdir : Base directory of nextflow execution
    
    Desc
    ----
    Takes .fna complete genome sequence files and runs Jellyfish to count kmers
    Saves kmer-count file path into the clean.csv metadata file

    """
    #Could potentially be done with multiprocessing instead although this doesnt take much time anyway
    filepath = rootdir + filename
    checkpath = rootdir + '/processed_data/cleanwcounts.csv'
    colnames = ['id', 'assembly', 'genus', 'species', 'seqfile', 'cntfile']
    dumpname = 'mer_counts_dumps.fa'

    data = pd.read_csv(filepath, names=colnames)
    id = 0
    data['seqfile'] = data['seqfile'].astype('str')
    data['cntfile'] = data['cntfile'].astype('str')
    files = data.seqfile.tolist()
    files2 = data.cntfile.tolist()

    for seqfile, cntfile in zip(files, files2):
        ext = os.path.splitext(str(seqfile))
        dirname = os.path.dirname(seqfile)
        if ext[-1] == ".fna":
            merpth = rootdir + dirname + '/' + 'mer_counts.jf'
            dumppth = rootdir + dirname + '/' + dumpname
            seqpth = rootdir + seqfile
            cntname = dirname + '/' + dumpname
            if cntfile == cntname:
                continue
            cmd = 'jellyfish count -m 11 -s 100M -C -o ' + merpth + ' ' + seqpth
            cmd2 = 'jellyfish dump ' + merpth + ' > ' + dumppth
            os.system(cmd)
            os.system(cmd2)
            data.at[id,'cntfile'] = cntname
            id = id + 1
        else:
            dumppth = "error"
            data.at[id,'cntfile'] = cntname
            id = id + 1
    filepath = rootdir + '/processed_data/cleanwcounts.csv'
    data.to_csv(filepath, index=False, header=False)

    return rootdir