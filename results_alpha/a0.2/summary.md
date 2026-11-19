## acc_all — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.268 ± 0.016 | 0.573 ± 0.035 | 0.354 ± 0.049 | 0.762 ± 0.017 | 0.117 ± 0.012 | 0.398 ± 0.034 | 0.340 ± 0.012 | 0.597 ± 0.019 | 0.812 ± 0.057 | 0.678 ± 0.043 | 0.877 ± 0.019 | 0.731 ± 0.003 | 0.646 ± 0.020 | 0.365 ± 0.005 | 0.306 ± 0.042 | 0.522 | 1.0 |

## acc_old — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.117 ± 0.021 | 0.773 ± 0.078 | 0.580 ± 0.036 | 0.668 ± 0.080 | 0.079 ± 0.015 | 0.589 ± 0.024 | 0.437 ± 0.042 | 0.810 ± 0.061 | 0.947 ± 0.015 | 0.680 ± 0.162 | 0.939 ± 0.015 | 0.760 ± 0.008 | 0.662 ± 0.004 | 0.645 ± 0.014 | 0.789 ± 0.119 | 0.632 | 1.0 |

## acc_new — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.418 ± 0.016 | 0.496 ± 0.051 | 0.344 ± 0.052 | 0.810 ± 0.065 | 0.131 ± 0.014 | 0.302 ± 0.058 | 0.240 ± 0.035 | 0.313 ± 0.076 | 0.745 ± 0.082 | 0.677 ± 0.024 | 0.845 ± 0.021 | 0.713 ± 0.000 | 0.640 ± 0.027 | 0.193 ± 0.014 | 0.104 ± 0.039 | 0.465 | 1.0 |

## auroc — K estimado

AUROC Old × New do escore de novidade

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.542 ± 0.023 | 0.904 ± 0.015 | 0.865 ± 0.032 | 0.950 ± 0.005 | 0.562 ± 0.012 | 0.865 ± 0.018 | 0.672 ± 0.024 | 0.917 ± 0.001 | 0.970 ± 0.007 | 0.957 ± 0.023 | 0.971 ± 0.026 | 0.988 ± 0.001 | 0.889 ± 0.015 | 0.648 ± 0.005 | 0.945 ± 0.012 | 0.843 | 1.0 |

## old_false_reject — K estimado

fração de Old de D_U rejeitada (alvo ≤ α)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.000 ± 0.000 | 0.121 ± 0.066 | 0.017 ± 0.004 | 0.055 ± 0.065 | 0.014 ± 0.008 | 0.132 ± 0.066 | 0.000 ± 0.000 | 0.061 ± 0.050 | 0.020 ± 0.006 | 0.006 ± 0.003 | 0.027 ± 0.007 | 0.094 ± 0.008 | 0.018 ± 0.011 | 0.000 ± 0.000 | 0.145 ± 0.077 | 0.047 | 1.0 |

## new_reject — K estimado

fração de New de D_U rejeitada (o resto é absorvido)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.000 ± 0.000 | 0.643 ± 0.217 | 0.475 ± 0.157 | 0.787 ± 0.103 | 0.028 ± 0.017 | 0.666 ± 0.173 | 0.000 ± 0.000 | 0.409 ± 0.139 | 0.888 ± 0.003 | 0.622 ± 0.104 | 0.911 ± 0.035 | 0.966 ± 0.002 | 0.731 ± 0.036 | 0.000 ± 0.000 | 0.861 ± 0.095 | 0.532 | 1.0 |

## K_new usado — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.0 | 3.6 | 7.0 | 2.0 | 1.6 | 2.0 | 0.0 | 8.6 | 4.4 | 2.8 | 5.0 | 2.0 | 2.0 | 0.0 | 13.0 |
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
