"""Genera teams/onefa_teams.parquet a partir de data-raw/teams.csv.

Uso (desde la raiz del repo):
    python scripts/build_teams.py

Valida el CSV antes de escribir el parquet. Si algo falla, no escribe nada.
"""
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
ENTRADA = ROOT / "data-raw" / "teams.csv"
SALIDA = ROOT / "teams" / "onefa_teams.parquet"

COLUMNAS = [
    "id", "nombre", "nombre_corto", "abreviatura", "institucion",
    "ciudad", "estado", "conferencia",
    "logo_url", "logo_oscuro_url",
    "color_primario", "color_primario_texto",
    "color_secundario", "color_secundario_texto",
    "estadio", "estadio_lat", "estadio_lng",
]
COLUMNAS_COLOR = [c for c in COLUMNAS if c.startswith("color_")]
OBLIGATORIAS = [
    "id", "nombre", "nombre_corto", "abreviatura", "institucion",
    "ciudad", "estado", "conferencia", "color_primario",
    "color_primario_texto", "estadio", "estadio_lat", "estadio_lng",
]


def validar(df: pd.DataFrame) -> list[str]:
    errores = []

    faltan = [c for c in COLUMNAS if c not in df.columns]
    sobran = [c for c in df.columns if c not in COLUMNAS]
    if faltan:
        errores.append(f"Faltan columnas: {faltan}")
    if sobran:
        errores.append(f"Columnas no esperadas: {sobran}")
    if faltan:
        return errores

    for col in ("id", "abreviatura"):
        dup = df.loc[df[col].duplicated(), col].tolist()
        if dup:
            errores.append(f"Valores repetidos en {col}: {dup}")

    for col in OBLIGATORIAS:
        vacios = df.loc[df[col].isna(), "id"].tolist()
        if vacios:
            errores.append(f"{col} vacio en: {vacios}")

    patron = re.compile(r"^#[0-9a-fA-F]{6}$")
    for col in COLUMNAS_COLOR:
        malos = df.loc[df[col].notna() & ~df[col].astype(str).str.match(patron), "id"].tolist()
        if malos:
            errores.append(f"{col} no es hex (#RRGGBB) en: {malos}")

    fuera = df.loc[
        ~df["estadio_lat"].between(14, 33) | ~df["estadio_lng"].between(-118, -86), "id"
    ].tolist()
    if fuera:
        errores.append(f"Coordenadas fuera de Mexico en: {fuera}")

    return errores


def main() -> int:
    df = pd.read_csv(ENTRADA, encoding="utf-8")
    errores = validar(df)
    if errores:
        print("No se genero el parquet:")
        for e in errores:
            print(f"  - {e}")
        return 1

    df = df[COLUMNAS].copy()
    texto = [c for c in COLUMNAS if not c.startswith("estadio_l")]
    df[texto] = df[texto].astype("string")
    df = df.sort_values("id").reset_index(drop=True)

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(SALIDA, index=False)
    print(f"OK: {len(df)} equipos -> {SALIDA.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
