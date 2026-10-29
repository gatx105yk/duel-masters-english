# Where things stand

Updated 29 Oct 2026.

---

## The one number that matters

Read from Search Console on 13 October 2026, three-month range, URL-prefix property
`https://duelmasters.editioncompass.com/`.

| | |
|---|---|
| Articles live | 43, all linked from the index |
| Pages indexed by Google | **1** — `rulings.html`, and nothing else |
| Not indexed | 42 — 35 "discovered, not crawled", 7 "crawled, not indexed" |
| Not yet in the report | 3 — the 10–13 October articles; sitemap last read 9 October |
| Clicks, all time | **0** |
| Impressions | 66 |
| Average position | 14.4 |

Forty-three articles, fact-checked to the point of re-reading source charts at
2000px, and Google has indexed one page. **This is not a sitemap problem and not a
quality problem.** "Discovered, not crawled" on 35 pages means no other site links
here, so Google will not spend crawl budget. Nothing written from here changes that.

### The two findings that are worse than the headline

**The home page is "crawled, not indexed".** Google fetches it and declines to list it.
Every one of the 43 internal links is hung off a page that is not in the index, so the
internal linking is doing nothing for discovery.

**Three of the four pages that have ever earned an impression are now on the
not-indexed side.** `2026-08-18-lionel-krone.html` holds average position 3.7, the best
on the site, and is "crawled, not indexed".

| Page with impressions | Impressions | Avg position | Index state |
|---|---|---|---|
| `rulings.html` | 33 | 15.2 | indexed |
| `2026-09-14-deck-rules.html` | 20 | 21.7 | crawled, not indexed |
| `2026-08-18-lionel-krone.html` | 15 | **3.7** | crawled, not indexed |
| `2026-09-14-how-to-play.html` | 13 | 36.4 | crawled, not indexed |

The index report is a snapshot of the current state and the performance report is three
months of history, so the two are not on the same clock. Read plainly, though, this looks
like coverage being **lost**, not merely never gained. Not proven — recheck before
treating it as fact.

Those four rows sum to 81 impressions against a reported total of 66. Google aggregates
some rows, and the cause was not established. Do not quote the per-page figures as a total.

### Crawled, not indexed — all 7

`(home page)` · `2026-08-10-dmps-nd-meta.html` · `2026-08-10-hall-of-fame.html` ·
`2026-08-18-lionel-krone.html` · `2026-09-08-the-three-decks.html` ·
`2026-09-14-deck-rules.html` · `2026-09-14-how-to-play.html`

### Discovered, not crawled — all 35

August: `calendar` · `magic-crossover` · `plays-grand-prix` · `plays-now-running` ·
`precious-idol-festival` · `heroes-set-summer` · `before-you-start` · `tournament-meta` ·
`plays-crossover-pack` · `railgun-collab` · `collab-aftermath` · `mana-in-plays` ·
`why-not-attack`

September: `how-the-data-works` · `japanese-sources` · `kamiart-mtg` ·
`watching-the-grand-prix` · `b-reishu-raid` · `grand-prix-result` · `all-division-decks` ·
`izanto` · `meta-shift` · `plays-vs-paper` · `set37-first-cards` · `set37-reaction` ·
`piloting-heavens-gate` · `set37-day-one` · `card-changes` · `first-numbers`

October: `known-issues` · `nine-days` · `what-players-say` · `same-decks` ·
`legend-battle-split`

Also: `glossary.html`

---

## Next, in order

### 1. Tell someone the site exists
Still not done. It has been on this list since 20 August, and it is now the only
thing blocking everything else.

- **r/DuelMastersPlays** — ~13 posts a week, mostly install and rules questions. `how-to-play`
  and `before-you-start` were written for exactly those people
- **Duel Masters Discord**, ~3,770 members, has a `duema-news` channel
- **Fandom wiki** — one external link would do it

One is enough. One inbound link is what moves 35 pages out of "discovered, not crawled"
— and it points at the home page, which is the page Google currently declines to index.

