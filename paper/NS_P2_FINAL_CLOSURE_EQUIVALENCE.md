# NS P2 final closure — finite-observation contraction is regularity-equivalent

**Date:** 2026-09-11  
**Status:** `DERIVED` phase-closure theorem under the declared modal finite-observation adapter.  
**Claim boundary:** this closes P2 as a research/reduction phase. It does **not** prove Clay Navier–Stokes global regularity.

## 1. Purpose

P2 and P2B reduced the finite-first Navier–Stokes programme to progressively sharper regularity-sensitive statements. The last surviving P2B target was

`NS-P2B-SCALE-CONTRACTION-UNIFORM`.

This note audits its non-vacuity. The conclusion is that, in the declared periodic modal/dyadic setting, the **existence** of the strict scale-contraction certificate is equivalent to regularity on the finite time interval. Therefore it is not a weaker bridge theorem waiting to be proved before regularity; it is a reformulation of the regularity target.

The constructive requirement "produce the certificate from finite/checkable information without assuming regularity" is stronger than the existential statement and remains a possible future direct attack, but it is not a residual P2 bridge that can be promoted as progress without new Clay-strength mathematics.

## 2. External adapter used only as the semantic implication

Balakrishna–Biswas (Research in the Mathematical Sciences 12, 46 (2025)) proves a regularity criterion for periodic 3D Navier–Stokes based on finitely many observations. In the modal case the observed field is the low-mode projection. Their Theorem 4.8 gives the time-window criterion used by P2B; their Theorems 4.5/4.6 and discussion establish necessary-and-sufficient finite-observation criteria for regularity in the corresponding type-I/modal setting.

P2B uses the alternate time-window quantity

\[
K_N(u)
:=\sup_t
\left(\int_t^{t+\tau_0}\|P_Nu(s)\|_{H^1}^{2p}\,ds\right)^{1/(2p)},
\qquad p>2.
\]

For the present closure theorem, only the following published implication is required:

\[
\text{finite-observation gate at one finite modal scale}
\Longrightarrow
\text{regularity on }[0,T].
\]

No unproved external statement is used in the reverse direction below.

## 3. Dyadic modal normalization

Take dyadic modal scales

\[
N_j=2^jN_0,
\]

and let `Lambda_j` denote the corresponding retained Stokes scale. Under the standard periodic modal normalization there is a fixed positive constant `c_Lambda` such that

\[
\Lambda_j=c_{\Lambda}N_j^2,
\qquad
\Lambda_{j+1}=4\Lambda_j.
\]

Set

\[
r:=\frac{2p}{p-2}>1
\]

and define the dimensionless P2B critical ratio

\[
\boxed{
R_j:=\frac{(K_{N_j}(u)^2)^r}{\Lambda_j}.
}
\]

The P2B finite-observation gate is eventually satisfied whenever `R_j -> 0`, because all remaining unforced initial-data terms are fixed in `j` while the admissible right-hand side grows proportionally to `Lambda_j`.

## 4. Scale-contraction property

Define `SC(T)` to mean that there exist

\[
j_0<\infty,
\quad 0\le\kappa<1,
\quad 0\le\rho<1,
\quad B<\infty,
\]

and finite nonnegative upper certificates `U_j` for every `j>=j0` such that

\[
R_j\le U_j
\]

and

\[
\boxed{
U_{j+1}\le\kappa U_j+B\rho^j.
}
\]

This is the existential mathematical core of `NS-P2B-SCALE-CONTRACTION-UNIFORM`.

## 5. Theorem `NS-P2-FINAL-EQUIV`

Under the declared periodic modal/dyadic setup and the published finite-observation regularity adapter, for a Leray–Hopf solution with admissible smooth initial datum on a finite interval `[0,T]`,

\[
\boxed{
\text{regularity on }[0,T]
\iff
SC(T).
}
\]

### Direction A — regularity implies strict scale contraction

Assume regularity on `[0,T]`. Then

