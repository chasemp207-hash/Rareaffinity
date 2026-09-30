"""Rare Affinity collection: sweater, fitted tee, boxy tee, boxy zip hoodie.

Writes print-ready SVGs to designs/print/. With --canvas DIR it also writes
the design-canvas artboards (garment mockups) into DIR/project/.

    python3 designs/collection.py [--canvas DIR]
"""
import json
import pathlib
import sys
from datetime import datetime, timezone

import build
from build import (BONE as WHITE, INK as BLACK, OXBLOOD as WINE, EMBER as WINE_BRIGHT,
                   STONE, DISPLAY, SERIF, MONO, ON_DARK, ON_LIGHT, page, inline_svg)

BLACK_CLOTH = "#1A1A1A"   # black garment, lifted so folds and shading read
STAGE = "#E7E4DE"


# ================================================================ graphics
def monogram(fg, accent, bg, uid="mo"):
    """Small embroidered Ra: fitted tee chest mark."""
    return "0 0 60 40", f"""
<text x="4" y="32" font-family="{DISPLAY}" font-weight="800" font-size="34" fill="{accent}">R</text>
<text x="29" y="33" font-family="{SERIF}" font-style="italic" font-size="36" fill="{accent}">a</text>"""


def symbol(fg, accent, bg, uid="sy"):
    """Two overlapping rings: sweater chest embroidery."""
    return "0 0 60 40", f"""
<defs><clipPath id="{uid}-c"><circle cx="24" cy="20" r="14"/></clipPath></defs>
<circle cx="36" cy="20" r="14" fill="{accent}" clip-path="url(#{uid}-c)"/>
<circle cx="24" cy="20" r="14" fill="none" stroke="{accent}" stroke-width="2.6"/>
<circle cx="36" cy="20" r="14" fill="none" stroke="{accent}" stroke-width="2.6"/>"""


def stitch(d, color, w=5):
    """A chain-stitch embroidered line."""
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="#ffffff" stroke-opacity=".35" stroke-width="{w * .3:.1f}" stroke-dasharray="2 4" stroke-linecap="round"/>')


ESCAPE_BOX = "M 310 170 L 240 170 L 240 270 L 340 270 L 340 192"
ESCAPE_OUT = ("M 292 232 C 276 230 272 208 290 206 C 310 204 308 230 290 228 "
              "C 316 214 330 196 338 176 C 350 140 380 110 404 88 C 420 72 430 62 440 50")
ESCAPE_BACK = ("M 160 50 C 156 110 108 170 170 230 C 232 290 384 222 372 320 "
               "C 362 400 228 362 248 440 C 260 484 322 486 340 468")


def escape_front(fg, accent, bg, uid="ef"):
    """Boxy tee front: a line breaks out of the box toward the shoulder."""
    return "0 0 600 640", stitch(ESCAPE_BOX, accent) + stitch(ESCAPE_OUT, accent)


def escape_back(fg, accent, bg, uid="eb"):
    """Boxy tee back: the line comes over the shoulder and signs off."""
    return "0 0 600 640", stitch(ESCAPE_BACK, accent) + f"""
<text x="300" y="516" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="30" fill="{accent}">outside the box.</text>
<text x="300" y="540" text-anchor="middle" font-family="{MONO}" font-weight="500" font-size="10" letter-spacing="4" fill="{accent}">RARE AFFINITY</text>"""


def chalk_filter(uid, seed):
    return f"""<filter id="{uid}-chalk{seed}" x="-5%" y="-5%" width="110%" height="110%">
<feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="3" seed="{seed}" result="n"/>
<feDisplacementMap in="SourceGraphic" in2="n" scale="4" xChannelSelector="R" yChannelSelector="G" result="d"/>
<feTurbulence type="fractalNoise" baseFrequency="1.3" numOctaves="2" seed="{seed + 7}" result="g"/>
<feColorMatrix in="g" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3.4 0 0 0 -.62" result="gm"/>
<feComposite in="d" in2="gm" operator="in"/>
</filter>"""


