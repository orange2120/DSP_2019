import os, sys
import matplotlib.pyplot as plt
import numpy as np
import librosa, librosa.display

mels_dir = './data/speech_data/L.S._Lee/eval'
mels_file = [s for s in os.listdir( mels_dir ) if s.endswith('.npy')]

print (mels_file)

for mf in mels_file:
    melspec = np.load( os.path.join(mels_dir, mf) )
    print (melspec.shape)
    librosa.display.specshow(melspec, sr=32000, x_axis='ms', y_axis='mel')
    plt.show()