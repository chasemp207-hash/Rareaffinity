"""Generate Rare Affinity graphics.

Writes print-ready SVGs to designs/print/. With --canvas DIR it also writes
the design-canvas artboards (garment mockups) into DIR/project/.

    python3 designs/build.py [--canvas DIR]
"""
import json
import pathlib
import sys
from datetime import datetime, timezone

# ---------------------------------------------------------------- palette
BONE = "#EFEAE0"
INK = "#141312"
OXBLOOD = "#7A1F1F"   # accent on light garments
EMBER = "#C8553D"     # accent on dark garments
STONE = "#5E584F"     # secondary text on bone (7:1 on BONE)
HEATHER = "#B9B2A6"   # heather-grey garment

ON_DARK = dict(fg=BONE, accent=EMBER, bg=INK)
ON_LIGHT = dict(fg=INK, accent=OXBLOOD, bg=BONE)

DISPLAY = "Syne, 'Arial Black', sans-serif"
SERIF = "'Instrument Serif', Georgia, serif"
MONO = "'IBM Plex Mono', 'Courier New', monospace"
FONTS_URL = ("https://fonts.googleapis.com/css2?family=Syne:wght@700;800"
             "&amp;family=Instrument+Serif:ital@0;1"
             "&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap")


# ---------------------------------------------------------------- graphics
# Each returns (viewBox, inner SVG markup). `uid` keeps ids unique when
# several graphics share one HTML page.

def wordmark(fg, accent, bg, uid="wm"):
    return "0 0 640 140", f"""
<text x="8" y="112" font-family="{DISPLAY}" font-weight="800" font-size="112" letter-spacing="-4" textLength="300" lengthAdjust="spacingAndGlyphs" fill="{fg}">RARE</text>
<text x="326" y="112" font-family="{SERIF}" font-style="italic" font-size="124" fill="{accent}">affinity</text>"""


def rare_form(fg, accent, bg, uid="rf"):
    """Back print: stacked RARE / affinity."""
    return "0 0 400 480", f"""
<text x="200" y="64" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="4" fill="{fg}">DROP 01 — RARE FORM</text>
<text x="200" y="210" text-anchor="middle" font-family="{DISPLAY}" font-weight="800" font-size="150" letter-spacing="-6" textLength="360" lengthAdjust="spacingAndGlyphs" fill="{fg}">RARE</text>
<text x="214" y="282" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="120" fill="{accent}">affinity</text>
<line x1="20" y1="330" x2="380" y2="330" stroke="{fg}" stroke-width="1.5"/>
<text x="20" y="356" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{fg}">NO. 001</text>
<text x="380" y="356" text-anchor="end" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{fg}">KEEP WHAT’S RARE</text>
<text x="200" y="450" text-anchor="middle" font-family="{MONO}" font-size="11" letter-spacing="5" fill="{fg}">LIMITED BY NATURE</text>"""


def one_in_eight(fg, accent, bg, uid="oe"):
    """Back print: a spec sheet for one person."""
    rows = [("SUBJECT", "YOU"), ("RARITY", "UNREPEATABLE"), ("AFFINITY", "BY CHOICE")]
    lines = []
    for i, (k, v) in enumerate(rows):
        y = 360 + i * 30
        lines.append(f'<line x1="20" y1="{y - 20}" x2="380" y2="{y - 20}" stroke="{fg}" stroke-width="1"/>')
        lines.append(f'<text x="20" y="{y}" font-family="{MONO}" font-size="13" letter-spacing="2" fill="{fg}">{k}</text>')
        lines.append(f'<text x="380" y="{y}" text-anchor="end" font-family="{MONO}" font-weight="500" font-size="13" letter-spacing="2" fill="{fg}">{v}</text>')
    lines.append(f'<line x1="20" y1="430" x2="380" y2="430" stroke="{fg}" stroke-width="1"/>')
    return "0 0 400 480", f"""
<text x="20" y="40" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{fg}">FILE 08 / RARE AFFINITY</text>
<text x="10" y="250" font-family="{DISPLAY}" font-weight="800" font-size="250" fill="{fg}">1</text>
<text x="176" y="250" font-family="{SERIF}" font-style="italic" font-size="110" fill="{accent}">in</text>
<text x="20" y="306" font-family="{DISPLAY}" font-weight="800" font-size="46" textLength="360" lengthAdjust="spacingAndGlyphs" fill="{fg}">8,000,000,000</text>
{chr(10).join(lines)}
<text x="200" y="464" text-anchor="middle" font-family="{MONO}" font-size="11" letter-spacing="5" fill="{fg}">THERE IS ONLY ONE</text>"""


