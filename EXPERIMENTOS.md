# Registro dos experimentos

Todos no cenário C2 (GCD transdutivo), nas 6 bases tabulares do PBN
(Troisemaine et al., DMKD 2024) com a divisão de classes conhecidas/novas
do PBN, 5 sementes, calibração `nested`. Cada pasta tem um CSV por base
(`<base>_c2_kest.csv` com K estimado, `<base>_c2_kknown.csv` com K
conhecido), o `summary.md` gerado pelo `summarize.py` e as versões das
bibliotecas (`versions.txt`). As bases não estão no repositório; para
recriá-las: `python prepare_pbn_datasets.py`.

| Pasta | α | Estimativa de K | Bases | O que testou | Conclusão |
|---|---|---|---|---|---|
| `results/` | 0,05 | silhueta nos rejeitados | 6 | primeira rodada | dic, mst, rf_msp e sskmeans empatados em ACC All; OCCs melhores em ACC Old e AUROC, piores em ACC New |
| `results_v2/a*/` | 0,05; 0,1; 0,2 | Vaze et al. (`labeled`) | letter, pendigits | sensibilidade a α | α = 0,1 é o melhor compromisso; o critério de Vaze subestima K (4,4 em vez de 7; 2,2 em vez de 5) |
| `results_ksil/` | 0,1 | silhueta nos rejeitados | letter, pendigits | estimador alternativo | acerta K no pendigits; superestima no letter (~30 em vez de 7) por causa dos fragmentos de classes antigas |
| `results_ksize/` | 0,1 | `sil-size` | letter, pendigits | correção dos fragmentos por tamanho | melhora pouco (K ~12 no letter) |
| `results_khdb/` | 0,1 | `hdbscan` | letter, pendigits | correção dos fragmentos por densidade | mst 0,777 de média, igual ao K conhecido (0,774) |
| `results_kleaf/` | 0,1 | `hdbscan-leaf` | letter | clusters mais finos | ganho pequeno e consistente no letter (0,656 → 0,660) |
| `results_main/` | 0,1 | `hdbscan-leaf` | 6 | resultado principal, famílias fixas | melhores OCCs superam rf_msp (+5) e sskmeans (+9) com p ≈ 0,002; CNAE-9 é a exceção |
| `results_v3/` | 0,1 | `hdbscan-leaf` | 6 | L2 no CNAE-9, HAR sem o atributo "sujeito", família `auto` | `auto` 0,736, acima de mst (+3,1; p = 0,014), rf_msp (+12) e sskmeans (+16); L2 resolve o CNAE-9; tirar o sujeito do HAR não muda nada |

## Resultado final: `results_final/`

Mesma configuração do `results_v3/` (α = 0,1, `hdbscan-leaf`, L2 no
CNAE-9, família `auto`), com o HAR de volta à versão do PBN (atributo
"sujeito" incluído; `data/har/preproc.json.unused`). As outras 5 bases são
cópias do `results_v3/`; só o HAR foi rodado de novo.

ACC All média nas 6 bases, K estimado (Wilcoxon pareado, 30 pares):

| Método | ACC All | Δ vs auto | p |
|---|---|---|---|
| auto | 0,737 | — | — |
| mst | 0,706 | −0,031 | 0,014 |
| gauss | 0,699 | −0,038 | 0,002 |
| rf_msp | 0,615 | −0,122 | < 0,001 |
| sskmeans | 0,581 | −0,156 | < 0,001 |

Com K conhecido, o `auto` também fica em 0,737. AUROC médio: auto 0,945,
rf_msp 0,826. No HAR, o resultado com e sem o "sujeito" é praticamente o
mesmo (auto 0,705 contra 0,702).

## SVM com γ ajustado: `results_v4/`

Mesma configuração do `results_final/`, com `svm` (γ padrão do
scikit-learn), `svm-cv` (γ escolhido em D_L por deixa-uma-classe-de-fora,
na grade {0,1; 0,3; 1; 3; 10} × o padrão) e o `auto` com as cinco variantes
`svm@g` entre as candidatas.

