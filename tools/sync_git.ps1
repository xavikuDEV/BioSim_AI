param (
    [string]$msg = "update: sincronización de infraestructura BioSim_AI"
)

Write-Host "🚀 Sincronizando con el Registro Sagrado (GitHub)..." -ForegroundColor Cyan

# 1. Asegurar que estamos en la rama correcta
git branch -M main

# 2. Añadir todos los archivos (respetando el .gitignore)
git add .

# 3. Crear el commit
git commit -m $msg

# 4. Empujar a la nube
git push origin main

Write-Host "✅ Sincronización completada." -ForegroundColor Green
Write-Host "🌍 Verifica tu proyecto en: https://github.com/xavikuDEV/BioSim_AI" -ForegroundColor Cyan