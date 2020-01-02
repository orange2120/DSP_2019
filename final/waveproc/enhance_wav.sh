input_file=../../../speech_data/YNC/YNC2.txt
input_dir=../../../speech_data/YNC/
output_dir=../../../speech_data/YNC/10db/

for name in `cat $input_file`
do
  echo "$name"
  ffmpeg -i "$input_dir$name" -d s16le -ar 32000 -af volume=+10dB "$output_dir${name}"
done
