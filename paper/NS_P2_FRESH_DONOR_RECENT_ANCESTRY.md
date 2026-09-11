# NS P2 — high fresh donors must have recent nonlinear ancestry

**Date:** 2026-09-11  
**Parent structural target:** `NS-P2-FRUSTRATION-OR-CUT` — **OPEN**  
**Uses:** `NS-FUB-A1-STOKES-H3-TAIL` — **DERIVED** in `paper/NS_FUB_A1_STOKES_NONLINEAR_TAIL_SPLIT.md`.  
**Checker:** `reproduction/checks/check_ns_p2_fresh_donor_recent_ancestry.py`

## 1. Why this closes a conceptual escape

The exact fresh-donor selected tree showed that one can write a phase-SAT dyadic channel chain if a new donor mode is simply available at every higher scale.

For the actual unforced NSE with smooth finite-energy initial data, high-frequency donors are not an external resource.  At positive time they decompose into

```text
positive-lag Stokes memory
+
recent nonlinear Duhamel transfer.
```

The repository already proves an all-scale high-frequency envelope for the positive-lag Stokes memory.  Therefore any donor whose H1 amplitude is appreciably larger than that envelope must have been created by the recent nonlinear window.

This does not yet control that recent ancestry, but it removes the interpretation of the conflict-free tree as a chain supplied by arbitrarily large free high-frequency donors.

---

## 2. Existing Stokes memory theorem

For every `delta>0`, the existing theorem gives

\[
\|Q_Ne^{\nu\delta\Delta}f\|_{H^3,F}^2
\le
\frac{192}{(2\nu\delta)^4(N+1)^2}\|f\|_{L^2,F}^2.
\]

Hence

\[
\boxed{
\|Q_Ne^{\nu\delta\Delta}f\|_{H^3,F}
\le
\frac{8\sqrt3}{(2\nu\delta)^2(N+1)}\|f\|_{L^2,F}.
}
\]

Since coefficient-weighted `H1,F` is dominated by `H3,F`, the same right-hand side bounds the H1 tail.

For an unforced Leray/strong solution on an interval where the mild identity is valid, the energy inequality gives

\[
\|u(t-\delta)\|_{L^2,F}\le \|u_0\|_{L^2,F}=:M_0.
\]

Therefore, for every `t>=delta`, define

\[
\boxed{
\varepsilon_{N,\delta}
:=
\frac{8\sqrt3\,M_0}
{(2\nu\delta)^2(N+1)}.
}
\]

Then

\[
\boxed{
\|Q_Ne^{\nu\delta\Delta}u(t-\delta)\|_{H^1,F}
\le\varepsilon_{N,\delta}.
}
\]

### Status

`NS-P2-FRESH-DONOR-STOKES-MEMORY-H1-TAIL` — **DERIVED** by direct specialization of the existing Stokes H3 tail theorem plus `H1<=H3` and the energy inequality.

---

## 3. Exact recent-ancestry decomposition for one donor coordinate

The positive-lag mild identity is

\[
u(t)=e^{\nu\delta\Delta}u(t-\delta)
-
\int_{t-\delta}^{t}
 e^{\nu(t-s)\Delta}\mathbb P\,\operatorname{div}(u\otimes u)(s)\,ds.
\]

Let `q` be any mode outside the cube cutoff `[-N,N]^3`, and let `X_q(t)` be one physical inhomogeneous H1 scalar polarization coordinate.

Write

\[
X_q(t)=M_q^{(\delta)}(t)+Y_q^{(\delta)}(t),
\]

where `M_q^(delta)` is the Stokes-memory coordinate and `Y_q^(delta)` is the recent nonlinear Duhamel coordinate.

The total tail estimate gives

\[
|M_q^{(\delta)}(t)|\le\varepsilon_{N,\delta}.
\]

Therefore the reverse triangle inequality yields

