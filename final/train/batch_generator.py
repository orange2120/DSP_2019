import ast, pickle
import numpy as np
from copy import deepcopy
from sklearn.utils import shuffle

class BatchGenerator(object):
  def __init__(self, dataframe, is_train, batch_size, normalize=True, shuffle=True, n_mels=128, conv_factor=8):
    self.is_train = is_train
    self.df = dataframe.copy()
    self.batch_size = batch_size

    self.melspec_path = self.df['melspec_path'].tolist()
    self.melspec_len = self.df['melspec_len'].tolist()

    if self.is_train:
      self.phone_seq = self.phone_seq_str_to_list( self.df['phone_seq'].tolist() )
      self.phone_seq_len = self.df['phone_seq_len'].tolist()
    else:
      self.phone_seq = None
      self.phone_seq_len = None

    self.num_samples = len( self.melspec_path )

    self.shuffle = True
    self.normalize = normalize
    self.n_mels = n_mels
    self.conv_factor = conv_factor
    self.cur_idx = 0

  def get_batch(self, idx):
    cur_batch_size = min(self.batch_size, self.num_samples - (self.batch_size * idx) )
    batch_x = self.melspec_path[ self.batch_size * idx : self.batch_size * (idx+1) ]
    batch_x_lens = self.melspec_len[ self.batch_size * idx : self.batch_size * (idx+1) ]

    if self.is_train:
      batch_y_seq = deepcopy( self.phone_seq[ self.batch_size * idx : self.batch_size * (idx+1) ] )
      batch_y_lens = self.phone_seq_len[ self.batch_size * idx : self.batch_size * (idx+1) ]

    batch_x_melspec = np.array( 
      [self.load_melspectrogram(fp, max(batch_x_lens)) for fp in batch_x]
    )
    assert ( batch_x_melspec.shape == (cur_batch_size, max(batch_x_lens), self.n_mels) )
    
    batch_x_lens = np.ceil( np.array(batch_x_lens) / self.conv_factor ) - 2
    assert ( batch_x_lens.shape == (cur_batch_size,) )

    if self.is_train:
      batch_y_seq = np.array( self.pad_phone_seq(batch_y_seq, max(batch_y_lens)+1) )
      assert ( batch_y_seq.shape == (cur_batch_size, max(batch_y_lens)+1) )

      batch_y_lens = np.array(batch_y_lens) + 1
      assert ( batch_y_lens.shape == (cur_batch_size,) )

      inputs = {
        'melspec_input': batch_x_melspec,
        'y_label': batch_y_seq,
        'pred_len': batch_x_lens,
        'label_len': batch_y_lens
      }

      outputs = {
        'ctc_loss': np.zeros( (cur_batch_size,) )
      }

    else:
      inputs = {
        'melspec_input': batch_x_melspec,
        'pred_len': batch_x_lens,
      }
      outputs = None

    return (inputs, outputs)

  def next_batch(self):
    while True:
      assert (self.batch_size <= len(self.melspec_path))

      if self.cur_idx * self.batch_size >= self.num_samples:
        self.cur_idx = 0
        if self.shuffle:
          self.shuffle_dataset()

      batch = self.get_batch(self.cur_idx)
      self.cur_idx += 1

      yield batch

  def phone_seq_str_to_list(self, phone_seq_strs):
    return [ast.literal_eval(p_seq) for p_seq in phone_seq_strs]

  def load_melspectrogram(self, spec_file, padlen):
    # spec = pickle.load( open(spec_file, 'rb') )	
    # spec = np.array(spec)
    spec = np.load(spec_file)

    if self.normalize:
      spec = (spec - np.min(spec)) / ( np.max(spec) - np.min(spec) + 1e-12 )

    if spec.shape[0] < padlen:
      if self.normalize:
        zero_pad = np.zeros( (padlen - spec.shape[0], spec.shape[1]) )
        spec = np.vstack( (spec, zero_pad) )
      else:
        min_pad = np.full( (padlen - spec.shape[0], spec.shape[1]), np.min(spec) )
        spec = np.vstack( (spec, min_pad) )

    assert ( spec.shape == (padlen, self.n_mels) )

    return spec
  
  def pad_phone_seq(self, phone_seqs, padlen):
    for i, seq in enumerate(phone_seqs):
      phone_seqs[i].extend( [0 for x in range(padlen - len(seq))] )

    return phone_seqs

  def shuffle_dataset(self):
    self.melspec_path, self.melspec_len, self.phone_seq, self.phone_seq_len = \
      shuffle(self.melspec_path, self.melspec_len, self.phone_seq, self.phone_seq_len)