#include <iostream>
#include <fstream>
#include <vector>
using namespace std;

int main(int argc, char* argv[])
{
    if (argc != 3)
    {
        cerr << "[ERROR] Invalid parameters!\n";
        exit(-1);
    }

    ifstream ifs(argv[1]);
    ofstream ofs(argv[2]);

    if (!ifs.is_open())
    {
        cerr << "[ERROR] Input file open failed!\n";
        exit(-1);
    }

    ifs.close();


    ofs.close();
}