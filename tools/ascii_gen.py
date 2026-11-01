#!/usr/bin/env python3
"""Convierte una imagen (o un texto) en arte ASCII calibrado para el README.

El arte vive dentro de un bloque monoespaciado junto a las specs de sistema,
así que la salida siempre mide exactamente `--cols` columnas por `--lines`
filas: las líneas cortas se rellenan con espacios a la derecha y el bloque se
centra verticalmente.

La corrección de aspecto compensa que una celda de carácter es más alta que
ancha. Sin ella, un círculo se ve como un óvalo alargado.

Uso:
    uv run --with pillow python tools/ascii_gen.py --text "JS"
    uv run --with pillow python tools/ascii_gen.py --image logo.png --invert
    uv run --with pillow python tools/ascii_gen.py --text "JS" --out tools/ascii_js.txt

Requiere Pillow (solo se usa para rasterizar; el arte final es texto plano).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Ordenados por densidad: el índice crece con la tinta del carácter.
RAMP = " .:-=+*#%@"

# Una celda monoespaciada es ~1.8-2.0 veces más alta que ancha. 0.55 deja el
# arte un poco más esbelto que 0.5 y compensa el line-height de GitHub.
ASPECTO_VERTICAL = 0.55

FUENTES = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
)


def cargar_fuente(tamano: int) -> ImageFont.FreeTypeFont:
    for ruta in FUENTES:
        if Path(ruta).is_file():
            return ImageFont.truetype(ruta, tamano)
    return ImageFont.load_default(size=tamano)


def _texto_rasterizado(texto: str, tamano: int) -> Image.Image:
    fuente = cargar_fuente(tamano)
    lineas = texto.splitlines() or [texto]
    ancho = tamano * max(1, max(len(linea) for linea in lineas))
    alto = tamano * (len(lineas) + 1)
    lienzo = Image.new("L", (ancho, alto), 255)
    dibujo = ImageDraw.Draw(lienzo)
    dibujo.multiline_text(
        (tamano // 4, tamano // 4),
        texto,
        font=fuente,
        fill=0,
        spacing=tamano // 8,
        align="center",
    )

    caja = lienzo.getbbox()
    if caja is None:
        raise ValueError("El texto no produjo píxeles")
    return lienzo.crop(caja)


def imagen_desde_texto(texto: str, tamano: int = 240, marco: bool = False) -> Image.Image:
    """Rasteriza el texto en negro sobre blanco, recortado a su tinta.

    Acepta saltos de línea (``"J\\nS"``) para monogramas apilados. Con
    ``marco`` añade un borde redondeado: da al monograma una silueta casi
    cuadrada que aprovecha las 14 filas del bloque fastfetch.
    """
    texto_img = _texto_rasterizado(texto, tamano)
    if not marco:
        return texto_img

    margen = tamano // 6
    grosor = max(2, tamano // 26)
    ancho = texto_img.width + 2 * margen
    alto = texto_img.height + 2 * margen
    lienzo = Image.new("L", (ancho, alto), 255)
    lienzo.paste(texto_img, (margen, margen))
    dibujo = ImageDraw.Draw(lienzo)
    radio = tamano // 5
    dibujo.rounded_rectangle(
        (grosor // 2, grosor // 2, ancho - grosor // 2 - 1, alto - grosor // 2 - 1),
        radius=radio,
        outline=0,
        width=grosor,
    )
    return lienzo


def imagen_desde_archivo(ruta: Path, invertir: bool) -> Image.Image:
    imagen = Image.open(ruta).convert("L")
    if invertir:
        # Trazo claro sobre fondo oscuro → trazo oscuro sobre fondo claro.
        imagen = Image.eval(imagen, lambda p: 255 - p)
    return imagen


def a_ascii(imagen: Image.Image, cols: int, lineas: int, aspecto: float) -> list[str]:
    ancho, alto = imagen.size
    if ancho == 0 or alto == 0:
        raise ValueError("La imagen no tiene dimensiones")

    # Filas necesarias para conservar la proporción tras la corrección.
    filas = max(1, round(cols * (alto / ancho) * aspecto))
    if filas > lineas:
        # Demasiado alta: se reduce el ancho efectivo para que quepa.
        filas = lineas
        cols = max(1, round(filas * (ancho / alto) / aspecto))

    reducida = imagen.resize((cols, filas), Image.Resampling.LANCZOS)
    pixeles = reducida.load()

    salida: list[str] = []
    for y in range(filas):
        fila = []
        for x in range(cols):
            luminancia = pixeles[x, y]
            # 0 (negro) → último carácter de la rampa; 255 (blanco) → espacio.
            indice = round((255 - luminancia) / 255 * (len(RAMP) - 1))
            fila.append(RAMP[indice])
        salida.append("".join(fila))
    return salida


def encuadrar(lineas_arte: list[str], cols: int, lineas: int) -> list[str]:
    """Centra el arte y garantiza un bloque rectangular de cols × lineas."""
    arriba = (lineas - len(lineas_arte)) // 2
    abajo = lineas - len(lineas_arte) - arriba
    vacia = " " * cols
    cuerpo = [linea.center(cols)[:cols] for linea in lineas_arte]
    return [vacia] * arriba + cuerpo + [vacia] * abajo


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Imagen/texto → ASCII calibrado")
    fuente = parser.add_mutually_exclusive_group()
    fuente.add_argument("--text", default="JS", help="Texto a rasterizar (default: JS)")
    fuente.add_argument("--image", type=Path, help="Imagen de entrada (PNG/JPG)")
    parser.add_argument("--cols", type=int, default=28, help="Ancho en columnas (default: 28)")
    parser.add_argument("--lines", type=int, default=14, help="Alto en líneas (default: 14)")
    parser.add_argument("--aspect", type=float, default=ASPECTO_VERTICAL, help="Corrección vertical (default: 0.55)")
    parser.add_argument("--font-size", type=int, default=240, help="Tamaño de rasterizado del texto")
    parser.add_argument("--frame", action="store_true", help="Borde redondeado alrededor del texto")
    parser.add_argument("--invert", action="store_true", help="Invertir imágenes con trazo claro sobre fondo oscuro")
    parser.add_argument("--specs", type=Path, help="Archivo de specs para componer la columna derecha")
    parser.add_argument("--gap", type=int, default=4, help="Espacios entre arte y specs (default: 4)")
    parser.add_argument("--out", type=Path, help="Guardar el bloque en un archivo (sin padding final)")
    args = parser.parse_args(argv)

    if args.cols < 1 or args.lines < 1:
        parser.error("--cols y --lines deben ser >= 1")

    if args.image:
        if not args.image.is_file():
            parser.error(f"No existe la imagen: {args.image}")
        imagen = imagen_desde_archivo(args.image, args.invert)
    else:
        imagen = imagen_desde_texto(args.text, args.font_size, args.frame)

    arte = a_ascii(imagen, args.cols, args.lines, args.aspect)
    bloque = encuadrar(arte, args.cols, args.lines)

    if args.specs:
        if not args.specs.is_file():
            parser.error(f"No existe el archivo de specs: {args.specs}")
        specs = args.specs.read_text(encoding="utf-8").splitlines()
        filas = max(len(bloque), len(specs))
        bloque += [" " * args.cols] * (filas - len(bloque))
        specs += [""] * (filas - len(specs))
        separador = " " * args.gap
        bloque = [
            (arte_linea + separador + spec_linea).rstrip()
            for arte_linea, spec_linea in zip(bloque, specs)
        ]
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text("\n".join(bloque) + "\n", encoding="utf-8")
            print(f"escrito: {args.out} ({filas} filas)", file=sys.stderr)
        else:
            print("\n".join(bloque))
        return 0

    texto = "\n".join(bloque)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        # Sin espacios finales: el archivo se puede versionar sin ruido.
        args.out.write_text("\n".join(linea.rstrip() for linea in bloque) + "\n", encoding="utf-8")
        print(f"escrito: {args.out} ({args.cols}x{args.lines})", file=sys.stderr)
    else:
        print(texto)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
