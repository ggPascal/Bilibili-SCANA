import random as rd
from keras.models import Model
from keras import layers
from keras import Input
from keras import callbacks
import os
import json
import numpy as np

def gpt_dataset_builder(comment_data_dict):
    proccess_index = 0
    target_list_sort = []
    up_list_sort = []
    down_list_sort = []

    for reply_id in list(comment_data_dict.keys()):
        current_encoded_message = comment_data_dict[reply_id]
        while proccess_index < len(current_encoded_message):
            if proccess_index == 0:
                current_up_list = [0]
            else:
                for up_index in range(0, proccess_index - 1):
                    current_up_list.append(current_encoded_message[up_index])
            if proccess_index == len(current_encoded_message) - 1 :
                current_down_list = [0]
            else:
                for down_index in range(proccess_index + 1, len(current_encoded_message) - 1):
                    current_down_list.append(current_encoded_message[down_index])
            target_list_sort.append(current_encoded_message[proccess_index])
            up_list_sort.append(current_up_list)
            down_list_sort.append(current_down_list)
    return target_list_sort, up_list_sort, down_list_sort

def random_up(target_list_sort, up_list_sort, down_list_sort):
    for rand_index in range(0, len(target_list_sort) - 1):

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

def split_dataset(percent, testset_present,target_list_rand, up_list_rand, down_list_rand):
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

    maxium_trainset_index = int((len(target_list_rand)- 1) * percent) 
    for split_index in range(0, maxium_trainset_index):
        train_target_list[split_index] = target_list_rand[split_index]
        train_up_list[split_index] = up_list_rand[split_index]
        train_down_list[split_index] = down_list_rand[split_index]
    
    minimize_testset_index = maxium_trainset_index + 1
    maxium_testset_index = int((len(target_list_rand)- 1 - minimize_testset_index)* testset_present) + minimize_testset_index
    split_index = 0 
    for split_index in range(minimize_testset_index, maxium_testset_index):
        test_target_list.append(target_list_rand[split_index])
        test_up_list.append(up_list_rand[split_index])
        test_down_list.append(up_list_rand[split_index])

    minimize_valset_index = maxium_testset_index + 1
    split_index = 0
    for split_index in range(minimize_valset_index, len(test_down_list) - 1):
        val_target_list.append(target_list_rand[split_index])
        val_up_list[split_index].append(up_list_rand[split_index])
        val_down_list[split_index].append(down_list_rand[split_index])
    

    return train_up_list, test_up_list,val_up_list ,train_down_list, test_down_list,val_down_list, train_target_list, test_target_list, val_target_list


def build_reglaiour_model(max_index_up_text):
    up_text = Input(shape=(None,), dtype='int32', name='up_text')
    down_text = Input(shape=(None,), dtype='int32', name='down_text')

    up_text = layers.Embedding(max_index_up_text, 64)

    cnn_up_text_1 = layers.Conv1D(500,1)(up_text)
    cnn_up_text_2 = layers.Conv1D(250,2)(up_text)
    cnn_up_text_3 = layers.Conv1D(125,4)(up_text)

    cnn_output = layers.Concatenate([cnn_up_text_1, cnn_up_text_2, cnn_up_text_3])

    lstm_output = layers.LSTM(600, return_sequences=True)(cnn_output)
    lstm_output = layers.LSTM(500, return_sequences=True)(lstm_output)
    lstm_output = layers.LSTM(400, return_sequences=True)(lstm_output)
    lstm_output = layers.LSTM(300)(lstm_output)

    final_output = layers.Dense(200)

    model = Model([up_text, down_text], final_output)
    model.compile(optimizer='RMSprop', loss='mse', metrics=['accuracy'])

    return model


data_root_dir = 'E:\\爬虫\\test-data\\BV1av411v7E1'
enc_dict_root_dir = 'E:\\爬虫\\test-data\\dec-enc-dict'

percent_of_transet = 0.5
testset_precent = 0.5

os.chdir(data_root_dir)
try:
    encode_comment_dict_file = open('encode_comment_dict.json','r', encoding='utf-8')
except:
    print("Could not read encode_comment_dict, are you sure you genterned it?")
    exit()

os.chdir(enc_dict_root_dir)
try:
    enc_dict_file = open('enc_dict.json', 'r', encoding='utf-8')
except:
    print("Could not read enc_dict, are you sure you have it?")
    exit()

enc_dict = json.load(enc_dict_file)
encode_comment_dict = json.load(encode_comment_dict_file)

print("building model")
max_enc_index = len(list(enc_dict.keys())) - 1
model = build_reglaiour_model(max_enc_index)

print("Inirliazing dataset...")
target_list_sort, up_list_sort, down_list_sort = gpt_dataset_builder(encode_comment_dict)

print("Randomizing dataset...")
target_list_rand, up_list_rand, down_list_rand = random_up(target_list_sort, up_list_sort, down_list_sort)

print("Split the dataset ")
train_up_list, test_up_list,val_up_list ,train_down_list, test_down_list,val_down_list, train_target_list, test_target_list, val_target_list = split_dataset(percent, testset_precent, target_list_rand, up_list_rand, down_list_rand)

print("transforming list to numpy array...")
train_up_arry = np.array(train_up_list)
train_target_arry = np.array(train_target_list)
train_down_arry = np.array(train_down_list)

test_up_arry = np.array(test_up_list)
test_target_arry = np.array(test_target_list)
test_down_arry = np.array(test_down_list)

val_target_arry = np.array(val_target_list)
val_down_arry = np.array(val_down_list)
val_up_arry = np.array(val_up_list)

print("Starting fitting model...")
tensor_callback = callbacks.TensorBoard(log_dir = './tesorboard', histogram_freq= 1, embeddings_freq= 1)
model.fit({'up_text': train_up_arry, 'down_text': train_down_arry}, train_target_arry,validation_data=({'up_text':val_up_arry, 'down_text':val_down_arry}, val_target_arry), verbose= 1 , callbacks= tensor_callback)




            