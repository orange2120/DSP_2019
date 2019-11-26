#include "../inc/disamb.h"

disamb::disamb()
{

}

disamb::~disamb()
{

}

// Viterbi algorithm
void disamb::Viterbi()
{

}

// read segmented text file
bool disamb::readSeg(const char*filename)
{
	ifstream ifs(filename);
	if (!ifs.is_open())
		return false;

	
	ifs.close();
	return true;
}

// read Zhu Yin to Big5 file
bool disamb::readZYB(const char*filename)
{
	ifstream ifs(filename);
	if (!ifs.is_open())
		return false;

	
	ifs.close();
	return true;
}

// read language model
bool disamb::readLM(const char *filename)
{
	ifstream ifs(filename);
	if (!ifs.is_open())
		return false;

	
	ifs.close();
	return true;
}

bool disamb::writeFile(const char*filename)
{
	ofstream ofs(filename);
	if (!ofs.is_open())
		return false;
	ofs << "<s> ";

	ofs << "</s>" << endl;
	ofs.close();
	return true;
}
