#!/bin/bash

for i in $(seq 330 660 9900);
do
    bash 3-train-arg.sh $i;
    bash 4-test.sh | grep accuracy > td/gauss_test_$i.txt;
done
