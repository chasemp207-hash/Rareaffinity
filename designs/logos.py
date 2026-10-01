"""Ten R∀ logo directions: an R beside an upside-down A.

Letters are real typeface outlines converted to SVG paths, so the files need
no fonts to print. Writes designs/logos/*.svg; with --canvas DIR also writes
canvas artboards to DIR/project/ and adds them to its canvas.json.

    python3 designs/logos.py [--canvas DIR]

Fonts (all SIL Open Font License) are downloaded once into designs/.fonts/.
"""
import json
import math
import pathlib
import sys
import urllib.request

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / ".fonts"
SOURCES = {
    "bodoni": "bodonimoda/BodoniModa%5Bopsz,wght%5D.ttf",
    "syne": "syne/Syne%5Bwght%5D.ttf",
    "instrument-italic": "instrumentserif/InstrumentSerif-Italic.ttf",
    "jost": "jost/Jost%5Bwght%5D.ttf",
}

BLACK = "#111111"
IVORY = "#F4F2EE"
WINE = "#6B1526"
WINE_DEEP = "#3E0C17"
GOLD = "#B8995A"
BLUSH = "#EFE2DD"

_fonts = {}


def font(name, **axes):
    key = (name, tuple(sorted(axes.items())))
    if key not in _fonts:
        CACHE.mkdir(exist_ok=True)
        path = CACHE / SOURCES[name].split("/")[-1].replace("%5B", "[").replace("%5D", "]")
        if not path.exists():
            url = "https://raw.githubusercontent.com/google/fonts/main/ofl/" + SOURCES[name]
            path.write_bytes(urllib.request.urlopen(url).read())
        f = TTFont(path)
        if "fvar" in f:
            f = instancer.instantiateVariableFont(f, axes)
        _fonts[key] = f
    return _fonts[key]


class Glyph:
    def __init__(self, f, char):
        gs = f.getGlyphSet()
        name = f.getBestCmap()[ord(char)]
        pen = SVGPathPen(gs)
        gs[name].draw(pen)
        self.d = pen.getCommands()
        bp = BoundsPen(gs)
        gs[name].draw(bp)
        self.xmin, self.ymin, self.xmax, self.ymax = bp.bounds or (0, 0, 0, 0)
        self.adv = gs[name].width
        self.upm = f["head"].unitsPerEm

    def width(self, size):
        return (self.xmax - self.xmin) * size / self.upm

    def height(self, size):
        return (self.ymax - self.ymin) * size / self.upm

    def place(self, left, base, size, fill, turn=None, extra=""):
        """Put the glyph's ink box at `left`, sitting on `base`.

        turn="rotate" spins it 180°, turn="flip" mirrors it top to bottom.
        """
        s = size / self.upm
        if turn == "rotate":
            # maps the ink box onto itself, turned 180° about its centre
            t = f"translate({left + s * self.xmax:.2f} {base - s * (self.ymax - self.ymin) - s * self.ymin:.2f}) scale({-s:.5f} {s:.5f})"
        elif turn == "flip":
            t = f"translate({left - s * self.xmin:.2f} {base - s * (self.ymax - self.ymin) - s * self.ymin:.2f}) scale({s:.5f} {s:.5f})"
        else:
            t = f"translate({left - s * self.xmin:.2f} {base + s * self.ymin:.2f}) scale({s:.5f} {-s:.5f})"
        return f'<path transform="{t}" d="{self.d}" fill="{fill}"{extra}/>'


def g(name, char, **axes):
    return Glyph(font(name, **axes), char)


def word(name, text, left, base, size, fill, tracking=0, flip_a=False, **axes):
    """Set a line of caps glyph by glyph; returns (markup, right edge)."""
    out, x = [], left
    f = font(name, **axes)
    for ch in text:
        if ch == " ":
            x += size * 0.32 + tracking
            continue
        gl = Glyph(f, ch)
        s = size / gl.upm
        if flip_a and ch == "A":
            out.append(gl.place(x + s * gl.xmin, base, size, fill, turn="rotate"))
        else:
            out.append(f'<path transform="translate({x:.2f} {base:.2f}) scale({s:.5f} {-s:.5f})" d="{gl.d}" fill="{fill}"/>')
        x += gl.adv * s + tracking
    return "".join(out), x - tracking


def word_width(name, text, size, tracking=0, **axes):
    return word(name, text, 0, 0, size, "#000", tracking, **axes)[1]


def centered(name, text, cx, base, size, fill, tracking=0, flip_a=False, **axes):
    w = word_width(name, text, size, tracking, **axes)
    return word(name, text, cx - w / 2, base, size, fill, tracking, flip_a, **axes)[0]


