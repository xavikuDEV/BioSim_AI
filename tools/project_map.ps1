function Get-Tree($Path, $Indent = "") {
    $items = Get-ChildItem -Path $Path | Where-Object { 
        $_.Name -notmatch "venv|\.git|\.vscode|\.agent|__pycache__|biosim\.db|\.pytest_cache" 
    }
    
    $count = $items.Count
    for($i=0; $i -lt $count; $i++) {
        $item = $items[$i]
        $isLast = ($i -eq $count - 1)
        
        # Selección de carácter de rama
        $char = if ($isLast) { "└── " } else { "├── " }
        
        # Construcción de la línea
        $line = $Indent + $char + $item.Name
        $line | Out-File -FilePath Structure.md -Append -Encoding utf8
        
        # Recursión para carpetas
        if ($item.PSIsContainer) {
            # Ajuste de indentación exacto para tu formato
            $nextIndent = if ($isLast) { "    " } else { "│   " }
            Get-Tree -Path $item.FullName -Indent ($Indent + $nextIndent)
        }
    }
}

# 1. Limpieza y Encabezado según tu estándar
$date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$header = "# 🗺️ Estructura del Proyecto: BioSim_AI`n"
$header += "## Generado: $date`n"
$header += "---`n"
$header | Out-File -FilePath Structure.md -Encoding utf8

# 2. Ejecución
Get-Tree -Path "."

# 3. Feedback
Write-Host "✅ Structure.md generado con el formato de diseño." -ForegroundColor Green