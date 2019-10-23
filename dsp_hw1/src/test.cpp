/****************************************************************************
  FileName     [ test.cpp ]
  Synopsis     [ test data and output HMM model ]
  Author       [ Orange Hsu ]
  Copyright    [ Copyleft(c) 2019-present , NTU, Taiwan ]
****************************************************************************/
#include <iostream>
#include "hmm.h"
#include "viterbi.h"
using namespace std;

int main(int argc, char *argv[])
{
    if (argc != 4)
    {
        perror("[ERROR] Invalid parameters!\n");
        exit(-1);
    }
    
    Viterbi vt;
    FILE *model_fp = open_or_die(argv[3], "w");

    vt.load_models(argv[1]);

    //vt.;
}