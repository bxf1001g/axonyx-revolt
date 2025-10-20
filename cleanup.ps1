# Pre-Commit Cleanup Script
# Remove unnecessary files before pushing to GitHub

Write-Host "🧹 Cleaning up repository for GitHub..." -ForegroundColor Cyan

# Files and folders to remove (not tracked by git)
$itemsToRemove = @(
    "Desktop",
    "check_duplicates.py",
    "screenshots",
    ".vscode",
    "tests/__pycache__"
)

foreach ($item in $itemsToRemove) {
    $fullPath = Join-Path $PSScriptRoot $item
    if (Test-Path $fullPath) {
        Write-Host "Removing: $item" -ForegroundColor Yellow
        Remove-Item $fullPath -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# Replace README
$newReadme = Join-Path $PSScriptRoot "README_NEW.md"
$readme = Join-Path $PSScriptRoot "README.md"

if (Test-Path $newReadme) {
    Write-Host "Updating README.md..." -ForegroundColor Green
    Copy-Item $newReadme $readme -Force
    Remove-Item $newReadme -Force
}

# Organize documentation
Write-Host "`nℹ️  Documentation organization:" -ForegroundColor Cyan
Write-Host "  Essential docs in root:" -ForegroundColor White
Write-Host "    - README.md" -ForegroundColor Gray
Write-Host "    - GETTING_STARTED.md" -ForegroundColor Gray
Write-Host "    - QUICK_REFERENCE.md" -ForegroundColor Gray
Write-Host "    - MODEL_SELECTION_GUIDE.md" -ForegroundColor Gray
Write-Host "`n  Additional docs in root:" -ForegroundColor White
Write-Host "    - SETUP_GUIDE.md" -ForegroundColor Gray
Write-Host "    - PROJECT_OVERVIEW.md" -ForegroundColor Gray
Write-Host "    - CONFIRMATION_GUIDE.md" -ForegroundColor Gray
Write-Host "    - CROSS_PC_COMPATIBILITY.md" -ForegroundColor Gray
Write-Host "    - TESSERACT_SETUP.md" -ForegroundColor Gray
Write-Host "    - HYBRID_INSTALLER_AUTOMATION.md" -ForegroundColor Gray
Write-Host "`n  Advanced docs in docs folder:" -ForegroundColor White
Write-Host "    - docs/FLUTTER_GUI_SETUP.md" -ForegroundColor Gray
Write-Host "    - docs/GUI_SUMMARY.md" -ForegroundColor Gray
Write-Host "    - docs/GUI_VISUAL_GUIDE.md" -ForegroundColor Gray
Write-Host "    - docs/IMAGE_DOWNLOAD_FEATURE.md" -ForegroundColor Gray
Write-Host "    - docs/INSTALLER_AUTOMATION_V2.md" -ForegroundColor Gray
Write-Host "    - docs/CORRECT_MODEL_IDS.md" -ForegroundColor Gray
Write-Host "    - docs/FIXES_APPLIED.md" -ForegroundColor Gray

Write-Host "`n✅ Cleanup complete!" -ForegroundColor Green
Write-Host "`n📝 Next steps:" -ForegroundColor Cyan
Write-Host "  1. Review changes: git status" -ForegroundColor White
Write-Host "  2. Stage files: git add ." -ForegroundColor White
Write-Host "  3. Commit: git commit -m 'Initial commit with Flutter GUI'" -ForegroundColor White
Write-Host "  4. Push: git push origin main" -ForegroundColor White
