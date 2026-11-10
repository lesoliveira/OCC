## acc_all — K estimado

| family | letter | média | rank médio |
|---|---|---|---|
| mst | 0.660 ± 0.006 | 0.660 | 1.0 |
| modes | 0.636 ± 0.007 | 0.636 | 2.0 |
| knn | 0.634 ± 0.018 | 0.634 | 3.0 |
| dic | 0.626 ± 0.007 | 0.626 | 4.0 |
| gauss | 0.620 ± 0.006 | 0.620 | 5.0 |
| rf_msp | 0.592 ± 0.004 | 0.592 | 6.0 |
| lr_msp | 0.504 ± 0.006 | 0.504 | 7.0 |
| svm | 0.471 ± 0.012 | 0.471 | 8.0 |
| sskmeans | 0.313 ± 0.014 | 0.313 | 9.0 |
| kmeans | 0.241 ± 0.007 | 0.241 | 10.0 |

## acc_old — K estimado

| family | letter | média | rank médio |
|---|---|---|---|
| mst | 0.915 ± 0.003 | 0.915 | 1.0 |
| modes | 0.896 ± 0.005 | 0.896 | 2.0 |
| knn | 0.856 ± 0.005 | 0.856 | 3.0 |
| dic | 0.836 ± 0.007 | 0.836 | 4.0 |
| gauss | 0.815 ± 0.006 | 0.815 | 5.0 |
| rf_msp | 0.811 ± 0.004 | 0.811 | 6.0 |
| svm | 0.597 ± 0.009 | 0.597 | 7.0 |
| lr_msp | 0.586 ± 0.006 | 0.586 | 8.0 |
| sskmeans | 0.277 ± 0.015 | 0.277 | 9.0 |
| kmeans | 0.245 ± 0.012 | 0.245 | 10.0 |

## acc_new — K estimado

| family | letter | média | rank médio |
|---|---|---|---|
| lr_msp | 0.395 ± 0.010 | 0.395 | 1.0 |
| gauss | 0.361 ± 0.010 | 0.361 | 2.0 |
| sskmeans | 0.360 ± 0.015 | 0.360 | 3.0 |
| dic | 0.346 ± 0.010 | 0.346 | 4.0 |
| knn | 0.338 ± 0.037 | 0.338 | 5.0 |
| mst | 0.321 ± 0.011 | 0.321 | 6.0 |
| svm | 0.303 ± 0.036 | 0.303 | 7.0 |
| rf_msp | 0.298 ± 0.011 | 0.298 | 8.0 |
| modes | 0.291 ± 0.017 | 0.291 | 9.0 |
| kmeans | 0.236 ± 0.008 | 0.236 | 10.0 |

## auroc — K estimado

AUROC Old × New do escore de novidade

| family | letter | média | rank médio |
|---|---|---|---|
| mst | 0.914 ± 0.002 | 0.914 | 1.0 |
| modes | 0.899 ± 0.006 | 0.899 | 2.0 |
| rf_msp | 0.896 ± 0.004 | 0.896 | 3.0 |
| dic | 0.894 ± 0.006 | 0.894 | 4.0 |
| knn | 0.875 ± 0.003 | 0.875 | 5.0 |
| gauss | 0.854 ± 0.003 | 0.854 | 6.0 |
| svm | 0.661 ± 0.003 | 0.661 | 7.0 |
| lr_msp | 0.629 ± 0.004 | 0.629 | 8.0 |

## old_false_reject — K estimado

fração de Old de D_U rejeitada (alvo ≤ α)

| family | letter | média | rank médio |
|---|---|---|---|
| gauss | 0.001 ± 0.001 | 0.001 | 1.0 |
| knn | 0.001 ± 0.000 | 0.001 | 2.0 |
| dic | 0.001 ± 0.001 | 0.001 | 3.0 |
| mst | 0.002 ± 0.000 | 0.002 | 4.0 |
| svm | 0.003 ± 0.001 | 0.003 | 5.0 |
| modes | 0.004 ± 0.001 | 0.004 | 6.0 |
| rf_msp | 0.008 ± 0.003 | 0.008 | 7.0 |
| lr_msp | 0.092 ± 0.008 | 0.092 | 8.0 |

## new_reject — K estimado

fração de New de D_U rejeitada (o resto é absorvido)

| family | letter | média | rank médio |
|---|---|---|---|
| modes | 0.371 ± 0.026 | 0.371 | 1.0 |
| mst | 0.350 ± 0.009 | 0.350 | 2.0 |
| gauss | 0.302 ± 0.005 | 0.302 | 3.0 |
| dic | 0.286 ± 0.006 | 0.286 | 4.0 |
| knn | 0.282 ± 0.003 | 0.282 | 5.0 |
| svm | 0.190 ± 0.011 | 0.190 | 6.0 |
| rf_msp | 0.183 ± 0.021 | 0.183 | 7.0 |
| lr_msp | 0.180 ± 0.008 | 0.180 | 8.0 |

## K_new usado — K estimado

| family | letter |
|---|---|
| dic | 3.2 |
| gauss | 3.2 |
| knn | 2.8 |
| lr_msp | 2.0 |
| modes | 4.2 |
| mst | 4.6 |
| rf_msp | 2.0 |
| sskmeans | 1.0 |
| svm | 2.8 |
| (verdadeiro) | 7.0 |

## Wilcoxon pareado em acc_all contra o melhor OCC (mst) — K estimado

| método | Δ média vs mst | p (Wilcoxon) | pares |
|---|---|---|---|
| modes | -0.024 | — | 5 |
| knn | -0.026 | — | 5 |
| dic | -0.034 | — | 5 |
| gauss | -0.04 | — | 5 |
| rf_msp | -0.069 | — | 5 |
| lr_msp | -0.156 | — | 5 |
| svm | -0.189 | — | 5 |
| sskmeans | -0.347 | — | 5 |
| kmeans | -0.42 | — | 5 |
