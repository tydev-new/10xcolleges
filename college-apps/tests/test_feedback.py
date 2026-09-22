#!/usr/bin/env python3
"""Offline tests for feedback.py — nothing is sent."""
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills" / "core" / "scripts"))

import feedback as fb  # noqa: E402
import scorecard as sc  # noqa: E402


class Payload(unittest.TestCase):
    def setUp(self):
        self._cache = sc.CACHE_DIR
        sc.CACHE_DIR = ROOT / "tests" / ".tmp-cache"

    def tearDown(self):
        import shutil
        shutil.rmtree(sc.CACHE_DIR, ignore_errors=True)
        sc.CACHE_DIR = self._cache

    def test_only_the_agreed_fields(self):
        p = fb.build("college-list", "2", 4, "The list felt right.")
        self.assertEqual(set(p), {"comment", "rating", "skill", "stage", "version", "client_id"})
        self.assertEqual(p["rating"], 4)
        self.assertEqual(p["client_id"], sc.client_id())

    def test_contact_details_are_redacted(self):
        p = fb.build("x", "", None, "email me at maya.r@example.com or 617-555-0142 thanks")
        self.assertNotIn("example.com", p["comment"])
        self.assertNotIn("555", p["comment"])
        self.assertIn("[email removed]", p["comment"])
        self.assertIn("[phone removed]", p["comment"])

    def test_empty_is_refused_and_long_is_refused(self):
        with self.assertRaises(SystemExit):
            fb.build("x", "", None, "   ")
        with self.assertRaises(SystemExit):
            fb.build("x", "", None, "y" * (fb.MAX_COMMENT + 1))

    def test_rating_alone_is_enough(self):
        self.assertEqual(fb.build("x", "", 5, "")["rating"], 5)

    def test_dry_run_prints_and_sends_nothing(self):
        with mock.patch.object(fb, "send") as send, mock.patch("sys.stdout") as out:
            fb.main(["--skill", "essay-coach", "--rating", "3", "--comment", "ok", "--dry-run"])
        send.assert_not_called()
        printed = "".join(str(c.args[0]) for c in out.write.call_args_list)
        self.assertIn('"comment": "ok"', printed)

    def test_url_is_the_proxy_feedback_endpoint(self):
        self.assertTrue(fb.FEEDBACK_URL.endswith("/v1/feedback"))
        self.assertTrue(fb.FEEDBACK_URL.startswith(sc.PROXY.rsplit("/v1/", 1)[0]))


class Sending(unittest.TestCase):
    def _resp(self, status):
        r = mock.Mock(); r.status_code = status; return r

    def test_failure_messages_are_plain(self):
        import requests
        payload = {"comment": "hi", "rating": None, "skill": "", "stage": "", "version": "1", "client_id": "abc"}
        for outcome in (requests.ConnectionError(), self._resp(500), self._resp(429)):
            with mock.patch.object(requests, "post", side_effect=[outcome] if isinstance(outcome, Exception) else None,
                                   return_value=None if isinstance(outcome, Exception) else outcome):
                with self.assertRaises(SystemExit) as cm:
                    fb.send(payload)
            msg = str(cm.exception).lower()
            for word in ("api", "key", "http", "status", "endpoint", "json"):
                self.assertNotIn(word, msg, f"leaked {word!r}: {msg}")

    def test_success_thanks(self):
        import requests
        with mock.patch.object(requests, "post", return_value=self._resp(201)):
            self.assertIn("Thank you", fb.send({"comment": "hi", "rating": None, "skill": "",
                                                "stage": "", "version": "1", "client_id": "abc"}))


if __name__ == "__main__":
    unittest.main(verbosity=2)
