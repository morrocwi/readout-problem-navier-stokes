# NS P2 — Cross-Family Boundary Cancellation Forces Planarity or Off-Plane Novelty

**Status:** NEW DERIVATION / PROPOSAL; exact symbolic local theorem  
**Global OCSR / Witness Soundness / cancellation compatibility:** OPEN  
**Clay Navier–Stokes regularity:** OPEN  
**Checker:** `reproduction/checks/check_ns_p2_cross_family_boundary_cancellation.py`

## 0. Reuse-first path

This note applies the central rule

```text
Toledo lookup -> Genesis compatibility -> reuse existing object -> derive only the missing piece -> mark PROPOSAL
```

and introduces no new global architecture.

Reused objects:

- the existing symmetric projected NSE interaction `B`;
- `PROP-P2-CANCELLATION-LEDGER-01` (exact cancellation accounting);
- the already-certified equal-source-shell direction lock from Standalone Sections 14 / 113;
- the antipodal strip boundary geometry from `NS_P2_ANTIPODAL_CANCELLATION_LADDER.md`;
- the Genesis/Toledo rule that a future-relevant nonzero full-convolution contribution must be retained, cancelled by a registered constraint, routed to a declared boundary, or returned as unresolved — never silently erased.

A Toledo lookup found no existing cross-family boundary-cancellation theorem. The result below is therefore a new proposal.

## 1. Boundary geometry

Rotate coordinates within the already-declared local frame so that the strip anchor is

\[
p=(0,P,0),\qquad a=e_3,\qquad P\ne0,
\]

and the planar strip boundary target is

\[
s=(K,L,0)\ne0.
\]

The uncancelled strip boundary source is a nonzero multiple of `e3`.

Now recruit an arbitrary external triad

\[
r+t=s,
\]

with divergence-free nonzero polarizations

\[
u\perp r,\qquad v\perp t,
\]

and suppose its contribution cancels the boundary source:

\[
\boxed{\mathcal B_{r,t}(u,v)=\gamma e_3,\qquad \gamma\ne0.}
\]

The question left open by the antipodal ladder was whether such a cross-family canceller can kill the boundary without generating a new registered consequence.

## 2. Exact anchor-cross determinant

Write

\[
r=(x,y,z).
\]

On the genuinely three-dimensional branch `z != 0`, use the transverse basis

\[
u_1=\left(1,0,-\frac{x}{z}\right),\qquad
u_2=\left(0,1,-\frac{y}{z}\right)
\]

for `r^perp`.

For the linear map

\[
L_r:u\in r^\perp\longmapsto \mathcal B_{p,r}(e_3,u)\in(p+r)^\perp,
\]

the exact 2-by-2 determinant in the corresponding transverse coordinates is

\[
\boxed{
\det L_r
=
\frac{z^2\bigl(|r|^2-|p|^2\bigr)}{|p+r|^2}.
}
\tag{CF-1}
\]

Likewise, since `t_z=-z`,

\[
\boxed{
\det L_t
=
\frac{z^2\bigl(|t|^2-|p|^2\bigr)}{|p+t|^2}.
}
\tag{CF-2}
\]

These are exact symbolic identities checked over the rational function field; no numerical approximation enters the PASS decision.

Therefore, for `z != 0`, if a nonzero polarization lies in the kernel of an anchor-cross map, the corresponding source must lie on the anchor shell:

\[
\mathcal B_{p,r}(e_3,u)=0,\ u\ne0
\Longrightarrow |r|=|p|,
\]

\[
\mathcal B_{p,t}(e_3,v)=0,\ v\ne0
\Longrightarrow |t|=|p|.
\]

## 3. Both cross channels cannot vanish on a genuinely 3D canceller

Assume for contradiction that

\[
\mathcal B_{p,r}(e_3,u)=0,
\qquad
\mathcal B_{p,t}(e_3,v)=0
\]

with `u,v` nonzero and `z != 0`.

By (CF-1)–(CF-2),

\[
|r|=|t|=|p|.
\]

Thus the external parent pair is equal-source-shell. The already-existing equal-shell direction-lock result then forces

\[
\mathcal B_{r,t}(u,v)\parallel r\times t.
\]

But, because `t=s-r` and `s=(K,L,0)`,

