# NEURALFLOW PowerShell Launcher
param (
    [string]$Mode = "all"
)

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "                NEURALFLOW: RNN ARCHITECTURE BENCHMARK SYSTEM" -ForegroundColor Cyan
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host " Comparative Study: Vanilla RNN vs Bidirectional RNN vs LSTM vs GRU" -ForegroundColor White
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "[ERROR] Python was not found in your system PATH!" -ForegroundColor Red
    Write-Host "Please install Python 3.10+ and check 'Add Python to PATH'." -ForegroundColor Yellow
    exit 1
}

function Open-Everything {
    Write-Host "`n[1/4] Starting Web Server (app.py)..." -ForegroundColor Green
    Start-Process -FilePath "python" -ArgumentList "app.py --port 8000 --no-browser" -WindowStyle Hidden
    Start-Sleep -Seconds 2

    Write-Host "[2/4] Opening Web Dashboard in Browser..." -ForegroundColor Green
    Start-Process "http://127.0.0.1:8000"

    Write-Host "[3/4] Opening Standalone HTML Research Report..." -ForegroundColor Green
    Start-Process "http://127.0.0.1:8000/reports/experiment_report.html"

    Write-Host "[4/4] Opening Enterprise Technical Report and Visualizations..." -ForegroundColor Green
    if (Test-Path ".\NEURALFLOW_ENTERPRISE_SYSTEM_REPORT.docx") {
        Start-Process ".\NEURALFLOW_ENTERPRISE_SYSTEM_REPORT.docx"
    } elseif (Test-Path ".\NEURALFLOW_COMPLETE_PROJECT_REPORT.docx") {
        Start-Process ".\NEURALFLOW_COMPLETE_PROJECT_REPORT.docx"
    }
    if (Test-Path ".\loss_curves.png") {
        Start-Process ".\loss_curves.png"
    }
    if (Test-Path ".\confusion_matrices.png") {
        Start-Process ".\confusion_matrices.png"
    }

    Write-Host "`n===============================================================================" -ForegroundColor Cyan
    Write-Host " [SUCCESS] All application interfaces and reports are open!" -ForegroundColor Green
    Write-Host " - Web Dashboard: http://127.0.0.1:8000" -ForegroundColor White
    Write-Host " - HTML Report:   http://127.0.0.1:8000/reports/experiment_report.html" -ForegroundColor White
    Write-Host " - Word Report:   NEURALFLOW_ENTERPRISE_SYSTEM_REPORT.docx" -ForegroundColor White
    Write-Host " - Visualizations: loss_curves.png, confusion_matrices.png" -ForegroundColor White
    Write-Host "===============================================================================" -ForegroundColor Cyan
}

if ($Mode -eq "all") {
    Open-Everything
    exit 0
}
elseif ($Mode -eq "web") {
    python app.py
    exit 0
}
elseif ($Mode -eq "train") {
    python run_experiment.py
    exit 0
}
elseif ($Mode -eq "report") {
    python generate_docx_report.py
    exit 0
}

Write-Host "Select an option to start:" -ForegroundColor Yellow
Write-Host "  [1] Open Everything at Once (Dashboard + HTML Report + Word Doc + Plots) [Default]" -ForegroundColor Green
Write-Host "  [2] Launch Web Dashboard Only" -ForegroundColor White
Write-Host "  [3] Run Full Deep Learning Training Benchmark" -ForegroundColor White
Write-Host "  [4] Generate Enterprise Technical Report (.docx)" -ForegroundColor White
Write-Host "  [5] Install/Verify Dependencies" -ForegroundColor White
Write-Host "  [6] Exit" -ForegroundColor Gray
Write-Host ""

$choice = Read-Host "Enter your choice (1-6, default=1)"
if ([string]::IsNullOrWhiteSpace($choice)) { $choice = "1" }

switch ($choice) {
    "1" { Open-Everything }
    "2" { python app.py }
    "3" { python run_experiment.py }
    "4" { python generate_docx_report.py }
    "5" { pip install -r requirements.txt }
    "6" { exit 0 }
    Default { Open-Everything }
}
