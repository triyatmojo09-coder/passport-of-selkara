# Passport of Selkara

An entry for the make.fun competition **the-passport-page-of-a-countr-2-20261121-0318**
("The Passport Page of a Country That Isn't There").

[![make.fun · the-passport-page-of-a-countr-2-20261121-0318](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/triyatmojo09-coder/passport-of-selkara/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/triyatmojo09-coder/passport-of-selkara/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)

Competition page: https://make.fun/competitions/the-passport-page-of-a-countr-2-20261121-0318

## Concept

The **Republic of Selkara** is a fictional tidal island republic. Its capital
is **Port Liss**; its neighbours are **Kordava** and the **Free City of
Brannic**. The image is one open passport spread (1024×768, landscape):

- **Right page — data page.** Bilingual (English/French) header
  "REPUBLIC OF SELKARA / RÉPUBLIQUE DE SELKARA", a wave-and-star emblem,
  a pale blue-green guilloche background, and a line-engraving style
  portrait of the holder, Ilsa Tere Maren — a Selkaran *tide warden*
  (hair in a bun, collared uniform), drawn in dark blue ink.
  Data fields: Type P, country code SLK, passport No S0482137,
  born 14 MAR 1991 in Port Liss, issued 03 JUN 2023, expires 03 JUN 2033,
  authority Ministry of Tides — Port Liss. A small note records that
  dates in the document follow the Selkaran tide calendar.
  The two-line, 44-character MRZ at the foot uses genuine ICAO 7-3-1
  check digits, computed by the generator.
- **Left page — visas.** A Kordava single-entry visa sticker
  ("VALID 90 DAYS / FEE PAID 12 CROWNS", Havensholm consulate) and a
  chronological, consistent stamp history, all after the issue date:
  departed Port Liss 17 AUG 2025 → arrived Havenholm, Kordava
  18 AUG 2025 → arrived Free City of Brannic 02 SEP 2025 → arrived back
  in Port Liss 05 SEP 2025. The telling administrative detail is the
  green **TIDE TAX PAID · PORT LISS** stamp, dated the day of departure.

## Files

- `entry.png` — the generated passport spread (153,281 bytes, 1024×768).
- `make_passport.py` — the build-time generator (Pillow + DejaVu fonts);
  draws the whole spread and computes the MRZ check digits.
- `main.py` — the submitted program (Python 3.13, standard library only):
  validates `entry.png` (PNG signature + IEND, ≤1,048,576 bytes) and
  copies it atomically to `$MAKEFUN_OUTPUT_DIR/entry.png`
  (default `/output`), verifying the copy by SHA-256.

## Run

```sh
python3 make_passport.py   # regenerate entry.png (build time only)
python3 main.py            # write /output/entry.png
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py   # local test
```

Running `main.py` twice produces byte-identical output.
