## ACC All média nas sessões

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.151 ± 0.007 | 0.482 ± 0.050 | 0.154 ± 0.045 | 0.603 ± 0.042 | 0.026 ± 0.009 | 0.544 ± 0.018 | 0.318 ± 0.016 | 0.666 ± 0.028 | 0.854 ± 0.014 | 0.814 ± 0.024 | 0.850 ± 0.047 | 0.654 ± 0.014 | 0.551 ± 0.059 | 0.293 ± 0.009 | 0.427 ± 0.064 | 0.492 |

## ACC All na última sessão

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.111 ± 0.006 | 0.457 ± 0.058 | 0.092 ± 0.027 | 0.563 ± 0.172 | 0.018 ± 0.006 | 0.479 ± 0.033 | 0.255 ± 0.053 | 0.613 ± 0.086 | 0.773 ± 0.061 | 0.766 ± 0.042 | 0.786 ± 0.112 | 0.617 ± 0.024 | 0.501 ± 0.096 | 0.278 ± 0.030 | 0.343 ± 0.043 | 0.443 |

## ACC New média (classes que estreiam na sessão)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.000 ± 0.000 | 0.304 ± 0.043 | 0.103 ± 0.018 | 0.452 ± 0.101 | 0.005 ± 0.003 | 0.321 ± 0.030 | 0.000 ± 0.000 | 0.333 ± 0.099 | 0.850 ± 0.032 | 0.800 ± 0.020 | 0.849 ± 0.112 | 0.609 ± 0.103 | 0.349 ± 0.040 | 0.023 ± 0.014 | 0.186 ± 0.084 | 0.346 |

## ACC Old média (classes já vistas, incl. descobertas)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.238 ± 0.011 | 0.705 ± 0.043 | 0.422 ± 0.071 | 0.752 ± 0.008 | 0.052 ± 0.022 | 0.776 ± 0.011 | 0.476 ± 0.017 | 0.807 ± 0.010 | 0.871 ± 0.009 | 0.848 ± 0.021 | 0.873 ± 0.014 | 0.719 ± 0.060 | 0.778 ± 0.046 | 0.500 ± 0.019 | 0.711 ± 0.037 | 0.635 |

## Esquecimento: acc_s0 (sessão 1) − acc_s0 (última); menor é melhor

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.005 ± 0.015 | -0.005 ± 0.037 | 0.018 ± 0.030 | 0.029 ± 0.038 | 0.007 ± 0.010 | -0.002 ± 0.018 | -0.002 ± 0.012 | -0.005 ± 0.017 | 0.043 ± 0.042 | 0.009 ± 0.034 | 0.056 ± 0.020 | 0.020 ± 0.028 | 0.015 ± 0.032 | -0.006 ± 0.014 | -0.019 ± 0.026 | 0.011 |

## Tempo médio por sessão (s)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.612 ± 0.307 | 1.967 ± 0.381 | 0.647 ± 0.186 | 5.622 ± 0.340 | 1.584 ± 1.871 | 1.442 ± 0.091 | 0.071 ± 0.042 | 0.566 ± 0.317 | 0.253 ± 0.122 | 0.677 ± 0.061 | 0.228 ± 0.094 | 0.215 ± 0.031 | 0.350 ± 0.180 | 0.243 ± 0.024 | 0.009 ± 0.005 | 0.966 |

## Clusters espúrios por semente (somados nas sessões), pela classe majoritária

| family | base | de classe da sessão 0 | de classe já descoberta | de classe nova | tamanho médio |
|---|---|---|---|---|---|
| auto-auroc | census | 0.0 | 0.0 | 0.0 | nan |
| auto-auroc | cnae9 | 0.0 | 0.0 | 1.2 | 20.0 |
| auto-auroc | covertype | 0.0 | 3.8 | 35.4 | 110.0 |
| auto-auroc | har | 0.0 | 0.6 | 1.6 | 235.0 |
| auto-auroc | helena | 0.4 | 0.0 | 0.0 | 1.0 |
| auto-auroc | isolet | 0.0 | 0.0 | 0.0 | nan |
| auto-auroc | krvsk | 0.0 | 0.0 | 0.0 | nan |
| auto-auroc | letter | 0.0 | 0.0 | 0.4 | 68.0 |
| auto-auroc | mfeat | 0.0 | 0.8 | 0.6 | 56.0 |
| auto-auroc | optdigits | 0.0 | 1.0 | 0.8 | 94.0 |
| auto-auroc | pendigits | 0.0 | 1.2 | 0.2 | 177.0 |
| auto-auroc | satimage | 0.0 | 0.4 | 2.2 | 272.0 |
| auto-auroc | segment | 0.0 | 0.2 | 1.4 | 68.0 |
| auto-auroc | volkert | 0.0 | 0.0 | 0.0 | nan |
| auto-auroc | vowel | 0.0 | 0.0 | 1.2 | 19.0 |

## Classes no modelo ao fim / classes verdadeiras (por semente)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 12/18, 12/18, 12/18, 12/18, 12/18 | 11/9, 10/9, 9/9, 10/9, 6/9 | 46/7, 43/7, 51/7, 39/7, 50/7 | 9/6, 7/6, 9/6, 7/6, 9/6 | 52/100, 52/100, 52/100, 52/100, 50/100 | 20/26, 19/26, 22/26, 20/26, 19/26 | 9/18, 9/18, 9/18, 9/18, 9/18 | 23/26, 26/26, 25/26, 24/26, 25/26 | 11/10, 11/10, 13/10, 11/10, 11/10 | 12/10, 11/10, 12/10, 12/10, 12/10 | 11/10, 12/10, 11/10, 12/10, 11/10 | 9/6, 9/6, 9/6, 7/6, 9/6 | 8/7, 9/7, 7/7, 9/7, 9/7 | 7/10, 7/10, 7/10, 5/10, 7/10 | 12/11, 13/11, 12/11, 12/11, 9/11 |

## Friedman nas bases (média das sementes por base) — ACC All média nas sessões

(precisa de ao menos 3 bases e 3 métodos)
