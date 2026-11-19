## acc_all — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.268 ± 0.016 | 0.602 ± 0.024 | 0.428 ± 0.070 | 0.706 ± 0.010 | 0.114 ± 0.012 | 0.579 ± 0.017 | 0.340 ± 0.012 | 0.659 ± 0.007 | 0.866 ± 0.016 | 0.752 ± 0.054 | 0.859 ± 0.051 | 0.686 ± 0.003 | 0.687 ± 0.015 | 0.370 ± 0.010 | 0.347 ± 0.040 | 0.551 | 1.0 |

## acc_old — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.117 ± 0.021 | 0.729 ± 0.018 | 0.563 ± 0.044 | 0.928 ± 0.011 | 0.080 ± 0.018 | 0.495 ± 0.095 | 0.437 ± 0.042 | 0.906 ± 0.007 | 0.962 ± 0.009 | 0.878 ± 0.109 | 0.960 ± 0.010 | 0.828 ± 0.005 | 0.663 ± 0.006 | 0.643 ± 0.016 | 0.629 ± 0.147 | 0.655 | 1.0 |

## acc_new — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.418 ± 0.016 | 0.552 ± 0.031 | 0.422 ± 0.075 | 0.591 ± 0.019 | 0.127 ± 0.014 | 0.621 ± 0.071 | 0.240 ± 0.035 | 0.329 ± 0.016 | 0.818 ± 0.029 | 0.689 ± 0.028 | 0.809 ± 0.072 | 0.602 ± 0.002 | 0.696 ± 0.018 | 0.201 ± 0.025 | 0.230 ± 0.117 | 0.490 | 1.0 |

## auroc — K estimado

AUROC Old × New do escore de novidade

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.542 ± 0.023 | 0.904 ± 0.015 | 0.865 ± 0.032 | 0.950 ± 0.005 | 0.562 ± 0.012 | 0.865 ± 0.018 | 0.672 ± 0.024 | 0.917 ± 0.001 | 0.970 ± 0.007 | 0.957 ± 0.023 | 0.971 ± 0.026 | 0.988 ± 0.001 | 0.889 ± 0.015 | 0.648 ± 0.005 | 0.945 ± 0.012 | 0.843 | 1.0 |

## old_false_reject — K estimado

fração de Old de D_U rejeitada (alvo ≤ α)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.000 ± 0.000 | 0.000 ± 0.000 | 0.005 ± 0.005 | 0.021 ± 0.005 | 0.003 ± 0.004 | 0.007 ± 0.002 | 0.000 ± 0.000 | 0.003 ± 0.002 | 0.012 ± 0.002 | 0.005 ± 0.001 | 0.017 ± 0.003 | 0.003 ± 0.001 | 0.006 ± 0.005 | 0.005 ± 0.011 | 0.036 ± 0.013 | 0.008 | 1.0 |

## new_reject — K estimado

fração de New de D_U rejeitada (o resto é absorvido)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média | rank médio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.000 ± 0.000 | 0.416 ± 0.055 | 0.303 ± 0.189 | 0.798 ± 0.021 | 0.008 ± 0.009 | 0.330 ± 0.041 | 0.000 ± 0.000 | 0.409 ± 0.028 | 0.860 ± 0.027 | 0.708 ± 0.119 | 0.877 ± 0.097 | 0.823 ± 0.003 | 0.565 ± 0.096 | 0.018 ± 0.040 | 0.497 ± 0.135 | 0.441 | 1.0 |

## K_new usado — K estimado

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.0 | 3.6 | 10.0 | 2.0 | 1.2 | 4.2 | 0.0 | 6.2 | 5.0 | 3.8 | 5.0 | 3.0 | 3.8 | 0.4 | 12.8 |
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
