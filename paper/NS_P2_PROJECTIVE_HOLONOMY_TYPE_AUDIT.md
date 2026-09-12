# NS P2 — Projective-Holonomy Type Audit and Three-Line Rigidity

**Status:** TYPE AUDIT + NEW DERIVATION / PROPOSAL; exact finite projective lemma  
**Parent:** `NS_P2_PLANE_SWITCH_NORMAL_LINEAGE.md`; Standalone Sections 113–114  
**Global FNW / OCSR / Witness Soundness / G6/G7:** OPEN  
**Clay Navier–Stokes regularity:** OPEN  
**Checker:** `reproduction/checks/check_ns_p2_projective_three_line_rigidity.py`

## 0. Reuse-first ruling

Standing rule:

```text
Toledo lookup -> Genesis compatibility -> reuse existing object -> derive only the missing piece -> mark PROPOSAL
```

The repository already contains substantial holonomy machinery. This note first separates two different typed objects that must not be silently identified.

### Type P — projective polarization-line holonomy

Standalone Sections 113–114 treat null interactions as projective transports

\[
T_e:\mathbb P(k_1^\perp)\to\mathbb P(k_2^\perp),
\]

with recurrent-loop condition

\[
\boxed{T_{\rm loop}(\lambda)=\lambda.}
\]

This acts on projective polarization / lineage classes.

### Type Phi — complex scalar phase-incidence holonomy

The existing complex/dyadic holonomy and packing notes use scalar Fourier-channel phases. A declared incidence cycle may carry a target mismatch `Delta=pi`, giving the exact local phase tax and, after finite fractional packing,

\[
\boxed{\sum_eT_e\le\sum_eA_e-c_0P,\qquad c_0=1-1/\sqrt2.}
\]

This acts on complex scalar channel phases and amplitudes.

These are not the same object. No existing Toledo/Genesis/NS theorem found in the reuse-first lookup identifies Type P holonomy with Type Phi holonomy.

Therefore the following inference is forbidden unless a separate channel-realization/coverage theorem is proved:

```text
nontrivial projective polarization holonomy
    -> complex phase-incidence pi cycle
    -> packed phase tax.
```

This audit prevents a type drift at the current FNW entrance.

## 1. Existing plane-switch reconstruction feeds Type P only

The current exact plane-switch identity is

\[
 n_j\times n_{j+1}
 =\Delta_j c_{j+1},
\qquad
\Delta_j=\det[c_j,c_{j+1},c_{j+2}].
\]

For a genuine switch `Delta_j != 0`,

\[
\boxed{[c_{j+1}]=[n_j\times n_{j+1}].}
\]

This reconstructs a retained projective lineage class from adjacent rank-2 plane normals. It therefore supplies data for Type P transport / FNW. By itself it does not construct a Type Phi conflict cycle.

## 2. Exact three-line projective rigidity

Let

\[
M\in PGL(2,\mathbb R)
\]

be the projective monodromy of a closed Type P transport loop on one reanchored two-dimensional polarization fiber.

Suppose the loop returns three distinct future-relevant projective lineage classes

\[
[\ell_1],\ [\ell_2],\ [\ell_3]\in\mathbb P^1
\]

and preserves each one:

\[
M[\ell_i]=[\ell_i],\qquad i=1,2,3.
\]

Then

\[
\boxed{M=I\quad\text{in }PGL(2,\mathbb R).}
\tag{PH-1}
\]

### Proof

Conjugate the first two distinct fixed classes to

\[
[1:0],\qquad[0:1].
\]

A linear representative preserving both lines is diagonal:

\[
\widetilde M=\begin{pmatrix}a&0\\0&d\end{pmatrix}.
\]

The third distinct line can be represented as `[1:t]` with `t != 0`. Projective fixation requires

\[
(a,dt)=\lambda(1,t).
\]

Hence `a=lambda` and, since `t != 0`, `d=lambda=a`. Therefore

\[
\widetilde M=aI,
\]

which is the identity in `PGL(2,R)`.

The exact checker verifies this reduction and also verifies that a nonidentity diagonal projective map may fix two distinct lines but not a generic third line.

### Status

`PROP-P3-PROJECTIVE-THREE-LINE-RIGIDITY-01` — **NEW DERIVATION / PROPOSAL; exact finite PASS**.

## 3. Consequence for the nonidentity-monodromy branch

A nonidentity Type P monodromy can preserve at most two distinct recurrent lineage classes:

\[
\boxed{
M\ne I
\Longrightarrow
\#\operatorname{Fix}_{\mathbb P^1}(M)\le2.
}
\tag{PH-2}
\]

