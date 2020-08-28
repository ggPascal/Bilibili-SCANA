import random as rd
from keras.models import Model
from keras.models import load_model
from keras import layers
from keras import Input
from keras import callbacks
import os
import json
import numpy as np
from tqdm import tqdm
import numba as nb
import tensorflow as tf

gpus = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(gpus[0], True)
# tf.compat.v1.keras.backend.set_session(tf.compat.v1.Session(config=config))

os.environ['NUMBA_WARNINGS'] = '0'

import keras.backend as K
def r2(y_true, y_pred):
    a = K.square(y_pred - y_true)
    b = K.sum(a)
    c = K.mean(y_true)
    d = K.square(y_true - c)
    e = K.sum(d)
    f = 1 - b/e
    return f

def gpt_dataset_builder(comment_data_dict):
    proccess_index = 0
    target_list_sort = []
    up_list_sort = []
    down_list_sort = []

    display_count = len(list(comment_data_dict.keys()))
    display_show = 1
    key_list = list(comment_data_dict.keys())
    for std_thow, reply_id in tqdm(enumerate(key_list), total = len(key_list)):
        # print('Working on '+str(display_show)+'/'+str(display_count))
        current_encoded_message = comment_data_dict[reply_id]
        while proccess_index < len(current_encoded_message):
            current_down_list = []
            current_up_list = []
            if proccess_index == 0:
                current_up_list = [0]

            else:
                up_index = 0
                while up_index == proccess_index - 1 or up_index < proccess_index - 1:
                    current_up_list.append(current_encoded_message[up_index])
                    up_index += 1
            
            if proccess_index == len(current_encoded_message) - 1:
                # TODO: Test wo delete it
                current_down_list = [0]
            else:
                # TODO: Replace with a while loop
                down_index = proccess_index + 1
                while (down_index == proccess_index + 1 or down_index > proccess_index) and (down_index < len(current_encoded_message) - 1 or down_index == len(current_encoded_message) - 1):
                    current_down_list.append(
                        current_encoded_message[down_index])
                    down_index += 1

            target_list_sort.append(current_encoded_message)
            up_list_sort.append(current_up_list)
            down_list_sort.append(current_down_list)
            proccess_index += 1
            display_show += 1
        proccess_index = 0
    return target_list_sort, up_list_sort, down_list_sort


def random_up(target_list_sort, up_list_sort, down_list_sort):
    display_count = len(target_list_sort)
    display_show = 1
    for rand_index in range(0, len(target_list_sort) - 1):
        # print("Randomizing on "+str(display_show)+"/" + str(display_count))
        target_index = rd.randint(0, len(target_list_sort) - 1)
        trans_up_list_source = up_list_sort[rand_index]
        trans_down_list_source = up_list_sort[rand_index]
        trans_target_list_source = target_list_sort[rand_index]

        trans_up_list_target = up_list_sort[target_index]
        trans_down_list_target = down_list_sort[target_index]
        trans_target_list_target = target_list_sort[target_index]

        target_list_sort[rand_index] = trans_target_list_target
        up_list_sort[rand_index] = trans_up_list_target
        down_list_sort[rand_index] = trans_down_list_target

        target_list_sort[target_index] = trans_target_list_source
        up_list_sort[target_index] = trans_up_list_source
        down_list_sort[target_index] = trans_down_list_source
    target_list_rand = target_list_sort
    up_list_rand = up_list_sort
    down_list_rand = down_list_sort
    return target_list_rand, up_list_rand, down_list_rand


def split_dataset(percent_of_transet, testset_present, target_list_rand, up_list_rand, down_list_rand):
    split_index = 0
    train_target_list = []
    train_up_list = []
    train_down_list = []
    test_target_list = []
    test_up_list = []
    test_down_list = []
    val_target_list = []
    val_up_list = []
    val_down_list = []

    maxium_trainset_index = int(
        (len(target_list_rand) - 1) * percent_of_transet)
    for std_thow, split_index in tqdm(enumerate(range(0, maxium_trainset_index)), total=maxium_trainset_index, desc='Train-set-build'):
        train_target_list.append(target_list_rand[split_index])
        train_up_list.append(up_list_rand[split_index])
        train_down_list.append(down_list_rand[split_index])

    minimize_testset_index = maxium_trainset_index + 1
    maxium_testset_index = int(
        (len(target_list_rand) - 1 - minimize_testset_index) * testset_present) + minimize_testset_index
    split_index = 0
    for std_thow, split_index in tqdm(enumerate(range(minimize_testset_index, maxium_testset_index)), total = maxium_testset_index - minimize_testset_index, desc = 'Test-set-build'):
        test_target_list.append(target_list_rand[split_index])
        test_up_list.append(up_list_rand[split_index])
        test_down_list.append(up_list_rand[split_index])

    return train_up_list, test_up_list, train_down_list, test_down_list, train_target_list, test_target_list

