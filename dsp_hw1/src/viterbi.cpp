#include "viterbi.h"

Viterbi::Viterbi()
{
}

Viterbi::~Viterbi()
{
}

int Viterbi::process_viterbi(HMM &hmm, const int &line)
{
    double maxProb = 0.0;
    for (int t = 0; t < _test_len; ++t)
    {
        for (int i = 0; i < hmm.state_num; ++i)
            _delta[t][i] = 0.0;
    }

    for (int i = 0; i < hmm.state_num; ++i)
    {
        _delta[0][i] = hmm.initial[i] * hmm.observation[_test_data[line][0] - 'A'][i];
    }
    
    for (int t = 1; t < _test_len; ++t)
    {
        double tmp = 0.0;
        double maxN = 0.0;

        for (int j = 0; j < hmm.state_num; ++j)
        {
            maxN = 0;
            for (int i = 0; i < hmm.state_num; ++i)
            {
                tmp = _delta[t - 1][i] * hmm.transition[i][j];
                if (tmp > maxN)
                    maxN = tmp;
            }
            _delta[t][j] = maxN * hmm.observation[_test_data[line][t] - 'A'][j];
        }
    }

    for (int i = 0; i < hmm.state_num; ++i)
    {
        maxProb = max(maxProb, _delta[_test_len - 1][i]);
    }
    return maxProb;
}

void Viterbi::process_models()
{
    double prob = 0.0;
    double maxProb = 0.0;
    for (int j = 0; j < _test_lines; ++j)
    {
        // cout << _test_lines << endl;
        // for (int i = 0; models.size(); ++i)
        for (int i = 0; i < _model_num; ++i)
        {
            cout << i << endl;
            prob = process_viterbi(_models[i], j);
            if (prob > maxProb)
            {
                maxProb = prob;
                _result_idx[j] = i;
            }
        }
    }
}

void Viterbi::load_models(const char *filename)
{
    FILE *fp = open_or_die(filename, "r");
    char model_name[100] = "";

    //_model_num = load_models(filename, test, MAX_MODELS);

    while (fscanf(fp, "%s", model_name) != EOF)
    {
        HMM h;
        loadHMM(&h, model_name);
        //models.push_back(h);
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
    {
        cout << i << endl;
        fprintf(fp, "model_%02d.txt\n", _result_idx[i] + 1);
    }

    fclose(fp);
}