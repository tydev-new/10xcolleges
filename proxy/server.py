"""Key-holding proxy for the College Scorecard API.

The 10xcolleges plugin's scorecard.py sends its normal query here instead of to
api.data.gov. This service adds the shared API key, caches responses, throttles per
client, and relays the upstream status, body, and rate-limit headers unchanged — so
the plugin's own error handling keeps working and no user ever needs a key.

Only school names and UNITIDs cross the wire. No student data is ever sent here.
"""
import hashlib
import json
import os
import time
from collections import OrderedDict, defaultdict

import httpx
from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

UPSTREAM = "https://api.data.gov/ed/collegescorecard/v1/schools"
KEY = os.environ.get("SCORECARD_API_KEY", "")
PER_CLIENT_HOUR = int(os.environ.get("PER_CLIENT_HOUR", "60"))
GLOBAL_HOUR = int(os.environ.get("GLOBAL_HOUR", "900"))      # headroom under data.gov's 1,000
CACHE_TTL = 30 * 24 * 3600
CACHE_MAX = 5000
ALLOWED_PARAMS = {"school.name", "fields", "per_page", "page", "school.operating", "id"}
RELAY_HEADERS = ("X-Ratelimit-Limit", "X-Ratelimit-Remaining")
FEEDBACK_PATH = os.environ.get("FEEDBACK_PATH", "feedback.jsonl")   # local-dev fallback only
FEEDBACK_PER_CLIENT_HOUR = 10
FEEDBACK_MAX = {"comment": 2000, "skill": 40, "stage": 40, "version": 20, "client_id": 64}
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")
# Supabase (optional). When both are set, feedback and usage go to Postgres via the
# REST API with the service key; otherwise feedback falls back to the JSONL file and
# usage isn't recorded.
SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")
FEEDBACK_TABLE = os.environ.get("SUPABASE_FEEDBACK_TABLE", "tenx_feedback")
USAGE_TABLE = os.environ.get("SUPABASE_USAGE_TABLE", "tenx_usage_events")

_cache: "OrderedDict[str, tuple]" = OrderedDict()   # key -> (expires, status, body, headers)
_hits: "dict[str, list[float]]" = defaultdict(list)  # client -> upstream-call timestamps


def client_of(request) -> str:
    """Who to throttle: the plugin's self-issued id, else the caller's IP."""
    cid = request.headers.get("x-client-id", "").strip()
    if cid and len(cid) <= 64 and cid.isalnum():
        return "id:" + cid
    ip = request.headers.get("fly-client-ip") or (request.client.host if request.client else "?")
    return "ip:" + ip


def spent(bucket: list, limit: int, now: float) -> bool:
    bucket[:] = [t for t in bucket if now - t < 3600]
    return len(bucket) >= limit


def remaining(client: str, now: float) -> int:
    spent(_hits[client], PER_CLIENT_HOUR, now)
    return max(0, PER_CLIENT_HOUR - len(_hits[client]))


def supabase_on() -> bool:
    return bool(SUPABASE_URL and SUPABASE_SERVICE_KEY)


def _sb_headers(prefer: str = "return=minimal") -> dict:
    return {"apikey": SUPABASE_SERVICE_KEY, "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
            "Content-Type": "application/json", "Prefer": prefer}


async def sb_insert(table: str, row: dict) -> bool:
    """Insert one row; True on success. Never raises — callers decide what a miss means."""
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.post(f"{SUPABASE_URL}/rest/v1/{table}", json=row, headers=_sb_headers())
        return r.status_code in (200, 201)
    except httpx.HTTPError:
        return False


async def sb_select(table: str, query: str) -> list | None:
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(f"{SUPABASE_URL}/rest/v1/{table}?{query}", headers=_sb_headers())
        return r.json() if r.status_code == 200 else None
    except (httpx.HTTPError, ValueError):
        return None


async def record_usage(client: str, q: dict, cache: str, status: int) -> None:
    """One row per lookup. Runs in the background; a failure is dropped, never surfaced."""
    if not supabase_on():
        return
    ids = [i for i in q.get("id", "").split(",") if i.strip()]
    await sb_insert(USAGE_TABLE, {
        "client_id": client.split(":", 1)[1] if client.startswith("id:") else None,
        "kind": "get" if ids else "search",
        "unitids": ids or None,
        "search_name": (q.get("school.name") or None) if not ids else None,
        "cache": cache,
        "status": status,
    })


async def upstream_get(params: dict) -> httpx.Response:
    async with httpx.AsyncClient(timeout=30) as c:
        return await c.get(UPSTREAM, params=params)


