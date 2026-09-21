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
  Appended as JSON lines to `/data/feedback.jsonl` on the volume.
- `GET /v1/feedback?n=200` — read the newest entries; needs
  `Authorization: Bearer <ADMIN_TOKEN>`.
- `GET /healthz` — liveness, whether the key is set, cache size.

## Deploy (fly.io)

```bash
fly auth login
fly volumes create feedback --size 1 --region iad --yes
fly secrets set SCORECARD_API_KEY=<your key from https://api.data.gov/signup/>
fly secrets set ADMIN_TOKEN=<any long random string, for reading feedback back>
fly deploy -a 10xcolleges-scorecard --ha=false
curl https://10xcolleges-scorecard.fly.dev/healthz
```

The machine stops when idle and wakes on the first request. The cache is in memory
and resets on restart; that's fine for this traffic. Feedback persists on the volume.

Read feedback:

```bash
curl -s -H "Authorization: Bearer $ADMIN_TOKEN" https://10xcolleges-scorecard.fly.dev/v1/feedback | python3 -m json.tool
```

## What it stores

| Data | Where | How long | Contains |
|---|---|---|---|
| Feedback users chose to send | `/data/feedback.jsonl` on the fly volume | until you delete it | comment, rating, skill, stage, plugin version, installation id, timestamp |
| Throttle counters | memory | rolling hour; gone on restart | installation id or IP → timestamps of upstream calls |
| Response cache | memory | 30 days; gone on restart | Scorecard responses keyed by query hash — school data only, no caller info |
| Request logs | fly.io platform logs | fly's short retention | method, path, status, client IP (fly's own access log; nothing written by this code) |

No per-user history of which schools were looked up is kept anywhere.

## Local

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
SCORECARD_API_KEY=… .venv/bin/uvicorn server:app --port 8080
```
