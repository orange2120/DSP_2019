input_file=../data/speech_data/YNC/YNC_new.txt
input_dir=../data/speech_data/YNC/
output_dir=../data/speech_data/YNC/10db/

for name in `cat $input_file`
do
  echo "$name"
  ffmpeg -i "$input_dir$name" -d s16le -ar 32000 -af volume=+10dB "$output_dir${name}"
done
