## acc_all — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.227 ± 0.012 | 0.353 ± 0.029 | 0.528 ± 0.016 | 0.582 ± 0.012 | 0.126 ± 0.030 | 0.401 ± 0.018 | 0.316 ± 0.006 | 0.539 ± 0.015 | 0.419 ± 0.053 | 0.480 ± 0.056 | 0.513 ± 0.053 | 0.454 ± 0.014 | 0.435 ± 0.031 | 0.337 ± 0.004 | 0.363 ± 0.024 | 0.405 | 1.0 |

## acc_old — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.078 ± 0.019 | 0.553 ± 0.133 | 0.685 ± 0.027 | 0.315 ± 0.035 | 0.051 ± 0.055 | 0.435 ± 0.055 | 0.353 ± 0.071 | 0.762 ± 0.031 | 0.621 ± 0.072 | 0.738 ± 0.036 | 0.665 ± 0.103 | 0.629 ± 0.197 | 0.320 ± 0.023 | 0.742 ± 0.006 | 0.604 ± 0.100 | 0.503 | 1.0 |

## acc_new — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.376 ± 0.039 | 0.275 ± 0.085 | 0.521 ± 0.018 | 0.720 ± 0.001 | 0.154 ± 0.032 | 0.383 ± 0.048 | 0.278 ± 0.064 | 0.241 ± 0.062 | 0.317 ± 0.106 | 0.350 ± 0.076 | 0.435 ± 0.109 | 0.350 ± 0.126 | 0.478 ± 0.049 | 0.087 ± 0.006 | 0.263 ± 0.065 | 0.349 | 1.0 |

## auroc — K estimado

AUROC Old × New do escore de novidade

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.439 ± 0.011 | 0.411 ± 0.117 | 0.270 ± 0.108 | 0.155 ± 0.003 | 0.488 ± 0.040 | 0.609 ± 0.038 | 0.579 ± 0.020 | 0.740 ± 0.051 | 0.505 ± 0.139 | 0.614 ± 0.131 | 0.474 ± 0.061 | 0.195 ± 0.063 | 0.521 ± 0.031 | 0.676 ± 0.005 | 0.850 ± 0.049 | 0.502 | 1.0 |

## old_false_reject — K estimado

fração de Old de D_U rejeitada (alvo ≤ α)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.091 ± 0.014 | 0.054 ± 0.050 | 0.000 ± 0.000 | 0.000 ± 0.000 | 0.043 ± 0.035 | 0.104 ± 0.008 | 0.000 ± 0.000 | 0.090 ± 0.018 | 0.075 ± 0.044 | 0.044 ± 0.060 | 0.051 ± 0.040 | 0.000 ± 0.000 | 0.018 ± 0.040 | 0.099 ± 0.007 | 0.073 ± 0.033 | 0.049 | 1.0 |

## new_reject — K estimado

fração de New de D_U rejeitada (o resto é absorvido)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.091 ± 0.030 | 0.055 ± 0.066 | 0.000 ± 0.000 | 0.000 ± 0.000 | 0.043 ± 0.031 | 0.222 ± 0.055 | 0.000 ± 0.000 | 0.217 ± 0.033 | 0.097 ± 0.077 | 0.245 ± 0.101 | 0.209 ± 0.059 | 0.000 ± 0.000 | 0.047 ± 0.105 | 0.203 ± 0.009 | 0.247 ± 0.095 | 0.112 | 1.0 |

## K_new usado — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 2.0 | 1.2 | 0.0 | 0.0 | 6.2 | 2.0 | 0.0 | 2.4 | 2.4 | 2.8 | 2.2 | 0.0 | 0.4 | 2.0 | 5.2 |
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