| Método | ACC All (K estimado) |
|---|---|
| auto (9 candidatas) | 0,730 |
| svm-cv | 0,711 |
| mst | 0,706 |
| gauss | 0,699 |
| svm (γ padrão) | 0,631 |
| rf_msp | 0,615 |
| sskmeans | 0,581 |

O ajuste de γ vale 8 pontos ao SVM, que empata com mst e gauss. Com mais
candidatas, o `auto` cai de 0,737 para 0,730 (no letter, escolhe `svm@10`
em vez do mst) e deixa de ser significativamente melhor que svm-cv
(p = 0,11) e mst (p = 0,07); continua acima de rf_msp e sskmeans
(p < 0,001).

## Critério do `auto`: `results_v5/`

Compara o critério novo do `auto` (`acc`: GCD simulado em D_L, escondendo
2 classes) com o original (`auto-auroc`: AUROC da rejeição, uma classe por
vez). Nesta rodada o `svm-cv` também usou `acc`.

ACC All média, K estimado, e perda em relação ao "oráculo" (a melhor
família fixa de cada base entre gauss, knn, mst, dic e svm-cv, que só se
conhece com os rótulos de D_U; média 0,754):

| Método | ACC All | Perda média | Pior perda (base) |
|---|---|---|---|
| auto-auroc | 0,730 | 0,024 | 0,039 (optdigits) |
| svm-cv | 0,725 | 0,030 | 0,130 (HAR) |
| mst | 0,706 | 0,049 | 0,128 (HAR) |
| auto (`acc`) | 0,699 | 0,055 | 0,140 (HAR) |
| gauss | 0,699 | 0,056 | 0,157 (optdigits) |
| rf_msp | 0,615 | 0,139 | 0,246 (mfeat) |
| sskmeans | 0,581 | 0,173 | 0,347 (letter) |

O critério `acc` escolhe o dic no CNAE-9 e no HAR (4 de 5 sementes), onde
o dic é ruim: com 3 ou 4 classes conhecidas, o problema simulado sobra com
1 ou 2 classes para treinar e fica ruidoso. O critério padrão volta a ser
`auroc`. O `auto-auroc` não é significativamente melhor que o svm-cv na
média (p = 0,95), mas é o mais robusto: a pior perda em relação ao
oráculo cai de 0,13 (svm-cv, mst) para 0,04.

## Cenário incremental (C4): `results_c4/`

`run_pbn_c4.sh pendigits letter`: 3 sessões, 5 sementes, α = 0,1,
`hdbscan-leaf` (ver `run_c4.py`). ACC All média nas sessões: mst 0,783,
svm-cv 0,779, auto-auroc 0,772, gauss 0,704, rf_msp re-treinado 0,678,
sskmeans 0,419 (auto-auroc contra rf_msp: +0,094, p = 0,002). O OCC
descobre melhor (ACC New ~0,61 contra 0,43) e atualiza ~5–10× mais rápido,
mas cria classes demais (letter: 28–32 para 26; pendigits: 13–15 para 10)
e perde 3–5 pontos nas classes da sessão 0 ao longo das sessões, contra
~1 ponto do rf_msp, que guarda e re-treina com todos os dados.

## C4: modo do HDBSCAN, `results_c4_leaf/` × `results_c4_eom/`

Diagnóstico dos clusters espúrios (que não casam com nenhuma classe):
quase todos vêm de classes novas partidas em dois, não de fragmentos de
classes antigas. Com o modo padrão do HDBSCAN (`hdbscan`, "eom") em vez do
`leaf`, no letter os espúrios por semente caem de 3,6 para 1,0 (mst) e de
6,2 para 2,2 (svm-cv); a ACC All média sobe de 0,685 para 0,708 (mst) e de
0,684 para 0,717 (svm-cv), e a ACC New de ~0,36 para ~0,44. No pendigits os
dois modos dão a mesma partição. O esquecimento não muda (OCC 3,6–4,9
pontos, rf_msp 0,5).

## C2 com o HDBSCAN no modo padrão: `results_v6/`

