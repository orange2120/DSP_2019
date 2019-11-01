import os
import sys
import subprocess

train_path = './train'
iters = [1, 2, 5, 10, 20, 50, 75, 100, 125, 150, 200, 300, 400, 500, 800, 1000]
model_init_path = './model_init.txt'
seq_path = './data/'
output_model_path = './'
model_list_path = './output/'

if len(sys.argv) > 2:
    print("[ERROR] Invalid parameters!")
    exit(-1)

for k in iters:
    fp = open(model_list_path + 'modellist_' + str(k) + '.txt', 'w')
    for i in range(1,6):
        #print('\nRunning seq ' + str(i))
        #subprocess.call([train_path, str(iters), model_init_path, seq_path + 
        #'train_seq_0' + str(i) + '.txt', output_model_path + str(k) + '_model_0' + str(i) + '.txt'])
        fp.write(str(k) + '_model_0' + str(i) + '.txt\n')

