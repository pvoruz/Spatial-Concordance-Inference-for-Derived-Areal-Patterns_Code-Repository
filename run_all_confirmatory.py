#!/usr/bin/env python3
"""Run/verify the confirmatory analysis package from source.

The default mode runs the official Geneva analysis, reverse-direction audit,
repository tests, and verifies the frozen reference hashes. `--full` also
recomputes the canonical benchmark, population-nuisance analyses and the
1,000-replicate frozen-basis singleton/pair-MSR sensitivity.
"""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
ENV=os.environ.copy(); ENV.update({'OPENBLAS_NUM_THREADS':'5','OMP_NUM_THREADS':'5','MKL_NUM_THREADS':'5'})

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(cmd,cwd=ROOT):
    print('+',' '.join(map(str,cmd)),flush=True)
    subprocess.run(list(map(str,cmd)),cwd=cwd,env=ENV,check=True)
def check(label,actual,expected,out):
    ok=actual==expected; out.append({'check':label,'status':'PASS' if ok else 'FAIL','actual':actual,'expected':expected}); return ok

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--full',action='store_true'); ap.add_argument('--out',default=str(ROOT/'reference_outputs/verification_report_v2.json')); a=ap.parse_args()
    checks=[]
    with tempfile.TemporaryDirectory(prefix='sci_verify_') as td:
        td=Path(td); off=td/'official'
        run([sys.executable,'scripts/official_application/02_run_semi_synthetic_tbi.py','--support','data/official_support/prepared_support.geojson','--config','configs/config_publication.json','--frozen-basis','configs/FROZEN_MEM_BASIS_OFFICIAL_GENEVA.npz','--output-dir',off])
        check('official results_summary SHA256',sha(off/'results_summary.json'),sha(ROOT/'reference_outputs/results_summary.json'),checks)
        # CSV may contain platform-level floating differences in latent-risk columns; compare the actual published inferential columns exactly.
        x=pd.read_csv(off/'semi_synthetic_unit_results.csv'); y=pd.read_csv(ROOT/'reference_outputs/semi_synthetic_unit_results.csv')
        cols=['synthetic_cases_18_59','synthetic_cases_60plus','estimated_log_rr_18_59','estimated_log_rr_60plus','primary_hotspot_18_59','primary_hotspot_60plus','secondary_rr15_hotspot_18_59','secondary_rr15_hotspot_60plus']
        for c in cols:
            check('official unit output '+c, x[c].tolist(), y[c].tolist(),checks)
        rev=td/'reverse.json'; run([sys.executable,'scripts/official_application/11_verify_reverse_direction.py','--out',rev]);
        expected_rev=ROOT/'reference_outputs/reverse_direction_results.json'
        if expected_rev.exists(): check('reverse direction JSON SHA256',sha(rev),sha(expected_rev),checks)
        run([sys.executable,'scripts/official_application/93_verify_official_seed_derivation.py'])
        run([sys.executable,'-m','pytest','-q'])
        if a.full:
            can=td/'canonical'; run([sys.executable,'scripts/reference_simulations/10_canonical_operator_target_benchmark.py','--reps','1000','--B','199','--outdir',can])
            check('canonical summary SHA256',sha(can/'canonical_benchmark_summary.csv'),sha(ROOT/'reference_outputs/canonical_benchmark_v1/canonical_benchmark_summary.csv'),checks)
            check('canonical replicates SHA256',sha(can/'canonical_benchmark_replicates.csv'),sha(ROOT/'reference_outputs/canonical_benchmark_v1/canonical_benchmark_replicates.csv'),checks)
            pc=td/'popcal'; run([sys.executable,'scripts/official_application/96_population_nuisance_calibration.py','--reps','1000','--outdir',pc])
            check('population calibration summary SHA256',sha(pc/'summary.csv'),sha(ROOT/'reference_outputs/population_nuisance_v1/calibration_confirmatory_summary.csv'),checks)
            pb=td/'popbasis'; run([sys.executable,'scripts/official_application/95_population_nuisance_basis_screen.py','--outdir',pb])
            check('population basis summary SHA256',sha(pb/'summary.csv'),sha(ROOT/'reference_outputs/population_nuisance_v1/basis_screen_summary.csv'),checks)
            msr=td/'msr'; run([sys.executable,'scripts/official_application/94_msr_variant_sensitivity.py','--reps','1000','--B','199','--rho-values','0','.5','.65','--outdir',msr])
            check('MSR v3 summary SHA256',sha(msr/'msr_variant_summary_reproduced.csv'),sha(ROOT/'reference_outputs/msr_variant_v3/msr_variant_summary_v3.csv'),checks)
    report={'status':'PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL','full':a.full,'environment':{'OPENBLAS_NUM_THREADS':5,'OMP_NUM_THREADS':5,'MKL_NUM_THREADS':5},'checks':checks}
    Path(a.out).parent.mkdir(parents=True,exist_ok=True); Path(a.out).write_text(json.dumps(report,indent=2,default=str)); print(json.dumps(report,indent=2,default=str))
    raise SystemExit(0 if report['status']=='PASS' else 1)
if __name__=='__main__': main()
