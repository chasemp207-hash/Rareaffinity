"""Refined symbols: three takes each on the swan, the diamond clover and the swallow.

Writes designs/refined/*.svg; with --canvas DIR also writes canvas artboards
to DIR/project/ and adds a "Refined" page to its canvas.json.

    python3 designs/refined.py [--canvas DIR]
"""
import json
import math
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from symbols import BLACK, IVORY, WINE, tapered, s07_swallows  # noqa: E402


def swallow_path():
    """The swallow outline from symbols.py, reused at any position."""
    body = s07_swallows()[1]
    return body.split('d="')[1].split('"')[0]


BIRD = swallow_path()


def bird(x, y, rot, scale, fill, flip=False):
    fx = " scale(-1 1)" if flip else ""
    return (f'<path d="{BIRD}" fill="{fill}" transform="translate({x} {y}) rotate({rot}){fx} '
            f'scale({scale}) translate(-300 -330)"/>')


def kite(rot, cx, cy, fill="none", stroke=None, sw=0, length=104, width=96, gap=7, facets=False):
    """A cut-gem leaf: its point at the centre, its flat table facing out along `rot`."""
    h, w = length, width / 2
    g, t = -gap, -gap - h
    d = f"M 0 {g} L {-w} {g - h * .6} L {-w * .55} {t} L {w * .55} {t} L {w} {g - h * .6} Z"
    st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else ""
    out = f'<path d="{d}" fill="{fill}"{st}/>'
    if facets:
        gy = g - h * .6
        out += (f'<path d="M {-w} {gy} L {w} {gy} M {-w * .55} {t} L {-w * .3} {gy} L 0 {t} L {w * .3} {gy} L {w * .55} {t} '
                f'M {-w * .3} {gy} L 0 {g} L {w * .3} {gy}" '
                f'fill="none" stroke="{stroke}" stroke-width="{sw * .6:.1f}" stroke-linejoin="round"/>')
    return f'<g transform="translate({cx} {cy}) rotate({rot})">{out}</g>'


# ================================================================ swan
def swan_line():
    """The swan in one continuous stroke, drawn like a figure 2."""
    d = ("M 150 296 C 166 380 270 412 360 380 C 420 358 432 310 396 280 "
         "C 350 242 330 184 368 160 C 398 142 432 158 438 192")
    return IVORY, (f'<g transform="translate(6 30)">'
                   f'<path d="{d}" fill="none" stroke="{BLACK}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>'
                   f'<path d="M 438 192 L 470 214" fill="none" stroke="{WINE}" stroke-width="14" stroke-linecap="round"/></g>')


def swan_origami():
    """A swan folded from paper: all straight edges, no crystal, no feathers."""
    tri = lambda pts, fill: f'<path d="M {pts} Z" fill="{fill}"/>'
    return IVORY, ('<g transform="translate(-14 20)">'
                   + tri("130 262 L 236 362 L 184 384", BLACK)            # tail
                   + tri("184 384 L 236 362 L 430 368 L 300 420", BLACK)  # body
                   + tri("236 362 L 430 368 L 330 300", "#2B2B2B")       # wing fold
                   + tri("372 368 L 412 368 L 388 168", BLACK)            # neck
                   + tri("388 168 L 398 214 L 428 196", BLACK)            # head
                   + tri("412 190 L 452 214 L 420 208", WINE)             # beak
                   + '</g>')


def swan_necks():
    """Only the two necks, kissing: a heart with no bodies, nothing extra."""
    neck = tapered([((282, 400), (196, 360), (166, 260), (206, 196)),
                    ((206, 196), (236, 150), (292, 158), (292, 198))], 30, 10)
    head = '<ellipse cx="288" cy="202" rx="13" ry="10" transform="rotate(70 288 202)"/>'
    beak = f'<path d="M 290 210 L 298 236 L 284 214 Z" fill="{WINE}"/>'
    one = f'<path d="{neck}"/>{head}'
    return BLACK, (f'<g transform="translate(0 10)"><g fill="{IVORY}">{one}</g>'
                   f'<g fill="{IVORY}" transform="translate(600 0) scale(-1 1)">{one}</g>{beak}'
                   f'<g transform="translate(600 0) scale(-1 1)">{beak}</g></g>')


# ================================================================ clover
def clover_solid():
    """Four diamonds for leaves; the fourth, rarest one is wine."""
    leaves = "".join(kite(r, 300, 270, WINE if r == 45 else BLACK) for r in (45, 135, 225, 315))
    stem = f'<path d="M 300 272 C 302 340 316 398 350 452" fill="none" stroke="{BLACK}" stroke-width="5" stroke-linecap="round"/>'
    return IVORY, stem + leaves


def clover_faceted():
    """Each leaf a cut stone, drawn in hairline like a jeweller's sketch."""
    leaves = "".join(kite(r, 300, 270, WINE if r == 45 else "none", BLACK, 2.6, facets=True)
                     for r in (45, 135, 225, 315))
    stem = f'<path d="M 300 276 C 302 340 316 398 350 452" fill="none" stroke="{BLACK}" stroke-width="2.6" stroke-linecap="round"/>'
    return IVORY, stem + leaves


