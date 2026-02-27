param ( [string]$name = "nueva_ley" )
$path = "docs/systems/SOURCE_$name.md"
$content = @"
# 📜 SOURCE: $($name.ToUpper()) (v1.0)
## 1. Capa Conceptual (Arquitecto)
- **Objetivo:** Simular la aceleración vertical constante hacia el centro del mundo.
- **Soberanía:** Implementación propia para control total de la constante G sin depender de RigidBodies externos.

## 2. Capa Matemática (Ingeniero)
- **Ecuación:** $$ \vec{v}_{t+1} = \vec{v}_t + \vec{g} \cdot \Delta t $$
- **Variables:** $\vec{g}$ (Vector Gravedad), $\Delta t$ (Paso de tiempo: 0.016s).

## 3. Capa de Archivos (Programador)
- **Lógica:** \`engine/physics_vault/$name.py\`
- **Integración:** \`engine/integration/euler.py\`

## 4. Capa de Validación (Dios)
- **KPI:** Un objeto soltado a 10m debe tocar el suelo en aprox. 1.42s ($t = \sqrt{2h/g}$).
- **Test:** \`tests/unit/test_$name`_drop.py\`
"@ 

# Forzamos UTF8 para evitar caracteres extraños
[System.IO.File]::WriteAllLines($path, $content)
Write-Host "✅ Documento de Verdad generado en $path (UTF-8)" -ForegroundColor Green