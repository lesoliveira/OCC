#!/usr/bin/env bash
# PBN no C2 nas 15 bases. Nas 7 bases do PBN usa os hiperparâmetros
# publicados; nas 8 do OpenML roda antes a busca (--tune), que grava em
# results_pbn/hparams/<base>.json e não é refeita se o arquivo já existir.
#
# Uso:
#   bash run_pbn_all.sh                      # as 15 bases
#   bash run_pbn_all.sh vowel segment        # só algumas
#   SEEDS="0" bash run_pbn_all.sh vowel      # teste rápido
set -euo pipefail
cd "$(dirname "$0")"
PY=python3; command -v python3 >/dev/null || PY=python
SEEDS="${SEEDS:-0 1 2 3 4}"
PBN_BASES="har letter pendigits census mfeat optdigits cnae9"
ALL="$PBN_BASES isolet satimage segment vowel krvsk covertype helena volkert"
BASES=("$@"); [ ${#BASES[@]} -eq 0 ] && read -r -a BASES <<< "$ALL"
for b in "${BASES[@]}"; do
  [ -f "data/$b/split.json" ] || { echo "ERRO: base '$b' não encontrada em data/"; exit 1; }
  if [[ " $PBN_BASES " != *" $b "* ]] && [ ! -f "results_pbn/hparams/$b.json" ]; then
    echo "== $b: busca de hiperparâmetros $(date +%T)"
    $PY run_pbn_baseline.py --data "data/$b" --tune
  fi
  echo "== $b: C2 $(date +%T)"
  $PY run_pbn_baseline.py --data "data/$b" --scenario c2 --seeds $SEEDS
done
echo "fim $(date +%T)"
