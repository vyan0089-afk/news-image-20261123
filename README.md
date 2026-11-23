# THE TWENTY-THIRD — Monday 23 November 2026 in one image

Entry for the make.fun bounty
[news-image-20261123](https://make.fun/bounty/news-image-20261123):
"Sum up 23 November's world news in one image".

## The image

A one-page newspaper front page, **1024 × 1024**, 35 stories across
7 regions, all of them events that happened or were first reported on
Monday 23 November 2026:

- **3 heroes** — COP31 collapses in Antalya with no deal on fossil
  fuels; the AI sell-off rattles world markets (Nikkei −5.06%,
  S&P 500 −3.7%); a Russian strike kills 11 in Dymer, near Kyiv.
- **12 illustrated feature cards** — Alcaraz wins his first ATP Finals
  crown; the Riemann proof claim faces checks [CLAIM]; the "El Chapo
  Isidro" capture risks a cartel succession war; Bitcoin back above
  $61,000; South Korea's exports pass $1 trillion; the Delta outage;
  the penny ends; the Belgian strike; Khartoum drone attacks; two
  tankers hit in the Strait of Hormuz; Gaza contamination; Márquez's
  eighth MotoGP title.
- **World map** with 20 numbered pins, a **DATE CHECK** box verifying
  the day is Monday 23 November 2026, and **20 more stories in brief**.

Uncertainty is labelled throughout: `[CLAIM]` for unverified claims,
`[REPORTED]` for single-source reports, `[FORECAST]` for the future.
Per-story sources (outlet + date/time) appear on heroes, cards and
briefs. No make.fun story is included.

## How it is built

`draw_entry.py` draws `entry.png` from scratch with Pillow (no
downloaded images, no network, fixed random seed — deterministic).
`main.py` (Python 3.13, standard library only) copies `entry.png` to
`/output/entry.png`; running it twice writes byte-identical output.

## Verification

- `entry.png`: 1024 × 1024, 373,706 bytes (well above 200 KB)
- Deterministic: two runs of `main.py` produce identical sha256
- Kit check on a clean clone: 0 failed (see submission report)

## License

MIT — see [LICENSE](LICENSE).
