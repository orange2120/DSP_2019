#ifndef __DISAMB_H__
#define __DISAMB_H__

#include <iostream>
#include <fstream>
#include <unordered_map>
#include <vector>
#include "Ngram.h"
#include "Vocab.h"
#include "File.h"

using namespace std;

#define NGRAM_ORDER 2 // for bigram encoding

class disamb
{
  public:
    disamb();
    ~disamb();

    double getBiGProb(const char *, const char *);
    void Viterbi(string &);
    void processing();
    bool readSeg(const char *);
    bool readMapping(const char *);
    bool readLM(const char *);
    bool writeFile(const char *);

  private:
    Vocab _voc;
    Ngram *_lm;
    unordered_map<string, vector<string> *> _map;
    double _delta**;
};

#endif // __DISAMB_H__
