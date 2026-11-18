#!/usr/bin/env bash
# Ablação p-valor x posteriori x híbrida (ClassWiseOCC.decision_).
#   bash results_post/run.sh c2   # transdutivo
#   bash results_post/run.sh c4   # incremental, T=3, tau de S0 + alpha_disc 0,3
cd "$(dirname "$0")/.."
S="$1"; J=()
for b in pendigits letter isolet; do for d in pvalue post hybrid; do J+=("$b $d"); done; done
printf '%s\n' "${J[@]}" | xargs -P 2 -L 1 bash -c '
b=$0; d=$1
if [ "'$S'" = c2 ]; then
  python3 -u -W ignore run_gcd.py --data data/$b --scenario c2 --families auto-auroc \
    --seeds 0 1 2 3 4 --alpha 0.1 --k-est hdbscan-leaf --decision $d \
    --out results_post/${b}_c2_$d.csv > results_post/${b}_c2_$d.log 2>&1
else
  python3 -u -W ignore run_c4.py --data data/$b --sessions 3 --families auto-auroc \
    --tau-s0 --alpha-disc 0.3 --decision $d \
    --out results_post/${b}_c4_$d.csv > results_post/${b}_c4_$d.log 2>&1
fi'
