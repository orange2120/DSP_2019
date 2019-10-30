#include "BWalg.h"
#include <iomanip>

BWalg::BWalg(HMM &h) : hmm(&h)
{
    //hmm = &h;
    for (int i = 0; i < TRAIN_SIZE; ++i)
        memset(_train_data[i], '\0', sizeof(char) * MAX_LINE);
    reset_var();
}

BWalg::BWalg(/* args */)
{
}

BWalg::~BWalg()
{
}

// Trainning process
void BWalg::train(int iters)
{
    // go through iterations
    for (int i = 0; i < iters; ++i)
    {
        // go through over all the trainning data
        for (int k = 0; k < _train_lines; ++k)
        {
            forward_alg(_train_data[k]);
            backward_alg(_train_data[k]);
            get_gamma(_train_data[k]);
            get_epsilon(_train_data[k]);
            accmulate();
        }
        update_model();
        reset_var();
    }
}

// Reset varibles
void BWalg::reset_var()
{
    for (int i = 0; i < MAX_SEQ ;++i)
        for (int j = 0; j < MAX_STATE; ++j)
        {
            _alpha[i][j] = 0;
            _beta[i][j] = 0;
            _gamma[j][i] = 0;
        }
    for (int i = 0; i < MAX_STATE ;++i)
        for (int j = 0; j < MAX_OBSERV; ++j)
            _gamma_obeserve[i][j] = 0;

    for (int i = 0; i < MAX_TRAIN_LEN; ++i)
        for (int j = 0; j < MAX_STATE; ++j)
            for (int k = 0; k < MAX_STATE; ++k)
                _epsilon[i][j][k] = 0;

    for (int j = 0; j < MAX_STATE; ++j)
            for (int k = 0; k < MAX_STATE; ++k)
                _sum_eps[j][k] = 0;

    for (int i = 0; i < MAX_STATE; ++i)
    {
        _sum_gamma_t1[i] = 0;
        _sum_gamma[i] = 0;
        _sum_gamma_t[i] = 0;
    }
}

// Forward algorithm : calculate forward matrix alpha_t = P(o1, o2...o_t, q_t = h | lambda)
void BWalg::forward_alg(const char *seq)
{
    // initialize alpha_1(i) = pi_i*b_i(o_1)
    for (int i = 0; i < hmm->state_num; ++i)
        _alpha[0][i] = hmm->initial[i] * hmm->observation[seq[0] - 'A'][i];
    
    // induction
    for (int t = 0; t < _train_len - 1; ++t)
    {
        for (int j = 0; j < hmm->state_num; ++j)
        {
            double sum = 0.0;
            // alpha_t(i) * a_ij
            for (int i = 0; i < hmm->state_num; ++i)
                sum += _alpha[t][i] * hmm->transition[i][j];
            // sum dot b_j(o_t+1)
            _alpha[t + 1][j] = sum * hmm->observation[seq[t + 1] - 'A'][j];
        }
    }
}

// Backward algorithm : calculate forward matrix beta_t = P(o_t+1, o_t+2...o_T, q_t = i | lambda)
void BWalg::backward_alg(const char *seq)
{
    // initialize
    for (int i = 0; i < hmm->state_num; ++i)
        _beta[_train_len - 1][i] = 1.0;

    // induction
    for (int t = _train_len - 2; t >= 0; --t)
    {
        for (int i = 0; i < hmm->state_num; ++i)
        {
            double sum = 0.0;
            for (int j = 0; j < hmm->state_num; ++j)
                sum += _beta[t + 1][j] * hmm->observation[seq[t + 1] - 'A'][j] * hmm->transition[i][j];
            //             beta_t+1(j)        b_j(o_t+1)                                        a_ij
            _beta[t][i] = sum;
        }
    }
}

// Calculate temporary varible "gamma"
void BWalg::get_gamma(const char *seq)
{
    for (int t = 0; t < _train_len; ++t)
    {  
        double sum = 0.0;
        for (int i = 0; i < hmm->state_num; ++i)
            sum += _alpha[t][i] * _beta[t][i];

        for (int i = 0; i < hmm->state_num; ++i)
            _gamma[i][t] = _alpha[t][i] * _beta[t][i] / sum;

        // gamma obervation
        for (int i = 0; i < hmm->state_num; ++i)
            _gamma_obeserve[seq[t] - 'A'][i] += _gamma[i][t];
    }
}

// Calculate temporary varible "epsilon"
void BWalg::get_epsilon(const char *seq)
{
    for (int t = 0; t < _train_len - 1; ++t)
    {
        double sum = 0.0;
        for (int i = 0; i < hmm->state_num; ++i)
            for (int j = 0; j < hmm->state_num; ++j)
                sum += _alpha[t][i] * hmm->transition[i][j] * hmm->observation[seq[t + 1] - 'A'][j] * _beta[t + 1][j];

        for (int i = 0; i < hmm->state_num; ++i)
            for (int j = 0; j < hmm->state_num; ++j)
                _epsilon[t][i][j] = _alpha[t][i] * hmm->transition[i][j] * hmm->observation[seq[t + 1] - 'A'][j] * _beta[t + 1][j] / sum;      
    }
}

// Accmulate varibles: gamma, epsilon
void BWalg::accmulate()
{
    for (int i = 0; i < hmm->state_num; ++i)
        _sum_gamma_t1[i] += _gamma[i][0];

    for (int t = 0; t < _train_len - 1; ++t)
    {
        for (int i = 0; i < hmm->state_num; ++i)
        {
            _sum_gamma[i] += _gamma[i][t];
            _sum_gamma_t[i] = _sum_gamma[i];
        }
    }

  //for (int t = 0; t < _train_len; ++t)
        for (int i = 0; i < hmm->state_num; ++i)
            //_sum_gamma_t[i] += _gamma[i][t];
            _sum_gamma_t[i] += _gamma[i][_train_len - 1];

    for (int i = 0; i < hmm->state_num; ++i)
        for (int j = 0; j < hmm->state_num; ++j)
            for (int t = 0; t < _train_len - 1; ++t)
                _sum_eps[i][j] += _epsilon[t][i][j];
}

void BWalg::update_model()
{
    // re-estimate pi
    for (int i = 0; i < hmm->state_num; ++i)
        hmm->initial[i] = _sum_gamma_t1[i] / _train_lines; // divide by number of samples

    // re-estimate A
    for (int i = 0; i < hmm->state_num; ++i)
    {
        for (int j = 0; j < hmm->state_num; ++j)
        {
            // accmulate epsilon over all samples
            hmm->transition[i][j] = _sum_eps[i][j] / _sum_gamma[i];
        }
    }

    // re-estimate B
    for (int i = 0; i < hmm->observ_num; ++i)
        for (int j = 0; j < hmm->state_num; ++j)
            hmm->observation[i][j] = _gamma_obeserve[i][j] / _sum_gamma_t[j];
}

// Load the observation sequence file (o1, o2...)
void BWalg::load_train(const char *filename)
{
    FILE *fp = open_or_die(filename, "r");
    char token[MAX_LINE] = "";
    
    while(fscanf(fp, "%s", token) != EOF)
    {
        strcpy(_train_data[_train_lines], token);
        _train_lines++;
    }
    _train_len = strlen(token);

    fclose(fp);
}

void BWalg::dump_td() const
{
    for(int i = 0 ;i < _train_lines; ++i)
        printf("%s\n", _train_data[i]);
}