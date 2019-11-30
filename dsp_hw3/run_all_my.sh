#!/bin/bash

for i in $(seq 1 1 10);
do
    echo Testing $i ...;
    ./mydisambig ./test_data/"$i"_sep.txt ZhuYin-Big5.map bigram.lm ./output/"$i"_dec.txt;
done