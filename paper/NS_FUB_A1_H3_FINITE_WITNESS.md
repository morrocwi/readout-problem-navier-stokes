# NS-FUB-A1 — H^3 Finite Galerkin Witness Decomposition

**Date:** 2026-09-11  
**Status:** theorem decomposition / bridge note. No Clay conclusion is promoted.  
**Primary issue:** `morrocwi/readout-problem-navier-stokes#25`.

## 1. Why this witness class

P2 negative controls in `morrocwi/information-discrete-math#127` rule out two weak ideas:

1. adjacent/local compatibility tending to zero does not imply all-scale convergence;
2. arbitrary global failure need not create a natural finite-prefix violation.

For Navier--Stokes, plain `L2`/energy agreement is therefore too weak to serve as the load-bearing singularity witness. The witness must be **regularity-sensitive**.

This note chooses the periodic Sobolev norm `H^3`, because `3 > 5/2` in three spatial dimensions and because the finite Fourier-Galerkin `H^3` norm is an exact finite weighted sum with integer weights.

For a finite Fourier state `v_N`, define

\[
\|v_N\|_{H^3}^2
=
\sum_{|k|_\infty\le N}
(1+|k|_2^2)^3\,|\widehat v_N(k)|^2.
\]

The finite sum is directly certifiable once the finitely many coefficient enclosures are certified.

---

## 2. Split the old NS-FUB-A1 into three statements

The old umbrella target

```text
FiniteTimeSingularity -> exists finite certified PDE-relevant failure
```

is too coarse. We split it into an existential analytic bridge, a finite verifier, and a constructive capture statement.

### NS-FUB-A1E — existential finite Galerkin exceedance bridge

Let `u` be a maximal smooth/strong periodic 3D incompressible Navier--Stokes solution on `[0,T*)`, with viscosity `nu>0`, smooth divergence-free initial data, and finite `T*`.

Assume the following standard analytic adapters explicitly:

1. **H^3 continuation adapter:** if `sup_{t<T*} ||u(t)||_{H^3} < infinity`, then the strong solution extends beyond `T*`;
2. **compact-interval Galerkin adapter:** for every `T<T*`, the standard divergence-free Fourier-Galerkin solutions `u_N` converge to `u` in `H^3`, uniformly on `[0,T]` (or in a form strong enough for the argument below).

Then

\[
\boxed{
T_*<\infty\text{ and no strong continuation}
\Longrightarrow
\forall B<\infty\;\exists N<\infty\;\exists q\in\mathbb Q,\ 0\le q<T_*:
\|u_N(q)\|_{H^3}>B.
}
\]

**Status:** DERIVED conditional on the two declared classical analytic adapters.

#### Proof route

If `||u(t)||_{H^3}` were bounded on `[0,T*)`, the continuation adapter would extend the solution, contradicting maximality. Therefore for every `B` there is a time `t0<T*` with `||u(t0)||_{H^3}` strictly above `B` by some margin.

By continuity of the strong solution in `H^3`, choose a nearby rational time `q<T*` at which the margin remains positive.

By compact-interval Galerkin convergence, choose finite `N` so that `||u_N(q)-u(q)||_{H^3}` is smaller than the remaining margin. The triangle inequality then gives `||u_N(q)||_{H^3}>B`.

The conclusion is finite-dimensional: one finite cutoff and one rational time.

### NS-FUB-A1V — exact finite verifier

Input:

- finite cutoff `N`;
- rational threshold `B>0`;
- finitely many rational interval enclosures for the real and imaginary parts of each retained Fourier velocity coefficient;
- a separate adapter assertion that the intervals really enclose the declared finite Galerkin state at the declared rational time.

The verifier computes an exact rational lower bound

\[
L_N
\le
\|u_N(q)\|_{H^3}^2
\]

by minimizing `|z|^2` over each rectangular complex interval and summing with the integer weight `(1+|k|^2)^3`.

It returns

```text
PASS iff L_N > B^2
HOLD otherwise.
```

The inequality checker is exact finite arithmetic. It does **not** itself prove that the intervals enclose the true Galerkin state; that is an adapter obligation.

**Status:** finite verifier target implemented by `reproduction/checks/check_ns_fub_a1_h3_certificate.py`; executable status comes only from CI.

### NS-FUB-A1C — constructive certified witness capture

Strengthened target:

\[
\boxed{
\mathsf{FiniteTimeSingularity}
\Longrightarrow
\text{a finite, machine-checkable A1V certificate can be constructed.}
}
\]

To prove this, the programme still needs an explicit validated adapter that can produce rational coefficient enclosures for the relevant finite Galerkin trajectory from the declared initial-data representation and viscosity, with a strict enough margin for A1V to return PASS.

**Status:** OPEN.

This separation matters: A1E is an existence theorem; A1V is a finite checker; A1C is the constructive bridge between them.

---

## 3. Non-vacuity audit

A1E imports a standard regularity continuation fact and Galerkin convergence below the putative singular time. Therefore A1E is **not** itself progress on excluding singularities. Its role is narrower: it identifies a finite-dimensional event that any singularity would force under explicit classical adapters.

The Clay-level leverage can only come from proving one of the following without assuming the desired regularity conclusion:

1. a uniform finite bound excluding A1E exceedances;
2. a validated finite recursion/tail theorem forcing such a bound;
3. another finite obstruction whose exclusion is genuinely easier than global regularity.

If the required finite premise simply restates a uniform `H^3` bound for all cutoffs and all times without a new proof mechanism, it must be marked HOLD under `PROP-FUB-06`.

---

## 4. Candidate converse bridge (A2 direction)

A clean but potentially vacuous converse template is

\[
\boxed{
\forall T<\infty\;\exists B_T<\infty\;
\forall N\;\forall t\in[0,T]:
\|u_N(t)\|_{H^3}\le B_T
\Longrightarrow
\text{a global strong solution exists on }[0,T].
}
\]

Under standard compactness/Galerkin theory this is a plausible classical bridge, but **proving the uniform bound is the hard part**. The research task is therefore not to celebrate this implication; it is to search for a finite certificate mechanism that forces the antecedent without already assuming regularity.

Status: bridge template / HOLD until a non-vacuous finite mechanism is supplied.

---

## 5. What P2 rules out for NS-FUB-A1

The following are not sufficient on their own:

- `||P_N u_M-u_N||_{L2} -> 0` only between adjacent cutoffs;
- finite energy agreement without a regularity-sensitive quantity;
- rank or observability failure of one reader;
- loss of conditioning of one inverse chart;
- a finite Galerkin discrepancy that is not connected to a continuation criterion.

Any cross-resolution ingredient used with A1 must supply an all-refinement Cauchy/tail modulus, summable envelope, or equivalent quantitative control rather than only local-step decay.

---

## 6. Next mathematical target

The immediate load-bearing question is now sharper:

> Can the repository's finite dynamics, tail accounting, and certificate recursion force a regularity-sensitive uniform bound or a summable all-scale envelope strong enough to exclude A1E exceedances, without assuming global regularity in the premise?

That question is the non-vacuous core of the NS attack after P2.
