#!/usr/bin/env python3
"""Fast cryptographic verification of the frozen v0.2.0 reference release.

This does not recompute simulations. It verifies that the exact frozen inputs,
MEM bases, reference outputs and current scripts match the release manifest.
Use run_all_confirmatory.py for computational re-execution.
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES=[
 'configs/FROZEN_MEM_BASIS_OFFICIAL_GENEVA.npz',
 'configs/FROZEN_MEM_BASIS_MSR_AUDIT.npz',
 'reference_outputs/results_summary.json',
 'reference_outputs/reverse_direction_results.json',
 'reference_outputs/canonical_benchmark_v1/canonical_benchmark_summary.csv',
 'reference_outputs/canonical_benchmark_v1/canonical_benchmark_replicates.csv',
 'reference_outputs/population_nuisance_v1/calibration_confirmatory_summary.csv',
 'reference_outputs/population_nuisance_v1/basis_screen_summary.csv',
 'reference_outputs/msr_variant_v3/msr_variant_summary_v3.csv',
 'scripts/reference_simulations/10_canonical_operator_target_benchmark.py',
 'scripts/official_application/94_msr_variant_sensitivity.py',
 'scripts/official_application/02_run_semi_synthetic_tbi.py',
 'scripts/official_application/11_verify_reverse_direction.py',
 'scripts/run_all_confirmatory.py',
]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
manifest_path=ROOT/'reference_outputs'/'release_v0.2.0_hash_manifest.json'
if '--write' in __import__('sys').argv:
    d={f:sha(ROOT/f) for f in FILES}
    manifest_path.write_text(json.dumps({'release':'v0.2.0','files':d},indent=2),encoding='utf-8')
    print(manifest_path); raise SystemExit(0)
exp=json.loads(manifest_path.read_text())['files']; bad=[]
for f,h in exp.items():
    a=sha(ROOT/f); ok=a==h; print(('PASS' if ok else 'FAIL'),f,a)
    if not ok: bad.append(f)
raise SystemExit(1 if bad else 0)
