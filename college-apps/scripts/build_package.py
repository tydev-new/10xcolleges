#!/usr/bin/env python3
"""Build the interim counselor package: one self-contained HTML file.

Everything is inlined (no external CSS/JS/fonts) so it survives being emailed, dropped
in a Drive folder, or opened offline. Print stylesheet included — the counselor gets a
clean PDF from Cmd-P with no navigation chrome.

Usage:
    build_package.py students/maya-rodriguez
    build_package.py students/maya-rodriguez --pdf     # also render PDF if possible
"""

import argparse
import html
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("markdown not installed. Run: .venv/bin/pip install markdown")

MD = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])

TIER_ORDER = {"reach": 0, "target": 1, "safety": 2}
TIER_LABEL = {
    "reach": "Reach",
    "target": "Target",
    "safety": "Safety",
}

CSS = """
:root{
  --ink:#1a1c20; --muted:#5b6270; --line:#dfe3ea; --bg:#ffffff; --panel:#f7f9fc;
  --accent:#1f3864; --reach:#b4472f; --target:#2b6a4d; --safety:#4a5aa8;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --ink:#e8eaee; --muted:#a2abbb; --line:#333947; --bg:#15171c; --panel:#1d2029;
    --accent:#8fb4ee; --reach:#e58a6f; --target:#6fc79b; --safety:#9aa8e8;
  }
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;}
.wrap{max-width:52rem;margin:0 auto;padding:2.5rem 1.25rem 5rem}
header.top{border-bottom:3px solid var(--accent);padding-bottom:1rem;margin-bottom:.5rem}
h1{font-size:1.85rem;margin:0 0 .2rem}
h2{font-size:1.25rem;margin:2.5rem 0 .75rem;padding-bottom:.35rem;
  border-bottom:1px solid var(--line)}
h3{font-size:1.02rem;margin:1.5rem 0 .4rem}
.sub{color:var(--muted);font-size:.92rem}
.badge{display:inline-block;padding:.12rem .5rem;border-radius:999px;font-size:.75rem;
  font-weight:600;letter-spacing:.02em;border:1px solid currentColor}
.reach{color:var(--reach)} .target{color:var(--target)} .safety{color:var(--safety)}
.agent{color:var(--reach)} .example{color:var(--muted)} .student{color:var(--target)}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:10px;
  padding:1rem 1.15rem;margin:1rem 0}
.ask{border-left:4px solid var(--accent)}
table{border-collapse:collapse;width:100%;font-size:.9rem;margin:.75rem 0}
th,td{text-align:left;padding:.5rem .6rem;border-bottom:1px solid var(--line);
  vertical-align:top}
th{font-weight:600;color:var(--muted);font-size:.78rem;text-transform:uppercase;
  letter-spacing:.04em}
.scroll{overflow-x:auto}
details{border:1px solid var(--line);border-radius:8px;margin:.6rem 0;background:var(--panel)}
details>summary{cursor:pointer;padding:.7rem 1rem;font-weight:600;list-style:none}
details>summary::-webkit-details-marker{display:none}
details>summary::before{content:"\\25B8 ";color:var(--muted)}
details[open]>summary::before{content:"\\25BE "}
details .body{padding:0 1rem 1rem;border-top:1px solid var(--line)}
blockquote{margin:.6rem 0;padding:.35rem 0 .35rem .9rem;border-left:3px solid var(--line);
  color:var(--muted)}
code{background:var(--panel);padding:.1rem .3rem;border-radius:4px;font-size:.87em}
.todo{color:var(--reach);font-weight:600}
footer{margin-top:3rem;padding-top:1rem;border-top:1px solid var(--line);
  color:var(--muted);font-size:.82rem}
ol.qs li{margin-bottom:.6rem}
.note{font-size:.85rem;color:var(--muted)}
@media print{
  :root{--ink:#000;--muted:#444;--line:#bbb;--bg:#fff;--panel:#f4f4f4;--accent:#1f3864}
  body{font-size:11pt}
  .wrap{max-width:none;padding:0}
  details{border:none;background:none}
  details>summary{padding-left:0}
  details .body{border:none;padding-left:0}
  details:not([open])>.body{display:block}
  h2{page-break-after:avoid} tr{page-break-inside:avoid}
  .noprint{display:none}
}
"""


def md(text):
    """Render embedded student/agent markdown to HTML.

    Angle brackets are escaped first. python-markdown passes raw HTML straight through,
    so an essay containing ordinary prose like `I thought <I could do better>` silently
    loses that span to an unknown tag in the counselor's copy — and a `<script>` in any
    file that reached a student folder would execute in a document this workflow
    explicitly emails around. Escaping leaves real markdown structure (#, *, |, `)
    untouched, so only the HTML injection path closes.
    """
    MD.reset()
    return MD.convert(html.escape(text or "", quote=False))


