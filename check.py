#!/usr/bin/env python3
"""Pre-publish checks for Duel Masters English.

Run from the repository root:

    python3 check.py              # everything
    python3 check.py FILE...      # only these pages, plus the file checks
    python3 check.py --list       # the list of checks, and nothing else
    python3 check.py --selftest   # break the repo 34 ways; each must be caught

Exit status is 0 only when no FAIL is reported. WARN never fails the run; it
marks something a person should read. In particular **every dated table cell
this script could not compare is a WARN**, so a gap in coverage is visible
instead of looking like a pass.

Why this exists
---------------
Every check is here because the mistake it looks for has shipped on this site.
`EDITORIAL.md` has the cases. The mechanical half of a fact-check pass costs
nothing to repeat, so the passes a person runs can go on the half a script
cannot do: reading the page as prose, and re-fetching the sources.

What it checks
--------------
Per page (52 of them):
  * all four description slots present, non-empty and identical
  * og:title and twitter:title agree; <title> non-empty; an h1 exists
  * canonical, og:url and the JSON-LD url all present, all on the live host,
    all pointing at this file
  * the JSON-LD block parses
  * open/close counts balance for 24 tags
  * no malformed HTML entities
  * no U+00B7 standing in for U+30FB, tested on the decoded text
  * no Japanese left outside a <span class="jp"> that is not in the baseline
  * every local link resolves, fragment and query stripped first
  * every dated table cell against `data-nd-daily.json`: deck shares, family
    totals, the games column, the leader name and the leader's share, in
    normal and transposed orientation, with or without a <thead>

Per data file:
  * `data-nd-daily.json` parses and has the shape the rest of this assumes
  * no gaps in the day series; every field typed and in range
  * every full day sums to 100.0, except a documented rounding exception,
    which is checked against its own recorded total AND by reconstructing the
    game counts
  * a `tracked` day cannot hold more slices than the convention allows, so
    relabelling one word cannot switch the sum check off
  * the leader fields recomputed from the entries, ties included
  * `data-deck-names.json` parses; ids unique; no chart label owned by two
    decks; every survey name either in the record or documented as absent

Per repository:
  * sitemap well-formed, no duplicates, and the set difference BOTH ways
    against the published pages
  * no HTML entities outside code spans in any markdown file
  * the Search Console ownership file and the other load-bearing files present

Measured against this site's own history, it would have caught
--------------------------------------------------------------
  * a deck percentage edited on a page and not in the data file, or the
    reverse, in any dated table it can parse — and it now says so about the
    ones it cannot, which it did not when first written: an audit found 117 of
    293 comparable cells and a whole transposed table of 54 going unchecked in
    silence. Coverage is printed as a number for that reason.
  * the duplicated `</article>` on four October pages, which it found on its
    first run.
  * `&middot;` standing in for U+30FB — but only since 26 October. On the
    first run this check read the raw file, so it passed that page clean while
    the bug was in it; a hand grep found it.
  * a description slot left stale, empty, or missing.
  * the five pages missing from `sitemap.xml`.
  * two labels swapped in the data file, *when their values differ* — the
    recomputed leader field catches it, and so does any page carrying either
    column. Swap two labels whose values are equal and nothing here notices.

And it would have caught NONE of these, which are the expensive ones
--------------------------------------------------------------------
  * "week four: Red Balga's low was 4.8" when the table says 3.6, or "four
    days apart" when it was two, or "all three fall inside the range" when the
    range quoted spans a boundary the page itself fenced off. Prose derived
    from a table is not comparable to a stored figure. **Superlatives are
    recomputed by hand against the whole series, every time.**
  * a figure attributed to the wrong side of a boundary. Which side of a date
    a number belongs on is a claim about dates, and nothing here knows what a
    boundary is.
  * a floor read as a total. On 26 October this script passed a page whose
    headline finding did not follow from its own data.
  * a card attributed to the wrong person, or a notice asserted not to exist
    an hour after it went up. Those are facts about the world.
  * a chart misread. Everything here is consistency with `data-nd-daily.json`,
    never truth; the chart is read by a person.

So this replaces the mechanical part of a fact-check pass and no part of the
judgement. A clean run means the passes a person spends are spent on reading
and on the sources, not that the page is right. On 26 October a clean run and
six wrong sentences were the same page.
"""

from __future__ import annotations

import datetime as dt
import html
import json
import os
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET

HOST = "https://duelmasters.editioncompass.com/"
DAILY = "data-nd-daily.json"
NAMES = "data-deck-names.json"
SITEMAP = "sitemap.xml"

# Site-wide tallies, so a coverage collapse is a number that moves.
TOTALS: dict[str, int] = {}
BASELINE = "check-baseline.json"

# Returned by read() instead of raising. No real file starts with this.
UNREADABLE = "\x00UNREADABLE\x00"

# A selftest anchor meaning "remove this file entirely".
DELETE_FILE = "\x00DELETE\x00"

# Pages that are not articles and are exempt from the per-page structure checks.
NOT_PAGES = {"404.html", "googleaf526fe342db2356.html"}
# The Search Console ownership file. CLAUDE.md: do not touch it.
OWNERSHIP = "googleaf526fe342db2356.html"

TAGS = ["div", "p", "table", "tbody", "thead", "tr", "ul", "ol", "li",
        "article", "main", "section", "h1", "h2", "h3", "span", "strong",
        "em", "b", "a", "blockquote", "footer", "header"]

ENTITIES = ("amp lt gt quot apos mdash ndash rsquo lsquo ldquo rdquo middot "
            "copy larr rarr uarr darr nbsp hellip deg times eacute minus "
            "dagger Dagger sect para bull prime Prime frac12 plusmn ne le ge "
            "trade reg").split()

# Column headers that are computed on the page rather than stored, so there is
# nothing in the data file to compare them against.
# Columns computed on the page from figures that ARE stored, so there is
# nothing single to compare them against.
DERIVED_HEADERS = {"pair", "red/white pair", "spread", "names that led",
                   "week"}

