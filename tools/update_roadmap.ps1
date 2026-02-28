# tools/update_roadmap.ps1
$path = "docs/ROADMAP.md"
if (-not (Test-Path $path)) { 
    Write-Host "⚠️ No se encontró ROADMAP.md" -ForegroundColor Yellow
    return 
}

$content = Get-Content $path -Raw

function Update-Hito([string]$text, [string]$hito, [bool]$condition) {
    if ($condition) {
        # Escapamos caracteres especiales de forma segura para PowerShell
        $escapedHito = [regex]::Escape($hito)
        # Buscamos el patrón "- [ ] **Hito**"
        $pattern = "(?m)^-\s*\[\s*\]\s*\*\*$escapedHito\*\*"
        $replacement = "- [x] **$hito**"
        return $text -replace $pattern, $replacement
    }
    return $text
}

# --- COMPROBACIONES EN EL NUEVO PUZLE MODULAR ---
$has_friction = [bool](Select-String -Path "engine/physics/forces.py" -Pattern "AIR_RESISTANCE" -ErrorAction SilentlyContinue)
$has_bounds   = [bool](Select-String -Path "engine/physics/forces.py" -Pattern "world_size" -ErrorAction SilentlyContinue)
$has_mitosis  = Test-Path "engine/biology/mitosis.py"
$has_db       = Test-Path "core/database.py"

# Actualizamos el contenido en cadena
$content = Update-Hito $content "Resistencia Atmosférica" $has_friction
$content = Update-Hito $content "Leyes de Frontera" $has_bounds
$content = Update-Hito $content "Mecanismo de Mitosis" $has_mitosis
$content = Update-Hito $content "Persistencia WAL" $has_db

# Guardamos el resultado
$content | Set-Content $path -Encoding UTF8
Write-Host "✅ Roadmap sincronizado con la nueva estructura modular." -ForegroundColor Green