def build_reglaiour_model_v1_1(max_index_up_text, maxium_legth):

    up_text = Input(shape=(None, maxium_legth),
                    name='up_text', dtype='float32')

    up_text_emb = layers.Embedding(max_index_up_text + 1, 64)(up_text)

    cnn_up_text_1 = layers.Conv1D(500, 1, padding='same')(up_text_emb)
    cnn_up_text_2 = layers.Conv1D(500, 2, padding='same')(up_text_emb)
    cnn_up_text_3 = layers.Conv1D(500, 4, padding='same')(up_text_emb)

    cnn_up_output = layers.add([cnn_up_text_1, cnn_up_text_2, cnn_up_text_3])
    cnn_up_output = layers.Reshape((maxium_legth, 500))(cnn_up_output)

    lstm_up_output = layers.LSTM(600, return_sequences=True)(cnn_up_output)

    down_text_tensor = Input(
        shape=(None, maxium_legth),  name='down_text', dtype='float32')

    down_text_tensor_emb = layers.Embedding(
        max_index_up_text + 1, 64)(down_text_tensor)
    cnn_down_output_1 = layers.Conv1D(
        500, 1, padding='same')(down_text_tensor_emb)
    cnn_down_output_2 = layers.Conv1D(
        500, 2, padding='same')(down_text_tensor_emb)
    cnn_down_output_3 = layers.Conv1D(
        500, 3, padding='same')(down_text_tensor_emb)

    cnn_down_output = layers.add(
        [cnn_down_output_1, cnn_down_output_2, cnn_down_output_3])
    cnn_down_output = layers.Reshape(
        (maxium_legth, 500))(cnn_down_output)

    lstm_down_output = layers.LSTM(600, return_sequences=True)(cnn_down_output)

    lstm_output = layers.concatenate([lstm_up_output, lstm_down_output])
    
    lstm_output = layers.LSTM(600)(lstm_output)
    lstm_output = layers.Flatten()(lstm_output)

    final_output = layers.Dense(200)(lstm_output)
    final_output = layers.Dense(1)(final_output)

    model = Model(inputs=[up_text, down_text_tensor], outputs=[final_output])
    model.compile(optimizer='Adadelta', loss='mean_squared_error', metrics=['accuracy', r2])

    return model

def build_reglaiour_model_v1_1_1(max_index_up_text, maxium_legth):

    up_text = Input(shape=(None, maxium_legth),
                    name='up_text', dtype='float32')

    up_text_emb = layers.Embedding(max_index_up_text + 1, 64)(up_text)

    cnn_up_text_1 = layers.Conv1D(500, 1, padding='same')(up_text_emb)
    cnn_up_text_2 = layers.Conv1D(500, 2, padding='same')(up_text_emb)
    cnn_up_text_3 = layers.Conv1D(500, 4, padding='same')(up_text_emb)

    cnn_up_output = layers.add([cnn_up_text_1, cnn_up_text_2, cnn_up_text_3])
    cnn_up_output = layers.Reshape((maxium_legth, 500))(cnn_up_output)

    lstm_up_output = layers.LSTM(600, return_sequences=True, dropout=0.1)(cnn_up_output)

    down_text_tensor = Input(
        shape=(None, maxium_legth),  name='down_text', dtype='float32')

    down_text_tensor_emb = layers.Embedding(
        max_index_up_text + 1, 64)(down_text_tensor)
    cnn_down_output_1 = layers.Conv1D(
        500, 1, padding='same')(down_text_tensor_emb)
    cnn_down_output_2 = layers.Conv1D(
        500, 2, padding='same')(down_text_tensor_emb)
    cnn_down_output_3 = layers.Conv1D(
        500, 3, padding='same')(down_text_tensor_emb)

    cnn_down_output = layers.add(
        [cnn_down_output_1, cnn_down_output_2, cnn_down_output_3])
    cnn_down_output = layers.Reshape(
        (maxium_legth, 500))(cnn_down_output)

    lstm_down_output = layers.LSTM(600, return_sequences=True, dropout=0.1)(cnn_down_output)

    lstm_output = layers.concatenate([lstm_up_output, lstm_down_output])
    
    lstm_output = layers.LSTM(600)(lstm_output)
    lstm_output = layers.Flatten()(lstm_output)

    final_output = layers.Dense(200)(lstm_output)
    final_output = layers.Dense(1)(final_output)

    model = Model(inputs=[up_text, down_text_tensor], outputs=[final_output])
    model.compile(optimizer='Adadelta', loss='mean_squared_error', metrics=['accuracy', r2])

    return model

