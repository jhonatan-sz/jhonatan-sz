#!/usr/bin/env python3
"""Genera profile.svg: la cabecera del README de perfil.

La idea es que el perfil se vea como la respuesta de una API, no como una
tarjeta decorativa: un `curl` y el JSON que devuelve. Sin dependencias y sin
servicios de terceros que se caigan: el SVG se genera y se commitea.

Uso:
    python3 generate_profile_svg.py

Editar DATOS y volver a correrlo es todo lo que hace falta para actualizar la
cabecera.
"""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

# --- datos que se muestran --------------------------------------------------
DATOS: dict[str, object] = {
    "nombre": "Jhonatan Sánchez",
    "rol": "Backend Developer",
    "formacion": "Ingeniería de Sistemas · 6º semestre",
    "ubicacion": "Colombia",
    "stack": [
        "TypeScript",
        "NestJS",
        "Prisma",
        "Python",
        "FastAPI",
        "PostgreSQL",
        "Redis",
        "Docker",
        "React",
        "Next.js",
    ],
    "enfoque": ["APIs REST", "automatización", "scraping"],
    "disponible_para": ["freelance", "prácticas"],
    "contacto": "jhonatan2000j@gmail.com",
}

URL = "https://api.github.com/jhonatan-sz"
PROMPT = f"jhonatan@dev:~ $ curl -s {URL}"
TITULO = "jhonatan-sz · perfil.json"

# --- estilo -----------------------------------------------------------------
FONDO = "#0D1117"      # fondo de la ventana
BORDE = "#30363D"      # borde y semáforo de la barra
BARRA = "#161B22"      # barra de título
ACENTO = "#F59E0B"     # ámbar: el único color de acento
TEXTO = "#E6EDF3"      # valores
APAGADO = "#8B949E"    # puntuación, prompt, título

FUENTE = (
    "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, "
    "'Liberation Mono', monospace"
)

MARGEN = 28
TAM_FUENTE = 14
ALTO_LINEA = 23
BARRA_ALTO = 40
ANCHO_MINIMO = 560
# Monospace a 14 px: el avance real de cada carácter ronda 0.62 em.
PX_POR_CARACTER = TAM_FUENTE * 0.62
# Longitud de línea a la que se reparten los arrays.
ANCHO_TEXTO = 72