Mesma configuração do `results_v4/`, trocando `hdbscan-leaf` por `hdbscan`
("eom"). Quase tudo igual, exceto o mfeat, onde o modo padrão funde as
classes novas (K_new estimado 2,0–2,4 em vez de 5; com `leaf`, 5,0): o
`auto-auroc` cai de 0,859 para 0,598 no mfeat e de 0,730 para 0,686 na
média. Os dois modos erram em direções opostas: o `leaf` parte classes
novas no letter do C4; o "eom" funde classes novas no mfeat do C2. O
padrão continua `hdbscan-leaf` nos dois cenários.

## C4 nas 6 bases: `results_c4/`

`bash run_pbn_c4.sh` (3 sessões, 5 sementes, α = 0,1, `hdbscan-leaf`). A
rodada antiga com só letter e pendigits foi sobrescrita; ela é igual a
`results_c4_leaf/`.

ACC All média nas sessões: auto-auroc 0,694; svm-cv 0,672; gauss 0,666;
mst 0,656; rf_msp re-treinado 0,635; sskmeans 0,487. O auto-auroc supera
todos com significância (Wilcoxon, 30 pares: svm-cv p = 0,014; gauss
p = 0,001; mst p = 0,014; rf_msp p = 0,013). O OCC ganha em 5 das 6 bases
(HAR: 0,581 contra 0,356 do rf_msp, que nunca descobre classe nenhuma); o
rf_msp ganha no CNAE-9 (0,569 contra 0,457). Na última sessão a vantagem
encolhe para 2 pontos (0,627 contra 0,608). Ponto fraco: interferência das
classes descobertas nas conhecidas quando há poucas conhecidas e as novas
são parecidas com elas: no HAR a acurácia nas classes da sessão 0 cai de
0,87 para 0,60 na sessão 2 (rf_msp: 0,97 estável); no CNAE-9, de 0,93 para
0,82. Tempo: mst e svm-cv são 5–10× mais rápidos que o rf_msp, mas o gauss
em alta dimensão (CNAE-9, HAR) é mais lento (1,6–4,8 s por sessão).

## C4 com prioridade às classes mais antigas: `results_c4_prio/`

Mesma rodada do `results_c4/` com `--priority`: entre as classes que
aceitam uma amostra, vence a mais antiga. A ACC All média não muda
(auto-auroc 0,694 nos dois; Δ = 0,000, p = 0,19), mas o esquecimento das
classes da sessão 0 cai de 8,9 para 2,0 pontos (p = 0,0001), no nível do
rf_msp re-treinado (1,8), sem guardar dados. No HAR, de 27,4 para −1,1;
no CNAE-9, de 11,9 para 2,0. Mesmo efeito em mst (16,0 → 2,1), svm-cv
(12,3 → 2,7) e gauss (9,2 → 1,9). A prioridade passa a ser o padrão do
`run_c4.py` (`--no-priority` desliga).

## C2 em 15 bases: `results_v7/`

As 6 do PBN (cópias do `results_v4/`), mais o Census (a 7ª do PBN) e 8 do
OpenML (`prepare_openml_datasets.py`, critérios fixados de antemão; o
shuttle foi reprovado: sobram 5 classes depois de descartar as com menos de
20 amostras). α = 0,1, `hdbscan-leaf`, `auto` com o critério AUROC.

ACC All média (K estimado): auto 0,546; svm-cv 0,529; mst 0,524; gauss
0,524; dic 0,516; knn 0,514; rf_msp 0,506; svm 0,491; lr_msp 0,464;
sskmeans 0,447; kmeans 0,371. Friedman nas bases: χ² = 31,6, p = 0,0005.
Holm só nos 4 baselines: auto supera kmeans (p = 0,0005), sskmeans
(0,008) e lr_msp (0,043), mas não o rf_msp (p = 0,21; o auto ganha em 9 de
15 bases). Entre as variantes de OCC, só o svm de γ padrão fica abaixo com
significância.