def build_reglaiour_model_v1_1_2(max_index_up_text, maxium_legth):

    up_text = Input(shape=(None, maxium_legth),
                    name='up_text', dtype='float32')

    up_text_tensor_emb = layers.Embedding(
        max_index_up_text + 1, 64)(up_text)
    cnn_up_output_1 = layers.Conv1D(
        500, 1, padding='same')(up_text_tensor_emb)
    cnn_up_output_2 = layers.Conv1D(
        500, 2, padding='same')(up_text_tensor_emb)
    cnn_up_output_3 = layers.Conv1D(
        500, 3, padding='same')(up_text_tensor_emb)
    cnn_up_output_1 = layers.MaxPool1D(2)(cnn_up_output_1)
    cnn_up_output_2 = layers.MaxPool1D(2)(cnn_up_output_2)
    cnn_up_output_3 = layers.MaxPool1D(2)(cnn_up_output_3)
    cnn_up_all_merge_output = layers.concatenate([cnn_up_output_1, cnn_up_output_2, cnn_up_output_3])
    cnn_up_all_merge_output = layers.Conv1D(500, 2, padding='same')(cnn_up_all_merge_output)

    lstm_up_output = layers.LSTM(600, return_sequences=True, dropout=0.1)(cnn_up_all_merge_output)

    down_text_tensor = Input(
        shape=(None, maxium_legth),  name='down_text', dtype='float32')

    down_text_tensor_emb = layers.Embedding(
        max_index_up_text + 1, 64)(down_text_tensor)
    cnn_down_output_1 = layers.Conv1D(
        500, 1, padding='same')(down_text_tensor_emb)
    cnn_down_output_2 = layers.Conv1D(
        500, 2, padding='same')(down_text_tensor_emb)
    cnn_down_output_3 = layers.Conv1D(
        500, 3, padding='same')(down_text_tensor_emb)
    cnn_down_output_1 = layers.MaxPool1D(2)(cnn_down_output_1)
    cnn_down_output_2 = layers.MaxPool1D(2)(cnn_down_output_2)
    cnn_down_output_3 = layers.MaxPool1D(2)(cnn_down_output_3)
    cnn_down_all_merge_output = layers.concatenate([cnn_down_output_1, cnn_down_output_2, cnn_down_output_3])
    cnn_down_all_merge_output = layers.Conv1D(500, 2, padding='same')(cnn_down_all_merge_output)
    

    lstm_down_output = layers.LSTM(600, return_sequences=True, dropout=0.1)(cnn_down_all_merge_output)

    lstm_output = layers.concatenate([lstm_up_output, lstm_down_output])
    
    lstm_output = layers.LSTM(600, return_sequences = True)(lstm_output)
    lstm_output = layers.LSTM(600)(lstm_output)
    lstm_output = layers.Flatten()(lstm_output)

    final_output = layers.Dense(200)(lstm_output)
    final_output = layers.Dense(max_enc_index)(final_output)

    model = Model(inputs=[up_text, down_text_tensor], outputs=[final_output])
    model.compile(optimizer='Adam', loss='mean_squared_error', metrics=['accuracy'])

    return model

def build_reglaiour_model_v1_1_3(max_index_up_text, maxium_legth):

    up_text = Input(shape=(maxium_legth),
                    name='up_text', dtype='float32')

    up_text_tensor_emb = layers.Embedding(
        max_index_up_text + 1, 64)(up_text)
    cnn_up_output_1 = layers.Conv1D(
        500, 1, padding='same')(up_text_tensor_emb)
    cnn_up_output_2 = layers.Conv1D(
        500, 2, padding='same')(up_text_tensor_emb)
    cnn_up_output_3 = layers.Conv1D(
        500, 3, padding='same')(up_text_tensor_emb)
    cnn_up_output_1 = layers.MaxPool1D(2)(cnn_up_output_1)
    cnn_up_output_2 = layers.MaxPool1D(2)(cnn_up_output_2)
    cnn_up_output_3 = layers.MaxPool1D(2)(cnn_up_output_3)
    cnn_up_all_merge_output = layers.concatenate([cnn_up_output_1, cnn_up_output_2, cnn_up_output_3])
    cnn_up_all_merge_output = layers.Conv1D(500, 2, padding='same')(cnn_up_all_merge_output)

    lstm_up_output = layers.LSTM(600, return_sequences=True, dropout=0.1)(cnn_up_all_merge_output)

    down_text_tensor = Input(
        shape=(maxium_legth),  name='down_text', dtype='float32')

    down_text_tensor_emb = layers.Embedding(
        max_index_up_text + 1, 64)(down_text_tensor)
    cnn_down_output_1 = layers.Conv1D(
        500, 1, padding='same')(down_text_tensor_emb)
    cnn_down_output_2 = layers.Conv1D(
        500, 2, padding='same')(down_text_tensor_emb)
    cnn_down_output_3 = layers.Conv1D(
        500, 3, padding='same')(down_text_tensor_emb)
    cnn_down_output_1 = layers.MaxPool1D(2)(cnn_down_output_1)
    cnn_down_output_2 = layers.MaxPool1D(2)(cnn_down_output_2)
    cnn_down_output_3 = layers.MaxPool1D(2)(cnn_down_output_3)
    cnn_down_all_merge_output = layers.concatenate([cnn_down_output_1, cnn_down_output_2, cnn_down_output_3])
    cnn_down_all_merge_output = layers.Conv1D(500, 2, padding='same')(cnn_down_all_merge_output)
    

    lstm_down_output = layers.LSTM(600, return_sequences=True)(cnn_down_all_merge_output)

    lstm_output = layers.concatenate([lstm_up_output, lstm_down_output])
    
    lstm_output = layers.LSTM(600)(lstm_output)
    lstm_output = layers.Flatten()(lstm_output)

    final_output = layers.Dense(200)(lstm_output)
    final_output = layers.Dense(max_index_up_text, activation='softmax')(final_output)

    model = Model(inputs=[up_text, down_text_tensor], outputs=[final_output])
    model.compile(optimizer='Adadelta', loss='mean_squared_error', metrics=['accuracy'])

    return model

