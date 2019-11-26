#include <iostream>
#include <fstream>
#include <unordered_map>
#include <vector>
#include <cstring>
using namespace std;

#define MAX_INPUT_LEN 50
#define BIG2UINT(x, y) ((uint16_t)x << 8) | (uint16_t)(y & 0xFF) // convert 2 byte Big5 character to 2 byte unsigned interger

#define VP pair<uint16_t, vector<uint16_t>*>

/*
    Big5 ZhuYin mapping:
    ㄅ~ㄏ: A374~A37E
    ㄐ~ㄦ: A3A1~A3B7
    ㄧ~ㄩ: A3B8~A3BA
    ˉ~ˋ  : A3BC~A3BF
*/

int main(int argc, char* argv[])
{
    if (argc != 3)
    {
        cerr << "[ERROR] Invalid parameters!\n";
        cerr << "Usage: ./map <Big5-ZhuYin mapping file> <ZhuYin-Big5 mapping file>\n";
        exit(-1);
    }

    ifstream ifs(argv[1]);
    ofstream ofs(argv[2]);

    if (!ifs.is_open())
    {
        cerr << "[ERROR] Input file open failed!\n";
        exit(-1);
    }

    uint16_t zhuYinMap[37];
    unordered_map<uint16_t, vector<uint16_t>*> zhuYins;

    // Fill the zhuYin map from ㄅ to ㄦ
    for (uint16_t i = 0; i < 11; ++i)
    {
        zhuYinMap[i] = 0xA374 + i;
        zhuYins.insert(VP(0xA374 + i, new vector<uint16_t>));
    }
    for (uint16_t i = 0; i < 11; ++i)
    {
        zhuYinMap[i + 11] = 0xA3A1 + i;
        zhuYins.insert(VP(0xA3A1 + i, new vector<uint16_t>));
    }
    zhuYins.insert(VP(0xA3B8, new vector<uint16_t>));
    zhuYins.insert(VP(0xA3B9, new vector<uint16_t>));
    zhuYins.insert(VP(0xA3BA, new vector<uint16_t>));
    zhuYinMap[21] = 0xA3B8;
    zhuYinMap[22] = 0xA3B9;
    zhuYinMap[23] = 0xA3BA;
    for (uint16_t i = 0 ; i < 13; ++i)
    {
        zhuYinMap[i + 24] = 0xA3AB + i;
        zhuYins.insert(VP(0xA3AB + i, new vector<uint16_t>));
    }

    // reserve space for characters
    unordered_map<uint16_t, vector<uint16_t>*>::const_iterator it = zhuYins.begin();
    for (; it != zhuYins.end(); ++it)
        it->second->reserve(100);

    char input[MAX_INPUT_LEN] = "";

    while(ifs.getline(input, MAX_INPUT_LEN, '\n'))
    {
        // get blank character pointer
        char *pch = strchr(input, ' ');
        char *poYin = NULL;
        pch++; // move pointer next to ' '
        uint16_t z = BIG2UINT(*(pch), *(pch + 1)); // get zhuYin capital

        vector<uint16_t> *v = zhuYins[z]; // get zhuYin array
        v->push_back(BIG2UINT(input[0], input[1])); // push BIG5 character into vector
        
        // handle polyphone
        while ((poYin = strchr(pch, '/')) != NULL)
        {
            poYin++; // get character next to "/"
            pch = poYin;
            uint16_t po = BIG2UINT(*poYin, *(poYin + 1));

            if (z != po)
            {
                v = zhuYins[po];
                v->push_back(BIG2UINT(input[0], input[1]));
            }
        }
    }
    ifs.close();

    vector<uint16_t> *vec;
    for (int i = 0; i < 37; ++i)
    {
        uint16_t zy = zhuYinMap[i];
        vec = zhuYins[zy];
        if (vec->empty())
            continue;

        ofs << (char)(zy >> 8) << (char)zy << " ";
        for (uint16_t j = 0; j < vec->size(); ++j)
            ofs << (char)(vec->at(j) >> 8) << (char)vec->at(j) << " ";
        ofs << endl;
        for (uint16_t j = 0; j < vec->size(); ++j)
            ofs << (char)(vec->at(j) >> 8) << (char)vec->at(j) << " " << (char)(vec->at(j) >> 8) << (char)vec->at(j) << endl;
    }
    ofs.close();
}