def repartir(items: list[str], ancho_max: int) -> list[list[str]]:
    """Reparte los items en líneas de longitud parecida.

    Evita el clásico final con un solo elemento colgando: calcula cuántas
    líneas hacen falta y reparte el ancho entre ellas.
    """
    total = sum(len(item) for item in items) + 2 * (len(items) - 1)
    lineas_necesarias = max(1, -(-(total + 4) // ancho_max))
    objetivo = -(-(total + 4) // lineas_necesarias) + 2

    lineas: list[list[str]] = []
    actual: list[str] = []
    largo = 0
    for item in items:
        if actual and largo + len(item) + 2 > objetivo:
            lineas.append(actual)
            actual = [item]
            largo = len(item)
        else:
            actual.append(item)
            largo += len(item) + 2
    if actual:
        lineas.append(actual)
    return lineas


def formatear(datos: dict[str, object], ancho_max: int = ANCHO_TEXTO) -> list[str]:
    """JSON legible pero compacto: los arrays cortos van en una línea."""
    lineas = ["{"]
    claves = list(datos)
    for indice, clave in enumerate(claves):
        valor = datos[clave]
        coma = "," if indice < len(claves) - 1 else ""
        prefijo = f'  "{clave}": '
        if isinstance(valor, list):
            items = [f'"{item}"' for item in valor]
            en_una_linea = prefijo + "[" + ", ".join(items) + "]" + coma
            if len(en_una_linea) <= ancho_max:
                lineas.append(en_una_linea)
                continue
            lineas.append(prefijo + "[")
            grupos = repartir(items, ancho_max)
            for pos, grupo in enumerate(grupos):
                final = "," if pos < len(grupos) - 1 else ""
                lineas.append("    " + ", ".join(grupo) + final)
            lineas.append("  ]" + coma)
        else:
            lineas.append(prefijo + f'"{valor}"' + coma)
    lineas.append("}")
    return lineas


def tramos_coloreados(linea: str) -> list[tuple[str, str]]:
    """Divide una línea de JSON en (texto, color).

    Una cadena seguida de ':' es una clave y va en acento; el resto de cadenas
    son valores y van en color de texto; todo lo demás (llaves, comas,
    indentación) va apagado.
    """
    tramos: list[tuple[str, str]] = []
    i = 0
    while i < len(linea):
        if linea[i] == '"':
            fin = linea.index('"', i + 1)
            cadena = linea[i : fin + 1]
            es_clave = linea[fin + 1 :].lstrip().startswith(":")
            tramos.append((cadena, ACENTO if es_clave else TEXTO))
            i = fin + 1
        else:
            j = i
            while j < len(linea) and linea[j] != '"':
                j += 1
            tramos.append((linea[i:j], APAGADO))
            i = j
    return tramos


def bloque_texto(lineas: list[str], y_inicial: int) -> list[str]:
    """Una línea por <text> con sus <tspan>, respetando el espacio."""
    salida: list[str] = []
    y = y_inicial
    for linea in lineas:
        tspans = "".join(
            f'<tspan fill="{color}">{escape(texto)}</tspan>'
            for texto, color in tramos_coloreados(linea)
            if texto
        )
        salida.append(
            f'<text x="{MARGEN}" y="{y}" xml:space="preserve">{tspans}</text>'
        )
        y += ALTO_LINEA
    return salida


def generar(destino: Path) -> None:
    cuerpo = formatear(DATOS)
    # El ancho se ajusta al contenido: ni un píxel de más.
    caracteres = max([len(PROMPT)] + [len(linea) for linea in cuerpo])
    ancho = max(ANCHO_MINIMO, round(caracteres * PX_POR_CARACTER) + 2 * MARGEN + 8)

    y_prompt = BARRA_ALTO + MARGEN + TAM_FUENTE
    alto = y_prompt + ALTO_LINEA * (len(cuerpo) + 1) + MARGEN - TAM_FUENTE

    partes: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{ancho}" '
        f'height="{alto}" viewBox="0 0 {ancho} {alto}" role="img" '
        f'font-family="{FUENTE}" font-size="{TAM_FUENTE}" '
        f'aria-label="Perfil de Jhonatan Sánchez">',
        "<title>Jhonatan Sánchez — perfil de backend</title>",
        f'<rect x="0" y="0" width="{ancho}" height="{alto}" rx="12" '
        f'fill="{FONDO}" stroke="{BORDE}"/>',
        f'<path d="M0 12a12 12 0 0 1 12-12h{ancho - 24}a12 12 0 0 1 12 12v'
        f'{BARRA_ALTO - 12}H0z" fill="{BARRA}"/>',
        f'<line x1="0" y1="{BARRA_ALTO}" x2="{ancho}" y2="{BARRA_ALTO}" '
        f'stroke="{BORDE}"/>',
        f'<circle cx="24" cy="20" r="6" fill="{BORDE}"/>',
        f'<circle cx="44" cy="20" r="6" fill="{BORDE}"/>',
        f'<circle cx="64" cy="20" r="6" fill="{BORDE}"/>',
        f'<text x="{ancho // 2}" y="24" text-anchor="middle" '
        f'font-size="12" fill="{APAGADO}">{escape(TITULO)}</text>',
        f'<text x="{MARGEN}" y="{y_prompt}" xml:space="preserve">'
        f'<tspan fill="{APAGADO}">jhonatan@dev</tspan>'
        f'<tspan fill="{APAGADO}">:</tspan>'
        f'<tspan fill="{APAGADO}">~</tspan>'
        f'<tspan fill="{ACENTO}"> $ </tspan>'
        f'<tspan fill="{TEXTO}">curl -s {URL}</tspan>'
        "</text>",
    ]
    partes.extend(bloque_texto(cuerpo, y_prompt + ALTO_LINEA))
    partes.append("</svg>")

    destino.write_text("\n".join(partes) + "\n", encoding="utf-8")


if __name__ == "__main__":
    salida = Path(__file__).with_name("profile.svg")
    generar(salida)
    print(f"escrito: {salida} ({salida.stat().st_size} bytes)")
