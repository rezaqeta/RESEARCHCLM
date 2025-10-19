<![CDATA[# Academia MCP Server Startup Script
# File: start-academia-mcp.ps1
# Purpose: Start the Academia MCP server with proper configuration

# Configuration
$VENV_PATH = "R:\IDE\VLE\RESEARCHCLM\academia-mcp-env"
$OPENROUTER_KEY = "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"
$TRANSPORT = "streamable-http"  # Options: stdio, streamable-http, sse

# Display header
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Academia MCP Server - Startup Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if virtual environment exists
Write-Host "[1/5] Checking virtual environment..." -ForegroundColor Yellow
if (-Not (Test-Path "$VENV_PATH\Scripts\python.exe")) {
    Write-Host "ERROR: Virtual environment not found at: $VENV_PATH" -ForegroundColor Red
    Write-Host "Please run: py -3.12 -m venv $VENV_PATH" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✓ Virtual environment found" -ForegroundColor Green
Write-Host ""

# Step 2: Activate virtual environment
Write-Host "[2/5] Activating virtual environment..." -ForegroundColor Yellow
try {
    & "$VENV_PATH\Scripts\Activate.ps1"
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to activate virtual environment" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Step 3: Set environment variables
Write-Host "[3/5] Setting environment variables..." -ForegroundColor Yellow
$env:OPENROUTER_API_KEY = $OPENROUTER_KEY
$env:WORKSPACE_DIR = "R:\IDE\VLE\RESEARCHCLM\academia-workspace"

# Create workspace directory if it doesn't exist
if (-Not (Test-Path $env:WORKSPACE_DIR)) {
    New-Item -ItemType Directory -Path $env:WORKSPACE_DIR -Force | Out-Null
    Write-Host "✓ Created workspace directory: $env:WORKSPACE_DIR" -ForegroundColor Green
}

Write-Host "✓ Environment variables set" -ForegroundColor Green
Write-Host "  - OPENROUTER_API_KEY: Set (hidden)" -ForegroundColor Gray
Write-Host "  - WORKSPACE_DIR: $env:WORKSPACE_DIR" -ForegroundColor Gray
Write-Host ""

# Step 4: Check Python and academia-mcp
Write-Host "[4/5] Verifying installation..." -ForegroundColor Yellow
$pythonVersion = & python --version 2>&1
Write-Host "  Python version: $pythonVersion" -ForegroundColor Gray

$academiaMcpCheck = & pip show academia-mcp 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: academia-mcp is not installed" -ForegroundColor Red
    Write-Host "Please run: pip install academia-mcp==1.8.1" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✓ academia-mcp is installed" -ForegroundColor Green
Write-Host ""

# Step 5: Start the server
Write-Host "[5/5] Starting Academia MCP Server..." -ForegroundColor Yellow
Write-Host "  Transport: $TRANSPORT" -ForegroundColor Gray
Write-Host "  Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Start the server
try {
    if ($TRANSPORT -eq "stdio") {
        python -m academia_mcp
    } else {
        python -m academia_mcp --transport $TRANSPORT
    }
} catch {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host "ERROR: Server stopped unexpectedly" -ForegroundColor Red
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host $_.Exception.Message -ForegroundColor Red
}

# Cleanup on exit
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Server stopped." -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Cyan
Read-Host "Press Enter to exit"
]]>