MONTHS = {m: i for i, m in enumerate(
    "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), 1)}


class Report:
    def __init__(self) -> None:
        self.fails: list[str] = []
        self.warns: list[str] = []
        self.passes = 0
        self.groups: list[str] = []

    def group(self, name: str) -> None:
        self.groups.append(name)
        print(f"\n\033[1m{name}\033[0m")

    def ok(self, cond: bool, msg: str, warn_only: bool = False) -> bool:
        if cond:
            self.passes += 1
            return True
        where = self.groups[-1] if self.groups else "?"
        if warn_only:
            self.warns.append(f"{where}: {msg}")
            print(f"  WARN  {msg}")
        else:
            self.fails.append(f"{where}: {msg}")
            print(f"  FAIL  {msg}")
        return False

    def note(self, msg: str) -> None:
        print(f"        {msg}")

    def summary(self) -> int:
        print()
        print("=" * 72)
        print(f"{self.passes} checks passed, "
              f"{len(self.fails)} failed, {len(self.warns)} warnings")
        if self.fails:
            print("\nFAILURES")
            for f in self.fails:
                print(f"  - {f}")
        if self.warns:
            print("\nWARNINGS (do not fail the run; look at each one)")
            for w in self.warns:
                print(f"  - {w}")
        if not self.fails:
            print("\nThe mechanical half is clean. Three things remain and none "
                  "of them are in here:")
            print("  1. Recompute every superlative against the whole series.")
            print("  2. Read the page end to end as prose.")
            print("  3. Re-fetch the sources. The publisher posts at 17:00 JST.")
        print("=" * 72)
        return 1 if self.fails else 0


# ---------------------------------------------------------------- helpers

def read(path: str) -> str:
    """Read a file as text. Never raises: a validator that crashes on bad
    input is worse than one that reports, so a missing or non-UTF-8 file comes
    back as a marker the caller checks."""
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return UNREADABLE + " (no such file)"
    except UnicodeDecodeError as exc:
        return UNREADABLE + f" (not valid UTF-8: {exc})"
    except OSError as exc:
        return UNREADABLE + f" ({exc})"


def strip_tags(s: str) -> str:
    # A space, not nothing: `<th>Red/white<br>pair</th>` must not become
    # `red/whitepair`, which silently stopped a column being compared.
    return re.sub(r"<[^>]+>", " ", s)


def cell_text(s: str) -> str:
    return html.unescape(strip_tags(s)).strip()


def meta(s: str, pattern: str) -> str | None:
    m = re.search(pattern, s)
    return html.unescape(m.group(1)) if m else None


def jsonld(s: str) -> dict | None:
    m = re.search(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>',
                  s, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def page_year(path: str) -> int | None:
    m = re.match(r"(\d{4})-\d{2}-\d{2}-", os.path.basename(path))
    return int(m.group(1)) if m else None


def looks_like_a_day(text: str) -> bool:
    """Whether a first cell is shaped like one of this site's date cells."""
    return bool(re.fullmatch(r"\d{1,2}\s+[A-Za-z]{3}\w*", text.strip()))


def parse_day(text: str, year: int | None) -> str | None:
    """'19 Oct' -> '2026-10-19'. None when the cell is not a date, or when no
    year could be inferred — the caller reports that case rather than skipping
    it, because a skipped row is indistinguishable from a checked one."""
    m = re.fullmatch(r"(\d{1,2})\s+([A-Z][a-z]{2})\w*", text.strip())
    if not m or year is None:
        return None
    mon = MONTHS.get(m.group(2))
    if not mon:
        return None
    return f"{year:04d}-{mon:02d}-{int(m.group(1)):02d}"


# ------------------------------------------------------- the daily dataset

def check_daily(r: Report) -> dict:
    r.group(f"{DAILY} — the record every page is checked against")
    raw = read(DAILY)
    if raw.startswith(UNREADABLE):
        r.ok(False, f"could not be read: {raw[len(UNREADABLE):].strip()}")
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        r.ok(False, f"does not parse: {exc}")
        return {}
    r.ok(True, "parses")

    days = data.get("days")
    if not isinstance(days, dict) or not days:
        r.ok(False, "has a non-empty 'days' object")
        return {}
    bad_shape = [d for d, x in days.items() if not isinstance(x, dict)
                 or not isinstance(x.get("entries"), dict)]
    if not r.ok(not bad_shape, f"every day is an object with entries "
                               f"({bad_shape[:3]})"):
        return {}
    dates = sorted(days)
    r.note(f"{len(days)} days, {dates[0]} to {dates[-1]}")

    # No gaps. A missing day is a day nobody read, and it should be visible.
    want = []
    d0, d1 = dt.date.fromisoformat(dates[0]), dt.date.fromisoformat(dates[-1])
    while d0 <= d1:
        want.append(d0.isoformat())
        d0 += dt.timedelta(days=1)
    missing = [d for d in want if d not in days]
    r.ok(not missing, f"no gaps in the series (missing: {missing})")

    diffs = data.get("known_convention_differences", [])
    sum_exempt = {d["day"] for d in diffs if d.get("column") == "(all)"}

    full = [d for d in dates if days[d]["completeness"] == "full"]
    r.note(f"{len(full)} full reads, {len(dates) - len(full)} partial")

    # The widest `tracked` day on record carries seven slices, because
    # `tracked` means the six columns this site followed at the time plus the
    # leader. Without this, relabelling one word turns the sum check off for
    # that day — which is the check CLAUDE.md calls the one that matters.
    TRACKED_MAX = 7

    for d in dates:
        x = days[d]
        r.ok(x.get("completeness") in ("full", "tracked"),
             f"{d}: completeness is full or tracked (got "
             f"{x.get('completeness')!r})")
        if x.get("completeness") == "tracked":
            r.ok(len(x["entries"]) <= TRACKED_MAX,
                 f"{d}: a tracked day has at most {TRACKED_MAX} slices, so a "
                 f"full day cannot be relabelled to escape the sum check "
                 f"(has {len(x['entries'])})")
        g = x.get("games")
        r.ok(isinstance(g, int) and not isinstance(g, bool) and g > 0,
             f"{d}: games is a positive integer (got {g!r})")
        r.ok(all(isinstance(v, (int, float)) and not isinstance(v, bool)
                 and 0 < v <= 100 for v in x["entries"].values()),
             f"{d}: every slice is a number in (0, 100]")
        ro = x.get("read_on")
        try:
            ro_ok = dt.date.fromisoformat(ro) >= dt.date.fromisoformat(d)
        except (TypeError, ValueError):
            ro_ok = False
        r.ok(ro_ok, f"{d}: read_on is an ISO date not before the day itself "
                    f"(got {ro!r})")

    # Sum check. This is the one that hid two short days for a fortnight when
    # it was run only over the week being written, so it runs over everything.
    for d in full:
        total = round(sum(days[d]["entries"].values()), 6)
        if d in sum_exempt:
            rec = next(e for e in diffs
                       if e.get("day") == d and e.get("column") == "(all)")
            if not r.ok(isinstance(rec.get("page_value"), (int, float)),
                        f"{d}: its rounding exception states a page_value"):
                continue
            r.ok(abs(total - rec["page_value"]) < 1e-6,
                 f"{d}: documented rounding exception sums to "
                 f"{rec['page_value']} (got {total})")
            # The check for a day like that is reconstructing the game counts.
            games = days[d]["games"]
            counts = [v * games / 100 for v in days[d]["entries"].values()]
            rounded = [round(c) for c in counts]
            off = max(abs(c - rc) for c, rc in zip(counts, rounded))
            r.ok(sum(rounded) == games and off < 0.5,
                 f"{d}: slices reconstruct to whole games summing to {games} "
                 f"(got {sum(rounded)}, worst slice off by {off:.2f})")
        else:
            r.ok(abs(total - 100.0) < 1e-6, f"{d}: sums to 100.0 (got {total})")

    # The leader fields are derived, so they can be recomputed rather than
    # trusted. "Largest named slice, unnamed bucket excluded, null on a tie."
    for d in dates:
        x = days[d]
        named = {k: v for k, v in x["entries"].items() if k != "その他"}
        if not named:
            continue
        top = max(named.values())
        tied = sorted(k for k, v in named.items() if v == top)
        if len(tied) > 1:
            r.ok(x.get("leading_named_deck") is None,
                 f"{d}: leading_named_deck is null on a {len(tied)}-way tie")
            r.ok(sorted(x.get("leader_tied_between") or []) == tied,
                 f"{d}: leader_tied_between is {tied} "
                 f"(got {sorted(x.get('leader_tied_between') or [])})")
        else:
            r.ok(x.get("leading_named_deck") == tied[0],
                 f"{d}: leading_named_deck is {tied[0]} "
                 f"(got {x.get('leading_named_deck')!r})")
            r.ok("leader_tied_between" not in x,
                 f"{d}: no leader_tied_between when there is no tie")
    return data


def check_names(r: Report, daily: dict) -> dict:
    r.group(f"{NAMES} — which source calls which deck what")
    raw = read(NAMES)
    if raw.startswith(UNREADABLE):
        r.ok(False, f"could not be read: {raw[len(UNREADABLE):].strip()}")
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        r.ok(False, f"does not parse: {exc}")
        return {}
    r.ok(True, "parses")

    ids = [d["id"] for d in data["decks"]]
    r.ok(len(ids) == len(set(ids)), f"deck ids are unique ({len(ids)} decks)")

    # A chart label must not belong to two decks, or a table check could pick
    # the wrong column.
    owner: dict[str, str] = {}
    clash = []
    for deck in data["decks"]:
        for n in deck["names"]:
            if n["name"] in owner and owner[n["name"]] != deck["id"]:
                clash.append((n["name"], owner[n["name"]], deck["id"]))
            owner[n["name"]] = deck["id"]
    r.ok(not clash, f"no chart label belongs to two decks ({clash})")

    # Every name marked as the survey's should appear in the survey record.
    labels = {k for d in daily.get("days", {}).values() for k in d["entries"]}
    for deck in data["decks"]:
        for n in deck["names"]:
            if "survey" in n.get("used_by", []):
                if n["name"] in labels:
                    r.ok(True, f"survey name {n['name']} appears in {DAILY}")
                elif n.get("absent_from_daily"):
                    r.note(f"{n['name']}: absent from {DAILY}, documented")
                else:
                    r.ok(False, f"survey name {n['name']} is on no chart in "
                                f"{DAILY} and the entry does not say why",
                         warn_only=True)
    return data


# -------------------------------------------------------------- page checks

def deck_family_index(daily: dict, names: dict) -> dict[str, list[str]]:
    """Table header (lowercased) -> the survey labels it stands for.

    A Japanese header is the chart's own label and stands for itself. An
    English header stands for a deck, and a deck may be ONE label or a family
    the survey splits across two; those pages print the family total, so the
    comparison is against the sum of the family's labels present that day.
    That was worked out from the record rather than assumed: every cell under
    the `Baraghiara` and `Magic Tools` headings equals either the single label
    or the two-label sum, depending on whether the survey split that day.

    The earlier version mapped a header to ONE label and gave up whenever a
    deck had more than one survey name in the record, which silently dropped
    51 cells across four pages.
    """
    labels = {k for d in daily.get("days", {}).values() for k in d["entries"]}
    idx: dict[str, list[str]] = {label.lower(): [label] for label in labels}
    for spelling in ("other", 'unlabelled "other"', "unnamed", "bucket"):
        idx[spelling] = ["その他"]
    for deck in names.get("decks", []):
        survey = [n["name"] for n in deck["names"]
                  if "survey" in n.get("used_by", []) and n["name"] in labels]
        if not survey:
            continue
        heads = [deck.get("site_name")] + list(deck.get("page_headers", []))
        for h in heads:
            if h:
                idx.setdefault(h.lower(), survey)
        # A header that means one specific label of a multi-label deck. The
        # 27 September page splits a family by civilisation into two columns,
        # so each of those is one label and not the family total.
        for h, lab in (deck.get("page_header_labels") or {}).items():
            if isinstance(lab, str):
                idx[h.lower()] = [lab]
            elif isinstance(lab, list):
                idx[h.lower()] = lab
    return idx


# Headers that hold the day's sample size.
GAMES_HEADERS = {"games", "games in sample", "sample"}
# Columns that hold a deck NAME rather than a share, checkable against the
# day's recorded leader.
LEADER_NAME_HEADERS = {"most-encountered deck", "leading named deck",
                       "chart leader", "leader"}
# The leader's own share, checkable against the day's largest named slice.
LEADER_SHARE_HEADERS = {"its share", "leader share"}


def check_page(r: Report, path: str, daily: dict, labels: dict[str, list[str]],
               exempt: set[tuple], baseline: dict) -> None:
    r.group(path)
    s = read(path)
    base = os.path.basename(path)

    # --- the four description slots. Checking fewer has shipped stale text.
    slots = {
        "meta": meta(s, r'<meta name="description" content="([^"]*)"'),
        "og": meta(s, r'<meta property="og:description" content="([^"]*)"'),
        "twitter": meta(s, r'<meta name="twitter:description" content="([^"]*)"'),
    }
    ld = jsonld(s)
    r.ok(ld is not None, "JSON-LD block parses")
    if ld:
        slots["json-ld"] = ld.get("description")
    present = {k: ("" if v is None else str(v)) for k, v in slots.items()
               if v is not None}
    r.ok(len(present) == 4, f"all four description slots exist "
                            f"(missing: {sorted(set(slots) - set(present))})")
    # Four identical empty slots agree with each other, which is how an empty
    # description passed as clean.
    empty = sorted(k for k, v in present.items() if not v.strip())
    r.ok(not empty, f"every description is not empty (empty: {empty})")
    if len(present) > 1:
        distinct = set(present.values())
        if not r.ok(len(distinct) == 1, "all description slots agree"):
            for k, v in present.items():
                r.note(f"{k:8s} {len(v):4d}  {v[:90]}")  # v is str by now

    # --- titles
    title = meta(s, r"<title>([^<]*)</title>")
    titles = {
        "og": meta(s, r'<meta property="og:title" content="([^"]*)"'),
        "twitter": meta(s, r'<meta name="twitter:title" content="([^"]*)"'),
    }
    r.ok(bool(title and title.strip()), "has a non-empty <title>")
    h1m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    r.ok(h1m is not None, "has an h1")
    if h1m and title:
        h1 = html.unescape(strip_tags(h1m.group(1))).strip()
        # og:title and twitter:title are the same slot twice over. They have no
        # reason to differ from each other, so a difference is stale text.
        tvals = {v for v in titles.values() if v}
        r.ok(len(tvals) <= 1, f"og:title and twitter:title agree ({tvals})")
        # There is deliberately no check that <title> matches the h1. It was
        # written, it fired on 24 of 52 pages, and every one of them was house
        # style: the title is written for a search result and the h1 for a
        # reader. A check that is false when nothing is wrong trains you to
        # ignore the output, which is worse than not having it.
        r.ok(bool(h1), "h1 is not empty")

    # --- canonical, og:url and the JSON-LD url all stay on the live host
    can = meta(s, r'<link rel="canonical" href="([^"]*)"')
    ogu = meta(s, r'<meta property="og:url" content="([^"]*)"')
    # Article pages carry the url as mainEntityOfPage.@id; the WebSite and
    # DefinedTermSet types on the home page and the glossary carry it as
    # `url`, which is the right idiom for those types. schema.org also allows
    # mainEntityOfPage to be a bare URL string. Accept all three spellings.
    mep = (ld or {}).get("mainEntityOfPage")
    ldu = (mep.get("@id") if isinstance(mep, dict)
           else mep if isinstance(mep, str) else None)
    if not ldu:
        u = (ld or {}).get("url")
        ldu = u if isinstance(u, str) else None
    slots_url = {"canonical": can, "og:url": ogu, "json-ld url": ldu}
    # A set of present values satisfies "they agree" with one survivor, which
    # is how a missing slot used to pass. Presence is its own check.
    absent = sorted(k for k, v in slots_url.items() if not v)
    r.ok(not absent, f"all three url slots are present (missing: {absent})")
    urls = {u for u in slots_url.values() if u}
    r.ok(len(urls) <= 1, f"canonical, og:url and JSON-LD url agree ({urls})")
    want = HOST if base == "index.html" else HOST + base
    for k, v in slots_url.items():
        if v:
            r.ok(v.startswith(HOST), f"{k} is on {HOST} ({v})")
            r.ok(v == want, f"{k} points at this file ({v} vs {want})")

    # --- tag balance. Pass 6 catches what surgical editing creates; this
    #     catches what surgical editing breaks.
    bad = []
    for tag in TAGS:
        o = len(re.findall(rf"<{tag}[\s>]", s))
        c = len(re.findall(rf"</{tag}>", s))
        if o != c:
            bad.append(f"{tag} {o}/{c}")
    r.ok(not bad, f"tag open/close counts balance ({', '.join(bad)})")

    # --- entities. A bare & is a rendering bug; a query string is not.
    masked = re.sub(r'(href|src)="[^"]*"', "", s)
    allowed = "|".join(ENTITIES)
    stray = re.findall(rf"&(?!(?:{allowed});|#\d+;|#x[0-9a-fA-F]+;)\S{{0,10}}",
                       masked)
    r.ok(not stray, f"no malformed entities ({stray[:4]})")

    # --- the middot. B・A・D and G・G・G use U+30FB; U+00B7 is a different
    #     character and has shipped twice as one. It has to be tested on the
    #     DECODED text: the first version of this check read the raw file and
    #     so missed `G&middot;G&middot;G`, the same bug spelled as an entity,
    #     on a page published the day before. The kicker separators are
    #     `&middot;` with a space either side, which does not match.
    wrong = re.findall(r"[A-Za-z　-鿿゠-ヿ]·"
                       r"[A-Za-z　-鿿゠-ヿ]", html.unescape(s))
    r.ok(not wrong, f"no U+00B7 used as a Japanese middle dot ({wrong})")

    # --- Japanese outside a jp span. Warn only: card names in 《》 and quoted
    #     notice titles in 「」 are legitimate, and so is the odd inline use.
    art = re.search(r"<article[^>]*>(.*?)</article>", s, re.S)
    rest = art.group(1) if art else s
    rest = re.sub(r"<script.*?</script>|<style.*?</style>", "", rest, flags=re.S)
    rest = re.sub(r'<span class="jp">.*?</span>', "", rest, flags=re.S)
    # Civilisation chips and glossary legends carry a bare kanji by design.
    rest = re.sub(r'<(\w+)[^>]*class="[^"]*(?:civ|legend|gl|c-)[^"]*"[^>]*>'
                  r".*?</\1>", "", rest, flags=re.S)
    rest = re.sub(r"《[^》]*》|「[^」]*」|『[^』]*』", "", rest)
    rest = re.sub(r'(href|src|content|alt|title|aria-label)="[^"]*"', "", rest)
    loose = {c for c in rest
             if ord(c) > 0x2E80 and unicodedata.category(c)[0] == "L"}
    known = set(baseline.get("loose_japanese", {}).get(base, ""))
    new = sorted(loose - known)
    r.ok(not new,
         f"no Japanese newly left outside a jp span ({''.join(new)})",
         warn_only=True)
    if loose and not new:
        r.note(f"{len(loose)} unwrapped Japanese characters, all in the baseline")

    # --- a dated correction belongs in a note box, not in the opening
    #     paragraph. Counted across the site on 29 October: 53 correction
    #     markers, 47 of them inside a .note box, the rest in a kicker
    #     dateline or a .cap follow-up, and NONE in a standfirst. The one
    #     that was is the edit this check was written for: a forward note
    #     added to week four landed inside its standfirst and split the
    #     paragraph in half.
    for sf in re.findall(r'<p class="standfirst">(.*?)</p>', s, re.S):
        hit = re.search(r"Corrected[ ,]|Correction,|Note added|Updated \d|"
                        r"Resolved,|Forward note", sf)
        r.ok(not hit, f"no dated correction inside the standfirst "
                      f"({hit.group(0) if hit else ''}) — it goes in a "
                      f"note box so the opening paragraph reads as written")

    # --- local links resolve
    # Strip the fragment and query rather than skipping hrefs that have one:
    # `no-such-page.html#x` used to be exempt from existing.
    targets = set()
    for h in re.findall(r'href="([^"]+)"', s):
        if h.startswith(("http", "mailto:", "//", "#", "?")):
            continue
        targets.add(re.split(r"[#?]", h, 1)[0])
    broken = sorted(t for t in targets if t and not os.path.exists(t))
    r.ok(not broken, f"every local link resolves ({broken})")

    # --- tables against the data file
    check_tables(r, path, s, daily, labels, exempt)


def check_tables(r: Report, path: str, s: str, daily: dict,
                 labels: dict[str, list[str]], exempt: dict) -> None:
    """Compare every dated table cell against the stored reading.

    **Everything it cannot compare, it says so about.** The first version
    skipped silently on a header it could not map, a cell it could not parse,
    a row whose date was not in the record, a table with no `<thead>`, a
    transposed table, a `colspan`, and a page whose filename carried no year.
    An audit found 117 of 293 comparable cells going unchecked with no trace,
    and a whole transposed table of 54. A silent skip is indistinguishable
    from a pass, which is the only thing worse than not checking.

    So an unparsed thing in a dated table is a WARN, not a shrug. WARN does
    not fail the publish gate; it is there to be read.
    """
    days = daily.get("days", {})
    year = page_year(path)
    base = os.path.basename(path)
    checked = 0
    dated_tables = [0]
    unmapped: set[str] = set()
    tables = re.findall(r"<table[^>]*>(.*?)</table>", s, re.S)

    def dated_rows(block: str) -> int:
        return sum(1 for row in re.findall(r"<tr[^>]*>(.*?)</tr>", block, re.S)
                   for c in re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)[:1]
                   if looks_like_a_day(cell_text(c)))

    for n, tbl in enumerate(tables, 1):
        where = f"table {n} of {len(tables)}"
        head = re.search(r"<thead>(.*?)</thead>", tbl, re.S)
        body = re.search(r"<tbody>(.*?)</tbody>", tbl, re.S)
        if head:
            head_block = head.group(1)
            rows_block = body.group(1) if body else tbl[head.end():]
        else:
            # Fifty tables on this site have no <thead>. Most carry no dated
            # rows, but skipping them outright left the ones that do
            # unchecked, so fall back to the table's first row as the header.
            first = re.search(r"<tr[^>]*>(.*?)</tr>", tbl, re.S)
            if not first:
                continue
            head_block = first.group(1)
            rows_block = tbl[first.end():]
        n_dated = dated_rows(rows_block)
        cols_raw = [re.sub(r"\s+", " ", cell_text(c)).strip()
                    for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>",
                                        head_block, re.S)]
        cols = [c.lower() for c in cols_raw]
        if not cols:
            r.ok(n_dated == 0,
                 f"{where} has {n_dated} dated rows and no usable header "
                 f"row, so none could be compared", warn_only=True)
            continue
        header_dates = sum(1 for c in cols if looks_like_a_day(c))
        transposed = n_dated == 0 and header_dates >= 2
        if n_dated == 0 and not transposed:
            continue
        dated_tables[0] += 1
        if year is None:
            r.ok(False, f"{where} has dated cells but this filename carries "
                        f"no date, so the script cannot infer a year for them "
                        f"and compared none", warn_only=True)
            continue

        # Build (date, header, cell) triples from whichever way round the
        # table is written. A transposed table - dates across the top, decks
        # down the side - used to be skipped outright: 56 cells of real
        # survey data on three pages, with nothing printed about it.
        triples: list[tuple[str, str, str]] = []
        for row in re.findall(r"<tr[^>]*>(.*?)</tr>", rows_block, re.S):
            raw_cells = re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", row, re.S)
            cells = [cell_text(c) for c in raw_cells]
            if not cells:
                continue
            key = cells[0]
            if not transposed and not looks_like_a_day(key):
                continue
            if len(cells) != len(cols):
                spans = sum(1 for c in raw_cells if "colspan" in c.lower())
                r.ok(False, f"{where} row {key!r} has {len(cells)} cells "
                            f"against {len(cols)} headers"
                            + (f" ({spans} with colspan)" if spans else "")
                            + ", so it could not be compared", warn_only=True)
                continue
            if transposed:
                for head, cell in zip(cols_raw[1:], cells[1:]):
                    if looks_like_a_day(head):
                        triples.append((head, key, cell))
            else:
                for head, cell in zip(cols[1:], cells[1:]):
                    triples.append((key, head, cell))

        seen_bad = set()
        for day_cell, header, cell in triples:
            day = parse_day(day_cell, year)
            if day is None or day not in days:
                if day_cell not in seen_bad:
                    seen_bad.add(day_cell)
                    r.ok(False, f"{where} {day_cell!r} resolves to "
                                f"{day or 'nothing'}, which is not in the "
                                f"record, so its cells could not be compared",
                         warn_only=True)
                continue
            rec = days[day]
            header = re.sub(r"\s+", " ", header).lower().strip()
            for header, cell in [(header, cell)]:
                head_key = header
                if head_key in DERIVED_HEADERS:
                    continue
                if head_key in GAMES_HEADERS:
                    if re.fullmatch(r"[\d,]+", cell):
                        checked += 1
                        r.ok(int(cell.replace(",", "")) == rec["games"],
                             f"{day} games: page {cell}, data {rec['games']}")
                    else:
                        r.ok(False, f"{day} games: {cell!r} could not be "
                                    f"compared", warn_only=True)
                    continue
                if head_key in LEADER_NAME_HEADERS:
                    want = rec.get("leading_named_deck")
                    tied = rec.get("leader_tied_between") or []
                    expect = sorted([want] if want else tied)
                    # These cells are written for a reader: "Jokers 26.5",
                    # "Raid and Jokers, both 20.8", "Dragerion and
                    # Baraghiara, tied", "see below". So recognise the deck
                    # names IN the cell rather than trying to split it.
                    # The page names a DECK; the record names a LABEL, and a
                    # deck may own two labels. So compare at deck level: the
                    # families named in the cell against the families the
                    # recorded leaders belong to.
                    low = cell.lower()
                    got = {frozenset(fam) for head, fam in labels.items()
                           if head and head in low}
                    # A family matched only because its name sits inside a
                    # longer one that also matched is not named here.
                    got = {f for f in got
                           if not any(f < o for o in got)}
                    if not got:
                        r.ok(False, f"{day} leader column: no deck name "
                                    f"recognised in {cell!r}, so it was not "
                                    f"compared with {expect}", warn_only=True)
                        continue
                    want_fams = set()
                    for lab in expect:
                        fams = [frozenset(f) for f in got if lab in f]
                        want_fams.update(fams or [frozenset([lab])])
                    checked += 1
                    r.ok(got == want_fams,
                         f"{day} leader column: page names "
                         f"{[sorted(f) for f in sorted(got, key=sorted)]}, "
                         f"data has {expect}")
                    # Many of these cells carry the share next to the name.
                    m = re.search(r"(\d+(?:\.\d+)?)", cell)
                    named = [v for k, v in rec["entries"].items()
                             if k != "その他"]
                    if m and named:
                        checked += 1
                        r.ok(abs(float(m.group(1)) - max(named)) < 1e-9,
                             f"{day} leader share in {cell!r}: page "
                             f"{m.group(1)}, largest named slice {max(named)}")
                    continue
                if head_key in LEADER_SHARE_HEADERS:
                    named = [v for k, v in rec["entries"].items()
                             if k != "その他"]
                    m = re.fullmatch(r"(\d+(?:\.\d+)?)\s*%?", cell)
                    if not m:
                        r.ok(False, f"{day} {head_key}: {cell!r} could not be "
                                    f"compared", warn_only=True)
                        continue
                    checked += 1
                    r.ok(named and abs(float(m.group(1)) - max(named)) < 1e-9,
                         f"{day} {head_key}: page {m.group(1)}, largest named "
                         f"slice {max(named) if named else None}")
                    continue
                family = labels.get(head_key)
                if family is None:
                    # Only a column of numbers is a missed comparison. A
                    # column of names, codes or card titles is just text.
                    if re.fullmatch(r"\d+(?:\.\d+)?\s*%?", cell):
                        unmapped.add(head_key)
                    continue
                here = [rec["entries"][k] for k in family
                        if k in rec["entries"]]
                stored = round(sum(here), 6) if here else None
                label = (family[0] if len(family) == 1
                         else " + ".join(k for k in family if k in rec["entries"])
                         or " / ".join(family))
                # A documented difference still gets checked, against the
                # figure the exemption itself records. Skipping it outright
                # left the cell unchecked forever, whatever the page later said.
                rule = exempt.get((base, day, head_key)) or \
                    exempt.get((base, day, label.lower()))
                if rule is not None:
                    want = rule.get("page_value")
                    m = re.fullmatch(r"(\d+(?:\.\d+)?)%?", cell)
                    if not isinstance(want, (int, float)):
                        r.ok(False, f"{day} {label}: documented difference "
                                    f"states no page_value to check against",
                             warn_only=True)
                    elif not m:
                        r.ok(False, f"{day} {label}: documented difference, "
                                    f"and {cell!r} could not be compared",
                             warn_only=True)
                    else:
                        checked += 1
                        r.ok(abs(float(m.group(1)) - want) < 1e-9,
                             f"{day} {label}: documented difference, page "
                             f"should read {want} (reads {m.group(1)})")
                    continue
                if re.fullmatch(r"not named|—|-|n/a|", cell, re.I):
                    checked += 1
                    r.ok(stored is None,
                         f"{day} {label}: page says {cell or 'blank'}, "
                         f"data has {stored}")
                    continue
                m = re.fullmatch(r"(\d+(?:\.\d+)?)\s*%?", cell)
                if not m:
                    r.ok(False, f"{day} {label}: page cell {cell!r} could not "
                                f"be compared with the stored {stored}",
                         warn_only=True)
                    continue
                if stored is None and rec.get("completeness") == "tracked":
                    # A tracked day is six columns plus the leader by design.
                    # A page carrying more than that is not wrong; the record
                    # is incomplete for that day, and saying so is the point.
                    r.ok(False, f"{day} {label}: page reads {m.group(1)} and "
                                f"this day is a partial read that does not "
                                f"hold that label, so it was not compared",
                         warn_only=True)
                    continue
                checked += 1
                r.ok(stored is not None and abs(float(m.group(1)) - stored) < 1e-9,
                     f"{day} {label}: page {m.group(1)}, data {stored}")
    if unmapped:
        for h in sorted(unmapped):
            r.ok(False, f'header "{h}" maps to no stored label, so its dated '
                        f"cells were not compared", warn_only=True)
    if checked:
        r.note(f"{checked} table cells compared against {DAILY}")
        TOTALS["cells"] = TOTALS.get("cells", 0) + checked
        TOTALS["pages"] = TOTALS.get("pages", 0) + 1
        TOTALS["tables"] = TOTALS.get("tables", 0) + dated_tables[0]


# ----------------------------------------------------------------- sitemap

def check_sitemap(r: Report) -> None:
    r.group(f"{SITEMAP} — the home page's only recorded referrer")
    raw = read(SITEMAP)
    if raw.startswith(UNREADABLE):
        r.ok(False, f"could not be read: {raw[len(UNREADABLE):].strip()}")
        return
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        r.ok(False, f"does not parse: {exc}")
        return
    r.ok(True, "well-formed XML")

    locs = [e.text.strip() for e in root.iter() if e.tag.endswith("loc") and e.text]
    r.ok(all(u.startswith(HOST) for u in locs),
         f"every loc is on {HOST} "
         f"({[u for u in locs if not u.startswith(HOST)][:3]})")
    paths = [u[len(HOST):] for u in locs if u.startswith(HOST)]
    dupes = sorted({p for p in paths if paths.count(p) > 1})
    r.ok(not dupes, f"no duplicate URLs ({dupes})")

    on_disk = {f for f in os.listdir(".")
               if f.endswith(".html") and f not in NOT_PAGES}
    listed = {("index.html" if p == "" else p) for p in paths}
    r.note(f"{len(locs)} URLs against {len(on_disk)} published pages")

    # Both directions. Reading the file does not catch an absence.
    r.ok(not (on_disk - listed),
         f"every published page is in the sitemap ({sorted(on_disk - listed)})")
    r.ok(not (listed - on_disk),
         f"every sitemap URL has a page ({sorted(listed - on_disk)})")


def check_markdown(r: Report) -> None:
    r.group("instruction files — a wrong rule outlives a wrong article")
    for f in sorted(x for x in os.listdir(".") if x.endswith(".md")):
        s = read(f)
        if s.startswith(UNREADABLE):
            r.ok(False, f"{f}: could not be read")
            continue
        # &mdash; in a markdown file renders literally. The first version
        # compared a COUNT of entities against a count of backticked ones,
        # which gave every backticked example one unit of slack anywhere in
        # the file. Strip the code spans first, then look at what is left.
        stripped = re.sub(r"```.*?```|`[^`\n]*`", "", s, flags=re.S)
        ents = sorted(set(re.findall(
            r"&(?:[a-zA-Z][a-zA-Z0-9]{1,10}|#\d{2,5}|#x[0-9a-fA-F]{2,4});",
            stripped)))
        r.ok(not ents, f"{f}: no HTML entities outside code spans ({ents})")
        r.ok("\t" not in s, f"{f}: no tab characters", warn_only=True)


def check_selftest_count(r: Report) -> None:
    """The instruction files state how many ways --selftest breaks the repo.
    That number has gone stale three times: it said sixteen for two rewrites,
    and the line added on 27 October telling a reader to keep it right was
    itself wrong by the 29th, one check later. A number a person has to
    remember to update is a number that will be wrong, so it is checked."""
    r.group("the instruction files' claims about this script")
    n = len(SELFTEST)
    r.note(f"--selftest has {n} cases")
    for f in ("CLAUDE.md", "EDITORIAL.md"):
        text = read(f)
        if text.startswith(UNREADABLE):
            r.ok(False, f"{f}: could not be read")
            continue
        claims = re.findall(r"(\d+|sixteen|seventeen|eighteen) ways", text)
        r.ok(bool(claims), f"{f} states how many ways --selftest breaks things")
        for c in claims:
            r.ok(c == str(n),
                 f"{f} says {c!r} ways and there are {n}")


def check_repo(r: Report) -> None:
    r.group("repository invariants")
    r.ok(os.path.exists(OWNERSHIP),
         f"{OWNERSHIP} is still present (Search Console ownership)")
    r.ok(os.path.exists("CNAME"), "CNAME is still present")
    for f in (DAILY, NAMES, SITEMAP, "style.css", "glossary.js"):
        r.ok(os.path.exists(f), f"{f} exists")


# -------------------------------------------------------------------- main

def main(argv: list[str]) -> int:
    if "--list" in argv:
        print(__doc__)
        return 0
    if "--selftest" in argv:
        return selftest()

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    r = Report()

    daily = check_daily(r)
    names = check_names(r, daily)
    labels = deck_family_index(daily, names)
    # Keyed lowercase, because the header row is lowercased before matching
    # and an entry written in title case silently matched nothing.
    exempt = {}
    for e in daily.get("known_convention_differences", []):
        col = e.get("column")
        if e.get("page") and e.get("day") and col:
            exempt[(e["page"], e["day"], col.lower())] = e

    baseline = {}
    if os.path.exists(BASELINE):
        try:
            baseline = json.loads(read(BASELINE))
        except json.JSONDecodeError as exc:
            r.group(BASELINE)
            r.ok(False, f"does not parse: {exc}")

    requested = [a for a in argv[1:] if not a.startswith("-")]
    if requested:
        pages = [os.path.basename(p) for p in requested]
    else:
        pages = sorted(f for f in os.listdir(".")
                       if f.endswith(".html") and f not in NOT_PAGES)

    for p in pages:
        if not os.path.exists(p):
            r.group(p)
            r.ok(False, "file does not exist")
            continue
        check_page(r, p, daily, labels, exempt, baseline)

    check_sitemap(r)
    check_markdown(r)
    check_selftest_count(r)
    check_repo(r)

    # A site-wide figure, so a coverage collapse is a number that moves. The
    # pass count moves with page count and day count and hides it: when one
    # `<br>` in a header stopped seven comparisons, the total went 1226 to
    # 1219 and nothing said why.
    r.group("coverage")
    r.note(f"{TOTALS.get('cells', 0)} table cells compared against {DAILY} "
           f"across {TOTALS.get('tables', 0)} dated tables on "
           f"{TOTALS.get('pages', 0)} pages")
    if TOTALS.get("uncompared"):
        r.note(f"{TOTALS['uncompared']} dated cells reported as not "
               f"comparable (see the warnings)")
    return r.summary()



# ----------------------------------------------------------------- selftest
#
# A check that stays true when the error happens is not a check. So each class
# of check below is run against a deliberately broken copy of the repository
# and has to fail. Run it after editing this file:
#
#     python3 check.py --selftest
#
# Every mutation is one of the mistakes that has actually shipped here, or the
# mechanical shape of one. If a mutation stops being caught, the check that was
# supposed to catch it has been broken, not the mutation.

# label, file, anchor, replacement, and the text the run MUST print.
# The expectation is the whole point: the first version of this selftest
# accepted "any WARN anywhere in the output" as proof a mutation was caught,
# which meant four checks could be DELETED and it still reported all green.
# Each entry now has to produce its own message.
SELFTEST = [
    ("a table cell disagreeing with the data file",
     "2026-10-26-raid-chart.html", "<td>290</td>", "<td>289</td>",
     "2026-10-25 games: page 289, data 290"),
    ("a deck percentage edited on the page only",
     "2026-10-26-raid-chart.html", "<strong>16.6</strong></td>",
     "<strong>16.8</strong></td>",
     "2026-10-25 赤白轟轟轟(レイド無し): page 16.8, data 16.6"),
    ("a deck shown as named on a day it is not",
     "2026-10-26-raid-chart.html",
     "<td>23 Oct</td><td>227</td><td><strong>not named</strong></td>",
     "<td>23 Oct</td><td>227</td><td>6.5</td>",
     "2026-10-23 赤白レイド: page 6.5, data None"),
    ("a dated cell the comparison cannot parse",
     "2026-10-26-raid-chart.html", "<td>16.6</td>", "<td>16.6&nbsp;%</td>",
     "could not be compared"),
    ("a dated table header that maps to nothing",
     "2026-10-24-week-four.html", "<th>Jokers</th>", "<th>Jokers Deck</th>",
     "header \"jokers deck\" maps to no stored label"),
    # A transposed table - dates across the top, decks down the side - used
    # to be skipped in silence: 56 cells of real survey data on three pages.
    ("a transposed table whose figures disagree with the record",
     "2026-09-27-first-numbers.html",
     "<td>Jokers</td><td>4.9%</td>", "<td>Jokers</td><td>9.9%</td>",
     "2026-09-24 ジョーカーズ: page 9.9, data 4.9"),
    ("a date typo that would hide a whole row",
     "2026-10-26-raid-chart.html", "<td>23 Oct</td>", "<td>23 Nov</td>",
     "which is not in the record"),
    ("a dated table on a page with no date in its filename",
     "glossary.html", "</article>",
     '<table><thead><tr><th>Day</th><th>Games</th></tr></thead>'
     '<tbody><tr><td>25 Oct</td><td>290</td></tr></tbody></table></article>',
     "cannot infer a year"),
    ("an exemption that no longer matches the page it exempts",
     DAILY, '"page": "2026-10-04-nine-days.html"',
     '"page": "2026-10-04-nine-days.html", "unused_marker": 1',
     "checks passed"),
    ("one description slot left stale",
     "2026-10-26-raid-chart.html",
     '<meta property="og:description" content="Three full days',
     '<meta property="og:description" content="Two full days',
     "all description slots agree"),
    ("a description slot emptied",
     "2026-10-26-raid-chart.html",
     '<meta name="description" content="Three full days',
     '<meta name="description" content=""><meta name="x" content="Three full days',
     "every description is not empty"),
    ("the title element removed",
     "2026-10-26-raid-chart.html", "<title>", "<titl e>",
     "has a non-empty <title>"),
    ("a canonical pointing somewhere else",
     "2026-10-26-raid-chart.html",
     '<link rel="canonical" href="https://duelmasters.editioncompass.com/'
     '2026-10-26-raid-chart.html">',
     '<link rel="canonical" href="https://example.com/x.html">',
     "canonical is on"),
    ("the JSON-LD url removed, leaving the other two to agree",
     "2026-10-26-raid-chart.html", '"mainEntityOfPage"', '"notTheEntity"',
     "all three url slots are present"),
    ("og:title and twitter:title disagreeing",
     "2026-10-26-raid-chart.html",
     '<meta name="twitter:title" content="A deck',
     '<meta name="twitter:title" content="Another deck',
     "og:title and twitter:title agree"),
    ("an unbalanced tag",
     "2026-10-26-raid-chart.html", "</article>", "</article><p>",
     "tag open/close counts balance"),
    ("the duplicated </article> this script found on four real pages",
     "2026-10-26-raid-chart.html", "</article>", "</article></article>",
     "article 1/2"),
    ("a link to a page that does not exist",
     "2026-10-26-raid-chart.html", 'href="2026-10-24-week-four.html">week four',
     'href="2026-10-24-week-forty.html">week four',
     "every local link resolves"),
    # The same break, carrying a fragment. The first version of the link
    # check excluded any href containing # or ?, so this one was exempt.
    ("the same broken link carrying a fragment",
     "2026-10-26-raid-chart.html", 'href="2026-10-24-week-four.html">week four',
     'href="2026-10-24-week-forty.html#x">week four',
     "2026-10-24-week-forty.html"),
    ("U+00B7 used as a Japanese middle dot",
     "2026-10-26-raid-chart.html", "<h1>", "<h1>キ·キ ",
     "no U+00B7 used as a Japanese middle dot"),
    # The same bug spelled as an entity. The first version of the middot check
    # read the raw file and passed this clean, which is how it shipped.
    ("U+00B7 as an entity, which the first version of the check missed",
     "2026-10-26-raid-chart.html", "<h1>", "<h1>G&middot;G&middot;G ",
     "no U+00B7 used as a Japanese middle dot"),
    # A dated note dropped into the opening paragraph instead of a box.
    ("a dated correction buried in the standfirst",
     "2026-10-29-week-five.html", '<p class="standfirst">Week five',
     '<p class="standfirst">Corrected 29 October. Week five',
     "no dated correction inside the standfirst"),
    ("a malformed entity",
     "2026-10-26-raid-chart.html", "<h1>", "<h1>&nope; ",
     "no malformed entities"),
    ("Japanese newly left outside a jp span",
     "2026-10-26-raid-chart.html", "<h1>", "<h1>小説工場 ",
     "no Japanese newly left outside a jp span"),
    ("the unnamed bucket edited on a week page",
     "2026-10-24-week-four.html", "<td>13.1</td>", "<td>13.7</td>",
     "2026-10-15 その他: page 13.7, data 13.1"),
    ("a sitemap entry removed",
     "sitemap.xml",
     "  <url>\n    <loc>https://duelmasters.editioncompass.com/"
     "2026-10-26-raid-chart.html</loc>\n", "  <url>\n    <loc>"
     "https://duelmasters.editioncompass.com/nope.html</loc>\n",
     "every published page is in the sitemap"),
    ("a duplicate sitemap URL",
     "sitemap.xml",
     "<loc>https://duelmasters.editioncompass.com/2026-10-26-raid-chart.html"
     "</loc>",
     "<loc>https://duelmasters.editioncompass.com/2026-10-25-raid-talk.html"
     "</loc>",
     "no duplicate URLs"),
    ("a day that no longer sums to 100.0",
     DAILY, '"赤単バルガ": 6.2', '"赤単バルガ": 6.4',
     "sums to 100.0"),
    # Downgrading one word used to switch the sum check off for that day.
    ("completeness downgraded to tracked to escape the sum check",
     DAILY,
     '"2026-10-23": {\n   "games": 227,\n   "completeness": "full"',
     '"2026-10-23": {\n   "games": 227,\n   "completeness": "tracked"',
     "a tracked day has at most"),
    ("a wrong leading_named_deck",
     DAILY,
     '"games": 227,\n   "completeness": "full",\n   "leading_named_deck": '
     '"ジョーカーズ"',
     '"games": 227,\n   "completeness": "full",\n   "leading_named_deck": '
     '"コットンゼニス"',
     "leading_named_deck is ジョーカーズ"),
    ("a gap in the series",
     DAILY, '"2026-10-10":', '"2026-11-10":',
     "no gaps in the series"),
    ("a day with no read_on",
     DAILY, '"read_on": "2026-10-26"', '"read_ON": "2026-10-26"',
     "read_on"),
    ("a data file that is not there at all",
     DAILY, DELETE_FILE, "", "could not be read"),
    # The count in the instruction files has gone stale three times.
    ("the stated selftest count going stale",
     "CLAUDE.md", "breaks the repository **36 ways**",
     "breaks the repository **34 ways**",
     "says '34' ways and there are 36"),
    ("an HTML entity in a markdown file",
     "CLAUDE.md", "# Start here", "# Start here &mdash;",
     "no HTML entities outside code spans"),
    ("an HTML entity hidden behind a backticked one",
     "TODO.md", "# Where things stand", "# Where things stand &mdash;",
     "no HTML entities outside code spans"),
]


def selftest() -> int:
    """Break the repository one way at a time; each break must be reported.

    The predicate is the point. The first version asked only whether the run
    exited non-zero or printed the word WARN anywhere, which is satisfied by
    any unrelated warning: four checks could be deleted outright and this
    still said "all caught". Each case now names the message its own check
    produces, and is only counted when that message appears.
    """
    import shutil
    import subprocess
    import tempfile

    here = os.path.dirname(os.path.abspath(__file__))
    fails = []
    print(f"Running {len(SELFTEST)} mutations. Each one has to produce its own "
          f"message.\n")
    for label, target, old, new, expect in SELFTEST:
        with tempfile.TemporaryDirectory() as tmp:
            work = os.path.join(tmp, "repo")
            shutil.copytree(here, work,
                            ignore=shutil.ignore_patterns(".git", "__pycache__"))
            path = os.path.join(work, target)
            if old == DELETE_FILE:
                os.remove(path)
                text, n = "", 1
            else:
                text = read(path)
                n = text.count(old)
            if n != 1:
                fails.append(f"{label}: anchor occurs {n} times in {target}, "
                             f"so this case tests nothing reliable")
                print(f"  ANCHOR  {label}  ({n} occurrences, need exactly 1)")
                continue
            if old != DELETE_FILE:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(text.replace(old, new, 1))
            out = subprocess.run([sys.executable, os.path.join(work, "check.py")],
                                 capture_output=True, text=True, cwd=work)
            stream = out.stdout + out.stderr
            if "Traceback" in stream:
                fails.append(f"{label}: the run CRASHED instead of reporting")
                print(f"  CRASH   {label}")
            elif expect in stream:
                flagged = out.returncode != 0
                print(f"  caught  {label}"
                      + ("" if flagged else "   (WARN only, exit 0)"))
            else:
                fails.append(f"{label}: expected {expect!r} in the output")
                print(f"  MISSED  {label}")

    print()
    if fails:
        print(f"{len(fails)} of {len(SELFTEST)} cases did not behave:")
        for f in fails:
            print(f"  - {f}")
        print("\nA check that stays true when the error happens is not a check,")
        print("and a selftest that passes with the check deleted is not a test.")
        return 1
    print(f"All {len(SELFTEST)} mutations produced their own message.")
    print("Cases marked \"WARN only\" do not fail `python3 check.py`, so they")
    print("do not fail the publish gate either. That is deliberate; know which.")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
