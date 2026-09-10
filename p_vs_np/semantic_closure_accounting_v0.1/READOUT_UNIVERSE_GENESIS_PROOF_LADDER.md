# Readout Universe + Readout Genesis proof ladder for P vs NP

**Status:** active research note. This note does **not** claim a proof of `P != NP`.

This is the proof ladder after the route-closure audit. The problem is translated into Readout Universe / Readout Genesis language first, then translated back to complexity theory only at the final bridge.

## 0. What the new N=2 Navier--Stokes certificate changes

The Navier--Stokes lane now has two finite resolutions at which the same qualitative chain has been realized:

```text
N=1: observability -> explicit quotient chart -> q_1 < 1 -> positive local radius
N=2: observability -> explicit 245D quotient chart -> q_2 <= 1/2 -> positive local radius
```

This matters methodologically: `rank saturation -> explicit chart -> quantitative certificate` is no longer a one-resolution accident. It is still a finite statement and does not imply an all-N theorem.

For P vs NP the transferable object is the **pattern**, not the Jacobian or numerical radius:

```text
structural distinguishability
    -> explicit reader-relative finite state/chart
    -> quantitative per-transform certificate
    -> global completion/lower-bound conclusion.
```

The computational analogue of the quantitative step remains OPEN.

---

## 1. Step-1 translation: SAT as a finite obstruction problem

For a CNF formula

`F = C_1 & ... & C_m`

and a Boolean assignment `a`, define the exact obstruction readout

`r_F(a)_j = 1` iff clause `C_j` is false under `a`,

and

`V_F(a) = sum_j r_F(a)_j`.

Then exactly

`SAT(F)=1  <->  exists a, V_F(a)=0`,

`SAT(F)=0  <->  forall a, V_F(a)>=1`.

This is a finite translation only. No continuum or infinite witness space is introduced.

**Status:** definition / exact finite semantics.

---

## 2. RD4 relocation: visible collapse is not global erasure

Readout Universe RD4 requires retention/injectivity at the generated-history level, while its append-only tape model shows that a visible contraction can coexist with an injective larger record.

Let a joint retained record be

`J_t(h) = (R_t(h), T_t(h))`,

where `R_t` is the part accessible to the next computational step and `T_t` is complementary retained tape/history. If `J_t` is injective, then

`h != h' and R_t(h)=R_t(h')  ->  T_t(h)!=T_t(h')`.

Thus RD4 does **not** imply that every distinction must stay in circuit working memory. It implies only that a genuine global collapse cannot be claimed while an injective complement still carries the distinction.

The paired decoder fact is immediate:

`R_t(h)=R_t(h') -> D(R_t(h))=D(R_t(h'))`.

So a downstream reader restricted to `R_t` cannot use a distinction that has left the accessible record unless the computation later re-accesses, recomputes, or semantically resolves it.

**Status:** finite structural theorem; Coq candidate in IDM `IDM_ReadoutUniverseAccessibleCompletion.v`.

---

## 3. Accessible Retain--Recompute--Resolve law

For a distinction `d` that can still change a declared future terminal readout, once `d` leaves the accessible state one of three things must happen before the terminal answer depends on it:

1. **RE-ACCESS / RETAIN:** a retained record carrying the relevant effect is read again;
2. **RECOMPUTE:** the effect is reconstructed from still-accessible information;
3. **RESOLVE:** a valid closure establishes that the distinction is no longer load-bearing for the terminal readout.

Schematic obligation:

`load_bearing(d,t) -> retain_or_reaccess(d,t) OR recompute(d,t) OR resolve(d,t)`.

This is the accessibility-correct form of the earlier RRR idea. Ontological/global tape retention is not counted as computational working memory unless a later step actually accesses it.

**Status:** structural schema; the universal **cost** version is OPEN.

---

## 4. Finite completion theorem

For an UNSAT decision, let `B_1,...,B_k` be finite cells/subcubes of assignment space. Suppose:

1. every assignment belongs to at least one `B_i`;
2. each `B_i` has an independently verified local obstruction, e.g. a clause falsified by every assignment extending that cell.

Then every assignment has positive obstruction and `F` is UNSAT.

In Readout language:

`resolved rejection cells + zero uncovered witness tail -> exact NO readout`.

This is the discrete fail-closed completion analogue of the EPSC pattern.

**Status:** generic finite theorem candidate in Coq; exact DPLL/subcube maker-checker diagnostic in IDM.

Important fence: an arbitrary polynomial-time SAT decider is not required to emit a DPLL tree, resolution proof, or this specific certificate.

---

## 5. Circuit -> accessible Genesis ledger

Use the already-built CGSL bridge to represent an actual Boolean circuit DAG without unfolding sharing. Each gate has one ledger entry and parent references preserve fanout/reuse.

The Readout-Universe correction is that the ledger distinguishes:

- `accessible state`: values/records available to downstream gates;
- `historical lineage`: provenance/tape retained for audit;
- `semantic role`: downstream readouts the quantity can still affect.

Only accessible, load-bearing information may be charged as current computational burden.

**Status:** bridge kernel exists; its use as a lower-bound representation remains conditional on the later capacity theorem.