def build_reglaiour_model_v1_1_4(max_index_up_text, maxium_legth):
    
    #Decoder part
    #Charater to words 
    up_text = Input(shape=(maxium_legth),
                    name='up_text', dtype='float32')

    up_text_tensor_emb = layers.Embedding(
        max_index_up_text + 1, 64)(up_text)
    cnn_up_output_1 = layers.Conv1D(
        500, 1, padding='same')(up_text_tensor_emb)
    cnn_up_output_2 = layers.Conv1D(
        500, 2, padding='same')(up_text_tensor_emb)
    cnn_up_output_3 = layers.Conv1D(
        500, 3, padding='same')(up_text_tensor_emb)
    cnn_up_output_1 = layers.MaxPool1D(2)(cnn_up_output_1)
    cnn_up_output_2 = layers.MaxPool1D(2)(cnn_up_output_2)
    cnn_up_output_3 = layers.MaxPool1D(2)(cnn_up_output_3)
    cnn_up_all_merge_output = layers.concatenate([cnn_up_output_1, cnn_up_output_2, cnn_up_output_3])
    cnn_up_all_merge_output = layers.Conv1D(500, 2, padding='same')(cnn_up_all_merge_output)

    lstm_up_output = layers.LSTM(600, return_sequences=True, dropout=0.1)(cnn_up_all_merge_output)

    down_text_tensor = Input(
        shape=(maxium_legth),  name='down_text', dtype='float32')

    down_text_tensor_emb = layers.Embedding(
        max_index_up_text + 1, 64)(down_text_tensor)
    cnn_down_output_1 = layers.Conv1D(
        500, 1, padding='same')(down_text_tensor_emb)
    cnn_down_output_2 = layers.Conv1D(
        500, 2, padding='same')(down_text_tensor_emb)
    cnn_down_output_3 = layers.Conv1D(
        500, 3, padding='same')(down_text_tensor_emb)
    cnn_down_output_1 = layers.MaxPool1D(2)(cnn_down_output_1)
    cnn_down_output_2 = layers.MaxPool1D(2)(cnn_down_output_2)
    cnn_down_output_3 = layers.MaxPool1D(2)(cnn_down_output_3)
    cnn_down_all_merge_output = layers.concatenate([cnn_down_output_1, cnn_down_output_2, cnn_down_output_3])
    cnn_down_all_merge_output = layers.Conv1D(500, 2, padding='same')(cnn_down_all_merge_output)
    

    lstm_down_output = layers.LSTM(600, return_sequences=True, dropout=0.1)(cnn_down_all_merge_output)

    lstm_output = layers.concatenate([lstm_up_output, lstm_down_output])
    
    # Words to sentence
    lstm_output = layers.LSTM(600, return_sequences=True)(lstm_output)
    lstm_output = layers.LSTM(700, return_sequences=True)(lstm_output)
    lstm_output = layers.LSTM(800, return_sequences=True)(lstm_output)

    # Convert part
    lstm_output = layers.LSTM(800, return_sequences = True)(lstm_output)
    lstm_output = layers.LSTM(800, return_sequences = True)(lstm_output)

    # Encode part
    lstm_output = layers.LSTM(800)(lstm_output)
    lstm_output = layers.Flatten()(lstm_output)

    final_output = layers.Dense(400)(lstm_output)
    final_output = layers.Dense(200)(lstm_output)
    final_output = layers.Dense(1)(final_output)

    model = Model(inputs=[up_text, down_text_tensor], outputs=[final_output])
    model.compile(optimizer='Adadelta', loss='mean_squared_error', metrics=['accuracy', r2])

    return model

