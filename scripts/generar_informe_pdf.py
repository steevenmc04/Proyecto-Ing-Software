"""Genera el informe final PDF a partir del Markdown de entrega."""

from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
)

RAIZ = Path(__file__).resolve().parents[1]
ORIGEN = RAIZ / "docs" / "entrega" / "TFINAL_Grupo01_MartinezSteeven.md"
DESTINO = RAIZ / "docs" / "entrega" / "TFINAL_Grupo01_MartinezSteeven.pdf"

AZUL = colors.HexColor("#123C52")
VERDE = colors.HexColor("#1E6B52")
GRIS = colors.HexColor("#52636D")


def limpiar_inline(texto: str) -> str:
    texto = re.sub(r"!\[[^\]]*]\([^)]+\)", "", texto)
    texto = re.sub(r"\[([^\]]+)]\(([^)]+)\)", r"\1 (\2)", texto)
    texto = texto.replace("**", "").replace("`", "")
    return texto


def encabezado_pie(canvas, documento) -> None:
    canvas.saveState()
    ancho, alto = A4
    canvas.setFillColor(AZUL)
    canvas.rect(0, alto - 1.1 * cm, ancho, 1.1 * cm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(1.6 * cm, alto - 0.7 * cm, "Sistema de Gestion de Caja de Ahorros")
    canvas.setFillColor(GRIS)
    canvas.drawRightString(
        ancho - 1.6 * cm,
        0.8 * cm,
        f"Grupo 01 - Pagina {documento.page}",
    )
    canvas.restoreState()


def imagen_ajustada(ruta: Path) -> Image:
    ancho, alto = ImageReader(str(ruta)).getSize()
    max_ancho = 16.5 * cm
    max_alto = 18 * cm
    escala = min(max_ancho / ancho, max_alto / alto)
    return Image(str(ruta), width=ancho * escala, height=alto * escala)


def construir_historia(texto: str) -> list:
    estilos = getSampleStyleSheet()
    estilos.add(
        ParagraphStyle(
            "Seccion",
            parent=estilos["Heading1"],
            textColor=AZUL,
            fontSize=17,
            leading=21,
            spaceBefore=14,
            spaceAfter=8,
        )
    )
    estilos.add(
        ParagraphStyle(
            "Subseccion",
            parent=estilos["Heading2"],
            textColor=VERDE,
            fontSize=13,
            leading=16,
            spaceBefore=10,
            spaceAfter=6,
        )
    )
    estilos.add(
        ParagraphStyle(
            "Cuerpo",
            parent=estilos["BodyText"],
            fontSize=9.5,
            leading=14,
            textColor=colors.HexColor("#1C2730"),
            spaceAfter=7,
        )
    )
    estilos.add(
        ParagraphStyle(
            "Lista",
            parent=estilos["BodyText"],
            fontSize=9.2,
            leading=13,
            leftIndent=14,
            firstLineIndent=-8,
            bulletIndent=4,
            spaceAfter=3,
        )
    )
    estilos.add(
        ParagraphStyle(
            "Codigo",
            parent=estilos["Code"],
            fontName="Courier",
            fontSize=7.5,
            leading=10,
            leftIndent=8,
            rightIndent=8,
            borderColor=colors.HexColor("#CBD5DC"),
            borderWidth=0.5,
            borderPadding=8,
            backColor=colors.HexColor("#F3F6F8"),
            spaceAfter=8,
        )
    )

    historia = []
    parrafo: list[str] = []
    codigo: list[str] = []
    en_codigo = False
    inicio_contenido = False

    def vaciar_parrafo() -> None:
        if parrafo:
            historia.append(
                Paragraph(limpiar_inline(" ".join(parrafo)), estilos["Cuerpo"])
            )
            parrafo.clear()

    for linea in texto.splitlines():
        if linea.startswith("## "):
            inicio_contenido = True
        if not inicio_contenido:
            continue
        if linea.startswith("# "):
            continue
        if linea.startswith("```"):
            vaciar_parrafo()
            if en_codigo:
                historia.append(
                    Preformatted("\n".join(codigo), estilos["Codigo"])
                )
                codigo.clear()
            en_codigo = not en_codigo
            continue
        if en_codigo:
            codigo.append(linea)
            continue
        if not linea.strip():
            vaciar_parrafo()
            continue
        if linea.startswith("## "):
            vaciar_parrafo()
            historia.append(Paragraph(limpiar_inline(linea[3:]), estilos["Seccion"]))
            continue
        if linea.startswith("### "):
            vaciar_parrafo()
            historia.append(
                Paragraph(limpiar_inline(linea[4:]), estilos["Subseccion"])
            )
            continue
        coincidencia_imagen = re.match(r"!\[([^]]+)]\(([^)]+)\)", linea)
        if coincidencia_imagen:
            vaciar_parrafo()
            ruta = (ORIGEN.parent / coincidencia_imagen.group(2)).resolve()
            historia.extend(
                [
                    Spacer(1, 4),
                    imagen_ajustada(ruta),
                    Paragraph(
                        coincidencia_imagen.group(1),
                        ParagraphStyle(
                            "PieImagen",
                            parent=estilos["Cuerpo"],
                            alignment=TA_CENTER,
                            textColor=GRIS,
                            fontSize=8,
                        ),
                    ),
                ]
            )
            continue
        if linea.startswith("- "):
            vaciar_parrafo()
            historia.append(
                Paragraph(
                    f"- {limpiar_inline(linea[2:])}",
                    estilos["Lista"],
                )
            )
            continue
        parrafo.append(linea.strip())

    vaciar_parrafo()
    return historia


def generar() -> None:
    texto = ORIGEN.read_text(encoding="utf-8")
    documento = SimpleDocTemplate(
        str(DESTINO),
        pagesize=A4,
        rightMargin=1.7 * cm,
        leftMargin=1.7 * cm,
        topMargin=1.7 * cm,
        bottomMargin=1.5 * cm,
        title="Proyecto Final - Sistema de Gestion de Caja de Ahorros",
        author="Steeven Ariel Martinez Campos",
    )

    portada_titulo = ParagraphStyle(
        "PortadaTitulo",
        fontName="Helvetica-Bold",
        fontSize=25,
        leading=31,
        textColor=AZUL,
        alignment=TA_CENTER,
        spaceAfter=16,
    )
    portada_subtitulo = ParagraphStyle(
        "PortadaSubtitulo",
        fontName="Helvetica",
        fontSize=13,
        leading=19,
        textColor=GRIS,
        alignment=TA_CENTER,
    )
    portada_autor = ParagraphStyle(
        "PortadaAutor",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=18,
        textColor=colors.HexColor("#1C2730"),
        alignment=TA_CENTER,
    )

    historia = [
        Spacer(1, 2.7 * cm),
        Paragraph("INGENIERIA DE SOFTWARE", portada_subtitulo),
        Spacer(1, 1.3 * cm),
        Paragraph("PROYECTO FINAL", portada_titulo),
        Paragraph("Sistema de Gestion de Caja de Ahorros", portada_titulo),
        Spacer(1, 2.1 * cm),
        Paragraph("Grupo 01", portada_autor),
        Paragraph("Steeven Ariel Martinez Campos", portada_autor),
        Spacer(1, 1.3 * cm),
        Paragraph("26 de julio de 2026", portada_subtitulo),
        Spacer(1, 2.0 * cm),
        Paragraph(
            "https://github.com/steevenmc04/Proyecto-Ing-Software",
            portada_subtitulo,
        ),
        PageBreak(),
    ]
    historia.extend(construir_historia(texto))

    documento.build(
        historia,
        onFirstPage=encabezado_pie,
        onLaterPages=encabezado_pie,
    )
    print(f"Informe generado: {DESTINO}")


if __name__ == "__main__":
    generar()
