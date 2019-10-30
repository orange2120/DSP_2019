import os
import sys
import subprocess

train_path = './train'
iters = 100
model_init_path = './model_init.txt'
seq_path = './data/'
output_model_path = './'

if len(sys.argv) > 2:
    print("[ERROR] Invalid parameters!")
    exit(-1)

if len(sys.argv) == 2:
    iters = int(sys.argv[1])

for i in range(1,6):
    print('\nRunning seq ' + str(i))
    subprocess.call([train_path, str(iters), model_init_path, seq_path + 'train_seq_0' + str(i) + '.txt', output_model_path + 'model_0' + str(i) + '.txt'])
