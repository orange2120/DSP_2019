# 2019 DSP Homework
2019 Fall, Digital Speech Processing

## HW#1 Discrete Hidden Markov Model
Implementing Discrete Hidden Markov Model

### Training
Given a oberservation sequence, applying Baum-Welch algorithm
- Calculate $\alpha$ (forward probabilities) and $\beta$ (backward probabilities)
- Calculate temporary variable $\epsilon$ and $\gamma$
- Update model parameters by given iteration times

$A:$ Transition probability ($N{\times}N$ matrix)  
$B:$ Observation probability (emission matrix) ($1{\times}N$ matrix)  
$\pi:$ State sequence($1{\times}N$ matrix)  

$T:$ Observation number ($T=50$ in this case)  
$N:$ State number ($N=6$ in this case)  
$\alpha_t(i):$ Forward variable matrix $(T{\times}N)$  
$\beta_t(i):$ Backward variable matrix $(T{\times}N)$  
$\gamma_t(i):$ Temporary variable ($N{\times}T$ matrix)  
$\epsilon_t(i,j):$ Temporary variable (total $T-1$, each $N{\times}N$ matrix)  
Notes:    
$A(i,j)=\{a_{ij}\}:$ prob. of state $i{\rightarrow}j$  
$B_{jt}=\{b_j(o_t)\}$  

***Note:***  
Accumlate interval  
$\epsilon_t(i,j): 1{\leq}t{\leq}T-1$  

### Utils
`run_train.py`: Auto run the given iterations for trainning program
Usage: `python3 run_train.py <iterations>`  
`check.py`: Compare the testing result with labeled data. Returns the testing accuracy.  
`run_iters.py`: Auto run multiple iterations. (defined in the file)  
`run_iters_tesr.py`: Auto run multiple testing procedures. (defined in the file)  
`check_iters.py`: The function is the same with `check.py` but for multiple iteraitons.

## HW#2-1 Automatic Speech Recognition of Mandarin Digits

## HW#3 ZhuYin Decoding

### ZhuYin to Big5 mapping

#### map
How to store Big5 characters?  
Every Big5 character is 2 byte, store it in `uint16_t`
```cpp
uint16_t ch = ((uint16_t)x << 8) | (uint16_t)(y & 0xFF);
```

### mydisambig
Mapping 注音 character back to 中文字

Example:
```
讓 他 十 分 ㄏ 怕
            ↓
讓 他 十 分 害 怕
```

Store Big5 characters in `string` type.

`q_{t}`: state at time `t`

Viterbi process:

Since every Big5 character has different numbers of possible states, we need capacity-flexible array to store states.

→ Using vector<string> array, for example:
```
覺 → 覺
ㄉ → 八 匕 卜 不 卞 巴 比 丙...
她 → 她
ㄉ → 丁 刀 刁 大 丹 仃 弔 斗...
ㄅ → 八 匕 卜 不 卞 巴 比 丙...
現 → 現
很 → 很
棒 → 棒
```
Perform Viterbi algorithm on bigram probability of each Chinese character.

#### Initialization
$\delta(i,j)$

Record the index of maximum probability at time `t` in the `map`.

#### backtracking
Find the maximum probability path

***NOTE***
The probability derivated from `LM` is expressed in logrithm. Use addition instead of multiplication.  

#### Tools
`generate_lm.sh`: Generate the language model from `ngram-count`   
`sep_testdata.sh`: Run the word separation script `separator_big5.pl` on test file 1~10.  
`run_all_my.sh`: Run all the test text file from 1~10 for `mydisambig` and output the results.  
`run_all_ref.sh`: Similar to  `run_all_my.sh` but for srilm `disambig`.  
`diff_res.sh`: Run `diff` between my results and reference results.  
