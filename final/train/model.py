import os, pickle, time
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import keras.backend as K
from keras.models import Model
from keras.layers import Input, Dense, GRU, Bidirectional, Lambda, Dropout, Conv2D, BatchNormalization, Reshape
from keras.layers import ReLU

def ctc_loss_fctn(args):
  y_pred, y_true, pred_len, label_len = args
  return K.ctc_batch_cost(y_true, y_pred[:, 2:, :], pred_len, label_len)

def ds2_model(phone_classes, freq_dim=128, fc_size=1024, rnn_size=512, rnn_layers=3):
  melspec_input = Input(shape=(None, freq_dim), name='melspec_input')
  x = Lambda(lambda x: K.expand_dims(x))(melspec_input)
  print (x.shape)

  x = Conv2D(filters=32, kernel_size=(11, 32), strides=(2, 2), padding='same', activation='relu', name='conv2d_1')(x)
  x = Conv2D(filters=32, kernel_size=(11, 16), strides=(2, 2), padding='same', activation='relu', name='conv2d_2')(x)
  x = Conv2D(filters=96, kernel_size=(7, 16), strides=(2, 2), padding='same', activation='relu', name='conv2d_3')(x)
  print (x.shape)

  x = Reshape((-1, int(x.shape[2] * x.shape[3])))(x)
  print (x.shape)

  for l in range(rnn_layers):
    x = BatchNormalization(axis=-1)(x)
    x = Bidirectional(GRU(rnn_size, return_sequences=True, name='gru_{}'.format(l+1)))(x)
    print (x.shape)

  y_pred = Dense(phone_classes, activation='softmax', name='y_pred')(x)
  print (y_pred.shape)

  y_label = Input(shape=(None,), dtype='int32', name='y_label')
  label_len = Input(shape=(1,), dtype='int32', name='label_len')
  pred_len = Input(shape=(1,), dtype='int32', name='pred_len')

  ctc_loss = Lambda(ctc_loss_fctn, output_shape=(1,), name='ctc_loss')([y_pred, y_label, pred_len, label_len])

  return Model(inputs=[melspec_input, y_label, pred_len, label_len], outputs=ctc_loss)

if __name__ == '__main__':
  model = ds2_model(219)
  model.summary()
