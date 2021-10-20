from keras_bert import load_trained_model_from_checkpoint
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, AveragePooling1D, Reshape, Dot, Flatten, Input
from tensorflow.keras.optimizers import Adam
from tensorflow import keras

def get_t_model(con_dict):
    config_path = con_dict['config_path']
    checkpoint_path = con_dict['checkpoint_path']
    T_weight_path = con_dict['T_weight_path']
    T_SEQ_LEN = 50

    T_model = load_trained_model_from_checkpoint(
        config_path
        ,checkpoint_path
        ,training = True
        ,trainable = True
        ,seq_len = T_SEQ_LEN)

    def bert_embedder(base_model):
        inputs = base_model.inputs[:2]
        bert_embedder = base_model.get_layer('Extract').output
        reshape_L = Reshape((768,1))(bert_embedder)
        pool_L = AveragePooling1D(pool_size = 3, padding = 'valid')(reshape_L)
        reshape_O = Flatten()(pool_L)
        model = Model(inputs = inputs, outputs = reshape_O)
        return model

    siam_bert = bert_embedder(T_model)

    in_one_tok = Input(batch_shape = (None, 50))
    in_one_pos = Input(batch_shape = (None, 50))
    in_two_tok = Input(batch_shape = (None, 50))
    in_two_pos = Input(batch_shape = (None, 50))
    siam_one = siam_bert([in_one_tok, in_one_pos])
    siam_two = siam_bert([in_two_tok, in_two_pos])
    cos_layer = Dot(axes = 1, normalize = True)([siam_one, siam_two])
    siam_model = Model(inputs = [in_one_tok, in_one_pos, in_two_tok, in_two_pos], outputs = cos_layer)
    siam_model.compile(loss = 'mse', optimizer = Adam(learning_rate = 0.00001))

    siam_model.load_weights(T_weight_path)
    Title_BERT = siam_model.layers[-2]

    return Title_BERT


def get_c_model(con_dict):
    config_path = con_dict['config_path']
    checkpoint_path = con_dict['checkpoint_path']
    C_weight_path = con_dict['C_weight_path']
    C_SEQ_LEN = 302

    C_model = load_trained_model_from_checkpoint(
        config_path
        ,checkpoint_path
        ,training = True
        ,trainable = True
        ,seq_len = C_SEQ_LEN)

    inputs = C_model.inputs[:2]
    bert_out = C_model.layers[-3].output
    outputs = Dense(1, activation='sigmoid',kernel_initializer=keras.initializers.TruncatedNormal(stddev=0.02),)(bert_out)
    Comment_BERT = Model(inputs, outputs)
    Comment_BERT.load_weights(C_weight_path)

    return Comment_BERT
