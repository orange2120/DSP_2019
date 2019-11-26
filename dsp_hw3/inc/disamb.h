#ifndef __DISAMB_H__
#define __DISAMB_H__

#include <iostream>
#include <fstream>
using namespace std;

class disamb
{
  public:
    disamb();
    ~disamb();
    void Viterbi();
    bool readSeg(const char *);
    bool readZYB(const char *);
    bool readLM(const char *);
    bool writeFile(const char *);

  private:

};


#endif // __DISAMB_H__
