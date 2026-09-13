"""Minimal synthetic SCI demonstration; no Geneva or patient data."""
import numpy as np
from sci.spatial import knn_graph, moran_basis, singleton_msr_ensemble
from sci.patterns import top_fraction_pattern
from sci.metrics import weighted_jaccard

rng = np.random.default_rng(42)
coords = rng.uniform(0, 10_000, size=(80, 2))
surface_a = rng.normal(size=80)
surface_b = 0.5 * surface_a + rng.normal(scale=0.9, size=80)

W = knn_graph(coords, k=6)
_, V, _ = moran_basis(W)
h_a = top_fraction_pattern(surface_a, 0.10)
h_b = top_fraction_pattern(surface_b, 0.10)
observed = weighted_jaccard(h_a, h_b)

ensemble = singleton_msr_ensemble(surface_b, V, B=499, seed=20260912)
null = np.array([weighted_jaccard(h_a, top_fraction_pattern(s, 0.10)) for s in ensemble])
p_value = (1 + np.sum(null >= observed)) / (len(null) + 1)
print({"J": observed, "p_sci": p_value})
