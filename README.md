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
$\alpha_t(i):$ Forward matrix $(T{\times}N)$  
$\beta_t(i):$ Backward matrix $(T{\times}N)$  
$\gamma_t(i):$ Temporary variable ($N{\times}T$ matrix)  
$\epsilon_t(i,j):$ Temporary variable (total $T-1$, each $N{\times}N$ matrix)  
