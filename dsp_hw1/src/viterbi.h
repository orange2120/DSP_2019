#ifndef _VITERBI_H_
#define _VITERBI_H_

#include <iostream>
#include <vector>
#include "../inc/hmm.h"
using namespace std;

class Viterbi
{
  public:
    Viterbi();
    ~Viterbi();

    void process_viterbi();
    void load_models(const char *);

  private: 
    double _delta[MAX_SEQ][MAX_STATE] = {0.0};
    double _beta[MAX_SEQ][MAX_STATE] = {0.0};
    vector<HMM> models;
};

#endif