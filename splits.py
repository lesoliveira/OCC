"""Splits do protocolo GCD (Vaze et al.) a partir de X, y quaisquer."""
import numpy as np


def gcd_split(y, old_frac=0.5, labeled_frac=0.5, old_classes=None, seed=0):
    """Devolve (idx_l, idx_u, old_classes).

    old_frac:      fração das classes que são Old (0.5; 0.8 no CIFAR-100)
    labeled_frac:  fração das amostras de cada classe Old que vai para D_L
    old_classes:   lista fixa de classes Old (ex.: a divisão do PBN);
                   se None, sorteia com a semente
    """
    y = np.asarray(y)
    rng = np.random.default_rng(seed)
    classes = np.unique(y)
    if old_classes is None:
        n_old = max(2, int(round(old_frac * len(classes))))
        old_classes = np.sort(rng.choice(classes, n_old, replace=False))
    old_classes = np.asarray(old_classes)
    idx_l, idx_u = [], []
    for c in classes:
        idx = np.flatnonzero(y == c)
        if c in old_classes:
            idx = rng.permutation(idx)
            n_l = int(round(labeled_frac * len(idx)))
            idx_l.append(idx[:n_l])
            idx_u.append(idx[n_l:])
        else:
            idx_u.append(idx)
    return np.concatenate(idx_l), np.concatenate(idx_u), old_classes


def ncd_split(y, old_frac=0.5, old_classes=None, seed=0):
    """Cenário C1: D_L = todas as amostras Old; D_U = só classes novas."""
    y = np.asarray(y)
    rng = np.random.default_rng(seed)
    classes = np.unique(y)
    if old_classes is None:
        n_old = max(2, int(round(old_frac * len(classes))))
        old_classes = np.sort(rng.choice(classes, n_old, replace=False))
    old = np.isin(y, old_classes)
    return np.flatnonzero(old), np.flatnonzero(~old), np.asarray(old_classes)
