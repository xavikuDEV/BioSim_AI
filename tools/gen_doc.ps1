param ( [string]$name = "nueva_ley" )
$path = "docs/systems/SOURCE_$name.md"
@"
# 📜 SOURCE: $($name.ToUpper()) (v1.0)
## 1. Capa Conceptual (Arquitecto)
- **Objetivo:** [Describir qué fenómeno natural simulamos]
- **Soberanía:** [Por qué no usamos motores externos para esto]

## 2. Capa Matemática (Ingeniero)
- **Ecuación:** $$ \vec{F} = m \cdot \vec{g} $$
- **Variables:** $m$ (Masa), $g$ (Gravedad), $\Delta t$ (Time Step)

## 3. Capa de Archivos (Programador)
- **Lógica:** `engine/physics_vault/$name.py`
- **Integración:** `engine/integration/euler.py`

## 4. Capa de Validación (Dios)
- **KPI:** [Ej: La entidad debe caer X metros en Y segundos]
- **Test:** `tests/test_$name.py`
"@ | Out-File -FilePath $path -Encoding utf8
Write-Host "✅ Documento de Verdad generado en $path" -ForegroundColor Green