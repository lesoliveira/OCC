# OCC para GCD com representações fixas (CPU)

Implementação das famílias de OCC do protocolo experimental, com
calibração conforme, rejeição, descoberta de classes novas e incorporação.
Tudo roda em CPU com numpy, scipy, scikit-learn e pandas.

## Instalação

```bash
pip install -r requirements.txt
python run_gcd.py --demo          # teste rápido na base digits (~15 s)
```

## Estrutura

```
occ/
  base.py         interface comum: fit(X), score(X); maior = mais típico
  families.py     OCC-Gauss (GaussianDD), OCC-kNN, OCC-SVM, MSTDD
  modes.py        MODES (KBS 2021) como família por classe
  dichotomy.py    OCC-Dic: dichotomizer global no espaço |a - b|
  calibration.py  ClassWiseOCC: um OCC por classe + p-valores conformes
  gcd.py          OCCDiscovery: rejeição -> agrupamento dos rejeitados -> incorporação
  kest.py         estimativa de K_new: silhueta e critério de Vaze et al.
  fragments.py    correção dos fragmentos de antigas nos rejeitados
  select.py       escolha da família por deixa-uma-classe-de-fora em D_L
  baselines.py    SS-k-means (Vaze et al.) e classificador fechado + MSP
  metrics.py      ACC húngaro (All/Old/New), AUROC, FPR@95, falsa rejeição
splits.py         splits GCD (C2) e NCD (C1) no padrão de Vaze et al.
run_gcd.py        executor por linha de comando, salva CSV
```

## Famílias (`--families`)

| Nome  | Escore | Observação |
| ----- | ------ | ---------- |
| gauss | log-verossimilhança gaussiana, covariância Ledoit-Wolf | estável em alta dimensão |
| knn   | menos a distância média aos k vizinhos | k = 5 |
| svm   | One-class SVM RBF | nu = 0,05 |
| mst   | menos a distância à aresta mais próxima da MST | reimplementação do MSTDD do dd_tools |
| modes | média dos OCCs dos clusters mais próximos, várias segmentações | base em `--modes-base` (padrão knn) |
| dic   | P(mesma classe) do dichotomizer, média das k referências | incorporar classe = guardar referências |

## Baselines (`--families`)

| Nome     | O que é | Usa D_L | Rejeição explícita |
| -------- | ------- | ------- | ------------------ |
| kmeans   | k-means em D_U com K total | não | não |
| sskmeans | k-means semi-supervisionado do GCD (Vaze et al.) | sim | não |
| rf_msp   | Random Forest + probabilidade máxima + k-means dos rejeitados | sim | sim |
| lr_msp   | regressão logística + probabilidade máxima + k-means | sim | sim |

No MSP, o limiar é o quantil alpha da probabilidade máxima de validação
cruzada em D_L, com a mesma semântica de alpha dos OCCs.

## Usando com os seus atributos

```bash
# C2 (GCD transdutivo), 5 repetições, K estimado pela silhueta
python run_gcd.py --X feats.npy --y labels.npy --scenario c2 \
    --seeds 0 1 2 3 4 --out results/base_c2.csv

# C1 (NCD) com a divisão Old fixa do PBN
python run_gcd.py --X feats.npy --y labels.npy --scenario c1 \
    --old-classes 0 1 2 3 4 --seeds 0
```

Opções úteis: `--alpha` (padrão 0,05), `--k-known` (usa o K verdadeiro das
classes novas), `--old-frac 0.8` (CIFAR-100), `--scale {all,labeled,none}`,
`--cal-mode {cv,split,nested}`.

**Padronização (`--scale`, padrão `all`)**: usa média e desvio de
D_L ∪ D_U, só dos atributos, sem rótulos, o que é legítimo no cenário
transdutivo. A opção `labeled` (só D_L) cria valores extremos quando um
atributo quase não varia nas classes antigas: no digits, até 90 desvios,
o que derruba o k-means de 0,78 para 0,59 de ACC All.