def ring_text(name, text, cx, cy, r, size, fill, tracking=0, fill_circle=False, **axes):
    """Glyphs around a circle, reading clockwise from the top."""
    f = font(name, **axes)
    glyphs = [(ch, Glyph(f, ch) if ch != " " else None) for ch in text]
    advs = [(gl.adv * size / gl.upm if gl else size * 0.3) + tracking for _, gl in glyphs]
    total = sum(advs)
    if fill_circle:  # spread the letters so the text closes the ring exactly
        extra = (2 * math.pi * r - total) / len(advs)
        advs = [a + extra for a in advs]
        total = 2 * math.pi * r
    ang = -math.pi / 2 - (total / r) / 2 if total < 2 * math.pi * r * .98 else -math.pi / 2
    out = []
    for (ch, gl), a in zip(glyphs, advs):
        mid = ang + (a / 2) / r
        if gl:
            s = size / gl.upm
            px, py = cx + r * math.cos(mid), cy + r * math.sin(mid)
            rot = math.degrees(mid) + 90
            out.append(f'<path transform="translate({px:.2f} {py:.2f}) rotate({rot:.2f}) '
                       f'translate({-gl.adv * s / 2:.2f} 0) scale({s:.5f} {-s:.5f})" d="{gl.d}" fill="{fill}"/>')
        ang += a / r
    return "".join(out)


def pair(name, size, gap, fill_r, fill_a, cx, base, turn="rotate", **axes):
    """R and an upside-down A, centred on cx."""
    r, a = g(name, "R", **axes), g(name, "A", **axes)
    w = r.width(size) + gap + a.width(size)
    left = cx - w / 2
    ra = a.place(left + r.width(size) + gap, base, size, fill_a, turn=turn)
    return r.place(left, base, size, fill_r) + ra, w


# ================================================================ the ten
# Each returns (stage colour, viewBox, svg body). Canvas is 600 x 600.

def l01_maison():
    """High-contrast Didone, set tight: the fashion-house mark."""
    mark, _ = pair("bodoni", 250, 6, BLACK, BLACK, 300, 352, wght=400, opsz=96)
    rule = f'<rect x="250" y="404" width="100" height="1.4" fill="{WINE}"/>'
    sub = centered("bodoni", "RARE AFFINITY", 300, 452, 20, BLACK, tracking=9, wght=500, opsz=11)
    return IVORY, mark + rule + sub


def l02_shared_stem():
    """One continuous monoline: R's leg is the A's stroke, R's bowl bar is the A's crossbar."""
    d = ("M 40 240 L 40 40 L 90 40 A 50 50 0 0 1 90 140 L 190 140 "
         "M 110 140 L 150 240 L 230 40")
    mark = (f'<g transform="translate(165 160)"><path d="{d}" fill="none" stroke="{IVORY}" '
            f'stroke-width="13" stroke-linejoin="miter" stroke-miterlimit="10" stroke-linecap="square"/></g>')
    sub = centered("jost", "RARE AFFINITY", 300, 480, 15, IVORY, tracking=8, wght=400)
    return WINE, mark + sub


def l03_canvas():
    """The monogram as an all-over pattern, the way heritage houses tile their initials."""
    tile, _ = pair("bodoni", 44, 1, GOLD, GOLD, 0, 0, wght=500, opsz=96)
    star = (f'<path d="M 0 -9 Q 1.2 -1.2 9 0 Q 1.2 1.2 0 9 Q -1.2 1.2 -9 0 Q -1.2 -1.2 0 -9 Z" fill="{GOLD}"/>')
    cells = []
    for row in range(-1, 9):
        for col in range(-1, 7):
            x = col * 100 + (50 if row % 2 else 0)
            y = row * 76 + 40
            cells.append(f'<g transform="translate({x} {y + 15})">{tile}</g>' if (row + col) % 2 == 0
                         else f'<g transform="translate({x} {y})">{star}</g>')
    return WINE_DEEP, "".join(cells)


def l04_thread():
    """Hairline letters tied together by one wine thread."""
    R = "M 40 240 L 40 40 L 95 40 A 50 50 0 0 1 95 140 L 40 140 M 92 140 L 150 240"
    A = "M 190 40 L 250 240 L 310 40"
    thread = "M 40 140 L 360 140"
    mark = (f'<g transform="translate(110 165)">'
            f'<path d="{R} {A}" fill="none" stroke="{BLACK}" stroke-width="4" stroke-linejoin="miter" stroke-miterlimit="12"/>'
            f'<path d="{thread}" fill="none" stroke="{WINE}" stroke-width="4"/>'
            f'<circle cx="366" cy="140" r="6" fill="{WINE}"/></g>')
    sub = centered("jost", "RARE AFFINITY", 300, 480, 15, BLACK, tracking=8, wght=300)
    return "#FFFFFF", mark + sub


