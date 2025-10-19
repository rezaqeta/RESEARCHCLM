# Academia MCP - Clean Installation Guide

## Problem: Mixed Python Environments

Your system has multiple Python packages installed globally (R:\packages\python\site-packages) which can conflict with virtual environment packages. This guide provides a clean installation approach.

## Solution: Isolated Installation

### Option 1: Using `uv` (Recommended by academia-mcp)

The academia-mcp project recommends using `uv` for package management:

1. **Install uv:**

```powershell
pip install uv
```

2. **Run academia-mcp with uv:**

```sh
uv run -m academia_mcp --transport streamable-http
```

This automatically handles dependencies in an isolated environment.

### Option 2: Fresh Virtual Environment

1. **Deactivate current environment:**

```powershell
deactivate
```

2. **Create a completely fresh environment:**

```powershell
py -3.12 -m venv --clear academia-mcp-clean
.\academia-mcp-clean\Scripts\Activate.ps1
```

3. **Upgrade pip:**

```powershell
python -m pip install --upgrade pip
```

4. **Install academia-mcp with no cache:**

```powershell
pip install --no-cache-dir academia-mcp==1.8.1
```

### Option 3: Using `pipx` (Isolated Application)

```powershell
# Install pipx if not already installed
pip install pipx

# Install academia-mcp as an isolated application
pipx install academia-mcp==1.8.1

# Run it
academia-mcp --transport streamable-http
```

## Fixing Current Installation

### Step 1: Check Python is using venv

```powershell
Get-Command python | Select-Object Source
# Should show: R:\IDE\VLE\RESEARCHCLM\academia-mcp-env\Scripts\python.exe
```

### Step 2: Reinstall problematic packages

```powershell
pip uninstall pydantic pydantic-core -y
pip install --no-cache-dir pydantic==2.12.0 pydantic-core==2.41.1
```

### Step 3: Test installation

```powershell
python -c "from pydantic import BaseModel; print('Pydantic works!')"
```

## Environment Variables Setup

### For Current Session (PowerShell)

```powershell
$env:OPENROUTER_API_KEY="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"
```

### For Permanent Setup (PowerShell Profile)

1. **Edit your PowerShell profile:**

```powershell
notepad $PROFILE
```

2. **Add these lines:**

```powershell
# Academia MCP Configuration
$env:OPENROUTER_API_KEY="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"
```

3. **Reload profile:**

```powershell
. $PROFILE
```

### Using .env File (Recommended)

1. **Create `.env` file in your project directory:**

```sh
# R:\IDE\VLE\RESEARCHCLM\.env
OPENROUTER_API_KEY=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
WORKSPACE_DIR=R:\IDE\VLE\RESEARCHCLM\academia-workspace
```

2. **Install python-dotenv:**

```sh
pip install python-dotenv
```

3. **Load in Python:**

```python
from dotenv import load_dotenv
load_dotenv()
```

## Verification Steps

### 1. Check Python Version

```powershell
python --version
# Expected: Python 3.12.x or higher
```

### 2. Check Package Installation

```powershell
pip show academia-mcp
```

Expected output:
```
Name: academia-mcp
Version: 1.8.1
Summary: An MCP server for AI models to search academic papers
Home-page: https://github.com/IlyaGusev/academia_mcp
Author: Ilya Gusev
Requires: mcp, xmltodict, types-xmltodict, requests, ...
Required-by: 
```

### 3. Test Import (Basic)

```powershell
python -c "import mcp; print('MCP installed')"
```

### 4. Test Server (When working)

```powershell
python -m academia_mcp --help
```

## Troubleshooting Common Issues

### Issue 1: "ModuleNotFoundError: No module named 'pydantic_core._pydantic_core'"

**Cause**: Mixed Python versions or corrupted installation

**Fix**:

```powershell
pip uninstall pydantic pydantic-core -y
pip install --force-reinstall --no-cache-dir pydantic pydantic-core
```

### Issue 2: "PermissionError: [WinError 5] Access is denied"

**Cause**: Another Python process is using the package

**Fix**:
1. Close all Python processes
2. Restart PowerShell
3. Reinstall the package

### Issue 3: Virtual Environment Not Activating

**Fix**:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\academia-mcp-env\Scripts\Activate.ps1
```

### Issue 4: Packages Installing to Global Directory

**Cause**: Virtual environment not properly activated

**Fix**:

```powershell
# Check current pip location
Get-Command pip | Select-Object Source
# Should be in: ...\academia-mcp-env\Scripts\pip.exe

# If not, reactivate:
deactivate
.\academia-mcp-env\Scripts\Activate.ps1
```

## Alternative: Docker Installation (Future)

If environment issues persist, consider using Docker:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN pip install academia-mcp==1.8.1

ENV OPENROUTER_API_KEY=""

CMD ["python", "-m", "academia_mcp", "--transport", "streamable-http"]
```

## Quick Start Script

Save this as `start-academia-mcp.ps1`:

```powershell
# Start Academia MCP Server
# Usage: .\start-academia-mcp.ps1

# Activate virtual environment
$venvPath = "R:\IDE\VLE\RESEARCHCLM\academia-mcp-env"
& "$venvPath\Scripts\Activate.ps1"

# Set API key
$env:OPENROUTER_API_KEY="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"

# Start server
Write-Host "Starting Academia MCP Server..." -ForegroundColor Green
python -m academia_mcp --transport streamable-http

# Keep window open on error
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error occurred. Press any key to exit..." -ForegroundColor Red
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
```

## Next Steps

1. ✅ Review this installation guide
2. ⬜ Choose an installation method (uv recommended)
3. ⬜ Set up environment variables
4. ⬜ Test the installation
5. ⬜ Configure your AI assistant to use academia-mcp

## Support

If issues persist, consider:
1. Creating a GitHub issue: https://github.com/IlyaGusev/academia_mcp/issues
2. Checking the MCP documentation: https://modelcontextprotocol.io/
3. Using `uv` for automatic dependency management

---

**Last Updated**: October 10, 2025



