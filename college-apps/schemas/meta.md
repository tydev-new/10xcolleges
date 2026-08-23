# Schema: meta.json & packet.json

Owner: `college-app` (`meta.json`), `counselor-package` (`packet.json`)
Class: **Index**

## `meta.json` — owned by college-app

Machine-readable JSON mirror of the college list. Kept in sync with `colleges.md` after every list change.

```json
{
  "slug": "jordan-k",
  "name": "Jordan K",
  "grad_year": 2027,
  "updated": "2026-08-23",
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
      "status": "researching"
    }
  ]
}
```

- `tier`: `safety` | `target` | `reach`
- `status`: `considering` | `researching` | `committed-to-apply` | `in-progress` | `submitted` | `decided` | `withdrawn`

---

## `packet.json` — owned by counselor-package

Extracted metadata rendered into `out/packet.docx`.