def falling_man(fg, accent, bg, uid="fm"):
    """Hoodie back: a man falling, painted in chalk, reaching for a wine heart."""
    segments = [  # (path, width): a solid figure built from tapered strokes
        ("M 138 150 L 98 98", 27), ("M 98 98 L 120 42", 19), ("M 120 42 L 104 30", 13),    # bent leg
        ("M 154 144 L 176 84", 27), ("M 176 84 L 168 24", 19), ("M 168 24 L 150 16", 13),  # straight leg
        ("M 186 250 L 230 230", 16), ("M 230 230 L 258 196", 13),                          # arm up
        ("M 158 264 L 128 300", 16), ("M 128 300 L 106 334", 13),                          # arm reaching
        ("M 176 266 L 182 286", 13),                                                       # neck
    ]
    solid = "".join(f'<path d="{d}" stroke-width="{w}"/>' for d, w in segments)
    sketch = "".join(f'<path d="{d}" stroke-width="2" stroke-opacity=".55" transform="translate({dx} {dy})"/>'
                     for (d, _), (dx, dy) in zip(segments, [(15, -6), (12, 6), (0, 0), (-15, 4), (-11, -2), (0, 0),
                                                            (3, -10), (9, -8), (-9, -6), (-9, -6), (0, 0)]) if dx or dy)
    speed = "".join(
        f'<path d="M {x} {y} L {x + 3} {y + h}" stroke-width="{w}" stroke-opacity=".7"/>'
        for x, y, h, w in ((70, 0, 60, 3), (112, 8, 22, 2), (206, 18, 80, 3), (236, 70, 64, 2.5),
                           (58, 110, 40, 2), (272, 130, 30, 2), (144, 206, 30, 2)))
    heart = ("M 78 400 C 48 380 46 356 64 352 C 74 350 78 360 78 364 "
             "C 78 360 82 350 92 352 C 110 356 108 380 78 400 Z")
    return "0 0 300 420", f"""
<defs>
{chalk_filter(uid, 3)}
{chalk_filter(uid, 5)}
</defs>
<g filter="url(#{uid}-chalk3)" fill="none" stroke="{fg}" stroke-linecap="round" stroke-linejoin="round">
{speed}
{solid}
<path d="M 126 158 L 158 140 L 194 248 L 154 272 Z" fill="{fg}" stroke-width="16"/>
<path d="M 124 162 Q 100 132 88 116 Q 118 124 142 146 Z M 160 144 Q 172 116 186 102 Q 182 132 168 154 Z" fill="{fg}" stroke-width="3"/>
<circle cx="190" cy="306" r="21" fill="{fg}" stroke="none"/>
<path d="M 172 318 Q 180 334 196 330 M 206 316 Q 214 330 208 340" stroke-width="3"/>
<circle cx="262" cy="190" r="8" fill="{fg}" stroke="none"/>
<circle cx="102" cy="340" r="8" fill="{fg}" stroke="none"/>
{sketch}
<path d="M 118 170 L 170 280 M 148 146 L 204 256" stroke-width="2" stroke-opacity=".45" transform="translate(-6 4)"/>
<text x="220" y="414" text-anchor="middle" font-family="{MONO}" font-weight="500" font-size="11" letter-spacing="4" fill="{fg}" stroke="none">RARE AFFINITY</text>
</g>
<g filter="url(#{uid}-chalk5)" fill="none" stroke="{accent}" stroke-linecap="round" stroke-linejoin="round">
<path d="{heart}" stroke-width="5"/>
<path d="{heart}" stroke-width="2.5" transform="translate(3 -2.5)" stroke-opacity=".75"/>
</g>"""


NEW_GRAPHICS = {
    "monogram-ra": monogram,
    "symbol-rings": symbol,
    "escape-line-front": escape_front,
    "escape-line-back": escape_back,
    "falling-man-chalk": falling_man,
}


