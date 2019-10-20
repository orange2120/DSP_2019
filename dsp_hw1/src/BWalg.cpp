#include "BWalg.h"
#include "hmm.h"

BWalg::BWalg(HMM &h)
{
    hmm = &h;
    for (int i = 0; i < TRAIN_SIZE; ++i)
        memset(train_data[i], '\0', sizeof(char)*MAX_LINE);
}
BWalg::BWalg(/* args */)
{
}

BWalg::~BWalg()
{
}

void BWalg::train(int iters)
{
    // go through iterations
    for (int i = 0; i < iters; ++i)
    {
        // go through over all the trainning data
        for (int k = 0; k < train_lines; ++k)
        {
        
            forward_alg(k);
            backward_alg(k);
            get_gamma(k);
            get_epsilon(k);
        }
    }
}

// Forward algorithm : calculate forward matrix alpha_t = P(o1, o2...o_t, qt = h | lambda)
void BWalg::forward_alg(const int &line)
{
    double sum[MAX_STATE] = {0.0};

    // initialize
    for (int i = 0; i < hmm->state_num; ++i)
        alpha[0][i] = hmm->initial[i] * hmm->observation[i][states[train_data[line][0]]];
    
    // induction
    for (int t = 1; t < train_len; ++t)
    {
        for (int j = 0; j < hmm->state_num; ++j)
        {
            // alpha_t(i) * a_ij
            for (int i = 0; i < hmm->state_num; ++i)
                sum[i] += alpha[t - 1][i] * hmm->transition[i][j];
            // sum dot b_j(o_t+1)
            alpha[t][j] = hmm->observation[j][train_data[line][t] - 'A'] * sum[j];
        }
    }
}

void BWalg::backward_alg(const int &line)
{
    //double sum[] = 0;
    // initialize
    for (int i = 0; i < hmm->state_num; ++i)
        beta[0][i] = 1.0;

    // induction
    for (int t = train_len - 2; t >= 0; --t)
    {
        for (int i = 0; i < hmm->state_num; ++i)
        {
            for (int j = 0; j < hmm->state_num; ++j)
                beta[t][i] =  beta[j][t + 1] * hmm->observation[t][train_data[line][t] - 'A'] * hmm->transition[i][j];
                //             beta_t+1(j)        b_j(o_t+1)                                        a_ij                
        }
    }
}

void BWalg::get_gamma()
{
    double sum_gamma[MAX_STATE][MAX_SEQ] = {0.0};
    for (int t = 0; t < train_len; ++t)
    {
        for (int i = 0; i < hmm->state_num; ++i)
            sum_gamma[i][t] = alpha[t][i] * beta[t][i];
    }
    for (int t = 0; t < train_len; ++t)
    {
        for (int i = 0; i < hmm->state_num; ++i)
            sum_gamma[i][t] = alpha[t][i] * beta[t][i];

        for (int i = 0; i < hmm->state_num; ++i)
            gamma[i][t] = alpha[t][i] * beta[t][i] / sum_gamma[i][t];
    }
}

void BWalg::get_epsilon()
{


}

// Load the observation sequence file (o1, o2...)
void BWalg::load_train(const char *filename)
{
    FILE *fp = open_or_die(filename, "r");

    char token[MAX_LINE] = "";
    
    while(fscanf(fp, "%s", token) != EOF)
    {
        strcpy(train_data[train_lines], token);
        train_lines++;
    }
    train_len = strlen(token);

    fclose(fp);
}

void BWalg::dump_td() const
{
    for(int i = 0 ;i < TRAIN_SIZE; ++i)
        printf("%s\n", train_data[i]);
}