def overlap(fg, accent, bg, uid="ov"):
    """Two circles; the overlap is where affinity lives."""
    return "0 0 400 400", f"""
<defs><clipPath id="{uid}-clip"><circle cx="155" cy="200" r="110"/></clipPath></defs>
<text x="200" y="52" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="5" fill="{fg}">WHERE WE OVERLAP</text>
<circle cx="245" cy="200" r="110" fill="{accent}" clip-path="url(#{uid}-clip)"/>
<circle cx="155" cy="200" r="110" fill="none" stroke="{fg}" stroke-width="3"/>
<circle cx="245" cy="200" r="110" fill="none" stroke="{fg}" stroke-width="3"/>
<text x="98" y="205" text-anchor="middle" font-family="{MONO}" font-weight="500" font-size="13" letter-spacing="3" fill="{fg}">RARE</text>
<text x="302" y="205" text-anchor="middle" font-family="{MONO}" font-weight="500" font-size="13" letter-spacing="3" fill="{fg}">AFFINITY</text>
<text x="200" y="216" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="44" fill="{bg}">us</text>
<text x="200" y="372" text-anchor="middle" font-family="{DISPLAY}" font-weight="800" font-size="30" textLength="250" lengthAdjust="spacingAndGlyphs" fill="{fg}">RARE AFFINITY</text>"""


def seal(fg, accent, bg, uid="sl"):
    """Round monogram: patches, embroidery, stickers."""
    return "0 0 300 300", f"""
<defs><path id="{uid}-ring" d="M 150 36 A 114 114 0 1 1 149.99 36"/></defs>
<circle cx="150" cy="150" r="142" fill="none" stroke="{fg}" stroke-width="3"/>
<circle cx="150" cy="150" r="98" fill="none" stroke="{fg}" stroke-width="1.5"/>
<text font-family="{MONO}" font-weight="500" font-size="15" fill="{fg}"><textPath href="#{uid}-ring" textLength="700" lengthAdjust="spacing">RARE AFFINITY • LIMITED BY NATURE • </textPath></text>
<text x="134" y="190" text-anchor="middle" font-family="{DISPLAY}" font-weight="800" font-size="118" fill="{fg}">R</text>
<text x="186" y="196" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="120" fill="{accent}">a</text>"""


GRAPHICS = {
    "wordmark": wordmark,
    "rare-form": rare_form,
    "one-in-eight-billion": one_in_eight,
    "overlap": overlap,
    "seal": seal,
}


def inline_svg(fn, colors, uid, width=None, height=None, extra=""):
    vb, body = fn(**colors, uid=uid)
    size = ""
    if width:
        size += f' width="{width}"'
    if height:
        size += f' height="{height}"'
    return f'<svg viewBox="{vb}"{size}{extra} xmlns="http://www.w3.org/2000/svg">{body}\n</svg>'


def write_print_files(out):
    out.mkdir(parents=True, exist_ok=True)
    for name, fn in GRAPHICS.items():
        for variant, colors in (("on-dark", ON_DARK), ("on-light", ON_LIGHT)):
            vb, body = fn(**colors, uid=name)
            svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">\n'
                   f'<style>@import url("{FONTS_URL}");</style>{body}\n</svg>\n')
            (out / f"{name}--{variant}.svg").write_text(svg)


# ---------------------------------------------------------------- canvas
TEE = ("M 214 34 C 248 70 352 70 386 34 L 500 76 L 580 206 L 494 250 "
       "L 462 204 L 462 612 Q 300 626 138 612 L 138 204 L 106 250 "
       "L 20 206 L 100 76 Z")
