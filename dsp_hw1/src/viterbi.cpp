#include "viterbi.h"
#include <cstring>

Viterbi::Viterbi()
{
}

Viterbi::~Viterbi()
{
}

double Viterbi::process_viterbi(HMM &hmm, const char *seq)
{
    double prob = 0.0;

    // initialization
    for (int i = 0; i < hmm.state_num; ++i)
        _delta[0][i] = hmm.initial[i] * hmm.observation[seq[0] - 'A'][i];

    // recursion
    for (int t = 1; t < _test_len; ++t)
    {
        for (int j = 0; j < hmm.state_num; ++j)
        {
            _delta[t][j] = 0;
            for (int i = 0; i < hmm.state_num; ++i)
                _delta[t][j] = max(_delta[t][j], _delta[t - 1][i] * hmm.transition[i][j]);
            
            _delta[t][j] *= hmm.observation[seq[t] - 'A'][j];
        }
    }

    // termination
    for (int i = 0; i < hmm.state_num; ++i)
        prob = max(prob, _delta[_test_len - 1][i]);

    return prob;
}

void Viterbi::process_models()
{
    for (int j = 0; j < _test_lines; ++j)
    {
        double prob = 0;
        double maxProb = 0;
        for (int i = 0; i < _model_num; ++i)
        {
            prob = process_viterbi(_models[i], _test_data[j]);
            if (prob > maxProb)
            {
                maxProb = prob;
                _result_prob[j] = prob;
                _result_idx[j] = i;
            }
        }
    }
}

void Viterbi::load_models(const char *filename)
{
    FILE *fp = open_or_die(filename, "r");
    char model_name[100] = "";

    while (fscanf(fp, "%s", model_name) != EOF)
    {
        HMM h;
        loadHMM(&h, model_name);
        _models[_model_num++] = h;
    }

    fclose(fp);
    cout << "Model loaded." << endl;

}

void Viterbi::load_test(const char *filename)
{
    FILE *fp = open_or_die(filename, "r");
    char token[100] = "";

    while(fscanf(fp, "%s", token) != EOF)
    {
        strcpy(_test_data[_test_lines], token);
        _test_lines++;
    }
    _test_len = strlen(token);

    fclose(fp);
}

void Viterbi::save_results(const char *filename)
{
    FILE *fp = open_or_die(filename, "w");

    for (int i = 0; i < _test_lines; ++i)
        fprintf(fp, "model_%02d.txt %.6e\n", _result_idx[i] + 1, _result_prob[i]);

    fclose(fp);
}