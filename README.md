# Taller 1: Logística Panini para la Copa Mundial 2026

Implementación de referencia para algoritmos de búsqueda en problemas de logística de distribución sobre la red vial de Colombia.

> **Nota sobre este documento**: La redacción y estructura de este README fueron mejorados con asistencia de IA, siguiendo el protocolo de uso responsable de herramientas de inteligencia artificial en el proceso educativo.

## Configuración Rápida

Desde esta carpeta, ejecuta:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Red Vial de Colombia

El archivo `data/colombia_roads.json` contiene un grafo real de la red vial colombiana extraído de OpenStreetMap:

- **Fuente**: Capa `gis_osm_roads_free` de `colombia-latest-free.gpkg.zip` (Geofabrik)
- **Filtrado**: Incluye rutas de tipo `motorway`, `trunk`, `primary`, `secondary`, `tertiary` y variantes
- **Procesamiento**: Grafo no dirigido, componente conexa más grande, costos en kilómetros
- **Simplificación**: Cadenas de grado-2 comprimidas para preservar intersecciones y endpoints
- **Tamaño final**: 41,718 nodos y 64,126 aristas no dirigidas
- **Validación**: Una única componente conexa, costos positivos, aristas simétricas

## Ejemplos de Ejecución

Instancias predefinidas disponibles en `data/instances.json`:

```bash
# Entrega simple (minimizar kilómetros)
python main.py --instance single_bogota_medellin --show

# Entrega simple con A* (búsqueda informada)
python main.py --instance single_bogota_cartagena_astar --show

# Minimizar tramos (búsqueda desinformada)
python main.py --instance stops_bogota_cali_bfs --show

# Profundidad iterativa (búsqueda con límite)
python main.py --instance ids_local_depth --show

# Entregas múltiples (TSP-like)
python main.py --instance multi_andes_caribe --show
python main.py --instance multi_national_challenge --show
```

**Tip**: Usa `--show` para visualizar la ruta en un mapa interactivo del navegador con tiles de OpenStreetMap.

## Emparejamientos Recomendados (Problema - Algoritmo)

| Tipo de Problema | Algoritmo Recomendado | Objetivo |
|---|---|---|
| **single** | `ucs` o `astar` | Minimizar kilómetros totales |
| **stops** | `dfs`, `bfs` o `ids` | Minimizar número de tramos (aristas) |
| **multi** | `astar` con heurística multi-entrega | Minimizar kilómetros visitando todas las entregas |

**Nota del CLI**: El programa muestra una advertencia cuando se selecciona un algoritmo válido pero no recomendado para el tipo de problema.

## Explorar el Grafo

El notebook `notebooks/graph_visualization.ipynb` permite explorar la red vial completa:

- Carga y validación del grafo
- Visualización interactiva con Plotly/OpenStreetMap de todos los nodos y aristas
- Tooltips con atributos de nodos y aristas
- Búsqueda y selección de IDs de nodos para crear casos personalizados

## Estructura del Proyecto

```
.
├── algorithms/
│   ├── search.py          # Implementación de 6 algoritmos de búsqueda
│   ├── heuristics.py      # Funciones heurísticas para búsqueda informada
│   ├── problems.py        # Definiciones de problemas de búsqueda
│   └── utils.py           # Estructuras de datos (Stack, Queue, PriorityQueue)
├── graph/
│   └── road_graph.py      # Carga y validación del grafo vial
├── visualization/
│   └── map_view.py        # Generación de mapas interactivos
├── data/
│   ├── colombia_roads.json # Red vial real (41,718 nodos)
│   └── instances.json      # Casos de prueba predefinidos
├── notebooks/
│   └── graph_visualization.ipynb  # Exploración interactiva del grafo
├── main.py                # Interfaz de línea de comandos
└── requirements.txt       # Dependencias del proyecto
```

## Algoritmos Implementados

1. **DFS (Depth-First Search)** - Exploración en profundidad
2. **BFS (Breadth-First Search)** - Exploración en amplitud
3. **UCS (Uniform Cost Search)** - Búsqueda de costo uniforme (óptima para grafos ponderados)
4. **A\* Search** - Búsqueda informada con heurística
5. **DLS (Depth-Limited Search)** - DFS con límite de profundidad
6. **IDS (Iterative Deepening Search)** - DFS iterativo con límites crecientes

## Heurísticas Implementadas

1. **straightLineHeuristic** - Distancia geodésica (Haversine) al destino
2. **multiDeliveryHeuristic** - Límite inferior MST para TSP
3. **straightLineMultiDeliveryHeuristic** - Variante rápida usando solo geodésica

Todas las heurísticas son **admisibles** (nunca sobrestiman el costo real) y **consistentes** (respetan la desigualdad triangular).

---

**Última actualización**: 2026-06-14  
**Versión**: 1.0 - Solución de Referencia
