import pickle, os
import linecache
import numpy as np
import matplotlib.pyplot as plt
from wav_to_melspec import read_wav, preemphasis, wav_to_melspec
from wav_to_melspec import plot_wav, plot_melspec

# TOKENIZER_PATH = './pickles/phone_tokenizer.pkl'
TRAIN_DATA_DIR = '../../../speech_data/YNC/seg10db/'
# PHONE_IDX_SEQS_PATH = './tiny_4096/phone_seq/phone_seqs.pkl'
MELSPEC_OUTPUT_DIR = '../../../speech_data/YNC/melspec_10db/'

SR = 32000
# NUM_SAMPLES = 4096
# PHONEME_LINE = 3

if not os.path.exists(MELSPEC_OUTPUT_DIR):
  os.mkdir(MELSPEC_OUTPUT_DIR)

entries = os.listdir( TRAIN_DATA_DIR )
print ( len(entries) )

# entries = entries[:NUM_SAMPLES * 2]
entries_wav = [ s for s in entries if s.endswith('.wav') ]
print ( len(entries_wav) )
entries_trn = [ s for s in entries if s.endswith('.trn') ]

# for i in range(NUM_SAMPLES):
#   assert ( entries_wav[i].split('.wav')[0] == entries_trn[i].split('.wav')[0] )

# ptk = pickle.load( open(TOKENIZER_PATH, 'rb') )
# print (ptk.dict_size)

# phone_seqs = []
# for i in range( len(entries_wav) ):
#   print ('processing phone seq #{}'.format(i))
#   phone_seq_i = linecache.getline(TRAIN_DATA_DIR + entries_trn[i], PHONEME_LINE).rstrip('\n')
#   phone_seqs.append( phone_seq_i )

# print ( len(phone_seqs) )

# phone_token_seqs = ptk.text_to_seqs( phone_seqs )
# print ( len(phone_token_seqs) )

# pickle.dump(phone_token_seqs, open(PHONE_IDX_SEQS_PATH, 'wb'))

spec_lens = []
for i in range( len(entries_wav) ):
  print ('processing mel spec #{}'.format(i))
  wav_path = TRAIN_DATA_DIR + entries_wav[i]

  wav = read_wav(wav_path, SR)
  wav = preemphasis(wav)
  melspec = wav_to_melspec(wav, SR, 800, 320, fmin=20, fmax=8000, transpose=True)

  if i < 10:
    plot_wav(wav, SR, show=True)
    plot_melspec(melspec, SR, 320, transposed=True, show=True)

  spec_lens.append( melspec.shape[0] )
  spec_filepath = MELSPEC_OUTPUT_DIR + entries_wav[i].split('.wav')[0] + '.spec'
  np.save(spec_filepath, melspec)

plt.hist(spec_lens)
plt.show()