import os, pickle, time
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import keras.backend as K
from keras.callbacks import Callback
from math import ceil
from textdistance import levenshtein

class ValPERCallback(Callback):
  def __init__(self, decode_fctn, train_gen, val_gen):
    self.decode_fctn = decode_fctn
    self.train_gen = train_gen
    self.val_gen = val_gen
    self.mean_per_log = []
    self.mean_val_per_log = []

  def on_train_begin(self, logs={}):
    if 'mean_per' not in self.params['metrics']:
      self.params['metrics'].append('mean_per')
    if 'val_mean_per' not in self.params['metrics']:
      self.params['metrics'].append('val_mean_per')

    logs['mean_per'] = float('inf')
    logs['val_mean_per'] = float('inf')

    return

  def on_epoch_end(self, epoch, logs={}):
    K.set_learning_phase(0)
    train_per, val_per = self.calc_per_epoch_end()
    logs['mean_per'], logs['val_mean_per'] = train_per, val_per
    K.set_learning_phase(1)

    return

  def calc_per_epoch_end(self):
    self.train_gen.cur_idx = 0
    self.val_gen.cur_idx = 0

    train_sent_cnt = 0
    val_sent_cnt = 0
    train_avg_per = 0.0
    val_avg_per = 0.0

    train_n_batches = ceil( self.train_gen.num_samples / self.train_gen.batch_size )
    val_n_batches = ceil( self.val_gen.num_samples / self.val_gen.batch_size )

    for b in range(train_n_batches):
      batch = next( self.train_gen.next_batch() )[0]
      decoded_seqs = self.decode_fctn(
        [batch['melspec_input'], batch['pred_len']]
      )[0]

      batch_n_samples = decoded_seqs.shape[0]
      batch_per_tot = 0.0

      for i in range( batch_n_samples ):
        train_sent_cnt += 1
        batch_per_tot += calc_per_single(decoded_seqs[i], batch['y_label'][i])

      train_avg_per = aggregate_per_avg(batch_n_samples, train_sent_cnt, batch_per_tot / batch_n_samples, train_avg_per)

    for b in range(val_n_batches):
      batch = next( self.val_gen.next_batch() )[0]
      decoded_seqs = self.decode_fctn(
        [batch['melspec_input'], batch['pred_len']]
      )[0]

      batch_n_samples = decoded_seqs.shape[0]
      batch_per_tot = 0.0

      for i in range( batch_n_samples ):
        val_sent_cnt += 1
        batch_per_tot += calc_per_single(decoded_seqs[i], batch['y_label'][i])

      val_avg_per = aggregate_per_avg(batch_n_samples, val_sent_cnt, batch_per_tot / batch_n_samples, val_avg_per)
    
    print ('Train Avg PER --', 100 * train_avg_per, '%%')
    print ('Val Avg PER --', 100 * val_avg_per, '%%')

    self.mean_per_log.append( train_avg_per )
    self.mean_val_per_log.append( val_avg_per )

    return train_avg_per, val_avg_per

def aggregate_per_avg(bt_size, all_size, bt_per, all_per):
  alpha = bt_size / all_size
  return (alpha * bt_per) + ((1.0 - alpha) * all_per)

def calc_per_single(pred_seq, true_seq):
  pred_seq = pred_seq.tolist()
  true_seq = true_seq.tolist()

  pred_seq = pred_seq[ : rindex(pred_seq, 0) + 1 ]
  true_seq = true_seq[ : true_seq.index(0) + 1 ]

  return float(levenshtein.distance(pred_seq, true_seq)) / float( len(true_seq) )

def rindex(arr, val):
  try:
    return len(arr) - arr[::-1].index(val) - 1
  except:
    return len(arr) - 1