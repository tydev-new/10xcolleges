#!/usr/bin/env python3
"""College Scorecard lookup with honest data vintages.

The Scorecard API's `latest.*` alias hides *which year* a number comes from, which makes
it impossible to cite properly. So for the numbers students actually quote — admit rate,
cost, net price — we probe explicit year-prefixed fields and report the newest year that
actually has data.

Usage:
    scorecard.py search "Michigan"                    # find candidates + UNITIDs
    scorecard.py get "University of Michigan"         # full dossier, markdown
    scorecard.py get --unitid 170976,201645,167358    # several schools, ONE request
    scorecard.py get --unitid 170976 --json           # machine-readable
    scorecard.py quota                                # requests left this hour

API key:
    Falls back to DEMO_KEY: ~10 requests/hour, shared per-IP. Workable, but batch your
    lookups — `get --unitid a,b,c` costs one request no matter how many schools.
    export SCORECARD_API_KEY=...   # free, 2 min, 1,000/hr: https://api.data.gov/signup/

Responses are cached under .cache/scorecard/ for 30 days so repeated dossier builds
don't burn the rate limit.
"""

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import date
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("requests not installed. Run: .venv/bin/pip install requests")

API = "https://api.data.gov/ed/collegescorecard/v1/schools"
# Under the user's home, never inside the plugin: an installed plugin directory may be
# read-only, and Cowork warns when plugin files change beneath it.
CACHE_DIR = Path(
    os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")
) / "10xcolleges" / "scorecard"
CACHE_TTL = 30 * 24 * 3600

# Probe years are derived from the current year, never hardcoded: Scorecard adds a field
# year each fall, and a frozen list would silently keep reporting the older year as
# "newest" — reintroducing exactly the vintage blindness this module exists to prevent.
# Probing a year that doesn't exist yet returns null rather than erroring (verified), so
# starting at the current year is safe.
#
# Depth is per-metric because they lag differently, and because every extra year costs
# ~28 query-string fields — at 8KB the request starts to break.
CORE_DEPTH = 6   # admit rate, cost, enrollment, grad rate: ~2 year lag
DEEP_DEPTH = 9   # debt and earnings: these trail much further behind
BAND_DEPTH = 4   # net price by income band: published alongside recent cost data


def probe_years(depth, today=None):
    year = (today or date.today()).year
    return list(range(year, year - depth, -1))

STATIC_FIELDS = [
    "id",
    "school.name",
    "school.city",
    "school.state",
    "school.school_url",
    "school.price_calculator_url",
    "school.ownership",
    "school.locale",
    "school.degrees_awarded.predominant",
]

# (label, field suffix, probe depth) — probed per year to establish vintage
VERSIONED = [
    ("admit_rate", "admissions.admission_rate.overall", CORE_DEPTH),
    ("sat_25", "admissions.sat_scores.25th_percentile.overall", CORE_DEPTH),
    ("sat_75", "admissions.sat_scores.75th_percentile.overall", CORE_DEPTH),
    # Many schools report only per-section SATs; summed as a fallback below.
    ("sat_25_rw", "admissions.sat_scores.25th_percentile.critical_reading", CORE_DEPTH),
    ("sat_75_rw", "admissions.sat_scores.75th_percentile.critical_reading", CORE_DEPTH),
    ("sat_25_m", "admissions.sat_scores.25th_percentile.math", CORE_DEPTH),
    ("sat_75_m", "admissions.sat_scores.75th_percentile.math", CORE_DEPTH),
    ("act_25", "admissions.act_scores.25th_percentile.cumulative", CORE_DEPTH),
    ("act_75", "admissions.act_scores.75th_percentile.cumulative", CORE_DEPTH),
    ("size", "student.size", CORE_DEPTH),
    ("tuition_in", "cost.tuition.in_state", CORE_DEPTH),
    ("tuition_out", "cost.tuition.out_of_state", CORE_DEPTH),
    ("coa", "cost.attendance.academic_year", CORE_DEPTH),
    ("net_price_pub", "cost.avg_net_price.public", CORE_DEPTH),
    ("net_price_priv", "cost.avg_net_price.private", CORE_DEPTH),
    ("grad_rate", "completion.completion_rate_4yr_150nt", CORE_DEPTH),
    ("median_debt", "aid.median_debt.completers.overall", DEEP_DEPTH),
    ("earnings_10yr", "earnings.10_yrs_after_entry.median", DEEP_DEPTH),
]

