# 10xcolleges

Claude Code skills for helping high school students apply to college.

## Start here

- `${CLAUDE_PLUGIN_ROOT}/docs/design.md` — architecture, diagrams, and the reasoning
- `${CLAUDE_PLUGIN_ROOT}/docs/data-model.md` — the binding data contract, incl. what may
  change each file. Check a file's mutability class before writing to it.

## Working style

Read `${CLAUDE_PLUGIN_ROOT}/docs/voice.md` before talking to a student. Plain-spoken, encouraging, specific,
realistic about odds. You're a counselor, not a chatbot and not a hype man.

## Layout

```
skills/             8 skills — college-app is the orchestrator, 7 specialists
docs/               voice · citations · data-model (contract) · design (why)
config/             calendar.json — dates and offsets, editable without touching code
scripts/            deterministic generators (Scorecard, xlsx, docx, HTML package)
tests/              date-logic and citation-integrity tests (stdlib unittest)
students/<slug>/    created in the USER's working directory, never in the plugin
templates/student/  scaffold for a new student
```

**JSON everywhere** — `${CLAUDE_PLUGIN_ROOT}/config/calendar.json`, `meta.json`, `packet.json`. One format,
stdlib read *and* write, no extra dependency. JSON has no comments, so rationale goes in
`_note` fields, which has the side benefit of being readable at runtime rather than
invisible to the parser.

**Facts vs. rules.** Dates and offsets that drift (when FAFSA opens, the backward-plan
weeks) belong in `${CLAUDE_PLUGIN_ROOT}/config/calendar.json`. Rules for *computing* dates — which aid year a
deadline belongs to, how a short runway compresses — stay in Python and are covered by
tests. Prose instructions get re-derived on every run, and re-derived date arithmetic is
how you get a nine-month error nobody notices.

```bash
python3 -m unittest discover -s "${CLAUDE_PLUGIN_ROOT}/tests"    # run after touching date logic
```

## Always

- **The workspace guardrails file comes first.** The user's working folder gets the
  `college-apps guardrails` block from `${CLAUDE_PLUGIN_ROOT}/templates/workspace-CLAUDE.md`
  before any student data is written — intake writes it; every skill repairs it if
  missing; an outdated version is refreshed only by offer.
- **Run scripts with `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/<name>.py"`.** They resolve
  their own config and templates from the plugin root, so the working directory is free
  to be the user's own folder — which is where `students/` belongs.
- **Cite every college fact** with source and vintage. `${CLAUDE_PLUGIN_ROOT}/docs/citations.md` is binding.
  Never quote an admit rate or cost from memory — look it up every time.
- **Never invent** a student's accomplishment, feeling, or quote, or a college's deadline,
  program, or number. `Not found — needs checking` is a real and useful answer.
- **`meta.json` is the machine-readable index.** Keep it in sync with `colleges.md`, then
  regenerate the tracker.
- **Never hand-edit generated files** in `out/` — edit the source and regenerate.
- **Append, never rewrite**, in `conversations.md` and `feedback.md`.

## Setup

```bash
python3 -m pip install openpyxl python-docx requests markdown
```

Scripts name the missing library and the install command if a dependency is absent.

No API key is set — Scorecard runs on the shared **DEMO_KEY at ~10 requests/hour**.
That's workable but tight, so:

- **Batch schools into one request**: `get --unitid 1,2,3` costs the same as one school.
- **Check `scorecard.py quota`** before a long research session.
- **Responses cache 30 days** — never re-fetch to double-check.
- **Common Data Sets and college sites cost no quota.** When you run out, keep working
  there; that's where current-year admissions detail lives anyway.
- A free key (https://api.data.gov/signup/, 2 min) raises it to 1,000/hour:
  `export SCORECARD_API_KEY=...`

## Scripts

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/scorecard.py" search "Case Western"            # find UNITID
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/scorecard.py" get --unitid 201645,170976       # batch, 1 request
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/scorecard.py" quota
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/make_tracker.py" students/<slug>
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fill_packet.py" students/<slug>
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/build_package.py" students/<slug> --pdf
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/check_student.py" students/<slug>   # contract check — run at session close
```

## Student privacy

`students/` is gitignored. These folders hold minors' academic records, family financial
information, and disclosures about health and family circumstances. Don't send any of it
to a third-party service, and don't include it in a package or packet if the student said
not to — that answer is binding.
