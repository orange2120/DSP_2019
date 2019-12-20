# Final Project

`seq_file_tok.py`: convert phoneme sequence to index sequence
`wav_to_melspec.py`: convert wav file to melspectrogram
`gen_dataset.py`: generate trainnig dataset

```bash
$ python3 seq_file_tok.py <filename list path> <output directory path>
$ python3 wav_to_melspec.py <wav path> <output directory path>
$ python3 gen_dataset.py <number of dataset> <source directory path> <phoneme secquence dir path> <melspectrogram dir path> <output dir path> # Create a 100 dataset in dir ./ : 100 ./data_thchs30/data ./ 
```