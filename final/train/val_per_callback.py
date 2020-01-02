import os, pickle, time
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import keras.backend as K
from keras.callbacks import Callback
from math import ceil
import matplotlib.pyplot as plt
from score_utils import aggregate_per_avg, calc_per_single, rindex

class ValPERCallback(Callback):
  def __init__(self, decode_fctn, train_gen, val_gen, model_dir):
    self.decode_fctn = decode_fctn
    self.train_gen = train_gen
    self.val_gen = val_gen
    self.mean_per_log = []
    self.mean_val_per_log = []
    self.shuffle = shuffle
    self.train_eval_samples = min(train_gen.num_samples, 1024)
    self.model_dir = model_dir
    self.record_file = open(model_dir + 'training.log', 'w')

  def on_train_begin(self, logs={}):
    if 'mean_per' not in self.params['metrics']:
      self.params['metrics'].append('mean_per')
    if 'val_mean_per' not in self.params['metrics']:
      self.params['metrics'].append('val_mean_per')

    logs['mean_per'] = float('inf')
    logs['val_mean_per'] = float('inf')
    self.record_file.write('Training on {} samples / Validating on {} samples\n'.format(self.train_gen.num_samples, self.val_gen.num_samples))
    self.record_file.write('===========================================================\n')

    return

  def on_train_end(self, logs={}):
    self.record_file.close()

    self.record_file = open(self.model_dir + 'per.log', 'w')
    self.record_file.write('+++++ Train mean PERs +++++\n')
    for i, per in enumerate(self.mean_per_log):
      self.record_file.write('  Epoch %02d: %.4f percent' % (i+1, per) )
      self.record_file.write('\n')
    self.record_file.write('++++++ Val mean PERs ++++++\n')
    for i, per in enumerate(self.mean_val_per_log):
      self.record_file.write('  Epoch %02d: %.4f percent' % (i+1, per) )
      self.record_file.write('\n')
    self.record_file.close()

    plt.plot( self.mean_per_log )
    plt.plot( self.mean_val_per_log )
    plt.title('Phoneme Error Rate (%)')
    plt.xlabel('Epoch')
    plt.ylabel('PER (%)')
    plt.legend(['train', 'val'])
    plt.show(block=False)
    plt.savefig(self.model_dir + 'per.png')

    return

  def on_epoch_end(self, epoch, logs={}):
    K.set_learning_phase(0)

    if self.shuffle:
      self.train_gen.shuffle_dataset()
    
    train_per, val_per = self.calc_per_epoch_end(epoch)
    logs['mean_per'], logs['val_mean_per'] = train_per, val_per
    K.set_learning_phase(1)

    return

  def calc_per_epoch_end(self, epoch):
    self.train_gen.cur_idx = 0
    self.val_gen.cur_idx = 0

    train_sent_cnt = 0
    val_sent_cnt = 0
    train_avg_per = 0.0
    val_avg_per = 0.0

    train_n_batches = ceil( self.train_eval_samples / self.train_gen.batch_size )
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

    val_per_records = []
    for b in range(val_n_batches):
      batch = next( self.val_gen.next_batch() )[0]
      decoded_seqs = self.decode_fctn(
        [batch['melspec_input'], batch['pred_len']]
      )[0]

      batch_n_samples = decoded_seqs.shape[0]
      batch_per_tot = 0.0

      for i in range( batch_n_samples ):
        val_sent_cnt += 1
        if b == 0:
          val_per_records.append( calc_per_single(decoded_seqs[i], batch['y_label'][i]) )
          batch_per_tot += val_per_records[-1]
        else:
          batch_per_tot += calc_per_single(decoded_seqs[i], batch['y_label'][i])

      val_avg_per = aggregate_per_avg(batch_n_samples, val_sent_cnt, batch_per_tot / batch_n_samples, val_avg_per)

      if b == 0:
        self.dump_val_records(epoch, val_per_records, decoded_seqs, batch['y_label'])
    
    print ('Train #samples --', train_sent_cnt)
    print ('Val #samples --', val_sent_cnt)
    print ('Train Avg PER --', 100 * train_avg_per, '%')
    print ('Val Avg PER --', 100 * val_avg_per, '%')

    self.dump_epoch_records(train_sent_cnt, val_sent_cnt, train_avg_per, val_avg_per)

    self.mean_per_log.append( 100 * train_avg_per )
    self.mean_val_per_log.append( 100 * val_avg_per )

    return train_avg_per, val_avg_per

  def dump_val_records(self, epoch, val_pers, preds, labels):
    self.record_file.write( 'Epoch {}:\n'.format(epoch+1) )
    self.record_file.write('===========================================================\n')
    for i in range( min(16, len(val_pers)) ):
      self.record_file.write('pred {}: {}\n'.format(i, preds[i]))
      self.record_file.write('true {}: {}\n'.format(i, labels[i]))
      self.record_file.write('PER: {}\n'.format(val_pers[i]))
      self.record_file.write('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')

    return

  def dump_epoch_records(self, train_cnts, val_cnts, train_per, val_per):
    self.record_file.write('Train #samples -- {}\n'.format(train_cnts))
    self.record_file.write('Val #samples -- {}\n'.format(val_cnts))
    self.record_file.write('Train Avg PER -- {} %\n'.format(100 * train_per))
    self.record_file.write('Val Avg PER -- {} %\n'.format(100 * val_per))
    self.record_file.write('===========================================================\n')

    return