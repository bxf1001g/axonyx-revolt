# Axonyx Revolt - GUI Quick Start Script

Write-Host "Axonyx Revolt - GUI Quick Start" -ForegroundColor Cyan
Write-Host ("=" * 50) -ForegroundColor Gray
Write-Host ""

# Check if Flutter is installed
Write-Host "[1/4] Checking Flutter installation..." -ForegroundColor Yellow
$flutterInstalled = Get-Command flutter -ErrorAction SilentlyContinue
if (-not $flutterInstalled) {
    Write-Host "ERROR: Flutter not found!" -ForegroundColor Red
    Write-Host "Please install Flutter from: https://flutter.dev/docs/get-started/install/windows" -ForegroundColor Yellow
    Write-Host "Or run: winget install --id=Flutter.Flutter -e" -ForegroundColor Yellow
    exit 1
}
Write-Host "SUCCESS: Flutter found - $(flutter --version | Select-Object -First 1)" -ForegroundColor Green

# Check if Python venv exists
Write-Host ""
Write-Host "[2/4] Checking Python environment..." -ForegroundColor Yellow
$venvPath = ".\.venv\Scripts\Activate.ps1"
if (-not (Test-Path $venvPath)) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Run: python -m venv .venv" -ForegroundColor Yellow
    exit 1
}
Write-Host "SUCCESS: Virtual environment found" -ForegroundColor Green

# Install Python dependencies
Write-Host ""
Write-Host "[3/4] Installing Python dependencies..." -ForegroundColor Yellow
& $venvPath
pip install -q fastapi uvicorn[standard]
if ($LASTEXITCODE -eq 0) {
    Write-Host "SUCCESS: Python dependencies installed" -ForegroundColor Green
} else {
    Write-Host "ERROR: Failed to install Python dependencies" -ForegroundColor Red
    exit 1
}

# Setup Flutter project
Write-Host ""
Write-Host "[4/4] Setting up Flutter project..." -ForegroundColor Yellow
Set-Location axonyx_gui

# Check if pubspec.yaml exists
if (-not (Test-Path "pubspec.yaml")) {
    Write-Host "ERROR: pubspec.yaml not found!" -ForegroundColor Red
    Write-Host "Make sure you're in the Axonyx_Revolt directory" -ForegroundColor Yellow
    exit 1
}

# Get Flutter dependencies
Write-Host "Getting Flutter dependencies..." -ForegroundColor Yellow
flutter pub get
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to get Flutter dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "SUCCESS: Flutter dependencies installed" -ForegroundColor Green

# Enable Windows desktop
Write-Host ""
Write-Host "Configuring Windows desktop support..." -ForegroundColor Yellow
flutter config --enable-windows-desktop
flutter create --platforms=windows .

Set-Location ..

Write-Host ""
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host ("=" * 50) -ForegroundColor Gray
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Start the Backend API:" -ForegroundColor Yellow
Write-Host "   cd D:\Git\Axonyx_Revolt" -ForegroundColor White
Write-Host "   .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "   python src/api_server.py" -ForegroundColor White
Write-Host ""
Write-Host "2. Start the Flutter GUI (new terminal):" -ForegroundColor Yellow
Write-Host "   cd D:\Git\Axonyx_Revolt\axonyx_gui" -ForegroundColor White
Write-Host "   flutter run -d windows" -ForegroundColor White
Write-Host ""
Write-Host "Backend URL: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Enjoy your beautiful GUI!" -ForegroundColor Magenta