---

## 6. Reader-relative chart: the computational analogue of the NS quotient chart

For a cut `t` in a circuit/trajectory, define two source histories `h,h'` to be equivalent when every **declared future continuation through the actual suffix computation** produces the same terminal readout:

`h ~_t h'  <->  O_future(h,u)=O_future(h',u) for every admissible future access/intervention u`.

The reader-relative chart is the quotient

`Q_t = H_t / ~_t`.

This is not a claim that the algorithm explicitly stores the quotient. It is a semantic audit object: it tells us which distinctions remain load-bearing at that cut.

Negative control: Equality can have exponentially many residual contexts and still a linear-size shared circuit. Therefore `|Q_t|` alone is not a circuit-size lower bound.

**Status:** quotient principle is supported by Genesis future-reader equivalence and existing FutureReadoutWidth work; unrestricted circuit lower bound does not follow.

---

## 7. The missing quantitative analogue of `q_N < 1`

The NS programme becomes quantitative only after the structural chart is equipped with a certified local inverse/contraction estimate. For P vs NP we need an analogous **finite discrete capacity certificate**.

Provisional object:

`Cap(g | Q_t, A_t, lineage_t)`

= the maximum amount of reader-relevant unresolved semantic burden that one admissible gate/step `g` can discharge, after allowing sharing, re-access and recomputation.

The target theorem must be universal over the actual circuit model:

`semantic_progress(g) <= Cap(g)`

and

`sum_{g in C} Cap(g) <= poly(n, |C|)`.

A notation analogous to the NS contraction factor may be introduced only after a concrete operator/metric exists. Writing a symbolic `q_C` without such an operator would merely rename the open problem.

**Status:** OPEN and load-bearing.

---

## 8. SAT semantic-demand theorem

Construct an explicit finite SAT family `F_n` and an answer-oblivious, representation-stable quantity

`Demand(F_n)`

such that:

1. it counts only distinctions exposed by declared future readers;
2. harmless renaming/re-encoding does not increase it;
3. sharing is charged once, not once per syntactic obligation;
4. recomputation is permitted but charged through the trajectory;
5. computing/certifying `Demand` does not call SAT, circuit minimization, or the target answer;
6. for every polynomial `p`, there are arbitrarily large `n` with

   `Demand(F_n) > p(n) * per_gate_capacity(n)`.

Combined with the universal capacity theorem, any exact circuit for SAT must then be superpolynomial.

**Status:** OPEN and load-bearing.

---

## 9. Transfer to P vs NP

Once Steps 7 and 8 are proved for unrestricted Boolean circuits, the existing demand/circuit transfer gives a superpolynomial lower bound for SAT circuit families:

`SAT notin P/poly`.

Since `P subseteq P/poly`, this implies

`P != NP`.

The implication is conditional on Steps 7 and 8; no claim of separation is made before they are closed.

---

## 10. Current proof status

```text
finite SAT obstruction translation                         CLOSED / definition
RD4 visible-collapse -> complementary-record distinction   Coq candidate
visible collision blocks visible-only decoder distinction  Coq candidate
finite rejection-cover completion                          Coq candidate + executable fixture
circuit -> sharing-preserving Genesis ledger               CLOSED structural kernel
future-reader quotient principle                           CLOSED structural/restricted kernels
accessible RRR cost theorem                                OPEN in unrestricted form
universal per-gate semantic capacity certificate           OPEN
explicit SAT superpolynomial semantic-demand theorem       OPEN
SAT notin P/poly                                            NOT PROVED
P != NP                                                     NOT PROVED
```

The new N=2 NS certificate strengthens confidence in the **research pattern** `structural chart -> quantitative certificate`; it does not supply either of the two open computational theorems.

---

## 11. Falsifiers / anti-overclaim gates

Reject any proposed continuation if it:

- treats global/ontological retention as mandatory circuit working memory;
- counts distinctions that no declared future reader can expose;
- forbids sharing or recomputation without a without-loss-of-generality proof;
- defines `Demand` using SAT answers or minimum circuit size;
- writes a `q_C`-style contraction coefficient without specifying an actual finite operator, norm/metric, and verifier;
- proves only a restricted proof-system lower bound but reports an unrestricted circuit lower bound;
- promotes finite experiments, N=1/N=2 analogies, or Coq bookkeeping kernels to `P != NP`.

## Internal lineage

- Readout Universe: `v2/INFORMATION_DNA.md`, `v2/TRANSLATION_PROTOCOL.md`, `v2/APPEND_ONLY_RECORD.md`, `v2/DOCTRINE_OF_QUANTITY.md`.
- Readout Genesis Universal Technical Whitepaper v1.2.0: retention-before-persistence, strong future-reader equivalence, sufficient-before-quotient, tape, closure/lineage ledger, claim non-borrowing.
- IDM branch `research/p-vs-np-readout`: decision readout, future-readout width, CGSL, RRR, demand/circuit dominance, and accessible-completion kernels.
- NS/EPSC lane: finite observability -> explicit symmetry slice/chart -> quantitative inverse certificate, now realized at fixed `N=1` and fixed `N=2`.