This has to be the author. Claude does not post to communities on anyone's behalf, and
Reddit is not reachable from its tools.

### 2. The の紋章 deck has no name yet

A deck appears on the ND survey that this site cannot name. Its chart label is four
characters ending `の紋章`, and the 604px source image renders it about ten pixels tall,
so the first character does not resolve at any magnification. Confirmed unreadable at
native 1:1 on 16 October.

It is recorded as `（判読不能）の紋章` on **1 October (4.3), 2 October (3.2) and
9 October (2.1)**, and listed in each day's `label_unresolved`.

To resolve it, find the name in a text source rather than a chart — a deck guide, a
tournament list, or a post that names it. Until then do not guess it and do not put it
in an article. It is not a column on any published page, so nothing is blocked.

**All fourteen full-read days (1–14 October) now sum to 100.0.** The seven September days are
partial six-column reads and the check does not apply to them. The 1 and 2 October re-read is done; every
published cell on the nine-day page (54) and the week two page (49) was re-checked
against the corrected data with no differences.

### 3. Indexing requests — continue tomorrow

Thirteen URLs are in Google's priority crawl queue: eleven on 13 October, two more on
14 October.

**The quota is a rolling window, not a calendar day.** Eleven went through at about
22:50 on the 13th. At 20:55 on the 14th — 22 hours later — only two more were accepted
before the third was refused with "1 日の割り当て量を超えたため、リクエストを処理できませんでした".
The message says to try tomorrow, but midnight is not what clears it. Budget about
thirteen per 24 hours and run the batch no earlier than the previous one.

Also: the confirmation marker takes 25–40 seconds to appear after the click. Reading it
too early reports a success as unconfirmed.

Submitted 13 Oct, confirmed queued:

`(home page)` · `glossary.html` · `2026-08-20-before-you-start.html` ·
`2026-08-31-mana-in-plays.html` · `2026-08-31-why-not-attack.html` ·
`2026-09-14-plays-vs-paper.html` · `2026-08-16-magic-crossover.html` ·
`2026-08-16-calendar.html` · `2026-09-08-how-the-data-works.html` ·
`2026-09-16-piloting-heavens-gate.html` · `2026-10-13-dragerion-talk.html`

Submitted 14 Oct, confirmed queued: `2026-10-11-dragerion-lead.html` ·
`2026-10-10-week-two.html`. Refused on quota, retry first:
`2026-09-08-japanese-sources.html`.

**Twenty-six of the thirty-five remain.** Work down them evergreen first — every page
that has ever earned an impression is a reference or beginner page, and no dated news
article has earned one. The seven "crawled, not indexed" are deliberately last:
Google has already fetched and declined them, so a second request changes nothing it
has not already judged.

**Two diagnostics came out of this, and both matter more than the requests.**

The home page was **last crawled on 19 August 2026**. Crawl allowed: yes. Fetch:
successful. Indexing allowed: yes. Nothing is technically blocking it. Google fetched
it and declined. Its only 参照元ページ is `sitemap.xml` — no page anywhere, inside or
outside the site, is recorded as linking to it.

Live URL inspection disagrees with the index report. The report files 35 pages as
"検出 - インデックス未登録", but inspecting them one by one returns
"**URL が Google に認識されていません**" for most of them — not merely uncrawled but
unknown. `magic-crossover` and `calendar` did come back as "検出", so it is not uniform.
The report is a periodic snapshot and inspection is live, so inspection is the truer
read, and it is worse than the report says.

Requesting indexing does not fix any of this. It forces a crawl; whether Google lists
the page is still Google's decision, and it has already crawled and declined seven.

**The sitemap was five pages short, found on 26 October.** It had 47 URLs against 52 published
pages. Missing: `2026-10-21-card-changes-october.html`, `2026-10-24-week-four.html`,
`2026-10-25-raid-talk.html`, `2026-10-26-raid-chart.html` — and **`2026-08-18-lionel-krone.html`,
which holds the best average position on the site at 3.7** and had never been in it at all.
All five added the same day.