\[
r\times t=r\times s
=
(-Lz,\ Kz,\ -Ky+Lx).
\]

Its horizontal squared magnitude is exactly

\[
\boxed{
(-Lz)^2+(Kz)^2
=z^2(K^2+L^2)>0
}
\]

when `z != 0` and `s != 0`.

Hence `r x t` cannot be parallel to `e3`, contradicting the assumed nonzero cancellation direction

\[
\mathcal B_{r,t}(u,v)=\gamma e_3.
\]

Therefore

\[
\boxed{
 z\ne0
 \Longrightarrow
 \max\left\{
 \|\mathcal B_{p,r}(e_3,u)\|,
 \|\mathcal B_{p,t}(e_3,v)\|
 \right\}>0.
}
\tag{CF-3}
\]

## 4. The forced descendant is genuinely off-plane

The two anchor-cross targets are

\[
p+r,
\qquad
p+t.
\]

Their third coordinates are respectively

\[
z,\qquad -z.
\]

Thus, on the genuinely 3D branch, any nonzero forced cross interaction lands outside the original planar strip:

\[
\boxed{
 z\ne0
 \Longrightarrow
 \text{at least one nonzero off-plane full-convolution descendant.}
}
\tag{CF-4}
\]

It cannot coincide with any wavevector of the planar antipodal strip.

## 5. Exact dichotomy

Combining the planar and genuinely 3D branches gives the local cross-family result:

\[
\boxed{
\begin{aligned}
&r+t=s\in e_3^\perp,\quad
\mathcal B_{r,t}(u,v)=\gamma e_3,\quad \gamma\ne0
\\
&\Longrightarrow
\begin{cases}
 r_z=t_z=0,
 &\text{the recruited cancelling triad is planar},\\[1mm]
 \text{or}\\[-2mm]
 \exists\,w\in\{p+r,p+t\}:\ w_z\ne0
 \text{ and the corresponding interaction is nonzero},
 &\text{off-plane novelty}.
\end{cases}
\end{aligned}
}
\tag{CF-5}
\]

This answers the precise question left at the end of the antipodal-ladder note: an arbitrary external triad cannot cancel a strip boundary **silently**. It either remains in the planar branch or full convolution forces an off-plane retained consequence.

## 6. Non-vacuity control

The checker includes the exact rational instance

\[
s=(1,2,0),\quad r=(1,0,1),\quad t=(0,2,-1),
\]

\[
u=(0,1,0),\qquad
v=\left(-\frac13,-\frac14,-\frac12\right),
\]

for which

\[
\mathcal B_{r,t}(u,v)=-e_3,
\]

while both anchor-cross descendants are nonzero and land at

\[
(1,1,1),\qquad (0,3,-1).
\]

So the genuinely 3D branch is nonempty.

## 7. Proposed result

`PROP-P3-CROSS-FAMILY-BOUNDARY-CANCEL-01` — **NEW DERIVATION / PROPOSAL; exact symbolic PASS**.

Bounded statement:

```text
For the declared antipodal-strip anchor geometry, any nonzero external triad
whose source exactly cancels an e3-directed planar strip-boundary source is
either planar, or full convolution with the strip anchor forces a nonzero
off-plane descendant.  Therefore cross-family cancellation cannot silently
terminate the strip boundary in one generation.
```

## 8. What is and is not closed

Closed by this proposal:

- the first arbitrary-external-triad cancellation question for the antipodal strip boundary;
- the equal-shell loophole, via the existing direction-lock result;
- the genuinely 3D silent-cancellation loophole, via (CF-1)–(CF-4).

Still OPEN:

- whether a larger 3D web can cancel the newly forced off-plane descendant with further recruited modes while remaining compact, productive and zero-defect;
- global multi-source cancellation compatibility;
- OCSR;
- Witness Soundness globally;
- G6/G7;
- Clay Navier–Stokes regularity.

## 9. Next reuse-first target

No new architecture is needed. The next missing piece is now narrower:

```text
Take the forced off-plane descendant from (CF-4).
Can further sources cancel it while keeping every resulting cross interaction
inside a compact zero-defect recurrent web?
```

The next pass should first reuse the same determinant/nullity machinery and the existing equal-shell direction lock on that off-plane target before proposing anything new.
