result = './result.txt'
label = './data/test_lbl.txt'

res = open(result, 'r')
lbl = open(label, 'r')

line_cnt = 0
correct = 0

try:
    res_list = res.readlines()
    lbl_list = lbl.readlines()

finally:
    res.close()
    lbl.close()

res_list[:] = [line.split() for line in res_list]
lbl_list[:] = [line.rstrip('\n') for line in lbl_list]

for line in lbl_list:
    if line == res_list[line_cnt][0]:
        correct += 1
    line_cnt += 1

print("Accuracy: {}".format(correct / line_cnt))