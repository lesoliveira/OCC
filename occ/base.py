"""Interface comum dos OCCs.

Convenção: score(X) devolve um vetor em que valores MAIORES indicam
amostras MAIS típicas da classe-alvo. Todas as famílias seguem essa
convenção, o que permite calibrá-las do mesmo jeito (ver calibration.py).
"""
from abc import ABC, abstractmethod

import numpy as np


class BaseOCC(ABC):
    """Classificador de uma classe: treina só com amostras da classe-alvo."""

    @abstractmethod
    def fit(self, X):
        """Treina com X (n_amostras, n_atributos) da classe-alvo."""

    @abstractmethod
    def score(self, X):
        """Escore de tipicidade; maior = mais parecido com a classe-alvo."""

    def _check(self, X):
        X = np.asarray(X, dtype=float)
        if X.ndim != 2:
            raise ValueError("X deve ser uma matriz 2D (amostras x atributos)")
        return X
