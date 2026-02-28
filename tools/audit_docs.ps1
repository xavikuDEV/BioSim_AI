# tools/audit_docs.ps1
Write-Host "🔍 Auditando Integridad Documental..." -ForegroundColor Cyan
$enginePath = "engine"
$sourcePath = "docs/systems"
$missing = 0

# Buscamos en todas las subcarpetas del motor (biology, physics, vault...)
$modules = Get-ChildItem -Path "$enginePath" -Recurse -Filter "*.py" | Where-Object { $_.Name -notmatch "__init__" }

foreach ($module in $modules) {
    $baseName = $module.BaseName
    $docFile = Join-Path $sourcePath "SOURCE_$baseName.md"
    
    if (-not (Test-Path $docFile)) {
        Write-Host "⚠️ GENERANDO FUENTE: '$baseName.py' -> SOURCE_$baseName.md" -ForegroundColor Yellow
        
        # --- PLANTILLA MAESTRA DE 4 CAPAS (SSoT) ---
        $template = @"
# 📑 Fuente de Verdad: $baseName (v1.0)

## 1. Capa Conceptual (Arquitecto)
[Describe aquí qué fenómeno biológico o físico simula este archivo basándote en el Manifiesto del Arquitecto]

## 2. Capa Matemática (Ingeniero)
[Escribe aquí las fórmulas en LaTeX o lógica matemática del sistema]

## 3. Capa de Archivos (Programador)
- **Lógica Principal:** $($module.FullName.Replace((Get-Location).Path, ""))
- **Dependencias:** core/registry.py

## 4. Capa de Validación (Dios)
[Describe el Test de Pytest que garantiza que esta ley es inmutable]
"@
        $template | Out-File -FilePath $docFile -Encoding UTF8
        $missing++
    }
}

if ($missing -eq 0) {
    Write-Host "✅ Integridad Documental OK. Todas las leyes están selladas." -ForegroundColor Green
} else {
    Write-Host "ℹ️ Se han creado $missing nuevas Fuentes de Verdad. Por favor, revísalas en la Wiki." -ForegroundColor Cyan
}