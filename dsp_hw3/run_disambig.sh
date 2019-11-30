#!/bin/bash

disambig -text $1 -map ZhuYin-Big5.map -lm bigram.lm -order 2 > $1_dis.txt