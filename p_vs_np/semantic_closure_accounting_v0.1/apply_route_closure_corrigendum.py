#!/usr/bin/env python3
"""Apply the v0.1.1 route-closure corrigendum to the Semantic Closure paper.

The patch is deliberately exact and fail-closed: every replacement must match
once unless the corrected text is already present. This preserves an auditable
source transformation rather than silently hand-editing the generated PDF.
"""
from pathlib import Path

P = Path(__file__).with_name("Semantic_Closure_Accounting_P_vs_NP_v0.1.tex")
text = P.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str) -> None:
    global text
    if new in text:
        print(f"already corrected: {label}")
        return
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"corrigendum fail-closed: {label}: expected 1 old match, got {count}")
    text = text.replace(old, new, 1)
    print(f"corrected: {label}")


replace_once(
    r"\date{September 10, 2026\\\small Preprint v0.1}",
    r"\date{September 10, 2026\\\small Preprint v0.1; route-closure corrigendum September 11, 2026}",
    "date/version note",
)

replace_once(
    "These observations leave one load-bearing problem open: construct a non-circular, sharing-aware semantic demand $H_n$ for $\\SAT_n$ and prove a capacity theorem valid for every small shared circuit, with $H_n/K_n$ superpolynomial.",
    "These observations leave one load-bearing problem open: construct a non-circular, sharing-aware semantic demand $H_n$ for $\\SAT_n$ and prove a capacity theorem valid for every small shared circuit, with $H_n/K_n$ not polynomially bounded.",
    "abstract asymptotic wording",
)

replace_once(
    "  \\item \\textbf{Superpolynomial demand/capacity ratio.} For every polynomial $p$, for all sufficiently large $n$,\n  \\[\n  H_n(\\SAT_n)>p(n)K_n.\n  \\]",
    "  \\item \\textbf{No polynomial upper bound on the demand/capacity ratio.} For every polynomial $p$ and every $N$, there exists $n\\ge N$ such that\n  \\[\n  H_n(\\SAT_n)>p(n)K_n.\n  \\]",
    "Property 3 exact P/poly target",
)

replace_once(
    "contradicting Property 3 for sufficiently large $n$. Hence $\\SAT\\notin\\Ppoly$.",
    "Property 3 applied to this polynomial $p$ supplies arbitrarily large $n$ with $H_n(\\SAT_n)>p(n)K_n$, contradicting the accounting inequality at such an $n$. Hence $\\SAT\\notin\\Ppoly$.",
    "conditional theorem proof",
)

replace_once(
    "The theorem is intentionally conditional. It shows that the bridges and arithmetic are sufficient \\emph{if and only if} the missing semantic demand/capacity premise can be supplied in a non-circular way.",
    "The theorem is intentionally conditional. It shows that the bridges and arithmetic are sufficient \\emph{provided that} the missing semantic demand/capacity premise can be supplied in a non-circular way. No converse is proved.",
    "iff -> sufficient-only corrigendum",
)

old_open = r"""\begin{conjecture}[SAT Semantic Demand Theorem --- open]
Construct an explicit semantic demand $H_n$ and a per-gate capacity scale $K_n$ for the canonical SAT function such that:
\[
\boxed{
H_n(\SAT_n)=n^{\omega(1)}K_n
}
\]
in the sense that $H_n(\SAT_n)/(K_n n^c)\to\infty$ for every fixed $c$, while the capacity theorem remains valid for every shared bounded-fan-in Boolean circuit after basis simulation.
\end{conjecture}"""
new_open = r"""\begin{conjecture}[SAT Semantic Demand Theorem --- open]
Construct an explicit semantic demand $H_n$ and a per-gate capacity scale $K_n$ for the canonical SAT function such that the ratio is not eventually bounded by any polynomial. In multiplication-only form:
\[
\boxed{
\forall p\text{ polynomial},\;\forall N,\;\exists n\ge N:\quad
H_n(\SAT_n)>p(n)K_n
}
\]
while the capacity theorem remains valid for every shared bounded-fan-in Boolean circuit after basis simulation.
\end{conjecture}"""
replace_once(old_open, new_open, "open theorem asymptotic correction")

anchor = r"""The theorem is intentionally conditional. It shows that the bridges and arithmetic are sufficient \emph{provided that} the missing semantic demand/capacity premise can be supplied in a non-circular way. No converse is proved.

\section{Future Work: The Open Load-Bearing Theorem}"""
inserted = r"""The theorem is intentionally conditional. It shows that the bridges and arithmetic are sufficient \emph{provided that} the missing semantic demand/capacity premise can be supplied in a non-circular way. No converse is proved.

\subsection{Route-closure theorem: demand already lower-bounds circuit size}
Let $CC(f_n)$ denote the minimum size of a correct circuit for a Boolean function $f_n$ in the declared circuit model. Suppose the universal accounting premise holds for every correct circuit $C$:
\[
H_n(f_n)\le |C|K_n.
\]
Applying it to a minimum-size correct circuit immediately gives
\[
\boxed{H_n(f_n)\le CC(f_n)K_n.}
\]
Consequently, for every integer gate budget $B$,
\[
BK_n<H_n(f_n)\quad\Longrightarrow\quad B<CC(f_n).
\]
This multiplication-only implication is also formalized in the accompanying IDM file \texttt{IDM\_DemandCircuitDominance.v}.

\begin{remark}[Route-closure consequence]
A non-polynomial lower bound on $H_n(\SAT_n)/K_n$ under an accounting theorem valid for all unrestricted shared circuits is already a non-polynomial Boolean-circuit lower bound for SAT. Thus the semantic accounting architecture organizes the missing breakthrough but does not make it weaker. The tautological assignment $H_n(f_n)=CC(f_n)$ and $K_n=1$ would be tight but is circular and is excluded by Property 1.
\end{remark}

\section{Future Work: The Open Load-Bearing Theorem}"""
if inserted not in text:
    count = text.count(anchor)
    if count != 1:
        raise SystemExit(f"corrigendum fail-closed: route-closure insertion: expected 1 anchor, got {count}")
    text = text.replace(anchor, inserted, 1)
    print("corrected: route-closure theorem insertion")
else:
    print("already corrected: route-closure theorem insertion")

replace_once(
    "The architecture is not a solution of P versus NP. The unresolved theorem is substantive: SAT must be shown to possess a superpolynomial semantic demand relative to the legal capacity of every small shared circuit, under a definition that is non-circular, recomputation-aware, sharing-aware, and robust to standard complexity barriers.",
    "The architecture is not a solution of P versus NP. The unresolved theorem is substantive: SAT must be shown to possess semantic demand relative to legal per-gate capacity that is not polynomially bounded for every small shared circuit, under a definition that is non-circular, recomputation-aware, sharing-aware, and robust to standard complexity barriers.",
    "conclusion asymptotic wording",
)

P.write_text(text, encoding="utf-8")
print("route-closure corrigendum: PASS")
