from __future__ import annotations
import math
import numpy as np
from scipy.linalg import eigh
from sklearn.neighbors import NearestNeighbors

def knn_graph(coords, k: int = 6):
    """Undirected k-nearest-neighbour graph, row-standardized."""
    x = np.asarray(coords, dtype=float)
    if k < 1 or k >= len(x):
        raise ValueError("k must be between 1 and n-1")
    _, idx = NearestNeighbors(n_neighbors=k + 1).fit(x).kneighbors(x)
    A = np.zeros((len(x), len(x)), dtype=float)
    for i in range(len(x)):
        for j in idx[i, 1:]:
            A[i, j] = A[j, i] = 1.0
    if np.any(A.sum(axis=1) == 0):
        raise ValueError("isolated spatial unit")
    return A / A.sum(axis=1, keepdims=True)

def moran_basis(W, drop_constant: bool = False, descending: bool = False):
    """Eigenbasis of the symmetrized, double-centred spatial operator."""
    W = np.asarray(W, dtype=float)
    S = (W + W.T) / 2.0
    C = S - S.mean(1, keepdims=True) - S.mean(0, keepdims=True) + S.mean()
    lam, V = eigh(C, check_finite=False)
    if drop_constant:
        const_idx = int(np.argmax(np.abs(V.T @ np.ones(len(V)) / math.sqrt(len(V)))))
        keep = np.arange(len(lam)) != const_idx
        lam, V = lam[keep], V[:, keep]
    if descending:
        order = np.argsort(lam)[::-1]
        lam, V = lam[order], V[:, order]
    return lam, V, C

def singleton_msr_ensemble(surface, V, B: int, seed: int):
    """Singleton MSR via independent sign randomization of spectral coefficients."""
    s = np.asarray(surface, dtype=float)
    z = s - s.mean()
    c = V.T @ z
    rng = np.random.default_rng(seed)
    active = np.abs(c) > 1e-12
    signs = np.ones((len(c), B), dtype=float)
    signs[active] = rng.choice([-1.0, 1.0], size=(active.sum(), B))
    return (s.mean() + V @ (c[:, None] * signs)).T

def pair_msr_ensemble(surface, V, B: int, seed: int):
    """Pair-MSR sensitivity using random rotations in consecutive eigenvector pairs."""
    s = np.asarray(surface, dtype=float)
    c = V.T @ (s - s.mean())
    rng = np.random.default_rng(seed)
    out = np.empty((len(c), B), dtype=float)
    upto = len(c) - (len(c) % 2)
    for j in range(0, upto, 2):
        radius = float(np.hypot(c[j], c[j + 1]))
        phi = rng.uniform(0, 2 * np.pi, size=B)
        out[j] = radius * np.cos(phi)
        out[j + 1] = radius * np.sin(phi)
    if len(c) % 2:
        out[-1] = c[-1] * rng.choice([-1.0, 1.0], size=B)
    return (s.mean() + V @ out).T
