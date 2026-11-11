## ACC All média nas sessões

| family | letter | pendigits | média |
|---|---|---|---|
| mst | 0.685 ± 0.030 | 0.880 ± 0.025 | 0.783 |
| svm-cv | 0.684 ± 0.024 | 0.874 ± 0.021 | 0.779 |
| auto-auroc | 0.684 ± 0.026 | 0.861 ± 0.050 | 0.772 |
| gauss | 0.608 ± 0.041 | 0.799 ± 0.026 | 0.704 |
| rf_msp | 0.651 ± 0.012 | 0.705 ± 0.012 | 0.678 |
| sskmeans | 0.263 ± 0.030 | 0.575 ± 0.095 | 0.419 |

## ACC All na última sessão

| family | letter | pendigits | média |
|---|---|---|---|
| mst | 0.643 ± 0.038 | 0.868 ± 0.074 | 0.755 |
| svm-cv | 0.634 ± 0.030 | 0.860 ± 0.073 | 0.747 |
| auto-auroc | 0.635 ± 0.042 | 0.816 ± 0.126 | 0.725 |
| rf_msp | 0.590 ± 0.019 | 0.766 ± 0.083 | 0.678 |
| gauss | 0.565 ± 0.019 | 0.763 ± 0.117 | 0.664 |
| sskmeans | 0.192 ± 0.028 | 0.585 ± 0.160 | 0.388 |

## ACC New média (classes que estreiam na sessão)

| family | letter | pendigits | média |
|---|---|---|---|
| svm-cv | 0.370 ± 0.028 | 0.861 ± 0.065 | 0.615 |
| mst | 0.351 ± 0.042 | 0.865 ± 0.067 | 0.608 |
| auto-auroc | 0.359 ± 0.040 | 0.801 ± 0.150 | 0.580 |
| gauss | 0.281 ± 0.017 | 0.674 ± 0.095 | 0.478 |
| rf_msp | 0.248 ± 0.024 | 0.615 ± 0.057 | 0.432 |
| sskmeans | 0.180 ± 0.026 | 0.456 ± 0.175 | 0.318 |

## ACC Old média (classes já vistas, incl. descobertas)

| family | letter | pendigits | média |
|---|---|---|---|
| mst | 0.831 ± 0.025 | 0.911 ± 0.009 | 0.871 |
| auto-auroc | 0.826 ± 0.021 | 0.913 ± 0.008 | 0.870 |
| svm-cv | 0.821 ± 0.022 | 0.904 ± 0.010 | 0.862 |
| rf_msp | 0.829 ± 0.014 | 0.834 ± 0.015 | 0.831 |
| gauss | 0.751 ± 0.045 | 0.899 ± 0.010 | 0.825 |
| sskmeans | 0.306 ± 0.052 | 0.715 ± 0.049 | 0.510 |

## Esquecimento: acc_s0 (sessão 1) − acc_s0 (última); menor é melhor

| family | letter | pendigits | média |
|---|---|---|---|
| rf_msp | -0.001 ± 0.009 | 0.014 ± 0.017 | 0.007 |
| auto-auroc | 0.029 ± 0.026 | 0.044 ± 0.033 | 0.036 |
| mst | 0.024 ± 0.024 | 0.055 ± 0.020 | 0.040 |
| gauss | 0.060 ± 0.041 | 0.032 ± 0.021 | 0.046 |
| svm-cv | 0.034 ± 0.021 | 0.064 ± 0.018 | 0.049 |
| sskmeans | 0.228 ± 0.020 | 0.062 ± 0.028 | 0.145 |

## Tempo médio por sessão (s)

| family | letter | pendigits | média |
|---|---|---|---|
| sskmeans | 4.524 ± 1.240 | 0.383 ± 0.021 | 2.454 |
| rf_msp | 1.507 ± 0.086 | 1.191 ± 0.010 | 1.349 |
| svm-cv | 0.279 ± 0.008 | 0.174 ± 0.029 | 0.227 |
| auto-auroc | 0.170 ± 0.096 | 0.205 ± 0.081 | 0.188 |
| mst | 0.102 ± 0.010 | 0.244 ± 0.009 | 0.173 |
| gauss | 0.048 ± 0.041 | 0.073 ± 0.021 | 0.061 |

## Clusters espúrios por semente (somados nas sessões), pela classe majoritária

| family | base | de classe da sessão 0 | de classe já descoberta | de classe nova | tamanho médio |
|---|---|---|---|---|---|
| auto-auroc | letter | 0.0 | 0.0 | 4.6 | 68.0 |
| auto-auroc | pendigits | 0.0 | 0.8 | 2.4 | 89.0 |
| gauss | letter | 0.0 | 0.0 | 2.6 | 62.0 |
| gauss | pendigits | 0.0 | 0.6 | 1.4 | 78.0 |
| mst | letter | 0.0 | 0.0 | 3.6 | 60.0 |
| mst | pendigits | 0.0 | 1.0 | 2.6 | 97.0 |
| rf_msp | letter | 0.0 | 0.2 | 1.8 | 67.0 |
| rf_msp | pendigits | 0.2 | 1.2 | 1.4 | 68.0 |
| sskmeans | letter | 25.2 | 8.2 | 30.2 | 59.0 |
| sskmeans | pendigits | 0.0 | 0.0 | 0.0 | nan |
| svm-cv | letter | 0.0 | 0.0 | 6.2 | 67.0 |
| svm-cv | pendigits | 0.0 | 1.0 | 3.0 | 98.0 |

## Classes no modelo ao fim / classes verdadeiras (por semente)

| family | letter | pendigits |
|---|---|---|
| auto-auroc | 30/26, 32/26, 28/26, 30/26, 32/26 | 12/10, 13/10, 13/10, 15/10, 13/10 |
| gauss | 26/26, 27/26, 29/26, 28/26, 29/26 | 12/10, 12/10, 12/10, 12/10, 12/10 |
| mst | 30/26, 28/26, 28/26, 30/26, 30/26 | 14/10, 13/10, 13/10, 15/10, 13/10 |
| rf_msp | 27/26, 26/26, 25/26, 34/26, 26/26 | 13/10, 14/10, 12/10, 13/10, 12/10 |
| sskmeans | 114/26, 70/26, 71/26, 119/26, 69/26 | 9/10, 8/10, 9/10, 8/10, 8/10 |
| svm-cv | 32/26, 32/26, 32/26, 33/26, 32/26 | 14/10, 13/10, 14/10, 15/10, 14/10 |

## Wilcoxon pareado na ACC All média contra auto-auroc

| método | Δ vs auto-auroc | p (Wilcoxon) | pares |
|---|---|---|---|
| mst | 0.01 | 0.5 | 10 |
| svm-cv | 0.007 | 0.9453 | 10 |
| gauss | -0.069 | 0.0039 | 10 |
| rf_msp | -0.094 | 0.002 | 10 |
| sskmeans | -0.353 | 0.002 | 10 |
