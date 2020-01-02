filename=../../../speech_data/YNC/YNC2.txt
filename_prefix=../../../speech_data/YNC/10db/
output_dir=../../../speech_data/YNC/seg10db

for WORD in `cat $filename`
do
    echo $WORD
    # echo $(filename_prefix)
    path=$filename_prefix$WORD
    python3 vad.py 3 $path $output_dir 3 15
done