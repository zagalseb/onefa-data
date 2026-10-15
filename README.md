# onefa-data

Datos de la ONEFA (Liga Mayor) en archivos parquet, para leerlos desde Python.
Inspirado en `sportsdataverse-data`.

Se leen con el paquete [`onefa-py`](https://github.com/zagalseb/onefa-py):

```python
from onefa import load_onefa_teams

teams = load_onefa_teams()
```

O directo con pandas:

```python
import pandas as pd

url = "https://raw.githubusercontent.com/zagalseb/onefa-data/main/teams/onefa_teams.parquet"
teams = pd.read_parquet(url)
```

## Contenido

| Carpeta | Archivo | Contenido |
|---|---|---|
| `teams/` | `onefa_teams.parquet` | Una fila por equipo: nombres, colores, logos y estadio |
| `data-raw/` | `teams.csv` | Fuente editable; de aqui se genera el parquet |
| `scripts/` | `build_teams.py` | Valida el CSV y genera el parquet |

## Columnas de `onefa_teams`

| Columna | Descripcion |
|---|---|
| `id` | Identificador estable (`borregos_mty`). Nunca se cambia |
| `nombre`, `nombre_corto` | Nombre completo y como se muestra en tablas |
| `abreviatura` | Clave corta unica (`MTY`, `ABS`) |
| `institucion` | Universidad o instituto |
| `ciudad`, `estado` | Ubicacion de la sede |
| `conferencia` | Conferencia en la que juega |
| `logo_url` | Logo en PNG para fondo claro |
| `logo_oscuro_url` | Logo para fondo oscuro (puede estar vacio) |
| `color_primario`, `color_secundario` | Colores en hex |
| `color_primario_texto`, `color_secundario_texto` | Color de texto legible sobre cada uno |
| `estadio` | Nombre del estadio |
| `estadio_lat`, `estadio_lng` | Coordenadas en grados decimales |

## Actualizar los datos

Solo hay que subir `data-raw/teams.csv`. Una GitHub Action (`.github/workflows/build-teams.yml`) valida el CSV, regenera `teams/onefa_teams.parquet` y lo guarda sola.

1. Editar `data-raw/teams.csv` (mismos nombres de columna) y subirlo a `main`.
2. Revisar la pestana **Actions** del repo: una palomita verde significa que el parquet se actualizo; una X roja significa que el CSV tiene un error (el log dice cual) y el parquet anterior sigue intacto.

La validacion rechaza IDs o abreviaturas repetidos, colores que no sean `#RRGGBB`, campos obligatorios vacios y coordenadas fuera de Mexico.

Para generarlo a mano: `python scripts/build_teams.py` (necesita `pandas` y `pyarrow`). Si trabajas en local, haz `git pull` antes de editar, porque la Action agrega commits.

El `id` de un equipo no cambia aunque cambie su nombre; todo lo demas (juegos, jugadores, jugadas) se va a referenciar con ese `id`.
