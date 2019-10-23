#ifndef __BWalg_h__
#define __BWalg_h__

#include <iostream>
#include "../inc/hmm.h"
using namespace std;

#define TRAIN_SIZE 10240
#define MAX_TRAIN_LEN 64

class BWalg
{
  public:
    BWalg(/* args */);
    BWalg(HMM &);
    ~BWalg();
    void train(int);
    void forward_alg(const int &);
    void backward_alg(const int &);
    void get_gamma(const int &);
    void get_epsilon(const int &);
    void update_model();
    void load_train(const char *);
    void dump_td() const;

  private:
    HMM *hmm;
    char _train_data[TRAIN_SIZE][MAX_LINE];
    int _train_len = 0;
    int _train_lines = 0;
    double _alpha[MAX_SEQ][MAX_STATE] = {0.0};
    double _beta[MAX_SEQ][MAX_STATE] = {0.0};
    double _gamma[MAX_STATE][MAX_SEQ] = {0.0};
    double _gamma_obeserve[MAX_STATE][MAX_OBSERV] = {0.0};
    double _epsilon[MAX_TRAIN_LEN][MAX_STATE][MAX_STATE] = {0.0};
};

#endif