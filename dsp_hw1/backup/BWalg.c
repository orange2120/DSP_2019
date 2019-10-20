#include "BWalg.h"
#include "hmm.h"

// T : observ_num
// calculate forward matrix : alpha
void forward_alg(HMM *hmm ,double **alpha)
{
    for(uint8_t i = 0; i < hmm->state_num; ++i)
        alpha[0][i] = hmm->initial[i] * (hmm->observation[i][0]);

    for(uint8_t i = 0; i < hmm->observ_num; ++i)
        for(int j = 0; j < hmm->state_num)
        alpha[j] = hmm->transition[][i];
}