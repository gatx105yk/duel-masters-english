#!/usr/bin/env python3
"""Pre-publish checks for Duel Masters English.

Run from the repository root:

    python3 check.py              # everything
    python3 check.py FILE...      # only these pages, plus the always-on file checks
    python3 check.py --list       # what each check does, and nothing else

Exit status is 0 only when no FAIL is reported. WARN never fails the run; it
marks something a human should look at.

Why this exists
---------------
Every check below is here because the mistake it looks for has actually shipped
on this site. `EDITORIAL.md` has the cases. The point is that the mechanical
half of a fact-check pass costs nothing to repeat, so the passes a person runs
can be spent on the half a script cannot do: reading the page as prose, and
re-fetching the sources.

Measured against this site's own history, it would have caught:

  * a deck percentage edited on a page and not in the data file, or the
    reverse, anywhere it appears in a dated table;
  * the duplicated `</article>` on four October pages, and `&middot;` standing
    in for U+30FB in `G・G・G`, both of which it found on its first run;
  * a description slot left stale;
  * the five pages missing from `sitemap.xml`, including the one with the best
    average position on the site.

And it would have caught NONE of these, which are the expensive ones:

  * "week four: Red Balga's low was 4.8" when the table says 3.6, or "four
    days apart" when it was two. Both are prose derived from a table, and a
    derived sentence is not comparable to a stored figure. **Superlatives are
    recomputed by hand against the whole series, every time.**
  * the 4.3 that was called a figure from before the card change when it was
    from after it. Which side of a boundary a figure belongs on is a claim
    about dates, and nothing here knows what a boundary is.
  * a card attributed to the wrong person, or a notice asserted not to exist
    an hour after it went up. Those are facts about the world.
  * two labels swapped in the data file. Everything here is consistency with
    `data-nd-daily.json`, never truth; the chart is read by a person.

So this replaces the mechanical part of a fact-check pass and no part of the
judgement. A clean run means the passes a person spends are spent on reading
and on the sources, not that the page is right.
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
BASELINE = "check-baseline.json"

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
DERIVED_HEADERS = {"pair", "red/white pair", "chart leader", "spread",
                   "leading named deck", "leader", "names that led",
                   "leader share", "week", "games"}

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
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s)


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


def parse_day(text: str, year: int | None) -> str | None:
    """'19 Oct' -> '2026-10-19'. Returns None when the cell is not a date."""
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
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        r.ok(False, f"does not parse: {exc}")
        return {}
    r.ok(True, "parses")

    days = data["days"]
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

    for d in dates:
        x = days[d]
        r.ok(x["completeness"] in ("full", "tracked"),
             f"{d}: completeness is full or tracked")
        r.ok(isinstance(x["games"], int) and x["games"] > 0,
             f"{d}: games is a positive integer")
        r.ok(all(isinstance(v, (int, float)) and v > 0
                 for v in x["entries"].values()),
             f"{d}: every slice is a positive number")
        r.ok(dt.date.fromisoformat(x["read_on"]) >= dt.date.fromisoformat(d),
             f"{d}: read_on ({x['read_on']}) is not before the day itself")

    # Sum check. This is the one that hid two short days for a fortnight when
    # it was run only over the week being written, so it runs over everything.
    for d in full:
        total = round(sum(days[d]["entries"].values()), 6)
        if d in sum_exempt:
            rec = next(e for e in diffs
                       if e.get("day") == d and e.get("column") == "(all)")
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
    try:
        data = json.loads(read(NAMES))
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

def deck_label_index(daily: dict, names: dict) -> dict[str, str]:
    """Header text (lowercased) -> chart label, for the table check."""
    labels = {k for d in daily.get("days", {}).values() for k in d["entries"]}
    idx: dict[str, str] = {label.lower(): label for label in labels}
    idx["other"] = "その他"
    for deck in names.get("decks", []):
        survey = [n["name"] for n in deck["names"]
                  if "survey" in n.get("used_by", [])]
        # A deck renamed by the survey has several survey names and only one
        # of them in the record; that one is unambiguous. A family the survey
        # SPLITS has two labels both in the record, and an English column for
        # it is a family total that is not comparable to either label, so it
        # stays unmapped. known_convention_differences names one such case.
        in_record = [n for n in survey if n in labels]
        if len(in_record) == 1 and deck.get("site_name"):
            idx.setdefault(deck["site_name"].lower(), in_record[0])
    return idx


def check_page(r: Report, path: str, daily: dict, labels: dict[str, str],
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
    present = {k: v for k, v in slots.items() if v is not None}
    r.ok(len(present) == 4, f"all four description slots exist "
                            f"(missing: {sorted(set(slots) - set(present))})")
    if len(present) > 1:
        distinct = set(present.values())
        if not r.ok(len(distinct) == 1, "all description slots agree"):
            for k, v in present.items():
                r.note(f"{k:8s} {len(v):4d}  {v[:90]}")

    # --- titles
    title = meta(s, r"<title>([^<]*)</title>")
    titles = {
        "og": meta(s, r'<meta property="og:title" content="([^"]*)"'),
        "twitter": meta(s, r'<meta name="twitter:title" content="([^"]*)"'),
    }
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
    ldu = (ld or {}).get("mainEntityOfPage", {}).get("@id")
    urls = {u for u in (can, ogu, ldu) if u}
    r.ok(len(urls) == 1, f"canonical, og:url and JSON-LD url agree ({urls})")
    if can:
        r.ok(can.startswith(HOST), f"canonical is on {HOST} ({can})")
        want = HOST if base == "index.html" else HOST + base
        r.ok(can == want, f"canonical points at this file ({can} vs {want})")

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

    # --- the middot. B・A・D and G・G・G use U+30FB; &middot; is a different
    #     character and shipped once as one.
    wrong = re.findall(r"[A-Za-z　-鿿゠-ヿ]·"
                       r"[A-Za-z　-鿿゠-ヿ]", s)
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

    # --- local links resolve
    broken = sorted({h for h in re.findall(r'href="([^"#?]+)"', s)
                     if not h.startswith(("http", "mailto:", "//"))
                     and not os.path.exists(h)})
    r.ok(not broken, f"every local link resolves ({broken})")

    # --- tables against the data file
    check_tables(r, path, s, daily, labels, exempt)


def check_tables(r: Report, path: str, s: str, daily: dict,
                 labels: dict[str, str], exempt: set[tuple]) -> None:
    """Compare every dated table cell against the stored reading.

    Opt-in by shape, not by configuration: a table is checked when its first
    column holds dates this file knows and a header names a chart label. A
    column whose header is not a label is skipped, so the older pages with
    English headers are checked where they can be and left alone where they
    cannot.
    """
    days = daily.get("days", {})
    year = page_year(path)
    checked = 0
    for tbl in re.findall(r"<table[^>]*>(.*?)</table>", s, re.S):
        head = re.search(r"<thead>(.*?)</thead>", tbl, re.S)
        if not head:
            continue
        cols = [cell_text(c).lower()
                for c in re.findall(r"<th[^>]*>(.*?)</th>", head.group(1), re.S)]
        body = re.search(r"<tbody>(.*?)</tbody>", tbl, re.S)
        if not body or not cols:
            continue
        for row in re.findall(r"<tr[^>]*>(.*?)</tr>", body.group(1), re.S):
            cells = [cell_text(c)
                     for c in re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)]
            if len(cells) != len(cols):
                continue
            day = parse_day(cells[0], year)
            if day is None or day not in days:
                continue
            rec = days[day]
            for header, cell in zip(cols[1:], cells[1:]):
                head_key = re.sub(r"\s+", " ", header).strip()
                if head_key in DERIVED_HEADERS and head_key != "games":
                    continue
                if head_key == "games":
                    if re.fullmatch(r"[\d,]+", cell):
                        checked += 1
                        r.ok(int(cell.replace(",", "")) == rec["games"],
                             f"{day} games: page {cell}, data {rec['games']}")
                    continue
                label = labels.get(head_key)
                if label is None:
                    continue
                key = (os.path.basename(path), day, label)
                if key in exempt or (os.path.basename(path), day, header) in exempt:
                    r.note(f"{day} {label}: documented difference, skipped")
                    continue
                stored = rec["entries"].get(label)
                if re.fullmatch(r"not named|&mdash;|—|-|n/a|", cell, re.I):
                    checked += 1
                    r.ok(stored is None,
                         f"{day} {label}: page says {cell or 'blank'}, "
                         f"data has {stored}")
                    continue
                m = re.fullmatch(r"(\d+(?:\.\d+)?)%?", cell)
                if not m:
                    continue
                checked += 1
                r.ok(stored is not None and abs(float(m.group(1)) - stored) < 1e-9,
                     f"{day} {label}: page {m.group(1)}, data {stored}")
    if checked:
        r.note(f"{checked} table cells compared against {DAILY}")


# ----------------------------------------------------------------- sitemap

def check_sitemap(r: Report) -> None:
    r.group(f"{SITEMAP} — the home page's only recorded referrer")
    try:
        root = ET.parse(SITEMAP).getroot()
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
        # &mdash; in a markdown file renders literally.
        ents = re.findall(r"&(?:mdash|ndash|rsquo|ldquo|rdquo|middot|amp|nbsp);", s)
        # TODO.md quotes an entity on purpose, in a rule about entities.
        inline = len(re.findall(r"`&[a-z#0-9]+;`", s))
        r.ok(len(ents) <= inline,
             f"{f}: no HTML entities outside backticks ({set(ents)})")
        r.ok("\t" not in s, f"{f}: no tab characters", warn_only=True)


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
    labels = deck_label_index(daily, names)
    exempt = {(d.get("page"), d.get("day"), d.get("column"))
              for d in daily.get("known_convention_differences", [])}

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
    check_repo(r)
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

SELFTEST = [
    ("a table cell disagreeing with the data file",
     "2026-10-26-raid-chart.html", "<td>290</td>", "<td>289</td>"),
    ("a deck percentage edited on the page only",
     "2026-10-26-raid-chart.html", "<strong>16.6</strong></td>",
     "<strong>16.8</strong></td>"),
    ("a deck shown as named on a day it is not",
     "2026-10-26-raid-chart.html",
     "<td>23 Oct</td><td>227</td><td><strong>not named</strong></td>",
     "<td>23 Oct</td><td>227</td><td>6.5</td>"),
    ("one description slot left stale",
     "2026-10-26-raid-chart.html",
     '<meta property="og:description" content="Three full days',
     '<meta property="og:description" content="Two full days'),
    ("a canonical pointing somewhere else",
     "2026-10-26-raid-chart.html",
     '<link rel="canonical" href="https://duelmasters.editioncompass.com/'
     '2026-10-26-raid-chart.html">',
     '<link rel="canonical" href="https://example.com/x.html">'),
    ("og:title and twitter:title disagreeing",
     "2026-10-26-raid-chart.html",
     '<meta name="twitter:title" content="A deck',
     '<meta name="twitter:title" content="Another deck'),
    ("an unbalanced tag",
     "2026-10-26-raid-chart.html", "</article>", "</article><p>"),
    ("a link to a page that does not exist",
     "2026-10-26-raid-chart.html", 'href="2026-10-25-raid-talk.html"',
     'href="2026-10-25-raid-chatter.html"'),
    ("U+00B7 used as a Japanese middle dot",
     "2026-10-26-raid-chart.html", "<h1>", "<h1>キ·キ "),
    ("a malformed entity",
     "2026-10-26-raid-chart.html", "<h1>", "<h1>&nope; "),
    ("Japanese newly left outside a jp span",
     "2026-10-26-raid-chart.html", "<h1>", "<h1>小説工場 "),
    ("the unnamed bucket edited on a week page",
     "2026-10-24-week-four.html", "<td>13.1</td>", "<td>13.7</td>"),
    ("a sitemap entry removed",
     "sitemap.xml",
     "  <url>\n    <loc>https://duelmasters.editioncompass.com/"
     "2026-10-26-raid-chart.html</loc>\n", "  <url>\n    <loc>"
     "https://duelmasters.editioncompass.com/nope.html</loc>\n"),
    ("a day that no longer sums to 100.0",
     DAILY, '"赤単バルガ": 6.2', '"赤単バルガ": 6.4'),
    ("a wrong leading_named_deck",
     DAILY, '"leading_named_deck": "ジョーカーズ"',
     '"leading_named_deck": "コットンゼニス"'),
    ("an HTML entity in a markdown file",
     "CLAUDE.md", "# Start here", "# Start here &mdash;"),
]


def selftest() -> int:
    import shutil
    import subprocess
    import tempfile

    here = os.path.dirname(os.path.abspath(__file__))
    fails = []
    print(f"Running {len(SELFTEST)} mutations. Each one has to be caught.\n")
    for label, target, old, new in SELFTEST:
        with tempfile.TemporaryDirectory() as tmp:
            work = os.path.join(tmp, "repo")
            shutil.copytree(here, work, ignore=shutil.ignore_patterns(".git"))
            path = os.path.join(work, target)
            text = read(path)
            if text.count(old) < 1:
                fails.append(f"{label}: anchor not found in {target}")
                print(f"  BROKEN  {label}  (anchor missing)")
                continue
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text.replace(old, new, 1))
            out = subprocess.run([sys.executable, os.path.join(work, "check.py")],
                                 capture_output=True, text=True, cwd=work)
            caught = out.returncode != 0 or "WARN" in out.stdout
            if caught:
                print(f"  caught  {label}")
            else:
                fails.append(f"{label}: NOT caught")
                print(f"  MISSED  {label}")

    print()
    if fails:
        print(f"{len(fails)} of {len(SELFTEST)} mutations were not caught:")
        for f in fails:
            print(f"  - {f}")
        print("\nA check that stays true when the error happens is not a check.")
        return 1
    print(f"All {len(SELFTEST)} mutations caught.")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