def build_reglaiour_model_v1_1_5(max_index_up_text, maxium_legth):
    
    #Decoder part
    #Charater to words 
    up_text = Input(shape=(maxium_legth),
                    name='up_text', dtype='float32')

    up_text_tensor_emb = layers.Embedding(
        max_index_up_text + 1, 64)(up_text)
    cnn_up_output_1 = layers.Conv1D(
        500, 1, padding='same')(up_text_tensor_emb)
    cnn_up_output_2 = layers.Conv1D(
        500, 2, padding='same')(up_text_tensor_emb)
    cnn_up_output_3 = layers.Conv1D(
        500, 3, padding='same')(up_text_tensor_emb)
    cnn_up_output_1 = layers.MaxPool1D(2, padding='same')(cnn_up_output_1)
    cnn_up_output_2 = layers.MaxPool1D(2, padding='same')(cnn_up_output_2)
    cnn_up_output_3 = layers.MaxPool1D(2, padding='same')(cnn_up_output_3)
    cnn_up_all_merge_output = layers.concatenate([cnn_up_output_1, cnn_up_output_2, cnn_up_output_3])
    cnn_up_all_merge_output = layers.Conv1D(500, 2, padding='same')(cnn_up_all_merge_output)

    lstm_up_output = layers.LSTM(600, return_sequences=True, dropout=0.1)(cnn_up_all_merge_output)

    down_text_tensor = Input(
        shape=(maxium_legth),  name='down_text', dtype='float32')

    down_text_tensor_emb = layers.Embedding(
        max_index_up_text + 1, 64)(down_text_tensor)
    cnn_down_output_1 = layers.Conv1D(
        500, 1, padding='same')(down_text_tensor_emb)
    cnn_down_output_2 = layers.Conv1D(
        500, 2, padding='same')(down_text_tensor_emb)
    cnn_down_output_3 = layers.Conv1D(
        500, 3, padding='same')(down_text_tensor_emb)
    cnn_down_output_1 = layers.MaxPool1D(2, padding='same')(cnn_down_output_1)
    cnn_down_output_2 = layers.MaxPool1D(2, padding='same')(cnn_down_output_2)
    cnn_down_output_3 = layers.MaxPool1D(2, padding='same')(cnn_down_output_3)
    cnn_down_all_merge_output = layers.concatenate([cnn_down_output_1, cnn_down_output_2, cnn_down_output_3])
    cnn_down_all_merge_output = layers.Conv1D(500, 2, padding='same')(cnn_down_all_merge_output)
    

    lstm_down_output = layers.LSTM(600, return_sequences=True, dropout=0.1)(cnn_down_all_merge_output)

    lstm_output = layers.concatenate([lstm_up_output, lstm_down_output])
    
    # Words to sentence
    lstm_output = layers.LSTM(600, return_sequences=True)(lstm_output)
    lstm_output = layers.LSTM(700, return_sequences=True)(lstm_output)
    lstm_output = layers.LSTM(800, return_sequences=True)(lstm_output)

    # Convert part
    lstm_output = layers.LSTM(800, return_sequences = True)(lstm_output)
    lstm_output = layers.LSTM(800, return_sequences = True)(lstm_output)

    # Encode part
    lstm_output = layers.LSTM(800)(lstm_output)
    lstm_output = layers.Flatten()(lstm_output)

    final_output = layers.Dense(400)(lstm_output)
    final_output = layers.Dense(200, activation='tanh')(lstm_output)
    final_output = layers.Dense(1, activation='sigmoid')(final_output)

    model = Model(inputs=[up_text, down_text_tensor], outputs=[final_output])
    model.compile(optimizer='Adam', loss='mean_squared_error', metrics=['accuracy'])

    return model

def build_reglaiour_model_v1_1_6(max_index_up_text, maxium_legth):
    
    #Decoder part
    #Charater to words 
    up_text = Input(shape=(maxium_legth),
                    name='up_text', dtype='float32')

    up_text_tensor_emb = layers.Embedding(
        max_index_up_text + 1, 64)(up_text)
    cnn_up_output_1 = layers.Conv1D(
        500, 1, padding='same')(up_text_tensor_emb)
    cnn_up_output_2 = layers.Conv1D(
        500, 2, padding='same')(up_text_tensor_emb)
    cnn_up_output_3 = layers.Conv1D(
        500, 3, padding='same')(up_text_tensor_emb)
    cnn_up_output_1 = layers.MaxPool1D(2, padding='same')(cnn_up_output_1)
    cnn_up_output_2 = layers.MaxPool1D(2, padding='same')(cnn_up_output_2)
    cnn_up_output_3 = layers.MaxPool1D(2, padding='same')(cnn_up_output_3)
    cnn_up_all_merge_output = layers.concatenate([cnn_up_output_1, cnn_up_output_2, cnn_up_output_3])
    cnn_up_all_merge_output = layers.Conv1D(500, 2, padding='same')(cnn_up_all_merge_output)

    lstm_up_output = layers.LSTM(500, return_sequences=True, dropout=0.1)(cnn_up_all_merge_output)

    down_text_tensor = Input(
        shape=(maxium_legth),  name='down_text', dtype='float32')

    down_text_tensor_emb = layers.Embedding(
        max_index_up_text + 1, 64)(down_text_tensor)
    cnn_down_output_1 = layers.Conv1D(
        500, 1, padding='same')(down_text_tensor_emb)
    cnn_down_output_2 = layers.Conv1D(
        500, 2, padding='same')(down_text_tensor_emb)
    cnn_down_output_3 = layers.Conv1D(
        500, 3, padding='same')(down_text_tensor_emb)
    cnn_down_output_1 = layers.MaxPool1D(2, padding='same')(cnn_down_output_1)
    cnn_down_output_2 = layers.MaxPool1D(2, padding='same')(cnn_down_output_2)
    cnn_down_output_3 = layers.MaxPool1D(2, padding='same')(cnn_down_output_3)
    cnn_down_all_merge_output = layers.concatenate([cnn_down_output_1, cnn_down_output_2, cnn_down_output_3])
    cnn_down_all_merge_output = layers.Conv1D(500, 2, padding='same')(cnn_down_all_merge_output)
    

    lstm_down_output = layers.LSTM(500, return_sequences=True, dropout=0.1)(cnn_down_all_merge_output)

    lstm_output = layers.concatenate([lstm_up_output, lstm_down_output])
    
    # Words to sentence
    lstm_output = layers.LSTM(500, return_sequences=True)(lstm_output)
    lstm_output = layers.LSTM(600, return_sequences=True)(lstm_output)

    # Convert part
    lstm_output = layers.LSTM(600, return_sequences = True)(lstm_output)

    # Encode part
    lstm_output = layers.LSTM(600)(lstm_output)
    lstm_output = layers.Flatten()(lstm_output)

    final_output = layers.Dense(400)(lstm_output)
    final_output = layers.Dense(200, activation='tanh')(lstm_output)
    final_output = layers.Dense(maxium_legth, activation='sigmoid')(final_output)

    model = Model(inputs=[up_text, down_text_tensor], outputs=[final_output])
    model.compile(optimizer='Adam', loss='mse')

    return model



