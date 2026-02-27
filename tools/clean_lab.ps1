# tools/clean_lab.ps1
Write-Host "🧹 Limpiando restos biológicos y logs..." -ForegroundColor Cyan

# Eliminar logs y snapshots
Remove-Item -Path "data/logs/*", "data/snapshots/*" -Force -ErrorAction SilentlyContinue

# Opcional: Eliminar base de datos de prueba
# Remove-Item -Path "data/db/biosim.db" -Force -ErrorAction SilentlyContinue

Write-Host "✨ Laboratorio listo para nueva ejecución." -ForegroundColor Green