INCOME_BANDS = ["0-30000", "30001-48000", "48001-75000", "75001-110000", "110001-plus"]

OWNERSHIP = {1: "public", 2: "private nonprofit", 3: "private for-profit"}
LOCALE = {
    11: "large city", 12: "midsize city", 13: "small city",
    21: "large suburb", 22: "midsize suburb", 23: "small suburb",
    31: "fringe town", 32: "distant town", 33: "remote town",
    41: "fringe rural", 42: "distant rural", 43: "remote rural",
}


_warned = False
QUOTA_FILE = CACHE_DIR / "quota.json"


def api_key():
    global _warned
    key = os.environ.get("SCORECARD_API_KEY", "").strip()
    if key:
        return key
    if not _warned:
        print(
            "note: using DEMO_KEY (~10 requests/hour, shared per-IP). Cached responses "
            "are free. Batch lookups with: get --unitid 1,2,3\n"
            "      A free key raises this to 1,000/hour: https://api.data.gov/signup/",
            file=sys.stderr,
        )
        _warned = True
    return "DEMO_KEY"


def record_quota(resp):
    """Track the rate-limit headers so callers can see the budget before spending it."""
    limit = resp.headers.get("X-Ratelimit-Limit")
    remaining = resp.headers.get("X-Ratelimit-Remaining")
    if remaining is None:
        return
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        QUOTA_FILE.write_text(json.dumps({
            "limit": limit, "remaining": remaining, "at": time.time(),
        }))
    except OSError:
        return
    if remaining.isdigit() and int(remaining) <= 3:
        print(f"warning: {remaining} of {limit} Scorecard requests left this hour. "
              "Cached schools still work; new ones will fail until the window resets.",
              file=sys.stderr)