# ================================================================ garments
def shading(uid, dark):
    hi = ".07" if dark else ".12"
    return f"""<linearGradient id="{uid}-sh" x1="0" x2="1" y1="0" y2="0">
<stop offset="0" stop-color="#000" stop-opacity=".2"/>
<stop offset=".2" stop-color="#000" stop-opacity="0"/>
<stop offset=".5" stop-color="#fff" stop-opacity="{hi}"/>
<stop offset=".8" stop-color="#000" stop-opacity="0"/>
<stop offset="1" stop-color="#000" stop-opacity=".2"/>
</linearGradient>
<linearGradient id="{uid}-vs" x1="0" x2="0" y1="0" y2="1">
<stop offset="0" stop-color="#fff" stop-opacity="{hi}"/>
<stop offset=".4" stop-color="#000" stop-opacity="0"/>
<stop offset="1" stop-color="#000" stop-opacity=".16"/>
</linearGradient>
<pattern id="{uid}-rib" width="6" height="10" patternUnits="userSpaceOnUse">
<path d="M 3 0 L 3 10" stroke="#000" stroke-opacity=".2" stroke-width="2"/>
</pattern>"""


def part(d, uid, fill, seam, texture=None, extra=""):
    """A garment panel: base color, optional texture, shading, seam line."""
    out = f'<path d="{d}" fill="{fill}"{extra}/>'
    if texture:
        out += f'<path d="{d}" fill="url(#{uid}-{texture})"/>'
    out += f'<path d="{d}" fill="url(#{uid}-sh)"/><path d="{d}" fill="url(#{uid}-vs)"/>'
    out += f'<path d="{d}" fill="none" stroke="{seam}" stroke-width="1.6" stroke-linejoin="round"/>'
    return out


def line(d, color, opacity, width=1.4, dash=None):
    dash = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-opacity="{opacity}" '
            f'stroke-width="{width}" stroke-linecap="round"{dash}/>')


def mirror(d):
    """Mirror an absolute path around x=300 (numbers come in x y pairs)."""
    out, xy = [], 0
    for tok in d.split():
        try:
            v = float(tok)
        except ValueError:
            out.append(tok)
            continue
        out.append(f"{600 - v:g}" if xy % 2 == 0 else tok)
        xy += 1
    return " ".join(out)


def garment_colors(body):
    dark = body in (BLACK, BLACK_CLOTH)
    return dark, ("#ffffff" if dark else "#000000"), (".22" if dark else ".28")


def sweater(uid, body, thread, zoom=None):
    dark, ink, op = garment_colors(body)
    seam = f"{ink}"
    knit = f"""<pattern id="{uid}-knit" width="10" height="12" patternUnits="userSpaceOnUse">
<path d="M 1 0 Q 3 8 5 11 M 9 0 Q 7 8 5 11" fill="none" stroke="#000" stroke-opacity=".12" stroke-width="1.8"/>
<path d="M 2 0 Q 3.6 6 5 9" fill="none" stroke="#fff" stroke-opacity=".12" stroke-width="1"/>
</pattern>
<pattern id="{uid}-cable" width="40" height="56" patternUnits="userSpaceOnUse">
<rect width="40" height="56" fill="{body}"/>
<path d="M 30 -2 C 30 14 10 14 10 28 C 10 42 30 42 30 58" fill="none" stroke="#000" stroke-opacity=".3" stroke-width="13"/>
<path d="M 30 -2 C 30 14 10 14 10 28 C 10 42 30 42 30 58" fill="none" stroke="{body}" stroke-width="9"/>
<path d="M 10 -2 C 10 14 30 14 30 28 C 30 42 10 42 10 58" fill="none" stroke="#000" stroke-opacity=".32" stroke-width="13"/>
<path d="M 10 -2 C 10 14 30 14 30 28 C 30 42 10 42 10 58" fill="none" stroke="{body}" stroke-width="9"/>
<path d="M 10 -2 C 10 14 30 14 30 28 C 30 42 10 42 10 58" fill="none" stroke="#fff" stroke-opacity=".16" stroke-width="2.5"/>
</pattern>"""
    sleeve = "M 132 72 Q 86 84 70 150 L 24 520 L 92 530 L 132 262 Z"
    cuff = "M 24 520 L 92 530 L 88 586 L 20 578 Z"
    torso = "M 220 42 C 254 76 346 76 380 42 L 468 72 L 468 560 L 132 560 L 132 72 Z"
    hem = "M 132 556 L 468 556 L 468 610 Q 300 616 132 610 Z"
    collar = "M 210 40 C 246 98 354 98 390 40 L 380 42 C 346 78 254 78 220 42 Z"
    inside = "M 220 42 C 254 70 346 70 380 42 C 340 28 260 28 220 42 Z"
    s = f'<defs>{shading(uid, dark)}{knit}</defs>'
    s += part(sleeve, uid, body, seam + "30", "knit") + part(mirror(sleeve), uid, body, seam + "30", "knit")
    s += part(torso, uid, body, seam + "30", "knit")
    for x in (240, 320):
        s += f'<rect x="{x}" y="96" width="40" height="460" fill="url(#{uid}-cable)"/>'
        s += line(f"M {x - 4} 100 L {x - 4} 556", "#000", ".22", 3)
        s += line(f"M {x + 44} 100 L {x + 44} 556", "#000", ".22", 3)
    s += f'<path d="{torso}" fill="url(#{uid}-sh)"/>'
    for d in (cuff, mirror(cuff), hem):
        s += part(d, uid, body, seam + "30", "rib")
    s += f'<path d="{inside}" fill="{body}"/><path d="{inside}" fill="#000" fill-opacity=".38"/>'
    s += part(collar, uid, body, seam + "30", "rib")
    s += inline_svg(symbol, dict(fg=thread, accent=thread, bg=body), f"{uid}-sy",
                    width=30, height=20, extra=' x="394" y="150"')
    vb = zoom or "0 0 600 640"
    return f'<svg viewBox="{vb}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Sweater">{s}</svg>'


