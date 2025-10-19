# LlamaIndex Environment Activation Script
# Quick start script for LlamaIndex

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "  LlamaIndex Research Environment" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""

# Change to project directory
$projectDir = "r:\IDE\VLE\RESEARCHCLM"
Set-Location $projectDir

Write-Host "📁 Working Directory: " -NoNewline -ForegroundColor Yellow
Write-Host $projectDir -ForegroundColor White
Write-Host ""

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow

$venvPath = Join-Path $projectDir "llamaindex_env\Scripts\Activate.ps1"

if (Test-Path $venvPath) {
    & $venvPath
    Write-Host "✅ Virtual environment activated!" -ForegroundColor Green
} else {
    Write-Host "❌ Virtual environment not found at: $venvPath" -ForegroundColor Red
    Write-Host "   Run: python -m venv llamaindex_env" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "  Available Commands" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""

Write-Host "  1. " -NoNewline -ForegroundColor Cyan
Write-Host "python llamaindex_pdf_chunker.py" -ForegroundColor White
Write-Host "     → Chunk PDFs into smaller pieces" -ForegroundColor Gray
Write-Host ""

Write-Host "  2. " -NoNewline -ForegroundColor Cyan
Write-Host "python llamaindex_local_search.py" -ForegroundColor White
Write-Host "     → Interactive search (no API key needed)" -ForegroundColor Gray
Write-Host ""

Write-Host "  3. " -NoNewline -ForegroundColor Cyan
Write-Host "python llamaindex_research_pipeline.py" -ForegroundColor White
Write-Host "     → Full research pipeline with metadata" -ForegroundColor Gray
Write-Host ""

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""

Write-Host "📖 Documentation:" -ForegroundColor Yellow
Write-Host "   - Quick Start: " -NoNewline
Write-Host "LLAMAINDEX_QUICKSTART.md" -ForegroundColor White
Write-Host "   - Full Guide:  " -NoNewline
Write-Host "LLAMAINDEX_GUIDE.md" -ForegroundColor White
Write-Host ""

Write-Host "🚀 Ready to go! Type your command above." -ForegroundColor Green
Write-Host ""




