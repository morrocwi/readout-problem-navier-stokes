# NS P2 — exact all-scale orthogonal-turn selected escape

**Date:** 2026-09-11  
**Parent target:** `NS-P2-FRUSTRATION-OR-CUT` — **OPEN**  
**Uses:** shared-mode turn trichotomy and the physical homogeneous `H1` channel normalization.  
**Checker:** `reproduction/checks/check_ns_p2_orthogonal_turn_allscale_escape.py`

## 1. Purpose

The shared-mode trichotomy reduces zero-dispersion non-planar ancestry to orthogonal plane turns.  This note red-teams the tempting shortcut

```text
orthogonal turns alone -> unavoidable phase frustration / scale loss.
```

That shortcut is false for a selected scalar channel tree.  There is an exact integer self-similar construction in which every consecutive pair of triad planes makes an orthogonal turn, the selected scalar chain is phase-SAT for every finite prefix, the physical homogeneous `H1` energy-transfer coefficient is independent of scale, and the backbone advances by more than one dyadic factor per step.

This is **not** a full invariant Navier--Stokes subsystem and does not close the parent P2 theorem.  Its role is to force the next attack onto the full NSE convolution / recent-nonlinear ancestry of the orthogonal-turn branch.

---

## 2. Integer similitude

Define

\[
A=
\begin{pmatrix}
3&0&4\\
4&0&-3\\
0&5&0
\end{pmatrix}.
\]

Direct multiplication gives

\[
\boxed{A^T A=25I},
\qquad
\boxed{\det A=125}.
\]

Hence

\[
Q:=A/5\in SO(3).
\]

So `A` is a scale-`5` orientation-preserving Euclidean similitude.

### Status

`NS-P2-ORTHOGONAL-TURN-SIMILITUDE` — **PASS** exact matrix identity.

---

## 3. Self-similar triad chain

Let

\[
p_0=e_1=(1,0,0),
\qquad
q_0=(2,4,0),
\qquad
k_0=p_0+q_0=(3,4,0)=Ae_1.
\]

For every integer `j>=0`, define

\[
\boxed{
 p_j=A^j p_0,
 \qquad
 q_j=A^j q_0,
 \qquad
 k_j=A^j k_0=p_{j+1}.
}
\]

Therefore each selected interaction is an exact integer Fourier triad

\[
\boxed{p_j+q_j=p_{j+1}}.
\]

The Euclidean lengths are exact:

\[
|p_j|=5^j,
\qquad
|q_j|=2\sqrt5\,5^j,
\qquad
|p_{j+1}|=5^{j+1}.
\]

All donors `q_j` are distinct from all backbone modes because their length ratio to `p_j` is the irrational number `2 sqrt(5)`.

### Status

`NS-P2-ORTHOGONAL-TURN-ALLSCALE-TRIADS` — **DERIVED**.

---

## 4. Every consecutive plane turn is orthogonal

Let

\[
n_j=p_j\times q_j
\]

be the nonzero normal of the `j`-th triad plane.  Since

\[
(Au)\times(Av)=\det(A)A^{-T}(u\times v)
\]

and `A^T A=25I`,

\[
A^{-T}=A/25,
\]

so

\[
\boxed{n_{j+1}=5A n_j=25Q n_j}.
\]

At the base scale,

\[
n_0=(0,0,4),
\qquad
A n_0=(16,-12,0),
\]

and therefore

\[
n_0\cdot n_1=0.
\]

Because `Q` preserves inner products, this propagates to every step:

\[
\boxed{n_j\cdot n_{j+1}=0\quad\text{for all }j\ge0.}
\]

Thus every shared-mode transition is the exact zero-dispersion non-planar case from the turn trichotomy: an orthogonal exchange of the two adapted projective axes.

The union of the chain is genuinely three-dimensional; for example

\[
p_0=(1,0,0),
\quad p_1=(3,4,0),
\quad p_2=(9,12,20)
\]

has determinant `80`.

### Status

`NS-P2-ORTHOGONAL-TURN-ALLSCALE-GEOMETRY` — **DERIVED**.

---

## 5. Adapted scalar chain and axis exchange

For the `j`-th triad let

\[
N_j=\frac{n_j}{|n_j|}
\]

and define its in-plane unit tangent at the backbone input by

\[
T_j=N_j\times\frac{p_j}{|p_j|}.
\]

For the adapted Fourier--Leray tensor, the channel

\[
(p_j,T_j)+(q_j,N_j)\to(p_{j+1},N_j)
\]

has raw scalar coefficient

\[
c_j=\frac{|p_j\times q_j|}{|p_j|}.
\]

At the base scale, `|p_0 x q_0|=4`, hence

\[
|p_j\times q_j|=4\,25^j
\]

