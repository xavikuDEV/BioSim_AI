# tools/update_roadmap.ps1
$path = "docs/ROADMAP.md"
$content = Get-Content $path -Raw # <--- CORREGIDO: Era Get-Content

function Mark-Hito([string]$hito, [bool]$condition) {
    if ($condition) {
        return $script:content -replace "- \[ \] \*\*$hito\*\*", "- [x] **$hito**"
    }
    return $script:content
}

# Comprobaciones
$has_friction = [bool](Select-String -Path "engine/movement_engine.py" -Pattern "AIR_RESISTANCE" -ErrorAction SilentlyContinue)
$has_bounds = [bool](Select-String -Path "engine/movement_engine.py" -Pattern "WORLD_SIZE" -ErrorAction SilentlyContinue)
$has_quadtree = Test-Path "engine/collision/quadtree.py"
$has_db = Test-Path "core/database.py"

$content = Mark-Hito "Colisión AABB" (Test-Path "engine/collision/aabb.py")
$content = Mark-Hito "Persistencia WAL" $has_db
$content = Mark-Hito "Optimización Espacial" $has_quadtree
$content = Mark-Hito "Leyes de Frontera" $has_bounds
$content = Mark-Hito "Resistencia Atmosférica" $has_friction

$content | Set-Content $path -Encoding UTF8
Write-Host "📍 Roadmap sincronizado con el tejido del universo." -ForegroundColor Cyan