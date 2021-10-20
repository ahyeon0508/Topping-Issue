from ToppingIssue.CLUSTER_CLASSIFIER import Article_cluster, Comment_classifier, Title_embedder
from ToppingIssue.MODEL_TOKEN import Model_builder
from ToppingIssue.UTILS import KEY_SUB_WORD, Reforger
import pandas as pd
from tqdm import tqdm
import copy

class PIPE_LINE:
    def __init__(self, con_dict):
        self.title_embedder = Title_embedder.TITLE_EMBEDDER(Model_builder.get_t_model(con_dict), con_dict['vocab_path'], 50)
        self.comment_classifier = Comment_classifier.COMMENT_CLASSIFIER(Model_builder.get_c_model(con_dict), con_dict['vocab_path'], 302)
        self.article_cluster = Article_cluster.ARTICLE_CLUSTER
        self.reforger = Reforger.REFORGER
        self.key_sub_word = KEY_SUB_WORD.KEY_SUB_WORD

    def __call__(self, raw_data, date, key, api_type):
        date_filter = (raw_data['Date'] == date)
        date_filtered_data = raw_data.loc[date_filter]
        date_filtered_data = date_filtered_data.reset_index().drop('index', axis = 1)

        title_vec = self.title_embedder(date_filtered_data['Title'])
        clust_info = self.article_cluster(title_vec['Title_vec'],0.65)

        temp_data = pd.concat([date_filtered_data, clust_info], axis = 1)
        temp_list = list(temp_data.loc[temp_data['cluster'] == 0, ['N_Comment','D_Comment']].index)
        date_filtered_data.loc[temp_list, ['N_Comment','D_Comment']] = 'NA', 'NA'

        cluster_list = sorted(clust_info['cluster'].unique())
        clust_name_list = list()
        lemma_score_df = pd.DataFrame(columns = ['lemma','size'])
        print('<GETTING KEY&SUB WORD>')
        for clust_no in tqdm(cluster_list[1:]):
            in_title = temp_data.loc[temp_data['cluster'] == clust_no, 'Title']
            title_out = self.key_sub_word(in_title, key, api_type)
            clust_name_list.append(title_out['lemma'].tolist())
            lemma_score_df = lemma_score_df.append(title_out)
        clust_name_list.insert(0,[])

        lemma_score_df = lemma_score_df.reset_index().drop('index', axis = 1)

        test_list = list()
        for i in clust_name_list:
            test_list.extend(i)

        merge_test = list(set(test_list))
        zeros = [0 for i in range(len(merge_test))]
        merge_df = pd.DataFrame({'key_words':merge_test, 'score':zeros})

        for i in range(len(lemma_score_df)):
            key_vocab = lemma_score_df.loc[i,'lemma']
            merge_df.loc[merge_df['key_words'] == key_vocab, 'score'] += 1
        merge_df = merge_df.sort_values(by = 'score',ascending = False)

        target_clust_name = copy.deepcopy(clust_name_list)
        
        zeros = [0 for i in range(len(target_clust_name))]
        c_name_merge_df = pd.DataFrame({'key_word':zeros, 'sub_words':zeros})
        for key_word in merge_df['key_words']:
            for temp_idx in range(len(target_clust_name)):
                if key_word in target_clust_name[temp_idx]:
                    target_clust_name[temp_idx].remove(key_word)
                    sub_words = target_clust_name[temp_idx]
                    c_name_merge_df.loc[temp_idx,'key_word'] = key_word
                    if sub_words == list():
                        sub_words = 0
                    else:
                        sub_words = ','.join(sub_words)
                    c_name_merge_df.loc[temp_idx,'sub_words'] = [sub_words]
                    target_clust_name[temp_idx] = list()

        N_comment_sentiment = self.comment_classifier(date_filtered_data['N_Comment'], 'N')
        D_comment_sentiment = self.comment_classifier(date_filtered_data['D_Comment'], 'D')
        jion_data_by_day = pd.concat([date_filtered_data, title_vec, N_comment_sentiment, D_comment_sentiment], axis = 1)

        refored_data = self.reforger(clust_info, jion_data_by_day)
        refored_data = refored_data.sort_values(by = 'Clust_NO').reset_index().drop('index', axis = 1)
        dates_df = pd.DataFrame([pd.to_datetime(date) for i in range(len(refored_data))], columns = ['DATE'])


        return_df = pd.concat([dates_df,refored_data,c_name_merge_df], axis = 1)
        return_df.loc[day_data['key_word'] == 0,'key_word'] = 'NA'
        return_df.loc[day_data['key_word'] == 0,'key_word'] = 'NA'
        return pd.concat([dates_df,refored_data,c_name_merge_df], axis = 1)

