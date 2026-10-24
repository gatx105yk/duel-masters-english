# The data files

Two JSON files, versioned here so that pages can be computed and checked rather
than re-derived by eye each time.

## Why this exists

The daily encounter survey is published as **images**. Every figure on this site
was read off a pie chart by hand. That is slow, and it is the step most likely to
go wrong, so the readings are written down once and reused.

It paid for itself immediately. Reconciling every table cell in the four meta
pages against `data-nd-daily.json` turned up exactly one difference, and
confirmed it was a deliberate convention rather than a mistake.

## `data-nd-daily.json`

One record per survey day, 24 September to 12 October 2026.

| field | meaning |
|---|---|
| `games` | the survey's own game count for that day |
| `entries` | every slice, labelled exactly as the chart labels it, as a percentage |
| `completeness` | `full` = every slice recorded; `tracked` = only the six columns this site followed at the time, plus the leader |
| `leading_named_deck` | largest **named** slice; the unnamed bucket is excluded; `null` on a tie |
| `leader_tied_between` | present only when two entries tie for the top |
| `read_on` | the date this site read that chart |
| `unread_label_share` | a slice whose share was legible but whose label was not, in the 604px source image |

Every `full` day sums to 100.0 **except where rounding makes that impossible**. On a
small enough sample each slice is a whole number of games, and rounding nineteen of them
to one decimal can lose a few tenths: 22 October 2026 sums to **99.6** at 46 games and is
correct as recorded. For a day like that the check is **reconstructing the game counts and
matching the stated sample size** — the 22nd's slices come to 8, 6, 3×3, 2×9 and 1×5, which
is exactly 46. It is listed in `known_convention_differences`; do not "fix" it.

Neither check catches **a label swapped between two slices**, so the days an argument rests
on were re-read at higher magnification before publishing.

## How to read one of those charts

The source image is **604×501** and the page around it is not quiet, so read it like this.

Clone the chart into a fixed-position `div` and give that div **the whole viewport and a solid
white background**. Then size the image so the entire chart fits in one screen — about 860px wide
gives 713px tall, which fits. One screenshot, whole chart, nothing behind it.

**Do not read it in two halves through a transparent probe.** That was the old method and it has
two faults: the page bleeds through, and a sidebar image can sit over a label on the right-hand
side without it being obvious that anything is missing. On 23 October a dark strip from the page
covered part of the right edge in exactly that way; the full-viewport white version showed the same
eleven labels, but only the second version could prove it.

Then:

1. **Count the labels and count the slices, and make the two numbers match.** Eleven labels and
   eleven wedges is the check, and it is the only one of these that actually proves completeness.

   The charts read in October draw their wedges in descending order with `その他` last — 23 October
   runs 21.1, 11.9, 10.1, 10.1, 8.8, 7.5, 6.6, 5.3, 2.6, 2.6 and then `その他` at 13.4 — but **do
   not lean on that.** It has only been observed on a few charts, 22 October has no `その他` at all,
   and the draw order is a property of the image that this file does not record, so it cannot be
   checked against the series. A missed slice also leaves the remaining order descending, so it
   would not show up anyway. Treat it as a thing you will probably see, not as a test.
2. **Re-render larger for any label an argument rests on** — 1600px wide, shifted to bring the
   label into view — and zoom on it. `赤単` and `赤白` are one stroke apart and were 2.6 and 11.9 on
   the same chart.
3. **A negative claim needs the whole-chart view.** "This deck is not on the chart" is a statement
   about every label, so it cannot be made from a half view at all.

**What will not resolve:** at 604px a small label renders about eight to eleven pixels tall and no
magnification recovers it — upscaling adds no information. The three `轟` of a `轟轟轟` deck name
never resolve; read the civilisation prefix and the `(レイド無し)` suffix, which do, and match the
name against one already in the series.

## `data-deck-names.json`

Which source calls which deck what. This site has twice published a wrong count
of one deck's names, so the record lives here rather than in anybody's head.

It also carries the ranked season name, which matters for a practical reason: the
season running to 15 October is named after a card that is also a deck name, so a
keyword search on that name returns posts about the season rather than the deck.
Three posts found that way were about the season, and one of them was misread as
being about the deck before publication.

## What not to do with this

**Do not publish `data-nd-daily.json` as a table.** It is this site's record of its
own readings of somebody else's survey. Pages quote the few figures an article
argues from, with attribution, and that is the line this site keeps. Republishing
the series wholesale would be taking the survey's work, which is exactly what this
site refuses to do with tier lists and decklists elsewhere.
