#ifndef __BWalg_h__
#define __BWalg_h__

#include "hmm.h"

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
    void get_gamma();
    void get_epsilon();
    void load_train(const char *);
    void dump_td() const;

  private:
    HMM *hmm;
    char train_data[TRAIN_SIZE][MAX_LINE];
    int train_len = 0;
    int train_lines = 0;
    double alpha[MAX_SEQ][MAX_STATE] = {0.0};
    double beta[MAX_SEQ][MAX_STATE] = {1.0};
    double gamma[MAX_STATE][MAX_SEQ] = {0.0};
    double epsilon[MAX_TRAIN_LEN][MAX_STATE][MAX_STATE] = {0.0};
    const char states[] = {'A', 'B', 'C', 'D', 'E', 'F'}; // state number sequence
};

#endif