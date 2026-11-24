## ACC All média nas sessões

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.140 ± 0.010 | 0.292 ± 0.045 | 0.100 ± 0.043 | 0.336 ± 0.019 | 0.053 ± 0.024 | 0.450 ± 0.019 | 0.296 ± 0.021 | 0.435 ± 0.115 | 0.432 ± 0.095 | 0.571 ± 0.059 | 0.434 ± 0.053 | 0.365 ± 0.062 | 0.275 ± 0.005 | 0.348 ± 0.014 | 0.360 ± 0.032 | 0.326 |

## ACC All na última sessão

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.114 ± 0.031 | 0.222 ± 0.061 | 0.072 ± 0.027 | 0.223 ± 0.011 | 0.039 ± 0.022 | 0.423 ± 0.045 | 0.241 ± 0.065 | 0.305 ± 0.144 | 0.377 ± 0.115 | 0.634 ± 0.084 | 0.412 ± 0.100 | 0.251 ± 0.037 | 0.212 ± 0.003 | 0.293 ± 0.019 | 0.248 ± 0.025 | 0.271 |

## ACC New média (classes que estreiam na sessão)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.077 ± 0.027 | 0.083 ± 0.145 | 0.075 ± 0.042 | 0.000 ± 0.000 | 0.023 ± 0.015 | 0.247 ± 0.034 | 0.000 ± 0.000 | 0.130 ± 0.070 | 0.107 ± 0.112 | 0.474 ± 0.066 | 0.162 ± 0.107 | 0.145 ± 0.325 | 0.000 ± 0.000 | 0.290 ± 0.063 | 0.132 ± 0.066 | 0.130 |

## ACC Old média (classes já vistas, incl. descobertas)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.177 ± 0.011 | 0.580 ± 0.049 | 0.409 ± 0.084 | 0.665 ± 0.029 | 0.090 ± 0.043 | 0.672 ± 0.028 | 0.445 ± 0.035 | 0.577 ± 0.132 | 0.750 ± 0.076 | 0.747 ± 0.068 | 0.724 ± 0.033 | 0.557 ± 0.161 | 0.631 ± 0.011 | 0.490 ± 0.015 | 0.631 ± 0.038 | 0.543 |

## Esquecimento: acc_s0 (sessão 1) − acc_s0 (última); menor é melhor

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.036 ± 0.021 | 0.262 ± 0.390 | 0.150 ± 0.077 | 0.011 ± 0.013 | 0.021 ± 0.046 | 0.091 ± 0.048 | -0.005 ± 0.021 | 0.373 ± 0.221 | 0.016 ± 0.006 | 0.249 ± 0.225 | 0.101 ± 0.075 | 0.136 ± 0.296 | 0.002 ± 0.007 | 0.177 ± 0.027 | 0.133 ± 0.094 | 0.117 |

## Tempo médio por sessão (s)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 1.718 ± 0.532 | 1.259 ± 0.767 | 0.700 ± 0.548 | 1.893 ± 0.054 | 3.479 ± 3.682 | 2.397 ± 0.450 | 0.283 ± 0.064 | 0.757 ± 0.232 | 0.165 ± 0.043 | 0.550 ± 0.095 | 0.167 ± 0.113 | 0.092 ± 0.158 | 0.116 ± 0.069 | 2.011 ± 0.230 | 0.013 ± 0.004 | 1.040 |

## Clusters espúrios por semente (somados nas sessões), pela classe majoritária

| family | base | de classe da sessão 0 | de classe já descoberta | de classe nova | tamanho médio |
|---|---|---|---|---|---|
| auto-auroc | census | 0.0 | 0.4 | 0.6 | 195.0 |
| auto-auroc | cnae9 | 0.0 | 0.2 | 0.0 | 41.0 |
| auto-auroc | covertype | 0.0 | 11.0 | 15.2 | 158.0 |
| auto-auroc | har | 0.0 | 0.0 | 0.0 | nan |
| auto-auroc | helena | 0.0 | 0.0 | 0.0 | nan |
| auto-auroc | isolet | 0.0 | 0.0 | 0.0 | nan |
| auto-auroc | krvsk | 0.0 | 0.0 | 0.0 | nan |
| auto-auroc | letter | 0.2 | 0.0 | 0.0 | 155.0 |
| auto-auroc | mfeat | 0.2 | 0.8 | 0.0 | 24.0 |
| auto-auroc | optdigits | 0.0 | 0.4 | 0.0 | 161.0 |
| auto-auroc | pendigits | 0.4 | 0.6 | 0.6 | 121.0 |
| auto-auroc | satimage | 0.0 | 0.2 | 0.4 | 716.0 |
| auto-auroc | segment | 0.0 | 0.2 | 0.0 | 1.0 |
| auto-auroc | volkert | 0.0 | 0.8 | 0.2 | 1166.0 |
| auto-auroc | vowel | 0.0 | 0.0 | 8.2 | 17.0 |

## Classes no modelo ao fim / classes verdadeiras (por semente)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 16/18, 18/18, 18/18, 18/18, 16/18 | 8/9, 10/9, 4/9, 4/9, 4/9 | 52/7, 46/7, 10/7, 46/7, 9/7 | 3/6, 3/6, 3/6, 3/6, 3/6 | 57/100, 56/100, 56/100, 57/100, 54/100 | 20/26, 19/26, 19/26, 20/26, 19/26 | 9/18, 9/18, 9/18, 9/18, 9/18 | 25/26, 21/26, 25/26, 25/26, 23/26 | 9/10, 7/10, 7/10, 14/10, 5/10 | 9/10, 11/10, 9/10, 10/10, 11/10 | 5/10, 7/10, 9/10, 12/10, 9/10 | 3/6, 3/6, 9/6, 3/6, 3/6 | 3/7, 3/7, 3/7, 3/7, 3/7 | 11/10, 11/10, 11/10, 11/10, 11/10 | 24/11, 11/11, 7/11, 23/11, 24/11 |

## Friedman nas bases (média das sementes por base) — ACC All média nas sessões

(precisa de ao menos 3 bases e 3 métodos)
