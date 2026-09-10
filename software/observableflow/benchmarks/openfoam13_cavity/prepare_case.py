#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import re

from observableflow.openfoam import generate_probes_function_object


def grid(values, z=0.005):
    return [(x, y, z) for y in values for x in values]


def main() -> None:
    ap = argparse.ArgumentParser(description="Instrument the OpenFOAM-13 cavity tutorial for ObservableFlow")
    ap.add_argument("case")
    ap.add_argument("--end-time", type=float, default=2.0)
    args = ap.parse_args()

    case = Path(args.case)
    control = case / "system" / "controlDict"
    text = control.read_text(encoding="utf-8")
    text, n = re.subn(r"(?m)^endTime\s+[^;]+;", f"endTime         {args.end_time:g};", text, count=1)
    if n != 1:
        raise RuntimeError("could not replace endTime in cavity controlDict")
    if "observableFlowCandidates" in text or "observableFlowReference" in text:
        raise RuntimeError("case appears to be instrumented already")

    candidates = grid([0.02, 0.04, 0.06, 0.08])
    reference = grid([0.0125, 0.025, 0.0375, 0.05, 0.0625, 0.075, 0.0875])

    cand_block = generate_probes_function_object(
        candidates, ["p", "U"], name="observableFlowCandidates",
        write_control="timeStep", write_interval=1, library='"libsampling.so"',
    )
    ref_block = generate_probes_function_object(
        reference, ["p", "U"], name="observableFlowReference",
        write_control="timeStep", write_interval=1, library='"libsampling.so"',
    )
    text += "\n\nfunctions\n{\n" + cand_block + "\n" + ref_block + "}\n"
    control.write_text(text, encoding="utf-8")

    print(f"instrumented: {case}")
    print(f"candidate probe locations: {len(candidates)} (p,U)")
    print(f"reference probe locations: {len(reference)} (p,U)")
    print(f"endTime: {args.end_time:g}")


if __name__ == "__main__":
    main()
