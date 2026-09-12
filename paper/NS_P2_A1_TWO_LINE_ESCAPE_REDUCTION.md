# NS P2 — A1 two-line nonidentity escape reduction

**Status:** REUSE-FIRST REDUCTION + NEW DERIVATION / PROPOSAL  
**Parent:** `NS_P2_PROJECTIVE_HOLONOMY_TYPE_AUDIT.md`, Standalone vNext §§10–14, 113–118  
**Global FNW / OCSR / Witness Soundness / G4/G6/G7:** OPEN  
**Clay Navier–Stokes regularity:** OPEN  
**Field declaration (O1 correction, 2026-09-13):** the two-line skeleton is taken over the real fixture field; over `ℂP¹` every nonidentity `M` still has at most two fixed lines, so the two-line skeleton survives complexification, but the elliptic exclusion of the parent paper does not (see that paper's field declaration; complex lane = T0-04).  
**Checker:** `reproduction/checks/check_ns_p2_orthogonal_turn_fullclosure_escape.py`

## 0. Reuse-first audit

Standing rule:

```text
Toledo lookup -> Genesis compatibility -> reuse existing object -> derive only the missing piece -> mark PROPOSAL
```

No Toledo object was found for the specific A1 two-line recurrence reduction below.

Reused repository results:

1. `PROP-P3-PROJECTIVE-THREE-LINE-RIGIDITY-01`:
   a nonidentity `PGL(2,R)` monodromy fixes at most two projective lineage classes.
2. shared-mode plane-turn trichotomy:
   same plane / orthogonal turn / positive projective frame dispersion.
3. positive projective frame dispersion:
   existing event-level frame-mismatch theorem gives a genuine scalar-channel frustration-or-amplitude-cut candidate with an explicit coefficient floor.
4. same-plane branch:
   exactly plane-supported NSE reduces to the regular 2D3C branch.
5. Standalone vNext §11:
   a nonplanar orthogonal zero-dispersion patch cannot remain geometrically zero-dispersion under full local closure beyond two generations unless a relevant coupling is suppressed/degenerate.
6. exact cancellation ledger and Genesis no-silent-loss discipline:
   a suppressed generated channel must be registered as cancellation / resolution / exit / defect / unresolved, not silently deleted.

The only new algebra in this note is an exact checker upgrade of item 5 and the resulting A1 reduction.

---

## 1. A1 as previously stated was stronger than necessary

After the three-line rigidity lemma, the nonidentity branch was phrased as the target

\[
M\ne I
+\text{productive recurrence}
\Longrightarrow
\text{third returned projective lineage}
\ \vee\
\text{registered terminal/exit/defect/resolution}.
\]

A full proof of an actual **third returned line** is not presently available, and is not needed as the first move.

The existing shared-mode geometry already supplies a sharper reduction:

```text
if a two-line-return web ever has positive projective frame dispersion,
    -> route to the existing event-level frustration/amplitude-cut branch;

if every active shared-mode transition has zero dispersion,
    -> each transition is same-plane or orthogonal-turn;

same-plane forever,
    -> planar / 2D3C regular branch;

nonplanar orthogonal-turn,
    -> full local closure forces positive dispersion within <=2 geometric
       closure generations unless one of the generated channels is suppressed.
```

Thus the genuinely hard residue is not the abstract existence of a third projective fixed line. It is the **recursive charging of suppressed full-convolution descendants**.

---

## 2. Exact orthogonal-turn full-closure geometry

Let

\[
p=(P,0,0),\qquad
q=(a,b,0),\qquad
r=(c,0,d),
\]

with `P,b,d != 0`.

The two parent plane normals are

\[
n_1=p\times q=(0,0,Pb),
\]

\[
n_2=p\times r=(0,-Pd,0),
\]

so they are orthogonal.

The cross geometry has normal

\[
\boxed{
n_3=q\times r=(bd,-ad,-bc).
}
\]

Because `bd != 0`, `n_3` cannot be parallel to either `n_1` or `n_2`. If the new geometry is also zero projective-dispersion relative to each parent plane, it must therefore be orthogonal to both.

The two exact dot products are

\[
\boxed{n_3\cdot n_1=-Pb^2c,}
\]

\[
\boxed{n_3\cdot n_2=Pad^2.}
\]

Thus zero dispersion with both parents forces

\[
\boxed{a=0,\qquad c=0.}
\]

The unique nondegenerate first-generation geometric survivor is therefore the mutually orthogonal triple

\[
p=(P,0,0),\qquad q=(0,Q,0),\qquad r=(0,0,R),
\]

with `P,Q,R != 0`.

Now full convolution produces the descendant wavevectors

\[
s=p+q=(P,Q,0),
\qquad
t=p+r=(P,0,R).
\]

Their common plane normal is

\[
\boxed{
n_{st}=s\times t=(QR,-PR,-PQ).
}
\]

Against the parent `p,q` plane normal, the squared cosine is

\[
\boxed{
c_{pq}^2
=\frac{P^2Q^2}{Q^2R^2+P^2R^2+P^2Q^2}.
}
\]

Against the parent `p,r` plane normal,

\[
\boxed{
c_{pr}^2
=\frac{P^2R^2}{Q^2R^2+P^2R^2+P^2Q^2}.
}
\]

For nonzero `P,Q,R`, both satisfy

\[
0<c^2<1.
\]

Hence both associated projective frame-dispersion invariants

\[
\mu=4c^2(1-c^2)
\]

are strictly positive.

### Status

`PROP-P3-ORTHOGONAL-TURN-FULLCLOSURE-ESCAPE-01` — **NEW DERIVATION / PROPOSAL; exact wavevector-geometry PASS**.

The checker verifies all identities symbolically.

### Important boundary

The statement is geometric. It does **not** prove every descendant scalar NSE channel is nonzero. If the required descendant is removed by polarization nullity, amplitude zero, exact cancellation, terminalization, exit, or defect, that suppression must be routed through the already-existing ledgers. This caveat is the remaining load-bearing branch.

---

## 3. A1 reduction

Let `M=T_loop` be the Type-P monodromy of a productive recurrent lineage web and assume

\[
M\ne I.
\]

By projective three-line rigidity, at most two distinct future-relevant lineage classes can be fixed by `M`.

Assume the web attempts to keep all returned projective lineage classes inside those two fixed lines.

At every active shared-mode event, exactly one of the following occurs.

### Branch 1 — positive projective frame dispersion

Then the already-derived shared-frame mismatch machinery applies to the **actual registered event geometry**. This is a valid Type-P-to-Type-Phi local realization because it passes through explicit Fourier triads, not through an abstract holonomy identification.

Outcome:

\[
\boxed{
\text{local phase-frustration tax}
\ \vee\
\text{amplitude/coupling cut}.
}
\]

No new phase-packing theorem is needed.

### Branch 2 — zero dispersion, same plane

If a connected productive component remains on one Fourier plane, it belongs to the existing planar / 2D3C regular branch.

### Branch 3 — zero dispersion, orthogonal turn

By `PROP-P3-ORTHOGONAL-TURN-FULLCLOSURE-ESCAPE-01`, exact full local closure creates positive projective frame dispersion within at most two geometric closure generations **unless** a required generated channel is suppressed.

Therefore

\[
\boxed{
\text{nonplanar zero-dispersion two-line patch}
\Rightarrow
\text{positive-dispersion event}
\ \vee\
\text{registered suppression}.
}
\]

Combining the three branches gives the A1 reduction

\[
\boxed{
\begin{aligned}
&M\ne I,
\quad\text{productive recurrent web},
\quad\#\operatorname{Fix}(M)\le2
\\
&\Longrightarrow
\text{planar/2D3C}
\ \vee\
\text{event-level frustration/cut}
\ \vee\
\text{full-convolution suppression ledger}.
\end{aligned}
}
\tag{A1-RED}
\]

### Status

`PROP-P3-A1-TWO-LINE-ESCAPE-REDUCTION-01` — **DERIVED AS A REUSE-FIRST REDUCTION**, conditional on the already-recorded planar and frame-mismatch theorems and on explicit registration of suppressed descendants.

This is **not** a proof of the nonidentity FNW branch, because repeated suppression may in principle be supplied by cancellation/degeneracy patterns that have not yet been globally charged.

---

## 4. What this changes in the attack map

The previous immediate target

```text
M != I -> force a third returned line
```

is now downgraded from the preferred move. It may still be true in some subfamilies, but proving it globally is stronger than necessary.

The preferred nonidentity route is now

```text
M != I
 -> at most two recurrent projective classes
 -> local shared-mode trichotomy
 -> planar
    OR positive-dispersion event-level tax/cut
    OR suppressed full-convolution descendant
 -> recursively charge suppression using OCSR + Witness Soundness.
```

Thus A1 has been reduced directly back to the canonical Standalone vNext bottleneck rather than spawning another independent global theorem.

---

## 5. Remaining exact obligation

The next missing piece is now

\[
\boxed{
\text{repeated suppression of the forced positive-dispersion descendants}
\Longrightarrow
\text{payable reader consequence / exit / degeneration}
}
\]

without using the false shortcut

\[
C_k>0\Rightarrow\text{physical defect}.
\]

This is precisely the existing OCSR + global multi-source cancellation compatibility + Witness Soundness frontier.

Falsification first:

```text
search for a compact productive full-convolution web that repeatedly cancels
or nulls every positive-dispersion descendant while remaining nonplanar,
zero-defect, no-exit, and reader-sufficient.
```

If such a web is exact, the current OCSR route is refuted. If every attempted suppression forces new retained constraints / escape / degeneracy, those exact cuts belong in OCSR.

---

## 6. Claim boundary

```text
orthogonal-turn full-closure wavevector geometry                 DERIVED exact / proposal
A1 two-line nonidentity branch reduction                         DERIVED reduction / proposal
recursive charging of suppressed descendants                     OPEN
OCSR                                                               OPEN
Witness Soundness                                                  OPEN
FNW / G6                                                           OPEN
G4 / G7                                                            OPEN
Clay Navier-Stokes regularity                                      OPEN
```