def l05_card():
    """The rare card: R reads at the top, the A reads from the other side."""
    r, a = g("bodoni", "R", wght=500, opsz=96), g("bodoni", "A", wght=500, opsz=96)
    diamond = lambda x, y, s: (f'<path d="M {x} {y - s} L {x + s * .7} {y} L {x} {y + s} '
                               f'L {x - s * .7} {y} Z" fill="{WINE}"/>')
    card = (f'<rect x="170" y="80" width="260" height="400" rx="16" fill="{IVORY}"/>'
            f'<rect x="184" y="94" width="232" height="372" rx="8" fill="none" stroke="{WINE}" stroke-width="1.2"/>')
    size = 78
    top = r.place(204, 178, size, BLACK) + diamond(204 + r.width(size) / 2, 206, 14)
    ax = 396 - a.width(size)
    bottom = (a.place(ax, 438, size, BLACK, turn="rotate")
              + diamond(ax + a.width(size) / 2, 438 - a.height(size) - 28, 14))
    centre = (f'<path d="M 300 236 L 330 280 L 300 324 L 270 280 Z" fill="none" stroke="{WINE}" stroke-width="1.6"/>'
              f'<path d="M 300 254 L 318 280 L 300 306 L 282 280 Z" fill="{WINE}"/>')
    return BLACK, card + top + bottom + centre


def l06_seal():
    """A gold wax-seal roundel."""
    ring = (f'<circle cx="300" cy="290" r="200" fill="none" stroke="{GOLD}" stroke-width="2"/>'
            f'<circle cx="300" cy="290" r="150" fill="none" stroke="{GOLD}" stroke-width="1"/>')
    text = ring_text("bodoni", "RARE AFFINITY · ONE OF ONE · RARE AFFINITY · ONE OF ONE · ", 300, 290, 166, 15, GOLD,
                     fill_circle=True, wght=500, opsz=11)
    mark, _ = pair("bodoni", 140, 2, GOLD, GOLD, 300, 339, wght=400, opsz=96)
    return BLACK, ring + text + mark


def l07_cutout():
    """Letters cut out of a wine block; the A's point breaks through the bottom edge."""
    r, a = g("syne", "R", wght=800), g("syne", "A", wght=800)
    size, gap = 128, 12
    left = 300 - (r.width(size) + gap + a.width(size)) / 2
    letters = (r.place(left, 292, size, "#000")
               + a.place(left + r.width(size) + gap, 404, size, "#000", turn="rotate"))
    box = 'x="100" y="130" width="400" height="240"'
    block = (f'<defs><mask id="l07-cut"><rect width="600" height="600" fill="#fff"/>{letters}</mask>'
             f'<mask id="l07-out"><rect width="600" height="600" fill="#fff"/><rect {box} fill="#000"/></mask></defs>'
             f'<rect {box} fill="{WINE}" mask="url(#l07-cut)"/>'
             f'<g mask="url(#l07-out)">{letters.replace("#000", WINE)}</g>')
    sub = centered("syne", "RARE AFFINITY", 300, 470, 18, BLACK, tracking=6, wght=700)
    return IVORY, block + sub


def l08_counterweight():
    """Italic R leaning forward, the A mirrored so it leans back: a zigzag of tension."""
    mark, _ = pair("instrument-italic", 300, -14, WINE_DEEP, WINE_DEEP, 300, 370, turn="flip")
    sub = centered("jost", "RARE AFFINITY", 300, 462, 15, WINE_DEEP, tracking=8, wght=400)
    return BLUSH, mark + sub


def l09_hairline():
    """Ultra-light geometric caps, wide apart, one wine point between them."""
    r, a = g("jost", "R", wght=100), g("jost", "A", wght=100)
    size, gap = 230, 70
    w = r.width(size) + gap + a.width(size)
    left = 300 - w / 2
    mark = r.place(left, 360, size, BLACK) + a.place(left + r.width(size) + gap, 360, size, BLACK, turn="rotate")
    dot = f'<circle cx="{left + r.width(size) + gap / 2:.1f}" cy="{360 - r.height(size) / 2:.1f}" r="7" fill="{WINE}"/>'
    sub = centered("jost", "RARE AFFINITY", 300, 452, 14, BLACK, tracking=11, wght=300)
    return "#FFFFFF", mark + dot + sub


