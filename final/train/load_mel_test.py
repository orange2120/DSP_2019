import os, sys
import numpy as np
# from os import listdir

spec_files = sys.argv[1]

fp = open(spec_files, "r")
fnameline = fp.readline()
fnameline = fp.readline()

while fnameline:
    fnameline = fnameline.split(',', 1)[0]
    spec = np.load(fnameline)

    print(spec.shape)
    fnameline = fp.readline()
    
fp.close()