def build_reglaiour_model(max_index_up_text, maxium_legth):

    up_text = Input(shape=(None, maxium_legth),
                    name='up_text', dtype='float32')

    up_text_emb = layers.Embedding(max_index_up_text + 1, 64)(up_text)

    cnn_up_text_1 = layers.Conv1D(500, 1, padding='same')(up_text_emb)
    cnn_up_text_2 = layers.Conv1D(500, 2, padding='same')(up_text_emb)
    cnn_up_text_3 = layers.Conv1D(500, 4, padding='same')(up_text_emb)

    cnn_up_output = layers.add([cnn_up_text_1, cnn_up_text_2, cnn_up_text_3])
    cnn_up_output = layers.Reshape((maxium_legth, 500))(cnn_up_output)

    lstm_up_output = layers.LSTM(600)(cnn_up_output)

    down_text_tensor = Input(
        shape=(None, maxium_legth),  name='down_text', dtype='float32')

    down_text_tensor_emb = layers.Embedding(
        max_index_up_text + 1, 64)(down_text_tensor)
    cnn_down_output_1 = layers.Conv1D(
        500, 1, padding='same')(down_text_tensor_emb)
    cnn_down_output_2 = layers.Conv1D(
        500, 2, padding='same')(down_text_tensor_emb)
    cnn_down_output_3 = layers.Conv1D(
        500, 3, padding='same')(down_text_tensor_emb)

    cnn_down_output = layers.add(
        [cnn_down_output_1, cnn_down_output_2, cnn_down_output_3])
    cnn_down_output = layers.Reshape(
        (maxium_legth, 500))(cnn_down_output)

    lstm_down_output = layers.LSTM(600)(cnn_down_output)

    lstm_output = layers.concatenate([lstm_up_output, lstm_down_output])
    lstm_output = layers.Flatten()(lstm_output)

    final_output = layers.Dense(200)(lstm_output)
    final_output = layers.Dense(1)(final_output)

    model = Model(inputs=[up_text, down_text_tensor], outputs=[final_output])
    model.compile(optimizer='Adadelta', loss='mean_squared_error', metrics=['accuracy', r2])

    return model


data_root_dir = 'E:\\爬虫\\test-data\\merged-data'
enc_dict_root_dir = 'E:\\爬虫\\test-data\\merged-data'
model_root_path = 'E:\\爬虫\\Fake-GPT3\\models\\tagged-bigger-data'
merged_data_root_path = 'E:\\爬虫\\test-data\\merged-data'

make_new_data = True
make_new_model = True
merged_data = True

load_model_data = False
load_arry_data = False

fit_model = True
r2_based_testing = False
show_predictoutput = False
test_accuracy = False

model_file_name = 'result_verson_1_6.h5'

percent_of_transet = 0.5
testset_precent = 0.5

os.chdir(data_root_dir)



if load_arry_data:
    try:
        os.chdir(data_root_dir)
        all_in_one_data = np.load('data_train_test_all_in_one.npz')
    except:
        print("Could not read numpy data file")
        make_new_data = True
    if make_new_data == False:
        train_up_arry = all_in_one_data['train_up_arry']
        train_down_arry = all_in_one_data['train_down_arry']
        train_target_arry = all_in_one_data['train_target_arry']

        if test_accuracy:
            test_up_arry = all_in_one_data['test_up_arry']
            test_down_arry = all_in_one_data['test_down_arry']
            test_target_arry = all_in_one_data['test_target_arry']
            test_target_orinal_arry = all_in_one_data['test_target_orianl_arry']
            maxium_legth = all_in_one_data['maxium_legth']
            maxium_legth = maxium_legth.tolist()

        if make_new_model:
            maxium_legth = all_in_one_data['maxium_legth']
            max_enc_index = all_in_one_data['max_enc_index']
            maxium_legth = maxium_legth.tolist()
            max_enc_index = max_enc_index.tolist()

if load_model_data:
    try:
        os.chdir(model_root_path)
        model_file_name = os.path.join(model_root_path, model_file_name)
        model = load_model(model_file_name, custom_objects={'r2': r2})
    except:
        print("Could not load model from " +
              model_file_name + "in " + model_root_path)
