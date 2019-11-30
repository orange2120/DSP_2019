#include "disamb.h"

disamb::disamb()
{
	_lm = new Ngram(_voc, NGRAM_ORDER);
}

disamb::~disamb()
{
	// clean the map
	unordered_map<string, vector<string> *>::iterator it;
	for (it = _map.begin(); it != _map.end(); ++it)
		delete it->second;
	delete _lm;
}

// get bigram probability, P(w1|w2)
inline double disamb::getBiGProb(const char* w1, const char* w2)
{
	VocabIndex wid1 = _voc.getIndex(w1);
	VocabIndex wid2 = _voc.getIndex(w2);
	if(wid1 == Vocab_None)  // OOV
        wid1 = _voc.getIndex(Vocab_Unknown);
    if(wid2 == Vocab_None)
        wid2 = _voc.getIndex(Vocab_Unknown);
	VocabIndex context[] = { wid1, Vocab_None };
	return _lm->wordProb(wid2, context);
}

// Viterbi algorithm
string disamb::Viterbi(string &str)
{
	vector<string> input_v;
	input_v.reserve(100);
	// split string and store into big5 character array
	for (unsigned i = 0; i < str.length(); i++) // first character must be "<s>", ommit it.
	{
		if (str[i] != ' ')
		{
			input_v.push_back(str.substr(i, 2));
			i += 2;
		}
	}
	
	unsigned len = input_v.size() + 1; // variable "t", that is, length of big5 string / 2
	input_v.push_back("</s>");		   // add </s> to the last of the string

	string result = "";
	vector<uint32_t> *state[len];
	for (unsigned i = 0; i < len; ++i)
		state[i] = new vector<uint32_t>;
	vector<double> *delta[len];
	for (unsigned i = 0; i < len; ++i)
		delta[i] = new vector<double>;

	// is a array to vector<string> pointer in the map
	vector<string> *input_map[len];
	for (unsigned i = 0; i < len; ++i)
	{
		input_map[i] = _map[input_v[i]];
		delta[i]->resize(input_map[i]->size());
		state[i]->resize(input_map[i]->size());
		// cerr << "map[" << i << "] = " << input_map[i]->size() << endl;
	}

	// initialization, delta_1(q_i) = P(W_1 = q_i)
	for (uint32_t i = 0; i < input_map[0]->size(); ++i)
		delta[0]->operator[](i) = getBiGProb("<s>", input_map[0]->operator[](i).c_str());

	double prob = 0;
	// recursion, delta_t(q_t) = max P(q_i|) P(W_1:t-1)
	for (uint32_t t = 1; t < len; ++t)
	{
		for (uint32_t i = 0; i < delta[t]->size(); ++i)
		{
			delta[t]->operator[](i) = -1e12;
			prob = 0;
			for (uint32_t j = 0; j < delta[t - 1]->size(); ++j) // find max in q_j
			{
				prob = delta[t - 1]->operator[](j) + getBiGProb(input_map[t - 1]->operator[](j).c_str(), input_map[t]->operator[](i).c_str()); // prev , next
				if (prob > delta[t]->operator[](i))
				{
					delta[t]->operator[](i) = prob; // max prob in time "t" of state j
					state[t]->operator[](i) = j; 	// index of max prob
				}
			}
		}
	}

	double maxProb = -1e12;
	uint32_t maxIdx = 0;

	// termination, *P = max(delta[T]) from state 1 to n
	for (uint32_t i = 0; i < delta[len - 1]->size(); ++i)
	{
		prob = delta[len - 1]->operator[](i);
		if (prob > maxProb)
		{
			maxProb = prob;
			maxIdx = i;
		}
	}

	// backtrack
	vector<string> out_v(len);
	for (int32_t t = len - 1; t >= 0; --t)
	{
		out_v[t] = input_map[t]->at(maxIdx);
		maxIdx = state[t]->operator[](maxIdx);
	}
	for (uint32_t t = 0; t < len - 1; ++t)
		result += out_v[t] + " "; // concatenate characters

	for (unsigned i = 0; i < len; ++i)
	{
		delete state[i];
		delete delta[i];
	}
	return result;
}

// read segmented text file line by line,
// runnging Viterbi process
// write decoded result to output file
bool disamb::processing(const char *ifName, const char* ofName)
{
	ifstream ifs(ifName);
	ofstream ofs(ofName);
	if (!ifs.is_open() || !ofs.is_open())
		return false;

	string str = "";
	while (getline(ifs, str, '\n'))
	{
		string out = Viterbi(str);
		ofs << "<s> " << out << "</s>" << endl;
	}

	ifs.close();
	ofs.close();
	return true;
}

// read Zhu Yin-to-Big5 file into hash table
bool disamb::readMapping(const char* filename)
{
	ifstream ifs(filename);
	if (!ifs.is_open())
		return false;

	vector<string> *v;
	string input;
	while (getline(ifs, input, '\n'))
	{
		uint32_t len = input.size();
		v = new vector<string>;
		_map.insert(pair<string, vector<string> *>(input.substr(0, 2), v)); // build map, the first character as key

		for (uint32_t i = 2; i < len; i++)
		{
			if (input[i] != ' ')
			{
				v->push_back(input.substr(i, 2));
				i += 2;
			}
		}
	}

	v = new vector<string>;
	v->push_back("</s>");
	_map.insert(pair<string, vector<string> *>("</s>", v));
	_nState = _map.size();

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