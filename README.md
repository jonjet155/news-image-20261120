# news-image-20261120 — "Friday 20 November 2026"

A one-page newspaper front page summing up Friday 20 November 2026 in
36 stories, drawn as flat 2D vector art with Python (PIL) at build time.

## The page

- **Masthead:** dark navy band, huge serif date, subline with the day's four
  biggest stories, thin multicolour stripe.
- **Stats strip:** 300,000+ evacuated ahead of Cyclone Akvan; ~30 ballistic
  missiles fired at Kyiv; KOSPI −5.2%; Japan core CPI 2.2%; Phillips 118;
  8 years for BepiColombo to reach Mercury.
- **13 illustrated panels:** 3 wide lead panels (Cyclone Akvan landfall in
  Odisha; Russian missile barrage on Kyiv; COP31 final day deadlocked in
  Antalya) + 10 feature panels (Asia AI sell-off, BepiColombo at Mercury,
  EU–UK reset deal, Japan inflation, China rates, Phillips 118, Bukele
  third-term bid, migrant boat off Yemen, Italy CGIL strike, pancreatic
  cancer pill trial). Every panel has a scene illustration filling most of
  the panel, a dark data band, a bold serif headline, a deck and a source.
- **Map:** quarter-page world map with 13 numbered pins matching the panels.
- **Also on:** 23 more briefs (items 14–36), each with place, headline and
  source.
- **Date check:** stories first reported Thursday 19 November are listed as
  excluded, so the page shows Friday's news only.

## Sources

Every headline was verified against real reporting from Friday 20 November
2026 (Reuters, AP, AFP, BBC, Al Jazeera, The Hindu, Yonhap, ICC, EU
Council, PBOC). Claims are attributed on the page, not stated as fact.

## Entry

`main.py` (Python 3.13, standard library only) copies the pre-built
`entry.png` into `$MAKEFUN_OUTPUT_DIR`. It runs twice and writes identical
bytes both times.
