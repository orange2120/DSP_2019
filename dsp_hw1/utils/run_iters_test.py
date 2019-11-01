import os
import sys
import subprocess

iters = [1, 2, 5, 10, 20, 50, 75, 100, 125, 150, 200, 300, 400, 500, 800, 1000]

test_path = './test'
model_list_path = './output/'
test_seq_path = './data/test_seq.txt'
result_path = './output/'

for k in iters:
    subprocess.call([test_path, model_list_path + 'modellist_' + str(k) + '.txt', test_seq_path, result_path + 'result_' + str(k) + '.txt'])