if make_new_data:
    if merged_data == False:
        try:
            encode_comment_dict_file = open(
                'encode_comment_dict.json', 'r', encoding='utf-8')
        except:
            print("Could not read encode_comment_dict, are you sure you genterned it?")
            exit()
        encode_comment_dict = json.load(encode_comment_dict_file)
    else:
        try:
            merged_encode_comment_dict_file = open(os.path.join(merged_data_root_path, 'merged_encode_comment_dict.json'))
        except:
            print("Could not read merged_encode_comment_dict, are you sure you have it?")
            exit()
        merged_encode_comment_dict = json.load(merged_encode_comment_dict_file)
        encode_comment_dict = {}
        for main_key in list(merged_encode_comment_dict.keys()):
            currrent_process_data_dict = merged_encode_comment_dict[main_key]
            for reply_id in list(currrent_process_data_dict.keys()):
                encode_comment_dict[reply_id] = currrent_process_data_dict[reply_id]

    os.chdir(enc_dict_root_dir)
    try:
        enc_dict_file = open('enc_dict.json', 'r', encoding='utf-8')
    except:
        print("Could not read enc_dict, are you sure you have it?")
        exit()

    enc_dict = json.load(enc_dict_file)

    print("Inirliazing dataset...")
    target_list_sort, up_list_sort, down_list_sort = gpt_dataset_builder(
        encode_comment_dict)

    print("Randomizing dataset...")
    target_list_rand, up_list_rand, down_list_rand = random_up(
        target_list_sort, up_list_sort, down_list_sort)

    print("Split the dataset ")
    train_up_list, test_up_list, train_down_list, test_down_list, train_target_list, test_target_list, = split_dataset(
        percent_of_transet, testset_precent, target_list_rand, up_list_rand, down_list_rand)

    print("Calculating the legth of each data")
    maxium_train_up_legth = max([len(i) for i in train_up_list]) + 1
    maxium_train_target_legth = 1
    maxium_train_down_legth = max([len(i) for i in train_down_list]) + 1

    maxium_test_up_legth = max([len(i) for i in test_up_list]) + 1
    maxium_test_down_legth = max([len(i) for i in test_down_list]) + 1
    maxium_test_target_legth = 1

    train_up_count = len(train_up_list)
    train_down_count = len(train_down_list)
    train_target_count = len(train_target_list)

    test_up_count = len(test_up_list)
    test_down_count = len(test_down_list)
    test_target_count = len(test_target_list) 

    maxium_legth = max([maxium_train_up_legth, maxium_train_down_legth]) + 1
    max_enc_index = len(list(enc_dict.keys()))

    print("Initlazing up array...")
    train_up_arry = np.zeros(
        (train_up_count, maxium_legth), dtype=np.float32)
    train_target_arry = np.zeros((train_target_count, maxium_legth), dtype=np.float32)
    train_down_arry = np.zeros(
        (train_down_count, maxium_legth), dtype=np.float32)

    test_up_arry = np.zeros(
        (test_up_count, maxium_legth), dtype=np.float32)
    test_target_arry = np.zeros(
        (test_target_count, maxium_legth), dtype=np.float32)
    test_target_orinal_arry = np.zeros(
        (test_target_count, maxium_legth), dtype=np.float32)
    test_down_arry = np.zeros(
        (test_down_count,  maxium_legth), dtype=np.float32)

    print("transforming list to numpy array...")

    @nb.jit
    def up_trans_train_arrary():
        for splet_index, train_spelt in tqdm(enumerate(train_up_list), total=len(train_up_list)):
            for charater_index, charater in enumerate(train_spelt):
                train_up_arry[splet_index,
                              charater_index] = charater / max_enc_index

    up_trans_train_arrary()
    print(train_up_arry)

    @nb.jit
    def target_trans_train_arrary():
        for splet_index, train_spelt in tqdm(enumerate(train_target_list), total=len(train_target_list)):
            for charater_index, charater in enumerate(train_spelt):
                train_target_arry[splet_index, charater_index] = charater / max_enc_index

    target_trans_train_arrary()

    @nb.jit
    def down_trans_train_arrary():
        for splet_index, train_spelt in tqdm(enumerate(train_down_list), total=len(train_down_list)):
            for charater_index, charater in enumerate(train_spelt):
                train_down_arry[splet_index,
                                charater_index] = charater / max_enc_index

    down_trans_train_arrary()

    @nb.jit
    def up_trans_test_arrary():
        for splet_index, test_spelt in tqdm(enumerate(test_up_list), total=len(test_up_list)):
            for charater_index, charater in enumerate(test_spelt):
                test_up_arry[splet_index,
                             charater_index] = charater / max_enc_index

    up_trans_test_arrary()

    @nb.jit
    def target_trans_test_arrary():
        for splet_index, test_spelt in tqdm(enumerate(test_target_list), total=len(test_target_list)):
            for charater_index, charater in enumerate(test_spelt):
                test_target_arry[splet_index, charater_index] = charater / max_enc_index


    target_trans_test_arrary()

    def target_trans_test_orinal_arrary():
        for splet_index, test_spelt in tqdm(enumerate(test_target_list), total=len(test_target_list)):
            for charater_index, charater in enumerate(test_spelt):
                test_target_orinal_arry[splet_index, charater_index] = charater 


    target_trans_test_orinal_arrary()

    @nb.jit
    def down_trans_test_arrary():
        for splet_index, test_spelt in tqdm(enumerate(test_down_list), total=len(test_down_list)):
            for charater_index, charater in enumerate(test_spelt):
                test_down_arry[splet_index,
                               charater_index] = charater / max_enc_index

    down_trans_test_arrary()

    os.chdir(data_root_dir)
    np.savez_compressed('data_train_test_all_in_one', train_up_arry=train_up_arry, train_down_arry=train_down_arry, train_target_arry=train_target_arry,
                        test_up_arry=test_up_arry, test_down_arry=test_down_arry, test_target_arry=test_target_arry, test_target_orianl_arry= test_target_orinal_arry, max_enc_index=max_enc_index, maxium_legth=maxium_legth)


