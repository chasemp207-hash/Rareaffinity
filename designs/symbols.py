"""Ten wordless Rare Affinity symbols, the way a polo player stands for Polo.

Writes designs/symbols/*.svg; with --canvas DIR also writes canvas artboards
to DIR/project/ and adds a "Symbols" page to its canvas.json.

    python3 designs/symbols.py [--canvas DIR]
"""
import json
import math
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent

BLACK = "#111111"
IVORY = "#F4F2EE"
WINE = "#6B1526"


# ---------------------------------------------------------------- helpers
def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return tuple(u ** 3 * a + 3 * u * u * t * b + 3 * u * t * t * c + t ** 3 * d
                 for a, b, c, d in zip(p0, p1, p2, p3))


def tapered(segments, w0, w1, steps=40):
    """A filled stroke along cubic segments whose width runs from w0 to w1."""
    pts = []
    for seg in segments:
        for i in range(steps + (1 if seg is segments[-1] else 0)):
            pts.append(cubic(*seg, i / steps))
    n = len(pts)
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        a, b = pts[max(i - 1, 0)], pts[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        w = (w0 + (w1 - w0) * i / (n - 1)) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    ring = left + right[::-1]
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in ring) + " Z"
    caps = (f'M {pts[0][0] + w0 / 2:.1f} {pts[0][1]:.1f} a {w0 / 2:.1f} {w0 / 2:.1f} 0 1 0 {-w0:.1f} 0 '
            f'a {w0 / 2:.1f} {w0 / 2:.1f} 0 1 0 {w0:.1f} 0 Z '
            f'M {pts[-1][0] + w1 / 2:.1f} {pts[-1][1]:.1f} a {w1 / 2:.1f} {w1 / 2:.1f} 0 1 0 {-w1:.1f} 0 '
            f'a {w1 / 2:.1f} {w1 / 2:.1f} 0 1 0 {w1:.1f} 0 Z')
    return d + " " + caps


def mirror_x(d, axis=300):
    """Mirror an absolute path made of M/C/L/Z commands around x = axis."""
    out, i = [], 0
    for tok in d.replace(",", " ").split():
        try:
            v = float(tok)
        except ValueError:
            out.append(tok)
            continue
        out.append(f"{2 * axis - v:g}" if i % 2 == 0 else tok)
        i += 1
    return " ".join(out)


def heart(cx, cy, s, rot=0, fill=BLACK):
    """A heart with its point at (cx, cy), lobes pointing away along `rot`."""
    d = ("M 0 0 C -6 -14 -40 -34 -40 -62 C -40 -84 -14 -92 0 -70 "
         "C 14 -92 40 -84 40 -62 C 40 -34 6 -14 0 0 Z")
    return f'<path transform="translate({cx} {cy}) rotate({rot}) scale({s})" d="{d}" fill="{fill}"/>'


# ---------------------------------------------------------------- the ten
# Each returns (background, svg body) on a 600 x 600 canvas.

def s01_black_swan():
    """A 'black swan' is the rare event. Black swans also mate for life."""
    body = ("M 150 296 C 178 334 214 376 278 382 C 346 388 398 372 410 336 "
            "C 416 316 404 300 386 296 C 332 286 300 262 258 254 "
            "C 216 246 182 264 150 296 Z")
    neck = tapered([((392, 304), (412, 246), (340, 218), (344, 168)),
                    ((344, 168), (347, 122), (400, 110), (412, 146))], 34, 15)
    head = '<ellipse cx="410" cy="148" rx="17" ry="12" transform="rotate(32 410 148)"/>'
    beak = f'<path d="M 418 146 L 456 176 L 414 160 Z" fill="{WINE}"/>'
    feathers = "".join(
        f'<path d="{d}" fill="none" stroke="{IVORY}" stroke-width="1.6" stroke-linecap="round"/>'
        for d in ("M 196 292 C 240 280 300 290 352 318", "M 214 316 C 256 306 304 316 340 338"))
    water = f'<path d="M 150 410 L 450 410" stroke="{BLACK}" stroke-width="1.4"/>'
    return IVORY, (f'<g transform="translate(-4 40)"><g fill="{BLACK}"><path d="{body}"/><path d="{neck}"/>{head}</g>'
                   f'{beak}{feathers}{water}</g>')


