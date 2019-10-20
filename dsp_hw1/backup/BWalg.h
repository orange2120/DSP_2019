#ifndef __BWalg_h__
#define __BWalg_h__

#include "hmm.h"

#define TRAIN_SIZE 10000

void forward_alg(HMM *, double **);
void backward_alg(HMM *, double **);

struct BWalg
{
    double alpha[MAX_OBSERV][MAX_STATE] = {0.0};
    double beta[MAX_STATE] = {1.0};
    char train_data[TRAIN_SIZE][MAX_LINE];
    char q[] = {'A', 'B', 'C', 'D', 'E', 'F'}; // state number sequence
};

#endif