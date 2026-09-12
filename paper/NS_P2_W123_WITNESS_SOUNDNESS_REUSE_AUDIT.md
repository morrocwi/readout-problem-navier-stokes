# NS P2 — W1/W2/W3 Witness-Soundness Reuse Audit

**Status:** NEW DERIVATION / PROPOSAL; exact on the three registered witnesses only  
**Global `NS-P2-WITNESS-SOUNDNESS`:** OPEN  
**Clay Navier–Stokes regularity:** OPEN  
**Checker:** `reproduction/checks/check_ns_p2_witness_soundness_w123.py`

## 0. Reuse-first governance

This note follows the central Toledo/Genesis reuse order:

```text
Toledo lookup
-> Genesis compatibility
-> reuse existing object
-> derive only the missing piece
-> mark PROPOSAL
```

No new root ontology, quotient architecture, cancellation notion, or Clay bridge is introduced here.

Reused objects:

- Toledo / Genesis domain-weld and sufficiency machinery (`weld/M.02.v1`, `weld/M.03.v1`, `weld/E.05.v1`, `weld/E.06.v1`, `weld/E.08.v1`);
- Readout Genesis `NoEarlyCollapse`, future-readout partitioning, mandatory lineage preservation, and named-defect accounting;
- P2 exact cancellation ledger

\[
C_k=\sum_\alpha\|g_{\alpha,k}\|-\left\|\sum_\alpha g_{\alpha,k}\right\|\ge0;
\]

- existing exact cancellation witnesses W1/W2/W3 from `NS_P2_MULTISOURCE_CANCELLATION_OCSR_GEN1.md`;
- existing full-local-convolution rule and the W3 depth-1 computation.

## 1. The correction

The open TODO asked whether `C_k > 0` should be interpreted as a payable physical loss `D_cancel` or as a constraint.

The cancellation ledger alone does **not** license

```text
C_k > 0  =>  physical loss > 0.
```

That implication is therefore not used.

Instead, when the shared target cancels exactly,

\[
\sum_\alpha g_{\alpha,k}=0,
\]

the cancellation is registered as an exact algebraic constraint on the source amplitudes / phases / polarizations. By Genesis sufficiency and lineage rules, that constraint may be discarded only after it is shown irrelevant to every declared future readout; it cannot be silently erased.

Thus the concrete witness-soundness question becomes:

> Does exact cancellation at the shared target make the whole finite source web lossless at the next full-convolution generation?

## 2. Exact depth-1 audit

The new checker independently reconstructs the existing W1/W2/W3 source states, imposes the Fourier reality partners, runs one exact full local-convolution generation, and aggregates every target exactly.

Results:

| witness | real modes | depth-1 targets | nonzero net targets | single-source nonzero targets | zero targets beyond `±k` |
|---|---:|---:|---:|---:|---:|
| W1 | 8 | 18 | 16 | 12 | 0 |
| W2 | 12 | 44 | 42 | 30 | 0 |
| W3 | 12 | 44 | 36 | 30 | 6 projection-zero targets |

For all three witnesses, the designated shared target `k` and its reality partner `-k` cancel exactly, but the full source web produces many other nonzero targets in the same generation.

In particular:

- W1: `±k` are the **only** zero-net targets; 16 of 18 targets are nonzero and 12 are single-source.
- W2: `±k` are the **only** zero-net targets; 42 of 44 targets are nonzero and 30 are single-source.
- W3: the previous result is independently reproduced: 36 of 44 targets are nonzero, including 30 single-source targets; six additional targets are exact projection zeros.

All counts are exact SymPy assertions; no floating-point tolerance enters a PASS decision.

## 3. Reusable conclusion

Define the already-existing source/net/cancellation quantities

\[
G_k:=\sum_\alpha\|g_{\alpha,k}\|,
\qquad
N_k:=\left\|\sum_\alpha g_{\alpha,k}\right\|,
\qquad
C_k=G_k-N_k.
\]

For a productive source family `G_k>0`, the ledger gives the elementary bifurcation:

```text
N_k > 0
    -> nonzero net response at k;
N_k = 0
    -> C_k = G_k > 0 and the exact relation sum g_{alpha,k}=0 must be registered.
```

The three fixtures now show that the second branch is **not terminal losslessness**: the exact cancellation relation at `k` coexists with forced off-target novelty under the same full-convolution state.

Therefore, on W1/W2/W3, the sound interpretation is:

```text
C_k > 0 is not automatically a payable physical defect.
Exact cancellation is a live registered constraint.
The source web cannot disappear merely because the shared target cancels.
```

This is the smallest conclusion licensed by the existing Genesis/Toledo machinery and the exact finite computation.

## 4. Proposed local status

`PROP-P3-CANCEL-CONSTRAINT-LIVE-W123-01` — **NEW DERIVATION / PROPOSAL; exact finite PASS on W1/W2/W3**.

Statement:

```text
For each of the registered cancellation witnesses W1/W2/W3,
exact cancellation at the designated shared target does not make the
one-generation full local convolution lossless. The cancellation relation
must therefore remain a live registered constraint (unless a later reader
sufficiency proof certifies it future-irrelevant); it is not licensed as a
positive physical-loss term merely from C_k > 0.
```

## 5. What is now closed and what remains open

Closed on these three fixtures:

- the `C_k > 0 = physical loss` shortcut is rejected;
- the `C_k > 0 = live constraint` reading passes the exact depth-1 test;
- W1 and W2 join W3 as exact examples where shared-target cancellation does not erase the web.

Still OPEN:

- global `NS-P2-WITNESS-SOUNDNESS` for arbitrary cancellation webs;
- global multi-source cancellation compatibility;
- antipodal-source configurations;
- OCSR beyond the certified finite seeds / generations;
- UBRR, full recurrent GIR, G7, and Clay regularity.

## 6. Next reusable move

Do not invent a new cancellation functional. Reuse the same registered constraint mechanism on the next smallest open family:

```text
antipodal-source cancellation
or
OCSR generation 2
```

and ask the same exact question:

```text
Does exact suppression/cancellation terminate the web,
or does full convolution force a retained descendant / new constraint?
```

That keeps the attack on the existing Standalone-vNext path rather than opening a new proof architecture.
