## ACC All média nas sessões

| family | letter | pendigits | média |
|---|---|---|---|
| svm-cv | 0.717 ± 0.010 | 0.875 ± 0.021 | 0.796 |
| mst | 0.708 ± 0.015 | 0.880 ± 0.025 | 0.794 |
| auto-auroc | 0.710 ± 0.015 | 0.861 ± 0.050 | 0.785 |
| gauss | 0.617 ± 0.041 | 0.799 ± 0.026 | 0.708 |
| rf_msp | 0.650 ± 0.012 | 0.708 ± 0.017 | 0.679 |
| sskmeans | 0.263 ± 0.030 | 0.575 ± 0.095 | 0.419 |

## ACC All na última sessão

| family | letter | pendigits | média |
|---|---|---|---|
| mst | 0.679 ± 0.042 | 0.870 ± 0.074 | 0.775 |
| svm-cv | 0.684 ± 0.053 | 0.863 ± 0.074 | 0.774 |
| auto-auroc | 0.674 ± 0.051 | 0.818 ± 0.126 | 0.746 |
| rf_msp | 0.592 ± 0.020 | 0.778 ± 0.058 | 0.685 |
| gauss | 0.588 ± 0.019 | 0.763 ± 0.117 | 0.676 |
| sskmeans | 0.192 ± 0.028 | 0.585 ± 0.160 | 0.388 |

## ACC New média (classes que estreiam na sessão)

| family | letter | pendigits | média |
|---|---|---|---|
| svm-cv | 0.465 ± 0.038 | 0.862 ± 0.065 | 0.664 |
| mst | 0.417 ± 0.027 | 0.866 ± 0.069 | 0.641 |
| auto-auroc | 0.430 ± 0.016 | 0.801 ± 0.150 | 0.616 |
| gauss | 0.317 ± 0.019 | 0.674 ± 0.095 | 0.495 |
| rf_msp | 0.250 ± 0.022 | 0.627 ± 0.036 | 0.438 |
| sskmeans | 0.180 ± 0.026 | 0.456 ± 0.175 | 0.318 |

## ACC Old média (classes já vistas, incl. descobertas)

| family | letter | pendigits | média |
|---|---|---|---|
| auto-auroc | 0.835 ± 0.018 | 0.913 ± 0.007 | 0.874 |
| mst | 0.838 ± 0.020 | 0.910 ± 0.008 | 0.874 |
| svm-cv | 0.831 ± 0.021 | 0.904 ± 0.010 | 0.868 |
| rf_msp | 0.825 ± 0.014 | 0.834 ± 0.015 | 0.830 |
| gauss | 0.750 ± 0.053 | 0.899 ± 0.010 | 0.824 |
| sskmeans | 0.306 ± 0.052 | 0.715 ± 0.049 | 0.510 |

## Esquecimento: acc_s0 (sessão 1) − acc_s0 (última); menor é melhor

| family | letter | pendigits | média |
|---|---|---|---|
| rf_msp | -0.003 ± 0.010 | 0.014 ± 0.017 | 0.005 |
| auto-auroc | 0.029 ± 0.026 | 0.044 ± 0.033 | 0.036 |
| mst | 0.024 ± 0.024 | 0.055 ± 0.020 | 0.040 |
| svm-cv | 0.034 ± 0.022 | 0.064 ± 0.019 | 0.049 |
| gauss | 0.069 ± 0.060 | 0.032 ± 0.021 | 0.051 |
| sskmeans | 0.228 ± 0.020 | 0.062 ± 0.028 | 0.145 |

## Tempo médio por sessão (s)

| family | letter | pendigits | média |
|---|---|---|---|
| sskmeans | 4.485 ± 1.292 | 0.386 ± 0.019 | 2.435 |
| rf_msp | 1.502 ± 0.093 | 1.192 ± 0.008 | 1.347 |
| svm-cv | 0.270 ± 0.008 | 0.163 ± 0.030 | 0.216 |
| auto-auroc | 0.179 ± 0.086 | 0.203 ± 0.080 | 0.191 |
| mst | 0.106 ± 0.009 | 0.241 ± 0.012 | 0.174 |
| gauss | 0.051 ± 0.053 | 0.075 ± 0.020 | 0.063 |

## Clusters espúrios por semente (somados nas sessões), pela classe majoritária

| family | base | de classe da sessão 0 | de classe já descoberta | de classe nova | tamanho médio |
|---|---|---|---|---|---|
| auto-auroc | letter | 0.0 | 0.0 | 1.6 | 109.0 |
| auto-auroc | pendigits | 0.0 | 0.8 | 2.0 | 93.0 |
| gauss | letter | 0.0 | 0.0 | 0.8 | 121.0 |
| gauss | pendigits | 0.0 | 0.6 | 1.4 | 78.0 |
| mst | letter | 0.0 | 0.0 | 1.0 | 112.0 |
| mst | pendigits | 0.0 | 1.0 | 2.0 | 106.0 |
| rf_msp | letter | 0.0 | 0.0 | 0.4 | 49.0 |
| rf_msp | pendigits | 0.2 | 1.2 | 1.2 | 68.0 |
| sskmeans | letter | 25.2 | 8.2 | 30.2 | 59.0 |
| sskmeans | pendigits | 0.0 | 0.0 | 0.0 | nan |
| svm-cv | letter | 0.0 | 0.0 | 2.2 | 98.0 |
| svm-cv | pendigits | 0.0 | 1.0 | 2.0 | 115.0 |

## Classes no modelo ao fim / classes verdadeiras (por semente)

| family | letter | pendigits |
|---|---|---|
| auto-auroc | 27/26, 29/26, 25/26, 27/26, 29/26 | 12/10, 12/10, 13/10, 14/10, 13/10 |
| gauss | 25/26, 26/26, 25/26, 26/26, 26/26 | 12/10, 12/10, 12/10, 12/10, 12/10 |
| mst | 27/26, 27/26, 25/26, 27/26, 28/26 | 13/10, 12/10, 13/10, 14/10, 13/10 |
| rf_msp | 25/26, 26/26, 25/26, 27/26, 26/26 | 13/10, 14/10, 12/10, 12/10, 12/10 |
| sskmeans | 114/26, 70/26, 71/26, 119/26, 69/26 | 9/10, 8/10, 9/10, 8/10, 8/10 |
| svm-cv | 29/26, 29/26, 25/26, 28/26, 29/26 | 13/10, 12/10, 13/10, 14/10, 13/10 |

## Wilcoxon pareado na ACC All média contra auto-auroc

| método | Δ vs auto-auroc | p (Wilcoxon) | pares |
|---|---|---|---|
| svm-cv | 0.011 | 0.5469 | 10 |
| mst | 0.009 | 0.75 | 10 |
| gauss | -0.078 | 0.0039 | 10 |
| rf_msp | -0.106 | 0.002 | 10 |
| sskmeans | -0.366 | 0.002 | 10 |