As 6 derrotas para o rf_msp se dividem em dois grupos:
- census, helena, krvsk, volkert: nenhum método detecta as classes novas
  nos atributos brutos (o maior AUROC entre os métodos fica entre 0,56 e
  0,73; o OCC não rejeita quase nada e K_new estimado ≈ 0). A ACC vira a
  acurácia de classificação das conhecidas, em que a floresta é melhor.
  Census: classes ordinais (anos de escolaridade).
- covertype (desbalanceado; K superestimado, 7,4 para 4) e vowel (990
  amostras, ~45 rotuladas por classe): o OCC detecta bem (AUROC 0,87 e
  0,95, contra 0,65 e 0,67 do rf_msp), mas agrupa mal.
Nas 11 bases em que algum método detecta as novas (maior AUROC ≥ 0,9), o
auto ganha do rf_msp em 9. AUROC do auto maior que o do rf_msp em 12 de 15
bases (Wilcoxon nas bases, p = 0,064).

## C4 em 15 bases: `results_c4_v2/`

As 6 do PBN são cópias do `results_c4_prio/`; as 9 novas rodaram com a
configuração final (prioridade, `hdbscan-leaf`). ACC All média nas sessões:
auto-auroc 0,474; rf_msp re-treinado 0,471; svm-cv 0,463; mst 0,453; gauss
0,445; sskmeans 0,363. Friedman nas bases: p = 0,17. O auto supera o
sskmeans (Holm, p = 0,036) e empata com o rf_msp (Δ = 0,004, p = 0,80).
Descoberta melhor no OCC (ACC New 0,303 contra 0,244) e reconhecimento
melhor no rf_msp (ACC Old 0,682 contra 0,637). Esquecimento igual (1,2 e
1,4 pontos). Nas 11 bases em que a novidade é detectável no C2, o auto
ganha do rf_msp em 7, perde em 3 (isolet, cnae9, segment) e empata em 1;
nas 4 sem sinal (census, helena, krvsk, volkert), perde em todas. Tempo
médio por sessão: auto 0,8 s, rf_msp 1,7 s (o gauss no isolet, com 617
atributos, leva 16 s).

## Cuidados ao comparar pastas

- Em `results/`, o `kmeans` com K estimado usava o K verdadeiro (erro
  corrigido a partir de `results_v2/`).
- Com `sil-size`, `hdbscan` e `hdbscan-leaf`, a coluna
  `old_false_reject` mede a falsa rejeição final, depois da reatribuição
  do ruído; a da etapa de rejeição é a das rodadas com K conhecido
  (~α).
- `data/<base>/preproc.json` muda os atributos para todos os métodos; em
  `results_v3/` vale para CNAE-9 (`l2`) e HAR (`drop_cols`).

## results_diag — teto supervisionado (diag_teto.py)

Com todas as classes rotuladas, acurácia por validação cruzada (3 partes) de um
RF e de um kNN no espaço padronizado, nas 15 bases. As 4 bases sem sinal são as
4 de menor teto: census 0,335, helena 0,333, volkert 0,633, krvsk 0,657 (RF);
todas as outras ficam acima de 0,82. Conclusão: em census e helena o limite é
dos dados, não da métrica. Maior diferença RF − kNN: vowel (0,97 contra 0,77)
e krvsk (0,66 contra 0,50), onde uma representação melhor pode ajudar.

Código novo: `occ/represent.py` e `--repr {raw,qpca,rfleaf}` no run_gcd.py
(padrão raw, resultados antigos inalterados). Piloto em results_repr/.

## results_repr — piloto de representações (C2, 3 sementes, α = 0,1)

Bases: vowel, krvsk, census, helena, volkert. Famílias: gauss, knn, mst, rf_msp
(sem auto). Comparado com results_v7 nas mesmas 3 sementes.

- `qpca` (quantílica + PCA branqueada): piora quase tudo; em vowel derruba o
  AUROC do gauss de 0,85 para 0,50. Descartada.