def clover_badge():
    """The diamond clover knocked out of a wine disc: a patch, a button, a stamp."""
    leaves = "".join(kite(r, 300, 286, IVORY, length=88, width=82, gap=5) for r in (45, 135, 225, 315))
    stem = f'<path d="M 300 288 C 302 336 312 372 336 404" fill="none" stroke="{IVORY}" stroke-width="4.5" stroke-linecap="round"/>'
    return BLACK, f'<circle cx="300" cy="300" r="170" fill="{WINE}"/>' + stem + leaves


# ================================================================ swallow
def swallow_single():
    """One swallow, alone and in flight."""
    return IVORY, bird(300, 310, 38, .9, BLACK)


def swallow_pair():
    """Two swallows turning toward each other; their wings frame a heart."""
    return IVORY, bird(206, 310, 62, .58, BLACK) + bird(394, 310, -62, .58, WINE, flip=True)


def swallow_badge():
    """The swallow cut out of a black disc, with the wine one escaping past the edge."""
    return IVORY, (f'<circle cx="300" cy="300" r="170" fill="{BLACK}"/>'
                   + bird(292, 316, 38, .72, IVORY) + bird(452, 150, 38, .3, WINE))


MARKS = [
    ("Swan", "Line", "The whole swan in one rounded stroke, like a logo you could draw in the air. Wine dot for the beak.", swan_line),
    ("Swan", "Origami", "A swan folded from paper: straight edges only, one shaded fold, a wine beak. Graphic and young, nothing like a crystal swan.", swan_origami),
    ("Swan", "Necks", "Only the two necks remain, kissing into a heart. Ivory on black, wine beaks.", swan_necks),
    ("Clover", "Diamond Leaves", "Four diamonds make the four-leaf clover; the rarest leaf is wine.", clover_solid),
    ("Clover", "Cut Stones", "Each leaf a faceted stone in hairline, like a jeweller's sketch.", clover_faceted),
    ("Clover", "Badge", "The diamond clover knocked out of a wine disc, for patches, buttons and packaging.", clover_badge),
    ("Swallow", "Solo", "One swallow in flight. The cleanest, smallest-size-friendly mark.", swallow_single),
    ("Swallow", "Pair", "A black and a wine swallow turning toward each other. Two that always find their way back.", swallow_pair),
    ("Swallow", "Badge", "A swallow cut from a black disc, with the wine one flying out past the edge.", swallow_badge),
]


def svg(i, standalone=False):
    bg, body = MARKS[i][3]()
    back = f'<rect width="600" height="600" fill="{bg}"/>' if standalone else ""
    size = "" if standalone else ' width="600" height="600"'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600"{size}>{back}{body}</svg>', bg


def slug(i):
    return f"{MARKS[i][0]}-{MARKS[i][1]}".lower().replace(" ", "-")


def write_files(out):
    out.mkdir(parents=True, exist_ok=True)
    for i in range(len(MARKS)):
        (out / f"{slug(i)}.svg").write_text(svg(i, standalone=True)[0] + "\n")


def board(i):
    import build
    family, name, idea, _ = MARKS[i]
    mark, bg = svg(i)
    body = f"""<div style="width: 600px; height: 780px; background: #FFFFFF; color: {BLACK}; display: flex; flex-direction: column">
<div style="width: 600px; height: 600px; background: {bg}; display: flex">{mark}</div>
<div style="height: 180px; box-sizing: border-box; padding: 24px 32px; display: flex; flex-direction: column; gap: 8px; border-top: 1px solid #11111122">
<div style="display: flex; align-items: baseline; gap: 14px">
<div style="font-size: 13px; letter-spacing: 3px; color: {WINE}">{family.upper()}</div>
<h2 style="margin: 0; font-family: Syne, sans-serif; font-weight: 800; font-size: 28px; letter-spacing: -0.5px">{name}</h2>
</div>
<p style="margin: 0; font-family: 'Instrument Serif', serif; font-style: italic; font-size: 19px; line-height: 1.3; color: #3A3734">{idea}</p>
</div>
</div>"""
    return build.page(f"{family} {name}", 600, 780, body)


def write_canvas(root):
    proj = root / "project"
    index = json.loads((proj / "canvas.json").read_text())
    for i in range(len(MARKS)):
        fname = f"Refined-{slug(i)}.dc.html"
        (proj / fname).write_text(board(i))
        index["boards"][fname] = dict(x=(i % 3) * 680, y=(i // 3) * 1240, w=600, h=780,
                                      page="refined", title=f"{MARKS[i][0]} — {MARKS[i][1]}")
        if fname not in index["order"]:
            index["order"].append(fname)
    if not any(p["id"] == "refined" for p in index["pages"]):
        index["pages"].insert(0, {"id": "refined", "name": "Refined"})
    for row, family in enumerate(("The Swan, made young", "The Diamond Clover", "The Swallow")):
        index["notes"][f"refined-{row}"] = {"x": 0, "y": row * 1240 - 260, "text": family,
                                            "kind": "title1", "maxW": 1960, "page": "refined"}
    index["launch"] = {"view": "canvas", "page": "refined"}
    (proj / "canvas.json").write_text(json.dumps(index, indent=1))


if __name__ == "__main__":
    write_files(HERE / "refined")
    if "--canvas" in sys.argv:
        write_canvas(pathlib.Path(sys.argv[sys.argv.index("--canvas") + 1]))