# Matches a TODO whether it sits at line start or as a list item ("- TODO:", "* TODO:",
# "1. TODO:"). Both forms occur in the templates, and counting only the bare form
# silently under-reports how much is still open.
TODO_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])?\s*TODO:", re.M)


def read(p):
    return p.read_text() if p.exists() else ""


def strip_h1(text):
    """Drop a leading H1 — the section already has its own heading."""
    return re.sub(r"\A\s*#\s+.*?\n", "", text or "", count=1)


def demote(text, levels=2):
    """Push embedded-file headings below the package's own h2 sections.

    Without this, a `## Fit` inside a research dossier renders as a sibling of
    "College research" itself, and the document outline reads as nonsense.
    """
    def sub(m):
        return "#" * min(len(m.group(1)) + levels, 6) + " "
    return re.sub(r"^(#{1,6})\s+", sub, text or "", flags=re.M)


def section_snapshot(profile):
    """Pull the top of profile.md through the goals section as the snapshot."""
    if not profile:
        return '<p class="todo">No profile.md yet — run the student-intake skill.</p>'
    body = strip_h1(profile)
    todos = len(TODO_RE.findall(body))
    out = md(demote(body, 1))
    if todos:
        out += (f'<p class="todo">{todos} item(s) still marked TODO in the profile — '
                "these are open questions, not oversights.</p>")
    return out


def section_criteria(sd):
    """What the student said they wanted — the checklist the list is measured against.

    Placed before the list so a counselor reads the criteria first and can react to the
    reasoning rather than only to the school names.
    """
    text = read(sd / "criteria.md")
    if not text.strip():
        return ('<p class="todo">No criteria.md yet — run student-intake, or have the '
                "student fill in the criteria worksheet.</p>")
    todos = len(TODO_RE.findall(text))
    out = md(demote(strip_h1(text)))
    if todos:
        out += (f'<p class="todo">{todos} open question(s) in the criteria — these are '
                "things that would sharpen the list but aren't settled yet.</p>")
    return out


def section_list(colleges):
    if not colleges:
        return '<p class="todo">No college list yet — run the college-list skill.</p>'

    rows = sorted(colleges, key=lambda c: (TIER_ORDER.get(c.get("tier"), 9),
                                           c.get("deadline") or "9999"))
    counts = {t: sum(1 for c in colleges if c.get("tier") == t)
              for t in ("reach", "target", "safety")}

    balance = (
        f'<p class="note">{counts["reach"]} reach &middot; {counts["target"]} target '
        f'&middot; {counts["safety"]} safety, {len(colleges)} total.</p>'
    )
    if counts["safety"] < 2:
        balance += ('<p class="todo">Fewer than two safeties. This list is not yet '
                    "balanced — that is the single most important thing to fix.</p>")

    head = ("<thead><tr><th>College</th><th>Tier</th><th>Plan</th><th>Deadline</th>"
            "<th>Status</th><th>Why it's on the list</th></tr></thead>")
    body = "".join(
        "<tr>"
        f"<td><strong>{html.escape(str(c.get('name','')))}</strong></td>"
        f"<td><span class='badge {c.get('tier','')}'>"
        f"{TIER_LABEL.get(c.get('tier'),'—')}</span></td>"
        f"<td>{html.escape(str(c.get('decision_plan') or '—'))}</td>"
        f"<td>{html.escape(str(c.get('deadline') or '—'))}</td>"
        f"<td>{html.escape(str(c.get('status') or '—'))}</td>"
        f"<td>{html.escape(str(c.get('rationale') or ''))}</td>"
        "</tr>"
        for c in rows
    )
    return balance + f'<div class="scroll"><table>{head}<tbody>{body}</tbody></table></div>'


def section_research(sd, colleges):
    files = sorted((sd / "research").glob("*.md")) if (sd / "research").exists() else []
    if not files:
        return '<p class="todo">No research dossiers yet — run the college-research skill.</p>'

    parts = []
    for f in files:
        text = read(f)
        m = re.search(r"\A\s*#\s+(.*)", text)
        title = m.group(1).strip() if m else f.stem.replace("-", " ").title()
        parts.append(
            f"<details><summary>{html.escape(title)}</summary>"
            f'<div class="body">{md(demote(strip_h1(text)))}</div></details>'
        )
    return "".join(parts)


from provenance import draft_provenance  # noqa: E402  (shared with check_student.py)


