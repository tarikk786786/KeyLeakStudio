@echo off
setlocal
chcp 65001 >nul
title KeyLeak Detector Studio - Runtime Security Scanner

echo ===============================================================================
echo Starting KeyLeak Detector Studio...
echo Repository: https://github.com/Amal-David/keyleak-detector
echo ===============================================================================
echo.

cd /d "%~dp0"

set "PYTHONIOENCODING=utf-8"
set "PYTHONUTF8=1"

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in system PATH.
    echo Please install Python 3.12 or higher.
    pause
    exit /b 1
)

python launcher.py %*

if %errorlevel% neq 0 (
    echo.
    echo [NOTICE] Process ended.
    pause
)

endlocal
