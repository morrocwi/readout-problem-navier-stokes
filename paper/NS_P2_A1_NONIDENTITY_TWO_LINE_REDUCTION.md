# NS P2 — A1 Nonidentity Type-P Monodromy Reduces to a Two-Line Skeleton

**Status:** NEW DERIVATION / PROPOSAL; exact finite projective algebra  
**Parent:** `paper/NS_P2_PROJECTIVE_HOLONOMY_TYPE_AUDIT.md`  
**Global FNW / OCSR / Witness Soundness / G4/G6/G7:** OPEN  
**Clay Navier–Stokes regularity:** OPEN  
**Checker:** `reproduction/checks/check_ns_p2_typeP_nonidentity_fixedline_classification.py`

## 0. Reuse-first ruling

Standing rule:

```text
Toledo lookup -> Genesis compatibility -> reuse existing object -> derive only the missing piece -> mark PROPOSAL
```

Reused objects:

- Type-P projective null transport `T_e` and loop monodromy `M=T_loop`;
- plane-switch capacity / two-lineage lock;
- plane-switch normal-lineage reconstruction;
- `PROP-P3-PROJECTIVE-THREE-LINE-RIGIDITY-01`;
- productive-triad exact self-closure and full-convolution discipline.

No Toledo object was found for the specific nonidentity fixed-line reduction below, so this note is a proposal.

## 1. Fixed projective lines of a 2x2 monodromy

Let a real invertible representative of the Type-P loop monodromy be

\[
A=\begin{pmatrix}a&b\\c&d\end{pmatrix}.
\]

A projective line `[X:Y]` is fixed exactly when `A(X,Y)^T` is proportional to `(X,Y)^T`, equivalently

\[
\boxed{
 cX^2+(d-a)XY-bY^2=0.
}
\tag{A1-1}
\]

The discriminant of this homogeneous quadratic is

\[
\boxed{
\Delta_P=(d-a)^2+4bc
=(\operatorname{tr}A)^2-4\det A.
}
\tag{A1-2}
\]

Therefore a nonidentity real projective monodromy has exactly one of the following real fixed-line patterns:

```text
Delta_P < 0  -> 0 real fixed projective lines;
Delta_P = 0  -> 1 real fixed projective line (double/parabolic);
Delta_P > 0  -> 2 real fixed projective lines.
```

Three distinct fixed projective lines force the identity in `PGL(2,R)` by the already-derived three-line rigidity theorem.

### Status

`PROP-P3-TYPEP-FIXEDLINE-CLASSIFICATION-01` — **NEW DERIVATION / PROPOSAL; exact finite algebra PASS**.

## 2. Consequence for a recurrent rank-2 retained web

A recurrent retained lineage class that returns to the base fiber without terminalization/exit/defect must satisfy

\[
M[\ell]=[\ell].
\]

A nondegenerate rank-2 retained plane requires two independent retained lineage classes.

Hence:

### Case E — no real fixed line

If `Delta_P<0`, then no real retained projective lineage can return exactly.

Therefore a zero-defect exact recurrence is impossible unless the purported returning lineage is resolved/terminalized/exits or the Type-P loop was not the correct dynamically sufficient return object.

### Case P — one real fixed line

If `Delta_P=0` and `M` is nonidentity, there is only one recurrent real projective class.

Therefore an exact rank-2 recurrent retained plane cannot be supported by two independent returned lineages. The branch must undergo rank drop / degeneration or a registered resolution/exit/defect.

### Case H — two real fixed lines

If `Delta_P>0`, then `M` has exactly two fixed projective classes

\[
[\ell_+],\qquad [\ell_-].
\]

Thus the only nonidentity Type-P branch still capable of supporting a recurrent rank-2 retained plane is the exact **two-line skeleton**:

\[
\boxed{
\operatorname{RetReturn}(M)
\subseteq
\{[\ell_+],[\ell_-]\}.
}
\tag{A1-3}
\]

Any future-relevant retained lineage that re-enters the base fiber with projective class outside this set is an immediate recurrence obstruction.

## 3. Correct definition of third re-entered lineage

For A1, define a **third re-entered lineage candidate** to be a projective class `[m]` such that:

1. `[m]` has an actual full-convolution lineage path;
2. after the declared joint reanchor it lies in the same base projective fiber on which `M` acts;
3. it remains future-reader relevant after reanchor;
4. it is not in the fixed set of `M`:

\[
\boxed{[m]\notin\operatorname{Fix}(M).}
\tag{A1-4}
\]

This terminology avoids calling `[m]` a recurrent lineage before recurrence has been established.

If exact recurrence requires this retained lineage to return unchanged, then

\[
M[m]=[m]
\]

contradicts (A1-4).

Hence

\[
\boxed{
M\neq I
+\text{third re-entered future-relevant lineage}
+\text{no terminal/exit/defect/resolution}
\Rightarrow
\text{recurrence incompatibility}.
}
\tag{A1-5}
\]

This is an exact logical consequence of the typed recurrence definition; the hard content is generating/returning such a lineage from full convolution.

## 4. A1 is now reduced to the two-line escape problem

The nonidentity branch no longer needs a generic holonomy classification theorem. After exact fixed-line classification, only one genuinely nondegenerate escape remains:

\[
\boxed{
M\neq I,
\quad \Delta_P>0,
\quad \text{all future-relevant returned lineages lie in exactly two fixed classes.}
}
\tag{A1-6}
\]

Call this the **two-line skeleton**.

The next theorem target is therefore:

\[
\boxed{
\text{productive full-convolution two-line skeleton}
\Rightarrow
\text{third re-entered lineage}
\vee
\text{rank drop / planar-degenerate branch}
\vee
\text{registered terminal/exit/defect/resolution}.
}
\tag{A1-7}
\]

Status: **OPEN**.

## 5. Relation to equal-shell / W3 / NPSC work

The existing anchor-cross nullity theorem says a nontrivial null transport edge is forced onto the equal-shell locus unless it is a rank-0 collapse edge. Therefore the invertible Type-P recurrence problem is concentrated on equal-shell webs.

This makes the A1 two-line skeleton the same structural arena already attacked by W3 / NPSC-style full-convolution closure tests.

Finite diagnostics can therefore be used as falsification/calibration for (A1-7), but must not be promoted to a theorem across arbitrary depth or unbounded mode boxes.

## 6. Claim boundary

Derived / exact finite algebra:

```text
projective fixed-line equation                                DERIVED
fixed-line discriminant classification                       DERIVED
nonidentity rank-2 recurrence -> only possible in 2-line case DERIVED conditionally on typed exact return
third re-entered lineage outside Fix(M) -> recurrence clash  DERIVED logical consequence
```

Still OPEN:

```text
full-convolution generation of a third re-entered lineage    OPEN
two-line skeleton impossibility in general                   OPEN
rank-0 collapse-edge recurrent classification                OPEN
identity-monodromy branch                                    OPEN
FNW / OCSR / Witness Soundness                               OPEN
G4 / G6 / G7                                                  OPEN
Clay Navier-Stokes regularity                                OPEN
```

## 7. Immediate falsification target

Search exactly for a productive equal-shell full-convolution recurrent web with:

```text
nonidentity M,
two real fixed projective lines,
all future-relevant retained returned lineages in those two lines,
no named terminal/exit/defect/resolution.
```

A single exact realized example refutes the strongest form of (A1-7). If every attempted populated full-convolution realization forces a third class or rank drop, that evidence should be accumulated without promoting finite search to a global theorem.
