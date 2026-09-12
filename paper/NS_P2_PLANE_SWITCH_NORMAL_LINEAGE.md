# NS P2 — Plane-Switch Normal/Lineage Reconstruction

**Status:** NEW DERIVATION / PROPOSAL; exact finite retained-space identity  
**Parents:** `PROP-P3-PLANE-SWITCH-CAPACITY-01`; existing projective-null connection / lineage architecture  
**Global FNW / OCSR / Witness Soundness / cancellation compatibility:** OPEN  
**Clay Navier–Stokes regularity:** OPEN  
**Checker:** `reproduction/checks/check_ns_p2_plane_switch_normal_lineage.py`

## 0. Reuse-first path

Standing rule:

```text
Toledo lookup -> Genesis compatibility -> reuse existing object -> derive only the missing piece -> mark PROPOSAL
```

A Toledo lookup found no canonical plane-normal / lineage reconstruction theorem.  The identity below is therefore a new proposal built only from the already-declared retained plane-switch geometry.

## 1. Basis-replacement chain

Represent consecutive rank-2 planes by retained lineage pairs

\[
W_j=\operatorname{span}\{c_j,c_{j+1}\},
\qquad
W_{j+1}=\operatorname{span}\{c_{j+1},c_{j+2}\}.
\]

Define projective plane normals

\[
n_j=c_j\times c_{j+1},
\qquad
n_{j+1}=c_{j+1}\times c_{j+2}.
\]

The switch is genuine exactly when

\[
\Delta_j:=\det[c_j\ c_{j+1}\ c_{j+2}]\neq0,
\]

because `Delta_j=0` means all three lineage directions are coplanar and the two rank-2 planes coincide.

## 2. Exact normal/lineage identity

Direct vector algebra gives

\[
\boxed{
 n_j\times n_{j+1}
 =
 \Delta_j\,c_{j+1}.
}
\tag{PN-1}
\]

The checker verifies this symbolically over generic coordinates.

Therefore, on every genuine plane switch,

\[
\boxed{
[c_{j+1}]
=
[n_j\times n_{j+1}].
}
\tag{PN-2}
\]

So the shared retained lineage direction is not an independent degree of freedom: it is projectively reconstructed from the two neighboring plane normals.

## 3. Consequence for a closed plane-switch loop

Consider

\[
W_0\to W_1\to\cdots\to W_{m-1}\to W_0
\]

with every step genuine.  Let `n_j` be the projective normal of `W_j`.  Then every shared lineage class is fixed by adjacent normals:

\[
[c_{j+1}]=[n_j\times n_{j+1}].
\]

Thus a closed basis-replacement loop has only one projective data stream, not two independent ones:

```text
plane-normal loop
        ↓ exact reconstruction
shared-lineage loop.
```

Any declared projective-null / lineage transport around the loop must agree with this reconstructed lineage sequence.  A mismatch is a named compatibility / translation defect rather than a silently adjustable polarization choice.

This is the first exact bridge from the local plane-switch reduction to the existing Standalone projective-null connection / holonomy language.

## 4. Degenerate branch is explicit

If

\[
\Delta_j=0,
\]

then

\[
n_j\times n_{j+1}=0.
\]

This is precisely the no-genuine-switch / coplanar branch.  The reconstruction rule does not divide by `Delta_j`; it simply classifies the branch:

```text
Delta_j != 0 -> genuine switch + lineage reconstructed from normals
Delta_j  = 0 -> same-plane / planar-degenerate branch
```

No hidden regularity or future-good behavior enters the classification.

## 5. Proposed result

`PROP-P3-PLANE-SWITCH-NORMAL-LINEAGE-01` — **NEW DERIVATION / PROPOSAL; exact finite PASS**.

Bounded statement:

```text
For a genuine rank-2 basis-replacement switch
W_j=span(c_j,c_{j+1}) -> W_{j+1}=span(c_{j+1},c_{j+2}),
with normals n_j=c_j×c_{j+1} and n_{j+1}=c_{j+1}×c_{j+2},

n_j×n_{j+1} = det[c_j,c_{j+1},c_{j+2}] c_{j+1}.

Hence the shared retained lineage class is determined projectively by adjacent
plane normals.  A closed genuine plane-switch loop therefore induces a uniquely
reconstructed lineage loop that must match the declared projective-null / lineage
transport or register a compatibility defect.
```

## 6. What this advances

The previous bottleneck was a closed basis-replacement loop

\[
(c_1,c_2)\to(c_2,c_3)\to\cdots\to(c_m,c_1).
\]

The new identity rewrites it as a **normal-loop compatibility problem**:

\[
[n_0],[n_1],\ldots,[n_{m-1}]
\quad\Longrightarrow\quad
[c_{j+1}]=[n_j\times n_{j+1}].
\]

Thus plane geometry and retained lineage can no longer be tuned independently to close recurrence.

## 7. What remains OPEN

Still OPEN:

- classification of normal loops compatible with the existing projective-null transport;
- whether a nontrivial compatible loop necessarily forces planarity / degeneration / registered cancellation;
- phase and amplitude compatibility around such a loop;
- global Witness Soundness and cancellation compatibility;
- FNW / OCSR;
- G6 / G7;
- Clay Navier–Stokes regularity.

## 8. Next reuse-first target

Reuse Standalone Section 114 projective-null loop transport.  Substitute the exact reconstructed classes

\[
[c_{j+1}]=[n_j\times n_{j+1}]
\]

into the loop condition

\[
T_{\rm loop}(\lambda)=\lambda.
\]

The next missing piece is therefore no longer generic plane switching.  It is:

```text
classify projective normal loops whose reconstructed lineage sequence is a
fixed point of the existing null-transport holonomy.
```

That is the current direct entrance into FNW.
