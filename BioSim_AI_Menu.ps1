$running = $true

function Show-Menu {
    Clear-Host
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "    🧬 BIOSIM_AI: COMMAND CENTER (v2.2)   " -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "1.  🌌 [ERA 0] Lanzar El Génesis (10k Entidades)"
    Write-Host "2.  📊 Actualizar Mapa de Soberanía (Structure.md)"
    Write-Host "3.  📂 Sincronizar con Registro Sagrado (GitHub)"
    Write-Host "4.  📝 Generar Nueva Fuente de Verdad (Doc 4 Capas)"
    Write-Host "5.  🧹 Purga de Laboratorio (Limpiar Cache/Logs)"
    Write-Host "6.  🏁 Ejecutar Suite de Estabilidad (Tests)"
    Write-Host "7.  🔍 Auditoría de Integridad Documental"
    Write-Host "8.  📖 Abrir Wiki del Proyecto (MkDocs)"
    Write-Host "9.  🩺 Diagnóstico de Salud del Sistema"
    Write-Host "10. 📍 Actualizar Hoja de Ruta (Roadmap)"
    Write-Host "11. SALIR"
    Write-Host "=========================================="
}

while ($running) {
    Show-Menu
    $choice = Read-Host "Selecciona una opción"
    switch ($choice) {
        "1" { python -m laboratory.white_room }
        "2" { .\tools\project_map.ps1; Write-Host "✅ Mapa OK."; Start-Sleep -Seconds 1 }
        "3" { 
            $msg = Read-Host "Mensaje del Commit (Vacío para cancelar)"
            if ($msg) { .\tools\sync_git.ps1 $msg; pause }
        }
        "4" { 
            $name = Read-Host "Nombre de la Ley (Vacío para cancelar)"
            if ($name) { .\tools\gen_doc.ps1 $name; Start-Sleep -Seconds 1 }
        }
        "5" { .\tools\clean_lab.ps1; pause }
        "6" { python -m pytest tests/; pause }
        "7" { .\tools\audit_docs.ps1; pause }
        "8" { 
            Write-Host "🌍 Abriendo Wiki en segundo plano..." -ForegroundColor Yellow
            Start-Process cmd "/c mkdocs serve" -WindowStyle Hidden
            Start-Sleep -Seconds 2
            Start-Process "http://127.0.0.1:8000"
        }
        "9" { .\tools\health_check.ps1; pause }
        "10" { .\tools\update_roadmap.ps1; Write-Host "✅ Roadmap actualizado."; pause }
        "11" { 
            Write-Host "👋 Cerrando sesión del Arquitecto..." -ForegroundColor Cyan
            $script:running = $false 
        }
        default { 
            Write-Host "❌ Opción no válida." -ForegroundColor Red
            Start-Sleep -Seconds 1 
        }
    }
}