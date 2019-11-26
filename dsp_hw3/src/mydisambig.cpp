#include <iostream>
#include "../inc/disamb.h"
using namespace std;

int main(int argc, char* argv[])
{
	if (argc != 5)
	{
		cerr << "[ERROR] Invalid parameters!\n";
		cerr << "Usage: ./mydisambig <segemented file> <ZhuYin-Big5 mapping> <language model> <output file>\n";
		exit(-1);
	}
	
	disamb dis;
	dis.readSeg(argv[1]);
	dis.readZYB(argv[2]);
	dis.readLM(argv[3]);

	dis.writeFile(argv[5]);
}