and

\[
\boxed{c_j=4\,5^j}.
\]

The orthogonal plane turn exchanges the adapted axes at the shared output/input mode.  At the base step,

\[
N_1\times\frac{p_1}{|p_1|}=N_0,
\]

and the similitude propagates the same relation at every scale:

\[
\boxed{T_{j+1}=N_j}
\]

up to the harmless projective sign convention.

Therefore the scalar output coordinate selected at step `j` is precisely the backbone scalar input coordinate selected at step `j+1`.

### Status

`NS-P2-ORTHOGONAL-TURN-AXIS-EXCHANGE` — **DERIVED**.

---

## 6. Cutoff-uniform homogeneous H1 coefficient

Use the physical homogeneous `H1` scalar coordinate

\[
X_{k,s}=|k|z_{k,s}.
\]

For an energy-transfer channel the homogeneous normalized coefficient is

\[
\Gamma_j^{H^1,hom}
=2c_j\frac{|p_{j+1}|}{|p_j||q_j|}.
\]

Substituting the exact scale laws gives

\[
\Gamma_j^{H^1,hom}
=2(4\,5^j)
\frac{5^{j+1}}
{5^j(2\sqrt5\,5^j)}
=\boxed{4\sqrt5}.
\]

Hence the selected orthogonal-turn chain has a strictly positive coefficient independent of the cutoff scale.

### Status

`NS-P2-ORTHOGONAL-TURN-H1-HOM-COEFF` — **DERIVED**.

This is the energy-transfer normalization; the corresponding normalized amplitude-ODE coefficient is half of this value.

---

## 7. Finite-prefix phase satisfiability

For the selected complex scalar channel at step `j`, maximal signed transfer imposes one affine phase relation among the backbone input, fresh donor and backbone output phases.  The donor mode `q_j` appears for the first time at that step and is not reused at any other scale.

Therefore, after choosing the backbone input phase, choose the fresh donor phase so that the `j`-th selected channel saturates its preferred phase.  The output phase then becomes the backbone phase for the next step through the axis-exchange identity above.

This recursive assignment works for every finite prefix.  There is no selected-channel phase holonomy cycle in the tree itself.

### Status

`NS-P2-ORTHOGONAL-TURN-SELECTED-TREE-SAT` — **DERIVED**.

Consequently:

`NS-P2-ORTHOGONAL-TURN-ALONE-FORCES-SELECTED-HOLONOMY` — **REFUTED**.

This does **not** assert that the full NSE interaction graph on these active modes is phase-SAT.

---

## 8. Dyadic progress

Although the construction scales Euclidean length by `5`, it also crosses at least one standard max-coordinate dyadic boundary at every step.  Indeed

\[
|v|_\infty\le |v|_2
\quad\text{and}\quad
|v|_\infty\ge |v|_2/\sqrt3.
\]

Therefore

\[
\frac{|p_{j+1}|_\infty}{|p_j|_\infty}
\ge
\frac{|p_{j+1}|_2/\sqrt3}{|p_j|_2}
=\frac5{\sqrt3}>2.
\]

Thus every selected step advances by more than a factor `2` in the cube-cutoff scale.

### Status

`NS-P2-ORTHOGONAL-TURN-DYADIC-PROGRESS` — **DERIVED**.

---

## 9. P2 consequence

The local geometric trichotomy is now red-teamed on its last zero-dispersion non-planar branch:

```text
same-plane branch
    -> 2D3C regular;

positive frame dispersion
    -> existing frustration/cut tax;

orthogonal-turn branch
    -> can still support an all-scale phase-SAT selected chain
       with cutoff-uniform H1 coupling.
```

Therefore spatial turn geometry alone still does not close P2.

The remaining meaningful attack is on the **full NSE convolution** generated by the all-scale orthogonal-turn chain, together with the already-derived recent-nonlinear ancestry reduction.  One must determine whether the off-tree interactions necessarily create packed holonomy / relative window loss, or whether there exists a richer full-interaction escape.

Current boundary:

```text
all-scale integer orthogonal-turn selected chain             DERIVED
selected finite-prefix phase SAT                             DERIVED
homogeneous H1 coefficient = 4 sqrt(5)                       DERIVED
max-coordinate dyadic progress > 2 per step                  DERIVED
orthogonal-turn geometry alone forces selected holonomy      REFUTED
full-convolution orthogonal-turn interaction closure          OPEN
recent-ancestry + induced-interaction relative scale loss     OPEN
K_N / R_j contraction                                        OPEN
NS-P2-FRUSTRATION-OR-CUT                                     OPEN
NS-P2B-SCALE-CONTRACTION-UNIFORM                             OPEN
Clay Navier--Stokes regularity                                OPEN
```
