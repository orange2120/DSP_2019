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