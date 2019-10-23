#include "BWalg.h"

BWalg::BWalg(HMM &h)
{
    hmm = &h;
    for (int i = 0; i < TRAIN_SIZE; ++i)
        memset(_train_data[i], '\0', sizeof(char) * MAX_LINE);
    for (int i = 0; i <MAX_SEQ ;++i)
        for (int j = 0; j < MAX_STATE; ++j)
        {
            _alpha[i][j] = 0.0;
            _beta[i][j] = 0.0;
            _gamma[j][i] = 0.0;
        }
    for (int i = 0; i < MAX_STATE ;++i)
        for (int j = 0; j < MAX_OBSERV; ++j)
            _gamma_obeserve[i][j] = 0.0;

    for (int i = 0; i < MAX_TRAIN_LEN; ++i)
        for (int j = 0; j < MAX_STATE; ++j)
            for (int k = 0; k < MAX_STATE; ++k)
                _epsilon[i][j][k] = 0.0;
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
        for (int k = 0; k < _train_lines; ++k)
        {
            forward_alg(k);
            backward_alg(k);
            get_gamma(k);
            get_epsilon(k);
        }
        update_model();
    }
}

// Forward algorithm : calculate forward matrix alpha_t = P(o1, o2...o_t, qt = h | lambda)
void BWalg::forward_alg(const int &line)
{
    // initialize alpha_1(i) = pi_i*b_i(o_1)
    for (int i = 0; i < hmm->state_num; ++i)
        _alpha[0][i] = hmm->initial[i] * hmm->observation[_train_data[line][0] - 'A'][i];
    
    // induction
    for (int t = 1; t < _train_len; ++t)
    {
        for (int j = 0; j < hmm->state_num; ++j)
        {
            // alpha_t(i) * a_ij
            for (int i = 0; i < hmm->state_num; ++i)
                _alpha[t][i] += _alpha[t - 1][i] * hmm->transition[i][j];
            // sum dot b_j(o_t+1)
            _alpha[t][j] *= hmm->observation[_train_data[line][t] - 'A'][j];
        }
    }
}

void BWalg::backward_alg(const int &line)
{
    // initialize
    for (int i = 0; i < hmm->state_num; ++i)
        _beta[_train_len - 1][i] = 1.0;

    // induction
    for (int t = _train_len - 2; t >= 0; --t)
    {
        for (int i = 0; i < hmm->state_num; ++i)
        {
            _beta[t][i] = 0.0;
            for (int j = 0; j < hmm->state_num; ++j)
                _beta[t][i] += _beta[t + 1][j] * hmm->observation[_train_data[line][t + 1] - 'A'][j] * hmm->transition[i][j];
                //             beta_t+1(j)        b_j(o_t+1)                                        a_ij                
        }
    }
}

void BWalg::get_gamma(const int &line)
{
    double sum = 0.0;
    for (int t = 0; t < _train_len; ++t)
    {  
        sum = 0.0;
        for (int i = 0; i < hmm->state_num; ++i)
            sum += _alpha[t][i] * _beta[t][i];
        
        for (int i = 0; i < hmm->state_num; ++i)
            _gamma[i][t] += _alpha[t][i] * _beta[t][i] / sum;
        
        for (int i = 0; i < hmm->observ_num; ++i)
        {
            for (int j = 0; j < hmm->state_num; ++j)
            {
                _gamma_obeserve[j][_train_data[line][t] - 'A'] = _gamma[i][t] / sum;
            }
        }
        
    }
}

void BWalg::get_epsilon(const int &line)
{
    double sum = 0.0;
    //double numerator[MAX_SEQ][MAX_STATE][MAX_STATE] = {0.0};
    for (int t = 0; t < _train_len - 1; ++t)
    {
        sum = 0.0;
        for (int i = 0; i < hmm->state_num; ++i)
        {
            for (int j = 0; j < hmm->state_num; ++j)
            {
                sum += _alpha[t][i] * hmm->transition[i][j] * hmm->observation[_train_data[line][t + 1] - 'A'][j] * _beta[t + 1][j];
                //sum += numerator[t][i][j];
                //_epsilon[t][i][j] = _alpha[t][i] * hmm->transition[i][j] * hmm->observation[_train_data[line][t + 1] - 'A'][j] * _beta[t + 1][j];
                //sum += _epsilon[t][i][j];
            }
        }
        for (int i = 0; i < hmm->state_num; ++i)
            for (int j = 0; j < hmm->state_num; ++j)
                 _epsilon[t][i][j] += _alpha[t][i] * hmm->transition[i][j] * hmm->observation[_train_data[line][t + 1] - 'A'][j] * _beta[t + 1][j] / sum;
                //_epsilon[t][i][j] += numerator[t][i][j] / sum;
                
    }
}

void BWalg::update_model()
{
    double denominator = 0.0;
    double numerator = 0.0;
    
    // re-estimate pi
    for (int i = 0; i < hmm->state_num; ++i)
        hmm->initial[i] = _gamma[i][0] / _train_lines; // divide by number of samples

    // re-estimate A
    for (int i = 0; i < hmm->state_num; ++i)
    {
        
        denominator = 0.0;
        for (int t = 0; t < _train_len - 1; ++t)
            denominator += _gamma[i][t];

        for (int j = 0; j < hmm->state_num; ++j)
        {
            hmm->transition[i][j] = 0.0;
            for (int t = 0; t < _train_len - 1; ++t)
                hmm->transition[i][j] += _epsilon[t][i][j];
            hmm->transition[i][j] /= denominator;

            cout << hmm->transition[i][j] << endl;
        }
        cout << endl;
    }

    // re-estimate B
    for (int i = 0; i < hmm->observ_num; ++i)
    {
    }
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
    for(int i = 0 ;i < TRAIN_SIZE; ++i)
        printf("%s\n", _train_data[i]);
}