# Rare Affinity — The Collection

Palette: **Black** `#141414` · **White** `#F4F2EE` · **Wine** `#6B1526` (on white) / `#A3263D` (on black)
Type: Syne 800 · Instrument Serif Italic · IBM Plex Mono

| # | Piece | Design | Print file(s) |
|---|---|---|---|
| 01 | The Knit — cable knit sweater | Two-ring symbol, tonal embroidery, left chest | `symbol-rings--*.svg` |
| 02 | The Fitted — fitted tee | Ra monogram embroidered in wine, left chest; wine flag label at hem | `monogram-ra--*.svg` |
| 03 | Escape Line — boxy tee | A wine chain-stitch line leaves a box, crosses the shoulder, ends on the back: "outside the box." | `escape-line-front--*.svg`, `escape-line-back--*.svg` |
| 04 | Falling — boxy zip hoodie | A man falling, painted in chalk, reaching for a wine heart | `falling-man-chalk--on-dark.svg` |

Each file comes as `--on-dark` (for black garments) and `--on-light` (for white garments).
Earlier concept graphics (`wordmark`, `rare-form`, `one-in-eight-billion`, `overlap`, `seal`) are also in `print/`.

## Before sending to a manufacturer
- **Embroidery (01, 02, 03):** send the SVG to your embroiderer for digitizing. The escape-line
  artwork is laid out on a 600×640 garment template, so it shows where the line crosses the shoulder seam.
- **Chalk print (04):** the chalk texture is an SVG filter. Open the file in a browser or Inkscape,
  export a 300 dpi PNG at print size (about 12×16 in), and print it with DTG or a high-density screen print.
- **Text:** fonts load from Google Fonts. Convert text to outlines before sending
  (Inkscape: *Path → Object to Path*).

## Editing
Garments and new graphics: `collection.py`. Palette and early concepts: `build.py`. Regenerate everything with:

    python3 designs/build.py

## Logos — R∀
Ten directions for the R + upside-down A mark live in `logos/` (01–10). Every letter is an
outlined path taken from open-source typefaces (Bodoni Moda, Syne, Instrument Serif, Jost), so the
files print without fonts. Regenerate with `pip install fonttools` then `python3 designs/logos.py`
(the fonts download once into `designs/.fonts/`).

## Symbols — no letters
Ten wordless marks in `symbols/` (01–10), the way a polo player stands for Polo:
Black Swan, Swan Pair, Four Hearts, Eclipse, Red Thread, The Key, Swallows, The Stone, Linked, The Pearl.
Regenerate with `python3 designs/symbols.py`.
