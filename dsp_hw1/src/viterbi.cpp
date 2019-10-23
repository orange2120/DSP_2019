#include "viterbi.h"

Viterbi::Viterbi()
{
}

Viterbi::~Viterbi()
{
}

void Viterbi::process_viterbi()
{
    
}

void Viterbi::load_models(const char *filename)
{
    FILE *fp = open_or_die(filename, "r");
    char model_name[100] = "";

    while(fscanf(fp, "%s", model_name) != EOF)
    {
        HMM h;
        loadHMM(&h, model_name);
        models.push_back(h);
    }

    fclose(fp);
}