#!/bin/bash

for i in $(seq 1 10);
do
	echo $i;
	perl ./separator_big5.pl ./test_data/"$i".txt > ./test_data/"$i"_sep.txt;
done
