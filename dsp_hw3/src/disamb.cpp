#include "disamb.h"

disamb::disamb()
{
	_lm = new Ngram(_voc, NGRAM_ORDER);

}

disamb::~disamb()
{
	unordered_map<string, vector<string> *>::iterator it;
	for (it = _map.begin(); it != _map.end(); ++it)
		delete it->second;
	delete _lm;
}

// get bigram probability, P(w1|w2)
double disamb::getBiGProb(const char* w1, const char* w2)
{
	VocabIndex wid1 = _voc.getIndex(w1);
	VocabIndex wid2 = _voc.getIndex(w2);
	if(wid1 == Vocab_None)  // OOV
        wid1 = _voc.getIndex(Vocab_Unknown);
    if(wid2 == Vocab_None)
        wid2 = _voc.getIndex(Vocab_Unknown);
	VocabIndex context[] = { wid1, Vocab_None };
	return _lm->wordProb( wid2, context);
}

// Viterbi algorithm
void disamb::Viterbi(string &str)
{
	unsigned t = str.length() / 2; // variable "t", that is, length of big5 string / 2
	string result = "";
	// initialization
	for (uint32_t i = 0; i < t; ++i)
	{
		_delta[i][i] = 

	}
	// recursion

	// termination

	// backtrack
}

void disamb::processing()
{

}

// read segmented text file line by line
bool disamb::readSeg(const char* filename)
{
	ifstream ifs(filename);
	if (!ifs.is_open())
		return false;

	string str = "";
	while (getline(ifs, str, '\n'))
	{

	}

	ifs.close();
	return true;
}

// read Zhu Yin-to-Big5 file into hash table
bool disamb::readMapping(const char* filename)
{
	ifstream ifs(filename);
	if (!ifs.is_open())
		return false;

	string input;
	while (getline(ifs, input, '\n'))
	{
		string big5char = "";
		unsigned len = input.size();
		big5char = input.substr(0, 2); // read in first big5 character
		// cout << len << endl;
		vector<string> *v = new vector<string>;
		_map.insert(pair<string, vector<string> *>(big5char, v)); // build map, the first character as key
	
		for (unsigned i = 2; i < len; i++)
		{
			if (input[i] == ' ')
			{
				big5char = input.substr(i + 1, 2);
				// cout << big5char << endl;
				v->push_back(big5char);
			}
		}
	}

	ifs.close();
	return true;
}

// read language model
bool disamb::readLM(const char* filename)
{
	File fp_lm(filename, "r");

	if (fp_lm.error())
		return false;

	_lm->read(fp_lm);

	fp_lm.close();
	return true;
}

/*
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
*/
