#!/usr/bin/env bash
# Cenário C4 (GCD incremental) nas bases do PBN. Ver run_c4.py.
#
# Uso:
#   bash run_pbn_c4.sh                       # bases presentes em data/
#   bash run_pbn_c4.sh pendigits letter      # só algumas
#   SESSIONS=3 OUT=results_c4 FAMILIES="mst svm-cv auto-auroc rf_msp sskmeans" bash run_pbn_c4.sh
#   K_EST=hdbscan OUT=results_c4_eom bash run_pbn_c4.sh pendigits letter
set -euo pipefail
cd "$(dirname "$0")"
BASES=("$@")
if [ ${#BASES[@]} -eq 0 ]; then
  for d in data/*/; do [ -f "$d/split.json" ] && BASES+=("$(basename "$d")"); done
fi
for b in "${BASES[@]}"; do
  [ -f "data/$b/split.json" ] || { echo "ERRO: base '$b' não encontrada em data/"; exit 1; }
done
SEEDS="${SEEDS:-0 1 2 3 4}"
SESSIONS="${SESSIONS:-3}"
ALPHA="${ALPHA:-0.1}"
OUT="${OUT:-results_c4}"
FAMILIES="${FAMILIES:-gauss mst svm-cv auto-auroc rf_msp sskmeans}"
K_EST="${K_EST:-hdbscan-leaf}"
PY="${PYTHON:-$(command -v python3 || command -v python)}"
mkdir -p "$OUT"
"$PY" - <<'PY' > "$OUT/versions.txt"
import platform, numpy, scipy, sklearn, pandas
print("python", platform.python_version())
for m in (numpy, scipy, sklearn, pandas):
    print(m.__name__, m.__version__)
PY
for b in "${BASES[@]}"; do
  echo "=== C4 $b"
  "$PY" -W ignore run_c4.py --data "data/$b" --seeds $SEEDS --sessions "$SESSIONS" \
      --alpha "$ALPHA" --k-est "$K_EST" --families $FAMILIES --out "$OUT/${b}_c4.csv"
done
"$PY" summarize_c4.py "$OUT"
