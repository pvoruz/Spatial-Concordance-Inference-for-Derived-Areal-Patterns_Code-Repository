#!/usr/bin/env bash
set -euo pipefail
python3 scripts/00_fetch_sitg_official.py
python3 scripts/01_validate_prepare_support.py --input data/OCS_POPULATION_SSECTEUR.geojson --output-dir outputs/support
python3 scripts/02_run_semi_synthetic_tbi.py --support outputs/support/prepared_support.geojson --config config_publication.json --output-dir outputs/application
