# Scorecard proxy

Lives in `proxy/` of the plugin repo; deploy and test from this directory.

A small service that holds the shared College Scorecard API key so plugin users
never need one. The plugin's `scorecard.py` sends its normal query here; the proxy
adds the key, caches responses for 30 days, throttles per client, and relays the
upstream status, body, and rate-limit headers unchanged.

Only school names and UNITIDs cross the wire. No student data is ever sent here.

## Behaviour

- `GET /v1/schools?…` — same query string `api.data.gov/ed/collegescorecard/v1/schools`
  takes; any `api_key` the client sends is ignored and the real one added. Only the
  parameters the plugin uses are forwarded (`school.name`, `fields`, `per_page`, `page`,
  `school.operating`, `id`); `per_page` is capped at 100.
- Cache: 30 days, keyed on the normalized query, up to 5,000 entries. Hits don't spend
  quota. Errors aren't cached.
- Throttle: 60 upstream calls per client per hour (`PER_CLIENT_HOUR`), 900 per hour
  overall (`GLOBAL_HOUR`, headroom under data.gov's 1,000). A client is the plugin's
  self-issued `X-Client-Id`, else the caller's IP. Over the limit → `429` with
  `Retry-After`.
- `POST /v1/feedback` — one piece of user-written feedback from the plugin's
  `feedback` skill: `comment` (≤2000 chars), optional `rating` 1–5, `skill`, `stage`,
  `version`, `client_id`. Anything else in the body is dropped. 10 per client per hour.

- `GET /v1/feedback?n=200` — read the newest entries; needs
  `Authorization: Bearer <ADMIN_TOKEN>`.
- `GET /healthz` — liveness, whether the key is set, cache size.

## Deploy (fly.io)

```bash
fly auth login
fly secrets set SCORECARD_API_KEY=<your key from https://api.data.gov/signup/>
fly secrets set ADMIN_TOKEN=<any long random string, for reading feedback back>
fly secrets set SUPABASE_SERVICE_KEY=<service_role key from the Supabase project's API settings>
fly deploy -a 10xcolleges-scorecard --ha=false
curl https://10xcolleges-scorecard.fly.dev/healthz
```

The machine stops when idle and wakes on the first request. The cache is in memory
and resets on restart; that's fine for this traffic. Nothing is stored on the machine;
feedback and usage live in Supabase.

Read feedback:

```bash
curl -s -H "Authorization: Bearer $ADMIN_TOKEN" https://10xcolleges-scorecard.fly.dev/v1/feedback | python3 -m json.tool
```

## What it stores

With `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` set (the normal deployment), two tables
in Supabase, both with row-level security on and no policies, so only the service key
can read or write them:

| Table | One row per | Columns |
|---|---|---|
| `tenx_feedback` | note a user chose to send | `at`, `client_id`, `skill`, `stage`, `rating`, `comment`, `version` |
| `tenx_usage_events` | Scorecard lookup | `at`, `client_id` (null for callers without one), `kind` (`get` / `search`), `unitids`, `search_name`, `cache` (`hit` / `miss`), `status` |

Views for the dashboard: `tenx_daily_usage` (lookups, hits, distinct installations per day)
and `tenx_top_schools` (lookups per UNITID, last 30 days). The `tenx_` prefix is because the
tables share the careercoach-v3-staging Supabase project (the one the 10xjobs v3 code uses).

`client_id` is the plugin's random per-installation id — it identifies an installation,
not a person. There is no student data in either table and no way for the proxy to
receive any.

Still in memory, gone on restart: throttle counters (installation id → timestamps) and
the 30-day response cache (school data only). Fly keeps its own short-lived access log.

Without Supabase configured (local development), feedback falls back to a `feedback.jsonl`
file in the working directory and usage isn't recorded. The deployed app has no volume.

## Local

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
SCORECARD_API_KEY=… .venv/bin/uvicorn server:app --port 8080
```