def l10_wordmark():
    """The full name with every A turned: R∀RE ∀FFINITY."""
    big = centered("jost", "RARE", 300, 280, 104, IVORY, tracking=22, flip_a=True, wght=500)
    small = centered("jost", "AFFINITY", 300, 352, 44, IVORY, tracking=24, flip_a=True, wght=400)
    rule = f'<rect x="270" y="310" width="60" height="2" fill="{WINE}"/>'
    return BLACK, big + rule + small


LOGOS = [
    ("Maison", "High-contrast Didone set tight, like a Paris fashion house. Prints cleanly at any size.", l01_maison),
    ("Shared Stem", "One unbroken line: the R's leg becomes the A's stroke, and its bowl bar becomes the A's crossbar.", l02_shared_stem),
    ("Monogram Canvas", "The mark tiled with a four-point star, like the monogram canvases of the great houses. For linings, bags and packaging.", l03_canvas),
    ("The Thread", "Hairline letters tied by one wine thread that starts in the R and ends in a knot.", l04_thread),
    ("The Rare Card", "A playing card: the R reads from one end, the A from the other. That's why it's upside down.", l05_card),
    ("Seal", "A gold roundel for buttons, wax seals, hardware and embossing.", l06_seal),
    ("Breakout", "Letters cut out of a wine block; the A's point breaks through the edge.", l07_cutout),
    ("Counterweight", "An italic R leans forward and the A leans back. Two opposite forces in balance.", l08_counterweight),
    ("Hairline", "Ultra-light caps held far apart with one wine point between them. Quiet luxury.", l09_hairline),
    ("R∀RE ∀FFINITY", "The full wordmark with every A turned, so the monogram's idea carries into the name.", l10_wordmark),
]


def svg(i, standalone=False):
    fn = LOGOS[i][2]
    bg, body = fn()
    back = f'<rect width="600" height="600" fill="{bg}"/>' if standalone else ""
    size = "" if standalone else ' width="600" height="600"'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600"'
            f'{size}>{back}{body}</svg>'), bg


def slug(i):
    return f"{i + 1:02d}-" + "".join(c if c.isalnum() else "-" for c in LOGOS[i][0].lower().replace("∀", "a")).strip("-")


def write_files(out):
    out.mkdir(parents=True, exist_ok=True)
    for i in range(len(LOGOS)):
        (out / f"{slug(i)}.svg").write_text(svg(i, standalone=True)[0] + "\n")


def board(i):
    import build
    name, idea, _ = LOGOS[i]
    mark, bg = svg(i)
    body = f"""<div style="width: 600px; height: 760px; background: #FFFFFF; color: {BLACK}; display: flex; flex-direction: column">
<div style="width: 600px; height: 600px; background: {bg}; display: flex">{mark}</div>
<div style="height: 160px; box-sizing: border-box; padding: 24px 32px; display: flex; flex-direction: column; gap: 8px; border-top: 1px solid #11111122">
<div style="display: flex; align-items: baseline; gap: 14px">
<div style="font-size: 13px; letter-spacing: 3px; color: {WINE}">{i + 1:02d}</div>
<h2 style="margin: 0; font-family: Syne, sans-serif; font-weight: 800; font-size: 28px; letter-spacing: -0.5px">{name}</h2>
</div>
<p style="margin: 0; font-family: 'Instrument Serif', serif; font-style: italic; font-size: 20px; line-height: 1.3; color: #3A3734">{idea}</p>
</div>
</div>"""
    return build.page(f"Logo {i + 1:02d} {name}", 600, 760, body)


def write_canvas(root):
    proj = root / "project"
    index = json.loads((proj / "canvas.json").read_text())
    for i in range(len(LOGOS)):
        fname = f"Logo-{slug(i)}.dc.html"
        (proj / fname).write_text(board(i))
        index["boards"][fname] = dict(x=(i % 5) * 680, y=(i // 5) * 880, w=600, h=760,
                                      page="logos", title=f"{i + 1:02d} {LOGOS[i][0]}")
        if fname not in index["order"]:
            index["order"].append(fname)
    if not any(p["id"] == "logos" for p in index["pages"]):
        index["pages"].insert(0, {"id": "logos", "name": "Logos"})
    index["notes"]["logos"] = {"x": 0, "y": -260, "text": "R∀ — ten logo directions",
                               "kind": "title1", "maxW": 3320, "page": "logos"}
    index["launch"] = {"view": "canvas", "page": "logos"}
    (proj / "canvas.json").write_text(json.dumps(index, indent=1))


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    write_files(HERE / "logos")
    if "--canvas" in sys.argv:
        write_canvas(pathlib.Path(sys.argv[sys.argv.index("--canvas") + 1]))
