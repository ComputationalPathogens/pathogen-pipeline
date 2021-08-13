from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

def create(datadir):
    colnames=['id','assembly','genus','species','seqfile','cntfile']
    data = pd.read_pickle(datadir+'/processed_data/features.pkl')
    labels = pd.read_csv(datadir+'/processed_data/clean.csv', names=colnames)
    labels = labels.species.tolist()
    data.index = labels
    label_enc = LabelEncoder()
    label_enc = label_enc.fit(labels)
    clrs = sns.color_palette("husl",14)
    lut = dict(zip(label_enc.classes_, clrs))
    rowclrs = []
    for x in labels:
        rowclrs.append(lut[x])
    
    sel = SelectKBest(f_classif,k=50000)
    kbestdata = sel.fit_transform(data,labels)
    kbestmask = sel.get_support()
    kbestlabels = data.columns[kbestmask]
    kbestdf = pd.DataFrame(kbestdata, columns=kbestlabels)
    kbestdf.index = labels
    snsplot = sns.clustermap(kbestdf, row_colors=rowclrs, vmin = 0, vmax = 100)
    handles = [Patch(facecolor=lut[name]) for name in lut]
    plt.legend(handles, lut, title='Species',
               bbox_to_anchor=(1, 1), bbox_transform=plt.gcf().transFigure, loc='upper right')
    
    snsplot.savefig(datadir+"/processed_data/ClusterMap.png")