---
name: core
description: Shared kit for the 10xcolleges skills — the validator and generator scripts, the file schemas every workspace file follows, the calendar config, workspace templates, and the voice and citation guides. Not a workflow on its own; the other 10xcolleges skills point here. Use it directly only to run a validator by hand or to look up a schema.
---

# core — the shared kit

Every other 10xcolleges skill reads from this folder. Nothing here talks to a student.

| What | Where | Used by |
|---|---|---|
| Validators (`check_*.py`) and generators (`make_tracker.py`, `build_package.py`, `fill_packet.py`) | `scripts/` | the skill that owns each file, plus `college-app` |
| Scorecard lookups through the shared proxy | `scripts/scorecard.py` | `college-research`, `college-list` |
| Feedback sender | `scripts/feedback.py` | `feedback` |
| File schemas — the contract each workspace file must follow | `schemas/` | all skills |
| Calendar (FAFSA opening, decision dates, buffers) | `config/calendar.json` | `app-tracker`, `financial-aid` |
| Workspace templates | `templates/` | `college-app`, `student-intake` |
| Voice, citation standard, data model | `references/voice.md`, `references/citations.md`, `references/data-model.md` | all skills |

## Where this folder is

- **Claude Code plugin:** `${CLAUDE_PLUGIN_ROOT}/skills/core`.
- **Any other agent** (Codex, Gemini CLI, ChatGPT, or a plain clone): the `core` folder installed next to the other 10xcolleges skills — `../core` from any skill's `SKILL.md`. Skills are written for either: read `${CLAUDE_PLUGIN_ROOT}/skills/core/...` as "the core folder".

## Requirements

The scripts need four Python packages:

```bash
python3 -m pip install -r <core>/requirements.txt      # openpyxl python-docx requests markdown
```

If one is missing, the script names it and the install command.

## Running a validator by hand

```bash
python3 <core>/scripts/check_list.py students/<slug>
python3 <core>/scripts/scorecard.py search "Case Western"
```

Every script prints plain-language findings and exits non-zero when a rule is broken; the rules are the ones listed in `references/data-model.md § Enforcement`.
