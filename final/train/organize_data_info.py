import pandas as pd
import numpy as np
import pickle, os
from sklearn.model_selection import train_test_split

def build_dataset_df(spectrogram_dir, phone_seqs_dir, sortagrad=True, save=False, save_dir=None, is_train=True, train_val_split=False, val_size=None):
  df_final = pd.DataFrame()

  spec_files = os.listdir(spectrogram_dir)
  spec_files = sorted(spec_files)
  print (spec_files[:10])

  if is_train:
    phone_files = os.listdir(phone_seqs_dir)
    assert ( len(spec_files) == len(phone_files) )
    phone_files = sorted(phone_files)
    print (phone_files[:10])

    for i in range( len(spec_files) ):
      print (spec_files[i].split('.spec')[0], phone_files[i].split('.phone')[0])
      assert ( spec_files[i].split('.spec')[0] == phone_files[i].split('.phone')[0] )

  spec_files = [spectrogram_dir + '/' + spec_fp for spec_fp in spec_files]
  if is_train:
    phone_files = [phone_seqs_dir + '/' + phone_fp for phone_fp in phone_files]
    assert ( len(spec_files) == len(phone_files) )

    phone_seqs = []
    for phone_fp in phone_files:
      phone_seqs.append( pickle.load( open(phone_fp, 'rb') ) )
    assert ( len(spec_files) == len(phone_seqs) )

    df_final['phone_seq'] = phone_seqs

  df_final['melspec_path'] = spec_files
  melspec_lens = []
  for melspec in spec_files:
    melspec_lens.append( np.load(melspec).shape[0] )
  df_final['melspec_len'] = melspec_lens

  if is_train:
    phone_seq_lens = []
    for seq in phone_seqs:
      phone_seq_lens.append( len(seq) )
    df_final['phone_seq_len'] = phone_seq_lens

  print( df_final.head(30) )
  print( df_final.info() )

  if save:
    if not train_val_split:
      if sortagrad:
        df_final = df_final.sort_values(by='melspec_len', ascending=True)

      if is_train:
        df_final.to_csv(save_dir + 'data_info.csv', index=False, encoding='utf-8')
      else:
        df_final.to_csv(save_dir + 'data_info_test.csv', index=False, encoding='utf-8')

    else:
      assert ( val_size is not None )
      df_train, df_val = train_test_split(df_final, random_state=42, test_size=val_size)
      print (df_train.info(), df_val.info())

      if sortagrad:
        df_train = df_train.sort_values(by='melspec_len', ascending=True)
        df_val = df_val.sort_values(by='melspec_len', ascending=True)

      df_train.to_csv(save_dir + 'data_info_train.csv', index=False, encoding='utf-8')
      df_val.to_csv(save_dir + 'data_info_val.csv', index=False, encoding='utf-8')

  return

if __name__ == '__main__':
  # build_dataset_df(
  #   '../../dataset_train/spectrogram', 
  #   '../../dataset_train/phoneme/', 
  #   save=True, save_dir='../../dataset_train/',
  #   train_val_split=False
  # )

  # build_dataset_df(
  #   '../../dataset_dev/spectrogram', 
  #   '../../dataset_dev/phoneme/', 
  #   save=True, save_dir='../../dataset_dev/',
  #   train_val_split=False
  # )

  build_dataset_df(
    '../data/speech_data/YNC/melspec_seg10db', 
    #'../data/speech_data/L.S._Lee/melspec_seg', 
    None, 
    save=True, save_dir='../data/speech_data/YNC/',
    #save=True, save_dir='../data/speech_data/L.S._Lee/',
    is_train=False,
    train_val_split=False
  )
