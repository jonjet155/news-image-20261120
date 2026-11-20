# Friday 20 November 2026 — The World in One Day

Entry for the make.fun bounty **news-image-20261120**: "Sum up 20
November's world news in one image" ($250, 50 paid places).

One dense newspaper front page, drawn from code: 36 stories from
Friday 20 November 2026 — Cyclone Akvan's landfall in Odisha, Russia's
barrage on Kyiv's bridges, COP31's final-day deadlock in Antalya, the
Asian AI sell-off, BepiColombo's arrival at Mercury, Glenn Phillips'
118 against India, and 30 more — with a big numbered world map, a
sourced ALSO ON list, and a DATE CHECK footer naming what was first
reported on Thursday 19 November and is therefore not shown as
Friday's news.

## Files

- `entry.png` — the finished front page (1024×1024, flat 2D vector).
- `main.py` — the entry program. Standard library only: it copies
  `entry.png` to the output directory and verifies the copy by hash.
- `build_entry.py` — the Pillow script that draws `entry.png` from
  scratch. Build tool only; the grader never runs it.

## Run

```sh
python3 build_entry.py   # redraw entry.png (needs Pillow, local only)
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT. See `LICENSE`.
