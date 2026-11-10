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

Pendente: `results_final/` — mesma configuração do `results_v3`, com o HAR
de volta à versão do PBN (atributo "sujeito" incluído;
`data/har/preproc.json.unused`). Só o HAR precisa rodar de novo:

```bash
mkdir -p results_final/a0.1 && cp results_v3/a0.1/*.csv results_final/a0.1/
K_EST=hdbscan-leaf ALPHAS="0.1" OUT=results_final \
  FAMILIES="kmeans sskmeans rf_msp lr_msp gauss knn mst dic auto" \
  bash run_pbn_gcd.sh har
```

## Cuidados ao comparar pastas

- Em `results/`, o `kmeans` com K estimado usava o K verdadeiro (erro
  corrigido a partir de `results_v2/`).
- Com `sil-size`, `hdbscan` e `hdbscan-leaf`, a coluna
  `old_false_reject` mede a falsa rejeição final, depois da reatribuição
  do ruído; a da etapa de rejeição é a das rodadas com K conhecido
  (~α).
- `data/<base>/preproc.json` muda os atributos para todos os métodos; em
  `results_v3/` vale para CNAE-9 (`l2`) e HAR (`drop_cols`).
