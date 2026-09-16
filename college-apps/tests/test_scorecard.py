#!/usr/bin/env python3
"""Offline tests for scorecard.py — no network, no quota.

Covers the citation-integrity logic: that probe years track the calendar, that a cost
estimate never silently mixes field years, and that quota reporting doesn't go stale.

Run:  .venv/bin/python -m unittest discover -s tests -v
"""

import json
import sys
import time
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import scorecard as sc  # noqa: E402


def metric(value, year):
    return {"value": value, "year": year}


class ProbeYears(unittest.TestCase):
    """A hardcoded year list silently pins vintages once a new year publishes."""

    def test_starts_at_current_year_and_counts_back(self):
        self.assertEqual(sc.probe_years(3, today=date(2026, 8, 12)),
                         [2026, 2025, 2024])

    def test_tracks_the_calendar_forward(self):
        self.assertEqual(sc.probe_years(2, today=date(2031, 1, 1))[0], 2031)

    def test_deep_metrics_reach_further_back(self):
        deep = sc.probe_years(sc.DEEP_DEPTH, today=date(2026, 1, 1))
        core = sc.probe_years(sc.CORE_DEPTH, today=date(2026, 1, 1))
        self.assertLess(min(deep), min(core),
                        "debt/earnings lag further and need a deeper probe")

    def test_query_stays_under_url_limit(self):
        """Every probe year adds ~28 fields; the request breaks somewhere past 8KB."""
        import urllib.parse
        q = urllib.parse.urlencode({
            "id": "170976", "fields": ",".join(sc.build_fields()),
            "per_page": 100,
        })
        self.assertLess(len(q), 8000, f"query string is {len(q)} chars")


class OutOfStateEstimate(unittest.TestCase):
    """coa + (tuition_out - tuition_in) is only honest when the years agree."""

    def test_same_year_gets_a_clean_citation(self):
        m = {"coa": metric(34654, 2024), "tuition_out": metric(60946, 2024),
             "tuition_in": metric(17736, 2024)}
        note = sc.oos_note(m, is_public=True)
        self.assertIn("$77,864", note)
        self.assertIn("2024-25 field year", note)
        self.assertNotIn("mixes field years", note)

    def test_mixed_years_are_flagged_not_hidden(self):
        m = {"coa": metric(34654, 2024), "tuition_out": metric(55000, 2021),
             "tuition_in": metric(17736, 2024)}
        note = sc.oos_note(m, is_public=True)
        self.assertIn("mixes field years", note)
        self.assertIn("2024", note)
        self.assertIn("2021", note)

    def test_private_schools_get_no_note(self):
        m = {"coa": metric(79788, 2024), "tuition_out": metric(64144, 2024),
             "tuition_in": metric(64144, 2024)}
        self.assertEqual(sc.oos_note(m, is_public=False), "")

    def test_missing_component_produces_nothing(self):
        m = {"coa": metric(34654, 2024), "tuition_out": metric(None, None),
             "tuition_in": metric(17736, 2024)}
        self.assertEqual(sc.oos_note(m, is_public=True), "")


class Citations(unittest.TestCase):
    def test_missing_value_never_invents_a_number(self):
        self.assertEqual(sc.cite(metric(None, None), sc.money),
                         "Not found — needs checking")

    def test_every_citation_carries_a_vintage(self):
        self.assertIn("2024-25 field year", sc.cite(metric(1000, 2024), sc.money))


class QuotaReporting(unittest.TestCase):
    def _write(self, remaining, age_minutes):
        sc.QUOTA_FILE.parent.mkdir(parents=True, exist_ok=True)
        sc.QUOTA_FILE.write_text(json.dumps({
            "limit": "10", "remaining": str(remaining),
            "at": time.time() - age_minutes * 60,
        }))

    def tearDown(self):
        sc.QUOTA_FILE.unlink(missing_ok=True)

    def test_fresh_reading_is_reported_as_current(self):
        self._write(4, age_minutes=5)
        self.assertIn("4 of 10", sc.quota_status())

    def test_stale_reading_is_not_reported_as_current(self):
        """A stale '0 remaining' would stall an agent told to check quota first."""
        self._write(0, age_minutes=90)
        status = sc.quota_status()
        self.assertIn("expired", status)
        self.assertIn("presumed available", status)

    def test_unreadable_record_does_not_crash(self):
        sc.QUOTA_FILE.parent.mkdir(parents=True, exist_ok=True)
        sc.QUOTA_FILE.write_text("{ truncated wri")
        self.assertIn("presumed available", sc.quota_status())


