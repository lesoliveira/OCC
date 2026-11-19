## acc_all — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.265 ± 0.012 | 0.601 ± 0.029 | 0.448 ± 0.050 | 0.580 ± 0.015 | 0.114 ± 0.011 | 0.575 ± 0.016 | 0.340 ± 0.012 | 0.668 ± 0.015 | 0.702 ± 0.047 | 0.740 ± 0.119 | 0.840 ± 0.069 | 0.686 ± 0.004 | 0.646 ± 0.013 | 0.365 ± 0.005 | 0.368 ± 0.034 | 0.529 | 1.0 |

## acc_old — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.117 ± 0.021 | 0.722 ± 0.025 | 0.559 ± 0.039 | 0.655 ± 0.011 | 0.078 ± 0.020 | 0.509 ± 0.060 | 0.437 ± 0.042 | 0.926 ± 0.005 | 0.929 ± 0.087 | 0.889 ± 0.115 | 0.898 ± 0.106 | 0.831 ± 0.010 | 0.662 ± 0.006 | 0.645 ± 0.014 | 0.456 ± 0.198 | 0.621 | 1.0 |

## acc_new — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.412 ± 0.008 | 0.554 ± 0.041 | 0.443 ± 0.053 | 0.541 ± 0.024 | 0.128 ± 0.014 | 0.608 ± 0.051 | 0.240 ± 0.035 | 0.323 ± 0.038 | 0.588 ± 0.052 | 0.664 ± 0.133 | 0.811 ± 0.053 | 0.600 ± 0.009 | 0.640 ± 0.017 | 0.193 ± 0.014 | 0.331 ± 0.127 | 0.472 | 1.0 |

## auroc — K estimado

AUROC Old × New do escore de novidade

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.542 ± 0.023 | 0.904 ± 0.015 | 0.865 ± 0.032 | 0.950 ± 0.005 | 0.562 ± 0.012 | 0.865 ± 0.018 | 0.672 ± 0.024 | 0.917 ± 0.001 | 0.970 ± 0.007 | 0.957 ± 0.023 | 0.971 ± 0.026 | 0.988 ± 0.001 | 0.889 ± 0.015 | 0.648 ± 0.005 | 0.945 ± 0.012 | 0.843 | 1.0 |

## old_false_reject — K estimado

fração de Old de D_U rejeitada (alvo ≤ α)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.000 ± 0.000 | 0.005 ± 0.012 | 0.002 ± 0.003 | 0.014 ± 0.003 | 0.000 ± 0.000 | 0.005 ± 0.002 | 0.000 ± 0.000 | 0.002 ± 0.001 | 0.008 ± 0.002 | 0.004 ± 0.003 | 0.011 ± 0.002 | 0.004 ± 0.001 | 0.004 ± 0.008 | 0.000 ± 0.000 | 0.012 ± 0.013 | 0.005 | 1.0 |

## new_reject — K estimado

fração de New de D_U rejeitada (o resto é absorvido)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.007 ± 0.016 | 0.408 ± 0.056 | 0.239 ± 0.146 | 0.540 ± 0.018 | 0.000 ± 0.000 | 0.303 ± 0.033 | 0.000 ± 0.000 | 0.365 ± 0.040 | 0.645 ± 0.071 | 0.622 ± 0.191 | 0.810 ± 0.188 | 0.855 ± 0.028 | 0.514 ± 0.081 | 0.000 ± 0.000 | 0.264 ± 0.188 | 0.372 | 1.0 |

## K_new usado — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.4 | 3.6 | 10.2 | 2.0 | 0.0 | 5.0 | 0.0 | 6.8 | 6.0 | 4.6 | 5.8 | 3.8 | 4.8 | 0.0 | 8.8 |
| (verdadeiro) | 6.0 | 5.0 | 4.0 | 3.0 | 50.0 | 13.0 | 9.0 | 7.0 | 5.0 | 5.0 | 5.0 | 3.0 | 4.0 | 5.0 | 6.0 |

## Escolha do auto-auroc — K estimado

| base | escolhas nas sementes |
|---|---|
| census | dic×3, knn×1, svm@3×1 |
| cnae9 | gauss×5 |
| covertype | gauss×3, mst×1, svm@10×1 |
| har | gauss×5 |
| helena | svm@0.3×2, gauss×1, svm@10×1, mst×1 |
| isolet | dic×4, gauss×1 |
| krvsk | mst×4, knn×1 |
| letter | svm@10×4, mst×1 |
| mfeat | gauss×4, svm@3×1 |
| optdigits | dic×3, svm@3×1, gauss×1 |
| pendigits | mst×3, gauss×2 |
| satimage | mst×4, knn×1 |
| segment | dic×5 |
| volkert | mst×5 |
| vowel | svm@10×5 |

## Friedman nas bases (média das sementes por base) — K estimado

(precisa de ao menos 3 bases e 3 métodos)