Therefore any productive zero-defect recurrent branch with nonidentity projective monodromy must prevent a third distinct future-relevant lineage class from returning to the same reanchored fiber.

That prevention must be accounted for by existing Genesis/Readout channels:

```text
registered resolution / terminalization
OR exit
OR named translation / lineage defect
OR collapse of generated lineage into one of the <=2 fixed classes
OR failure to generate a third future-relevant class.
```

This is a finite rigidity statement about the projective return map. It is not yet FNW.

## 4. Identity monodromy remains the hard branch

(PH-1) does **not** exclude recurrence when

\[
M=I.
\]

Indeed identity projective monodromy fixes every lineage class. Therefore the exact projective classification now splits the FNW entrance into

\[
\boxed{
\text{nonidentity monodromy}
\Rightarrow
\text{at most two returned projective lineage classes},
}

and

\[
\boxed{
\text{identity monodromy}
\Rightarrow
\text{requires separate productive fixed-web rigidity}.}
\]

This matches the existing Genesis strategy: exclude retained novelty on nonidentity return first; treat identity-monodromy productive recurrence as the real equality case.

## 5. Where the existing Type Phi holonomy machinery re-enters

The repository already has an exact gauge-aware phase-holonomy/cut route:

```text
shared-mode frame mismatch / frame-compatible dyadic conflict cycle
    -> declared four-channel pi cycles
    -> finite fractional packing
    -> strict packed tax OR small weighted hitting cut
    -> time-window version without phase-persistence assumption.
```

Those results should be reused verbatim once an actual full-convolution channel web has been shown to contain the corresponding Type Phi cycle family.

The current missing bridge is therefore not another packing theorem. It is the typed realization/coverage statement

\[
\boxed{
\text{Type P recurrent lineage / plane-switch web}
\longrightarrow
\text{actual registered full-convolution channel network}
\longrightarrow
\text{Type Phi conflict-cycle coverage or classified remainder}.
}
\tag{PH-3}
\]

`(PH-3)` is **OPEN**.

## 6. Exact routing obligations for the coverage audit

For each proposed recurrent plane-switch/basis-replacement loop, the next audit must:

1. attach a concrete Fourier-mode address and registered event ancestry to every retained lineage class;
2. expand the actual full-convolution scalar channels of those events;
3. compute the existing shared-mode projective frame dispersion `D_p`;
4. if `D_p>0`, route the corresponding weighted incident pairs to the already-derived frame-mismatch frustration/cut machinery;
5. if `D_p=0`, use the existing same-plane / orthogonal-turn trichotomy;
6. on frame-compatible 3D sectors, search the existing frame-compatible four-channel `pi` cycle catalogue;
7. if no declared conflict cycle occurs, classify the exact remainder instead of calling it harmless.

Known remainder facts that must be reused:

- same-plane support belongs to the planar/2D3C regular branch;
- cycle-free fresh-donor transfer can remain dyadic and H1-nondegenerate, so `no cycle -> weak` is REFUTED;
- the fresh-donor selected tree is not dynamically closed: consecutive donors generate off-tree interactions;
- donor overlap on a time window pays an exact response-or-cancellation charge;
- sufficiently large high-frequency donors have recent nonlinear ancestry rather than free Stokes memory.

Thus the conflict-poor remainder is a **recursive response/cancellation/ancestry problem**, not a missing phase-packing lemma.

## 7. Sharpened current frontier

The correct current attack vector is

\[
\boxed{
\begin{aligned}
\text{recurrent plane-switch / lineage candidate}
&\to \text{typed event realization}\\
&\to \text{gauge-robust channel coverage}\\
&\to
\begin{cases}
\text{packed Type Phi holonomy tax},\\
\text{small hitting cut + conflict-poor remainder},\\
\text{planar / degenerate / exit branch},\\
\text{UNRESOLVED if realization/coverage fails}.
\end{cases}
\end{aligned}}
\]

For Type P itself:

\[
\boxed{
\text{three distinct recurrent lineage classes}
\Rightarrow
M=I.
}
\]

So the next genuinely new mathematical targets are only:

```text
A. third-line generation/return on the nonidentity Type-P branch;
B. identity-monodromy productive-web rigidity;
C. Type-P -> actual-channel coverage / conflict-poor remainder control.
```

No new holonomy architecture is needed.

## 8. Claim boundary

Still OPEN:

- Type-P lineage web -> Type-Phi conflict-cycle coverage;
- third distinct future-relevant lineage generation/return in every productive nonidentity recurrent web;
- identity-monodromy productive-web rigidity;
- recursive non-overcounting of response/cancellation channels in the fresh-donor remainder;
- FNW / OCSR / Witness Soundness;
- G4 / G6 / G7;
- Clay Navier–Stokes regularity.