TEE_COLLAR = "M 214 34 C 248 70 352 70 386 34 C 360 84 240 84 214 34 Z"
CREW = ("M 214 34 C 248 70 352 70 386 34 L 496 72 Q 540 120 566 300 "
        "L 598 560 L 530 576 L 472 290 L 470 590 Q 470 612 450 612 "
        "L 150 612 Q 130 612 130 590 L 128 290 L 70 576 L 2 560 "
        "L 34 300 Q 60 120 104 72 Z")
CREW_RIBS = ("M 150 596 L 450 596 M 14 548 L 80 562 M 520 562 L 586 548")

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="{fonts}">
<style>
body{{margin:0;font-family:'IBM Plex Mono',monospace;background:{bg}}}
a{{color:{ox}}}a:hover{{color:{ink}}}
</style>
</helmet>
"""

TAIL = """
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
class Component extends DCLogic {{
renderVals() {{
return {{}};
}}
}}
</script>
</body>
</html>
"""


def page(title, w, h, body):
    return (HEAD.format(title=title, fonts=FONTS_URL.replace("&amp;", "&amp;"),
                        bg=BONE, ox=OXBLOOD, ink=INK)
            + body + TAIL.format(w=w, h=h))


def garment_board(title, number, shape, garment, colors, graphic, uid, meta):
    ribs = CREW_RIBS if shape == CREW else ""
    collar = TEE_COLLAR if shape == TEE else ""
    seam = "#00000033" if garment != INK else "#ffffff22"
    art = inline_svg(graphic, colors, uid, width=250, height=300 if graphic is not overlap else 250,
                     extra=' x="175" y="150"')
    specs = "".join(
        f'<div style="display: flex; justify-content: space-between; gap: 16px; padding: 10px 0; border-top: 1px solid #14131233; font-size: 13px; color: {INK}">'
        f'<span style="color: {STONE}">{k}</span><span>{v}</span></div>'
        for k, v in meta)
    body = f"""<div style="width: 640px; height: 820px; box-sizing: border-box; padding: 40px; background: {BONE}; display: flex; flex-direction: column; gap: 24px; color: {INK}">
<div style="display: flex; justify-content: space-between; align-items: baseline">
<div style="font-size: 12px; letter-spacing: 3px; color: {STONE}">{number}</div>
<div style="font-size: 12px; letter-spacing: 3px; color: {STONE}">BACK VIEW</div>
</div>
<div style="height: 460px; display: flex; align-items: center; justify-content: center; background: #E4DED2; border-radius: 4px">
<svg viewBox="0 0 600 640" width="420" height="448" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{title} mockup">
<path d="{shape}" fill="{garment}" stroke="{seam}" stroke-width="2" stroke-linejoin="round"/>
<path d="{collar}{ribs}" fill="{garment}" stroke="{seam}" stroke-width="2"/>
{art}
</svg>
</div>
<div style="display: flex; flex-direction: column; gap: 4px">
<h2 style="margin: 0; font-family: Syne, sans-serif; font-weight: 800; font-size: 34px; letter-spacing: -1px">{title}</h2>
</div>
<div style="display: flex; flex-direction: column">{specs}</div>
</div>"""
    return page(title, 640, 820, body)


def main_board():
    swatches = [("Bone", BONE, INK), ("Ink", INK, BONE), ("Oxblood", OXBLOOD, BONE),
                ("Ember", EMBER, INK), ("Heather", HEATHER, INK)]
    sw = "".join(
        f'<div style="display: flex; flex-direction: column; gap: 8px">'
        f'<div style="height: 96px; background: {c}; border: 1px solid #14131226; border-radius: 4px; display: flex; align-items: flex-end; padding: 10px; box-sizing: border-box; color: {t}; font-size: 12px">{c}</div>'
        f'<div style="font-size: 13px">{n}</div></div>'
        for n, c, t in swatches)
    body = f"""<div style="width: 1280px; height: 900px; box-sizing: border-box; padding: 64px; background: {BONE}; color: {INK}; display: flex; flex-direction: column; gap: 48px">
