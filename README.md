# OCC for GCD with fixed representations (CPU)

Implementation of the OCC families of the experimental protocol, with
conformal calibration, rejection, discovery of novel classes and
incorporation. Everything runs on CPU with numpy, scipy, scikit-learn and
pandas.

## Installation

```bash
pip install -r requirements.txt
python run_gcd.py --demo          # quick test on the digits data set (~15 s)
```

## Structure

```
occ/
  base.py         common interface: fit(X), score(X); higher = more typical
  families.py     OCC-Gauss (GaussianDD), OCC-kNN, OCC-SVM, MSTDD
  modes.py        MODES (KBS 2021) as a per-class family
  dichotomy.py    OCC-Dic: global dichotomizer in the |a - b| space
  calibration.py  ClassWiseOCC: one OCC per class + conformal p-values
  gcd.py          OCCDiscovery: rejection -> clustering of the rejected -> incorporation
  kest.py         estimation of K_new: silhouette and the criterion of Vaze et al.
  fragments.py    correction of the fragments of known classes among the rejected
  select.py       choice of the family by leave-one-class-out on D_L
  baselines.py    SS-k-means (Vaze et al.) and closed-set classifier + rejector
  metrics.py      Hungarian ACC (All/Old/New), AUROC, FPR@95, false rejection
splits.py         GCD (C2) and NCD (C1) splits following Vaze et al.
run_gcd.py        command-line runner, saves a CSV
```

## Families (`--families`)

| Name  | Score | Note |
| ----- | ----- | ---- |
| gauss | Gaussian log-likelihood, Ledoit-Wolf covariance | stable in high dimension |
| knn   | minus the mean distance to the k neighbours | k = 5 |
| svm   | RBF one-class SVM | nu = 0.05 |
| mst   | minus the distance to the nearest edge of the MST | reimplementation of MSTDD from dd_tools |
| modes | mean of the OCCs of the nearest clusters, several segmentations | base in `--modes-base` (default knn) |
| dic   | P(same class) from the dichotomizer, mean over the k references | incorporating a class = storing its references |

## Baselines (`--families`)

| Name     | What it is | Uses D_L | Explicit rejection |
| -------- | ---------- | -------- | ------------------ |
| kmeans   | k-means on D_U with the total K | no | no |
| sskmeans | semi-supervised k-means of GCD (Vaze et al.) | yes | no |
| rf_msp   | random forest + maximum probability + k-means of the rejected | yes | yes |
| lr_msp   | logistic regression + maximum probability + k-means | yes | yes |
| hgb_msp  | histogram gradient boosting + maximum probability | yes | yes |
| ova_hgb  | one binary gradient boosting per class (one-vs-all), not normalized across classes | yes | yes |
| if_rf    | isolation forest on D_L as rejector, random forest classifies the accepted | yes | yes |

For these rejectors, the threshold is the alpha quantile of a cross-validated
score on D_L, with the same meaning of alpha as for the OCCs.

## Using your own features

```bash
# C2 (transductive GCD), 5 repetitions, K estimated by the silhouette
python run_gcd.py --X feats.npy --y labels.npy --scenario c2 \
    --seeds 0 1 2 3 4 --out results/base_c2.csv

# C1 (NCD) with the fixed Old split of PBN
python run_gcd.py --X feats.npy --y labels.npy --scenario c1 \
    --old-classes 0 1 2 3 4 --seeds 0
```

Useful options: `--alpha` (default 0.05), `--k-known` (uses the true K of
the novel classes), `--old-frac 0.8` (CIFAR-100), `--scale {all,labeled,none}`,
`--cal-mode {cv,split,nested}`.

**Standardization (`--scale`, default `all`)**: uses the mean and standard
deviation of D_L ∪ D_U, of the attributes only, without labels, which is
legitimate in the transductive setting. The `labeled` option (D_L only)
creates extreme values when an attribute barely varies within the known
classes: on digits, up to 90 standard deviations, which drops k-means from
0.78 to 0.59 ACC All.

