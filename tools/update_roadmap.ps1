# Este script leerá si existen archivos en engine/collision y marcará el ROADMAP
$roadmap = Get-Content "docs/ROADMAP.md"
if (Test-Path "engine/collision/aabb.py") {
    $roadmap = $roadmap -replace "- \[ \] \*\*Colisión AABB\*\*", "- [x] **Colisión AABB**"
}
$roadmap | Out-File "docs/ROADMAP.md" -Encoding utf8
Write-Host "📍 Roadmap actualizado con el progreso físico." -ForegroundColor Cyan