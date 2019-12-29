import sys, os, pickle
import linecache
import phone_tokenizer as pt

TOKENIZER_PKL_PATH = './pickle/phone_tokenizer.pkl'
IDX_OUTPUT_DIR = './output/'

phoneme_line = 3


def main():
    
    if len(sys.argv) != 1:
        IDX_OUTPUT_DIR = sys.argv[2]

    with open(TOKENIZER_PKL_PATH, 'rb') as p:
        ptk = pickle.load(p)
    p.close()

    fp = open(sys.argv[1], "r")
    fnameline = fp.readline()

    while fnameline:
        # print(fnameline)
        fnameline = fnameline.rstrip() # remove '\n'

        seq_list = []
        seq_list.append(linecache.getline(fnameline, phoneme_line))
        # print(seq_list)
        output = ptk.text_to_seqs(seq_list)
        print(os.path.basename(fnameline))
        pickle.dump(output, open(IDX_OUTPUT_DIR + '/'  + os.path.basename(fnameline) + '.pkl', 'wb'))

        fnameline = fp.readline()
    
    fp.close()

if __name__ == "__main__":
    main()
