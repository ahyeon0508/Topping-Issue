from ToppingIssue.UTILS.ETRI_API import ETRI_API
import pandas as pd 
import re

def MORP_TO_DF(morp_df, test):
    for j in range(len(test['return_object']['sentence'])):
            for i in range(len(test['return_object']['sentence'][j]['morp'])):
                morp_df = morp_df.append(test['return_object']['sentence'][j]['morp'][i], ignore_index=True)
    return morp_df

def WORD_TO_LIST(word_list, test):
    for j in range(len(test['return_object']['sentence'])):
            for i in range(len(test['return_object']['sentence'][j]['word'])):
                word_list.append(test['return_object']['sentence'][j]['word'][i]['text'])
    return word_list

def clean_text(readData):
  text = re.sub('[-=+,#/\?:^@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', ' ', readData)
  text_rr = ' '.join(text.split())
  return text_rr

def char_joiner(x):
    if len(x) == 1:
        return x[0]
    else:
        return ''.join(x)

def KEY_SUB_WORD(in_title, key, api_type):
    title_list = in_title
    origin_morp_df = pd.DataFrame(columns = ['id','lemma','type','position','weight'])
    word_list = []

    for title in title_list:
        test_text1 = clean_text(title)
        test_response1 = ETRI_API(key, api_type, test_text1)
        origin_morp_df = MORP_TO_DF(origin_morp_df, test_response1)
        word_list = WORD_TO_LIST(word_list, test_response1)
    morp_df = origin_morp_df.reset_index().drop('index', axis = 1)

    flag, st_idx = True, 0
    join_text = pd.DataFrame()
    max_idx = (len(morp_df)-1)
    while flag:
        if st_idx < max_idx:
            if st_idx + 2 <= max_idx:
                concat_text_base = [morp_df.loc[st_idx,'lemma'],morp_df.loc[st_idx+1,'lemma'],morp_df.loc[st_idx+2,'lemma']]
                concat_morp_base = [morp_df.loc[st_idx,'type'],morp_df.loc[st_idx+1,'type'],morp_df.loc[st_idx+2,'type']]
                two_step = ''.join(concat_text_base)
                one_step = ''.join(concat_text_base[:2])
                if two_step in word_list:
                    join_text = join_text.append({'word': concat_text_base,'morp': concat_morp_base}, ignore_index = True)
                    st_idx += 3
                elif one_step in word_list:
                    join_text = join_text.append({'word': concat_text_base[:2],'morp': concat_morp_base[:2]}, ignore_index = True)
                    st_idx += 2
                else:
                    join_text = join_text.append({'word' : [concat_text_base[0]], 'morp' : [concat_morp_base[0]]}, ignore_index = True)
                    st_idx += 1
            elif st_idx + 1 <= max_idx:
                concat_text_base = [morp_df.loc[st_idx,'lemma'],morp_df.loc[st_idx+1,'lemma']]
                concat_morp_base = [morp_df.loc[st_idx,'type'],morp_df.loc[st_idx+1,'type']]
                one_step = ''.join(concat_text_base)
                if one_step in word_list:
                    join_text = join_text.append({'word': concat_text_base,'morp': concat_morp_base}, ignore_index = True)
                    st_idx += 2
                else:
                    join_text = join_text.append({'word' : [concat_text_base[0]], 'morp': [concat_morp_base[0]]}, ignore_index = True)
                    st_idx += 1
        elif st_idx == max_idx:
            join_text = join_text.append({'word' : [morp_df.loc[st_idx,'lemma']], 'morp': [morp_df.loc[st_idx,'type']]}, ignore_index = True)
            st_idx += 1
        if st_idx > max_idx:
            flag = False

    morp_del_list = ['EM','EP','EF','EC','ETN','ETM','XP','XPN','XS','XSV','XSA','JK','JKS','JKC','JKG','JKO','JKB','JKV','JKQ','JX','JC','IC','SF','VCN','VCP','NNB']
    for i in range(len(join_text)):
        end_morp = join_text.loc[i,'morp'][-1]
        if end_morp in morp_del_list:
            if len(join_text.loc[i,'morp']) == 1:
                join_text.loc[i,'word'] = None
                join_text.loc[i,'morp'] = None

            else:
                join_text.loc[i,'word'] = join_text.loc[i,'word'][:-1]
                join_text.loc[i,'morp'] = join_text.loc[i,'morp'][:-1]

    join_text = join_text.dropna().reset_index().drop('index', axis = 1)

    for i in range(len(join_text)):
        if len(join_text.loc[i,'morp']) == 1:
            if ('V' in join_text.loc[i,'morp'][0]):
                join_text.loc[i,'word'] = None

    join_text = join_text.dropna().reset_index().drop('index', axis = 1)

    join_text['full_word'] = join_text['word'].map(lambda x: char_joiner(x))

    count_df = join_text['full_word'].value_counts().reset_index()
    count_df.columns = ['lemma', 'size']


    title_out = count_df[count_df['size'] > (len(title_list)*0.5)]
    return title_out