"""Offline tests: upstream is faked, no network."""
import unittest
from unittest import mock

import httpx
from starlette.testclient import TestClient

import server


def fake_response(status=200, body=b'{"results":[{"id":1}]}', headers=None):
    return httpx.Response(status, content=body,
                          headers=headers or {"X-Ratelimit-Limit": "1000", "X-Ratelimit-Remaining": "999"},
                          request=httpx.Request("GET", server.UPSTREAM))


class Base(unittest.TestCase):
    def setUp(self):
        server._cache.clear(); server._hits.clear()
        server.KEY = "secret-key"
        self.client = TestClient(server.app)


class Forwarding(Base):
    def test_adds_key_and_relays_body_and_headers(self):
        with mock.patch.object(server, "upstream_get", mock.AsyncMock(return_value=fake_response())) as up:
            r = self.client.get("/v1/schools?school.name=Michigan&per_page=5&api_key=DEMO_KEY")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {"results": [{"id": 1}]})
        sent = up.call_args.args[0]
        self.assertEqual(sent["api_key"], "secret-key")
        self.assertEqual(sent["school.name"], "Michigan")
        self.assertEqual(r.headers["X-Ratelimit-Limit"], "1000")
        self.assertEqual(r.headers["X-Cache"], "miss")

    def test_key_never_leaks_into_response(self):
        with mock.patch.object(server, "upstream_get", mock.AsyncMock(return_value=fake_response())):
            r = self.client.get("/v1/schools?id=170976")
        self.assertNotIn("secret-key", r.text)
        self.assertNotIn("secret-key", str(r.headers))

    def test_unknown_params_are_dropped_and_empty_query_rejected(self):
        with mock.patch.object(server, "upstream_get", mock.AsyncMock(return_value=fake_response())) as up:
            self.client.get("/v1/schools?id=1&evil=1")
        self.assertNotIn("evil", up.call_args.args[0])
        self.assertEqual(self.client.get("/v1/schools?evil=1").status_code, 400)

    def test_per_page_capped(self):
        self.assertEqual(self.client.get("/v1/schools?id=1&per_page=500").status_code, 400)

    def test_upstream_error_status_is_relayed(self):
        with mock.patch.object(server, "upstream_get", mock.AsyncMock(return_value=fake_response(403, b'{"error":{"code":"OVER_RATE_LIMIT"}}'))):
            r = self.client.get("/v1/schools?id=1")
        self.assertEqual(r.status_code, 403)
        self.assertIn("OVER_RATE_LIMIT", r.text)

    def test_upstream_unreachable_is_502(self):
        with mock.patch.object(server, "upstream_get", mock.AsyncMock(side_effect=httpx.ConnectError("x"))):
            self.assertEqual(self.client.get("/v1/schools?id=1").status_code, 502)


class Caching(Base):
    def test_second_identical_query_never_hits_upstream(self):
        with mock.patch.object(server, "upstream_get", mock.AsyncMock(return_value=fake_response())) as up:
            self.client.get("/v1/schools?id=1&fields=a,b")
            r = self.client.get("/v1/schools?fields=a,b&id=1")      # same query, different order
        self.assertEqual(up.call_count, 1)
        self.assertEqual(r.headers["X-Cache"], "hit")

    def test_cache_hits_do_not_spend_quota(self):
        with mock.patch.object(server, "upstream_get", mock.AsyncMock(return_value=fake_response())):
            self.client.get("/v1/schools?id=1", headers={"X-Client-Id": "abc"})
            r = self.client.get("/v1/schools?id=1", headers={"X-Client-Id": "abc"})
        self.assertEqual(int(r.headers["X-Ratelimit-Remaining"]), server.PER_CLIENT_HOUR - 1)

    def test_errors_are_not_cached(self):
        with mock.patch.object(server, "upstream_get", mock.AsyncMock(return_value=fake_response(500, b"{}"))) as up:
            self.client.get("/v1/schools?id=1"); self.client.get("/v1/schools?id=1")
        self.assertEqual(up.call_count, 2)