def fitted_tee(uid, body, accent, zoom=None):
    dark, ink, op = garment_colors(body)
    torso = ("M 228 40 C 258 72 342 72 372 40 L 452 64 L 522 168 L 464 204 L 440 180 "
             "Q 420 330 438 600 Q 300 612 162 600 Q 180 330 160 180 L 136 204 L 78 168 L 148 64 Z")
    collar = "M 220 40 C 250 92 350 92 380 40 L 372 40 C 342 74 258 74 228 40 Z"
    inside = "M 228 40 C 258 70 342 70 372 40 C 340 30 260 30 228 40 Z"
    s = f'<defs>{shading(uid, dark)}</defs>'
    s += part(torso, uid, body, ink + "30")
    s += f'<path d="{inside}" fill="{body}"/><path d="{inside}" fill="#000" fill-opacity=".4"/>'
    s += part(collar, uid, body, ink + "30", "rib")
    for d in ("M 148 64 Q 172 120 160 180", "M 88 158 L 144 192", "M 164 588 Q 300 600 436 588"):
        s += line(d, ink, op, 1.3, "4 3") if d.startswith("M 88") or d.startswith("M 164") else line(d, ink, op, 1.4)
        if not d.startswith("M 164"):
            m = mirror(d)
            s += line(m, ink, op, 1.3, "4 3") if d.startswith("M 88") else line(m, ink, op, 1.4)
    for d in ("M 186 420 Q 200 450 192 490", "M 412 400 Q 398 440 408 480", "M 260 560 Q 280 574 300 578"):
        s += line(d, ink, ".08", 6)
    s += f'<rect x="161" y="556" width="7" height="22" rx="1" fill="{accent}"/>'
    s += inline_svg(monogram, dict(fg=accent, accent=accent, bg=body), f"{uid}-mo",
                    width=33, height=22, extra=' x="372" y="140"')
    vb = zoom or "0 0 600 640"
    return f'<svg viewBox="{vb}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Fitted tee">{s}</svg>'


