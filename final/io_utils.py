import pickle
import pandas as pd

def read_data_df(csv_path, train=True):
  df = pd.read_csv(csv_path, encoding='utf-8')

  if not train:
    df = df[ ['melspec_path', 'melspec_len'] ]

  print (df.info())
  print (df.head())

  return df

def load_phone_tokenizer(tkn_path):
  tkn = pickle.load( open(tkn_path, 'rb') )
  print ('tokenizer dict size:', tkn.dict_size)
  return tkn