class Throttle(Base):
    def test_per_client_limit_then_429_with_retry_after(self):
        server.PER_CLIENT_HOUR = 2
        with mock.patch.object(server, "upstream_get", mock.AsyncMock(return_value=fake_response())):
            h = {"X-Client-Id": "abc"}
            self.client.get("/v1/schools?id=1", headers=h)
            self.client.get("/v1/schools?id=2", headers=h)
            r = self.client.get("/v1/schools?id=3", headers=h)
        self.assertEqual(r.status_code, 429)
        self.assertEqual(r.headers["X-Ratelimit-Remaining"], "0")
        self.assertIn("Retry-After", r.headers)
        server.PER_CLIENT_HOUR = 60

    def test_clients_are_throttled_independently(self):
        server.PER_CLIENT_HOUR = 1
        with mock.patch.object(server, "upstream_get", mock.AsyncMock(return_value=fake_response())):
            self.client.get("/v1/schools?id=1", headers={"X-Client-Id": "aaa"})
            r = self.client.get("/v1/schools?id=2", headers={"X-Client-Id": "bbb"})
        self.assertEqual(r.status_code, 200)
        server.PER_CLIENT_HOUR = 60

    def test_global_cap_protects_the_shared_key(self):
        server.GLOBAL_HOUR = 1
        with mock.patch.object(server, "upstream_get", mock.AsyncMock(return_value=fake_response())):
            self.client.get("/v1/schools?id=1", headers={"X-Client-Id": "aaa"})
            r = self.client.get("/v1/schools?id=2", headers={"X-Client-Id": "bbb"})
        self.assertEqual(r.status_code, 429)
        server.GLOBAL_HOUR = 900

    def test_bad_client_id_falls_back_to_ip(self):
        req = mock.Mock(); req.headers = {"x-client-id": "not valid!!", "fly-client-ip": "1.2.3.4"}
        self.assertEqual(server.client_of(req), "ip:1.2.3.4")


class Feedback(Base):
    def setUp(self):
        super().setUp()
        import tempfile, os as _os
        self.dir = tempfile.mkdtemp()
        server.FEEDBACK_PATH = _os.path.join(self.dir, "fb.jsonl")
        server.ADMIN_TOKEN = "admin-secret"
        server._fb_hits.clear()

    def test_stores_only_known_fields(self):
        r = self.client.post("/v1/feedback", json={
            "comment": "The list was great", "rating": 5, "skill": "college-list",
            "stage": "2", "version": "1.0.0", "client_id": "abc",
            "student_name": "Maya", "profile": "secret"})          # must be dropped
        self.assertEqual(r.status_code, 201)
        stored = open(server.FEEDBACK_PATH).read()
        self.assertIn("The list was great", stored)
        self.assertNotIn("Maya", stored); self.assertNotIn("secret", stored)

    def test_rejects_empty_oversized_and_bad_rating(self):
        self.assertEqual(self.client.post("/v1/feedback", json={}).status_code, 400)
        self.assertEqual(self.client.post("/v1/feedback", json={"comment": "x" * 2001}).status_code, 400)
        self.assertEqual(self.client.post("/v1/feedback", json={"rating": 9}).status_code, 400)
        self.assertEqual(self.client.post("/v1/feedback", json={"rating": 3}).status_code, 201)

    def test_readback_needs_admin_token(self):
        self.client.post("/v1/feedback", json={"comment": "hi"})
        self.assertEqual(self.client.get("/v1/feedback").status_code, 401)
        r = self.client.get("/v1/feedback", headers={"Authorization": "Bearer admin-secret"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["count"], 1)
        self.assertEqual(r.json()["items"][0]["comment"], "hi")

    def test_feedback_is_throttled_per_client(self):
        server.FEEDBACK_PER_CLIENT_HOUR = 2
        h = {"X-Client-Id": "abc"}
        self.client.post("/v1/feedback", json={"comment": "1"}, headers=h)
        self.client.post("/v1/feedback", json={"comment": "2"}, headers=h)
        self.assertEqual(self.client.post("/v1/feedback", json={"comment": "3"}, headers=h).status_code, 429)
        server.FEEDBACK_PER_CLIENT_HOUR = 10


if __name__ == "__main__":
    unittest.main(verbosity=2)
