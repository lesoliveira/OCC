## acc_all — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.268 ± 0.016 | 0.570 ± 0.021 | 0.465 ± 0.056 | 0.703 ± 0.010 | 0.114 ± 0.011 | 0.479 ± 0.038 | 0.340 ± 0.012 | 0.605 ± 0.006 | 0.852 ± 0.011 | 0.629 ± 0.063 | 0.857 ± 0.053 | 0.747 ± 0.003 | 0.662 ± 0.037 | 0.365 ± 0.005 | 0.375 ± 0.026 | 0.536 | 1.0 |

## acc_old — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.117 ± 0.021 | 0.787 ± 0.094 | 0.562 ± 0.043 | 0.923 ± 0.012 | 0.078 ± 0.020 | 0.465 ± 0.129 | 0.437 ± 0.042 | 0.850 ± 0.045 | 0.962 ± 0.010 | 0.653 ± 0.103 | 0.960 ± 0.011 | 0.808 ± 0.007 | 0.664 ± 0.002 | 0.645 ± 0.014 | 0.484 ± 0.180 | 0.626 | 1.0 |

## acc_new — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.418 ± 0.016 | 0.485 ± 0.035 | 0.460 ± 0.059 | 0.590 ± 0.012 | 0.128 ± 0.014 | 0.487 ± 0.118 | 0.240 ± 0.035 | 0.279 ± 0.057 | 0.797 ± 0.020 | 0.617 ± 0.045 | 0.804 ± 0.074 | 0.711 ± 0.001 | 0.662 ± 0.052 | 0.193 ± 0.014 | 0.330 ± 0.104 | 0.480 | 1.0 |

## auroc — K estimado

AUROC Old × New do escore de novidade

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.542 ± 0.023 | 0.904 ± 0.015 | 0.865 ± 0.032 | 0.950 ± 0.005 | 0.562 ± 0.012 | 0.865 ± 0.018 | 0.672 ± 0.024 | 0.917 ± 0.001 | 0.970 ± 0.007 | 0.957 ± 0.023 | 0.971 ± 0.026 | 0.988 ± 0.001 | 0.889 ± 0.015 | 0.648 ± 0.005 | 0.945 ± 0.012 | 0.843 | 1.0 |

## old_false_reject — K estimado

fração de Old de D_U rejeitada (alvo ≤ α)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.000 ± 0.000 | 0.038 ± 0.053 | 0.003 ± 0.004 | 0.028 ± 0.023 | 0.000 ± 0.000 | 0.027 ± 0.040 | 0.000 ± 0.000 | 0.007 ± 0.014 | 0.012 ± 0.003 | 0.003 ± 0.002 | 0.016 ± 0.003 | 0.030 ± 0.003 | 0.003 ± 0.004 | 0.000 ± 0.000 | 0.029 ± 0.021 | 0.013 | 1.0 |

## new_reject — K estimado

fração de New de D_U rejeitada (o resto é absorvido)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.000 ± 0.000 | 0.502 ± 0.196 | 0.257 ± 0.160 | 0.787 ± 0.028 | 0.000 ± 0.000 | 0.365 ± 0.165 | 0.000 ± 0.000 | 0.251 ± 0.022 | 0.847 ± 0.023 | 0.508 ± 0.128 | 0.866 ± 0.094 | 0.946 ± 0.005 | 0.514 ± 0.081 | 0.000 ± 0.000 | 0.317 ± 0.180 | 0.411 | 1.0 |

## K_new usado — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.0 | 3.6 | 5.4 | 2.0 | 0.0 | 2.0 | 0.0 | 3.0 | 5.0 | 2.4 | 5.0 | 2.0 | 2.6 | 0.0 | 3.2 |
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