## Tabular data sets of PBN (setting C2)

```bash
python prepare_pbn_datasets.py            # downloads from UCI; --with-census includes Census (~360 MB)
bash run_pbn_gcd.sh                       # 5 seeds, K estimated and known, α = 0.05 0.1 0.2
# only some data sets, another α, another folder, other families:
ALPHAS="0.1" OUT=results_v2 bash run_pbn_gcd.sh pendigits letter
FAMILIES="mst dic mst+ssk rf_msp" bash run_pbn_gcd.sh pendigits
```

Each α produces `$OUT/a<α>/summary.md`, with ACC All/Old/New, AUROC, false
rejection of Old, rejection of New (what is not rejected was absorbed by a
known class) and the K_new used by each method.

**Estimation of K (`--k-est`, default `labeled`)**: the criterion of Vaze
et al. (CVPR 2022): k-means on D_L ∪ D_U for each candidate K, choosing the
K that maximizes the Hungarian ACC on the labeled samples. The same estimate
is used for every method, which isolates the effect of the rejection.
`silhouette` is the old behaviour (each method estimates on its own
rejected samples).

**Correction of the fragments (`--k-est sil-size` or `hdbscan`)**: with
many known classes, the samples rejected by mistake form a small fragment
of each known class, and the silhouette counts each fragment as a novel
class (letter: ~30 instead of 7). The expected size of a fragment is
α/(1−α) × the accepted samples of the class, and the threshold is
τ = `--frag-c` (default 2) × the median of these sizes. `sil-size` returns
the clusters smaller than τ to the known classes and reclusters the rest.
`hdbscan` uses HDBSCAN with min_cluster_size = τ and sends the noise to the
nearest centroid (it falls back to `sil-size` if it finds no cluster).
`hdbscan-leaf` uses `cluster_selection_method="leaf"`, which picks finer
clusters and can separate neighbouring novel classes that the default mode
merges (on letter, `hdbscan` estimated 3.8 classes instead of 7). Details in
`occ/fragments.py`.

**Per-data-set preprocessing (`data/<base>/preproc.json`)**: if present,
`run_gcd.py --data` applies it to every method. Keys: `drop_cols` (removed
columns) and `l2` (normalizes each row, so the Euclidean distance becomes a
function of the cosine, and turns standardization off). We use
`{"l2": true}` on CNAE-9 (sparse word counts) and `{"drop_cols": [561]}` on
HAR (PBN adds the subject identifier as an attribute, which makes distances
group by person). `--no-preproc` ignores the file.

**Family `auto`**: chooses the OCC family with D_L only. Each known class
(up to 5) is left out and treated as novel, the others are split into
training (70%) and test, and the family with the highest mean AUROC of
known × "novel" wins. Candidates in `--auto-families` (default gauss knn mst
dic and the SVM with γ ∈ {0.1, 0.3, 1, 3, 10} × the default, written
`svm@g`). The CSV stores the chosen family (`chosen`) and the AUROCs
(`loco_*`).

**Criterion of `auto` (`--auto-criterion`, default `auroc`)**: `acc`
simulates the whole GCD on D_L. It hides 2 known classes (1 if there are
fewer than 4), runs rejection + HDBSCAN and measures ACC All, with ties
(< 0.005) broken by the simulated AUROC. `auroc` is the original criterion
(rejection only, one hidden class at a time). On the PBN data sets, `acc`
was worse (0.699 against 0.730, `results_v5/`): with 3 or 4 known classes,
the simulated GCD is small and noisy. The family `auto-auroc` always runs
`auto` with `auroc`. The same criterion applies to `svm-cv`.

**SVM with tuned γ (`svm-cv`)**: the one-class SVM cannot tune γ by
ordinary cross-validation, because there are no negatives. `svm-cv` uses the
same protocol as `auto` (hide a known class and treat it as novel) to choose
γ on the grid above. `svm` is the default γ of scikit-learn (`scale`).

