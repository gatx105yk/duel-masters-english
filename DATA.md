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
