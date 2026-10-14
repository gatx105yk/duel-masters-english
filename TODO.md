# Where things stand

Updated 13 Oct 2026.

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

### 2. Indexing requests — continue tomorrow

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

### 3. Week three meta article — due 15 Oct
Covers 8–14 October. Eight through twelve are already read and in `data-nd-daily.json`;
13 and 14 publish the following mornings. The ranked season ends 15 Oct 23:59, so the last
days of the window may show a rush.

The week does not have a single leader: 8 and 9 October went to 赤白レイド, 10 October to
HADESドラゲリオン, 11 October was a tie between HADESドラゲリオン and バラギアラループ, and
12 October to コットンゼニス. Four different answers in five days, against one deck leading
six of seven the week before — do not reuse last week's framing.

### 4. Cloudflare Web Analytics
Needs a token from the author. Worth doing **after** item 1, not before — there is
currently nothing to measure.

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

**Recompute from the published table, not from the sentence.** Superlatives are where
the errors are, and they have to be checked against the whole series rather than the
window the article covers.

**All four description slots.** `meta`, `og`, `twitter`, JSON-LD. Checking fewer has
shipped stale text twice.

**Check every official page, not one.** The Heroes Set article was rewritten *incorrectly*
because a sale-day notice omits its own contents and points back to an advance notice.

**Copy Japanese, never retype it.** 課 for 誣 turned a card's name into a different word.

**A hashtag is not membership.**

**X announces, the news index documents — sometimes days later, sometimes never.** As of
13 October the streamer event, the seventh collaboration and the ranked season name are all
X-only. Say which it is.

---

## Calendar

| Date | What |
|---|---|
| **15 Oct** | Ranked season `HADES・ドラゲリオンカップ` ends, 23:59 |
| 16–17 Oct | Minogami Cup FINAL STAGE |
| 17 Oct | DM26-EX4 Dueking FOREVER 2026 (paper) |
| 21 Oct | Legend Battle ends, 23:59 |
| 26–31 Oct | BATTLE ARENA 2026 AUTUMN, qualifier 1 |
| 8 Nov | Qualifier 2 |
| 21 Nov | Finals |
| TBC | にじさんじ collaboration 7th, and the `電脳対戦 -WAR OF PLAY'S-` pack |
| Nov–Dec | PLAY'S regular set, then the anniversary set — which resets what is ND legal |

The anniversary set is the next thing that changes the format underneath every meta page.
