import pandas as pd
from tqdm import tqdm
import numpy as np
from numpy import dot
from numpy.linalg import norm

def ARTICLE_CLUSTER(sen_vec, cut):
    clusters = pd.DataFrame({'idx': range(len(sen_vec)), 'cluster':np.zeros(len(sen_vec))})
    clust = 1
    print('\n\t<Sorting Articles>')
    for idx_ in tqdm(range(len(sen_vec))):
        if clusters.iloc[idx_,1] != 0:
            continue
        sorting_list = [idx_]
        base_vec = sen_vec[idx_]
        base_norm = norm(base_vec)
        target_idx_list = list(clusters.loc[clusters['cluster'] == 0, 'idx'])
        if idx_ in target_idx_list:
            target_idx_list.remove(idx_)
        for target_idx in target_idx_list:
            target_vec = sen_vec[target_idx]
            cos_score = dot(base_vec, target_vec)/(base_norm*norm(target_vec))
            if cos_score >= cut:
                sorting_list.append(target_idx)
            else:
                continue
        if len(sorting_list) > 1:
            clusters.iloc[sorting_list,1] = clust
            clust += 1
    print('\n<ARTICLE CLUSTERING FIN>')
    return clusters
