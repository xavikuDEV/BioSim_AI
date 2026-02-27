param ( [string]$msg = "update: sincronización controlada" )

Write-Host "🛡️ Iniciando Protocolo de Vigilancia antes de subir..." -ForegroundColor Cyan

# 1. Actualizar Mapa
Write-Host "📍 Actualizando Structure.md..." -ForegroundColor Gray
.\tools\project_map.ps1 | Out-Null

# 2. Ejecutar Auditoría
$audit = .\tools\audit_docs.ps1
if ($audit -match "❌") {
    Write-Host "🛑 ERROR: No puedes subir cambios si falta documentación." -ForegroundColor Red
    exit
}

# 3. Ejecutar Tests
Write-Host "🧪 Validando estabilidad del motor..." -ForegroundColor Gray
python -m pytest tests/ --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "🛑 ERROR: Los tests han fallado. El código es inestable." -ForegroundColor Red
    exit
}

# 4. Sincronización Real
Write-Host "🚀 Todo correcto. Empujando al Registro Sagrado..." -ForegroundColor Green
git add .
git commit -m $msg
git push origin main