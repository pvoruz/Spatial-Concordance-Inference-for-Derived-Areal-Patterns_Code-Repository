from __future__ import annotations
import numpy as np

def weighted_jaccard(a, b, weights=None) -> float:
    """Weighted Jaccard of Boolean areal patterns."""
    a = np.asarray(a, dtype=bool)
    b = np.asarray(b, dtype=bool)
    if a.shape != b.shape:
        raise ValueError("a and b must have the same shape")
    w = np.ones(a.size, dtype=float) if weights is None else np.asarray(weights, dtype=float)
    if w.shape != a.shape:
        raise ValueError("weights must match pattern shape")
    if np.any(w < 0):
        raise ValueError("weights must be non-negative")
    union = np.sum(w[a | b])
    return float(np.sum(w[a & b]) / union) if union > 0 else np.nan

def containment(a, b, weights=None) -> float:
    """Fraction of pattern a contained in b under the selected measure."""
    a = np.asarray(a, dtype=bool)
    b = np.asarray(b, dtype=bool)
    w = np.ones(a.size, dtype=float) if weights is None else np.asarray(weights, dtype=float)
    denom = np.sum(w[a])
    return float(np.sum(w[a & b]) / denom) if denom > 0 else np.nan
