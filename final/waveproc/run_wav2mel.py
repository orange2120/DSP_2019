import sys, os

OUTPUT_DIR = './'

def main():
    print(len(sys.argv))
    if len(sys.argv) != 3:
        print('[ERROR] Invalid parameter!')
        exit(-1)

    OUTPUT_DIR = sys.argv[2]

    fp = open(sys.argv[1], "r")
    fnameline = fp.readline()
    while fnameline:
        # print(fnameline)
        fnameline = fnameline.rstrip() # remove '\n'
        # print('python3 wav_to_melspec.py ' + fnameline + ' ' + OUTPUT_DIR)
        os.system('python3 wav_to_melspec.py ' + fnameline + ' ' + OUTPUT_DIR)
        fnameline = fp.readline()
    fp.close()

if __name__ == "__main__":
    main()