def s02_swan_pair():
    """Two swans whose necks draw one heart between them."""
    body = ("M 112 330 C 140 364 186 398 246 400 C 286 402 304 388 298 364 "
            "C 292 344 272 334 250 330 C 206 318 168 306 144 312 C 128 316 118 322 112 330 Z")
    neck = tapered([((282, 352), (210, 330), (172, 250), (206, 196)),
                    ((206, 196), (236, 152), (290, 160), (292, 196))], 26, 11)
    head = '<ellipse cx="289" cy="200" rx="13" ry="10" transform="rotate(70 289 200)"/>'
    one = f'<path d="{body}"/><path d="{neck}"/>{head}'
    left = f'<g fill="{BLACK}">{one}</g>'
    right = f'<g fill="{WINE}" transform="translate(600 0) scale(-1 1)">{one}</g>'
    return IVORY, f'<g transform="translate(0 24)">{left}{right}</g>'


def s03_clover():
    """A four-leaf clover is rare; every leaf here is a heart."""
    leaves = "".join(
        heart(300 + 5 * math.sin(math.radians(r)), 262 - 5 * math.cos(math.radians(r)), 1.25, r,
              WINE if r == 45 else BLACK) for r in (45, 135, 225, 315))
    stem = f'<path d="M 300 264 C 300 340 314 400 352 462" fill="none" stroke="{BLACK}" stroke-width="5" stroke-linecap="round"/>'
    return IVORY, stem + leaves


def s04_eclipse():
    """An eclipse: two bodies align, rarely. The bright point is the diamond ring."""
    return BLACK, (f'<circle cx="286" cy="300" r="108" fill="{IVORY}"/>'
                   f'<circle cx="314" cy="300" r="108" fill="{BLACK}" stroke="{IVORY}" stroke-width="1.4"/>'
                   f'<circle cx="300" cy="192.9" r="5" fill="{WINE}"/>'
                   f'<circle cx="300" cy="192.9" r="12" fill="none" stroke="{WINE}" stroke-width="1"/>')


def s05_red_thread():
    """The red thread of fate: one line that ties two people, with a single loop."""
    d = ("M 70 360 C 170 360 250 352 298 318 C 352 280 360 214 312 206 "
         "C 262 198 252 268 300 318 C 340 358 430 364 530 360")
    return IVORY, (f'<path d="{d}" fill="none" stroke="{WINE}" stroke-width="4" stroke-linecap="round"/>'
                   f'<circle cx="70" cy="360" r="5" fill="{WINE}"/><circle cx="530" cy="360" r="5" fill="{WINE}"/>')


def s06_key():
    """One key for one lock. The bow is a heart."""
    bow = ("M 300 238 C 294 224 262 206 262 180 C 262 158 288 150 300 170 "
           "C 312 150 338 158 338 180 C 338 206 306 224 300 238 Z")
    return IVORY, (f'<g transform="translate(300 300) scale(1.3) translate(-300 -300)">'
                   f'<path d="{bow}" fill="none" stroke="{BLACK}" stroke-width="4" stroke-linejoin="round"/>'
                   f'<rect x="297" y="236" width="6" height="196" fill="{BLACK}"/>'
                   f'<rect x="286" y="250" width="28" height="4" fill="{BLACK}"/>'
                   f'<path d="M 303 396 L 326 396 L 326 406 L 316 406 L 316 414 L 326 414 L 326 430 L 303 430 Z" fill="{BLACK}"/>'
                   f'<circle cx="300" cy="186" r="5" fill="{WINE}"/></g>')


