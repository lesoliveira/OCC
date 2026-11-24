## acc_all — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.228 ± 0.015 | 0.568 ± 0.016 | 0.462 ± 0.068 | 0.690 ± 0.014 | 0.127 ± 0.024 | 0.556 ± 0.020 | 0.318 ± 0.008 | 0.628 ± 0.013 | 0.854 ± 0.014 | 0.746 ± 0.065 | 0.859 ± 0.052 | 0.725 ± 0.030 | 0.668 ± 0.021 | 0.318 ± 0.003 | 0.366 ± 0.025 | 0.541 | 1.0 |

## acc_old — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.055 ± 0.017 | 0.721 ± 0.024 | 0.696 ± 0.021 | 0.887 ± 0.014 | 0.044 ± 0.057 | 0.447 ± 0.120 | 0.335 ± 0.061 | 0.873 ± 0.022 | 0.950 ± 0.021 | 0.836 ± 0.175 | 0.960 ± 0.011 | 0.787 ± 0.009 | 0.663 ± 0.003 | 0.723 ± 0.009 | 0.668 ± 0.067 | 0.643 | 1.0 |

## acc_new — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.402 ± 0.033 | 0.508 ± 0.029 | 0.452 ± 0.072 | 0.588 ± 0.021 | 0.159 ± 0.023 | 0.610 ± 0.087 | 0.300 ± 0.050 | 0.301 ± 0.027 | 0.806 ± 0.025 | 0.701 ± 0.055 | 0.807 ± 0.073 | 0.688 ± 0.051 | 0.669 ± 0.029 | 0.068 ± 0.002 | 0.240 ± 0.059 | 0.487 | 1.0 |

## auroc — K estimado

AUROC Old × New do escore de novidade

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.542 ± 0.023 | 0.904 ± 0.015 | 0.865 ± 0.032 | 0.950 ± 0.005 | 0.562 ± 0.012 | 0.865 ± 0.018 | 0.672 ± 0.024 | 0.917 ± 0.001 | 0.970 ± 0.007 | 0.957 ± 0.023 | 0.971 ± 0.026 | 0.988 ± 0.001 | 0.889 ± 0.015 | 0.648 ± 0.005 | 0.945 ± 0.012 | 0.843 | 1.0 |

## old_false_reject — K estimado

fração de Old de D_U rejeitada (alvo ≤ α)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.000 ± 0.000 | 0.000 ± 0.000 | 0.003 ± 0.004 | 0.018 ± 0.005 | 0.003 ± 0.002 | 0.007 ± 0.002 | 0.000 ± 0.000 | 0.002 ± 0.001 | 0.011 ± 0.001 | 0.003 ± 0.002 | 0.017 ± 0.003 | 0.021 ± 0.010 | 0.004 ± 0.004 | 0.060 ± 0.007 | 0.032 ± 0.012 | 0.012 | 1.0 |

## new_reject — K estimado

fração de New de D_U rejeitada (o resto é absorvido)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.000 ± 0.000 | 0.377 ± 0.053 | 0.261 ± 0.163 | 0.783 ± 0.028 | 0.010 ± 0.007 | 0.276 ± 0.050 | 0.000 ± 0.000 | 0.363 ± 0.036 | 0.853 ± 0.024 | 0.676 ± 0.141 | 0.870 ± 0.092 | 0.918 ± 0.053 | 0.541 ± 0.066 | 0.122 ± 0.010 | 0.464 ± 0.109 | 0.434 | 1.0 |

## K_new usado — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.0 | 2.6 | 5.4 | 2.0 | 2.0 | 3.4 | 0.0 | 4.6 | 5.0 | 3.6 | 5.0 | 2.2 | 3.4 | 4.4 | 6.8 |
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