\[
\boxed{
|Y_q^{(\delta)}(t)|
\ge
\bigl(|X_q(t)|-\varepsilon_{N,\delta}\bigr)_+.
}
\]

### Status

`NS-P2-FRESH-DONOR-RECENT-ANCESTRY` — **DERIVED**.

---

## 4. Large donor implies a fixed recent fraction

If

\[
|X_q(t)|\ge 2\varepsilon_{N,\delta},
\]

then

\[
\boxed{
|Y_q^{(\delta)}(t)|\ge\frac12|X_q(t)|.
}
\]

More generally, for any `theta in (0,1)`, if

\[
|X_q(t)|\ge\frac{1}{1-\theta}\varepsilon_{N,\delta},
\]

then

\[
|Y_q^{(\delta)}(t)|\ge\theta|X_q(t)|.
\]

### Status

`NS-P2-FRESH-DONOR-LARGE-IMPLIES-RECENT` — **DERIVED**.

---

## 5. Application to the self-similar fresh-donor pair

For the block at scale `n`,

\[
q_0=n(1,0,1),
\qquad
q_1=n(2,0,-1).
\]

Both modes lie outside the cube `[-(n-1),n-1]^3`.  Choosing

\[
N=n-1
\]

gives the common Stokes-memory envelope

\[
\boxed{
\varepsilon_{n,\delta}^{\rm donor}
=
\frac{8\sqrt3\,M_0}
{(2\nu\delta)^2 n}.
}
\]

Thus, at any time `t>=delta`, if both donor coordinates satisfy

\[
|X_{q_0}(t)|,\ |X_{q_1}(t)|
\ge2\varepsilon_{n,\delta}^{\rm donor},
\]

then each donor has at least half of its H1 amplitude supplied by the recent nonlinear Duhamel window.

The fresh-donor tree therefore cannot be interpreted at high scale as a large donor chain carried only by positive-lag linear memory.

### Status

`NS-P2-FRESH-DONOR-PAIR-RECENT-ANCESTRY` — **DERIVED**.

---

## 6. Combination with the donor window charge

The companion window-charge theorem gives the exact all-scale interaction inequality

\[
\frac1{\sqrt2}|X_{q_0}X_{q_1}|
\le
|D_r|+|R_r|,
\qquad r=q_0+q_1.
\]

The present lemma says that whenever both donors are above their explicit `O(1/n)` memory threshold, both donors themselves are substantially recent-nonlinear objects.

Hence the conflict-poor branch has been reduced to a recursive recent-nonlinear statement:

\[
\boxed{
\text{large consecutive high-scale donors}
\Longrightarrow
\text{recent nonlinear ancestry for both donors}
+
\text{response/cancellation charge for their interaction}.
}
\]

This is the form needed for the next attack on recursive cancellation/ancestry closure.

---

## 7. Claim boundary

The theorem does **not** yet prove that the recent nonlinear ancestry is small.  In fact `NS_FUB_A1_STOKES_NONLINEAR_TAIL_SPLIT.md` already identifies the recent nonlinear window as the load-bearing part where bare heat-semigroup smoothing is insufficient.

Therefore the exact frontier is now

```text
positive-lag donor memory                                  controlled / decays O(1/n)
large fresh donor                                          -> recent nonlinear ancestry DERIVED
consecutive donor overlap                                  -> response/cancellation charge DERIVED
recursive recent-nonlinear ancestry/cancellation closure   OPEN
recent nonlinear window -> K_N contraction                OPEN
constructive R_j recurrence                               OPEN
NS-P2-FRUSTRATION-OR-CUT                                  OPEN
NS-P2B-SCALE-CONTRACTION-UNIFORM                          OPEN
Clay Navier-Stokes regularity                             OPEN
```

This is not a new regularity criterion.  It removes a specific free-donor escape from the constructive P2 mechanism and points the remaining proof obligation back to the already identified recent nonlinear transfer term.
