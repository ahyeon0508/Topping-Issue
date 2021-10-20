from collections import Counter
from ToppingIssue.MODEL_TOKEN.Tokenizer import give_me_token
from tqdm import tqdm
import numpy as np 
import pandas as pd

def sigmoid_sorter_neut(num):
    if 0 <= num < 0.4:
        return 'bad'
    elif 0.4 <= num <= 0.6:
        return 'neut'
    elif 0.6 < num <= 1:
        return 'good'

def sigmoid_sorter_binary(num):
    if 0 <= num <= 0.5:
        return 'bad'
    elif 0.5 < num <= 1:
        return 'good'

class COMMENT_CLASSIFIER:
    def __init__(self, model, vocab_path, SEQ_LEN, sort_type = 'neut'):
        self.model = model
        self.give_toke = give_me_token(vocab_path, SEQ_LEN)
        self.SEQ_LEN = SEQ_LEN
        if sort_type == 'binary':
            self.sorter = sigmoid_sorter_binary
        elif sort_type == 'neut':
            self.sorter = sigmoid_sorter_neut
        print('\n<COMMENT CLASSIFIER READY>')

    def __call__(self, all_comments, portal): # data is an out put of data_reforging
        good_list, bad_list, neut_list = list(), list(), list()
        count = 1
        for article_comments in all_comments:
            print(f'\n<processing article NO{count} out of {len(all_comments)}>')
            if article_comments == 'NA':
                print(f'article NO{count} has no comments')
                good_list.append(0)
                bad_list.append(0) 
                neut_list.append(0)
                count += 1
                continue
            else:
                pure_comments = np.array(article_comments).flatten()[::3]
            tokens, poss = list(), list()
            for single_comment in pure_comments:
                tokenized_sen, position_sen = self.give_toke(single_comment)
                tokens.append(tokenized_sen)
                poss.append(position_sen)
            y_hat_list = list()
            print(f'getting sentiment from article NO{count}')
            for tok,pos in tqdm(zip(tokens,poss), total = len(tokens)):
                tok, pos = tok.reshape(-1,self.SEQ_LEN), pos.reshape(-1,self.SEQ_LEN)
                y_hat = self.model.predict([tok,pos])
                y_hat_list.append(self.sorter(y_hat))
            sentiment_count = Counter(y_hat_list)
            if self.sorter == sigmoid_sorter_binary:
                good_list.append(sentiment_count['good'])
                bad_list.append(sentiment_count['bad'])
            elif self.sorter == sigmoid_sorter_neut:
                good_list.append(sentiment_count['good'])
                bad_list.append(sentiment_count['bad'])
                neut_list.append(sentiment_count['neut'])
            count += 1
        print('\nCOMMENT CLASSIFIER FIN')
        if self.sorter == sigmoid_sorter_binary:
            return pd.DataFrame({f'{portal}_Good': good_list, f'{portal}_Bad':bad_list})
        elif self.sorter == sigmoid_sorter_neut:
            return pd.DataFrame({f'{portal}_Good': good_list, f'{portal}_Bad':bad_list, f'{portal}_Neut':neut_list})