## Bases tabulares do PBN (cenário C2)

```bash
python prepare_pbn_datasets.py            # baixa da UCI; --with-census inclui o Census (~360 MB)
bash run_pbn_gcd.sh                       # 5 sementes, K estimado e conhecido, α = 0,05 0,1 0,2
# só algumas bases, outro α, outra pasta, outras famílias:
ALPHAS="0.1" OUT=results_v2 bash run_pbn_gcd.sh pendigits letter
FAMILIES="mst dic mst+ssk rf_msp" bash run_pbn_gcd.sh pendigits
```

Cada α gera `$OUT/a<α>/summary.md`, com ACC All/Old/New, AUROC, falsa
rejeição de Old, rejeição de New (o que não é rejeitado foi absorvido por
uma classe antiga) e o K_new usado por cada método.

**Estimativa de K (`--k-est`, padrão `labeled`)**: critério de Vaze et al.
(CVPR 2022): k-means em D_L ∪ D_U para cada K candidato e escolha do K que
maximiza a ACC húngara nas amostras rotuladas. A mesma estimativa vale
para todos os métodos, o que isola o efeito da rejeição. `silhouette` é
o comportamento antigo (cada método estima nos seus rejeitados).

**Correção dos fragmentos (`--k-est sil-size` ou `hdbscan`)**: com
muitas classes antigas, os rejeitados por engano formam um pequeno
fragmento de cada antiga, e a silhueta conta cada fragmento como classe
nova (letter: ~30 em vez de 7). O tamanho esperado de um fragmento é
α/(1−α) × aceitos da classe, e o limiar é τ = `--frag-c` (padrão 2) × a
mediana desses tamanhos. `sil-size` devolve às antigas os clusters
menores que τ e reagrupa o resto; `hdbscan` usa o HDBSCAN com
min_cluster_size = τ e manda o ruído para o centróide mais próximo (cai
para `sil-size` se não achar nenhum cluster); `hdbscan-leaf` usa
`cluster_selection_method="leaf"`, que escolhe clusters mais finos e pode
separar classes novas vizinhas que o modo padrão funde (no letter, o
`hdbscan` estimou 3,8 classes em vez de 7). Detalhes em
`occ/fragments.py`.

**Pré-processamento por base (`data/<base>/preproc.json`)**: se existir,
o `run_gcd.py --data` aplica a todos os métodos. Chaves: `drop_cols`
(colunas removidas) e `l2` (normaliza cada linha; a distância euclidiana
vira função do cosseno; desliga a padronização). Usamos `{"l2": true}` no
CNAE-9 (contagens de palavras esparsas) e `{"drop_cols": [561]}` no HAR
(o PBN acrescenta o identificador do sujeito como atributo, o que faz as
distâncias agruparem por pessoa). `--no-preproc` ignora o arquivo.

**Família `auto`**: escolhe a família de OCC só com D_L. Cada classe
conhecida (até 5) é deixada de fora e tratada como nova; as demais são
divididas em treino (70%) e teste; vence a família com maior AUROC médio
antigas × "nova". Candidatas em `--auto-families` (padrão gauss knn mst
dic). O CSV guarda a família escolhida (`chosen`) e os AUROCs (`loco_*`).

**Variante `+ssk`** (ex.: `mst+ssk`): os rejeitados vão para o SS-k-means
com as antigas ancoradas em D_L, em vez de k-means isolado. Fica fora do
padrão: no digits, quase zera a falsa rejeição, mas devolve às classes
antigas também as amostras novas próximas delas (o 6 vai para o 4, o 9 para
o 3), e o casamento húngaro então troca as antigas: ACC Old cai de 0,82
para 0,39–0,54.

O `prepare_pbn_datasets.py` reproduz o pré-processamento e a divisão de
classes conhecidas/novas do repositório oficial do PBN e salva em
`data/<base>/`. O `run_pbn_gcd.sh` grava um CSV por base em `results/`,
as versões das bibliotecas em `results/versions.txt`, e chama o
`summarize.py`, que monta `results/summary.md` com média ± desvio por base,
rank médio e Wilcoxon pareado contra o melhor OCC.

