# Axonyx Revolt - GUI Launcher

param(
    [switch]$Backend,
    [switch]$GUI,
    [switch]$Both
)

function Start-Backend {
    Write-Host "Starting Backend API Server..." -ForegroundColor Cyan
    Write-Host ""
    
    Set-Location $PSScriptRoot
    & .\.venv\Scripts\Activate.ps1
    
    Write-Host "Backend URL: http://localhost:8000" -ForegroundColor Green
    Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Green
    Write-Host ""
    
    python src/api_server.py
}

function Start-GUI {
    Write-Host "Starting Flutter GUI..." -ForegroundColor Cyan
    Write-Host ""
    
    Set-Location "$PSScriptRoot\axonyx_gui"
    
    Write-Host "Launching Axonyx Revolt GUI..." -ForegroundColor Green
    Write-Host ""
    
    flutter run -d windows --release
}

function Start-Both {
    Write-Host "Starting Both Backend and GUI..." -ForegroundColor Cyan
    Write-Host ""
    
    # Start backend in new terminal
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '$PSScriptRoot\launch_gui.ps1' -Backend"
    
    # Wait a bit for backend to start
    Start-Sleep -Seconds 3
    
    # Start GUI in current terminal
    Start-GUI
}

# Main logic
if ($Backend) {
    Start-Backend
}
elseif ($GUI) {
    Start-GUI
}
elseif ($Both) {
    Start-Both
}
else {
    Write-Host "Axonyx Revolt - GUI Launcher" -ForegroundColor Cyan
    Write-Host ("=" * 50) -ForegroundColor Gray
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\launch_gui.ps1 -Backend    # Start backend API only" -ForegroundColor White
    Write-Host "  .\launch_gui.ps1 -GUI        # Start GUI only" -ForegroundColor White
    Write-Host "  .\launch_gui.ps1 -Both       # Start both (recommended)" -ForegroundColor White
    Write-Host ""
    Write-Host "Recommended: Run with -Both flag" -ForegroundColor Cyan
    Write-Host ""
    
    $choice = Read-Host "Start both? (y/n)"
    if ($choice -eq 'y' -or $choice -eq 'Y') {
        Start-Both
    }
}