- `rfleaf` (folhas de um RF treinado em D_L): melhora o AUROC dos OCCs em
  krvsk (mst 0,68 -> 0,76), helena (gauss 0,57 -> 0,62) e census (knn 0,51 ->
  0,59); em volkert o melhor continua sendo o rf_msp (0,73). A ACC All sobe
  pouco (krvsk mst 0,345 -> 0,382; helena gauss 0,125 -> 0,176) e os OCCs
  continuam abaixo do rf_msp nas 4 bases de novidade não detectável. Em vowel
  iguala o que o auto já obtinha com svm no espaço original.

Conclusão: representações baratas não destravam essas bases, o que concorda
com o diagnóstico do teto supervisionado (limite dos dados).

### Vowel sem as colunas de contexto (`results_repr/vowel_sem_contexto.csv`)

Teste de confirmação, NÃO é o resultado oficial (o pré-processamento das bases
do OpenML foi fixado de antemão). O vowel tem 19 colunas one-hot de contexto:
treino/teste (2), locutor (15) e sexo (2). Sem elas, C2, 5 sementes, α = 0,1:
auto 0,366 -> 0,481 (AUROC 0,945 -> 0,964), rf_msp 0,456 -> 0,449,
sskmeans 0,163 -> 0,312, kmeans 0,081 -> 0,178. O auto passa o rf_msp.
Confirma que os grupos naturais do espaço original eram de contexto (locutor),
não de vogal. A ACC continua moderada: o K estimado fica em 4,8 de 6.

## results_pc — seleção por classe (`auto-pc`), C2, 15 bases, 5 sementes

Cada classe conhecida fica com a família cujo OCC melhor separa a própria
classe das classes escondidas (mesma simulação do auto). Comparado com o auto
de results_v7, mesmas sementes.

Resultado negativo: ACC All média 0,544 contra 0,546 do auto (Wilcoxon nas
bases p = 0,64; 5 bases melhoram mais de 0,005 e 6 pioram). O AUROC médio cai
de 0,843 para 0,822, com quedas grandes em covertype (0,865 -> 0,686) e har
(0,950 -> 0,824), as duas com só 3 classes conhecidas: cada classe é avaliada
contra no máximo 2 classes escondidas, e a escolha fica ruidosa. Melhores
casos: optdigits (+0,036) e pendigits (+0,021). Pior: isolet (-0,044).

Conclusão: a seleção por classe não melhora sobre o auto; a seleção por
amostra (dinâmica) fica como trabalho futuro. O auto continua o padrão.

## results_img_diag — CIFAR-10 com DINO, subamostra de 5 mil, 1 semente (diagnóstico)

Primeiro teste (768 dimensões, L2): auto/gauss 0,617 de ACC All, AUROC 0,842,
só 49% das novas rejeitadas; k-means 0,685 (K estimado) e 0,845 (K conhecido,
igual ao publicado por Vaze et al., 0,836). Causa: 250 amostras rotuladas por
classe em 768 dimensões. Com PCA sem rótulos em D_L ∪ D_U (`--repr pcaN`):

| dim | gauss ACC | gauss AUROC | knn ACC | AUROC simulado (gauss) |
|---|---|---|---|---|
| 768 | 0,617 | 0,842 | 0,601 | 0,934 |
| 8   | 0,730 | 0,908 | 0,747 | 0,942 |
| 16  | 0,789 | 0,941 | 0,785 | 0,962 |
| 32  | 0,773 | 0,957 | 0,755 | 0,971 |
| 64  | 0,754 | 0,945 | 0,750 | 0,976 |
| 128 | 0,729 | 0,927 | 0,710 | 0,974 |

PCA branqueada (pcaw64) piora (gauss 0,555). O AUROC simulado em D_L (classes
escondidas) põe as 768 dimensões em último e escolheria 64: dá para escolher a
dimensão sem olhar D_U. Com K conhecido e pca32: knn 0,815, k-means 0,847.
Uma semente e subamostra: confirmar na base completa.

## results_img_k e results_ksil15 — estimador de K: sil-size x hdbscan-leaf

