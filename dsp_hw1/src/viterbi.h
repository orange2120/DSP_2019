#ifndef _VITERBI_H_
#define _VITERBI_H_

#include <iostream>
#include <cstdio>
#include <cstdlib>
#include "../inc/hmm.h"
using namespace std;

#define TEST_SIZE 4096
#define MAX_MODELS 10

class Viterbi
{
  public:
    Viterbi();
    ~Viterbi();

    void predict_model();
    int process_viterbi(HMM &, const int &);
    void process_models();
    void load_models(const char *);
    void load_test(const char *);
    void save_results(const char *);

  private:
    double _delta[MAX_SEQ][MAX_STATE] = {0.0};
    char _test_data[TEST_SIZE][MAX_LINE];
    int _result_idx[TEST_SIZE] = {0};
    int _test_lines = 0.0;
    int _test_len = 0.0;
    int _model_num = 0;
    //vector<HMM> models;
    HMM _models[MAX_MODELS];
};

#endif