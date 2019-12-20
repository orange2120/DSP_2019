import sys,os
from shutil import copyfile

def main():
    print(sys.argv)
    if len(sys.argv) != 6:
        print('Invalid parameter')
        exit(-1)
    
    DATASET_NUM = int(sys.argv[1])
    SRC_DIR_PATH = sys.argv[2]
    PHOME_DIR_PATH = sys.argv[3]
    MSG_DIR_PATH = sys.argv[4]
    OUT_DIR_PATH = sys.argv[5] + 'dataset_' + sys.argv[1]

    if not os.path.isdir(OUT_DIR_PATH):
        os.mkdir(OUT_DIR_PATH)
        os.mkdir(OUT_DIR_PATH + '/wav/')
        os.mkdir(OUT_DIR_PATH + '/phoneme/')
        os.mkdir(OUT_DIR_PATH + '/spectrogram/')

    fileList = os.listdir(SRC_DIR_PATH)
    wavList = []
    phonemeList = os.listdir(PHOME_DIR_PATH)
    msgList = os.listdir(MSG_DIR_PATH)

    # print(len(fileList))

    for i in fileList:
        if i.endswith('.wav'):
            wavList.append(i)

    if DATASET_NUM > len(wavList):
        DATASET_NUM = len(wavList)

    print(DATASET_NUM)
    # print(len(wavList))
    # print(wavList)
    # print(len(phonemeList))
    # print(phonemeList)
    # print(len(msgList))

    for i in range(0, DATASET_NUM):
        # print(OUT_DIR_PATH + '/wav/' +  wavList[i])
        # copyfile(SRC_DIR_PATH + '/' + wavList[i], OUT_DIR_PATH + '/wav/' +  wavList[i])
        copyfile(PHOME_DIR_PATH + '/'  + phonemeList[i], OUT_DIR_PATH + '/phoneme/' + phonemeList[i])
        copyfile(MSG_DIR_PATH + '/' + msgList[i], OUT_DIR_PATH + '/spectrogram/' + msgList[i])

if __name__ == "__main__":
    main()