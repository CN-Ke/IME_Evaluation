#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt

#global variables
TRUE  = 1
FALSE = 0
L = np.array([4, 8, 16, 32, 64])
cache_size_words = 8  #32Bytes 
#cache_size_words = 16 #64Bytes 
#cache_size_words = 32 #128Bytes 

# get option A hight/width shape of Matrix A (vs1)
def op_A_get_hw_matA(L):
  h_matA = np.array([2, 4, 4, 8, 8])
  w_matA = np.array([2, 2, 4, 4, 8])
  #Note Option A star special handle when L is not lamda's square
  spcial_handle_matA = np.array([1, 2, 1, 2, 1])
  w_matA_special = w_matA*spcial_handle_matA    
  return h_matA, w_matA, w_matA_special

# get option B hight/width shape of Matrix A (vs1)
def op_B_get_hw_matA(L):
  h_matA = L
  w_matA = np.full(5,1) 
  return h_matA, w_matA

# get option C hight/width shape of Matrix A (vs1)
def op_C_get_hw_matA(L):
  h_matA = np.array([2, 4, 8, 16, 32]) 
  w_matA = np.full(5,2) 
  return h_matA, w_matA

# get option E hight/width shape of Matrix A (vs1)
def op_E_get_hw_matA(L):
  h_matA = np.array([2, 4, 8, 16, 32]) 
  w_matA = np.full(5,2) 
  return h_matA, w_matA

# compute locality of option A
def op_A_com_loc(L, RegM, RegN):
  h_matA, w_matA, w_matA_special = op_A_get_hw_matA(L)
  locality_matA  = cache_size_words/w_matA_special
  eff_m = h_matA*RegM
  eff_k = w_matA_special*locality_matA
  eff_n = w_matA*RegN
  eff_mac = eff_m*eff_k*eff_n
  eff_red_dot_m = eff_m
  eff_red_dot_n = eff_k*eff_n/cache_size_words
  eff_red_dot   = eff_red_dot_m+eff_red_dot_n
  com_loc = eff_mac/eff_red_dot  
  return com_loc 

# compute locality of option B
def op_B_com_loc(L, RegM, RegN):
  h_matA, w_matA = op_B_get_hw_matA(L)
  eff_m = h_matA*RegM
  eff_k = np.full(5,cache_size_words)
  eff_n = h_matA*RegN 
  eff_mac = eff_m*eff_k*eff_n
  eff_red_dot_m = eff_m
  eff_red_dot_n = eff_k*eff_n/cache_size_words
  eff_red_dot   = eff_red_dot_m+eff_red_dot_n
  com_loc = eff_mac/eff_red_dot  
  return com_loc 

# compute locality of option C
def op_C_com_loc(L, RegM, RegN):
  h_matA, w_matA = op_C_get_hw_matA(L)
  eff_m = h_matA*RegM
  eff_k = np.full(5,cache_size_words)
  eff_n = h_matA*RegN 
  eff_mac = eff_m*eff_k*eff_n
  eff_red_dot_m = eff_m
  eff_red_dot_n = eff_k*eff_n/cache_size_words
  eff_red_dot   = eff_red_dot_m+eff_red_dot_n
  com_loc = eff_mac/eff_red_dot  
  return com_loc 

# compute locality of option E
def op_C_com_loc(L, RegM, RegN):
  h_matA, w_matA = op_C_get_hw_matA(L)
  eff_m = h_matA*RegM
  eff_k = np.full(5,cache_size_words)
  eff_n = h_matA*RegN 
  eff_mac = eff_m*eff_k*eff_n
  eff_red_dot_m = eff_m
  eff_red_dot_n = eff_k*eff_n/cache_size_words
  eff_red_dot   = eff_red_dot_m+eff_red_dot_n
  com_loc = eff_mac/eff_red_dot  
  return com_loc 

RegM  = np.array([5, 4, 5, 4, 5])
RegN  = np.array([4, 4, 4, 4, 4])
A_loc = op_A_com_loc(L, RegM, RegN)

RegM  = np.array([3, 3, 28/16, 30/32, 30/64]) # where 28,30,30 are affordable Matrix C used VRF numbers
RegN  = np.array([2, 1, 1, 1, 1])
B_loc = op_B_com_loc(L, RegM, RegN)

RegM  = np.array([5, 3, 2, 1, 1])
RegN  = np.array([4, 4, 3, 3, 1])
C_loc = op_C_com_loc(L, RegM, RegN)

RegM  = np.array([5, 4, 3, 3, 1.5])
RegN  = np.array([4, 3, 2, 1, 1])
E_loc = op_C_com_loc(L, RegM, RegN)

plt.plot(L, A_loc, label='Option A*(optimal)', marker='o')
plt.plot(L, B_loc, label='Option B(optimal)', marker='^')
plt.plot(L, C_loc, label='Option C(optimal)', marker='*')
plt.plot(L, E_loc, label='Option E(optimal)', marker='+')

plt.legend()
plt.title('cache line size ' + str(cache_size_words*4) + ' (Bytes)')
plt.xlabel('L(Words)')
plt.ylabel('Compute Locality(MAC/# of $-DRAM access)')
plt.show()