def check_draft_labels(sd):
    """Refuse to build a package containing an undeclared draft.

    The essay skill promises a counselor that agent-written prose is never presented as
    the student's own work. That promise was model discipline only — nothing verified
    it. An unlabeled draft is exactly the failure this guards: it renders identically to
    a student's, and a counselor who later reads the submitted essay notices.
    """
    base = sd / "essays"
    if not base.exists():
        return
    unlabeled = [
        f for d in base.iterdir() if d.is_dir()
        for f in sorted(d.glob("draft-*.md"))
        if draft_provenance(read(f))[0] is None
    ]
    if unlabeled:
        lines = "\n".join(f"    {f.relative_to(sd)}" for f in unlabeled)
        sys.exit(
            "Draft(s) with no provenance header:\n"
            f"{lines}\n\n"
            "Every draft must open with one of:\n"
            "    > **STUDENT DRAFT**\n"
            "    > **AGENT FIRST DRAFT — ...**\n"
            "    > **EXAMPLE — ... Do not submit.**\n\n"
            "Refusing to build a package that could present agent prose as the "
            "student's own work."
        )


def section_essays(sd):
    base = sd / "essays"
    dirs = sorted(d for d in base.iterdir() if d.is_dir()) if base.exists() else []
    if not dirs:
        return '<p class="todo">No essays started yet — run the essay-coach skill.</p>'

    rows, details = [], []
    for d in dirs:
        drafts = sorted(d.glob("draft-*.md"))
        reviews = sorted(d.glob("review-*.md"))
        brief = d / "brief.md"
        latest = drafts[-1] if drafts else None
        college, _, prompt = d.name.partition("--")
        title = (f"{college.replace('-', ' ').title()} — "
                 f"{prompt.replace('-', ' ') or 'personal statement'}")
        status = (f"draft {len(drafts)}" if drafts else
                  ("brief only" if brief.exists() else "not started"))
        words = len(read(latest).split()) if latest else 0
        kind, label = draft_provenance(read(latest)) if latest else (None, None)

        rows.append(
            "<tr>"
            f"<td>{html.escape(college.replace('-', ' ').title())}</td>"
            f"<td>{html.escape(prompt.replace('-', ' '))}</td>"
            f"<td>{status}</td>"
            f"<td>{words or '—'}</td>"
            f"<td>{len(reviews)}</td>"
            + (f"<td><span class='badge {kind}'>{html.escape(label)}</span></td>"
               if kind else "<td>—</td>")
            + "</tr>"
        )

        # The brief carries the rubric and the chosen angle — the thing a counselor can
        # most usefully push back on while the essay is still changeable.
        if brief.exists():
            details.append(
                f"<details><summary>{html.escape(title)} — brief (rubric &amp; angle)"
                f"</summary><div class=\"body\">{md(demote(strip_h1(read(brief))))}"
                "</div></details>"
            )
        if latest:
            warn = ('<p class="todo">This draft is agent-written scaffolding. It is not '
                    "the student's work and must be rewritten before submission.</p>"
                    if kind == "agent" else "")
            details.append(
                f"<details><summary>{html.escape(title)} ({latest.stem})</summary>"
                f'<div class="body">{warn}{md(demote(read(latest)))}</div></details>'
            )

    head = ("<thead><tr><th>College</th><th>Prompt</th><th>Status</th>"
            "<th>Words</th><th>Rounds</th><th>Latest draft by</th></tr></thead>")
    return (f'<div class="scroll"><table>{head}<tbody>{"".join(rows)}</tbody></table></div>'
            + '<p class="note">Every draft declares its author in its header, and the '
              "package will not build if one doesn't. Briefs and current drafts below.</p>"
            + "".join(details))


def section_recs(sd, meta):
    recs = meta.get("recommenders", [])
    parts = []
    if recs:
        head = ("<thead><tr><th>Recommender</th><th>Subject</th><th>Asked</th>"
                "<th>Agreed</th><th>Brag sheet sent</th><th>Submitted</th></tr></thead>")
        body = "".join(
            "<tr>"
            f"<td>{html.escape(str(r.get('name','')))}</td>"
            f"<td>{html.escape(str(r.get('subject') or '—'))}</td>"
            f"<td>{html.escape(str(r.get('asked_on') or '—'))}</td>"
            f"<td>{html.escape(str(r.get('agreed') or '—'))}</td>"
            f"<td>{html.escape(str(r.get('brag_sheet_sent') or '—'))}</td>"
            f"<td>{html.escape(str(r.get('submitted') or '—'))}</td>"
            "</tr>" for r in recs
        )
        parts.append(f'<div class="scroll"><table>{head}<tbody>{body}</tbody></table></div>')
    else:
        parts.append('<p class="todo">No recommenders recorded yet.</p>')

    base = sd / "recs"
    if base.exists():
        for prefix, label in (("brag-sheet--", "Brag sheet"),
                              ("request--", "Request to send")):
            for f in sorted(base.glob(f"{prefix}*.md")):
                who = f.stem.replace(prefix, "").replace("-", " ").title()
                parts.append(
                    f"<details><summary>{label} — {html.escape(who)}</summary>"
                    f'<div class="body">{md(demote(strip_h1(read(f))))}</div></details>'
                )
    return "".join(parts)


