# 10xcolleges

A Claude plugin that works through college applications the way a good high school
counselor would: builds a balanced list, researches schools with cited sources, coaches
essays without ghostwriting them, plans recommendation letters, tracks every deadline, and
packages the whole thing for a school counselor to review.

Plain-spoken, encouraging, and honest about odds. It will tell a student that a 5% school
is a lottery ticket, and then help them apply anyway if they want to.

---

## What's ready now — the first wave

Two skills are built, reviewed, and measured; the rest of the plugin still works but
hasn't been through the same process yet.

| Skill | What it does for you | How it's kept honest |
|---|---|---|
| **student-intake** | Sets up your folder, reads your packet or transcript, then interviews you — two or three questions at a time — until the college list has what it needs: a budget (and who set it), your unweighted GPA, a direction, and what you want and don't want. Everything in your words, every line tagged with where it came from, blanks left as blanks. | A script checks the files after every turn: no untagged line, no blank filled with a guess, and it counts the gate (`gate N/4`) so a guessed budget never passes as a real one. |
| **essay-coach** | One essay at a time — you name it ("the Pomona one"). Writes a brief first: what the prompt really asks, a rubric from the college's own guidance where it exists, angles from things you've actually done. Then reviews draft by draft: a score against the rubric, the one big thing to change, line fixes, one real question. Your own read of your draft is welcome and optional. Two rounds at the same score and it changes the approach instead of nagging. | Every draft says who wrote it on its first line; a script refuses to build a package without it. Nothing in an agent draft can be a fact that isn't in your record. A second, blind reader gives three lines on every draft. Reviews are never edited after the fact. |

Both were measured with a simulated student over multi-turn conversations (the test
harness is in `college-apps/tests/always-on/`; the results are in
`college-apps/docs/evals/eval-first-wave-2026-08-22.md`). What they will not do: write
your essay, name a college during intake, guess a number, or look outside the folder you
chose.

---

## Install

### In Claude Cowork

1. Open **Customize** in the sidebar, then **Plugins**.
2. Select **Add marketplace** and enter:

   ```
   tydev-new/10xcolleges
   ```

3. **College Applications** appears in the list. Click **Install**.

That's it. The eight skills load automatically and activate when you mention anything
about applying to college.

### In Claude Code

```
/plugin marketplace add tydev-new/10xcolleges
/plugin install college-apps@10xcolleges
```

### One-time setup

The spreadsheet, Word, and web outputs need four Python libraries:

```bash
python3 -m pip install openpyxl python-docx requests markdown
```

If you skip this, the skills still work — the scripts just tell you which library is
missing when you first generate a file.

**College data works out of the box.** It uses the US Department of Education's College
Scorecard on a shared demo key, which allows about 10 lookups an hour. The plugin is built
for that: it fetches a whole college list in a single request and caches results for 30
days. When it starts getting in the way, a free key takes two minutes with no approval
wait and raises the limit to 1,000/hour:

```bash
export SCORECARD_API_KEY=your_key_here   # https://api.data.gov/signup/
```

---

## Using it

Just say what you need. The plugin figures out where you are and what comes next.

**Starting out** — hand it whatever your school gave you:

> Help me get started with my college applications. Here's my counselor packet:
> ~/Downloads/Post-Secondary Options Packet.pdf

First it settles where your files live — usually the folder you opened, named as a path;
if that looks like the wrong place (a code project, your home folder) it asks, and writes
nothing until you answer. Then it reads the packet and interviews you — not a form, a
conversation. What you want to
study, how sure you are, what you'd do on a free Saturday, and what turns you off. That
last question narrows a list faster than anything else and almost nobody asks it.

It will also ask what your family can spend. If nobody has had that conversation yet,
that's the most useful thing it can tell you in September rather than April.

**Building a list:**

> Where should I apply? I want mechanical engineering, in-state or nearby, under $25k a year.

You get 8–12 schools in three tiers with the reasoning for each, checked against real
admit rates and real net prices. A school you can get into but can't afford is not counted
as a safety.

**Researching a school:**

> What's Northeastern actually like for computer science? Can we afford it?

**Essays** — you name the essay, and it has a choice built into it:

> Here's the Michigan supplement: "Describe the unique qualities that attract you..."

It starts by decoding what the prompt is really asking, writing a rubric, and proposing
three or four angles drawn from things you've actually done. Then it asks how you want the
first draft to happen:

- **You write it.** Slowest, best result — the voice is yours from the start.
- **You see a sample first.** A short passage on a *different* topic, so you can see what
  specificity looks like before facing a blank page.
- **It drafts first.** Fastest start, built only from your own material. Clearly labeled,
  and handed back with instructions to rewrite it from scratch rather than edit it.

Reviews score the draft against the rubric (`3/5`), tell you what's working, the one
biggest thing to change, a few line fixes, and one real question. They never rewrite your
sentences for you. If you want to score your own draft first, it takes your read and shows
you where you differ — that gap is the coaching. Two drafts at the same score and it
stops asking for another round and offers a different move.

**Recommendation letters:**

> I need to ask Ms. Alvarez for a letter. Can you help me put something together?

You get a brag sheet built for *that* teacher — specific moments from their classroom,
including the bad test you recovered from — plus the ask itself.

**Staying on top of it:**

> What do I need to do this week?

**Sharing with your counselor:**

> Can you put together something I can send Mr. Reyes?

---

## What you get

| File | What it is |
|---|---|
| `students/<name>/profile.md` | Everything about you, with every line tagged by source |
| `students/<name>/criteria.md` | What you're looking for — the checklist your list is measured against |
| `students/<name>/colleges.md` | The list, with the reasoning and the numbers |
| `students/<name>/research/*.md` | A cited dossier per school |
| `students/<name>/essays/…` | Brief, then every draft and review, never overwritten |
| `students/<name>/recs/…` | Brag sheets and request emails |
| `students/<name>/out/tracker.xlsx` | Deadlines plus a task list built backwards from each one |
| `students/<name>/out/package.html` | A counselor-ready review document (prints to PDF) |
| `students/<name>/out/packet.docx` | Your school's own packet, filled in |

Everything lives in your working folder as plain files you can read, edit, and keep.

---

## What it won't do

- **Quote a college fact without a source and a date.** Every admit rate, cost, and
  deadline carries where it came from and what year it's from. Numbers move; memory is
  stale. When something can't be verified it says "needs checking" instead of guessing.
- **Invent anything about you.** Not an award, not a number of volunteer hours, not a
  feeling. If it isn't in your profile or something you said, it asks.
- **Give you a percentage.** "You have a 34% chance at Michigan" is false precision
  dressed up as expertise. You get tiers and the reasoning behind them.
- **Call a school a safety when your family can't pay for it.**
- **Pass its own writing off as yours.** Every draft records who wrote it, and the
  counselor package refuses to build if one doesn't — so an agent-written draft can never
  quietly reach a counselor as your work.

---

## Where the numbers come from

**College Scorecard** (US Dept. of Education) for admit rates, net price by family income,
graduation rates, and earnings — reported with the actual data year rather than hidden
behind a "latest" label.

**Each college's Common Data Set** for current-year admissions detail, especially section
C7, which states in the school's own words how much they weigh essays, recommendations,
and demonstrated interest. It's the most useful and least-known document in admissions.

**The college's own website** for deadlines and required essays. Nothing else counts for a
deadline.

Ranking and review sites are used only for campus texture, always labeled as impression
rather than fact.

---

## Adjusting it

Dates drift. `college-apps/config/calendar.json` holds the ones that do — when FAFSA opens,
how many weeks before a deadline to ask for recommendations, the default key dates — so you
can correct them without touching any code. Each carries a note explaining why it's set the
way it is.

---

## Your data stays yours

Student folders are gitignored and never leave your machine unless you send them
somewhere. These files hold a minor's academic record, family financial details, and
sometimes disclosures about health or family circumstances. If a student says something
shouldn't go in their counselor letter, that answer is treated as binding everywhere.

---

## Development

```bash
git clone https://github.com/tydev-new/10xcolleges.git
cd 10xcolleges
python3 -m pip install openpyxl python-docx requests markdown
python3 -m unittest discover -s college-apps/tests
```

**Design docs:** [`design.md`](college-apps/docs/design.md) for architecture and the
reasoning behind it, [`data-model.md`](college-apps/docs/data-model.md) for the data
contract — every file, who writes it, and what may change it.

63 tests, mostly pinning date arithmetic — which aid year a January deadline belongs to,
what happens when a student starts eight weeks late, what happens when a deadline is
mistyped. That logic is where a bug costs a family real money, so it isn't left to
spot-checking.

## License

MIT — see [LICENSE](LICENSE).
