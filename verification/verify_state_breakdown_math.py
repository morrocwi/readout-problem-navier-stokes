import itertools
import numpy as np
from numpy.linalg import norm, eigh

# ---------- exact finite witness ----------
S = list(itertools.product([0,1], repeat=3))

def F(s):
    a,b,c = s
    return (1-a,b,1-c)

def FD(d):
    a,b = d
    return (1-a,b)

def q(s):
    a,b,c = s
    return (a,b)

def O(s):
    return s[1]

def OD(d):
    return d[1]

def Q(d):
    return d[0]

assert all(q(F(s)) == FD(q(s)) for s in S)
assert all(O(s) == OD(q(s)) for s in S)
assert all(F(F(s)) == s for s in S)

z, zp = (0,0,0), (1,0,1)
x,y = z,zp
for k in range(10000):
    assert O(x) == O(y)
    assert Q(q(x)) != Q(q(y))
    x,y = F(x),F(y)

print('finite states:', len(S))
print('dynamical weld:', sum(q(F(s)) == FD(q(s)) for s in S), '/', len(S))
print('observational weld:', sum(O(s) == OD(q(s)) for s in S), '/', len(S))
print('F^2 = Id:', all(F(F(s)) == s for s in S))
print('witness verified through k=9999; period-2 proof implies all k>=0')

# ---------- retained linear model / Euler convergence ----------
# cycle graph Laplacian m=8
m=8
L = np.zeros((m,m))
for i in range(m):
    L[i,i] = 2
    L[i,(i-1)%m] = -1
    L[i,(i+1)%m] = -1

tau = 0.7
w,V = eigh(L)
lmax = w.max()
print('lambda_max:', lmax)
print('Euler stability threshold h <=', 2*tau/lmax)

I0 = np.linspace(-1.0, 1.0, m)
G = np.cos(np.arange(m)) * 0.2
T=1.0

# exact solution modewise for constant G
c0 = V.T @ I0
g = V.T @ G
ce = np.empty_like(c0)
for j,lam in enumerate(w):
    if abs(lam) < 1e-12:
        ce[j] = c0[j] + (T/tau)*g[j]
    else:
        e = np.exp(-lam*T/tau)
        ce[j] = e*c0[j] + (1-e)*g[j]/lam
I_exact = V @ ce

errs=[]
for h in [0.1,0.05,0.025,0.0125]:
    N = int(round(T/h))
    h = T/N
    I=I0.copy()
    A=np.eye(m)-(h/tau)*L
    rho=max(abs(np.linalg.eigvalsh(A)))
    for _ in range(N):
        I=A@I+(h/tau)*G
    err=norm(I-I_exact)
    errs.append(err)
    print(f'h={h:.5f} rho(A)={rho:.8f} error={err:.10e}')
print('error ratios:', [errs[i]/errs[i+1] for i in range(len(errs)-1)])
