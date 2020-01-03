filename=../data/speech_data/YNC/YNC2.txt
filename_prefix=../data/speech_data/YNC/10db/
output_dir=../data/speech_data/YNC/seg10db/

for WORD in `cat $filename`
do
    echo $WORD
    # echo $(filename_prefix)
    path=$filename_prefix$WORD
    python3 ../vad.py 2 $path $output_dir 5 15
done