def section_asks(sd, meta):
    """The point of the package: what we actually want back from the counselor."""
    custom = read(sd / "counselor-questions.md")
    if custom.strip():
        return md(strip_h1(custom))

    colleges = meta.get("colleges", [])
    safeties = sum(1 for c in colleges if c.get("tier") == "safety")
    qs = [
        "Does the tiering look right to you? You know how our applicants have actually "
        "fared at these schools — Scorecard data doesn't capture that.",
        "Are there schools you'd add that we've missed, especially ones where our "
        "students tend to do well?",
    ]
    if safeties < 2:
        qs.insert(0, "We're light on safeties. Which schools would you point to that this "
                     "student would genuinely be happy attending?")
    qs += [
        "For the counselor letter: is there context about the school profile, our course "
        "offerings, or grading that admissions readers should have?",
        "Do the teacher recommender choices make sense, or would you steer differently?",
        "Anything in the timeline that looks unrealistic given what else this student "
        "has going on this fall?",
    ]
    items = "".join(f"<li>{html.escape(q)}</li>" for q in qs)
    return (f'<div class="panel ask"><p><strong>Where we would most value your '
            f"input:</strong></p><ol class='qs'>{items}</ol>"
            '<p class="note">Reply however is easiest — inline, email, or a five-minute '
            "conversation. Anything you flag gets folded into the next revision.</p></div>")


def build(sd, meta):
    check_draft_labels(sd)
    name = meta.get("name") or sd.name.replace("-", " ").title()
    today = date.today().isoformat()
    profile = read(sd / "profile.md")
    colleges = meta.get("colleges", [])

    parts = [
        '<div class="wrap">',
        '<header class="top">',
        f"<h1>{html.escape(name)} — College Application Package</h1>",
        f'<p class="sub">Interim draft for counselor review &middot; {today}'
        + (f" &middot; Class of {meta['grad_year']}" if meta.get("grad_year") else "")
        + "</p>",
        "</header>",
        '<div class="panel"><p><strong>What this is.</strong> A work-in-progress '
        "snapshot of where this student stands: who they are, the list so far and why, "
        "what the research says, and where the essays and recommendations sit. "
        "Nothing here is final. The last section is what we would most like your read "
        "on.</p></div>",
        "<h2>Where we'd value your input</h2>", section_asks(sd, meta),
        "<h2>Student snapshot</h2>", section_snapshot(profile),
        "<h2>What they're looking for</h2>", section_criteria(sd),
        "<h2>The list</h2>", section_list(colleges),
        "<h2>College research</h2>", section_research(sd, colleges),
        "<h2>Essays</h2>", section_essays(sd),
        "<h2>Recommendations</h2>", section_recs(sd, meta),
        "<footer>Generated by the 10xcolleges counselor-package skill on "
        f"{today}. College facts carry their source and vintage inline; anything marked "
        '"needs checking" was not verifiable and should not be treated as known. '
        "Admission tiers are judgments, not predictions.</footer>",
        "</div>",
    ]

    return (f"<title>{html.escape(name)} — Application Package</title>"
            f"<style>{CSS}</style>" + "\n".join(parts))


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("student_dir")
    p.add_argument("-o", "--out")
    p.add_argument("--pdf", action="store_true", help="also render PDF via headless Chrome")
    args = p.parse_args()

    sd = Path(args.student_dir)
    if not sd.exists():
        sys.exit(f"No such student directory: {sd}")
    meta_path = sd / "meta.json"
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}

    out = Path(args.out) if args.out else sd / "out" / "package.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(sd, meta))
    print(f"Wrote {out}")

    if args.pdf:
        chrome = next(
            (c for c in [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Chromium.app/Contents/MacOS/Chromium",
                "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            ] if Path(c).exists()),
            None,
        )
        pdf = out.with_suffix(".pdf")
        if not chrome:
            print("  no Chrome/Chromium/Edge found — open the HTML and Cmd-P to PDF")
            return
        subprocess.run(
            [chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer",
             f"--print-to-pdf={pdf}", out.resolve().as_uri()],
            check=False, capture_output=True, timeout=120,
        )
        print(f"Wrote {pdf}" if pdf.exists() else "  PDF render failed — use Cmd-P instead")


if __name__ == "__main__":
    main()
