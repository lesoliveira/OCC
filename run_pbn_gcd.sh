#!/usr/bin/env bash
# Cenário C2 (GCD transdutivo) nas bases do PBN, com a divisão de classes do
# PBN, 5 sementes, K estimado (Vaze et al.) e K conhecido, para cada alpha
# em ALPHAS. Resultados em $OUT/a<alpha>/ (um summary.md por alpha).
# Pré-requisito: python prepare_pbn_datasets.py
#
# Uso:
#   bash run_pbn_gcd.sh                      # bases presentes em data/
#   bash run_pbn_gcd.sh pendigits optdigits  # só algumas
#   ALPHAS="0.05 0.1 0.2" OUT=results_v2 bash run_pbn_gcd.sh pendigits letter
#   FAMILIES="mst mst+ssk rf_msp" bash run_pbn_gcd.sh pendigits
#   EXTRA="--repr pca64" OUT=results_x bash run_pbn_gcd.sh ...   (opções extras do run_gcd.py)
#   K_EST=silhouette KKNOWN=0 ALPHAS="0.1" OUT=results_ksil bash run_pbn_gcd.sh pendigits letter
set -euo pipefail
cd "$(dirname "$0")"

DATA="${DATA:-data}"   # pasta das bases (data_img para as de imagem)
BASES=("$@")
if [ ${#BASES[@]} -eq 0 ]; then
  BASES=()
  for d in "$DATA"/*/; do [ -f "$d/split.json" ] && BASES+=("$(basename "$d")"); done
fi
SEEDS="${SEEDS:-0 1 2 3 4}"
ALPHAS="${ALPHAS:-0.05 0.1 0.2}"
OUT="${OUT:-results}"
K_EST="${K_EST:-labeled}"   # labeled (Vaze et al.) ou silhouette (nos rejeitados)
KKNOWN="${KKNOWN:-1}"       # 0 pula a rodada com K conhecido
FAM_ARG=()
[ -n "${FAMILIES:-}" ] && FAM_ARG=(--families $FAMILIES)
mkdir -p "$OUT"
PY="${PYTHON:-$(command -v python3 || command -v python)}"
echo "usando $PY"

"$PY" - <<'PY' > "$OUT/versions.txt"
import platform, numpy, scipy, sklearn, pandas
print("python", platform.python_version())
for m in (numpy, scipy, sklearn, pandas):
    print(m.__name__, m.__version__)
PY

for b in "${BASES[@]}"; do
  [ -f "$DATA/$b/split.json" ] || { echo "ERRO: base '$b' não encontrada em $DATA/"; exit 1; }
done

for a in $ALPHAS; do
  R="$OUT/a$a"; mkdir -p "$R"
  for b in "${BASES[@]}"; do
    echo "=== alpha=$a $b: K estimado"
    "$PY" -W ignore run_gcd.py --data "$DATA/$b" --seeds $SEEDS --alpha "$a" \
        --cal-mode nested --k-est "$K_EST" ${FAM_ARG[@]+"${FAM_ARG[@]}"} ${EXTRA:-} --out "$R/${b}_c2_kest.csv"
    [ "$KKNOWN" = 0 ] && continue
    echo "=== alpha=$a $b: K conhecido"
    "$PY" -W ignore run_gcd.py --data "$DATA/$b" --seeds $SEEDS --alpha "$a" \
        --cal-mode nested --k-known ${FAM_ARG[@]+"${FAM_ARG[@]}"} ${EXTRA:-} --out "$R/${b}_c2_kknown.csv"
  done
  "$PY" summarize.py "$R"
done
