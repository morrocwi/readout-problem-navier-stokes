# Exact Physical Harmonic Probe: Two-Mode Terminal Support and Retained RK4 Cone

## Status

This note records the physical harmonic reader used by
`checks/check_volume6_ns_harmonic_probe.py` and separates three claims:

1. the reader identity is exact for the fixed finite Fourier representation;
2. the backward relevance cone is obtained directly from the Navier--Stokes triad graph and the classical RK4 DAG;
3. any runtime speed-up is only a finite diagnostic of the implementation used by the checker.

Nothing here is a continuum Navier--Stokes regularity theorem, a singularity theorem, or an all-resolution acceleration theorem.

---

## 1. Physical reader

On the periodic cube, for a real velocity field

\[
u(x,T)=\sum_{k\in K_M}\widehat u_k(T)e^{ik\cdot x},
\]

define the real harmonic measurement

\[
\boxed{
Q_{k_0,\phi}(T)
=
\frac{1}{(2\pi)^3}
\int_{[0,2\pi]^3}
 u(x,T)\cos(k_0\cdot x+\phi)\,dx.
}
\]

Using

\[
\cos(k_0\cdot x+\phi)
=
\frac12
\left(
 e^{i(k_0\cdot x+\phi)}
+
 e^{-i(k_0\cdot x+\phi)}
\right),
\]

Fourier orthogonality gives

\[
\boxed{
Q_{k_0,\phi}(T)
=
\frac12
\left(
\widehat u_{-k_0}(T)e^{i\phi}
+
\widehat u_{k_0}(T)e^{-i\phi}
\right).
}
\]

For a real field,

\[
\widehat u_{-k_0}=\overline{\widehat u_{k_0}},
\]

so the readout is real up to floating-point roundoff.

The terminal support is therefore exactly

\[
\boxed{
S_Q=\{k_0,-k_0\},
\qquad |S_Q|=2.
}
\]

This is a physical-space weighted volume measurement, not a single complex Fourier coefficient.

---

## 2. Exact triad dependency operator

For any retained mode set \(S\subseteq K_M\), define

\[
\boxed{
D(S)
=
S\cup
\{p,q\in K_M:\ p+q=k\text{ for some }k\in S\}.
}
\]

This is a dependency pullback forced by the quadratic Navier--Stokes convolution. It is not a closure model.

For one classical RK4 step with terminal support \(S_Q\), the exact stage requirements are

\[
\boxed{K_4=S_Q,}
\]

\[
\boxed{K_3=D(K_4),}
\]

\[
\boxed{K_2=D(K_3),}
\]

\[
\boxed{K_1=D(K_2),}
\]

and the exact input requirement is

\[
\boxed{S_{\rm in}=D(K_1).}
\]

If the retained state agrees with the full finite Galerkin state on \(S_{\rm in}\), then stage induction gives equality on \(K_1,K_2,K_3,K_4\), and therefore

\[
\boxed{
Q_{k_0,\phi}^{\rm retained}(T)
=
Q_{k_0,\phi}^{\rm full}(T)
}
\]

for the same fixed finite RK4 recurrence, up to arithmetic roundoff.

---

## 3. Corner-probe finite witness

For the finite cube

\[
K_M=\{-3,\ldots,3\}^3\setminus\{0\},
\]

there are

\[
|K_M|=342
\]

retained Fourier modes.

For the corner harmonic probe

\[
\boxed{k_0=(3,3,3),}
\]

the checker obtains the one-step RK4 cone

\[
\boxed{
|K_1|=342,
\qquad
|K_2|=342,
\qquad
|K_3|=126,
\qquad
|K_4|=2.
}
\]

Thus the terminal reader occupies only

\[
\boxed{
\frac{2}{342}\approx0.00585
}
\]

of the retained modes, while its exact nonlinear dependence expands gradually rather than saturating after the first pullback as the plane-average reader does.

For the declared ordered-triad work count, the same finite case gives approximately

\[
\boxed{
G_{\rm structural}\approx1.658
}
\]

for one RK4 step.

This is a structural work count, not a universal wall-clock speed-up theorem.

---

## 4. Segmented fused-triad kernel

The original fused kernel accumulates ordered triad contributions with

```python
np.add.at(...)
```

The harmonic checker additionally evaluates a segmented accumulation using

```python
np.add.reduceat(...)
```

because the compiled triads are contiguous by output mode.

If the ordered contributions for output \(k_j\) form a contiguous segment \(\mathcal S_j\), both kernels compute the same sum

\[
\boxed{
N_{k_j}
=
\sum_{r\in\mathcal S_j} c_r.
}
\]

The checker therefore treats segmented accumulation as an implementation transformation of the same finite ordered-triad sum, not as a new physical equation.

The finite diagnostic verifies both

\[
\boxed{
\|F_{\rm segmented}-F_{\rm original}\|_\infty
\le10^{-12}
}
\]

and

\[
\boxed{
\|F_{\rm segmented}-F_{\rm FFT}\|_\infty
\le10^{-12}
}
\]

on the tested finite cubes before reporting timing.

---

## 5. Comparison with the exact plane-average reader

The plane-average terminal support is sparse,

\[
|A_x|=2K,
\]

but the separate theorem in `NS_PHYSICAL_PLANE_AVERAGE.md` proves

\[
\boxed{D(A_x)=K_M.}
\]

Hence sparsity of the terminal reader alone does not determine acceleration.

The harmonic example shows that the relevant object is the growth of the entire backward dependency cone:

\[
\boxed{
S_Q
\longrightarrow
D(S_Q)
\longrightarrow
D^2(S_Q)
\longrightarrow\cdots.
}
\]

Two readers with similarly small terminal output dimension can have very different retained computational cost.

---

## 6. Claim boundary

Established here / by the executable checker:

- exact physical harmonic-reader identity for the fixed finite Fourier representation;
- exact two-mode terminal support;
- exact RK4 dependency pullback rule;
- finite cone sizes for the tested cubes;
- finite retained/full task agreement to the declared numerical gate;
- finite equivalence of the segmented and original ordered-triad accumulation to the declared numerical gate.

Not established:

- that corner probes are globally optimal among all physical readers;
- a universal speed-up factor;
- exact-in-time continuum Navier--Stokes evolution;
- any resolution of the Millennium Prize problem.

The optimization question suggested by this result is recorded separately in
`NS_READOUT_DESIGN_ACCELERATION.md`.