\[
M_T:=\|u\|_{L^\infty(0,T;H^1)}<\infty.
\]

Since `P_N` is an `H^1`-contractive spectral projection,

\[
\|P_Nu(t)\|_{H^1}\le M_T.
\]

Therefore every time window obeys

\[
K_N(u)^2
\le
\tau_0^{1/p}M_T^2.
\]

Raising to `r=2p/(p-2)` gives a cutoff-independent constant

\[
C_T^*:=
\left(\tau_0^{1/p}M_T^2\right)^r<\infty
\]

such that

\[
R_j\le\frac{C_T^*}{\Lambda_j}.
\]

Choose

\[
U_j:=\frac{C_T^*}{\Lambda_j}.
\]

Because `Lambda_{j+1}=4 Lambda_j`,

\[
\boxed{
U_{j+1}=\frac14 U_j.
}
\]

Thus `SC(T)` holds with

\[
\kappa=\frac14,
\qquad B=0,
\]

and arbitrary `0<=rho<1`.

This direction uses only the definition of regularity and spectral projection monotonicity.

### Direction B — strict scale contraction implies regularity

Assume `SC(T)`. Iterating

\[
U_{j+1}\le\kappa U_j+B\rho^j,
\qquad \max\{\kappa,\rho\}<1,
\]

shows

\[
U_j\to0.
\]

Hence

\[
0\le R_j\le U_j\to0.
\]

In the unforced P2B modal adapter, divide the finite-observation inequality by the modal scale `Lambda_j` (equivalently by `h_j^{-2}` up to a fixed normalization). The observation-dependent contribution is a fixed positive adapter constant times `R_j`, while the initial-data and lowest-eigenvalue contributions are fixed in `j` divided by `Lambda_j`. Consequently every normalized left-hand contribution tends to zero, while the normalized admissible right-hand threshold is a fixed positive constant.

Therefore there exists a finite `j_*` for which the published finite-observation gate is satisfied. The adapter then yields regularity of `u` on `[0,T]`.

Thus

\[
SC(T)\Longrightarrow\text{regularity on }[0,T].
\]

Combining both directions proves the equivalence.

## 6. Consequence for the P2 programme

The last P2B residual cannot honestly be advertised as a separate lower-strength bridge:

```text
strict all-scale contraction
        <=>
regularity on the target finite interval
```

at the existential theorem level.

Therefore a proof of `NS-P2B-SCALE-CONTRACTION-UNIFORM` that simply postulates or derives `U_j` using information equivalent to a uniform regularity bound would violate the programme's non-vacuity rule.

The only potentially new direction would be an **effective finite constructor** producing the contraction certificates from weaker finite information. Such a constructor would itself constitute new regularity-level mathematics. It is not supplied by IDM, Readout Genesis, Readout Universe, the existing NS finite accounting, or the published finite-observation theorem.

## 7. Final P2 ruling

```text
P2 = CLOSED AS A RESEARCH / REDUCTION PHASE
P2B finite-observation route = CLOSED AS REGULARITY-EQUIVALENT
NS-P2-H3-MARGIN-UNIFORM = no longer an active separate bridge target
NS-P2B-SCALE-CONTRACTION-UNIFORM = regularity-equivalent existentially
Clay Navier-Stokes global regularity = OPEN
```

All previously derived finite certificates, no-go controls, EPSC lifts, and scale-contraction algebra remain valid supporting mathematics. They do not combine into an unconditional global-regularity proof.

## 8. Anti-reopening rule

Do not reopen P2 merely by replacing regularity with another criterion known or proved to be necessary and sufficient for regularity. A new NS lane must demonstrate one of the following before being treated as a genuine bridge advance:

1. a premise strictly weaker than known regularity criteria together with a new implication to regularity;
2. a constructive finite theorem whose hypotheses are independently verifiable without a regularity oracle;
3. a counterexample or structural theorem that changes the known regularity frontier.

Otherwise record the proposal as `REGULARITY-EQUIVALENT / HOLD`, not as an open intermediate bridge.
