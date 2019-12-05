#include "Ngram.h"

#include <iostream>
#include <fstream>
#include <unordered_map>
#include <vector>

using namespace std;

#define NGRAM_ORDER 2 // for bigram encoding
#define MIN_PROB -1e12

inline double getBiGProb(const char *, const char *);
string Viterbi(string &);

Vocab _voc;
Ngram _lm(_voc, NGRAM_ORDER); // language model
unordered_map<string, vector<string> *> map;

int main(int argc, char* argv[])
{
	if (argc != 5)
	{
		cerr << "[ERROR] Invalid parameters!\n";
		cerr << "Usage: ./mydisambig <segemented file> <ZhuYin-Big5 mapping> <language model> <output file>\n";
		exit(-1);
	}

    

    ifstream fmap(argv[2]);
	if (!fmap.is_open())
		return 0;

	vector<string> *v;
	string input;
	while (getline(fmap, input, '\n'))
	{
		uint32_t len = input.size();
		v = new vector<string>;
		map.insert(pair<string, vector<string> *>(input.substr(0, 2), v)); // build map, the first character as key

		for (uint32_t i = 2; i < len; i++) // read after second character
		{
			if (input[i] != ' ')
			{
				v->push_back(input.substr(i, 2));
				i += 2;
			}
		}
	}
    fmap.close();

    File fp_lm(argv[3], "r");
	if (fp_lm.error())
		return 0;
	_lm.read(fp_lm);
	fp_lm.close();

    ifstream ifs(argv[1]);
	ofstream ofs(argv[4]);
	if (!ifs.is_open() || !ofs.is_open())
		return false;

	string str = "";
	while (getline(ifs, str, '\n'))
	{
		ofs << "<s>" << Viterbi(str) << "</s>" << endl;
	}

	ifs.close();
	ofs.close();

}

// get bigram probability, P(w1|w2)
inline double getBiGProb(const char* w1, const char* w2)
{
	VocabIndex wid1 = _voc.getIndex(w1);
	VocabIndex wid2 = _voc.getIndex(w2);
	if(wid1 == Vocab_None)  // replace OOV with <unk>
        wid1 = _voc.getIndex(Vocab_Unknown);
    if(wid2 == Vocab_None)
        wid2 = _voc.getIndex(Vocab_Unknown);
	VocabIndex context[] = { wid1, Vocab_None };
	return _lm.wordProb(wid2, context);
}

// Viterbi algorithm
string Viterbi(string &str)
{
	uint32_t len = 2; // variable "t", that is, length of big5 string / 2 + 2 (<s> + input + </s>)
	uint32_t maxIdx = 0;
	LogP prob = MIN_PROB;
	LogP maxProb = MIN_PROB;
	vector<vector<string> *> input_map;
	input_map.reserve(100);
	input_map.push_back(map["<s>"]); // add <s> to the first of the string
	// split string and store into big5 character array
	for (unsigned i = 0; i < str.length(); ++i)
	{
		if (str[i] != ' ')
		{
			input_map.push_back(map[str.substr(i, 2)]);
			len++;
			i += 2;
		}
	}
	input_map.push_back(map["</s>"]);  // add </s> to the last of the string

	string result = "";
	vector<vector<uint32_t>> state(len);
	vector<vector<LogP>> delta(len);
	// cerr << input_map.size() << endl;

	for (unsigned i = 0; i < len; ++i)
	{
		state[i].resize(input_map[i]->size());
		delta[i].resize(input_map[i]->size());
		// cerr << "[" << i << "]" << input_map[i]->size() << " ";
	}
	// cerr << endl;

	// recursion, delta_t(q_t) = max P(q_i|) P(W_1:t-1)
	for (uint32_t t = 1; t < len; ++t)
	{
		for (uint32_t i = 0; i < delta[t].size(); ++i)
		{
			delta[t][i] = MIN_PROB;
			prob = MIN_PROB;
			for (uint32_t j = 0; j < delta[t - 1].size(); ++j) // find max in q_j
			{
				prob = delta[t - 1][j] + getBiGProb(input_map[t - 1]->operator[](j).c_str(), input_map[t]->operator[](i).c_str()); // prev , next
				if (prob > delta[t][i])
				{
					delta[t][i] = prob; // max prob in time "t" of state j
					state[t][i] = j; 	// index of max prob
				}
			}
		}
	}

	// termination, *P = max(delta[T]) from state 1 to n
	for (uint32_t i = 0; i < delta[len - 1].size(); ++i)
	{
		prob = delta[len - 1][i];
		if (prob > maxProb)
		{
			maxProb = prob;
			maxIdx = i;
		}
	}

	// backtrack
	vector<string> out_v(len); // output string sequence
	for (int32_t t = len - 1; t > 0; --t)
	{
		out_v[t] = input_map[t]->operator[](maxIdx);
		maxIdx = state[t][maxIdx];
	}
	for (uint32_t t = 0; t < len - 1; ++t)
		result += out_v[t] + " "; // concatenate characters

	return result;
}