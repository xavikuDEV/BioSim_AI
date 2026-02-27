Write-Host "🧪 Ejecutando Suite de Validación Global..." -ForegroundColor Cyan

# Ejecutar todos los archivos que empiecen por test_ en la carpeta tests/
$tests = Get-ChildItem -Path "tests" -Recurse -Filter "test_*.py"

foreach ($t in $tests) {
    Write-Host "Running: $($t.Name)" -ForegroundColor Gray
    python -m pytest $t.FullName --quiet
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "🏁 El Universo es estable." -ForegroundColor Green
} else {
    Write-Host "❌ Inestabilidad detectada en los tests." -ForegroundColor Red
}