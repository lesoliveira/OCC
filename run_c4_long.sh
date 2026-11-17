#!/usr/bin/env bash
# GCD incremental com stream mais longo (T=10 sessões), para medir como o
# tempo por sessão cresce com a história. Mesma configuração final do
# results_c4_v2 (prioridade, hdbscan-leaf), só muda o número de sessões.
#
# Uso (no diretório OCC):
#   bash run_c4_long.sh                       # auto e RF-MSP nas 6 bases
#   PBN=1 bash run_c4_long.sh                 # inclui o PBN (mais lento, precisa de torch)
#   SESSIONS=6 bash run_c4_long.sh letter     # outra configuração
set -euo pipefail
cd "$(dirname "$0")"
BASES=("$@")
[ ${#BASES[@]} -eq 0 ] && BASES=(letter isolet covertype volkert helena pendigits)
FAMILIES="auto-auroc rf_msp"
[ "${PBN:-0}" = "1" ] && FAMILIES="$FAMILIES pbn"
SESSIONS="${SESSIONS:-10}" OUT="${OUT:-results_c4_long}" FAMILIES="$FAMILIES" \
  bash run_pbn_c4.sh "${BASES[@]}"
