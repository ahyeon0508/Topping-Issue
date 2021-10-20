import pandas as pd
from tqdm import tqdm

def min_max(data):
    x_min, x_max = min(data), max(data)
    return (data-x_min)/(x_max-x_min)

def REFORGER(clust_info, db_data):
    return_df = pd.DataFrame(columns = ['Clust_NO','Title','Link','Content','Clean_text','Comment_cnt','Sentiment_cnt','Article_cnt','N_Good','N_Neut','N_Bad','D_Good','D_Neut','D_Bad'])
    db_data['N_Sentiment_cnt'] = db_data['N_Sentiment'].map(lambda x: sum(list(x.values())))
    db_data['D_Sentiment_cnt'] = db_data['D_Sentiment'].map(lambda x: sum(list(x.values())))
    total_cluster = list(clust_info['cluster'].unique())
    no_clust_count = (clust_info['cluster'] == 0).sum()
    print(f'\n\t<Total {len(total_cluster)-1} clusters found (DATA with NO cluster : {no_clust_count})>')

    for i in tqdm(total_cluster):
        clust_i_idx = list(clust_info.loc[clust_info['cluster'] == i,'idx'])
        clust_i_data = db_data.iloc[clust_i_idx,:]

        appending_dict = {
            'Clust_NO' : i,
            'Title' : list(clust_i_data['Title']),
            'Link' : list(clust_i_data['Link']),
            'Content' : list(clust_i_data['Content']),
            'Clean_text' : list(clust_i_data['Title_clean']),
            'Comment_cnt' : (clust_i_data['N_Comment_cnt'].sum() + clust_i_data['D_Comment_cnt'].sum()),
            'Sentiment_cnt' : (clust_i_data['N_Sentiment_cnt'].sum() + clust_i_data['D_Sentiment_cnt'].sum()),
            'Article_cnt' : len(clust_i_data['Title']),
            'N_Good' : clust_i_data['N_Good'].sum(),
            'N_Neut' : clust_i_data['N_Neut'].sum(),
            'N_Bad' : clust_i_data['N_Bad'].sum(),
            'D_Good' : clust_i_data['D_Good'].sum(),
            'D_Neut' : clust_i_data['D_Neut'].sum(),
            'D_Bad' : clust_i_data['D_Bad'].sum()}

        return_df = return_df.append(appending_dict, ignore_index=True)
    return return_df