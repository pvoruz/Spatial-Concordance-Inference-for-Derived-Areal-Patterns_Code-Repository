from __future__ import annotations
import numpy as np

def population_design(population, degree: int = 1):
    """Design in z(log1p population), optionally including centred powers."""
    pop = np.asarray(population, dtype=float)
    lp = np.log1p(pop)
    sd = lp.std()
    z = (lp - lp.mean()) / (sd if sd > 0 else 1.0)
    cols = [np.ones(len(z)), z]
    names = ["intercept", "zlog1p"]
    if degree >= 2:
        z2 = z ** 2
        cols.append(z2 - z2.mean()); names.append("centered_zlog1p_sq")
    if degree >= 3:
        z3 = z ** 3
        cols.append(z3 - z3.mean()); names.append("centered_zlog1p_cu")
    if degree not in (1, 2, 3):
        raise ValueError("degree must be 1, 2, or 3")
    return np.column_stack(cols), z, names

def population_mean_structure(surface, population, degree: int = 1):
    X, z, names = population_design(population, degree)
    s = np.asarray(surface, dtype=float)
    coef = np.linalg.lstsq(X, s, rcond=None)[0]
    mean = X @ coef
    residual = s - mean
    max_abs_Xte = float(np.max(np.abs(X.T @ residual)))
    return mean, residual, coef, z, names, max_abs_Xte
