@echo off
cd /d "%~dp0"

set PYTHONUTF8=1

REM Default tuning values (can be overridden via .env or environment)
if not defined MISTRAL_IMAGE_MAX_SIDE set MISTRAL_IMAGE_MAX_SIDE=1024
if not defined MISTRAL_IMAGE_QUALITY set MISTRAL_IMAGE_QUALITY=85
if not defined MISTRAL_MAX_RETRIES set MISTRAL_MAX_RETRIES=3
if not defined MISTRAL_RETRY_DELAY_SECONDS set MISTRAL_RETRY_DELAY_SECONDS=2

REM Install/upgrade dependencies (safe to re-run)
python -u -m pip install --upgrade pip
python -u -m pip install -r requirements.txt

python -u main.py