async def schools(request):
    q = {k: v for k, v in request.query_params.items() if k in ALLOWED_PARAMS}
    if not q:
        return JSONResponse({"error": "no supported query parameters"}, 400)
    try:
        if int(q.get("per_page", 1)) > 100:
            return JSONResponse({"error": "per_page must be 100 or less"}, 400)
    except ValueError:
        return JSONResponse({"error": "per_page must be a number"}, 400)

    now = time.time()
    client = client_of(request)
    ck = hashlib.sha256(json.dumps(q, sort_keys=True).encode()).hexdigest()

    hit = _cache.get(ck)
    if hit and hit[0] > now:
        _cache.move_to_end(ck)
        _, status, body, hdrs = hit
        return Response(body, status, {**hdrs, "X-Cache": "hit",
                        "X-Ratelimit-Remaining": str(remaining(client, now))},
                        media_type="application/json",
                        background=BackgroundTask(record_usage, client, q, "hit", status))

    if spent(_hits[client], PER_CLIENT_HOUR, now) or spent(_hits["*"], GLOBAL_HOUR, now):
        return JSONResponse({"error": "rate limit"}, 429, {
            "X-Ratelimit-Limit": str(PER_CLIENT_HOUR), "X-Ratelimit-Remaining": "0",
            "Retry-After": "600"})
    _hits[client].append(now)
    _hits["*"].append(now)

    try:
        r = await upstream_get({**q, "api_key": KEY})
    except httpx.HTTPError as e:
        return JSONResponse({"error": f"upstream unreachable: {type(e).__name__}"}, 502)

    hdrs = {h: r.headers[h] for h in RELAY_HEADERS if h in r.headers}
    if r.status_code == 200:
        _cache[ck] = (now + CACHE_TTL, 200, r.content, hdrs)
        _cache.move_to_end(ck)
        while len(_cache) > CACHE_MAX:
            _cache.popitem(last=False)
    return Response(r.content, r.status_code, {**hdrs, "X-Cache": "miss",
                    "X-Ratelimit-Remaining": str(remaining(client, now))},
                    media_type="application/json",
                    background=BackgroundTask(record_usage, client, q, "miss", r.status_code))


_fb_hits: "dict[str, list[float]]" = defaultdict(list)


async def feedback_post(request):
    """Store one piece of user-written feedback. Only the fields below are kept."""
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"error": "body must be JSON"}, 400)
    if not isinstance(data, dict):
        return JSONResponse({"error": "body must be an object"}, 400)
    rec = {}
    for k, cap in FEEDBACK_MAX.items():
        v = data.get(k, "")
        if not isinstance(v, str):
            return JSONResponse({"error": f"{k} must be a string"}, 400)
        if len(v) > cap:
            return JSONResponse({"error": f"{k} too long (max {cap})"}, 400)
        rec[k] = v.strip()
    rating = data.get("rating")
    if rating is not None and (not isinstance(rating, int) or not 1 <= rating <= 5):
        return JSONResponse({"error": "rating must be 1-5"}, 400)
    if not rec["comment"] and rating is None:
        return JSONResponse({"error": "nothing to record"}, 400)
    rec["rating"] = rating

    now = time.time()
    client = client_of(request)
    if spent(_fb_hits[client], FEEDBACK_PER_CLIENT_HOUR, now):
        return JSONResponse({"error": "rate limit"}, 429, {"Retry-After": "600"})
    _fb_hits[client].append(now)

    if supabase_on():
        if not await sb_insert(FEEDBACK_TABLE, rec):
            return JSONResponse({"error": "could not store"}, 500)
        return JSONResponse({"ok": True}, 201)
    rec["at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    try:
        os.makedirs(os.path.dirname(FEEDBACK_PATH) or ".", exist_ok=True)
        with open(FEEDBACK_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except OSError as e:
        return JSONResponse({"error": f"could not store: {type(e).__name__}"}, 500)
    return JSONResponse({"ok": True}, 201)


async def feedback_get(request):
    """Read back stored feedback. Admin only: Authorization: Bearer <ADMIN_TOKEN>."""
    auth = request.headers.get("authorization", "")
    if not ADMIN_TOKEN or auth != f"Bearer {ADMIN_TOKEN}":
        return JSONResponse({"error": "unauthorized"}, 401)
    try:
        n = min(int(request.query_params.get("n", "200")), 5000)
    except ValueError:
        n = 200
    if supabase_on():
        rows = await sb_select(FEEDBACK_TABLE, f"select=*&order=at.desc&limit={n}")
        if rows is None:
            return JSONResponse({"error": "could not read"}, 502)
        return JSONResponse({"count": len(rows), "items": rows})
    try:
        with open(FEEDBACK_PATH, encoding="utf-8") as f:
            lines = f.readlines()[-n:]
    except FileNotFoundError:
        lines = []
    return JSONResponse({"count": len(lines), "items": [json.loads(l) for l in lines if l.strip()]})


async def healthz(request):
    return JSONResponse({"ok": True, "key_set": bool(KEY), "cached": len(_cache),
                         "store": "supabase" if supabase_on() else "file"})


app = Starlette(routes=[
    Route("/v1/schools", schools),
    Route("/v1/feedback", feedback_post, methods=["POST"]),
    Route("/v1/feedback", feedback_get, methods=["GET"]),
    Route("/healthz", healthz),
])
