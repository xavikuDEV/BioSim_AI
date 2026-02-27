$path = "docs/ROADMAP.md"
$content = Get-Content $path -Raw

# Marcamos los hitos si los archivos existen
if (Test-Path "engine/collision/aabb.py") {
    $content = $content -replace "- \[ \] \*\*Colisión AABB\*\*", "- [x] **Colisión AABB**"
}
if (Test-Path "core/database.py") {
    $content = $content -replace "- \[ \] \*\*Persistencia WAL\*\*", "- [x] **Persistencia WAL**"
}
# Aseguramos Spawn Masivo
if (Test-Path "laboratory/white_room.py") {
    $content = $content -replace "- \[ \] \*\*Spawn Masivo\*\*", "- [x] **Spawn Masivo**"
}

$content | Set-Content $path -Encoding UTF8
Write-Host "📍 Roadmap sincronizado." -ForegroundColor Cyan