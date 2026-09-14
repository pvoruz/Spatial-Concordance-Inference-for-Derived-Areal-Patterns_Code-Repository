"""Reusable components for Spatial Concordance Inference (SCI)."""
from .metrics import weighted_jaccard, containment
from .patterns import top_fraction_pattern, absolute_threshold_pattern
from .spatial import knn_graph, moran_basis, singleton_msr_ensemble, pair_msr_ensemble
from .simulate import correlated_gaussian_fields, exact_multinomial_events, gaussian_log_rr_surface
from .nuisance import population_design, population_mean_structure
