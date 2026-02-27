# 📜 SOURCE: AABB (v1.0)
## 1. Capa Conceptual (Arquitecto)
- **Objetivo:** Impedir que las entidades atraviesen el suelo y, en el futuro, que se atraviesen entre sí.
- **Soberanía:** Detección geométrica pura (Axis-Aligned Bounding Box) para máximo rendimiento con 10,000 agentes.

## 2. Capa Matemática (Ingeniero)
- **Condición de Suelo:** $y_{pos} - radio \le 0$
- **Resolución:** $v_{y} = -v_{y} \cdot elasticidad$
- **Fricción:** $v_{x,z} = v_{x,z} \cdot fricción\_suelo$

## 3. Capa de Archivos (Programador)
- **Lógica:** `engine/collision/aabb.py`
- **Integración:** `engine/movement_engine.py`

## 4. Capa de Validación (Dios)
- **KPI:** Las entidades deben rebotar al tocar $y=0$ y perder altura en cada salto.
- **Test:** Ejecución visual en Sala Blanca (Era 0).