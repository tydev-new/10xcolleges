# College Applications — Counselor Plugin

A Claude plugin that guides high school students through the complete college application campaign the way a master college counselor would—from initial intake and major fit to list building, school research, affordability, essay coaching, teacher recommendations, timeline tracking, and counselor review packets.

Install from the [10xcolleges marketplace](https://github.com/tydev-new/10xcolleges).

---

## The 8-Stage Counseling Suite

| Stage | Skill Name | What It Does | Deterministic Validator | Formal Schema | E2E Status |
|:---:|---|---|---|---|:---:|
| **0** | **`college-app`** | **Lead Counselor & Orchestrator:** Front-door discovery, "Single Next Step" triage, and multi-intent execution. | Coordinates validators, manages `meta.json` | [`schemas/meta.md`](schemas/meta.md) | **100% PASS** (`m1-college-app`) |
| **1a** | **`student-intake`** | **Student Record & Criteria:** Uncovers activities, roles, and reflections; sets budget ceiling and deal-breakers. | [`check_record.py`](scripts/check_record.py) | [`schemas/profile.md`](schemas/profile.md)<br>[`schemas/criteria.md`](schemas/criteria.md) | **100% PASS** (`i1-intake-rounds`) |
| **1b** | **`major-fit`** | **Academic Direction:** Analyzes major admit disparities, pairs adjacent majors, audits transfer hurdles. | [`check_major.py`](scripts/check_major.py) | [`schemas/academic-direction.md`](schemas/academic-direction.md) | **100% PASS** (Unit Suite) |
| **2** | **`college-list`** | **Balanced College List:** Builds 8–12 school list enforcing the 2-safety floor (academic + financial). | [`check_list.py`](scripts/check_list.py) | [`schemas/colleges.md`](schemas/colleges.md) | **100% PASS** (`l1-list-build`) |
| **3** | **`college-research`** | **Grounded School Dossiers:** Cites Common Data Set stats, departmental labs, culture, and deadlines. | [`check_research.py`](scripts/check_research.py) | [`schemas/research.md`](schemas/research.md) | **100% PASS** (`r1-research-school`) |
| **4** | **`financial-aid`** | **Affordability & Net Price:** Audits Net Price Calculator figures, models need/merit aid, plans FAFSA/CSS. | [`check_aid.py`](scripts/check_aid.py) | [`schemas/financial-aid.md`](schemas/financial-aid.md) | **100% PASS** (`f1-financial-aid`) |
| **5** | **`essay-coach`** | **Anti-Ghostwriting Essay Coach:** Builds rubrics from college guidance, explores angles, draft-by-draft review. | [`check_draft.py`](scripts/check_draft.py) | [`schemas/essay.md`](schemas/essay.md) | **100% PASS** (`e3-review-rounds`) |
| **6** | **`rec-request`** | **Faculty Recommendations:** Recommender audit (1 STEM + 1 Hum), in-person scripts, brag sheets, FERPA. | [`check_rec.py`](scripts/check_rec.py) | [`schemas/recs.md`](schemas/recs.md) | **100% PASS** (`k1-rec-request`) |
| **7** | **`app-tracker`** | **Deadline & Spreadsheet Engine:** Backwards planning, 7-day crash buffer, generates 5-sheet `tracker.xlsx`. | [`make_tracker.py`](scripts/make_tracker.py) | [`schemas/tracker.md`](schemas/tracker.md) | **100% PASS** (Date Suite: 19/19) |
| **8** | **`counselor-package`** | **Counselor Review & Options Packet:** 4 high-leverage asks, `package.html` review dossier, and `packet.docx`. | [`build_package.py`](scripts/build_package.py)<br>[`fill_packet.py`](scripts/fill_packet.py) | [`schemas/counselor.md`](schemas/counselor.md) | **100% PASS** (`p1-counselor-package`) |

---

Full system documentation, architecture guides, and test instructions are in the [repository root README](https://github.com/tydev-new/10xcolleges#readme).