if make_new_model:
    print("building model")

    # model = build_reglaiour_model(max_enc_index, maxium_legth)
    model = build_reglaiour_model_v1_1_6(max_enc_index, maxium_legth)
    model.save(os.path.join(model_root_path,"init_verson_1_6.h5"))
    print(model.summary())
if fit_model:
    print("Starting fitting model...")
    tensor_callback = callbacks.TensorBoard(
        log_dir='E:\\爬虫\\Fake-GPT3\\tensorboard\\tagged-bigger-data', histogram_freq=1, embeddings_freq=1, update_freq='batch')
    save_checkpoint = callbacks.ModelCheckpoint("E:\\爬虫\\Fake-GPT3\\Check-point\\tagged-bigger-data\\best_train_loss_1_6.h5",
                                                monitor='train_loss', verbose=1, save_best_only=False, save_weights_only=False, mode='auto', period=1)

    auto_stop = callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=0,
                                        verbose=0, mode='auto', baseline=None, restore_best_weights=False)

    model.fit({'up_text': train_up_arry, 'down_text': train_down_arry},
            train_target_arry, verbose=1, callbacks=[tensor_callback, save_checkpoint,auto_stop], epochs=10, validation_split=0.4, batch_size=30)
    model.save(os.path.join(model_root_path,"result_verson_1_6.h5"))

if r2_based_testing:
    from sklearn.metrics import r2_score
    model_output_array = model.predict({'up_text': test_up_arry, 'down_text': test_down_arry})
    r2_ouput = r2_score(test_target_arry, model_output_array)
    print('r2_socre : '+ str(r2_ouput))

if show_predictoutput:
    import random
    max_spelt_index = len(test_target_arry)
    model_output_array = model.predict({'up_text': test_up_arry, 'down_text': test_down_arry})

    current_spelt_index = random.randint(0, max_spelt_index -1 )

    current_test_up_arry = test_up_arry[current_spelt_index]
    current_test_down_arry = test_down_arry[current_spelt_index]
    current_test_target_arry = test_target_arry[current_spelt_index]

    print('model_output:')
    print(model_output_array)
    print('expected output:')
    print(test_target_arry)
if test_accuracy :
    import random
    from keras.losses import mean_squared_error
    max_spelt_index = len(test_target_arry)
    index_exit_list = []

    current_test_up_arry = np.zeros((99, maxium_legth), dtype=np.float32)
    current_test_down_arry = np.zeros((99, maxium_legth), dtype=np.float32)
    current_test_target_orinal_arry = np.zeros((99, maxium_legth), dtype=np.float32)
    current_test_target_arry = np.zeros((99, maxium_legth), dtype=np.float32)

    for control_index in range(0, 99):
        current_spelt_index = random.randint(0, max_spelt_index)
        while current_spelt_index in index_exit_list :
            current_spelt_index = random.randint(0, max_spelt_index)

        current_test_up_arry[control_index] = test_up_arry[current_spelt_index]
        current_test_down_arry[control_index] = test_down_arry[current_spelt_index]
        current_test_target_arry[control_index] = test_target_arry[current_spelt_index]
        current_test_target_orinal_arry[control_index] = test_target_orinal_arry[current_spelt_index]
        index_exit_list.append(current_spelt_index)

    model_output_array = model.predict({'up_text': current_test_up_arry, 'down_text': current_test_down_arry})

    avange_accuracy_orinal_split_list = []
    avange_worng_distance_orinal_split_list = []

    for accuracy_test_index in range(0,len(model_output_array) - 1):
        current_accuracy_test_target_orinal_arry = current_test_target_orinal_arry[accuracy_test_index]
        current_accuracy_test_model_output_array = model_output_array[accuracy_test_index]

        worng_count = 0
        worng_distance_list = []
        for split_accuracy_test_index in range(0,len(current_accuracy_test_model_output_array) - 1):
            orinal_test_target = current_accuracy_test_target_orinal_arry[split_accuracy_test_index]
            orinal_model_output = current_accuracy_test_model_output_array[split_accuracy_test_index] * max_enc_index

            if orinal_model_output > int(orinal_model_output) + 0.5 or orinal_model_output == int(orinal_model_output) + 0.5 :
                orinal_model_output = int(orinal_model_output) + 1
            else:
                orinal_model_output = int(orinal_model_output)
            
            if orinal_model_output != orinal_test_target :
                worng_count += 1
                worng_distance_list.append(orinal_model_output - orinal_test_target)
        
        avange_accuracy_orinal_split_list.append(worng_count / maxium_legth)
        avange_worng_distance_orinal_split_list.append(sum(worng_distance_list) / maxium_legth)
    
    avange_accuracy_orinal = sum(avange_accuracy_orinal_split_list) / 100
    avange_worng_distance_orinal = sum(avange_worng_distance_orinal_split_list) / 100
    testset_loss = mean_squared_error(current_test_target_arry, model_output_array)

    print("Test set loss is :")
    print(testset_loss)
    print("The avange accuracy when you use it: ")
    print(avange_accuracy_orinal)
    print("The avange worng distance when you use it :")
    print(avange_accuracy_orinal)

exit()




    
    