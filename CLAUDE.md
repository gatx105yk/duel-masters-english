# Start here

English coverage of **Duel Masters PLAY'S**, translated from Japanese sources.
Static HTML on GitHub Pages at duelmasters.editioncompass.com. One author.

This file is the door. The detail lives in the files below — read the ones the
task touches **before** starting, not after something goes wrong.

| File | Read it when |
|---|---|
| `EDITORIAL.md` | writing anything. How each kind of article has to be written, and what cannot be claimed |
| `ARTICLE-QUEUE.md` | deciding whether something is worth covering, and in what order |
| `WATCH-TASK.md` | checking for news. Which sources, in which order, and what each one cannot tell you |
| `DATA.md` | touching any number. Points at the two data files |
| `TODO.md` | picking up work. The author's own list; it can lag behind what has actually shipped |

## Publishing

**Commit and push normally.** The Claude GitHub App was installed for this repository on
13 October 2026, so `git push` works. Edit files on disk, commit, push.

Before replacing text in a file, **count how many times the anchor string occurs.** Strings
that look unique often are not, and a silent second match corrupts the file.

### If push ever returns 403 again

The app installation has lapsed. Reinstall it at
https://github.com/apps/claude/installations/select_target, or reconnect GitHub from
claude.ai settings. Until then the fallback is driving the GitHub web editor with
JavaScript against CodeMirror, committing in two steps — and that route has caused real
damage twice: a commit made while the renderer was frozen wrote an **empty file**, and a
frozen tab silently dropped two commits. On that route, never assume a commit landed;
confirm the byte count with `git fetch` every time.

## Before anything is published

Recompute every claim **from the table on the page**, not from the sentence you wrote.
Superlatives are where the errors are: "first", "longest", "lowest" have to be checked
against the whole series, not the window the article covers.

Then reconcile the page against `data-nd-daily.json`. Anything that differs on purpose
belongs in that file's `known_convention_differences`, so the next person does not
"fix" it.

**Check all four description slots agree**: `meta name=description`, `og:description`,
`twitter:description`, and the JSON-LD `description`. Checking fewer has shipped stale
text more than once.

**Re-check the sources in the last minutes, not just the article.** Checking the page against what
you gathered cannot catch a notice that went up while you were writing. The publisher posts at
**17:00 JST**. Never assert that something has not appeared at a time later than you actually
looked. `EDITORIAL.md` has the case that made this a rule.

Fact-check again **after** publishing. On this site that pass keeps finding things.

### Verify a deploy from a fresh fetch, never from the rendered page

The browser is not a witness. It has bitten twice:

- **It auto-translates.** The page renders in Japanese, so the words on screen are Google's, not
  the file's. A card name once looked corrupted on screen and was correct in the source.
- **It renders from cache.** On 21 October a corrected caption showed its pre-correction wording
  in the tab while the live file already had the fix — one more step and that would have been
  reported as a regression that never happened.

So confirm a deploy with `fetch(url, {cache:'reload'})` and a cache-busting parameter, and read
the **source string**. Use the rendered page only for what the source cannot show: layout, whether
a block renders at all, whether an image loads.

## Corrections are dated and say what was wrong

The publisher edits its own notices in place with no archive, and this site has made a
point of not doing that. When something here is wrong, add a dated note that says what
it said before. Do not quietly edit.

## Lines that do not move

- Community reaction is reported as **what was said**. It never becomes fact.
- **Never write from inference.** "Not stated" is not "does not exist". Two things announced
  in one broadcast are not one thing.
- Never reproduce another site's assembled work — tier tables, rankings, decklists,
  aggregates. A few facts with attribution is fine. This applies to the data files too:
  they are working notes, not something to publish as a table.
- Card and deck names come from the community translation patch. Effects are translated here.
- The survey publishes as images. Every figure was read off a chart by hand, so a day whose
  slices do not sum to 100.0 was **probably** misread &mdash; but check the sample size first.
  Where each slice is a whole number of games, rounding can leave the total short: 22 October
  sums to 99.6 at 46 games and is right. Reconstruct the counts before changing anything, and
  read `known_convention_differences` in `data-nd-daily.json`. Neither check catches two labels
  swapped.
- **Do not touch `googleaf526fe342db2356.html`.** It is the Search Console ownership file.
- canonical, `og:url` and the JSON-LD url all stay on `https://duelmasters.editioncompass.com/`.

## Not done on the author's behalf

Entering credentials, 2FA codes, payment or tax details; creating accounts; accepting terms;
posting to communities as the author. Ask instead.