The sitemap is the home page's only recorded 参照元ページ, so it is the one discovery route this
site controls, and nothing was checking it. **Add the entry in the same commit as the article**, and
run a published-pages-against-sitemap diff when touching it: the check is a set difference, not
reading the file.

### 4. Week five meta article — due 29 Oct

Week four shipped on 24 October as `2026-10-24-week-four.html`, two days late. `DRAFT-week-four.md`
is gone with it; the reusable publish-day order is now in `EDITORIAL.md`.

**Week five is 22–28 October, and it is the first week under the changed card.** Two things
make it awkward and both have to be said on the page:

- **22 October is not a whole day.** The game was down from 23:15 on the 21st until 16:00 on the
  22nd, so that day is about eight hours of play. Its chart is published.
- **23 October is the first full day under the new text.** Its chart publishes on the morning of
  the 24th.

Do not read the first days after the change as the change working or not working. The standing
example is in the week four piece: Jokers went 26.5, 14.3, 22.7, 20.8 across four days with nothing
altered in the game.

**State on 28 October, 16:30: six of the seven days are read.** Only the 28th is missing and its
chart publishes on the morning of the 29th, which is the due date. **The 27th changes the shape of
the week**: `赤白轟轟轟(レイド無し)` reads **22.7 and leads outright for the first time**, a series
high against 16.6 on the 25th — but on **110 games**, where only 46 and 84 are smaller among the
full reads and 110 ties 20 October exactly. Nine decks are named plus the bucket, which is the
series minimum and a five-way tie, so write "as few as the chart has ever named", never "the
fewest since". Do not let the 22.7 carry the piece on its own.

**Earlier state, 27 October, 23:00: five of the seven days were read.** The 27th's chart publishes on the
morning of the 28th and the 28th's on the morning of the 29th, so **this cannot be written before
the 29th** — and `EDITORIAL.md` says in as many words not to publish a short week, because week
four's seventh day changed two of its findings and its headline.

What the five read days look like, as a starting point and not as findings:

| | 22 Oct | 23 Oct | 24 Oct | 25 Oct | 26 Oct |
|---|---|---|---|---|---|
| Games | 46 | 227 | 146 | 290 | 309 |
| Slices | 19 | 11 | 13 | 14 | 12 |
| Leader | `バラギアラループ` | `ジョーカーズ` | `ジョーカーズ` | tie | `ジョーカーズ` |

and the 27th, read on the 28th: **110 games, 10 slices, leader `赤白轟轟轟(レイド無し)` at 22.7**.

**A third caveat for the page, on top of the two above.** The 22nd has **nineteen named slices and
no unnamed bucket at all**, against eleven to fourteen on every other day of the week. At 46 games
the survey labelled everything, so that day's figures are not comparable to the rest on slice count
or on bucket size, and **a week-wide statement about the bucket has to say so**. The sum check
already treats it as the documented rounding exception at 99.6.

`ジョーカーズ` led or tied the first four days since the change and then did not: on the 27th it is
second at 16.4. **That run is over before the week is, which is the reason not to write a week from
five days of it.** Write the leader column from the finished week.

**Three of its seven days are already written up** on `2026-10-26-raid-chart.html`, so week five
should not re-argue them. What that page established and the week page can lean on: the red/white
pair's floor ran 10.7–27.7 over the twenty-one full days before the change and reads 11.9, 11.6,
16.6 since; the 12.3-point rise is smaller than two swings in the series that happened with nothing
altered; and `赤白レイド` is the only one of the eight long-run decks missing from the last three
charts. **Recompute all of it against the finished week** — the 26th, 27th and 28th are not in any
of those figures, and the publish-day order in `EDITORIAL.md` exists because the last day has twice
changed a finding.

### 5. The balance change: written, and the trigger closed

