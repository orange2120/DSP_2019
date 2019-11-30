#!/bin/bash

ngram-count ‒text corpus_sep.txt ‒write bigram.count ‒order 2
ngram-count ‒read bigram.count ‒lm bigram.lm ‒order 2 -unk