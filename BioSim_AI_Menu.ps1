$running = $true

function Show-Menu {
    Clear-Host
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "    🧬 BIOSIM_AI: COMMAND CENTER (v3.0)    " -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "1.  🌌 [ERA 0] Lanzar El Génesis (Laboratorio)"
    Write-Host "2.  📊 Actualizar Mapa de Estructura (Structure.md)"
    Write-Host "3.  📂 Sincronizar con GitHub (Registro Sagrado)"
    Write-Host "4.  📝 Documentar Nueva Ley (SOURCE_*.md)"
    Write-Host "5.  🧹 Purga Total (Cache, Logs y DB)"
    Write-Host "6.  🏁 Suite de Estabilidad (PyTest Global)"
    Write-Host "7.  🔍 Auditoría de Integridad Documental"
    Write-Host "8.  📖 Abrir Wiki del Proyecto (MkDocs)"
    Write-Host "9.  🩺 Diagnóstico de Salud (Sistema + Datos)"
    Write-Host "10. 📍 Sincronizar Hoja de Ruta (Roadmap)"
    Write-Host "11. SALIR"
    Write-Host "=========================================="
}

while ($running) {
    Show-Menu
    $choice = Read-Host "Selecciona una opción"
    switch ($choice) {
        "1"  { python -m laboratory.white_room }
        "2"  { .\tools\project_map.ps1; Write-Host "✅ Mapa OK."; Start-Sleep -Seconds 1 }
        "3"  { 
            $msg = Read-Host "Mensaje del Commit"
            if ($msg) { .\tools\sync_git.ps1 $msg; pause }
        }
        "4"  { 
            $name = Read-Host "Nombre del Sistema"
            if ($name) { .\tools\gen_doc.ps1 $name; Start-Sleep -Seconds 1 }
        }
        "5"  { .\tools\clean_lab.ps1; pause }
        "6"  { python -m pytest tests/; pause }
        "7"  { .\tools\audit_docs.ps1; pause }
        "8"  { 
            Write-Host "🌍 Wiki en http://127.0.0.1:8000" -ForegroundColor Yellow
            Start-Process cmd "/c mkdocs serve" -WindowStyle Hidden
            Start-Sleep -Seconds 2
            Start-Process "http://127.0.0.1:8000"
        }
        "9"  { 
            Write-Host "`n🩺 Iniciando Diagnóstico Integral..." -ForegroundColor Cyan
            .\tools\health_check.ps1
            python .\tools\health_check.py
            pause 
        }
        "10" { .\tools\update_roadmap.ps1; pause }
        "11" { $script:running = $false }
        default { Write-Host "❌ Opción no válida." -ForegroundColor Red; Start-Sleep -Seconds 1 }
    }
}