**Published 26 October: `2026-10-26-raid-chart.html`** — the data side, which was owed from the 24th.
The trigger set on the 24th held on all three days: `赤白レイド` unnamed on the 23rd, 24th and 25th, and
`赤白轟轟轟(レイド無し)` at 11.9, 11.6 and 16.6, tied for first on the 25th at 290 games. It links to
`2026-10-25-raid-talk.html` for the player side rather than repeating it, and it reaches **no verdict on
the change** — the notice says balance adjustment and names no deck, so there is no stated intent to
measure against.

**Three findings in it that were not in the dated notes**, and they are the reason it was worth a page:

- **The colours did not leave; one of their two builds replaced the other.** Adding the two red/white
  columns, the pair's floor ran 10.7–27.7 across the twenty-one full days before the change, averaging
  about 18. Since the change: 11.9, 11.6, 16.6 — all three inside the old range, in its lower half.
- **The size of the move is ordinary for this survey.** 4.3 → 16.6 is 12.3 points. The two widest
  three-day swings in the series are larger and both happened with nothing altered: Raid itself
  24.1 → 8.3 (15.8) on 17–19 October, and Jokers 10.8 → 26.5 (15.7) on 16–18 October. **The timing is
  the finding, not the magnitude.**
- **No superlative about the length of the run survives.** Six decks are named on all twenty-five
  full-read days and are still going; `青魔導具` has missed one. Raid is on 22 of 25 and is **the only
  one of the eight long-run decks absent from the last three charts** — that is the defensible sentence,
  and "the longest run in the series" would have been false.

**One error was corrected the same morning it was published.** The 26 October note on the card-change
page said `赤白轟轟轟(レイド無し)` had a best of "4.3 on the nine days it appeared **before the change**".
The 4.3 is 22 October, which is **after** it — play resumed at 16:00 that day under the new text, as the
same page says two paragraphs lower. Eight of the nine are before the change and their ceiling is 3.6.
The 4.3 is also two games on a 46-game day against 3.6 being six games out of 166. Corrected with a dated
note on the card-change page, in `data-nd-daily.json`, and in a correction box on the new page.
`2026-10-25-raid-talk.html` and this file said "previous best", which was true, and were left alone.

