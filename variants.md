# Variants — news-image-20261118 round 2

Date summed up: **Wednesday 18 November 2026**. All three variants carry the
same six stories (same facts, same illustrations, same date banner) and differ
only in layout. Text is rendered with PIL/DejaVu, never by the image model, so
no variant has garbled text. All are 1024×1024 PNG, ≤1 MiB.

## The six stories (researched 19 Nov 2026, WIB)

1. **Gulf war escalates (Middle East)** — U.S. jets struck a Revolutionary
   Guard missile site on Qeshm Island; Iran fired back at Kuwait (Ali Al
   Salem Air Base) and Bahrain. Sources: Just Security Early Edition,
   Reuters/WSJ via One Turn, NPR.
2. **Crimea bridge partly collapses (Ukraine)** — Ukrainian drones/missiles
   hit the Kerch bridge a second day; one arch/span fell into the strait.
   Sources: Horizon, One Turn, Just Security.
3. **Xi hosts Putin in Shenzhen (China)** — Xi and Putin met ahead of
   three-way talks with Trump on Ukraine, Iran and trade. Sources: AFP/AP
   via Open Chronicle, NPR.
4. **Peltola wins Alaska (U.S. politics)** — Democrat Mary Peltola beat Sen.
   Dan Sullivan; Democrats take a 56–44 Senate majority. Sources: AP/Alaska
   Public Media via Open Chronicle, NPR.
5. **Ebola doubles in DR Congo (health)** — 11,000+ cases, 5,400+ deaths;
   nearly three in four infected children under five do not survive.
   Sources: UN via One Turn, Horizon.
6. **Cyclone Xavier (Pacific)** — Category 5 storm hit the northern Cook
   Islands. Source: One Turn.

## Variant A — newspaper front page (CHOSEN)

- Masthead banner with the date in 40 px bold; full-width hero image of the
  Gulf missile strikes with the biggest headline (32 px, one line) and a
  one-line summary; 2×2 grid for Bridge / Summit / Alaska / Ebola (image +
  kicker + headline + one-line summary each); red footer strip for Cyclone
  Xavier with thumbnail + headline.
- 884,986 bytes.

## Variant B — six-panel mosaic

- Same date banner; 2×3 grid of equal panels, every story the same size
  (image 196 px + kicker + headline + one-line summary). Cleanest and most
  uniform, but flat: no story stands out as the day's lead.
- 327,383 bytes (palette-quantised; colours survive, flat style).

## Variant C — lead story + list

- Gulf hero fills the whole left column (600×600) with a 40 px lead headline
  underneath; five stories stacked in a right-hand list with thumbnails.
- Most dramatic lead, but the right column is dense (headlines wrap to three
  lines, thumbnails cramped) and the lead block leaves empty white space at
  the bottom.
- 912,489 bytes.

## Why A wins

Judged by the bounty criteria, in order:

1. **Names the day + specific events** — all three tie (same banner, same six
   dated stories).
2. **Selection & breadth** — all three tie (Middle East, Ukraine, China,
   U.S. politics, African health, Pacific weather).
3. **Reads** — A wins: the day's biggest story (Gulf) gets the largest image
   and the largest headline in one line; every other story still has a clear
   picture, headline and summary. B is uniform but nothing signals what
   mattered most; C's list column is the hardest to scan.
4. **Faithful** — all three tie (same verified facts, no hype).
5. **Craft** — A wins: a real front page with one clear hierarchy (banner →
   hero → grid → footer strip), no overflow, no empty space, no clipped text.
   B is a close second; C loses points for the cramped list and the empty
   patch under the lead block.

## Build notes

- Six illustrations generated with the image model, text-free on purpose
  (`assets/`): gulf-strikes, crimea-bridge, shenzhen-summit, alaska-senate,
  ebola-drc, cyclone-xavier. Each was inspected visually; all clean, no text
  artefacts.
- Composition by `compose.py` (PIL, DejaVu Sans/Serif). First pass had text
  overflow in the grid/list cells (summaries clipped by the next row); fixed
  by shortening summaries to one line (A/B) / two lines (C) and re-checking
  all three renders visually.
- `entry.png` = `variants/variant-a.png` (byte-identical copy).
