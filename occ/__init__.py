"""Famílias de OCC para GCD com representações fixas (CPU)."""
from .families import GaussOCC, KNNOCC, SVMOCC, MSTOCC, make_occ
from .modes import MODESOCC
from .dichotomy import Dichotomizer, DichotomyOCC
from .calibration import ClassWiseOCC
from .kest import estimate_k, estimate_k_labeled
from .gcd import OCCDiscovery
from .select import select_family, select_per_class, loco_auroc, parse_spec, SVM_GRID
from .baselines import SSKMeans, ClosedMSP
from .metrics import cluster_acc, gcd_acc, rejection_metrics

FAMILY_NAMES = ["gauss", "knn", "svm", "mst", "modes", "dic"]
BASELINE_NAMES = ["kmeans", "sskmeans", "rf_msp", "lr_msp"]
# "+ssk": os rejeitados vão para o SS-k-means com as antigas ancoradas
SSK_NAMES = ["gauss+ssk", "knn+ssk", "mst+ssk", "dic+ssk", "rf_msp+ssk"]