def quota_status():
    if not QUOTA_FILE.exists():
        return "No requests recorded yet — full quota presumed available."
    try:
        q = json.loads(QUOTA_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return "Quota record unreadable — full quota presumed available."

    mins = int((time.time() - q["at"]) / 60)
    # The window rolls hourly, so a reading older than an hour says nothing about now.
    # Reporting a stale "0 remaining" would stall an agent that was told to check first.
    if mins >= 60:
        return (f"Last reading ({q['remaining']} of {q['limit']}) was {mins} min ago — "
                "expired. The hourly window has since reset; full quota presumed available.")
    return (f"{q['remaining']} of {q['limit']} requests remaining "
            f"as of {mins} min ago. Resets ~{60 - mins} min from now.")


def fetch(params):
    """GET with a 30-day disk cache keyed on the request params."""
    cache_key = hashlib.sha256(
        json.dumps(params, sort_keys=True).encode()
    ).hexdigest()[:32]
    cache_file = CACHE_DIR / f"{cache_key}.json"

    if cache_file.exists() and time.time() - cache_file.stat().st_mtime < CACHE_TTL:
        return json.loads(cache_file.read_text())

    resp = requests.get(API, params={**params, "api_key": api_key()}, timeout=30)
    record_quota(resp)

    # api.data.gov returns 403 for BOTH an exhausted quota and a bad API key. Reporting
    # a key problem as a rate limit sends the user off to wait an hour, repeatedly, for
    # a condition that will never clear on its own. Disambiguate from the body.
    if resp.status_code in (429, 403):
        body = resp.text[:500]
        if "API_KEY_INVALID" in body or "API_KEY_MISSING" in body:
            sys.exit(
                "Scorecard rejected the API key in SCORECARD_API_KEY.\n\n"
                "  • Check for a typo or stray whitespace in the exported value.\n"
                "  • Get a fresh key (2 min): https://api.data.gov/signup/\n"
                "  • Or unset it to fall back to DEMO_KEY: unset SCORECARD_API_KEY\n\n"
                "This is not a rate limit — waiting will not fix it."
            )
        using_demo = not os.environ.get("SCORECARD_API_KEY", "").strip()
        sys.exit(
            "Scorecard rate limit reached"
            + (" on the shared DEMO_KEY." if using_demo else ".")
            + "\n\nOptions:\n"
            "  1. Wait — the window rolls hourly.\n"
            "  2. Get a free key (2 min, no approval): https://api.data.gov/signup/\n"
            "     then: export SCORECARD_API_KEY=...\n"
            "  3. Keep working — schools already researched are cached for 30 days,\n"
            "     and Common Data Sets on the colleges' own sites cost no quota.\n"
        )
    resp.raise_for_status()
    data = resp.json()

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(json.dumps(data))
    return data


def search(name, limit=10):
    data = fetch({
        "school.name": name,
        "fields": ",".join(STATIC_FIELDS + ["latest.student.size",
                                            "latest.admissions.admission_rate.overall"]),
        "per_page": limit,
        "school.operating": 1,
    })
    return data.get("results", [])


def build_fields():
    fields = list(STATIC_FIELDS)
    for _label, suffix, depth in VERSIONED:
        for year in probe_years(depth):
            fields.append(f"{year}.{suffix}")
    for year in probe_years(BAND_DEPTH):
        for band in INCOME_BANDS:
            fields.append(f"{year}.cost.net_price.public.by_income_level.{band}")
            fields.append(f"{year}.cost.net_price.private.by_income_level.{band}")
    return fields


def newest(row, suffix, depth):
    """Return (value, year) for the newest year with a non-null value."""
    for year in probe_years(depth):
        val = row.get(f"{year}.{suffix}")
        if val is not None:
            return val, year
    return None, None


def get_many(unitids):
    """Fetch several schools in ONE request.

    This is the difference between researching a 10-school list and burning an entire
    hour of DEMO_KEY quota doing it one school at a time.
    """
    wanted = [str(u).strip() for u in unitids if str(u).strip()]
    if len(wanted) > 100:
        sys.exit(f"{len(wanted)} UNITIDs requested but the API returns at most 100 per "
                 "call. Split the batch rather than losing schools silently.")

    results = fetch({
        "id": ",".join(wanted),
        "fields": ",".join(build_fields()),
        "per_page": 100,
    }).get("results", [])

    # Reconcile against what was asked for. A wrong or retired UNITID otherwise just
    # vanishes from the batch — that college ends up with no research file at all, and
    # nothing in the output says so.
    got = {str(r.get("id")) for r in results}
    missing = [u for u in wanted if u not in got]
    if missing:
        print(f"warning: no Scorecard match for UNITID(s): {', '.join(missing)}. "
              "Verify with: scorecard.py search \"<college name>\"", file=sys.stderr)

    return [shape(r) for r in results]


def get(unitid=None, name=None):
    params = {"fields": ",".join(build_fields()), "per_page": 5}
    if unitid:
        params["id"] = unitid
    else:
        params["school.name"] = name
        params["school.operating"] = 1

    results = fetch(params).get("results", [])
    if not results:
        return None
    return shape(results[0])


def shape(row):
    out = {
        "unitid": row.get("id"),
        "name": row.get("school.name"),
        "city": row.get("school.city"),
        "state": row.get("school.state"),
        "url": row.get("school.school_url"),
        "npc_url": row.get("school.price_calculator_url"),
        "ownership": OWNERSHIP.get(row.get("school.ownership"), "unknown"),
        "locale": LOCALE.get(row.get("school.locale"), "unknown"),
        "metrics": {},
        "net_price_by_income": {},
    }

    for label, suffix, depth in VERSIONED:
        val, year = newest(row, suffix, depth)
        out["metrics"][label] = {"value": val, "year": year}

    # Fall back to summing per-section SATs when a school reports no composite.
    for lo_hi in ("25", "75"):
        comp = out["metrics"][f"sat_{lo_hi}"]
        if comp["value"] is None:
            rw = out["metrics"][f"sat_{lo_hi}_rw"]
            mt = out["metrics"][f"sat_{lo_hi}_m"]
            if rw["value"] is not None and mt["value"] is not None:
                comp["value"] = rw["value"] + mt["value"]
                comp["year"] = min(rw["year"], mt["year"])

    is_public = row.get("school.ownership") == 1
    out["is_public"] = is_public
    sector = "public" if is_public else "private"
    for band in INCOME_BANDS:
        val, year = newest(row, f"cost.net_price.{sector}.by_income_level.{band}",
                            BAND_DEPTH)
        if val is not None:
            out["net_price_by_income"][band] = {"value": val, "year": year}

    return out


def money(v):
    return f"${v:,.0f}" if isinstance(v, (int, float)) else "not reported"


def pct(v):
    return f"{v * 100:.1f}%" if isinstance(v, (int, float)) else "not reported"


def cite(entry, formatter):
    val, year = entry["value"], entry["year"]
    if val is None:
        return "Not found — needs checking"
    return f"{formatter(val)} (Scorecard, {year}-{str(year + 1)[2:]} field year)"


def oos_note(m, is_public):
    """Out-of-state sticker estimate for publics, only when the vintages agree.

    The arithmetic is coa + (tuition_out - tuition_in), but each term is resolved
    independently by newest() and can land on a different field year. Adding a current
    COA to a three-year-old tuition delta produces a confident, unlabeled, wrong number
    — in a module whose whole premise is that a cost figure without a year is not a
    citation.
    """
    if not is_public:
        return ""
    keys = ("coa", "tuition_out", "tuition_in")
    if any(m[k]["value"] is None for k in keys):
        return ""

    years = {m[k]["year"] for k in keys}
    est = money(m["coa"]["value"] + m["tuition_out"]["value"] - m["tuition_in"]["value"])
    if len(years) == 1:
        year = years.pop()
        return (f"  \n  *Out-of-state students at this public pay roughly {est} "
                f"(Scorecard, {year}-{str(year + 1)[2:]} field year) — Scorecard's COA "
                "covers in-state only.*")
    return (f"  \n  *Out-of-state sticker is roughly {est}, but this mixes field years "
            f"({', '.join(str(y) for y in sorted(years, reverse=True))}) — treat it as "
            "an estimate and confirm against the college's own cost page.*")


def render(d):
    m = d["metrics"]
    lines = [
        f"# {d['name']}",
        "",
        f"{d['city']}, {d['state']} — {d['ownership']}, {d['locale']}",
        f"UNITID {d['unitid']}" + (f" — <{d['url']}>" if d.get("url") else ""),
        "",
        "## Scorecard facts",
        "",
        f"- **Admit rate:** {cite(m['admit_rate'], pct)}",
        f"- **Undergrad enrollment:** {cite(m['size'], lambda v: f'{v:,}')}",
        f"- **SAT middle 50%:** "
        + (
            f"{m['sat_25']['value']:.0f}–{m['sat_75']['value']:.0f} "
            f"(Scorecard, {m['sat_75']['year']} field year)"
            if m["sat_25"]["value"] and m["sat_75"]["value"]
            else "Not found — needs checking"
        ),
        f"- **ACT middle 50%:** "
        + (
            f"{m['act_25']['value']:.0f}–{m['act_75']['value']:.0f} "
            f"(Scorecard, {m['act_75']['year']} field year)"
            if m["act_25"]["value"] and m["act_75"]["value"]
            else "Not found — needs checking"
        ),
        f"- **4-yr grad rate (150% time):** {cite(m['grad_rate'], pct)}",
        "",
        "## Cost",
        "",
        f"- **Tuition, in-state:** {cite(m['tuition_in'], money)}",
        f"- **Tuition, out-of-state:** {cite(m['tuition_out'], money)}",
        # Scorecard reports academic-year COA for in-state/in-district students at
        # publics. Printing that unlabeled beside a $60k out-of-state tuition would
        # badly understate the real cost for an out-of-state applicant.
        f"- **Cost of attendance (sticker{', in-state' if d.get('is_public') else ''}):** "
        + cite(m["coa"], money)
        + oos_note(m, d.get("is_public")),
        f"- **Average net price:** "
        + cite(
            m["net_price_pub"] if m["net_price_pub"]["value"] else m["net_price_priv"],
            money,
        ),
        f"- **Median debt at graduation:** {cite(m['median_debt'], money)}",
        f"- **Median earnings, 10 yrs after entry:** {cite(m['earnings_10yr'], money)}",
    ]

    if d["net_price_by_income"]:
        lines += ["", "### Average net price by family income", ""]
        labels = {
            "0-30000": "Under $30k",
            "30001-48000": "$30–48k",
            "48001-75000": "$48–75k",
            "75001-110000": "$75–110k",
            "110001-plus": "$110k+",
        }
        for band, entry in d["net_price_by_income"].items():
            lines.append(f"- {labels[band]}: {cite(entry, money)}")

    if d.get("npc_url"):
        npc = d["npc_url"]
        if not npc.startswith("http"):
            npc = "https://" + npc
        lines += [
            "",
            f"**Run the Net Price Calculator** for a real number: <{npc}>",
            "",
            "*Net price is what families actually pay after grants. The sticker price "
            "above is what almost nobody pays at a well-endowed private, and roughly "
            "what everyone pays as an out-of-state public applicant.*",
        ]

    lines += [
        "",
        "---",
        "*Source: US Dept. of Education College Scorecard. Federal data lags ~2 years — "
        "check the college's own Common Data Set for current-year admissions detail, and "
        "the college's own site for deadlines.*",
    ]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="find schools by name")
    s.add_argument("name")
    s.add_argument("--limit", type=int, default=10)

    g = sub.add_parser("get", help="full dossier for one or more schools")
    g.add_argument("name", nargs="?")
    g.add_argument("--unitid", help="one UNITID, or several comma-separated "
                                    "(one request for all of them)")
    g.add_argument("--json", action="store_true")

    sub.add_parser("quota", help="how many requests are left this hour")

    args = p.parse_args()

    if args.cmd == "quota":
        print(quota_status())
        return

    if args.cmd == "search":
        rows = search(args.name, args.limit)
        if not rows:
            print(f"No match for {args.name!r}.")
            return
        for r in rows:
            rate = r.get("latest.admissions.admission_rate.overall")
            size = r.get("latest.student.size")
            print(
                f"{r['id']:>8}  {r['school.name']} "
                f"({r.get('school.city')}, {r.get('school.state')}) "
                f"— admit {pct(rate)}, {size:,} undergrads" if size else
                f"{r['id']:>8}  {r['school.name']}"
            )
        return

    if not args.name and not args.unitid:
        sys.exit("Give a name or --unitid.")

    if args.unitid and "," in str(args.unitid):
        rows = get_many(str(args.unitid).split(","))
        if not rows:
            sys.exit("No matches for those UNITIDs.")
        print(json.dumps(rows, indent=2) if args.json
              else "\n\n---\n\n".join(render(r) for r in rows))
        return

    d = get(unitid=args.unitid, name=args.name)
    if not d:
        sys.exit(f"No match. Try: scorecard.py search {args.name!r}")
    print(json.dumps(d, indent=2) if args.json else render(d))


if __name__ == "__main__":
    main()
