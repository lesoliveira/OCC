## acc_all — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.268 ± 0.016 | 0.549 ± 0.034 | 0.475 ± 0.050 | 0.700 ± 0.010 | 0.114 ± 0.011 | 0.467 ± 0.031 | 0.340 ± 0.012 | 0.578 ± 0.013 | 0.839 ± 0.033 | 0.630 ± 0.064 | 0.844 ± 0.069 | 0.747 ± 0.003 | 0.658 ± 0.023 | 0.365 ± 0.005 | 0.389 ± 0.015 | 0.531 | 1.0 |

## acc_old — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.117 ± 0.021 | 0.769 ± 0.112 | 0.561 ± 0.042 | 0.908 ± 0.041 | 0.078 ± 0.020 | 0.514 ± 0.109 | 0.437 ± 0.042 | 0.825 ± 0.025 | 0.921 ± 0.085 | 0.653 ± 0.103 | 0.887 ± 0.111 | 0.807 ± 0.007 | 0.664 ± 0.002 | 0.645 ± 0.014 | 0.521 ± 0.206 | 0.621 | 1.0 |

## acc_new — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.418 ± 0.016 | 0.464 ± 0.028 | 0.471 ± 0.054 | 0.593 ± 0.024 | 0.128 ± 0.014 | 0.443 ± 0.095 | 0.240 ± 0.035 | 0.249 ± 0.025 | 0.797 ± 0.018 | 0.619 ± 0.047 | 0.822 ± 0.048 | 0.711 ± 0.001 | 0.656 ± 0.031 | 0.193 ± 0.014 | 0.334 ± 0.107 | 0.476 | 1.0 |

## auroc — K estimado

AUROC Old × New do escore de novidade

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.542 ± 0.023 | 0.904 ± 0.015 | 0.865 ± 0.032 | 0.950 ± 0.005 | 0.562 ± 0.012 | 0.865 ± 0.018 | 0.672 ± 0.024 | 0.917 ± 0.001 | 0.970 ± 0.007 | 0.957 ± 0.023 | 0.971 ± 0.026 | 0.988 ± 0.001 | 0.889 ± 0.015 | 0.648 ± 0.005 | 0.945 ± 0.012 | 0.843 | 1.0 |

## old_false_reject — K estimado

fração de Old de D_U rejeitada (alvo ≤ α)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.000 ± 0.000 | 0.063 ± 0.043 | 0.003 ± 0.004 | 0.049 ± 0.046 | 0.000 ± 0.000 | 0.039 ± 0.040 | 0.000 ± 0.000 | 0.002 ± 0.002 | 0.012 ± 0.003 | 0.003 ± 0.002 | 0.016 ± 0.003 | 0.032 ± 0.005 | 0.002 ± 0.004 | 0.000 ± 0.000 | 0.025 ± 0.017 | 0.016 | 1.0 |

## new_reject — K estimado

fração de New de D_U rejeitada (o resto é absorvido)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.000 ± 0.000 | 0.546 ± 0.161 | 0.213 ± 0.133 | 0.806 ± 0.045 | 0.000 ± 0.000 | 0.434 ± 0.168 | 0.000 ± 0.000 | 0.075 ± 0.049 | 0.828 ± 0.060 | 0.507 ± 0.130 | 0.858 ± 0.099 | 0.943 ± 0.006 | 0.522 ± 0.102 | 0.000 ± 0.000 | 0.333 ± 0.198 | 0.404 | 1.0 |

## K_new usado — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.0 | 4.0 | 3.8 | 2.0 | 0.0 | 2.0 | 0.0 | 2.0 | 4.8 | 2.4 | 4.6 | 2.0 | 2.0 | 0.0 | 2.4 |
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
