import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter


def plot_wav(wav, sr, show=False):
  librosa.display.waveplot(wav, sr=sr)
  if show:
    plt.show()
  return

def plot_melspec(spec, sr, hop_len, transposed=True, fmin=20, fmax=8000, show=False):
  if transposed:
    spec = spec.T
  
  librosa.display.specshow(spec, sr=sr, hop_length=hop_len, x_axis='time', y_axis='mel', fmin=fmin, fmax=fmax)
  plt.colorbar(format='%+2.0f dB')

  if show:
    plt.show()

  return

def read_wav(wav_path, sr, duration=None, mono=True):
  wav, sr = librosa.load(wav_path, sr=sr, duration=duration, mono=mono)
  return wav

def preemphasis(wav, alpha=0.97):
  return lfilter([1, -alpha], [1], wav)

def wav_to_melspec(wav, sr, window_len, hop_len, fmin=20, fmax=8000, n_mels=128, transpose=True):
  spec = librosa.feature.melspectrogram(
    y=wav, sr=sr, n_fft=window_len, hop_length=hop_len, center=False, fmin=fmin, fmax=fmax, n_mels=n_mels,
  )

  if transpose:
    spec = spec.T

  return librosa.power_to_db(spec, ref=np.max)



TEST_WAV_PATH = './data_thchs30/data/A2_7.wav'
SR = 16000

''' Example on how to produce Mel-spectrogram(dB) from a .wav file '''
if __name__ == '__main__':
  y = read_wav(TEST_WAV_PATH, SR)
  print (y.shape)

  plot_wav(y, SR, show=True)
  y = preemphasis(y)

  #  window_len: 25 ms, hop_len: 10ms 
  #  Transpose to make dimension -- (timesteps, mels) 
  y_melspec = wav_to_melspec(y, SR, 400, 160, fmin=20, fmax=8000, transpose=True)
  print (y_melspec.shape)

  plot_melspec(y_melspec, SR, 160, transposed=True, show=True)
