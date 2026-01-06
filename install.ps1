Write-Host "Verificando Python..." -ForegroundColor Cyan

try {
    $pythonVersion = py --version 2>&1
    if (-not $pythonVersion) {
        $pythonVersion = python --version 2>&1
    }
    Write-Host "Python encontrado: $pythonVersion" -ForegroundColor Green
    $pythonCmd = if (Get-Command py -ErrorAction SilentlyContinue) { "py" } else { "python" }
} catch {
    Write-Host "Python nao encontrado! Por favor, instale o Python primeiro." -ForegroundColor Red
    Write-Host "Baixe em: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host ""
Write-Host "Atualizando pip..." -ForegroundColor Cyan
& $pythonCmd -m pip install --upgrade pip

Write-Host ""
Write-Host "Instalando dependencias do requirements.txt..." -ForegroundColor Cyan
& $pythonCmd -m pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Dependencias instaladas com sucesso!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Erro ao instalar dependencias!" -ForegroundColor Red
}

Read-Host "Pressione Enter para sair"