def boxy_tee(uid, body, accent, back=False):
    dark, ink, op = garment_colors(body)
    neck = "C 256 58 344 58 378 44" if back else "C 256 78 344 78 378 44"
    torso = (f"M 222 44 {neck} L 498 72 L 584 250 L 506 290 L 486 296 L 486 574 "
             "L 114 574 L 114 296 L 94 290 L 16 250 L 102 72 Z")
    s = f'<defs>{shading(uid, dark)}</defs>'
    s += part(torso, uid, body, ink + "30")
    if back:
        s += part("M 212 42 C 248 70 352 70 388 42 L 378 44 C 344 58 256 58 222 44 Z", uid, body, ink + "30", "rib")
    else:
        inside = "M 222 44 C 256 76 344 76 378 44 C 340 30 260 30 222 44 Z"
        s += f'<path d="{inside}" fill="{body}"/><path d="{inside}" fill="#000" fill-opacity=".4"/>'
        s += part("M 208 42 C 246 106 354 106 392 42 L 378 44 C 344 80 256 80 222 44 Z", uid, body, ink + "30", "rib")
    for d in ("M 128 66 Q 124 180 114 296", "M 28 240 L 100 278"):
        dash = "4 3" if d.startswith("M 28") else None
        s += line(d, ink, op, 1.4, dash) + line(mirror(d), ink, op, 1.4, dash)
    s += line("M 116 560 L 484 560", ink, op, 1.3, "4 3")
    for d in ("M 170 380 Q 184 430 176 500", "M 430 360 Q 418 420 426 490"):
        s += line(d, ink, ".07", 8)
    art = escape_back if back else escape_front
    vb, body_svg = art(fg=accent, accent=accent, bg=body, uid=uid)
    s += body_svg
    return (f'<svg viewBox="0 0 600 640" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-label="Boxy tee {"back" if back else "front"}">{s}</svg>')


def zip_hoodie(uid, body, accent, back=False):
    dark, ink, op = garment_colors(body)
    outline = ("M 196 88 L 112 110 Q 72 136 62 216 L 26 524 L 102 538 L 134 300 L 134 604 "
               "L 466 604 L 466 300 L 498 538 L 574 524 L 538 216 Q 528 136 488 110 L 404 88 Z")
    cuff = "M 26 524 L 102 538 L 98 594 L 22 582 Z"
    hem = "M 134 600 L 466 600 L 466 658 L 134 658 Z"
    s = f'<defs>{shading(uid, dark)}</defs>'
    if not back:
        s += part("M 190 96 C 176 0 424 0 410 96 Z", uid, body, ink + "30", extra=' fill-opacity="1"')
        s += '<path d="M 190 96 C 176 0 424 0 410 96 Z" fill="#000" fill-opacity=".35"/>'
    s += part(outline, uid, body, ink + "30")
    for d in (cuff, mirror(cuff), hem):
        s += part(d, uid, body, ink + "30", "rib")
    s += line("M 152 104 Q 142 200 134 300", ink, op, 1.4) + line(mirror("M 152 104 Q 142 200 134 300"), ink, op, 1.4)
    for d in ("M 110 300 Q 104 360 92 420", "M 120 200 Q 100 260 96 300", "M 200 300 Q 214 360 206 420"):
        s += line(d, ink, ".06", 8) + line(mirror(d), ink, ".06", 8)
    if back:
        hood = "M 206 92 C 196 -6 404 -6 394 92 Q 380 150 300 170 Q 220 150 206 92 Z"
        s += part(hood, uid, body, ink + "30")
        s += line("M 300 8 L 300 170", ink, op, 1.4)
        s += line("M 222 120 Q 300 150 378 120", ink, ".08", 10)
        vb, art = falling_man(fg=WHITE, accent=WINE_BRIGHT, bg=body, uid=uid)
        s += f'<svg viewBox="{vb}" x="156" y="200" width="288" height="384">{art}</svg>'
    else:
        s += '<path d="M 226 92 C 222 36 378 36 374 92 L 300 172 Z" fill="#0a0a0a"/>'
        left = "M 190 96 C 176 40 226 34 226 92 L 300 172 C 250 164 200 134 190 96 Z"
        s += part(left, uid, body, ink + "30") + part(mirror(left), uid, body, ink + "30")
        for x in (276, 324):
            dx = -8 if x < 300 else 8
            s += f'<path d="M {x} 150 Q {x + dx / 2} 210 {x + dx} 262" fill="none" stroke="{accent}" stroke-width="5" stroke-linecap="round"/>'
            s += f'<rect x="{x + dx - 3}" y="258" width="6" height="16" rx="2" fill="#c9c6c0"/>'
        s += line("M 300 172 L 300 656", "#2e2e2e", "1", 8)
        s += line("M 300 172 L 300 656", "#6a6a6a", "1", 5, "1.5 2.5")
        s += f'<rect x="294" y="180" width="12" height="28" rx="3" fill="{accent}"/><circle cx="300" cy="202" r="2.5" fill="{body}"/>'
        pocket = "M 150 574 L 150 470 Q 168 428 208 410 L 292 410"
        s += line(pocket, ink, op, 1.5) + line(mirror(pocket), ink, op, 1.5)
        s += line("M 154 470 Q 172 432 210 416", ink, op, 1.2, "4 3") + line(mirror("M 154 470 Q 172 432 210 416"), ink, op, 1.2, "4 3")
    return (f'<svg viewBox="0 -10 600 680" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-label="Boxy zip hoodie {"back" if back else "front"}">{s}</svg>')