<div style="display: flex; justify-content: space-between; align-items: flex-end; gap: 40px">
{inline_svg(wordmark, ON_LIGHT, "m-wm", width=700, height=153)}
<div style="font-size: 13px; letter-spacing: 3px; line-height: 1.8; text-align: right; color: {STONE}">BRAND SHEET<br>DROP 01</div>
</div>
<div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 40px">
<div style="display: flex; flex-direction: column; gap: 16px">
<div style="font-size: 12px; letter-spacing: 3px; color: {STONE}">MONOGRAM SEAL</div>
<div style="height: 300px; background: {INK}; border-radius: 4px; display: flex; align-items: center; justify-content: center">{inline_svg(seal, ON_DARK, "m-sl", width=240, height=240)}</div>
</div>
<div style="display: flex; flex-direction: column; gap: 16px">
<div style="font-size: 12px; letter-spacing: 3px; color: {STONE}">SYMBOL</div>
<div style="height: 300px; background: #E4DED2; border-radius: 4px; display: flex; align-items: center; justify-content: center">{inline_svg(overlap, ON_LIGHT, "m-ov", width=270, height=270)}</div>
</div>
<div style="display: flex; flex-direction: column; gap: 16px">
<div style="font-size: 12px; letter-spacing: 3px; color: {STONE}">TYPE</div>
<div style="height: 300px; display: flex; flex-direction: column; justify-content: space-between; border-top: 1px solid {INK}; padding-top: 16px; box-sizing: border-box">
<div><div style="font-family: Syne, sans-serif; font-weight: 800; font-size: 48px; letter-spacing: -2px; line-height: 1">Syne 800</div><div style="font-size: 12px; color: {STONE}; margin-top: 6px">Headlines, the RARE in the wordmark</div></div>
<div><div style="font-family: 'Instrument Serif', serif; font-style: italic; font-size: 52px; line-height: 1; color: {OXBLOOD}">Instrument Serif</div><div style="font-size: 12px; color: {STONE}; margin-top: 6px">The feeling word, always italic, always accent</div></div>
<div><div style="font-size: 20px; font-weight: 500; letter-spacing: 3px">IBM PLEX MONO</div><div style="font-size: 12px; color: {STONE}; margin-top: 6px">Tags, specs, small caps with wide tracking</div></div>
</div>
</div>
</div>
<div style="display: flex; flex-direction: column; gap: 16px">
<div style="font-size: 12px; letter-spacing: 3px; color: {STONE}">PALETTE</div>
<div style="display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 24px">{sw}</div>
</div>
</div>"""
    return page("Rare Affinity brand sheet", 1280, 900, body)


def patch_board():
    body = f"""<div style="width: 640px; height: 700px; box-sizing: border-box; padding: 40px; background: {BONE}; color: {INK}; display: flex; flex-direction: column; gap: 24px">
<div style="font-size: 12px; letter-spacing: 3px; color: {STONE}">05 — EMBROIDERED PATCH</div>
<div style="display: flex; gap: 24px; align-items: center; justify-content: center; flex-grow: 1; background: #E4DED2; border-radius: 4px">
<div style="width: 250px; height: 250px; border-radius: 50%; background: {INK}; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 0 6px {EMBER}">{inline_svg(seal, ON_DARK, "p-sl1", width=220, height=220)}</div>
<div style="width: 250px; height: 250px; border-radius: 50%; background: {BONE}; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 0 6px {INK}">{inline_svg(seal, ON_LIGHT, "p-sl2", width=220, height=220)}</div>
</div>
<h2 style="margin: 0; font-family: Syne, sans-serif; font-weight: 800; font-size: 34px; letter-spacing: -1px">Seal Patch</h2>
<div style="font-size: 13px; line-height: 1.6; color: {STONE}">3" merrowed-edge patch in two colorways. Works for caps, totes and the left chest of the crewneck.</div>
</div>"""
    return page("Seal patch", 640, 700, body)


def labels_board():
    body = f"""<div style="width: 800px; height: 700px; box-sizing: border-box; padding: 40px; background: {BONE}; color: {INK}; display: flex; flex-direction: column; gap: 24px">
