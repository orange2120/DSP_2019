import os, sys, pickle, time
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import keras.backend as K
import pandas as pd
from keras.optimizers import Adam
from math import ceil

from batch_generator import BatchGenerator
from model import ds2_model
from val_per_callback import ValPERCallback

def read_data_df(csv_path):
  df = pd.read_csv(csv_path, encoding='utf-8')
  print (df.info())
  print (df.head())
  return df

def load_phone_tokenizer(tkn_path):
  tkn = pickle.load( open(tkn_path, 'rb') )
  print ('tokenizer dict size:', tkn.dict_size)
  return tkn

if __name__ == '__main__':
  train_df, val_df = read_data_df(sys.argv[1])[:300], read_data_df(sys.argv[2])[:120]
  phone_tokenizer = load_phone_tokenizer(sys.argv[3])
  lr = float( sys.argv[4] )
  bt_size = int( sys.argv[5] )

  train_btgen = BatchGenerator(train_df, is_train=True, batch_size=bt_size)
  val_btgen = BatchGenerator(val_df, is_train=False, batch_size=bt_size)

  model = ds2_model(phone_tokenizer.dict_size + 2)
  model.summary()
  
  adam_opt = Adam(lr=lr)
  model.compile(
    adam_opt, 
    loss={'ctc_loss': lambda y_true, y_pred: y_pred}
  )

  # Validation Callback -- decode to phoneme sequences
  melspec_input = model.get_layer('melspec_input').input
  pred_len = K.squeeze(model.get_layer('pred_len').input, axis=-1)
  y_pred = model.get_layer('y_pred').output[:, 2:, :]

  top_k_decoded, _ = K.ctc_decode(y_pred, pred_len, greedy=False, beam_width=10)
  decode_fctn = K.function([melspec_input, pred_len], [top_k_decoded[0]])

  val_cb = ValPERCallback(decode_fctn, train_btgen, val_btgen)

  model.fit_generator(
    generator=train_btgen.next_batch(),
    steps_per_epoch=ceil( train_btgen.num_samples / bt_size ),
    epochs=20,
    validation_data=val_btgen.next_batch(),
    validation_steps=ceil( val_btgen.num_samples / bt_size ),
    callbacks=[val_cb]
  )
