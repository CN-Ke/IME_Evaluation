import numpy as np
import matplotlib.pyplot as plt

#global variables
TRUE  = 1
FALSE = 0
L = np.array([4, 8, 16, 32, 64])

def option_A_get_lambda(val):
  lambda_a = val**(1/2)
  lambda_a = lambda_a.astype(int)
  return (lambda_a)

def option_A_D(val, RegM, RegN, mode):
  if mode == "real":
    lambda_a = option_A_get_lambda(val)
  elif mode == "fake":
    lambda_a = val**(1/2)
  else:
    print("ERROR:Not support lambda calculation")
    assert 0
  mac = RegM*RegN*(lambda_a**3)
  #Note only lamda**2 words are loads, insted of L words
  load_words = (RegM+RegN)*(lambda_a**2)
  return (mac/load_words)

def option_B(val):
  return (16*val)/(16+val)

def option_B_opt(val, RegA4x1, RegN):
  mac = RegA4x1*RegN*val
  load_words = RegA4x1+RegN*val
  return (mac/load_words)

def option_C_opt(val, alpha, LambdaM, RegN):
  mac = LambdaM*RegN*val*alpha
  load_words = LambdaM*alpha*alpha + RegN*val
  return (mac/load_words)

def option_C_restrict(val, alpha):
  return (16*val*alpha)/(2*val + 8*(alpha**2))

def option_E(L, M, N):
  return (M*N*L)/(2*(M+N))

RegM  = np.array([5, 5, 5, 5, 5])
RegN  = np.array([4, 4, 4, 4, 4])
A_D_opt = option_A_D(L, RegM, RegN, "real")
RegM  = np.array([4, 4, 4, 4, 4])
RegN  = np.array([4, 4, 4, 4, 4])
A_D_restrict = option_A_D(L, RegM, RegN, "real")
#A_D_fake    = option_A_D(L, RegM, RegN, "fake")

RegA4x1    = np.array([12, 24, 24, 24, 28])
RegN       = np.array([2, 1, 1, 1, 1])
B_opt      = option_B_opt(L, RegA4x1, RegN)
B_restrict = option_B(L)

LambdaM    = np.array([5, 6, 8, 8, 16])
RegN       = np.array([4, 4, 3, 3, 1])
C_opt      = option_C_opt(L, 2, LambdaM, RegN)
LambdaM    = np.array([4, 8, 8, 8, 16])
RegN       = np.array([4, 2, 2, 2, 1])
C_restrict = option_C_opt(L, 2, LambdaM, RegN)
C_alpha2   = option_C_restrict(L,2)
C_alpha4   = option_C_restrict(L,4)

M_opt  = np.array([5, 4, 3, 3, 1.5])
N_opt  = np.array([4, 3, 2, 1, 1])
E_opt  = option_E(L,M_opt,N_opt)

M_restrict = np.array([4, 4, 2, 2, 1])
N_restrict = np.array([4, 2, 2, 1, 1])
E_restrict = option_E(L,M_restrict,N_restrict)

#plt.plot(L, A_D_opt, label='Option A/D(optimal)', marker='o')
#plt.plot(L, A_D_restrict, label='Option A/D(restrict)', marker='x')
#plt.plot(L, A_D_fake, label='Option A/D(preliminary)', marker='o')

#plt.plot(L, B_opt, label='Option B(optimal)', marker='^')
#plt.plot(L, B_restrict, label='Option B(restrict)', marker='^')

# Fix Alpha
#plt.plot(L, C_alpha2, 'b-o', label='Option C(alpha=2)')
#plt.plot(L, C_alpha4, 'r-o', label='Option C(alpha=4)')

# Fix Lemma
#print("Option C(new lemma):",C_opt)
#print("Option C(legacy lemma):",C_restrict)
plt.plot(L, C_opt, 'b-o', label='Option C(optimal)')
plt.plot(L, C_restrict, 'm-o', label='Option C(restrict)')

#print("Option E(optimal):",E_opt)
#plt.plot(L, E_opt, label='Option E(optimal)', marker='X')
#plt.plot(L, E_restrict, label='Option E(restrict)', marker='+')

plt.legend()
plt.xlabel('L(Words)')
plt.ylabel('compute intensity(MAC/Words)')
plt.show()

