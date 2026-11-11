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

## Cuidados ao comparar pastas

- Em `results/`, o `kmeans` com K estimado usava o K verdadeiro (erro
  corrigido a partir de `results_v2/`).
- Com `sil-size`, `hdbscan` e `hdbscan-leaf`, a coluna
  `old_false_reject` mede a falsa rejeição final, depois da reatribuição
  do ruído; a da etapa de rejeição é a das rodadas com K conhecido
  (~α).
- `data/<base>/preproc.json` muda os atributos para todos os métodos; em
  `results_v3/` vale para CNAE-9 (`l2`) e HAR (`drop_cols`).
