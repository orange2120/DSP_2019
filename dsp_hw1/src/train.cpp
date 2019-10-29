/****************************************************************************
  FileName     [ train.cpp ]
  Synopsis     [ training data and output HMM model ]
  Author       [ Orange Hsu ]
  Copyright    [ Copyleft(c) 2019-present , NTU, Taiwan ]
****************************************************************************/
#include <iostream>
#include "hmm.h"
#include "BWalg.h"
using namespace std;

int main(int argc, char *argv[])
{
    if (argc != 5)
    {
        perror("[ERROR] Invalid parameters!\n");
        exit(-1);
    }

    int iterations = 0;

    HMM hmm;
    BWalg bw(hmm);
    FILE *model_fp = open_or_die(argv[4], "w");

    iterations = atoi(argv[1]);
    printf("Train iterations: %d\n", iterations);

    loadHMM(&hmm, argv[2]);        // load models
    bw.load_train(argv[3]);        // load trainning data

    bw.train(iterations);

    dumpHMM(model_fp, &hmm); // dump trained model to file
}