import os, sys, pickle, time
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import keras.backend as K 
from textdistance import levenshtein

def create_decode_fctn(model): 
  melspec_input = model.get_layer('melspec_input').input
  pred_len = K.squeeze(model.get_layer('pred_len').input, axis=-1)
  y_pred = model.get_layer('y_pred').output[:, 2:, :]

  top_k_decoded, _ = K.ctc_decode(y_pred, pred_len, greedy=False, beam_width=10)
  
  return K.function([melspec_input, pred_len], [top_k_decoded[0]])

def aggregate_per_avg(bt_size, all_size, bt_per, all_per):
  alpha = bt_size / all_size
  return (alpha * bt_per) + ((1.0 - alpha) * all_per)

def calc_per_single(pred_seq, true_seq):
  pred_seq = pred_seq.tolist()
  true_seq = true_seq.tolist()
  # print ('true ori:', true_seq)
  # print ('pred ori:', pred_seq)

  pred_seq = pred_seq[ : rindex(pred_seq, 0) + 1 ]
  true_seq = true_seq[ : true_seq.index(0) + 1 ]
  PER = float(levenshtein.distance(pred_seq, true_seq)) / float( len(true_seq) )
  # print ('true:', true_seq)
  # print ('pred:', pred_seq)
  # print ('PER: ', PER)
  # print ('===============================================')

  return PER

def rindex(arr, val):
  try:
    return len(arr) - arr[::-1].index(val) - 1
  except:
    return len(arr) - 1