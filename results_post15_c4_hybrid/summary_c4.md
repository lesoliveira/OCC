## ACC All média nas sessões

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.116 ± 0.010 | 0.472 ± 0.045 | 0.157 ± 0.046 | 0.592 ± 0.044 | 0.044 ± 0.018 | 0.543 ± 0.017 | 0.290 ± 0.022 | 0.653 ± 0.034 | 0.853 ± 0.014 | 0.816 ± 0.023 | 0.850 ± 0.048 | 0.637 ± 0.018 | 0.551 ± 0.058 | 0.312 ± 0.006 | 0.421 ± 0.063 | 0.487 |

## ACC All na última sessão

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.083 ± 0.006 | 0.439 ± 0.083 | 0.094 ± 0.028 | 0.557 ± 0.166 | 0.030 ± 0.011 | 0.478 ± 0.032 | 0.236 ± 0.065 | 0.604 ± 0.090 | 0.772 ± 0.062 | 0.769 ± 0.044 | 0.785 ± 0.112 | 0.608 ± 0.024 | 0.501 ± 0.096 | 0.293 ± 0.031 | 0.338 ± 0.040 | 0.439 |

## ACC New média (classes que estreiam na sessão)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.000 ± 0.000 | 0.304 ± 0.043 | 0.103 ± 0.018 | 0.452 ± 0.101 | 0.005 ± 0.003 | 0.321 ± 0.030 | 0.000 ± 0.000 | 0.333 ± 0.099 | 0.850 ± 0.032 | 0.800 ± 0.020 | 0.849 ± 0.112 | 0.609 ± 0.103 | 0.349 ± 0.040 | 0.023 ± 0.014 | 0.186 ± 0.084 | 0.346 |

## ACC Old média (classes já vistas, incl. descobertas)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.182 ± 0.016 | 0.687 ± 0.039 | 0.444 ± 0.068 | 0.731 ± 0.033 | 0.092 ± 0.045 | 0.774 ± 0.007 | 0.435 ± 0.037 | 0.787 ± 0.018 | 0.869 ± 0.012 | 0.851 ± 0.019 | 0.873 ± 0.014 | 0.688 ± 0.065 | 0.779 ± 0.046 | 0.537 ± 0.015 | 0.698 ± 0.036 | 0.628 |

## Esquecimento: acc_s0 (sessão 1) − acc_s0 (última); menor é melhor

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 0.008 ± 0.007 | -0.011 ± 0.031 | 0.016 ± 0.029 | 0.048 ± 0.046 | 0.004 ± 0.008 | 0.002 ± 0.019 | -0.001 ± 0.016 | -0.010 ± 0.016 | 0.039 ± 0.046 | 0.010 ± 0.031 | 0.058 ± 0.018 | 0.010 ± 0.014 | 0.015 ± 0.032 | 0.004 ± 0.009 | -0.011 ± 0.033 | 0.012 |

## Tempo médio por sessão (s)

| family | census | cnae9 | covertype | har | helena | isolet | krvsk | letter | mfeat | optdigits | pendigits | satimage | segment | volkert | vowel | média |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| auto-auroc | 1.313 ± 0.638 | 3.072 ± 0.622 | 0.905 ± 0.198 | 9.111 ± 0.683 | 3.202 ± 3.835 | 2.424 ± 0.110 | 0.252 ± 0.088 | 0.775 ± 0.386 | 0.384 ± 0.189 | 1.014 ± 0.095 | 0.277 ± 0.101 | 0.282 ± 0.036 | 0.500 ± 0.258 | 0.548 ± 0.023 | 0.012 ± 0.007 | 1.605 |

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
