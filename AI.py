import keras
from keras import Input, layers
from keras.models import Model
def text_encode():
    for charater in text:
        if charater not in encode.keys():
            text_number[len(text_number)] = 0
            continue
        text_number[len(text_number)]=encode[str(charater)]

def basic_ana_model_build():
    model_input = Input(shape=200,)
    x = layers.Embedding(1000)(x)
    x = layers.Conv1D(40,6,activation='relu')(x)
    x = layers.Embedding(700)(x)
    x = layers.LSTM(800)(x)
    x = layers.LSTM(800)(x)
    kind_output = layers.Dense(400,activation='sigmod',name='kind')(x)
    happy_output = layers.Dense(400,activation='sigmoid',name='happy_index')(x)
    angry_output = layers.Dense(400,activation='sigmoid',name='angry_index')(x)
    sad_output = layers.Dense(400,activation='sigmoid',name='sad_index')(x)
    model = Model(model_input,[kind_output,happy_output,angry_output,sad_output])
    model.compile(optimizer='rmsprop',loss={'kind':'binary_crossentropy','happy_index':'mse','angry_index':'mse','sad_index':'mse'})
    model.save(model_file_path)

def model_train():
    text_encode()
    model.fit(text_tensor,label_dire,epochs=100,batch_size=80)
    model.save(model_file_path)



