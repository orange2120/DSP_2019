import sys
import linecache
import phone_tokenizer as PT

phoneme_line = 3
seqs = []

def main():
    fp = open(sys.argv[1], "r")
    fnameline = fp.readline()

    while fnameline:
        # print(fnameline)
        fnameline = fnameline.rstrip() # remove '\n'
        seq = linecache.getline(fnameline, phoneme_line)
        
        seq_list = seq.split()
        # print(seq_list)
        for i in seq_list:
            
        fnameline = fp.readline()


if __name__ == "__main__":
    main()