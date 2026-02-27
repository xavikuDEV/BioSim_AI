function Show-Menu {
    Clear-Host
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "   🧬 BIOSIM_AI: COMMAND CENTER (v1.0)   " -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "1. 🧪 Ejecutar Sala Blanca (Visualizador)"
    Write-Host "2. 📊 Generar Mapa del Proyecto (Structure.md)"
    Write-Host "3. 📂 Sincronizar con GitHub (Git Push)"
    Write-Host "4. 📝 Crear Nueva Documentación (4 Capas)"
    Write-Host "5. 🧹 Limpiar Laboratorio (Logs/Cache)"
    Write-Host "6. 🏁 Ejecutar Suite de Tests"
    Write-Host "7. 🔍 Auditar Integridad Documental"
    Write-Host "8. 📖 Lanzar Wiki (MkDocs)"
    Write-Host "9.  EXIT"
    Write-Host "=========================================="
}

while ($true) {
    Show-Menu
    $choice = Read-Host "Selecciona una opción"
    switch ($choice) {
        1 { python laboratory/white_room.py }
        2 { .\tools\project_map.ps1 }
        3 { 
            $msg = Read-Host "Mensaje del Commit"
            .\tools\sync_git.ps1 $msg 
          }
        4 { 
            $name = Read-Host "Nombre del Sistema/Ley"
            .\tools\gen_doc.ps1 $name 
          }
        5 { .\tools\clean_lab.ps1 }
        6 { python -m pytest tests/ }
        7 { .\tools\audit_docs.ps1 }
        8 { Write-Host "Cierra la pestaña del navegador para volver al menú." -ForegroundColor Yellow; mkdocs serve }
        9 { break } # Sale del bucle
        default { Write-Host "Opción no válida" -ForegroundColor Red; Start-Sleep -Seconds 1 }
    }
}