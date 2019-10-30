#ifndef __BWALG_H__
#define __BWALG_H__

#include <iostream>
#include "../inc/hmm.h"
using namespace std;

#define TRAIN_SIZE 10240
#define MAX_TRAIN_LEN 64
#define _MAX_SEQ 64

class BWalg
{
  public:
    BWalg(/* args */);
    BWalg(HMM &);
    ~BWalg();
    void train(int);
    void reset_var();
    void forward_alg(const char *);
    void backward_alg(const char *);
    void get_gamma(const char *);
    void get_epsilon(const char *);
    void accmulate();
    void update_model();
    void load_train(const char *);
    void dump_td() const;

  private:
    HMM *hmm;
    char _train_data[TRAIN_SIZE][_MAX_SEQ];
    int _train_len = 0;
    int _train_lines = 0;
    double _alpha[_MAX_SEQ][MAX_STATE] = {0.0};
    double _beta[_MAX_SEQ][MAX_STATE] = {0.0};
    double _gamma[MAX_STATE][_MAX_SEQ] = {0.0};
    double _gamma_obeserve[MAX_STATE][MAX_OBSERV] = {0.0};
    double _sum_gamma_t1[MAX_STATE] = {0.0};
    double _sum_gamma[MAX_STATE] = {0.0};
    double _sum_gamma_t[MAX_STATE] = {0.0};
    double _epsilon[MAX_TRAIN_LEN][MAX_STATE][MAX_STATE] = {0.0};
    double _sum_eps[MAX_STATE][MAX_STATE] = {0.0};
};

#endif