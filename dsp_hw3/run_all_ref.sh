#!/bin/bash

for i in $(seq 1 1 10);
do
    echo Testing $i ...;
    disambig -text ./test_data/"$i"_sep.txt -map ZhuYin-Big5.map -lm bigram.lm -order 2 >./output/"$i"_dec_ref.txt;
done

echo done.