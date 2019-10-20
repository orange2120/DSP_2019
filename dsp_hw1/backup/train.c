#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "hmm.h"
#include "BWalg.h"

void load_Train(char [][MAX_LINE], const char *);
void dump_Td(char [][MAX_LINE]);

int main(int argc, char *argv[])
{
    if (argc != 5)
    {
        perror("[ERROR] Invalid parameters!\n");
        exit(-1);
    }

    int iterations = 0;
    

    HMM hmm;
    FILE *model_fp = open_or_die(argv[4], "w");

    for(int i = 0; i< TRAIN_SIZE; ++i)
        memset(train_data[i], '\0', sizeof(char)*MAX_LINE);

    iterations = atoi(argv[1]);
    loadHMM(&hmm, argv[2]);             // load models
    load_Train(train_data, argv[3]);    // load trainning data

    printf("File loaded\n");
    printf("iters: %d\n", iterations);
    /*
    for(int i = 0; i < iterations; ++i)
    {

    }
    */
    dumpHMM(model_fp, &hmm); // dump trained model to file
    //dump_Td(train_data);
}

// Load the observation sequence file (o1, o2...)
//void load_Train(char **td, const char *filename)
void load_Train(char td[][MAX_LINE], const char *filename)
{
    FILE *fp = open_or_die(filename, "r");

    char token[MAX_LINE] = "";
    int cnt = 0;
    while(fscanf(fp, "%s", token) != EOF)
    {
        strcpy(td[cnt], token);
        cnt++;
    }

    fclose(fp);
}

//void dump_Td(char **td)
void dump_Td(char td[][MAX_LINE])
{
    for(int i = 0 ;i < TRAIN_SIZE; ++i)
        printf("%s\n", td[i]);
}