def s07_swallows():
    """Swallows return to the same partner every year."""
    half = ("M 300 196 C 309 196 314 206 314 218 C 314 230 316 238 322 242 "
            "C 380 226 460 236 520 300 C 456 270 392 270 328 288 "
            "C 326 302 324 314 318 326 C 334 372 348 420 366 468 "
            "C 338 428 316 398 300 380")
    parts = half.split(" C ")
    # left half: mirror and walk the right half backwards so it closes cleanly
    pts = [tuple(map(float, half[2:].split(" C ")[0].split()))]
    segs = []
    for c in parts[1:]:
        n = list(map(float, c.split()))
        segs.append([(n[0], n[1]), (n[2], n[3]), (n[4], n[5])])
    back = []
    prev = pts[0]
    chain = [prev]
    for s in segs:
        chain.append(s[2])
    for i in range(len(segs) - 1, -1, -1):
        c1, c2, end = segs[i]
        start = chain[i]
        back.append(f"C {600 - c2[0]:g} {c2[1]:g} {600 - c1[0]:g} {c1[1]:g} {600 - start[0]:g} {start[1]:g}")
    bird = half + " " + " ".join(back) + " Z"
    big = f'<path d="{bird}" fill="{BLACK}" transform="translate(262 340) rotate(38) scale(.82) translate(-300 -320)"/>'
    small = f'<path d="{bird}" fill="{WINE}" transform="translate(432 176) rotate(38) scale(.36) translate(-300 -320)"/>'
    return IVORY, big + small


def s08_diamond():
    """The rare stone, in hairline. One facet holds the colour."""
    line = lambda d: f'<path d="{d}" fill="none" stroke="{IVORY}" stroke-width="2" stroke-linejoin="round"/>'
    return WINE, (f'<path d="M 240 260 L 300 220 L 360 260 Z" fill="{IVORY}"/>'
                  + line("M 250 220 L 350 220 L 420 260 L 300 430 L 180 260 Z")
                  + line("M 180 260 L 420 260")
                  + line("M 250 220 L 240 260 L 300 220 L 360 260 L 350 220")
                  + line("M 240 260 L 300 430 L 360 260 M 300 260 L 300 430"))


def s09_rings():
    """Two rings, linked: neither can leave without the other."""
    ring = lambda cx, color, extra="": (
        f'<circle cx="{cx}" cy="300" r="86" fill="none" stroke="{IVORY}" stroke-width="18"{extra}/>'
        f'<circle cx="{cx}" cy="300" r="86" fill="none" stroke="{color}" stroke-width="6"{extra}/>')
    clip = '<clipPath id="s09-over"><rect x="276" y="206" width="48" height="44"/></clipPath>'
    return IVORY, (f'<defs>{clip}</defs>' + ring(258, WINE) + ring(342, BLACK)
                   + ring(258, WINE, ' clip-path="url(#s09-over)"'))


def s10_pearl():
    """The rare find: a shell, open, with one wine pearl."""
    cx, cy, r = 300, 380, 176
    ribs, edge = [], []
    n = 11
    for i in range(n + 1):
        a = math.radians(200 + i * 140 / n)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        ribs.append(f"M {cx} {cy} L {x:.1f} {y:.1f}")
        edge.append((x, y))
    scallop = f"M {edge[0][0]:.1f} {edge[0][1]:.1f} " + " ".join(
        f"A 26 26 0 0 1 {x:.1f} {y:.1f}" for x, y in edge[1:])
    return IVORY, (f'<path d="{" ".join(ribs)}" stroke="{BLACK}" stroke-width="1.6"/>'
                   f'<path d="{scallop}" fill="none" stroke="{BLACK}" stroke-width="3" stroke-linejoin="round"/>'
                   f'<circle cx="300" cy="370" r="34" fill="{IVORY}"/>'
                   f'<circle cx="300" cy="366" r="27" fill="{WINE}"/>'
                   f'<circle cx="291" cy="357" r="5.5" fill="{IVORY}" fill-opacity=".5"/>')