**Still not claimable, and the page says each one:** that the change caused this (the collaboration set,
the deck builders and the Legend Battle all opened the same afternoon, and the deck-builder pool changed
at the same maintenance); that "not a named slice" means zero (the ceiling is read off each chart's own
smallest label — 2.6, 2.1, 2.1 — and the survey's labelling rule is not published); that the survey
follows players rather than counting decks met.

**Before writing anything further about the card, read the whole card.** The September
`2026-09-12-b-reishu-raid.html` had to be corrected because its abilities were read one line at a time and
the protection was missed. The 21 October change page makes the same point about the new wording: the
protection clause lost its subject, and that reading is this site's, not the publisher's. **It has still
not been checked in the running game.**

### 6. Cloudflare Web Analytics
Needs a token from the author. Worth doing **after** item 1, not before — there is
currently nothing to measure.

---

## 29 October: two rules replaced by two mechanisms

The three cross-file rules written earlier the same day asked a person to remember to open files
they were not writing. Two of them are gone, replaced by things that run:

- **`python3 check.py --prose`** prints the prose that changed in every edited `.html` and `.md`
  file, tags gone and one sentence per line, with the file list from `git`, and names the edited
  files that have no prose. Use it before the prose pass.
- **`<q cite="FILE.html">...</q>`** is now how this site quotes another of its pages, and
  `check.py` requires the quoted words to appear verbatim in that file. Its first run failed on
  **both** quotations already published on the week five page. `EDITORIAL.md` has the case.

`check.py` also now reads the stated `--selftest` count back out of `CLAUDE.md`, `EDITORIAL.md`
**and its own docstring** — the docstring was left out of the first version of that check and was
already stale when it was written. The count is **39**, and nothing about it is a person's job.

## One September re-read settles two open items at once

Found on 29 October while working through both separately. **They are the same job.**

- The six `赤単バルガ` warnings and the two `青黒魔導具` warnings on
  `2026-09-27-first-numbers.html` are all cells for **24-29 September**, days the record holds as
  `tracked` -- the six columns this site followed at the time, plus the leader. The page published
  figures that were read off those charts and never written into the record, so `check.py` has
  nothing to compare them against and says so eight times.
- `ジョラゴンジョーカーズ` needs the **24-26 September** labels re-read to find out whether the
  survey used that name on those days, as `data-deck-names.json` says it did until the 27th.

So: **re-read 24-29 September in full and promote those six days from `tracked` to `full`.** That
answers both -- the eight cells become comparable, and the Jokers label either is or is not on the
24th to 26th. It is chart work, which is the expensive and error-prone kind, which is why it sits
here as a decision rather than being done quietly.

**What it costs, honestly.** Six charts read by hand at 1700px or better, every slice, each day
reconciled to 100.0 or reconstructed by game count. That is the work that has produced this site's
worst errors. **And it may not settle the Jokers name**: a label too small to resolve stays
unresolved, which is already the case for `（判読不能）の紋章` on three October days.

**The alternative is to close both as deliberate.** Record the eight cells in
`known_convention_differences` as "page read the full chart, the record tracked six columns", and
mark the `ジョラゴンジョーカーズ` note as unverifiable without a re-read. That costs nothing, keeps
the record honest, and leaves the warnings count at 15 forever. **Neither option is wrong; they
cost different things.** Nothing is blocked either way: no published page uses the Jokers name, and
the 赤単バルガ figures are already published and were read from the charts.

---

## `check.py`: what it still cannot compare, and one hole it found in the data

Audited on 26 October by an agent that had not written it. The audit's findings are fixed;
these are the ones left standing on purpose, and `python3 check.py` names each of them as a
warning on every run. **15 warnings is the expected count.** If it changes, read why.

**The hole in the record.** `2026-09-27-first-numbers.html` publishes `赤単バルガ` figures for
24–29 September — **8.5, 11.7, 10.5, 7.0, 11.6, 6.5** — and `data-nd-daily.json` does not hold
them, because those seven days are six-column `tracked` reads. The page is not wrong; the record
is short. Folding them in would make those days seven-column reads, which breaks the stated
`tracked` convention and the check that enforces it, so **this is a decision, not a chore**:
either widen the convention and say so in the file, or leave the gap and leave the warning.
The same applies to `青黒魔導具`, which that page also carries for two of those days.

**Dates outside the record.** `2026-09-13-grand-prix-result.html` (21 Sep) and
`2026-09-14-meta-shift.html` (5, 13, 23 Sep) carry survey figures from before 24 September,
which is where the record starts. Nothing to fix unless the record is ever extended backwards.

**One prose cell.** `2026-10-13-dragerion-talk.html` writes a leader cell as "see below". Correct
for a reader, not comparable by a script.

**Untested assertion sites.** `--selftest` covers 34 cases and the file has about 50 assertion
sites, so roughly a third are unmutated — they work, and were verified by hand once, but a future
edit could break one without the selftest noticing. **Add the mutation in the same commit as the
check** is the rule in `EDITORIAL.md`; this backlog is what ignoring it looks like.

---

## Two deck-name questions `check.py` raised, 26 October

Both are in `data-deck-names.json` marked as the **survey's** own names, and neither is on any
chart in `data-nd-daily.json`. Annotated there rather than changed, because changing either
would be a guess about which source said it.

- **`ジョラゴンジョーカーズ`** — its note says it was the survey's name until 27 September. The
  record starts 24 September and carries `ジョーカーズ` from that day, so **the 24-26 September
  rows should carry the old name if the note is right.** Those three days are partial
  six-column reads. Resolve by re-reading those three charts, not by editing either file.
- **`自然ジョーカーズ`** — no note saying when the survey used it, and it is on no chart. It may
  be a players' name recorded as the survey's.

Neither blocks anything: no published page uses either name. This site has twice published a
wrong count of one deck's names, which is why the file exists, so leave them visible.

---

## Uncovered, found on the news index

**`news/16522`, 23 October: 「11月度公認大会開催！」** — November's official tournaments. Found during
the pre-push source check on 26 October and **it is nowhere on this site**: not the calendar, not this
file. It is the newest item on the news index, so nothing has been published since it.

Probably a calendar entry rather than an article, and the monthly series before it was never covered
either, which is its own gap. **Read the notice before deciding** — the September equivalent is not on
the calendar, so there is no precedent here to copy.

---

## Worth writing, not written

| Piece | Why | Lifespan |
|---|---|---|
| Battle Arena explained | Every card is rented, entry is free, and it is invisible from outside Japan | Long |
| The two English discontinuations | 2006 and 2014, and what happened between | Permanent |
| PLAY'S balance-change history | Separate from the paper Hall of Fame, which is already written | Long |

---

## Standing rules

**Fact-check before publishing and again after.** The old rule said two passes. On the
13 October community article it took four, and **every one of them found something** — a
misread season name, a head/body count mismatch, a mistranslation of `〜ぶり`, and a deck
name in common use that this site had missed while publishing two pages that counted
deck names. Do not skip a pass because the last one was clean.

**"All N days" claims: count them.** Twice in two days a sum-check statement was published with
the wrong N — "all twenty-one days sum to 100.0" when only the fourteen full-read days do, the
seven tracked days being partial by design. Write the number the checker printed, not the number
of rows in the file.

**Run the sum check across the whole series, not the week being written.** Confining it to the
current window hid two short days for a fortnight.

**Compare description slots after decoding HTML entities.** `&#39;` in a meta attribute and `'`
in JSON-LD are the same string; a checker that compares them raw reports false mismatches.

**Recompute from the published table, not from the sentence.** Superlatives are where
the errors are, and they have to be checked against the whole series rather than the
window the article covers.

**All four description slots.** `meta`, `og`, `twitter`, JSON-LD. Checking fewer has
shipped stale text twice.

**Check every official page, not one.** The Heroes Set article was rewritten *incorrectly*
because a sale-day notice omits its own contents and points back to an advance notice.

**Copy Japanese, never retype it.** 課 for 誣 turned a card's name into a different word.

**A hashtag is not membership.**

**X announces, the news index documents — sometimes days later, sometimes never.** Say which
it is, and **measure the lag rather than assuming it**. The Railgun collaboration was revealed
on 23 August and had its first notice on 25 August, two days later, ending with four notices
including an overview that gave the deck builder contents. The seventh にじさんじ collaboration
was revealed on 12 October, got its first notice on **19 October — seven days** — and the three
detail notices on **20 October at 17:00**, two days before it opens. The ranked season that started
16 October did get a page; the one before it never did. The streamer event of 12 October still has
no page at all.

**Measured, now closed: two days (Railgun), seven (this one), never (the streamer event).** The
product codes did arrive as text in the deck-builder notice, and reading them off box art had
produced a wrong one.

---

## Calendar

**Do not keep a second copy here.** This section used to duplicate
`2026-08-16-calendar.html` and went stale: on 18 October it still showed the
にじさんじ collaboration and the `電脳対戦` pack as one `TBC` row, three days after
both were dated and separated on the real calendar, and it was missing the new
ranked season, DM26-EX5 and DM26-BD1 entirely.

`2026-08-16-calendar.html` is the calendar — 29 entries, no TBC rows. Read it
there.

The two dates worth carrying in your head: **22 October**, when the collaboration
opens, and the **November regular set plus the 7th anniversary set**, which is the
next thing that changes what is legal in New Division underneath every meta page.
Neither anniversary-set date is announced.