<div style="font-size: 12px; letter-spacing: 3px; color: {STONE}">06 — HANG TAG &amp; NECK LABEL</div>
<div style="display: flex; gap: 40px; align-items: center; justify-content: center; flex-grow: 1; background: #E4DED2; border-radius: 4px">
<div style="width: 220px; height: 380px; background: {INK}; color: {BONE}; border-radius: 6px; box-sizing: border-box; padding: 28px 22px; display: flex; flex-direction: column; justify-content: space-between; align-items: center">
<div style="width: 16px; height: 16px; border-radius: 50%; background: #E4DED2"></div>
{inline_svg(wordmark, ON_DARK, "l-wm", width=176, height=39)}
<div style="font-size: 10px; letter-spacing: 2px; line-height: 1.9; text-align: center; opacity: 0.85">NO. ____ / ____<br>LIMITED BY NATURE</div>
</div>
<div style="display: flex; flex-direction: column; gap: 16px; align-items: center">
<div style="width: 260px; height: 84px; background: {OXBLOOD}; display: flex; align-items: center; justify-content: space-between; padding: 0 20px; box-sizing: border-box; border-radius: 2px">
{inline_svg(wordmark, dict(fg=BONE, accent=BONE, bg=OXBLOOD), "l-wm2", width=150, height=33)}
<div style="font-size: 14px; font-weight: 500; color: {BONE}; border: 1px solid {BONE}; padding: 4px 8px">[SIZE]</div>
</div>
<div style="font-size: 11px; letter-spacing: 2px; color: {STONE}">WOVEN NECK LABEL</div>
</div>
</div>
<div style="font-size: 13px; line-height: 1.6; color: {STONE}">Hand-number each piece on the tag. The blank lines are the point: every piece is one of a count.</div>
</div>"""
    return page("Hang tag and neck label", 800, 700, body)


def write_canvas(root):
    proj = root / "project"
    proj.mkdir(parents=True, exist_ok=True)
    boards = {
        "Main.dc.html": (main_board(), dict(x=0, y=0, w=1280, h=900, title="Brand sheet")),
        "Tee-Rare-Form.dc.html": (garment_board(
            "Rare Form Tee", "01 — HEAVYWEIGHT TEE", TEE, INK, ON_DARK, rare_form, "g1",
            [("Garment", "Black, 240 gsm cotton"), ("Print", "Back, screen print, 2 colors"),
             ("Front", "Small seal, left chest"), ("Price", "[YOUR PRICE]")]),
            dict(x=0, y=1260, w=640, h=820)),
        "Tee-One-In-Eight.dc.html": (garment_board(
            "One in Eight Billion", "02 — HEAVYWEIGHT TEE", TEE, BONE, ON_LIGHT, one_in_eight, "g2",
            [("Garment", "Bone, 240 gsm cotton"), ("Print", "Back, screen print, 2 colors"),
             ("Front", "Wordmark, left chest"), ("Price", "[YOUR PRICE]")]),
            dict(x=720, y=1260, w=640, h=820)),
        "Crew-Overlap.dc.html": (garment_board(
            "Overlap Crewneck", "03 — FLEECE CREWNECK", CREW, HEATHER, ON_LIGHT, overlap, "g3",
            [("Garment", "Heather grey, 400 gsm fleece"), ("Print", "Back, puff print, 2 colors"),
             ("Front", "Seal patch, left chest"), ("Price", "[YOUR PRICE]")]),
            dict(x=1440, y=1260, w=640, h=820)),
        "Seal-Patch.dc.html": (patch_board(), dict(x=0, y=2420, w=640, h=700)),
        "Labels.dc.html": (labels_board(), dict(x=720, y=2420, w=800, h=700)),
    }
    index = {
        "v": 3,
        "createdOnFiles": {"v": 1, "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")},
        "title": "Rare Affinity Collection",
        "launch": {"view": "canvas"},
        "pages": [],
        "boards": {k: v[1] for k, v in boards.items()},
        "order": list(boards),
        "notes": {
            "drop": {"x": 0, "y": 1000, "text": "Drop 01 — Garments", "kind": "title1", "maxW": 2080},
            "details": {"x": 0, "y": 2160, "text": "Details", "kind": "title1", "maxW": 1520},
        },
        "designSystems": [],
    }
    (proj / "canvas.json").write_text(json.dumps(index, indent=1))
    for name, (html, _) in boards.items():
        (proj / name).write_text(html)


if __name__ == "__main__":
    here = pathlib.Path(__file__).resolve().parent
    write_print_files(here / "print")
    if "--canvas" in sys.argv:
        write_canvas(pathlib.Path(sys.argv[sys.argv.index("--canvas") + 1]))
