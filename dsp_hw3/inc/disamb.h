#ifndef __DISAMB_H__
#define __DISAMB_H__

#include <iostream>
#include <fstream>
#include <unordered_map>
#include <vector>
#include "Ngram.h"

using namespace std;

#define NGRAM_ORDER 2 // for bigram encoding
#define MIN_PROB -1e12

class disamb
{
  public:
    disamb();
    ~disamb();

    inline double getBiGProb(const char *, const char *);
    string Viterbi(string &);
    bool processing(const char *, const char *);
    bool readMapping(const char *);
    bool readLM(const char *);

  private:
    Vocab _voc;
    Ngram *_lm; // language model
    unordered_map<string, vector<string> *> _map;
};

#endif // __DISAMB_H__