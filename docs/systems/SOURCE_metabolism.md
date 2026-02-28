# 🧬 Sistema de Metabolismo Primordial

## 1. Propósito (The Why)
Simular el consumo de recursos biológicos (Glucógeno) basado en el coste de existencia y el esfuerzo físico.

## 2. Implementación Técnica (The How)
Utiliza una `BioLayer` vinculada al ID de la entidad en el `REGISTRY`. El cálculo de gasto sigue la lógica de dos capas:
- **Metabolismo Basal:** Gasto constante por unidad de tiempo ($dt$).
- **Costo Cinético:** Gasto proporcional al cuadrado de la velocidad ($\sum v^2$).

## 3. Atributos Biológicos
- `energy`: Nivel actual (0 a 100).
- `metabolic_rate`: Gasto base (0.05 por tick).
- `is_alive`: Estado binario de la entidad.

## 4. Flujo de Muerte
Cuando `energy <= 0`, el motor metabólico marca la entidad como fallecida, llama a `log_death` y solicita al `REGISTRY` la eliminación de la entidad.