#!/usr/bin/env bash
# One-command reproduction lane for the finite energy-observability paper.
# Default: full exact rerun. Use --quick to verify committed certificates only.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"
PY="${PYTHON:-python3}"
MODE="${1:-full}"
OUT="$HERE/results/reproduced_energy_observability"
mkdir -p "$OUT"

if ! command -v "$PY" >/dev/null 2>&1; then
  echo "ERROR: python3 not found" >&2
  exit 2
fi

if [[ "$MODE" == "--quick" || "$MODE" == "quick" ]]; then
  "$PY" checks/check_energy_observability_manifest.py
  exit $?
fi

if [[ "$MODE" != "full" && "$MODE" != "--full" ]]; then
  echo "usage: bash reproduction/reproduce_energy_observability.sh [full|--full|quick|--quick]" >&2
  exit 2
fi

run() {
  local name="$1"; shift
  echo "=================================================================="
  echo " $name"
  echo "=================================================================="
  "$@" 2>&1 | tee "$OUT/${name}.log"
}

run positive_viscosity "$PY" checks/check_positive_viscosity_scaling.py
run k1_observability "$PY" checks/check_volume6_ns_observability.py
run k2_scalar_energy "$PY" checks/check_k2_energy_observability.py
run k3_shell_energy "$PY" checks/check_k3_shell_energy_observability.py
run manifest "$PY" checks/check_energy_observability_manifest.py

cat > "$OUT/STATUS.txt" <<EOF
PASS
Simulation=No
All requested exact finite-field checks exited successfully.
Paper: paper/NS_ENERGY_OBSERVABILITY_ALL_K_FINAL.tex
EOF

echo
cat "$OUT/STATUS.txt"
