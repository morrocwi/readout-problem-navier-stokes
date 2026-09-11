# NS P2 — time-window holonomy packing without phase-switching loss

**Date:** 2026-09-11  
**Parent target:** `NS-P2B-SCALE-CONTRACTION-UNIFORM` — **OPEN**  
**Structural parent:** `NS-P2-FRUSTRATION-OR-CUT` — **OPEN**  
**Checker:** `reproduction/checks/check_ns_p2_holonomy_window_packing.py`

## 1. Purpose

The P2 handoff identified temporal phase switching as a possible escape:

```text
at one time edge e1 is phase-frustrated,
then the network switches,
and later a different edge is frustrated.
```

For a fixed declared family of exact holonomy cycles, the non-overcounted packing theorem makes that particular escape unnecessary to track edge-by-edge.

The reason is simple but load-bearing: the aggregate packing tax is **pointwise in time**.  It can therefore be integrated before identifying which edge pays the tax.

---

## 2. Pointwise input

At each time `t`, let

\[
A_e(t)\ge0
\]

be the channel amplitude prefactors, let

\[
S(t)=\sum_eA_e(t),
\]

and run the exact fractional packing construction on the declared four-channel `pi`-holonomy cycle family to obtain packed mass

\[
P(t)\ge0.
\]

The packing theorem gives, pointwise,

\[
\boxed{
T(t):=\sum_eT_e(t)
\le
S(t)-c_0P(t),
}
\]

where

\[
\boxed{c_0=1-1/\sqrt2.}
\]

No statement here fixes which member of a cycle has phase error at least `pi/4`; that edge may change arbitrarily with time.

---

## 3. Exact window integration

Let `I=[t_0,t_1]` be any finite observation window on which the quantities are integrable.  Define

\[
S_I=\int_I S(t)\,dt,
\qquad
P_I=\int_I P(t)\,dt,
\qquad
T_I=\int_I T(t)\,dt.
\]

Integrating the pointwise inequality gives

\[
\boxed{
T_I\le S_I-c_0P_I.
}
\]

This step uses no phase-velocity estimate, no persistence of one frustrated edge, and no bound on the switching frequency.

### Status

`NS-P2-HOLONOMY-WINDOW-TAX` — **DERIVED**.

---

## 4. Window packing-or-cut dichotomy

Fix

\[
0<\eta<1/4.
\]

### Branch A — integrated packed mass is substantial

If

\[
P_I\ge\eta S_I,
\]

then

\[
\boxed{
T_I\le(1-c_0\eta)S_I.
}
\]

The strict factor is independent of how the identity of the frustrated edge switches in time.

### Branch B — integrated packed mass is small

If

\[
P_I<\eta S_I,
\]

run the pointwise greedy packing and let `H(t)` be its saturated hitting set.  The finite packing theorem gives

\[
A(H(t),t)\le4P(t)
\]

at each time.  Therefore

\[
\boxed{
\int_I A(H(t),t)\,dt
\le4P_I
<4\eta S_I.
}
\]

At every time, deleting `H(t)` intersects every declared conflict cycle.  Thus the time-dependent cut may switch arbitrarily, but its **total window weight** is controlled.

### Status

`NS-P2-HOLONOMY-WINDOW-PACKING-OR-CUT` — **DERIVED**.

---

## 5. What temporal switching is and is not still open

This result removes one previously stated obstacle:

```text
fast switching of which channel is phase-frustrated
    does not erase the aggregate holonomy tax.
```

Record:

`NS-P2-PHASE-SWITCHING-EVADES-PACKED-HOLONOMY-TAX` — **REFUTED**.

The refutation is specific to the aggregate packed-cycle branch.  It does **not** solve the full temporal problem, because the small-packing branch still leaves a time-dependent conflict-free remainder and a time-dependent small hitting cut.

The new frontier is therefore sharper:

\[
\boxed{
\text{small integrated packed mass}
\Longrightarrow
\text{control time-dependent conflict-free / fresh-donor remainder}.
}
\]

No separate phase-persistence theorem is needed for Branch A.

---

## 6. Connection to the finite-observation route

The observation quantity is

\[
K_N=
\sup_t
\left(
\int_t^{t+\tau_0}\|P_Nu(s)\|_{H^1}^{2p}\,ds
\right)^{1/(2p)}.
\]

The exact gauge-compatible holonomy cycle already has a cutoff-uniform physical H1 coupling floor, so a future NSE-specific coverage theorem may use its H1 channel prefactors as `A_e(t)`.

If one proves on every sufficiently high dyadic window that

\[
P_I\ge\eta S_I
\]

for one fixed `eta>0`, then the holonomy mechanism already supplies a strict time-integrated spatial factor

\[
\kappa_{hol}=1-c_0\eta<1.
\]

What is not yet proved is the adapter from this channel-envelope deficit to the required recurrence for `K_N` or `R_j`.  In the alternative branch, the fresh-donor tree counterexample shows that conflict-free remainder control must use additional dynamics rather than phase geometry alone.

---

## 7. Exact checker fixture

The checker uses several rational time cells with exact symbolic `c_0`.  In every cell it verifies

\[
T_i\le S_i-c_0P_i,
\]

then verifies exactly that summation yields

\[
\sum_iT_i\le\sum_iS_i-c_0\sum_iP_i.
\]

It also audits the integrated hitting-set estimate

\[
\sum_iH_i\le4\sum_iP_i.
\]

### Status

`NS-P2-HOLONOMY-WINDOW-FIXTURE` — **PASS**.

---

## 8. Current claim boundary

```text
pointwise non-overcounted holonomy tax                     DERIVED
window-integrated holonomy tax                            DERIVED
arbitrary edge switching does not erase packed tax        DERIVED / matching refutation
window small-packing -> small integrated hitting cut      DERIVED
conflict-free fresh-donor remainder control               OPEN
channel-envelope -> K_N / R_j contraction adapter         OPEN
constructive R_j recurrence                               OPEN
NS-P2-FRUSTRATION-OR-CUT                                  OPEN
NS-P2B-SCALE-CONTRACTION-UNIFORM                          OPEN
Clay Navier-Stokes regularity                             OPEN
```
