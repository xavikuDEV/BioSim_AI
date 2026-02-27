Write-Host "🔍 Auditando Integridad Documental..." -ForegroundColor Cyan

$engines = Get-ChildItem -Path "engine/physics_vault", "engine/biology" -Filter "*.py" | Where-Object { $_.Name -notmatch "__init__" }
$missing = 0

foreach ($file in $engines) {
    $name = $file.BaseName
    $docPath = "docs/systems/SOURCE_$name.md"
    
    if (-not (Test-Path $docPath)) {
        Write-Host "⚠️ FALTA DOC: El motor '$($file.Name)' no tiene SOURCE_$name.md" -ForegroundColor Yellow
        $missing++
    }
}

if ($missing -eq 0) {
    Write-Host "✅ Documentación al 100%. Soberanía garantizada." -ForegroundColor Green
} else {
    Write-Host "❌ Faltan $missing documentos de Verdad." -ForegroundColor Red
}