# ================================================================ boards
def garment_view(svg, label, w=460, h=490):
    return (f'<div style="display: flex; flex-direction: column; align-items: center; gap: 12px">'
            f'<div style="width: {w}px; height: {h}px; display: flex">{svg}</div>'
            f'<div style="font-size: 11px; letter-spacing: 3px; color: {STONE}">{label}</div></div>')


def zoom_view(svg, label):
    return (f'<div style="display: flex; flex-direction: column; align-items: center; gap: 12px">'
            f'<div style="width: 190px; height: 190px; border-radius: 50%; overflow: hidden; '
            f'box-shadow: 0 0 0 1px #14141433, 0 12px 30px #1414142e; display: flex">{svg}</div>'
            f'<div style="font-size: 11px; letter-spacing: 3px; color: {STONE}">{label}</div></div>')


def board(title, number, pitch, stage, specs):
    rows = "".join(
        f'<div style="display: flex; flex-direction: column; gap: 6px; padding-top: 12px; border-top: 1px solid {BLACK}">'
        f'<div style="font-size: 11px; letter-spacing: 3px; color: {STONE}">{k.upper()}</div>'
        f'<div style="font-size: 14px; line-height: 1.5; color: {BLACK}">{v}</div></div>'
        for k, v in specs)
    body = f"""<div style="width: 1180px; height: 940px; box-sizing: border-box; padding: 48px; background: {WHITE}; color: {BLACK}; display: flex; flex-direction: column; gap: 28px">
<div style="display: flex; justify-content: space-between; align-items: flex-end; gap: 40px">
<div style="display: flex; flex-direction: column; gap: 10px">
<div style="font-size: 12px; letter-spacing: 3px; color: {WINE}">{number}</div>
<h2 style="margin: 0; font-family: Syne, sans-serif; font-weight: 800; font-size: 44px; letter-spacing: -1.5px; line-height: 1">{title}</h2>
</div>
<div style="max-width: 440px; font-family: 'Instrument Serif', serif; font-style: italic; font-size: 22px; line-height: 1.3; text-align: right">{pitch}</div>
</div>
<div style="height: 590px; background: {STAGE}; border-radius: 4px; display: flex; align-items: center; justify-content: space-evenly; padding: 20px; box-sizing: border-box">
{stage}
</div>
<div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 24px">{rows}</div>
</div>"""
    return page(title, 1180, 940, body)


def sweater_board():
    stage = (garment_view(sweater("sw1", WHITE, WINE), "IVORY / WINE THREAD", 420, 450)
             + garment_view(sweater("sw2", WINE, WHITE), "WINE / IVORY THREAD", 420, 450)
             + zoom_view(sweater("sw3", WHITE, WINE, zoom="372 120 76 76"), "DETAIL"))
    return board("The Knit", "01 — CABLE KNIT SWEATER",
                 "Quiet on purpose. Twin cables, and one small mark where your heart is.",
                 stage,
                 [("Material", "Heavy gauge merino-cotton, knit texture"),
                  ("Detail", "Twin cable panels, ribbed collar, cuffs and hem"),
                  ("Design", "Two-ring symbol, tonal embroidery, left chest, 1 in"),
                  ("Colorways", "Ivory with wine thread · Wine with ivory thread")])


def fitted_board():
    stage = (garment_view(fitted_tee("ft1", BLACK_CLOTH, WINE_BRIGHT), "BLACK / WINE THREAD", 420, 450)
             + garment_view(fitted_tee("ft2", WHITE, WINE), "WHITE / WINE THREAD", 420, 450)
             + zoom_view(fitted_tee("ft3", BLACK_CLOTH, WINE_BRIGHT, zoom="360 122 60 60"), "DETAIL"))
    return board("The Fitted", "02 — FITTED TEE",
                 "Cut close to the body. The only logo is the one you have to lean in to see.",
                 stage,
                 [("Material", "Compact cotton jersey, slim fit"),
                  ("Detail", "Narrow ribbed collar, cover-stitched hems"),
                  ("Design", "Ra monogram embroidered in wine, left chest; wine flag label at hem"),
                  ("Colorways", "Black · White")])


