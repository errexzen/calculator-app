$ErrorActionPreference = "Stop"

$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    Write-Error ".venv Python interpreter not found. Create and activate .venv first."
}

Push-Location $PSScriptRoot
try {
    & $python -m pip install -r requirements.txt
    & $python -m PyInstaller --name CalculatorApp --onefile --windowed --clean main.py
    Write-Host "Build completed. EXE output: dist\CalculatorApp.exe"
}
finally {
    Pop-Location
}
