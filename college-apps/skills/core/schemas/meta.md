# Schema: meta.json & packet.json

Owner: `college-app` (`meta.json`), `counselor-package` (`packet.json`)
Class: **Index**

Location: `students/<slug>/meta.json`, `students/<slug>/packet.json`

Machine-readable JSON state files that drive tracker spreadsheets (`out/tracker.xlsx`) and post-secondary options packet generation (`out/packet.docx`).

---

## `meta.json` — owned by college-app

Machine-readable JSON mirror of the college list, recommenders, and key dates. Kept strictly in sync with `colleges.md` after every list change, and read directly by `make_tracker.py`.

```json
{
  "slug": "jordan-k",
  "name": "Jordan K",
  "grad_year": 2027,
  "updated": "2026-09-02",
  "colleges": [
    {
      "name": "University of Michigan",
      "slug": "university-of-michigan",
      "unitid": 170976,
      "tier": "target",
      "decision_plan": "EA",
      "deadline": "2026-11-01",
      "app_type": "Common App",
      "counselor_letter": true,
      "status": "in-progress"
    }
  ],
  "recommenders": [
    {
      "name": "Ms. Alvarez",
      "subject": "AP Physics C",
      "grade_taught": "11th",
      "asked_on": "2026-09-02",
      "agreed": "yes",
      "brag_sheet_sent": "yes",
      "colleges": "All Common App",
      "submitted": "no",
      "thank_you": "no",
      "notes": "Spoke after 4th period; brag sheet delivered."
    }
  ],
  "key_dates": [
    {
      "date": "2026-11-01",
      "what": "Early Action Deadlines (Michigan, Purdue, UIUC)",
      "notes": "Submit application materials and confirm test score sends 2 weeks prior."
    }
  ]
}
```

### Enumerations & Field Types:
- **`tier`:** `"safety"` | `"target"` | `"reach"`
- **`decision_plan`:** `"EA"` (Early Action) | `"ED"` (Early Decision I) | `"ED II"` (Early Decision II) | `"REA"` (Restricted Early Action) | `"RD"` (Regular Decision) | `"Rolling"`
- **`app_type`:** `"Common App"` | `"Coalition"` | `"UC Application"` | `"ApplyTexas"` | `"Institutional Portal"`
- **`status`:** `"considering"` | `"researching"` | `"committed-to-apply"` | `"in-progress"` | `"submitted"` | `"decided"` | `"withdrawn"`
- **`recommenders[].agreed`:** `"yes"` | `"no"`
- **`recommenders[].submitted`:** `"yes"` | `"no"`

---

## `packet.json` — owned by counselor-package

Extracted metadata structured from `profile.md`, `academic-direction.md`, and `meta.json`, rendered deterministically into `out/packet.docx` by `scripts/fill_packet.py`.

```json
{
  "name": "Jordan K",
  "email": "jordan.k@example.com",
  "phone": "(555) 234-5678",
  "high_school": "Oak Park High School",
  "grad_year": 2027,
  "classes": [
    {
      "first": "AP Physics C",
      "second": "AP Physics C"
    },
    {
      "first": "AP Calculus BC",
      "second": "AP Calculus BC"
    },
    {
      "first": "AP English Literature",
      "second": "AP English Literature"
    }
  ],
  "teachers": [
    "Ms. Alvarez — AP Physics C, 11th",
    "Mr. Davis — AP English Language, 11th"
  ],
  "school_activities": [
    {
      "name": "Robotics Club",
      "grades": "9-12",
      "role": "Build Team Captain"
    }
  ],
  "outside_activities": [
    {
      "name": "Community Bike Repair Stand",
      "grades": "10-12",
      "role": "Founder & Volunteer"
    }
  ],
  "hobbies": [
    "Restoring vintage mopeds",
    "Analog synthesizer soldering"
  ],
  "honors": [
    {
      "name": "National Merit Commended Scholar",
      "grades": "11",
      "award": "PSAT NMSC Recognition"
    }
  ],
  "work": [
    {
      "employer": "Trader Joe's",
      "grades": "11-12",
      "position": "Grocery Cashier (12 hrs/wk)"
    }
  ],
  "reflections": {
    "qualities": [
      {
        "quality": "Mechanical Persistence",
        "example": "Redesigned robot transmission three times after motor stalls during regional qualifiers."
      }
    ],
    "academic_growth": [
      "Struggled with rotational dynamics first semester; came to lunch office hours and earned a 5 on the AP exam."
    ],
    "intellectual_growth": [
      "Learned to enjoy analytical debate in AP Lang even when disagreeing with peers."
    ],
    "impact_campus": "Trained six underclassmen on machining safety and manual lathe operation.",
    "impact_community": "Kept neighborhood bikes operational for low-income commuters outside public library.",
    "challenges": "Balanced 15-hour weekly job and varsity robotics while maintaining rigorous STEM courseload.",
    "challenges_include": "Yes",
    "majors": [
      "Mechanical Engineering",
      "Applied Physics"
    ]
  },
  "colleges": [
    {
      "name": "University of Michigan",
      "tier": "target",
      "decision_plan": "EA",
      "deadline": "2026-11-01"
    }
  ],
  "parent_worksheet": {
    "1": "Curious, tenacious, and quietly helpful to younger peers.",
    "2": "Has grown from a shy builder into a vocal mentor who leads team strategy.",
    "3": "Maintained the free community bike clinic for two winters without prompting.",
    "4": "Worked 12 hours a week to help with household living expenses without complaining.",
    "5": "Designing the custom adaptive tricycle controller for a local middle schooler.",
    "6": "Please highlight their ability to handle real responsibility and maintain academic rigor simultaneously."
  }
}
```

### Invariants:
- All keys are optional; missing keys render deterministically as `"[to be completed]"` in `out/packet.docx`.
- The `reflections` and `parent_worksheet` entries directly populate the counselor packet narrative so the high school counselor can write a comprehensive, evidence-rich Secondary School Report (SSR).
