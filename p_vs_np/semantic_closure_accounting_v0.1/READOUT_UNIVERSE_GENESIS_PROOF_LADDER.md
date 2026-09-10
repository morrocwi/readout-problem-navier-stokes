# Readout Universe + Readout Genesis proof ladder for P vs NP

**Status:** active research note. This note does **not** claim a proof of `P != NP`.

This is the proof ladder after the route-closure audit. The problem is translated into Readout Universe / Readout Genesis language first, then translated back to complexity theory only at the final bridge.

## 0. What the new N=2 Navier--Stokes certificate changes

The Navier--Stokes lane now has two finite resolutions at which the same qualitative chain has been realized:

```text
N=1: observability -> explicit quotient chart -> q_1 < 1 -> positive local radius
N=2: observability -> explicit 245D quotient chart -> q_2 <= 1/2 -> positive local radius
```

This matters methodologically: `structural saturation -> explicit chart -> quantitative certificate` is no longer a one-resolution accident. It remains a finite statement and does not imply an all-N theorem.

For P vs NP the transferable object is only the **methodological pattern**:

```text
structural statement
    -> explicit finite semantic representation
    -> quantitative transform certificate
    -> global conclusion.
```

The inverse/observability map itself does **not** transfer to SAT. SAT's input formula is already fully given; its hard transform is existential projection over witnesses.

---

## 1. Step-1 translation: SAT as finite existential projection

For a CNF formula

`F = C_1 & ... & C_m`

and a Boolean assignment `a`, define the exact obstruction readout

`r_F(a)_j = 1` iff clause `C_j` is false under `a`,

and

`V_F(a) = sum_j r_F(a)_j`.

Then exactly

`SAT(F)=1  <->  exists a, V_F(a)=0`,

`SAT(F)=0  <->  forall a, V_F(a)>=1`.

Equivalently, if `R(F,a)` is the polynomial-time verifier relation,

`SAT(F) = OR_a R(F,a) = (pi_exists R)(F)`.

This is a finite existential projection, not a continuum limit and not a state-reconstruction problem.

**Status:** exact finite semantics; Coq kernel in IDM `IDM_ExistentialProjection.v`.

---

## 2. Crucial model guard: SAT is not an identifiability problem

The formula encoding itself is known exactly to the algorithm. The identity input reader

`q_in(F)=F`

is sufficient from the first step. Thus there is no missing input-state inverse analogous to the NS observation map.

Consequently:

- a null-space/observability lower bound on the formula input is the wrong object;
- NoEarlyCollapse cannot force witness retention, because the decider only needs the projected decision bit;
- the hard question is the cost of **constructing the existential projection**.

The NS `q_N` story remains a useful discipline: do not jump from a structural property to a complexity conclusion without a quantitative certificate. But the computational certificate must be a gate-generation/projection-capacity theorem, not a Jacobian inverse theorem.

---

## 3. RD4 relocation: visible collapse is not global erasure

Readout Universe RD4 requires retention/injectivity at the generated-history level, while its append-only tape model shows that a visible contraction can coexist with an injective larger record.

Let a joint retained record be

`J_t(h) = (R_t(h), T_t(h))`,

where `R_t` is the currently exposed component and `T_t` is complementary retained tape/history. If `J_t` is injective, then

`h != h' and R_t(h)=R_t(h')  ->  T_t(h)!=T_t(h')`.

This is a correct finite structural theorem. It does **not** mean every distinction must stay in circuit working memory.

For standard Boolean circuits the correction is stronger: a wire may fan out to arbitrarily many later gates at no additional gate cost. Therefore a circuit-size proof may not charge ordinary rereading/reuse as a fresh computation step.

**Status:** finite structural kernel + explicit free-reread guard in IDM.

---

## 4. Circuit-native semantic generation

A standard fan-in-two circuit is best translated as a generated semantic algebra.

Begin with input projections (and declared constants):

`G_0 = {x_1,...,x_n,0,1}`.

Each gate generates exactly one new extensional Boolean function from one or two previously generated functions:

`G_{t+1} = G_t union { b(g,h) }`.

All existing generated wires may be reused freely. Sharing is therefore preserved by construction.

A size-`s` circuit is a length-`s` semantic-generation ledger whose generated set contains the target function.

This is the correct circuit analogue of Genesis generation/lineage. The cost unit is **new semantic generation**, not tape reread.

**Status:** CGSL supplies the one-entry-per-gate syntax/semantics bridge; free-fanout is now an explicit model guard.

---

## 5. Finite completion theorem remains useful but restricted

For an UNSAT decision, let `B_1,...,B_k` be finite cells/subcubes of assignment space. Suppose:

1. every assignment belongs to at least one `B_i`;
2. each `B_i` has an independently verified local obstruction, e.g. a clause falsified by every assignment extending that cell.

Then every assignment is rejected and `F` is UNSAT.

In Readout language:

`resolved rejection cells + zero uncovered witness tail -> exact NO readout`.

This is an exact finite completion theorem and is executable in IDM. But an arbitrary polynomial-time SAT decider is not required to emit a DPLL tree, resolution proof, or this specific certificate.

**Status:** Coq kernel + finite maker/checker diagnostic; restricted certificate route only.

---

## 6. Why static reader charts still do not give circuit size

For any quotient of an `n`-bit input space,

`|Q| <= 2^n`, hence `log2 |Q| <= n`.

For all partial restrictions, there are only `3^n` restrictions, hence residual-profile information is at most `n log2 3` bits.

Equality supplies the decisive sharing control: exponentially many residual contexts can coexist with a linear-size shared circuit.

Therefore neither raw reader-equivalence class count nor retained information size can be the missing unrestricted-circuit lower-bound invariant.

