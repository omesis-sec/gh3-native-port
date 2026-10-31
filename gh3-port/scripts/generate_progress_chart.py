"""Generate the three README progress charts from one milestone estimate."""

from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / "docs" / "images"
ESTIMATE = 15

COPY = {
    "en": {
        "title": "ROAD TO PLAYABLE", "subtitle": "GUITAR HERO III  /  PS2 → WINDOWS",
        "estimate": "ENGINEERING ESTIMATE", "range": "uncertainty range 10–20%",
        "caption": "toward one complete, playable song", "scale": "FIRST PLAYABLE BUILD",
        "stages": [
            ("01", "DISC + BUILD", "verified game revision", "DONE"),
            ("02", "NATIVE BOOT", "loads game resources", "PARTIAL"),
            ("03", "VISIBLE MENU", "first rendered frame", "NEXT"),
            ("04", "RHYTHM LOOP", "input + synced audio", "OPEN"),
            ("05", "FULL SONG", "results + return", "OPEN"),
        ],
        "evidence": "OBSERVED EVIDENCE", "a": "9,822", "al": "translated entries",
        "b": "50k", "bl": "IOP memory cycles", "c": "55 s", "cl": "active Debug run · black screen",
        "note": "Estimate is subjective; milestones require repeatable tests, not translated-code counts.",
    },
    "pt-BR": {
        "title": "CAMINHO ATÉ JOGÁVEL", "subtitle": "GUITAR HERO III  /  PS2 → WINDOWS",
        "estimate": "ESTIMATIVA TÉCNICA", "range": "faixa de incerteza 10–20%",
        "caption": "até uma música completa e jogável", "scale": "PRIMEIRA BUILD JOGÁVEL",
        "stages": [
            ("01", "DISCO + BUILD", "edição verificada", "FEITO"),
            ("02", "BOOT NATIVO", "carrega recursos", "PARCIAL"),
            ("03", "MENU VISÍVEL", "primeiro quadro", "PRÓXIMO"),
            ("04", "RITMO", "entrada + áudio", "PENDENTE"),
            ("05", "MÚSICA INTEIRA", "resultado + retorno", "PENDENTE"),
        ],
        "evidence": "EVIDÊNCIAS OBSERVADAS", "a": "9.822", "al": "entradas traduzidas",
        "b": "50 mil", "bl": "ciclos de memória IOP", "c": "55 s", "cl": "Debug ativo · tela preta",
        "note": "Estimativa subjetiva; os marcos exigem testes reproduzíveis, não contagem de código.",
    },
    "es": {
        "title": "CAMINO A JUGABLE", "subtitle": "GUITAR HERO III  /  PS2 → WINDOWS",
        "estimate": "ESTIMACIÓN TÉCNICA", "range": "margen de incertidumbre 10–20%",
        "caption": "hasta una canción completa y jugable", "scale": "PRIMERA VERSIÓN JUGABLE",
        "stages": [
            ("01", "DISCO + BUILD", "edición verificada", "HECHO"),
            ("02", "INICIO NATIVO", "carga recursos", "PARCIAL"),
            ("03", "MENÚ VISIBLE", "primer fotograma", "SIGUIENTE"),
            ("04", "RITMO", "controles + audio", "PENDIENTE"),
            ("05", "CANCIÓN ENTERA", "resultado + regreso", "PENDIENTE"),
        ],
        "evidence": "DATOS OBSERVADOS", "a": "9822", "al": "entradas traducidas",
        "b": "50 mil", "bl": "ciclos de memoria IOP", "c": "55 s", "cl": "Debug activo · pantalla negra",
        "note": "Estimación subjetiva; los hitos exigen pruebas repetibles, no recuentos de código.",
    },
}


def label(x, y, value, size=16, fill="#eef5ff", weight=500, extra=""):
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" '
            f'font-weight="{weight}" {extra}>{escape(value)}</text>')


