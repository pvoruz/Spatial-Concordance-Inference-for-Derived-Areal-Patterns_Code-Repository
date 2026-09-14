from __future__ import annotations
import numpy as np

def top_fraction_pattern(values, fraction: float = 0.10):
    """Fixed-mass pattern containing approximately the top fraction of units."""
    v = np.asarray(values, dtype=float)
    if not 0 < fraction < 1:
        raise ValueError("fraction must lie in (0,1)")
    k = max(1, int(round(fraction * len(v))))
    idx = np.argpartition(v, len(v) - k)[len(v) - k:]
    h = np.zeros(len(v), dtype=bool)
    h[idx] = True
    return h

def absolute_threshold_pattern(values, threshold: float):
    """Variable-mass pattern defined by values > threshold."""
    return np.asarray(values, dtype=float) > float(threshold)
