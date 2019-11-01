iters = [1, 2, 5, 10, 20, 50, 75, 100, 125, 150, 200, 300, 400, 500, 800, 1000]

result_path = './output/'
label = './data/test_lbl.txt'
acc_path = './output/accu.txt'

lbl = open(label, 'r')
acc = open(acc_path, 'w')

try:
    lbl_list = lbl.readlines()

finally:
    lbl.close()

lbl_list[:] = [line.rstrip('\n') for line in lbl_list]

for k in iters:
    res = open(result_path + 'result_' + str(k) + '.txt', 'r')

    line_cnt = 0
    correct = 0

    try:
        res_list = res.readlines()

    finally:
        res.close()

    res_list[:] = [line.split() for line in res_list]

    for line in lbl_list:
        if line == res_list[line_cnt][0]:
            correct += 1
        line_cnt += 1

    acc.write(str(k) + ',' + str(correct / line_cnt) + '\n')
    print("Accuracy: {}".format(correct / line_cnt))