def render(copy):
    stages = []
    colors = ["#43dfb2", "#ffbf69", "#79afff", "#697a92", "#697a92"]
    for i, (number, title, detail, state) in enumerate(copy["stages"]):
        x = 55 + i * 224
        color = colors[i]
        stages.extend([
            f'<rect x="{x}" y="315" width="204" height="155" rx="15" fill="#142338" stroke="{color}" stroke-opacity=".65"/>',
            f'<circle cx="{x+26}" cy="342" r="15" fill="{color}" fill-opacity=".15"/>',
            label(x+16, 347, number, 13, color, 800),
            label(x+18, 388, title, 17, "#f2f7ff", 800),
            label(x+18, 415, detail, 14, "#a9bdd5"),
            f'<rect x="{x+18}" y="435" width="{max(64,len(state)*8+20)}" height="22" rx="11" fill="{color}" fill-opacity=".16"/>',
            label(x+29, 451, state, 11, color, 800),
        ])
        if i < 4:
            stages.append(f'<path d="M{x+205} 392 H{x+223}" stroke="{color}" stroke-width="2" marker-end="url(#arrow)"/>')
    cards = []
    for i, (value, desc) in enumerate(((copy["a"], copy["al"]), (copy["b"], copy["bl"]), (copy["c"], copy["cl"]))):
        x = 55 + i * 375
        cards.extend([
            f'<rect x="{x}" y="530" width="350" height="92" rx="14" fill="#101f34" stroke="#2b4564"/>',
            label(x+18, 568, value, 29, "#d8f9f0", 800),
            label(x+18, 597, desc, 14, "#a9bdd5"),
        ])
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="690" viewBox="0 0 1200 690" role="img">',
        f'<title>{escape(copy["title"])} — {ESTIMATE}%</title>',
        f'<desc>{escape(copy["note"])}</desc>',
        '<defs><pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#29405b" stroke-opacity=".22"/></pattern><linearGradient id="track"><stop stop-color="#43dfb2"/><stop offset="1" stop-color="#76bbf5"/></linearGradient><marker id="arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#6d91b3"/></marker></defs>',
        '<rect width="1200" height="690" rx="20" fill="#0b1728"/><rect width="1200" height="690" rx="20" fill="url(#grid)"/>',
        '<g font-family="Arial, Helvetica, sans-serif">',
        '<rect x="55" y="43" width="7" height="54" rx="3" fill="#43dfb2"/>',
        label(77, 69, copy["title"], 27, "#f0f7ff", 800),
        label(77, 91, copy["subtitle"], 13, "#88a6c5", 700, 'letter-spacing="2"'),
        label(55, 142, copy["estimate"], 13, "#96aec8", 700, 'letter-spacing="2"'),
        label(55, 187, f"{ESTIMATE}%", 54, "#43dfb2", 800),
        label(175, 174, copy["caption"], 18, "#e6effa", 600),
        label(175, 197, copy["range"], 14, "#a9bdd5"),
        '<rect x="55" y="224" width="1090" height="24" rx="12" fill="#25374d"/>',
        f'<rect x="55" y="224" width="{1090*ESTIMATE//100}" height="24" rx="12" fill="url(#track)"/>',
        f'<circle cx="{55+1090*ESTIMATE//100}" cy="236" r="10" fill="#e4fff6" stroke="#43dfb2" stroke-width="3"/>',
        label(55, 281, "0%", 13, "#95acc6"),
        label(1076, 281, "100%", 13, "#95acc6"),
        label(879, 281, copy["scale"], 13, "#a9bdd5", 700),
        *stages,
        label(55, 507, copy["evidence"], 13, "#91abc9", 700, 'letter-spacing="2"'),
        *cards,
        label(55, 659, copy["note"], 14, "#93a9c1"),
        '</g></svg>',
    ]
    return "\n".join(parts) + "\n"


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for language, copy in COPY.items():
        destination = OUT / f"road-to-playable.{language}.svg"
        destination.write_text(render(copy), encoding="utf-8")
        print(destination)