Três cuidados ao comparar com o artigo do PBN:

- Nas rodadas antigas (pasta `results/` sem `a<α>`), o `kmeans` em "K
  estimado" usava o K verdadeiro; agora usa a estimativa.
- O PBN reporta o cenário NCD (C1): o conjunto não rotulado tem só classes
  novas, e a ACC é medida no teste. Aqui rodamos GCD (C2), em que D_U
  mistura antigas e novas. Os números não são comparáveis diretamente;
  para isso falta adaptar o PBN ao GCD (próximo passo).
- Com a divisão fixa do PBN, as 5 sementes variam as amostras de D_L e
  D_U, não quais classes são novas.
- CNAE-9: os rótulos vão de 1 a 9, mas a divisão do PBN inclui a classe 0,
  que não existe; por isso ficam 4 conhecidas e 5 novas, como no artigo.

## Decisões de implementação a conhecer

- **Calibração por validação cruzada dentro da classe** (`cal_mode="cv"`,
  5 folds). Com n pontos de calibração, o menor p-valor possível é
  1/(n+1); só há rejeição se 1/(n+1) < α. Reservar 20% de uma classe com
  45 amostras dá 9 pontos e torna a rejeição impossível com α = 0,05.
  Na validação cruzada, a classe inteira serve de calibração e o OCC final
  é treinado com todas as amostras. O código avisa quando a classe é
  pequena demais.
- **OCC-Dic**: com `--cal-mode cv`, o classificador de pares é treinado com
  todo D_L e a calibração fica otimista (falsa rejeição de Old 0,28 com
  α = 0,2). Use `--cal-mode nested`: uma floresta por fold, sem vazamento
  (falsa rejeição 0,16; ACC Old 0,72 para 0,84; custo de 5 florestas a mais).
  Para as outras famílias, `nested` é igual a `cv`.
- **MODES**: usa 4 dos 13 índices do NbClust (silhueta, Calinski-Harabasz,
  Davies-Bouldin, Dunn); cada OCC de cluster é padronizado pelos seus
  escores de treino antes da média; a poda por região de competência entre
  classes fica desligada, porque em mundo aberto ela força a escolha entre
  classes conhecidas.
- **Rótulos**: o executor converte qualquer rótulo para inteiros 0..C-1;
  -1 é reservado para rejeição.

## Teste na base digits (pixels brutos, 5 Old / 5 New, α = 0,2, K conhecido, 5 sementes)

| Método | ACC All | ACC Old | ACC New | AUROC | Falsa rej. Old |
| ------ | ------- | ------- | ------- | ----- | -------------- |
| rf_msp | 0,737 | 0,818 | 0,697 | 0,952 | 0,18 |
| mst | 0,722 | 0,784 | 0,692 | 0,917 | 0,18 |
| dic (nested) | 0,700 | 0,838 | 0,631 | 0,952 | 0,16 |
| gauss | 0,699 | 0,779 | 0,659 | 0,909 | 0,18 |
| lr_msp | 0,691 | 0,798 | 0,637 | 0,905 | 0,20 |
| knn | 0,673 | 0,789 | 0,614 | 0,894 | 0,17 |
| svm | 0,660 | 0,806 | 0,587 | 0,885 | 0,18 |
| kmeans | 0,654 | 0,511 | 0,726 | | |
| sskmeans | 0,653 | 0,646 | 0,656 | | |
| modes | 0,628 | 0,792 | 0,546 | 0,880 | 0,15 |

O classificador fechado com MSP é o baseline a bater: em pixels brutos,
ele supera todos os OCCs. O digits serve como teste de fumaça; o teste
real é com atributos DINO e as bases do PBN. A silhueta tende a
subestimar K_new nessa base (escolhe 2 em vez de 5).
