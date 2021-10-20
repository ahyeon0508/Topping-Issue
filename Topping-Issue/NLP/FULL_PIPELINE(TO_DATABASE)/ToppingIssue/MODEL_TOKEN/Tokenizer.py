import tensorflow as tf
import numpy as np
from ToppingIssue.ETRI.tokenization import FullTokenizer

class give_me_token:
    def __init__(self, vocab_path, SEQ_LEN):
        tf.gfile = tf.io.gfile
        self.tokenizer = FullTokenizer(vocab_path, do_lower_case = False)
        self.SEQ_LEN = SEQ_LEN

    def __call__(self,text):
        token_input = self.tokenizer.tokenize(text)
        #token_char = token_input.copy()
        if len(token_input) >= self.SEQ_LEN-2:
            token_input = token_input[:(self.SEQ_LEN-2)]
        SE_marked_sen = (["[CLS]"]+token_input+["[SEP]"])
        sen_idx = self.tokenizer.convert_tokens_to_ids(SE_marked_sen)
        sen_idx.extend([0] * (self.SEQ_LEN - len(SE_marked_sen)))
        tokenized_sen = np.array(sen_idx).astype(np.float32)
        position_sen = np.zeros_like(tokenized_sen)
        return tokenized_sen, position_sen#, token_char


def one_hot_encoding(sen_idx, vocab_size):
    sen_mat = list()
    for word_idx in sen_idx:
        one_hot_vector = [0]*(vocab_size)
        one_hot_vector[word_idx]=1
        sen_mat.append(one_hot_vector)
    return np.array(sen_mat)


class give_me_all_token:
    def __init__(self, vocab_path, vocab_size, SEQ_LEN):
        tf.gfile = tf.io.gfile
        self.tokenizer = FullTokenizer(vocab_path, do_lower_case = False)
        self.SEQ_LEN = SEQ_LEN
        self.vocab_size = vocab_size

    def __call__(self,text):
        token_input = self.tokenizer.tokenize(text)
        tokenized_origin_sen = token_input.copy() 
        if len(token_input) >= self.SEQ_LEN:
            token_input = token_input[:(self.SEQ_LEN-2)]
        SE_marked_sen = (["[CLS]"]+token_input+["[SEP]"])
        sen_idx = self.tokenizer.convert_tokens_to_ids(SE_marked_sen)
        sen_idx.extend([0] * (self.SEQ_LEN - len(SE_marked_sen)))
        tokenized_sen = np.array(sen_idx).astype(np.float32).flatten()
        position_sen = np.zeros_like(tokenized_sen).flatten()

        MLM_out = one_hot_encoding(sen_idx,self.vocab_size)

        masking_sen = token_input.copy()
        masking_cnt = int(round(len(token_input)*0.15,0))
        idx_list = np.arange(len(token_input))
        masking_idx = np.random.choice(idx_list, masking_cnt, replace = False)        

        for i in masking_idx:
            masking_sen[i] = '[MASK]'

        mask_SE_marked_sen = (["[CLS]"]+masking_sen+["[SEP]"])
        mask_sen_idx = self.tokenizer.convert_tokens_to_ids(mask_SE_marked_sen)
        mask_sen_idx.extend([0] * (self.SEQ_LEN - len(mask_SE_marked_sen)))        
        masked_sen = np.array(mask_sen_idx).astype(np.float32).flatten()

        NSP_out = np.array([0,0]).flatten()

        return tokenized_sen, position_sen, masked_sen, NSP_out, MLM_out

