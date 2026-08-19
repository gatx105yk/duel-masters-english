# Duel Masters watch — scheduled task

A collection routine, run daily. It **collects and reports**. It does not write articles and does not
judge anything.

---

## The instruction

```
Duel Masters / Duel Masters PLAY'S — daily collection run.

Report only. Do not draft an article. Do not evaluate cards, decks or news.

=== SOURCES, in this order ===

1. https://dmps.takaratomy.co.jp/news/
   List every item published since the last run. For each: date, title, URL.
   Open any item whose title mentions a set, a card, a regulation change,
   an event, or a balance adjustment, and copy the relevant lines verbatim.

2. https://dm.takaratomy.co.jp/
   Same treatment. Always check
   https://dm.takaratomy.co.jp/rule/regulation/ regardless of whether the
   front page mentions it — Hall of Fame changes are announced there first.

3. https://x.com/dmps_info
4. https://x.com/t2duema
   For each post since the last run, record:
     - timestamp
     - the post text, copied exactly, in Japanese
     - any card names in 《》, copied exactly, character for character
     - repost count, like count, view count
     - the post URL

=== HARD RULES ===

- Copy Japanese text. Never retype it. A card name transcribed by hand is a
  card name with a wrong kanji in it.
- Do not infer which set a card belongs to. If a post carries a hashtag,
  record the hashtag. Do not conclude anything from it.
- Do not translate. Report the Japanese as-is.
- If a fact appears on X but not on the official site, say so explicitly:
  "X only, not on the official site as of <time>".
- If a page fails to load, say so. Never fill a gap with a guess.
- No adjectives. "A card was revealed" — not "an exciting new card".

=== COMMUNITY VOLUME ===

Search X for デュエプレ and デュエマ, last 24 hours, top posts.

Report only the shape of the response:
  - roughly how many posts mention a given card or topic
  - the highest view count seen on any single post about it
  - whether the posts come from many separate accounts or a few

Do NOT quote individual users. Do NOT name accounts other than the two
official ones. Do NOT characterise sentiment as positive or negative —
report volume, not mood.

=== OUTPUT FORMAT ===

## Since last run
(one line per item, or "nothing new")

## Official site — PLAY'S
date | title | URL
verbatim excerpt of anything substantive

## Official site — paper TCG
same

## Hall of Fame page
"unchanged" or the full diff

## Official X posts
timestamp | JP text | card names | RP / likes / views | URL

## Community volume
topic | approx post count | peak views | many accounts or few

## Flagged for a human
Anything that looks like it might matter, with no explanation of why.
Just the item and where it came from.
```

---

## Why it is shaped this way

Three errors in one article, all in the interpretation layer:

| Error | Cause |
|---|---|
| Assigned a card to the wrong set | Inferred set membership from a shared hashtag |
| Wrong kanji in a card name | Retyped instead of copied |
| Attributed wiki data to an official notice | Merged two sources |

None of those are possible if the task only copies and never concludes. Anything the collector
cannot do without reasoning is left for a person.

## What stays manual

Deciding whether something is worth an article. Working out what a change means. Writing. All of it.

The collector answers "what happened". A person answers "so what".
