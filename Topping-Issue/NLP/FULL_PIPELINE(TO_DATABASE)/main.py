import os
os.getcwd()
os.chdir('working_DIR')

from ToppingIssue.PIPE_LINE import PIPE_LINE
import pickle


# 4_bert_download_004_bert_eojeol_tensorflow (한국어 BERT 언어모델)
base_path = './ToppingIssue/ETRI/4_bert_download_004_bert_eojeol_tensorflow'
con_dict = {
    'config_path' : os.path.join(base_path, 'bert_config.json'),
    'checkpoint_path' : os.path.join(base_path, 'model.ckpt-56000'),
    'vocab_path' : os.path.join(base_path, 'vocab.korean.rawtext.list'),
    'T_weight_path' : os.path.join(base_path, 'model(siam)_data(klue)_batch(20)_epoch(1)_loss(mse)_ADAM(0.00001).h5'),
    'C_weight_path' : os.path.join(base_path, 'sentiment_bert_naver_ai_batch10_seq302_ALL.h5'),
}

pipe_line = PIPE_LINE(con_dict)


# raw_data COLUMNS = ['Date', 'Title', 'Content', 'Content_len', 'N_Comment', 'N_Comment_cnt', 
#                     'N_Sentiment', 'D_Comment','D_Comment_cnt', 'D_Sentiment', 'Link', 'Press', 'Title_clean']
with open('DATA_DIRECTORY', 'rb') as f:
    raw_data = pickle.load(f)

key = 'ETRI_OPEN_API_KEY'
api_type = 'morp'
date = 'yyyy-mm-dd'

daily_clustered_data = pipe_line(raw_data, date, key, api_type)






