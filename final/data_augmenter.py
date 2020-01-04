import os, pickle, random, sys
import numpy as np
import pandas as pd
from math import ceil
sys.path.append('./waveproc/')

from wav_to_melspec_aug import plot_wav, plot_melspec, read_wav, dump_wav
from wav_to_melspec_aug import preemphasis, wav_to_melspec
from wav_to_melspec_aug import freq_change, speed_change, add_noise

class DataAugmenter(object):
  def __init__(self, wav_dir, phone_dir, wav_output_dir, melspec_output_dir, info_save_dir, wav_sr=16000, n_samples=None, aug_per_wav=4, sortagrad=True):
    self.wav_sr = wav_sr
    self.wav_dir = wav_dir
    self.phone_dir = phone_dir
    self.wav_output_dir = wav_output_dir
    self.melspec_output_dir = melspec_output_dir
    self.aug_per_wav = aug_per_wav
    self.n_samples = n_samples
    self.sortagrad = sortagrad
    self.info_save_dir = info_save_dir

    self.wav_files = self._get_wav_files()
    self.phone_seqs, self.phone_seq_lens = self._get_phones()

    self.melspec_len = []
    self.melspec_files = []

    self.aug_choices = [x for x in range(1, 8)]
    self.conv_factor = 8

  def _get_wav_files(self):
    wav_files = sorted(
      [s for s in os.listdir( self.wav_dir ) if s.endswith('.wav')]
    )

    if self.n_samples:
      wav_files = wav_files[:self.n_samples]

    return wav_files

  def _get_phones(self):
    phone_files = sorted(os.listdir( self.phone_dir ))

    if self.n_samples:
      phone_files = phone_files[:self.n_samples]

    for i in range( len(phone_files) ):
      # print (i, self.wav_files[i], phone_files[i])
      assert ( self.wav_files[i].split('.')[0] == phone_files[i].split('.')[0] )

    phone_seqs, phone_seq_lens = [], []
    for f in phone_files:
      ph_seq = pickle.load(open(os.path.join(self.phone_dir, f), 'rb'))
      phone_seqs.extend( self.aug_per_wav * [ph_seq] )
      phone_seq_lens.extend( self.aug_per_wav * [len(ph_seq)] )

    assert ( len(phone_seq_lens) == len(phone_seqs) )
    print ('total samples:', len(phone_seqs))

    return phone_seqs, phone_seq_lens

  def _dump_wav_melspec_pair(self, wav_file, melspec_file, wav, melspec):
    dump_wav(wav_file, wav, self.wav_sr)
    np.save(melspec_file, melspec)

    return

  def _augment_single(self, wav, label_len, aug_speed, aug_freq, aug_noise):
    speed, freq_step, noise_lev = None, None, None
    suffix = ''
    
    if aug_speed:
      is_legal = False
      while not is_legal:
        speed = random.uniform(0.8, 1.2)
        if ceil(wav.shape[0] / (speed * 160 * self.conv_factor)) - 2 > label_len:
          is_legal = True

      wav = speed_change(wav, speed)
      suffix += '_sp_{:.2f}'.format(speed)

    if aug_freq:
      is_legal = False
      while not is_legal:
        freq_step = random.randint(-5, 5)
        if freq_step:
          is_legal = True

      wav = freq_change(wav, freq_step, self.wav_sr)
      suffix += '_freq_{}'.format(freq_step)

    if aug_noise:
      noise_lev = random.uniform(0.02, 0.1)
      wav = add_noise(wav, noise_lev)
      suffix += '_noise_{:.2f}'.format(noise_lev)

    melspec = wav_to_melspec(wav, self.wav_sr, int(self.wav_sr * 25 / 1000), int(self.wav_sr * 10 / 1000))
    melspec_len = melspec.shape[0]
    print (' -- augmented: speed={}, freq={}, noise={}'.format(speed, freq_step, noise_lev))

    return wav, melspec, melspec_len, suffix

  def augmentation(self):
    if not os.path.exists( self.wav_output_dir ):
      os.mkdir( self.wav_output_dir )
    if not os.path.exists( self.melspec_output_dir ):
      os.mkdir( self.melspec_output_dir )

    window_len = int(self.wav_sr * 25 / 1000)
    hop_len = int(self.wav_sr * 10 / 1000)

    print (window_len, hop_len)

    for idx, wav_file in enumerate(self.wav_files):
      print ('processing wav #{}'.format(idx))

      wav = read_wav( os.path.join(self.wav_dir, wav_file), self.wav_sr )
      wav = preemphasis(wav)

      base_melspec_path = wav_file.replace('.wav', '.spec')
      base_melspec = wav_to_melspec(wav, self.wav_sr, window_len, hop_len)
      
      self._dump_wav_melspec_pair(
        os.path.join(self.wav_output_dir, wav_file),
        os.path.join(self.melspec_output_dir, base_melspec_path), 
        wav, base_melspec
      )

      self.melspec_files.append( os.path.join(self.melspec_output_dir, base_melspec_path) + '.npy' )
      self.melspec_len.append( base_melspec.shape[0] )

      # if idx < 5:
      #   plot_wav(wav, self.wav_sr, show=True)
      #   plot_melspec(base_melspec, self.wav_sr, hop_len, transposed=True, show=True)

      aug_opts = random.sample(self.aug_choices, self.aug_per_wav - 1)
      sample_label_len = self.phone_seq_lens[idx] + 1
      for opt in aug_opts:
        speed, freq, noise = (opt >> 2), (opt >> 1) % 2, (opt % 2)
        print (speed, freq, noise)
        
        aug_wav, aug_melspec, aug_melspec_len, aug_filename = self._augment_single(wav, sample_label_len, speed, freq, noise)

        aug_melspec_file = base_melspec_path.split('.spec')[0] + aug_filename + '.spec'
        aug_wav_file = wav_file.split('.wav')[0] + aug_filename + '.wav'
        self.melspec_files.append( os.path.join(self.melspec_output_dir, aug_melspec_file) + '.npy' )
        self.melspec_len.append( aug_melspec_len )

        self._dump_wav_melspec_pair(
          os.path.join(self.wav_output_dir, aug_wav_file),
          os.path.join(self.melspec_output_dir, aug_melspec_file), 
          aug_wav, aug_melspec
        )

        # if idx < 5:
        #   plot_wav(aug_wav, self.wav_sr, show=True)
        #   plot_melspec(aug_melspec, self.wav_sr, hop_len, transposed=True, show=True)

    return

  def dump_data_info(self):
    df = pd.DataFrame()

    df['melspec_path'] = self.melspec_files
    df['melspec_len'] = self.melspec_len
    df['phone_seq'] = self.phone_seqs
    df['phone_seq_len'] = self.phone_seq_lens

    print( df.head(30) )
    print( df.info() )

    if self.sortagrad:
      df = df.sort_values(by='melspec_len', ascending=True)

    df.to_csv(os.path.join(self.info_save_dir, 'data_info.csv'), index=False, encoding='utf-8')

    return


if __name__ == '__main__':
  aug = DataAugmenter(
    './data_thchs30/train/',
    './data/dataset_train/phoneme',
    './data/dataset_train_aug/wav',
    './data/dataset_train_aug/melspec',
    './data/dataset_train_aug/',
    n_samples=None,
  )

  aug.augmentation()
  aug.dump_data_info()