class Routing(unittest.TestCase):
    """No key → the shared proxy, quietly. Own key → api.data.gov on their quota."""

    def setUp(self):
        self.tmp = Path(__file__).parent / ".tmp-cache"
        self._cache = sc.CACHE_DIR
        sc.CACHE_DIR = self.tmp

    def tearDown(self):
        sc.CACHE_DIR = self._cache
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_default_is_the_proxy(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            self.assertEqual(sc.endpoint(), sc.PROXY)
            self.assertTrue(sc.proxied())
            self.assertEqual(sc.api_key(), "")

    def test_own_key_goes_direct(self):
        with mock.patch.dict("os.environ", {"SCORECARD_API_KEY": "abc"}, clear=True):
            self.assertEqual(sc.endpoint(), sc.API_UPSTREAM)
            self.assertFalse(sc.proxied())
            self.assertEqual(sc.api_key(), "abc")

    def test_explicit_url_wins(self):
        with mock.patch.dict("os.environ", {"SCORECARD_API_URL": "https://x.test/v1/schools"}, clear=True):
            self.assertEqual(sc.endpoint(), "https://x.test/v1/schools")

    def test_client_id_is_stable_and_opaque(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            a, b = sc.client_id(), sc.client_id()
        self.assertEqual(a, b)
        self.assertEqual(len(a), 32)
        self.assertTrue(a.isalnum())

    def _resp(self, status=200, body='{"results": []}', headers=None):
        r = mock.Mock()
        r.status_code = status; r.text = body; r.json.return_value = json.loads(body)
        r.headers = headers or {}; r.raise_for_status = mock.Mock()
        return r

    def test_proxied_request_sends_client_id_and_no_key(self):
        with mock.patch.dict("os.environ", {}, clear=True), \
             mock.patch.object(sc.requests, "get", return_value=self._resp()) as get:
            sc.fetch({"id": "1"})
        url = get.call_args.args[0]; kw = get.call_args.kwargs
        self.assertEqual(url, sc.PROXY)
        self.assertNotIn("api_key", kw["params"])
        self.assertEqual(kw["headers"]["X-Client-Id"], sc.client_id())

    def test_busy_proxy_speaks_plainly(self):
        """A user without a key must never be told about keys, quotas, or APIs."""
        with mock.patch.dict("os.environ", {}, clear=True), \
             mock.patch.object(sc.requests, "get", return_value=self._resp(429, '{"error":"rate limit"}')):
            with self.assertRaises(SystemExit) as cm:
                sc.fetch({"id": "2"})
        msg = str(cm.exception).lower()
        for word in ("api", "key", "quota", "demo", "data.gov", "rate limit"):
            self.assertNotIn(word, msg, f"leaked {word!r}: {msg}")
        self.assertIn("busy", msg)
        self.assertIn("already researched", msg)

    def test_unreachable_proxy_falls_back_quietly(self):
        import requests as rq
        ok = self._resp()
        with mock.patch.dict("os.environ", {}, clear=True), \
             mock.patch.object(sc.requests, "get", side_effect=[rq.ConnectionError(), ok]) as get, \
             mock.patch("sys.stderr") as err:
            data = sc.fetch({"id": "3"})
        self.assertEqual(data, {"results": []})
        self.assertEqual(get.call_count, 2)
        second = get.call_args_list[1]
        self.assertEqual(second.args[0], sc.API_UPSTREAM)
        self.assertEqual(second.kwargs["params"]["api_key"], "DEMO_KEY")
        self.assertEqual(err.write.call_count, 0, "fallback must be silent")

    def test_own_key_users_keep_the_technical_diagnosis(self):
        with mock.patch.dict("os.environ", {"SCORECARD_API_KEY": "bad"}, clear=True), \
             mock.patch.object(sc.requests, "get", return_value=self._resp(403, '{"error":{"code":"API_KEY_INVALID"}}')):
            with self.assertRaises(SystemExit) as cm:
                sc.fetch({"id": "4"})
        self.assertIn("rejected the API key", str(cm.exception))


class BatchReconciliation(unittest.TestCase):
    """A UNITID that returns nothing must not vanish without comment."""

    def test_missing_unitid_warns(self):
        fake = {"results": [{"id": 170976, "school.name": "Michigan",
                             "school.ownership": 1}]}
        with mock.patch.object(sc, "fetch", return_value=fake):
            with mock.patch("sys.stderr") as err:
                rows = sc.get_many(["170976", "999999"])
        self.assertEqual(len(rows), 1)
        printed = "".join(str(c) for c in err.write.call_args_list)
        self.assertIn("999999", printed)

    def test_oversized_batch_refuses_rather_than_truncating(self):
        with self.assertRaises(SystemExit):
            sc.get_many([str(i) for i in range(101)])


if __name__ == "__main__":
    unittest.main(verbosity=2)