SYMBOLS = [
    ("Black Swan", "A black swan is the rare event, and swans mate for life. Rare and affinity in one animal. The beak carries the wine.", s01_black_swan),
    ("Swan Pair", "Two swans, one black and one wine. Their necks draw a single heart between them.", s02_swan_pair),
    ("Four Hearts", "A four-leaf clover is the rare find. Every leaf is a heart, and one is wine.", s03_clover),
    ("Eclipse", "Two bodies line up only rarely. The wine point is the diamond ring at the moment they meet.", s04_eclipse),
    ("Red Thread", "The legend of the red thread: one cord ties two people who are meant to meet. It makes a single loop.", s05_red_thread),
    ("The Key", "One key, one lock. An antique key with a heart for a bow.", s06_key),
    ("Swallows", "Swallows return to the same partner every year. A black swallow, and a wine one following.", s07_swallows),
    ("The Stone", "The rare stone in hairline, with one facet filled.", s08_diamond),
    ("Linked", "Two rings woven together. Neither can leave without the other.", s09_rings),
    ("The Pearl", "The rare find: an open shell holding one wine pearl.", s10_pearl),
]


def svg(i, standalone=False):
    bg, body = SYMBOLS[i][2]()
    back = f'<rect width="600" height="600" fill="{bg}"/>' if standalone else ""
    size = "" if standalone else ' width="600" height="600"'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600"{size}>{back}{body}</svg>', bg


def slug(i):
    return f"{i + 1:02d}-" + SYMBOLS[i][0].lower().replace(" ", "-")


def write_files(out):
    out.mkdir(parents=True, exist_ok=True)
    for i in range(len(SYMBOLS)):
        (out / f"{slug(i)}.svg").write_text(svg(i, standalone=True)[0] + "\n")


def board(i):
    import build
    name, idea, _ = SYMBOLS[i]
    mark, bg = svg(i)
    body = f"""<div style="width: 600px; height: 780px; background: #FFFFFF; color: {BLACK}; display: flex; flex-direction: column">
<div style="width: 600px; height: 600px; background: {bg}; display: flex">{mark}</div>
<div style="height: 180px; box-sizing: border-box; padding: 24px 32px; display: flex; flex-direction: column; gap: 8px; border-top: 1px solid #11111122">
<div style="display: flex; align-items: baseline; gap: 14px">
<div style="font-size: 13px; letter-spacing: 3px; color: {WINE}">{i + 1:02d}</div>
<h2 style="margin: 0; font-family: Syne, sans-serif; font-weight: 800; font-size: 28px; letter-spacing: -0.5px">{name}</h2>
</div>
<p style="margin: 0; font-family: 'Instrument Serif', serif; font-style: italic; font-size: 19px; line-height: 1.3; color: #3A3734">{idea}</p>
</div>
</div>"""
    return build.page(f"Symbol {i + 1:02d} {name}", 600, 780, body)


def write_canvas(root):
    proj = root / "project"
    index = json.loads((proj / "canvas.json").read_text())
    for i in range(len(SYMBOLS)):
        fname = f"Symbol-{slug(i)}.dc.html"
        (proj / fname).write_text(board(i))
        index["boards"][fname] = dict(x=(i % 5) * 680, y=(i // 5) * 900, w=600, h=780,
                                      page="symbols", title=f"{i + 1:02d} {SYMBOLS[i][0]}")
        if fname not in index["order"]:
            index["order"].append(fname)
    if not any(p["id"] == "symbols" for p in index["pages"]):
        index["pages"].insert(0, {"id": "symbols", "name": "Symbols"})
    index["notes"]["symbols"] = {"x": 0, "y": -260, "text": "Symbols — no letters",
                                 "kind": "title1", "maxW": 3320, "page": "symbols"}
    index["launch"] = {"view": "canvas", "page": "symbols"}
    (proj / "canvas.json").write_text(json.dumps(index, indent=1))


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    write_files(HERE / "symbols")
    if "--canvas" in sys.argv:
        write_canvas(pathlib.Path(sys.argv[sys.argv.index("--canvas") + 1]))