**Variant `+ssk`** (e.g. `mst+ssk`): the rejected samples go to SS-k-means
with the known classes anchored on D_L, instead of plain k-means. It is not
the default: on digits it nearly removes false rejection, but it also
returns to the known classes the novel samples close to them (6 goes to 4,
9 to 3), and the Hungarian matching then swaps the known classes: ACC Old
drops from 0.82 to 0.39–0.54.

**Decision rule (`--decision`, default `pvalue`)**: `post` replaces the
conformal p-values by posterior probabilities (kernel density of the score
of each class, normalized across classes), and `hybrid` rejects with the
p-values and chooses among the accepting classes by the posterior. Used in
the ablation of the paper.

`prepare_pbn_datasets.py` reproduces the preprocessing and the known/novel
class split of the official PBN repository and saves them in
`data/<base>/`. `run_pbn_gcd.sh` writes one CSV per data set in `results/`,
the library versions in `results/versions.txt`, and calls `summarize.py`,
which builds `results/summary.md` with mean ± standard deviation per data
set, mean rank and paired Wilcoxon test against the best OCC.

Cautions when comparing with the PBN paper:

- In the old runs (folder `results/` without `a<α>`), `kmeans` with
  "estimated K" used the true K. It now uses the estimate.
- PBN reports the NCD setting (C1): the unlabeled set holds only novel
  classes, and ACC is measured on the test split. Here we run GCD (C2), in
  which D_U mixes known and novel classes, so the numbers are not directly
  comparable.
- With the fixed split of PBN, the 5 seeds vary the samples of D_L and D_U,
  not which classes are novel.
- CNAE-9: labels go from 1 to 9, but the split of PBN includes class 0,
  which does not exist. Hence 4 known and 5 novel classes, as in the paper.

## Additional data sets from OpenML

```bash
python prepare_pbn_datasets.py --only census --with-census   # the 7th data set of PBN
python prepare_openml_datasets.py                            # 9 candidates from OpenML
```

Criteria fixed before running the methods (see the header of
`prepare_openml_datasets.py`): ≥ 6 classes, ≥ 500 samples, classes with
fewer than 20 samples discarded, no raw images, and stratified subsampling
above 20,000 samples. Known classes = half of the classes, drawn with a
fixed seed. Each data set gets a `meta.json` with its source and
characteristics. The `summary.md` files include the Friedman test over data
sets (one observation per data set) and the Wilcoxon test with Holm's
correction.

## Incremental setting (C4)

```bash
bash run_pbn_c4.sh pendigits letter       # 3 sessions, 5 seeds, α = 0.1
bash run_pbn_c4.sh                        # every data set in data/
SESSIONS=10 bash run_pbn_c4.sh letter     # longer stream
```

Protocol (`run_c4.py`), inspired by Continual GCD (MetaGCD, Happy):
session 0 with D_L (half of the samples of the known classes). The novel
classes, drawn by the seed, debut over T sessions (default 3). Each
unlabeled batch brings part of the known classes, 60% of the classes that
debut and the rest of the ones discovered before. There are no labels after
session 0, sessions are disjoint, and standardization uses session 0 only.
The OCC incorporates each discovered cluster as a novel class without
retraining the known ones. `rf_msp` is retrained at every session with the
pseudo-labels (and must store the data), and `sskmeans` is refitted at every
session. The cluster → class matching is fixed in the session where the
cluster appears, so that a discovery error propagates. `summarize_c4.py`
produces `summary_c4.md` with ACC All/Old/New, forgetting of the classes of
session 0, discovered classes and time per session.

Options used in the paper: `--tau-s0` computes the fragment threshold τ once,
from the class sizes of session 0, and keeps it fixed, and `--alpha-disc 0.3`
makes discovered classes accept a sample only when its p-value is at least
0.3. Example:

```bash
EXTRA="--tau-s0 --alpha-disc 0.3" FAMILIES="auto-auroc" OUT=results_c4_tau bash run_pbn_c4.sh
```

## Implementation decisions worth knowing

- **Calibration by cross-validation within the class** (`cal_mode="cv"`,
  5 folds). With n calibration points, the smallest possible p-value is
  1/(n+1), and rejection is only possible if 1/(n+1) < α. Holding out 20%
  of a class with 45 samples gives 9 points and makes rejection impossible
  with α = 0.05. With cross-validation the whole class serves as
  calibration and the final OCC is trained with all samples. The code warns
  when a class is too small.
- **OCC-Dic**: with `--cal-mode cv`, the pair classifier is trained with all
  of D_L and the calibration is optimistic (false rejection of Old 0.28 with
  α = 0.2). Use `--cal-mode nested`: one forest per fold, without leakage
  (false rejection 0.16, ACC Old from 0.72 to 0.84, at the cost of 5 more
  forests). For the other families, `nested` is the same as `cv`.
- **MODES**: uses 4 of the 13 NbClust indices (silhouette,
  Calinski-Harabasz, Davies-Bouldin, Dunn). Each cluster OCC is standardized
  by its training scores before averaging. Pruning by region of competence
  between classes is off, because in an open world it forces a choice among
  known classes.
- **Labels**: the runner converts any label to integers 0..C-1, and -1 is
  reserved for rejection.

## Test on digits (raw pixels, 5 Old / 5 New, α = 0.2, known K, 5 seeds)

| Method | ACC All | ACC Old | ACC New | AUROC | False rej. Old |
| ------ | ------- | ------- | ------- | ----- | -------------- |
| rf_msp | 0.737 | 0.818 | 0.697 | 0.952 | 0.18 |
| mst | 0.722 | 0.784 | 0.692 | 0.917 | 0.18 |
| dic (nested) | 0.700 | 0.838 | 0.631 | 0.952 | 0.16 |
| gauss | 0.699 | 0.779 | 0.659 | 0.909 | 0.18 |
| lr_msp | 0.691 | 0.798 | 0.637 | 0.905 | 0.20 |
| knn | 0.673 | 0.789 | 0.614 | 0.894 | 0.17 |
| svm | 0.660 | 0.806 | 0.587 | 0.885 | 0.18 |
| kmeans | 0.654 | 0.511 | 0.726 | | |
| sskmeans | 0.653 | 0.646 | 0.656 | | |
| modes | 0.628 | 0.792 | 0.546 | 0.880 | 0.15 |

The closed-set classifier with MSP is the baseline to beat: on raw pixels it
outperforms every OCC. Digits serves as a smoke test, and the real tests are
with DINO features and the PBN data sets. The silhouette tends to
underestimate K_new on this data set (it chooses 2 instead of 5).

## Study with images (frozen DINO)

```bash
pip install torch torchvision certifi timm
python prepare_image_features.py --only cifar10 --max-samples 5000   # quick test
python prepare_image_features.py --only cifar10 cifar100             # full
python prepare_image_features.py --only cub --ssb-split cub_osr_splits.pkl
bash run_images.sh cifar10        # C2 in results_img/, C4 in results_img_c4/
```

`prepare_image_features.py` extracts the CLS vector of DINO ViT-B/16 once and
saves it in `data_img/<base>/` in the format of the tabular data sets, with
the class split of Vaze et al. (the same as SimGCD). After that everything
runs on CPU. For CUB, the SSB split comes from the SimGCD repository
(`data/ssb_splits/cub_osr_splits.pkl`). The scripts `run_pbn_gcd.sh` and
`run_pbn_c4.sh` accept `DATA=data_img`.

## Per-class selection (`auto-pc`)

`--families auto-pc` in `run_gcd.py`: each known class gets the family whose
OCC best separates the class from the hidden classes (same simulation as
`auto`, `occ/select.py: select_per_class`). Results in `results_pc/`.
