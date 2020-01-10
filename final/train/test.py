import os, sys, pickle, time
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
sys.path.append('../')

import numpy as np
import pandas as pd
import keras.backend as K
from math import ceil

from io_utils import read_data_df, load_phone_tokenizer
from score_utils import create_decode_fctn
from model import ds2_model
from batch_generator import BatchGenerator

def predict(test_df, batch_size, model, decode_fctn, phone_tokenizer):
  test_generator = BatchGenerator(test_df, is_train=False, shuffle=False, batch_size=batch_size)
  n_batches = ceil(test_generator.num_samples / batch_size)

  entries_name = [
    s.split('/')[-1].split('.spec')[0] \
      for s in test_df['melspec_path'].tolist()
  ]
  #print (entries_name)

  decoded_phone_seqs = []
  for b in range(n_batches):
    print ('decoding batch #{} ...'.format(b+1))
    batch, _ = test_generator.get_batch(b)
    decoded_seqs = decode_fctn(
      [ batch['melspec_input'], batch['pred_len'] ]
    )[0]
    decoded_batch_phone_seqs = phone_tokenizer.seqs_to_text( decoded_seqs.tolist() )
    
    print (decoded_batch_phone_seqs)

    decoded_phone_seqs.extend( decoded_batch_phone_seqs )

  assert ( len(decoded_phone_seqs) == test_generator.num_samples )

  return decoded_phone_seqs, entries_name

def dump_predictions(output_dir, phone_seqs, entries_name):
  if not os.path.exists(output_dir):
    os.mkdir(output_dir)

  for idx, seq in enumerate(phone_seqs):
    output_fname = output_dir + entries_name[idx] + '.phone.trn.txt'
    with open(output_fname, 'w') as f:
      f.write(seq)
  
  return

if __name__ == '__main__':
  test_df = read_data_df( sys.argv[1], train=False )
  phone_tokenizer = load_phone_tokenizer( sys.argv[2] )
  model_weights_path = sys.argv[3]
  output_dir = sys.argv[4]
  test_batch_size = int(sys.argv[5])

  model = ds2_model(phone_tokenizer.dict_size + 2)
  model.load_weights( model_weights_path )

  decode_fctn= create_decode_fctn(model)

  pred_phone_seqs, entries_name = predict(test_df, test_batch_size, model, decode_fctn, phone_tokenizer)

  print('pred phone seq')
  print (len(pred_phone_seqs))
  print (pred_phone_seqs[:10])

  dump_predictions(output_dir, pred_phone_seqs, entries_name)
