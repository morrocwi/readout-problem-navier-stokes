# NS P2 — all-n dyadic complex phase holonomy

**Date:** 2026-09-11  
**Parent target:** `NS-P2-FRUSTRATION-OR-CUT` — **OPEN**  
**Checker:** `reproduction/checks/check_ns_p2_dyadic_phase_holonomy_alln.py`

## Result

A direct exact Fourier–Leray search produces a stronger complex phase-holonomy family in which **every declared channel crosses the dyadic max-frequency boundary**.

For every integer `n>=1`, take

\[
p=(0,0,n),\qquad q=(n,-n,n),\qquad k=(n,-n,2n),
\]

so

\[
p+q=k,
\qquad |p|_\infty=|q|_\infty=n,
\qquad |k|_\infty=2n.
\]

Use the same unnormalised real divergence-free basis convention as the other P2 symbolic checkers and the four polarization channels

\[
\begin{aligned}
A:\;&p/e_1+q/e_1\to k/e_1,\\
B:\;&p/e_1+q/e_2\to k/e_1,\\
C:\;&p/e_1+q/e_1\to k/e_2,\\
D:\;&p/e_1+q/e_2\to k/e_2.
\end{aligned}
\]

For a scalar channel `p+q=k`, the Fourier–Leray coefficient is derived from the actual convection tensor and the channel contribution has the form

\[
\dot z_k=-ic_\tau z_pz_q,
\]

hence

\[
\frac{d}{dt}|z_k|^2
=2c_\tau\operatorname{Im}(z_pz_q\overline{z_k}).
\]

The exact coefficients are

\[
\boxed{
c_A=-\frac{n^2}{5},\qquad
c_B=+\frac{3n^3}{5},\qquad
c_C=-\frac{n}{15},\qquad
c_D=-\frac{7n^2}{15}.
}
\]

All are nonzero for every integer `n>=1`.

## Exact holonomy obstruction

For each channel let its phase row be

\[
r_\tau:\quad \phi_p+\phi_q-\phi_k.
\]

The four incidence rows satisfy

\[
\boxed{
r_A-r_B-r_C+r_D=0.
}
\]

Outward saturation requests target phases `sign(c_tau)*pi/2`, therefore the four targets in quarter-turn units are

\[
(-1,+1,-1,-1).
\]

Applying the same row relation to the targets gives

\[
-1-(+1)-(-1)+(-1)=-2,
\]

that is,

\[
-\pi\not\equiv0\pmod{2\pi}.
\]

Therefore

\[
\boxed{
\text{no complex phase assignment can saturate all four }n\to2n\text{ channels simultaneously}.
}
\]

This is an exact complex shared-mode/shared-polarization obstruction in actual Fourier–Leray channels, not the earlier four-real-monomial sign artifact.

### Status

`NS-P2-DYADIC-COMPLEX-HOLONOMY-ALLN` — **DERIVED**, with an exact symbolic checker returning PASS for the encoded identities.

## Quantitative tax

Let `Theta_i^*` be each maximizing target and let

\[
\varepsilon_i=\Theta_i-\Theta_i^*.
\]

The holonomy relation forces

\[
\varepsilon_A-\varepsilon_B-\varepsilon_C+\varepsilon_D
\equiv\pi\pmod{2\pi}.
\]

Hence at least one channel has circular phase error

\[
\boxed{
\max_i\operatorname{dist}_{\mathbb T}(\Theta_i,\Theta_i^*)\ge\frac{\pi}{4}.
}
\]

Writing the available amplitude prefactor of channel `i` as `A_i>=0`, its outward contribution is

\[
T_i=A_i\cos\varepsilon_i.
\]

Therefore

\[
\boxed{
\sum_iT_i
\le
\sum_iA_i
-
\left(1-\frac1{\sqrt2}\right)\min_iA_i.
}
\]

For any threshold `lambda>0` this yields the local dichotomy:

```text
min_i A_i <= lambda
    -> amplitude cut

min_i A_i > lambda
    -> strict phase-frustration tax > (1-1/sqrt(2))*lambda
```

### Status

`NS-P2-DYADIC-LOCAL-FRUSTRATION-OR-CUT` — **DERIVED**.

## H3-normalized scale dependence

With scalar-coordinate inhomogeneous `H^3` weight

\[
W_{k,s}=|h_{k,s}|^2(1+|k|^2)^3,
\]

the four normalized output-production coefficient magnitudes share the exact factor

\[
F_n=
\frac{n(6n^2+1)^{3/2}}
{(n^2+1)^{3/2}(3n^2+1)^{3/2}},
\]

with

\[
\Gamma_A=\frac{\sqrt{10}}5F_n,
\quad
\Gamma_B=\frac{\sqrt{30}}5F_n,
\quad
\Gamma_C=\frac{2\sqrt{15}}{15}F_n,
\quad
\Gamma_D=\frac{14\sqrt5}{15}F_n.
\]

In particular,

\[
F_n\sim\frac{2\sqrt2}{n^2}.
\]

Thus the geometry is explicit: the local normalized coupling itself carries `n^{-2}` scaling. Any cutoff-independent contraction claim must therefore combine the holonomy tax with the scale-critical amplitude/flux normalization rather than silently treating the local coefficient as uniform.

## Claim boundary

This advances FW-2/FW-3/FW-4 from the P2 handoff:

```text
actual Fourier-Leray network
  -> exact all-n phase holonomy
  -> genuine dyadic n -> 2n crossing
  -> pi/4 angular deficit
  -> local frustration-or-cut tax
```

It does **not** prove a boundary coverage theorem. A critical-flux state may concentrate on channels outside this motif, on phase-satisfiable sparse/tree-like subnetworks, or on configurations where one motif amplitude prefactor is small.

Therefore the parent theorem remains

```text
NS-P2-FRUSTRATION-OR-CUT — OPEN
```

and no regularity/Clay claim changes status.

## Next load-bearing target

The next theorem is now sharply localized:

\[
\boxed{
\text{critical dyadic boundary flux}
\Longrightarrow
\text{positive weighted coverage by taxed holonomy motifs}
\ \text{or}\
\text{a quantitative amplitude/geometry remainder}.
}
\]

The next checker should enumerate exact boundary-crossing channels, classify symmetry/orbit shapes, and test whether high-weight channels can avoid all holonomy cycles by concentrating on a phase-satisfiable forest. A SAT forest is a useful counterexample to over-broad coverage; an unavoidable cycle cover would be the route toward the parent theorem.
