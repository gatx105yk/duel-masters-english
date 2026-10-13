# Where things stand

Updated 13 Oct 2026.

---

## The one number that matters

| | |
|---|---|
| Articles live | 43, all linked from the index |
| Pages indexed by Google | **1** |
| Not indexed | 42 — 35 "discovered, not crawled", 7 "crawled, not indexed" |
| Clicks, all time | **0** |
| Impressions | 66 |
| Average position | 14.4 |

Forty-three articles, fact-checked to the point of re-reading source charts at
2000px, and Google has indexed one page. **This is not a sitemap problem and not a
quality problem.** "Discovered, not crawled" on 35 pages means no other site links
here, so Google will not spend crawl budget. Nothing written from here changes that.

---

## Next, in order

### 1. Tell someone the site exists
Still not done. It has been the top item since 20 August, and it is now the only
thing blocking everything else.

- **r/DuelMastersPlays** — ~13 posts a week, mostly install and rules questions. `how-to-play`
  and `before-you-start` were written for exactly those people
- **Duel Masters Discord**, ~3,770 members, has a `duema-news` channel
- **Fandom wiki** — one external link would do it

One is enough. One inbound link is what moves 35 pages out of "discovered, not crawled".

This has to be the author. Claude does not post to communities on anyone's behalf, and
Reddit is not reachable from its tools.

### 2. Grant write access to the repo
Everything is currently published by driving the GitHub web editor with JavaScript,
because `git push` returns 403. That has produced one empty-file commit and two
renderer freezes. The fix is one of:

- install the Claude GitHub App for this repo: https://github.com/apps/claude/installations/select_target
- or reconnect GitHub: https://claude.ai/customize/connectors?auth_start=github&auth_start_force=1

Not urgent. It removes a class of accident and a lot of time.

### 3. Week three meta article — due 15 Oct
Covers 8–14 October. Eight through twelve are already read and in `data-nd-daily.json`;
13 and 14 publish the following mornings. The ranked season ends 15 Oct 23:59, so the last
days of the window may show a rush.

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

**Copy Japanese, never retype it.** 課 for 語 turned a card's name into a different word.

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
