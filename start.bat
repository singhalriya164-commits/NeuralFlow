@echo off
setlocal enabledelayedexpansion
title NEURALFLOW - Comparative RNN Benchmark

cd /d "%~dp0"

echo ===============================================================================
echo                NEURALFLOW: RNN ARCHITECTURE BENCHMARK SYSTEM
echo ===============================================================================
echo  Comparative Study: Vanilla RNN vs Bidirectional RNN vs LSTM vs GRU
echo ===============================================================================
echo.

:: Check Python installation
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python was not found in your system PATH!
    echo Please install Python 3.10+ and check "Add Python to PATH".
    pause
    exit /b 1
)

:: If argument given, jump directly
if /i "%1"=="all" goto run_all
if /i "%1"=="web" goto run_web
if /i "%1"=="dashboard" goto run_web
if /i "%1"=="train" goto run_train
if /i "%1"=="report" goto run_report
if /i "%1"=="install" goto run_install

:menu
echo Select an option to start:
echo.
echo   [1] Open Everything at Once (Dashboard + HTML Report + Word Doc + Plots) [Default]
echo   [2] Launch Web Dashboard Only (http://127.0.0.1:8000)
echo   [3] Run Full Deep Learning Training Benchmark (Retrain all 4 models)
echo   [4] Generate Enterprise Technical Report (.docx)
echo   [5] Install/Verify Dependencies (pip install -r requirements.txt)
echo   [6] Exit
echo.
set /p choice="Enter your choice (1-6, default=1): "
if "%choice%"=="" set choice=1
if "%choice%"=="1" goto run_all
if "%choice%"=="2" goto run_web
if "%choice%"=="3" goto run_train
if "%choice%"=="4" goto run_report
if "%choice%"=="5" goto run_install
if "%choice%"=="6" exit /b 0

echo Invalid selection. Please choose 1 to 6.
echo.
goto menu

:run_all
echo.
echo ===============================================================================
echo [1/4] Starting NeuralFlow Web Server...
start "" /b python app.py --port 8000 --no-browser
timeout /t 2 /nobreak >nul

echo [2/4] Opening Interactive Web Dashboard...
start http://127.0.0.1:8000

echo [3/4] Opening Standalone HTML Research Report...
start http://127.0.0.1:8000/reports/experiment_report.html

echo [4/4] Opening Enterprise Technical Report and Visualizations...
if exist "NEURALFLOW_ENTERPRISE_SYSTEM_REPORT.docx" (start "" "NEURALFLOW_ENTERPRISE_SYSTEM_REPORT.docx") else (if exist "NEURALFLOW_COMPLETE_PROJECT_REPORT.docx" start "" "NEURALFLOW_COMPLETE_PROJECT_REPORT.docx")
if exist "loss_curves.png" start "" "loss_curves.png"
if exist "confusion_matrices.png" start "" "confusion_matrices.png"

echo.
echo ===============================================================================
echo [SUCCESS] Everything has been opened!
echo - Web Dashboard: http://127.0.0.1:8000
echo - HTML Report:   http://127.0.0.1:8000/reports/experiment_report.html
echo - Word Document: NEURALFLOW_COMPLETE_PROJECT_REPORT.docx
echo - Key Plots:     loss_curves.png, confusion_matrices.png
echo ===============================================================================
echo Keep this terminal open while using the web dashboard.
echo Press Ctrl+C or close this window when done.
python -c "import time; [time.sleep(3600) for _ in range(24)]"
goto end

:run_web
echo.
echo [Starting] Launching NeuralFlow Web Dashboard...
echo [URL] http://127.0.0.1:8000
echo (Opening dashboard in your default browser...)
python app.py
goto end

:run_train
echo.
echo [Starting] Executing Full Comparative Training Benchmark...
echo (Training Vanilla RNN, Bidirectional RNN, LSTM, and GRU on CPU/GPU...)
python run_experiment.py
goto end

:run_report
echo.
echo [Starting] Compiling Enterprise Architectural Report (.docx)...
python generate_docx_report.py
goto end

:run_install
echo.
echo [Starting] Installing required dependencies from requirements.txt...
pip install -r requirements.txt
echo.
echo [Done] Dependencies check completed.
pause
goto menu

:end
pause