def boxy_board():
    stage = (garment_view(boxy_tee("bx1", WHITE, WINE), "FRONT", 500, 530)
             + garment_view(boxy_tee("bx2", WHITE, WINE, back=True), "BACK", 500, 530))
    return board("Escape Line", "03 — BOXY TEE",
                 "One line breaks out of the box, climbs over the shoulder and finishes on the back.",
                 stage,
                 [("Material", "Heavyweight cotton, boxy cut, dropped shoulder"),
                  ("Detail", "Thick ribbed collar, cropped body"),
                  ("Design", "Continuous wine chain-stitch line, front to back across the shoulder seam"),
                  ("Why it spreads", "The design is only complete when you turn around. Every photo needs two angles.")])


def hoodie_board():
    stage = (garment_view(zip_hoodie("hd1", BLACK_CLOTH, WINE_BRIGHT), "FRONT", 480, 540)
             + garment_view(zip_hoodie("hd2", BLACK_CLOTH, WINE_BRIGHT, back=True), "BACK", 480, 540))
    return board("Falling", "04 — BOXY ZIP HOODIE",
                 "A man falls, drawn in chalk, reaching for one wine heart.",
                 stage,
                 [("Material", "Heavyweight fleece, boxy cut, dropped shoulder"),
                  ("Detail", "Full zip with wine pull, wine drawcords, split kangaroo pocket"),
                  ("Design", "Chalk-textured back print, white with wine heart"),
                  ("Print", "DTG or high-density screen print from a 300 dpi raster to keep the chalk grain")])


# ================================================================ output
def write_print_files(out):
    build.GRAPHICS.update(NEW_GRAPHICS)
    build.write_print_files(out)


def write_canvas(root):
    proj = root / "project"
    build.write_canvas(root)  # early concepts + brand sheet
    index = json.loads((proj / "canvas.json").read_text())
    for name, entry in index["boards"].items():
        if name != "Main.dc.html":
            entry["page"] = "concepts"
            entry["y"] -= 1260 if entry["y"] >= 2420 else 1260
            entry["y"] += 260
    index["notes"] = {
        "collection": {"x": 0, "y": 1000, "text": "The Collection", "kind": "title1", "maxW": 2440, "page": "collection"},
        "drop": {"x": 0, "y": 0, "text": "Early concepts", "kind": "title1", "maxW": 2080, "page": "concepts"},
    }
    new = {
        "Knit-Sweater.dc.html": (sweater_board(), dict(x=0, y=1240, title="01 The Knit")),
        "Fitted-Tee.dc.html": (fitted_board(), dict(x=1260, y=1240, title="02 The Fitted")),
        "Boxy-Tee.dc.html": (boxy_board(), dict(x=0, y=2300, title="03 Escape Line")),
        "Zip-Hoodie.dc.html": (hoodie_board(), dict(x=1260, y=2300, title="04 Falling")),
    }
    for name, (html, entry) in new.items():
        (proj / name).write_text(html)
        index["boards"][name] = dict(entry, w=1180, h=940, page="collection")
    index["boards"]["Main.dc.html"]["page"] = "collection"
    index["pages"] = [{"id": "collection", "name": "Collection"}, {"id": "concepts", "name": "Early concepts"}]
    index["launch"] = {"view": "canvas", "page": "collection"}
    index["order"] = ["Main.dc.html", *new, *[n for n in index["order"] if n != "Main.dc.html"]]
    (proj / "canvas.json").write_text(json.dumps(index, indent=1))


def main():
    here = pathlib.Path(__file__).resolve().parent
    write_print_files(here / "print")
    if "--canvas" in sys.argv:
        write_canvas(pathlib.Path(sys.argv[sys.argv.index("--canvas") + 1]))


if __name__ == "__main__":
    main()