CIFAR-10 completo (DINO, PCA 64, C2, 3 sementes; results_img_k/): o HDBSCAN
marca ~58% dos rejeitados como ruído (densidade rala em 64 dimensões), funde
classes novas vizinhas e devolve ~7 mil rejeitados às classes antigas (só ~1,1
mil eram antigas). auto: hdbscan-leaf 0,660 ± 0,002 (K = 3 de 5); sil-size
0,841 ± 0,001 (K = 5 nas 3 sementes), igual ao K conhecido. A rodada de 3
sementes feita no Mac (results_img/, hdbscan-leaf) reproduz os mesmos números.

Tabulares, auto, 5 sementes (results_ksil15/ contra results_v7/): hdbscan-leaf
0,547 e sil-size 0,521 de média; sil-size ganha em 4 bases (satimage +0,055,
optdigits +0,045, covertype +0,035, vowel +0,019) e perde em 8, com colapsos
em mfeat (−0,298, K = 2 de 5) e isolet (−0,142, K = 2 de 13), e superestima no
letter (K = 20 de 7). Wilcoxon nas bases p = 0,64.

Escolher o estimador pelo GCD simulado em D_L (2 classes escondidas;
results_ksil15/sim_cifar10.csv) acerta o CIFAR-10 mas erra 5 de 8 bases
tabulares, incluindo o mfeat. Conclusão: nenhum estimador serve aos dois tipos
de dados e não há como escolher só com D_L. hdbscan-leaf continua o padrão.

## results_c1 — cenário C1 (protocolo do PBN), 7 bases do PBN, K conhecido, 3 sementes

Avaliação transdutiva (novas de X_train). k-means no espaço original:
har 0,759, letter 0,521, pendigits 0,867, mfeat 0,896, optdigits 0,776,
cnae9 0,679, census 0,498 (média 0,714). Bate com a coluna k-means da tabela
3 do PBN (média 69,5, avaliada no teste), o que confirma bases e divisões.
Os OCCs (gauss, mst) ficam abaixo do k-means em todas as bases: no C1 todo o
D_U é de classes novas por hipótese, a rejeição só atrapalha (manda novas para
classes antigas) e o método não tem o que oferecer. O C1 entra no artigo só
como validação do protocolo; a comparação com o PBN é no C2 e no C4.

PBN reimplementado em occ/pbn.py (PyTorch, segue o código oficial) e
run_pbn_baseline.py: --scenario c1 reproduz o protocolo do artigo (ACC no
teste) para validar; --scenario c2 roda o PBN no GCD; --tune aplica a busca
de hiperparâmetros do artigo nas bases sem hiperparâmetros publicados.

### results_pbn — validação do PBN reimplementado (C1, protocolo do artigo, 10 rodadas)

ACC no teste (novas), nosso / publicado (tabelas 4 e 5 do PBN):

| base | K conhecido | K estimado |
|---|---|---|
| har | 0,784 / 0,767 | 0,711 / 0,711 |
| letter | 0,653 / 0,624 | 0,624 / 0,613 |
| pendigits | 0,824 / 0,828 | 0,832 / 0,830 |
| census | 0,633 / 0,624 | 0,482 / 0,498 |
| mfeat | 0,912 / 0,917 | 0,899 / 0,906 |
| optdigits | 0,933 / 0,926 | 0,877 / 0,905 |
| cnae9 | 0,704 / 0,726 | 0,425 / 0,508 |
| média | 0,778 / 0,773 | 0,693 / 0,710 |

Com K conhecido a reimplementação reproduz o artigo (diferenças dentro de um
desvio). Com K estimado fica 1,7 ponto abaixo na média, quase todo no cnae9
(K estimado 2,5 contra 5 no artigo). Rodado no Mac (CPU), cerca de 1 hora.

Nota (PBN no C2): o primeiro teste no vowel estimou K total = 3 com 5 classes
conhecidas (K_new = −2, ACC Old 0). O intervalo da silhueta passou de [2, 3·n_old]
para [n_old + 1, n_old + 30]. O k-means de referência do run_gcd.py ainda usa
[2, 3·n_old] e tem o mesmo defeito; rever antes da tabela final.
