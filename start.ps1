# Quick Start Script for Windows Agent
# Run this after installing dependencies

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Windows 11 Agentic AI - Quick Start" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "Found: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Virtual environment created!" -ForegroundColor Green
    Write-Host ""
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Check if dependencies are installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
$anthropicInstalled = pip show anthropic 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host "Dependencies installed!" -ForegroundColor Green
} else {
    Write-Host "Dependencies already installed!" -ForegroundColor Green
}
Write-Host ""

# Check for .env file
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host ""
    Write-Host "IMPORTANT: Edit .env file and add your Anthropic API key!" -ForegroundColor Red
    Write-Host "Get your key from: https://console.anthropic.com/" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter after you've added your API key to .env"
}

# Run the agent
Write-Host "Starting Windows Agent..." -ForegroundColor Green
Write-Host ""
python src/main.py
