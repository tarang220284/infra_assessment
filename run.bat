@echo off
REM Backup & IRE Discovery Tool — single-command launcher (Windows)
setlocal
cd /d "%~dp0"

if not exist ".venv" (
  echo [setup] creating local virtualenv (.venv)...
  python -m venv .venv
  call .venv\Scripts\activate.bat
  pip install --quiet --upgrade pip
  pip install --quiet -r requirements.txt
) else (
  call .venv\Scripts\activate.bat
)

if not exist "data\seed.json" (
  echo [setup] ingesting source artifacts...
  python ingest.py
)

python app.py %*
endlocal
