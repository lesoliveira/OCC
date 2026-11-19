## acc_all — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.268 ± 0.016 | 0.625 ± 0.015 | 0.421 ± 0.073 | 0.706 ± 0.010 | 0.114 ± 0.011 | 0.586 ± 0.022 | 0.340 ± 0.012 | 0.669 ± 0.010 | 0.827 ± 0.030 | 0.835 ± 0.060 | 0.861 ± 0.051 | 0.695 ± 0.003 | 0.648 ± 0.028 | 0.377 ± 0.012 | 0.344 ± 0.046 | 0.554 | 1.0 |

## acc_old — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.117 ± 0.021 | 0.774 ± 0.110 | 0.563 ± 0.044 | 0.928 ± 0.011 | 0.080 ± 0.018 | 0.495 ± 0.095 | 0.437 ± 0.042 | 0.906 ± 0.007 | 0.961 ± 0.011 | 0.952 ± 0.009 | 0.959 ± 0.010 | 0.825 ± 0.006 | 0.658 ± 0.009 | 0.623 ± 0.024 | 0.629 ± 0.147 | 0.661 | 1.0 |

## acc_new — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.418 ± 0.016 | 0.567 ± 0.036 | 0.415 ± 0.078 | 0.592 ± 0.019 | 0.127 ± 0.013 | 0.632 ± 0.079 | 0.240 ± 0.035 | 0.353 ± 0.033 | 0.760 ± 0.046 | 0.776 ± 0.087 | 0.811 ± 0.072 | 0.618 ± 0.004 | 0.645 ± 0.037 | 0.224 ± 0.032 | 0.225 ± 0.126 | 0.493 | 1.0 |

## auroc — K estimado

AUROC Old × New do escore de novidade

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.542 ± 0.023 | 0.904 ± 0.015 | 0.865 ± 0.032 | 0.950 ± 0.005 | 0.562 ± 0.012 | 0.865 ± 0.018 | 0.672 ± 0.024 | 0.917 ± 0.001 | 0.970 ± 0.007 | 0.957 ± 0.023 | 0.971 ± 0.026 | 0.988 ± 0.001 | 0.889 ± 0.015 | 0.648 ± 0.005 | 0.945 ± 0.012 | 0.843 | 1.0 |

## old_false_reject — K estimado

fração de Old de D_U rejeitada (alvo ≤ α)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.000 ± 0.000 | 0.003 ± 0.005 | 0.005 ± 0.005 | 0.021 ± 0.005 | 0.003 ± 0.004 | 0.007 ± 0.002 | 0.000 ± 0.000 | 0.005 ± 0.002 | 0.014 ± 0.004 | 0.006 ± 0.004 | 0.018 ± 0.002 | 0.005 ± 0.001 | 0.010 ± 0.010 | 0.034 ± 0.020 | 0.036 ± 0.013 | 0.011 | 1.0 |

## new_reject — K estimado

fração de New de D_U rejeitada (o resto é absorvido)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.000 ± 0.000 | 0.513 ± 0.060 | 0.311 ± 0.193 | 0.800 ± 0.021 | 0.010 ± 0.008 | 0.354 ± 0.056 | 0.000 ± 0.000 | 0.432 ± 0.037 | 0.865 ± 0.023 | 0.789 ± 0.089 | 0.889 ± 0.107 | 0.884 ± 0.004 | 0.571 ± 0.090 | 0.079 ± 0.046 | 0.529 ± 0.122 | 0.468 | 1.0 |

## K_new usado — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.0 | 4.4 | 12.4 | 2.0 | 1.6 | 5.0 | 0.0 | 9.0 | 6.2 | 5.0 | 5.6 | 4.0 | 6.0 | 2.0 | 16.8 |
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
