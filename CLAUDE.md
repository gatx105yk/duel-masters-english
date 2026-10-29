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
| `check.py` | **before every publish.** `python3 check.py`. Its docstring lists what it cannot catch |

## Publishing

**Commit and push normally.** The Claude GitHub App was installed for this repository on
13 October 2026, so `git push` works. Edit files on disk, commit, push.

Before replacing text in a file, **count how many times the anchor string occurs.** Strings
that look unique often are not, and a silent second match corrupts the file.

**A new article means a `sitemap.xml` entry in the same commit.** The sitemap is the home page's only
recorded referrer, and on 26 October it was five pages short — including the page with the best
average position on the site. Diff published pages against the sitemap both ways; reading the file does
not catch an absence.

### If push ever returns 403 again

The app installation has lapsed. Reinstall it at
https://github.com/apps/claude/installations/select_target, or reconnect GitHub from
claude.ai settings. Until then the fallback is driving the GitHub web editor with
JavaScript against CodeMirror, committing in two steps — and that route has caused real
damage twice: a commit made while the renderer was frozen wrote an **empty file**, and a
frozen tab silently dropped two commits. On that route, never assume a commit landed;
confirm the byte count with `git fetch` every time.

## Before anything is published

**Run `python3 check.py` first.** It takes a quarter of a second and does the mechanical
half: every dated table cell against `data-nd-daily.json`, the four description slots, the
canonical/`og:url`/JSON-LD trio, tag balance, entities, the middle dot, local links, the
sitemap both ways, every `<q cite>` quotation against the page it names, and a dated correction
left sitting in an opening paragraph. Exit 0 means that half is clean and nothing more.
`python3 check.py --list` says what it does **and what it cannot do**; read that list before
trusting a clean run.

`python3 check.py --selftest` breaks the repository **39 ways** and requires each break to
produce its own message — run it after editing `check.py`. **That number is not yours to keep
right.** `check.py` reads it back out of this file, out of `EDITORIAL.md` and out of its own
docstring, and fails the run if any of the three has drifted. It was yours until 29 October and
it was wrong three times running: it said sixteen for two rewrites; the line added on 27 October
telling you to keep it right was itself stale by the 29th; and the check written that day to end
the problem left the script's own docstring out of its scan, so it sat one screen above a stale
number of its own. Add a check and the three numbers move themselves, or the run fails.

`python3 check.py --prose` prints what changed **as a reader sees it** — tags gone, one sentence
per line — in every `.html` and `.md` file this session edited, and names the edited files that
have no prose to diff. The file list comes from `git`, not from memory. Run it before the prose
pass, so the pass reaches the files you were **not** thinking about.

Then do the half it cannot.

Recompute every claim **from the table on the page**, not from the sentence you wrote.
Superlatives are where the errors are: "first", "longest", "lowest" have to be checked
against the whole series, not the window the article covers.

**And ask which side of a boundary each figure is on.** A season change or a card change splits a
window, and a figure from the wrong side of it reads as evidence. "Earlier" and "previous" are free;
**"before the change" is a dated claim and costs a check.** `EDITORIAL.md` has the case, which happened
in a dated note added to an older page rather than in an article.

Then reconcile the page against `data-nd-daily.json`. Anything that differs on purpose
belongs in that file's `known_convention_differences`, so the next person does not
"fix" it.

**Quote another page; do not characterise it.** Write it as
`<q cite="FILE.html">the exact words</q>` and `check.py` verifies those words against that file
on every run. This is not a style preference: it is the only form of a cross-page claim that
carries its own evidence, and a sentence you cannot write this way is a sentence you have not
checked. The quote marks come from `style.css`, so the markup holds nothing but the quoted words.

On 29 October three errors survived every pass run on a new page and none of them were about the
new page: two were claims about what older pages say, and one was a note that had landed inside an
older page's opening paragraph the day before. The rules written that day asked a person to
remember to open other files; **`--prose` and `<q cite>` replaced both of them the same day**,
after the quotation check found that the two quotations already on the new page were **both**
misquotations — words dropped from the middle of one and the end of the other, quote marks and
full stop intact, every numeric check passing. `EDITORIAL.md` has the case.

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

### Compare a size against the same kind of size, or do not compare it

**27 October.** A deploy was reported here as not landing. It had landed. The check was
`wc -c` on disk against the length of the fetched text, and those are **different
measurements**: `wc -c` counts bytes, a fetched string's `.length` counts characters. Every
page on this site is mostly Japanese, which is **three bytes per character in UTF-8**, so the
two never agree — the calendar is 45,805 bytes and 43,539 characters. The poll condition was
`len > 44000`, which that page can never satisfy, so it would have reported failure forever.

Two rules out of it:

- **Verify by source string, not by size.** The string test was already right and already in
  this file; it is what correctly said "not yet" at 23:00 and would have said "yes" at 23:05.
  A size is a weaker test even when the units match, because it cannot say *which* change
  landed. If a size is used anyway, compare characters with characters: in Python,
  `len(open(p, encoding='utf-8').read())`, never `wc -c`.
- **A Pages build can take longer than a few minutes.** This one finished about five minutes
  after the push, which was after the polling gave up. Before reporting a deploy as failed,
  read the `last-modified` header — it dates the build — and say what time the check was made.
  "Not deployed as of 23:03" is a claim that stays true; "not deployed" is not.

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
  slices do not sum to 100.0 was **probably** misread — but check the sample size first.
  Where each slice is a whole number of games, rounding can leave the total short: 22 October
  sums to 99.6 at 46 games and is right. Reconstruct the counts before changing anything, and
  read `known_convention_differences` in `data-nd-daily.json`. Neither check catches two labels
  swapped.
- **Do not touch `googleaf526fe342db2356.html`.** It is the Search Console ownership file.
- canonical, `og:url` and the JSON-LD url all stay on `https://duelmasters.editioncompass.com/`.

## Not done on the author's behalf

Entering credentials, 2FA codes, payment or tax details; creating accounts; accepting terms;
posting to communities as the author. Ask instead.
