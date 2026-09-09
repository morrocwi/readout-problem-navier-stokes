#!/usr/bin/env bash
# One-command reproduction runner for the Readout-Navier-Stokes Development Series
# (GLS-2026-006 + GLS-2026-007, Volumes 1-6). Runs every check script under checks/ and
# regenerates LEDGER.json / LEDGER.md. Exit code is nonzero if any check script reported
# an actual failure (a claim it attempted to verify did not hold) -- it is NOT nonzero
# just because some claims are legitimately tiered Dr/Open.
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

echo "=================================================================="
echo " Readout-Navier-Stokes Development Series -- reproduction runner"
echo "=================================================================="
echo

PY=python3
if ! command -v "$PY" >/dev/null 2>&1; then
    echo "ERROR: python3 not found on PATH" >&2
    exit 2
fi

"$PY" generate_ledger.py
status=$?

echo
echo "=================================================================="
if [ "$status" -eq 0 ]; then
    echo " All mechanically-checkable claims passed. See LEDGER.md / LEDGER.json."
else
    echo " One or more check scripts reported a FAILED claim. See output above and LEDGER.md."
fi
echo "=================================================================="

exit "$status"
