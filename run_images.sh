#!/usr/bin/env bash
# Estudo com imagens: C2 e C4 sobre as características do DINO em data_img/
# (geradas por prepare_image_features.py). Usa os mesmos scripts das bases
# tabulares, com a configuração final (alpha 0,1, hdbscan-leaf).
#
# Uso:
#   bash run_images.sh                 # todas as bases em data_img/
#   bash run_images.sh cifar10         # só algumas
#   SEEDS="0" bash run_images.sh cifar10        # teste rápido, uma semente
#   SO_C2=1 bash run_images.sh cifar10          # pula o C4
set -euo pipefail
cd "$(dirname "$0")"
export DATA="${DATA:-data_img}"
export SEEDS="${SEEDS:-0 1 2}"
FAM_C2="${FAM_C2:-auto mst gauss rf_msp lr_msp sskmeans kmeans}"
FAM_C4="${FAM_C4:-auto-auroc mst gauss rf_msp sskmeans}"

ALPHAS="0.1" K_EST=hdbscan-leaf KKNOWN="${KKNOWN:-1}" OUT="${OUT_C2:-results_img}" \
  FAMILIES="$FAM_C2" bash run_pbn_gcd.sh "$@"
[ "${SO_C2:-0}" = 1 ] && exit 0
ALPHA=0.1 K_EST=hdbscan-leaf OUT="${OUT_C4:-results_img_c4}" \
  FAMILIES="$FAM_C4" bash run_pbn_c4.sh "$@"
