## ACC All média nas sessões

| family | covertype | helena | volkert | média |
|---|---|---|---|---|
| auto-auroc | 0.130 ± 0.019 | 0.027 ± 0.009 | 0.309 ± 0.005 | 0.155 |

## ACC All na última sessão

| family | covertype | helena | volkert | média |
|---|---|---|---|---|
| auto-auroc | 0.122 ± 0.020 | 0.016 ± 0.008 | 0.387 ± 0.012 | 0.175 |

## ACC New média (classes que estreiam na sessão)

| family | covertype | helena | volkert | média |
|---|---|---|---|---|
| auto-auroc | 0.094 ± 0.021 | 0.006 ± 0.006 | 0.000 ± 0.000 | 0.033 |

## ACC Old média (classes já vistas, incl. descobertas)

| family | covertype | helena | volkert | média |
|---|---|---|---|---|
| auto-auroc | 0.260 ± 0.037 | 0.047 ± 0.019 | 0.458 ± 0.005 | 0.255 |

## Esquecimento: acc_s0 (sessão 1) − acc_s0 (última); menor é melhor

| family | covertype | helena | volkert | média |
|---|---|---|---|---|
| auto-auroc | 0.006 ± 0.089 | -0.003 ± 0.012 | -0.011 ± 0.019 | -0.002 |

## Tempo médio por sessão (s)

| family | covertype | helena | volkert | média |
|---|---|---|---|---|
| auto-auroc | 0.551 ± 0.260 | 0.667 ± 0.824 | 0.062 ± 0.005 | 0.427 |

## Clusters espúrios por semente (somados nas sessões), pela classe majoritária

| family | base | de classe da sessão 0 | de classe já descoberta | de classe nova | tamanho médio |
|---|---|---|---|---|---|
| auto-auroc | covertype | 0.0 | 0.2 | 33.0 | 100.0 |
| auto-auroc | helena | 0.6 | 0.2 | 0.6 | 9.0 |
| auto-auroc | volkert | 0.0 | 0.0 | 0.0 | nan |

## Classes no modelo ao fim / classes verdadeiras (por semente)

| family | covertype | helena | volkert |
|---|---|---|---|
| auto-auroc | 40/7, 39/7, 45/7, 33/7, 43/7 | 52/100, 52/100, 52/100, 52/100, 50/100 | 5/10, 5/10, 5/10, 5/10, 5/10 |

## Friedman nas bases (média das sementes por base) — ACC All média nas sessões

(precisa de ao menos 3 bases e 3 métodos)
