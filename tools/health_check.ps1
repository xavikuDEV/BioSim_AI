Write-Host "🩺 BIOSIM_AI: DIAGNÓSTICO DE SISTEMA" -ForegroundColor Cyan
$status = @{ "Verde" = 0; "Rojo" = 0 }

function Check($name, $cmd) {
    Invoke-Expression $cmd | Out-Null
    if ($LASTEXITCODE -eq 0) { 
        Write-Host "  [OK] $name" -ForegroundColor Green
        $script:status["Verde"]++
    } else { 
        Write-Host "  [FAIL] $name" -ForegroundColor Red
        $script:status["Rojo"]++
    }
}

# Verificaciones
Check "Python 3.11" "python --version"
Check "Ursina Engine" "python -c 'import ursina'"
Check "Base de Datos" "Test-Path data/db/biosim.db"

Write-Host "------------------------------------"
Write-Host "RESUMEN: $($status['Verde']) OK / $($status['Rojo']) FALLOS" -ForegroundColor Cyan