from ToppingIssue.MODEL_TOKEN.Tokenizer import give_me_token
from tqdm import tqdm
import numpy as np
import pandas as pd

class TITLE_EMBEDDER:
    def __init__(self, model, vocab_path, SEQ_LEN):
        self.model = model
        self.give_toke = give_me_token(vocab_path, SEQ_LEN)
        self.SEQ_LEN = SEQ_LEN
        print('\n<TITLE EMBEDDER READY>')

    def __call__(self, text_list):
        print('\n\t<tokenizing data>')
        test_T, test_P = list(), list()
        for text in tqdm(text_list):
            tok_sen, pos_sen = self.give_toke(text)
            test_T.append(tok_sen)
            test_P.append(pos_sen)
        test_T, test_P = np.array(test_T), np.array(test_P)
        test_T = test_T.reshape(len(text_list), 1, self.SEQ_LEN)
        test_P = test_P.reshape(len(text_list), 1, self.SEQ_LEN)
        y_hats = list()
        print('\n\t<getting vectors>')
        for i in tqdm(range(len(text_list))):
            test_x = [test_T[i,:,:], test_P[i,:,:]]
            y_hat = self.model.predict(test_x)
            y_hats.extend(y_hat)
        sen_vec = list()
        print('\n\t<reshaping>')
        for i in tqdm(y_hats):
            temp = i.flatten()
            sen_vec.append(temp)
        print('\n<TITLE EMBEDDING FIN>')
        return pd.DataFrame({'Title_vec' : sen_vec})
