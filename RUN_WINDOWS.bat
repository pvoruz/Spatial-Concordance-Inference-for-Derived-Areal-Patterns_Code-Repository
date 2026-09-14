@echo off
python scripts\00_fetch_sitg_official.py
if errorlevel 1 goto manual
python scripts\01_validate_prepare_support.py --input data\OCS_POPULATION_SSECTEUR.geojson --output-dir outputs\support
if errorlevel 1 exit /b 1
python scripts\02_run_semi_synthetic_tbi.py --support outputs\support\prepared_support.geojson --config config_publication.json --output-dir outputs\application
exit /b 0
:manual
echo Automatic SITG download failed. Download OCS_POPULATION_SSECTEUR manually from SITG.
exit /b 1
