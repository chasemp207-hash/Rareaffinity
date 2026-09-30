# Rare Affinity — Drop 01 designs

Print files live in `print/`. Each graphic comes in two colorways:
`--on-dark` (bone + ember, for black garments) and `--on-light` (ink + oxblood, for bone/heather garments).

| Graphic | Use |
|---|---|
| `wordmark` | Left-chest print, neck label, hang tag |
| `rare-form` | Back print — Rare Form Tee (black) |
| `one-in-eight-billion` | Back print — One in Eight Billion Tee (bone) |
| `overlap` | Back print — Overlap Crewneck (heather); also the brand symbol |
| `seal` | Round monogram — patches, embroidery, stickers |

## Brand basics
- **Palette:** Bone `#EFEAE0` · Ink `#141312` · Oxblood `#7A1F1F` · Ember `#C8553D` · Heather `#B9B2A6`
- **Type:** Syne 800 (headlines) · Instrument Serif Italic (the feeling word, always in the accent color) · IBM Plex Mono (tags and specs, wide tracking)

## Before sending to a printer
The SVGs load their fonts from Google Fonts. Printers usually need text converted to outlines:
open the file in Illustrator, Inkscape or Figma with the three fonts installed, then outline all text
(Inkscape: *Path → Object to Path*) and export a PDF or SVG at final print size.

## Editing
All graphics come from `build.py`. Change colors or copy there, then run:

    python3 designs/build.py
