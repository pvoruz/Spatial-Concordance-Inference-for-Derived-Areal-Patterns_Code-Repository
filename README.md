# Spatial Concordance Inference (SCI)

Open research-code repository accompanying:

**Spatial Concordance Inference for Derived Areal Patterns**

Target journal: *Spatial Statistics*.

SCI treats a hotspot map as a **derived statistical object** produced by a spatial estimator and a classifier. The repository contains archived source code from the frozen semi-synthetic Geneva workflow, validation scripts, reusable implementations of the core SCI components, documented figure-generation code, versioned development snapshots, and synthetic reference outputs.

## Read these first

- [`docs/CODE_PROVENANCE.md`](docs/CODE_PROVENANCE.md) — which files are archived originals versus later clean/reconstructed implementations.
- [`AI_USE_DISCLOSURE.md`](AI_USE_DISCLOSURE.md) — transparent statement on generative-AI assistance.
- [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md) — reproduction workflow and environment limitations.
- [`data/README.md`](data/README.md) — data boundary and public support acquisition.

## Repository structure

```text
src/sci/                       Reusable SCI library
scripts/official_application/  Archived original v5 application/validation scripts
scripts/reference_simulations/ Reconstructed reference implementations of earlier experiments
scripts/figures/               Reproducible figure scripts
configs/                       Frozen publication configuration and seed manifests
reference_outputs/             Synthetic/machine-readable reference outputs and manifests
archive/v1...v5/               Historical code snapshots preserved without rewriting
docs/                           Provenance, reproducibility, manuscript/code mapping
tests/                          Unit tests
```

## Scientific components

- unit-count, true-area, and population-weighted Jaccard estimands;
- pattern-conditional versus pattern-estimation-aware inference;
- singleton Moran spectral randomization (MSR);
- pair-MSR sensitivity;
- exact-N population-offset multinomial event generation;
- population-conditioned residual MSR;
- prospective estimability handling;
- directional/reference-conditional inference;
- frozen configurations, deterministic seed derivation, and SHA-256 provenance.

## Quick start

```bash
git clone https://github.com/pvoruz/Spatial-Concordance-Inference-for-Derived-Areal-Patterns_Code-Repository.git
cd spatial-concordance-inference

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e .
pytest -q
python examples_quickstart.py
```

## Reproducibility repair and canonical release

Release v0.2.0 resolves the provenance issues found during the automatic re-analysis audit. It adds:

- a frozen MEM basis for the official Geneva application;
- a separate frozen MEM basis for the singleton-versus-pair MSR sensitivity;
- the source-complete canonical fixed-versus-variable-mass benchmark;
- deterministic population-nuisance validation outputs;
- an end-to-end confirmation runner (`scripts/run_all_confirmatory.py`);
- explicit separation of superseded historical development results from current article-level evidence.

See [`docs/REPRODUCIBILITY_FIX_2026-09-13.md`](docs/REPRODUCIBILITY_FIX_2026-09-13.md).

## Important data boundary

The Geneva application is **strictly semi-synthetic**.

**Real**
- official Geneva areal geography and public population denominators;
- published aggregate clinical margins.

**Synthetic**
- all clinical spatial event allocations;
- latent risk fields;
- estimated risk surfaces;
- hotspot patterns.

No patient residential coordinates or empirical TBI hotspot geometries are distributed.

## Code provenance

The official Geneva application and its v5 validation scripts are preserved as **archived originals**. Some earlier simulation-development analyses were performed interactively and are not all available as standalone historical scripts. Their historical numerical values are retained in the methodological audit only and are not used as current confirmatory article evidence. Article-level simulation claims use the source-complete canonical benchmark and frozen validation workflows distributed in this release. Reconstructed code is always labelled and is never represented as the historical source file that produced a superseded development result.

## AI transparency

Generative AI was used as an assistive tool during the project. Full disclosure: [`AI_USE_DISCLOSURE.md`](AI_USE_DISCLOSURE.md).

## Citation

See [`CITATION.cff`](CITATION.cff). Add the manuscript DOI and repository/Zenodo DOI before release.

## License

Prepared under the MIT License for code. Confirm institutional/co-author approval before the first public release.
