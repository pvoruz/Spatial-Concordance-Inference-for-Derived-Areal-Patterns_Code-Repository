import numpy as np
from sci.metrics import weighted_jaccard
from sci.patterns import top_fraction_pattern
from sci.spatial import knn_graph, moran_basis, singleton_msr_ensemble
from sci.nuisance import population_mean_structure

def test_weighted_jaccard():
    a=np.array([1,1,0,0],bool); b=np.array([1,0,1,0],bool)
    assert abs(weighted_jaccard(a,b) - 1/3) < 1e-12
    w=np.array([2.,1.,1.,1.])
    assert abs(weighted_jaccard(a,b,w) - 0.5) < 1e-12

def test_top_fraction_mass():
    assert top_fraction_pattern(np.arange(100),0.10).sum() == 10

def test_msr_shapes():
    rng=np.random.default_rng(1)
    coords=rng.normal(size=(30,2))
    W=knn_graph(coords,4)
    _,V,_=moran_basis(W)
    ens=singleton_msr_ensemble(rng.normal(size=30),V,19,2)
    assert ens.shape == (19,30)

def test_population_residual_orthogonality():
    pop=np.arange(1,51,dtype=float)
    s=np.log1p(pop) + np.sin(np.arange(50))
    *_, ortho = population_mean_structure(s,pop,degree=1)
    assert ortho < 1e-8
