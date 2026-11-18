## ACC All média nas sessões

| family | covertype | helena | isolet | letter | pendigits | volkert | média |
|---|---|---|---|---|---|---|---|
| auto-auroc | 0.130 ± 0.019 | 0.027 ± 0.009 | 0.519 ± 0.022 | 0.600 ± 0.010 | 0.653 ± 0.053 | 0.309 ± 0.005 | 0.373 |

## ACC All na última sessão

| family | covertype | helena | isolet | letter | pendigits | volkert | média |
|---|---|---|---|---|---|---|---|
| auto-auroc | 0.122 ± 0.020 | 0.016 ± 0.008 | 0.346 ± 0.012 | 0.653 ± 0.036 | 0.694 ± 0.068 | 0.387 ± 0.012 | 0.370 |

## ACC New média (classes que estreiam na sessão)

| family | covertype | helena | isolet | letter | pendigits | volkert | média |
|---|---|---|---|---|---|---|---|
| auto-auroc | 0.094 ± 0.021 | 0.006 ± 0.006 | 0.292 ± 0.033 | 0.169 ± 0.030 | 0.495 ± 0.058 | 0.000 ± 0.000 | 0.176 |

## ACC Old média (classes já vistas, incl. descobertas)

| family | covertype | helena | isolet | letter | pendigits | volkert | média |
|---|---|---|---|---|---|---|---|
| auto-auroc | 0.260 ± 0.037 | 0.047 ± 0.019 | 0.688 ± 0.017 | 0.757 ± 0.016 | 0.759 ± 0.044 | 0.458 ± 0.005 | 0.495 |

## Esquecimento: acc_s0 (sessão 1) − acc_s0 (última); menor é melhor

| family | covertype | helena | isolet | letter | pendigits | volkert | média |
|---|---|---|---|---|---|---|---|
| auto-auroc | 0.006 ± 0.089 | -0.003 ± 0.012 | 0.019 ± 0.056 | 0.024 ± 0.034 | 0.011 ± 0.050 | -0.011 ± 0.019 | 0.008 |

## Tempo médio por sessão (s)

| family | covertype | helena | isolet | letter | pendigits | volkert | média |
|---|---|---|---|---|---|---|---|
| auto-auroc | 0.551 ± 0.260 | 0.667 ± 0.824 | 1.369 ± 0.199 | 0.207 ± 0.117 | 0.102 ± 0.021 | 0.062 ± 0.005 | 0.493 |

## Clusters espúrios por semente (somados nas sessões), pela classe majoritária

| family | base | de classe da sessão 0 | de classe já descoberta | de classe nova | tamanho médio |
|---|---|---|---|---|---|
| auto-auroc | covertype | 0.0 | 0.2 | 33.0 | 100.0 |
| auto-auroc | helena | 0.6 | 0.2 | 0.6 | 9.0 |
| auto-auroc | isolet | 0.0 | 0.0 | 2.0 | 54.0 |
| auto-auroc | letter | 0.0 | 0.0 | 2.0 | 82.0 |
| auto-auroc | pendigits | 0.0 | 0.0 | 4.8 | 190.0 |
| auto-auroc | volkert | 0.0 | 0.0 | 0.0 | nan |

## Classes no modelo ao fim / classes verdadeiras (por semente)

| family | covertype | helena | isolet | letter | pendigits | volkert |
|---|---|---|---|---|---|---|
| auto-auroc | 40/7, 39/7, 45/7, 33/7, 43/7 | 52/100, 52/100, 52/100, 52/100, 50/100 | 26/26, 25/26, 23/26, 25/26, 29/26 | 23/26, 25/26, 25/26, 21/26, 29/26 | 13/10, 15/10, 15/10, 15/10, 15/10 | 5/10, 5/10, 5/10, 5/10, 5/10 |

## Friedman nas bases (média das sementes por base) — ACC All média nas sessões

(precisa de ao menos 3 bases e 3 métodos)
