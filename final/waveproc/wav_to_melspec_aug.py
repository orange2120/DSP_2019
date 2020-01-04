import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter
import soundfile

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

def dump_wav(wav_path, wav, sr, format='wav', subtype='PCM_16'):
  soundfile.write(wav_path, wav, sr, format=format, subtype=subtype)

def trim_wav(wav, top_db=60):
  wav, interv = librosa.effects.trim(wav, top_db=top_db)
  return wav

def speed_change(wav, rate):
  wav = librosa.effects.time_stretch(wav, rate)
  scale = max( np.max(wav), abs(np.min(wav)) )
  return wav / scale

def freq_change(wav, steps, sr):
  wav = librosa.effects.pitch_shift(wav, sr, steps)
  scale =  max( np.max(wav), abs(np.min(wav)) )
  return wav / scale

def calc_rms_amplitude(wav):
  energies = np.square(wav)
  rms_amp = np.sqrt( np.sum(energies) / wav.shape[0] )

  return rms_amp

def add_noise(wav, level):
  gauss_scale = level * calc_rms_amplitude(wav)
  # print (gauss_scale)
  noise = np.random.normal(size=wav.shape, scale=gauss_scale)
  # print (noise)
  new_wav = wav + noise

  scale =  max( np.max(wav), abs(np.min(wav)) )
  return new_wav / scale

def preemphasis(wav, alpha=0.97):
  return lfilter([1, -alpha], [1], wav)

def wav_to_melspec(wav, sr, window_len, hop_len, fmin=20, fmax=8000, n_mels=128, transpose=True):
  spec = librosa.feature.melspectrogram(
    y=wav, sr=sr, n_fft=window_len, hop_length=hop_len, center=False, fmin=fmin, fmax=fmax, n_mels=n_mels,
  )

  if transpose:
    spec = spec.T

  return librosa.power_to_db(spec, ref=np.max)



TEST_WAV_PATH = './data_thchs30/data/A8_44.wav'
SR = 16000

''' Example on how to produce Mel-spectrogram(dB) from a .wav file '''
if __name__ == '__main__':
  y = read_wav(TEST_WAV_PATH, SR)
  print (y.shape)

  dump_wav('aug_test/ori.wav', y, SR)
  plot_wav(y, SR, show=True)
  
  y = preemphasis(y)
  dump_wav('aug_test/preemph.wav', y, SR)

  y = add_noise(y, 0.12)
  plot_wav(y, SR, show=True)
  dump_wav('aug_test/preemph_noise.wav', y, SR)
  
  y = speed_change(y, 1.2)
  dump_wav('aug_test/pre_sp.wav', y, SR)
  
  y = freq_change(y, 3, SR)
  dump_wav('aug_test/pre_sp_freq.wav', y, SR)
  
  print (y.shape)
  plot_wav(y, SR, show=True)

  #  window_len: 25 ms, hop_len: 10ms 
  #  Transpose to make dimension -- (timesteps, mels) 
  # y_melspec = wav_to_melspec(y, SR, 400, 160, fmin=20, fmax=8000, transpose=True)
  # print (y_melspec.shape)

  # plot_melspec(y_melspec, SR, 160, transposed=True, show=True)
