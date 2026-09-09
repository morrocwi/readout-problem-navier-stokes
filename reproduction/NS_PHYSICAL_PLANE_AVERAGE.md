# Exact Physical Plane-Average Readout: Sparse Terminal Support, Immediate Triad Saturation

## 1. Physical reader

On the periodic cube, define the plane-average velocity normal to the `x` axis by

\[
\bar u(x,T)=\frac{1}{(2\pi)^2}\int_0^{2\pi}\int_0^{2\pi}u(x,y,z,T)\,dy\,dz.
\]

For

\[
u(x,y,z,T)=\sum_{k\in K_M}\hat u_k(T)e^{i(k_xx+k_yy+k_zz)},
\]

Fourier orthogonality gives the exact finite readout

\[
\boxed{
\bar u(x,T)=\sum_{k\in A_x}\hat u_k(T)e^{ik_xx}
}
\]

with

\[
A_x=\{(a,0,0):1\le |a|\le K\}.
\]

Thus, for the zero-mean cube

\[
K_M=\{-K,\ldots,K\}^3\setminus\{0\},
\]

the reader uses only

\[
|A_x|=2K
\]

out of

\[
|K_M|=(2K+1)^3-1
\]

modes.

The same statement holds under coordinate permutation for plane averages normal to `y` or `z`.

## 2. Exact NS dependency pullback

For a mode set `S`, define one ordered-triad dependency pullback

\[
D(S)=S\cup\{p,q\in K_M:\ p+q=k\text{ for some }k\in S\}.
\]

This is a dependency operator, not a closure model.

### Theorem: one-pullback saturation

For every integer cutoff `K >= 1`,

\[
\boxed{D(A_x)=K_M.}
\]

### Proof

Take arbitrary `p in K_M`.

If `p in A_x`, then `p in D(A_x)` by definition.

Otherwise choose

\[
a=\begin{cases}
K,&p_x\ge0,\\
-K,&p_x<0.
\end{cases}
\]

Then `k=(a,0,0) in A_x`. Define

\[
q=k-p=(a-p_x,-p_y,-p_z).
\]

Since `p_x in [-K,K]`, the chosen sign gives

\[
|a-p_x|\le K.
\]

Also `|p_y|,|p_z| <= K`, hence every component of `q` lies in `[-K,K]`. Because `p notin A_x`, at least one transverse component is nonzero whenever needed, so `q != 0`. Therefore `q in K_M` and

\[
p+q=k\in A_x.
\]

Hence `p in D(A_x)`. Since `p` was arbitrary,

\[
K_M\subseteq D(A_x).
\]

The reverse inclusion is immediate from the definition of `D`. Therefore

\[
D(A_x)=K_M.
\]

QED.

## 3. Consequence for classical RK4

For terminal set `A_x`, exact stage pullback gives

\[
K_4=A_x,
\]

\[
K_3=D(A_x)=K_M,
\]

and therefore

\[
K_2=K_1=S_{\rm in}=K_M.
\]

So one exact RK4 step saves structural triad work only in the terminal `k4` stage. For a multi-step horizon, every earlier time step is fully relevant because the input relevance of the final step is already `K_M`.

Let

\[
C=\sum_{k\in K_M}|\mathcal T_k|
\]

be the ordered-triad work for one full RHS evaluation and

\[
C_A=\sum_{k\in A_x}|\mathcal T_k|
\]

the work for the axis terminal modes.

For horizon `H`, full RK4 work is

\[
C_{\rm full}=4HC.
\]

The exact retained slicing work is

\[
\boxed{
C_R=(4H-1)C+C_A.
}
\]

Hence the structural gain is

\[
\boxed{
G_H=\frac{4HC}{(4H-1)C+C_A}.
}
\]

Since `0 < C_A < C`,

\[
\boxed{
1<G_H<\frac{4H}{4H-1}.
}
\]

In particular,

\[
G_1<\frac43,\qquad
G_2<\frac87,\qquad
G_3<\frac{12}{11},
\]

and

\[
\lim_{H\to\infty}G_H=1.
\]

This is a structural ceiling for exact plane-average slicing under this classical RK4 dependency graph. Backend improvements such as vectorized fused triads can add implementation speedups at small cutoffs, but those are separate from the readout-slicing gain.

## 4. Incompressibility consequence

For `k=(a,0,0)` the Leray constraint is

\[
k\cdot\hat u_k=a\hat u_{k,x}=0.
\]

Thus each nonzero terminal axis mode satisfies

\[
\hat u_{k,x}=0,
\]

so the plane-average component along the plane normal vanishes:

\[
\boxed{\bar u_x(x,T)=0}
\]

for the zero-mean finite state. The nontrivial physical plane-average readout is therefore carried by the two transverse velocity components.

## 5. Interpretation through Readout / IDM

The terminal reader is genuinely sparse:

\[
\frac{|A_x|}{|K_M|}
=
\frac{2K}{(2K+1)^3-1}
\to0.
\]

But sparse terminal support does not imply a sparse dynamical dependency cone:

\[
\boxed{
|A_x|\ll|K_M|
\quad\not\Rightarrow\quad
|D(A_x)|\ll|K_M|.
}
\]

For this reader,

\[
|D(A_x)|=|K_M|.
\]

So the correct acceleration question is not only whether the reader is low-dimensional or Fourier-sparse. It is whether its **backward NS triad cone remains sparse over the declared numerical horizon and integrator DAG**.

## 6. Reproduction

Executable checker:

```text
reproduction/checks/check_volume6_ns_plane_average.py
```

It checks:

1. sparse terminal support;
2. one-pullback saturation on the tested cubes;
3. retained/full RK4 terminal readout agreement;
4. direct-triad/FFT backend equivalence;
5. real-field and incompressibility residuals;
6. the exact finite structural work law;
7. finite timing as diagnostic only.

## Claim boundary

This result is about a fixed finite Fourier-Galerkin state space and a fixed classical RK4 recurrence. It is not a continuum Navier-Stokes regularity theorem and does not claim a universal runtime speedup.
