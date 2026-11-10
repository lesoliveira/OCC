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

## Cuidados ao comparar pastas

- Em `results/`, o `kmeans` com K estimado usava o K verdadeiro (erro
  corrigido a partir de `results_v2/`).
- Com `sil-size`, `hdbscan` e `hdbscan-leaf`, a coluna
  `old_false_reject` mede a falsa rejeição final, depois da reatribuição
  do ruído; a da etapa de rejeição é a das rodadas com K conhecido
  (~α).
- `data/<base>/preproc.json` muda os atributos para todos os métodos; em
  `results_v3/` vale para CNAE-9 (`l2`) e HAR (`drop_cols`).
