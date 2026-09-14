from __future__ import annotations
import math
import numpy as np
from scipy.spatial.distance import cdist

def correlated_gaussian_fields(coords, rho: float, spatial_range: float, seed: int):
    """Generate two standardized smooth Gaussian fields with latent correlation rho."""
    x = np.asarray(coords, dtype=float)
    D = cdist(x, x)
    K = np.exp(-(D / float(spatial_range)) ** 2) + np.eye(len(x)) * 1e-8
    L = np.linalg.cholesky(K)
    rng = np.random.default_rng(seed)
    g = L @ rng.normal(size=len(x))
    e = L @ rng.normal(size=len(x))
    g = (g - g.mean()) / g.std()
    e = (e - e.mean()) / e.std()
    s = rho * g + math.sqrt(max(0.0, 1 - rho * rho)) * e
    s = (s - s.mean()) / s.std()
    return g, s

def exact_multinomial_events(population, risk, N: int, beta: float, seed: int):
    """Exact-N population-offset multinomial event generation."""
    p = np.asarray(population, dtype=float)
    r = np.asarray(risk, dtype=float)
    w = p * np.exp(float(beta) * r)
    w = w / w.sum()
    return np.random.default_rng(seed).multinomial(int(N), w)

def gaussian_log_rr_surface(counts, population, coords, bandwidth: float):
    """Centroid-evaluated Gaussian-kernel log relative-risk surface."""
    c = np.asarray(counts, dtype=float)
    p = np.asarray(population, dtype=float)
    x = np.asarray(coords, dtype=float)
    D = cdist(x, x)
    K = np.exp(-0.5 * (D / float(bandwidth)) ** 2)
    den = K @ p
    local = (K @ c) / den
    global_rate = c.sum() / p.sum()
    return np.log(np.clip(local / global_rate, 1e-12, None))