**Status:** no-go / route correction; exact finite static-measure audit added in IDM.

---

## 7. Universal Semantic Capacity: the missing quantitative theorem

The computational analogue of the NS quantitative step must be defined on the **actual generated prefix**, not on a static state alone.

Let

`A_t = A_f(G_t,L_t)`

be an adaptive, target-specific unresolved burden after the first `t` semantic-generation steps. A valid theorem must satisfy:

### Initial demand

`A_0 >= D_n(f)`.

### Completion

If `f in G_s`, then `A_s=0`.

### One-gate discharge bound

For every admissible gate extension,

`A_t - A_{t+1} <= K_n(t,G_t,L_t)`.

With a uniform `K_n`, telescoping gives

`D_n(f) <= s K_n`, hence `s >= D_n(f)/K_n`.

The arithmetic is already formalized by the transform-potential and demand/circuit kernels. The missing theorem is a non-circular construction of `A_f` and a universal one-gate capacity bound that survive sharing and arbitrary legal rewrites.

**Status:** OPEN and load-bearing.

---

## 8. Existential Projection Transform Complexity

SAT is the projection

`pi_exists R(F,.)`.

The research target can therefore be stated as an independent lower certificate for the cost of compiling a polynomial-time verifier relation into its existential projection.

Schematic interface:

`LB_exists(R_n) <= PTC(R_n)`

where `PTC` is the cost of generating the projection in the declared circuit model.

This is useful only if `LB_exists` is defined independently of SAT answers, minimum circuit size, or a hidden equivalence oracle. Defining `LB_exists` to equal circuit size would be circular and is forbidden.

**Status:** exact finite projection semantics CLOSED; non-circular unrestricted lower certificate OPEN.

---

## 9. Adaptive Semantic Generation Adversary (ASGA)

The next concrete object is a prefix adversary

`A_t = Update(f,G_t,L_t)`

with an integer burden `W(A_t)` such that:

1. the initial state is built from the explicit target/verifier family without solving circuit minimization;
2. adding one gate updates the adversary from the previous state plus that gate;
3. the checker can verify the update locally;
4. if the target has been generated then `W=0`;
5. every allowed gate has certified bounded discharge;
6. Equality, parity, free fanout and high-sharing circuits are mandatory negative controls.

This is intentionally close to adaptive fusion / approximation / constructive gate-elimination ideas already audited in the IDM branch. The Readout contribution is the reader-role, accessibility, lineage and claim-boundary discipline; it is not yet a new superpolynomial lower-bound theorem.

**Status:** OPEN and load-bearing.

---

## 10. SAT semantic-demand theorem

For an explicit NP verifier family, prove that the ASGA initial burden dominates every polynomial aggregate gate capacity on arbitrarily large input lengths:

`for every polynomial p and every N, exists n>=N:`

`D_n(SAT) > p(n) K_n`.

Together with Universal Semantic Capacity, any exact SAT circuit family must then be superpolynomial.

**Status:** OPEN and load-bearing.

---

## 11. Transfer to P vs NP

Once Sections 7 and 10 are proved for unrestricted Boolean circuits,

`SAT notin P/poly`.

Since `P subseteq P/poly`,

`P != NP`.

This implication remains conditional. No separation is claimed before the two load-bearing theorems are actually proved.

---

## 12. Current proof status

```text
finite SAT obstruction / existential-projection semantics    CLOSED / Coq candidate
RD4 visible-collapse -> complementary-record distinction     finite structural kernel
free circuit reread/fanout cannot be charged as new gate     explicit model guard
finite rejection-cover completion                            Coq candidate + executable fixture
circuit -> sharing-preserving Genesis ledger                 CLOSED structural kernel
static quotient/residual information as superpoly LB         REJECTED / information ceiling
Universal Semantic Capacity                                  OPEN
non-circular existential-projection lower certificate        OPEN
SAT superpolynomial semantic-demand theorem                  OPEN
SAT notin P/poly                                              NOT PROVED
P != NP                                                       NOT PROVED
```

The N=2 NS certificate strengthens confidence in the general research discipline `structural statement -> explicit representation -> quantitative certificate`. It does **not** provide the missing circuit capacity theorem.

---

## 13. Falsifiers / anti-overclaim gates

Reject any proposed continuation if it:

- treats SAT as missing-input observability when the complete formula is already available;
- treats global/ontological retention as mandatory circuit working memory;
- charges free fanout or ordinary rereading as a new gate;
- counts distinctions that no declared future reader can expose;
- forbids sharing or recomputation without a without-loss-of-generality proof;
- defines `Demand` using SAT answers or minimum circuit size;
- writes a `q_C`-style coefficient without specifying a concrete finite update/capacity operator and verifier;
- proves only a restricted proof-system lower bound but reports an unrestricted circuit lower bound;
- promotes finite experiments, N=1/N=2 analogies, or Coq bookkeeping kernels to `P != NP`.

## Internal lineage

- Readout Universe: `v2/INFORMATION_DNA.md`, `v2/TRANSLATION_PROTOCOL.md`, `v2/APPEND_ONLY_RECORD.md`, `v2/DOCTRINE_OF_QUANTITY.md`.
- Readout Genesis Universal Technical Whitepaper v1.2.0: retention-before-persistence, strong future-reader equivalence, sufficient-before-quotient, tape, closure/lineage ledger, claim non-borrowing.
- IDM branch `research/p-vs-np-readout`: decision readout, future-readout width, CGSL, RRR, demand/circuit dominance, accessible-completion, free-reread guard, semantic-capacity audit, and existential-projection kernels.
- NS/EPSC lane: finite observability -> explicit symmetry slice/chart -> quantitative inverse certificate, realized at fixed `N=1` and fixed `N=2`; used here only as a methodological pattern.
