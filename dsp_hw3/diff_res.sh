#!/bin/bash

for i in $(seq 1 1 10);
do
    echo Running diff on $i ...;
    diff output/"$i"_dec.txt output/"$i"_dec_ref.txt
done

echo done.