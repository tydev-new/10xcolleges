#!/usr/bin/env python3
"""Send one piece of user-written feedback to the 10xcolleges team.

The user sees the exact payload before anything is sent and says yes. Only these
fields ever leave the machine: the words the user wrote for this purpose, an optional
1–5 rating, which skill and stage they were in, the plugin version, and the same
opaque installation id the Scorecard proxy uses. No student names, files, or
conversation text — the skill never passes them, and this script has no way to read
them.

Usage:
    feedback.py --skill college-list --stage 2 --rating 4 --comment "The list felt right."
    feedback.py --skill essay-coach --comment "Too many rounds" --dry-run   # show, don't send
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scorecard  # noqa: E402  (client_id and the proxy base live there)

FEEDBACK_URL = scorecard.PROXY.rsplit("/v1/", 1)[0] + "/v1/feedback"
MAX_COMMENT = 2000

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE = re.compile(r"(?<!\d)(?:\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}(?!\d)")


def redact(text):
    """Belt-and-braces: a user may paste contact details without meaning to."""
    text = EMAIL.sub("[email removed]", text)
    return PHONE.sub("[phone removed]", text)


def version():
    for cand in (Path(os.environ.get("CLAUDE_PLUGIN_ROOT", "")) / ".claude-plugin" / "plugin.json",
                 Path(__file__).resolve().parent.parent / ".claude-plugin" / "plugin.json"):
        try:
            return str(json.loads(cand.read_text()).get("version", "unknown"))[:20]
        except (OSError, ValueError):
            continue
    return "unknown"


def build(skill, stage, rating, comment):
    comment = redact((comment or "").strip())
    if len(comment) > MAX_COMMENT:
        sys.exit(f"That's a bit long — please keep it under {MAX_COMMENT} characters.")
    if not comment and rating is None:
        sys.exit("Nothing to send: add a rating (1-5) or a comment.")
    return {
        "comment": comment,
        "rating": rating,
        "skill": (skill or "")[:40],
        "stage": (stage or "")[:40],
        "version": version(),
        "client_id": scorecard.client_id(),
    }


def send(payload):
    try:
        import requests
    except ImportError:
        sys.exit("requests not installed. Run: python3 -m pip install requests")
    try:
        r = requests.post(FEEDBACK_URL, json=payload, timeout=15,
                          headers={"X-Client-Id": payload["client_id"]})
    except requests.RequestException:
        sys.exit("Couldn't send just now — no connection to the feedback service. "
                 "Nothing was lost; try again later, or skip it.")
    if r.status_code == 201:
        return "Sent. Thank you — this goes straight to the people building 10xcolleges."
    if r.status_code == 429:
        sys.exit("That's plenty of feedback for now — thank you. Try again in an hour if there's more.")
    sys.exit("Couldn't send just now. Nothing was lost; try again later, or skip it.")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skill", default="")
    ap.add_argument("--stage", default="")
    ap.add_argument("--rating", type=int, choices=range(1, 6))
    ap.add_argument("--comment", default="")
    ap.add_argument("--dry-run", action="store_true", help="print the payload, send nothing")
    args = ap.parse_args(argv)
    payload = build(args.skill, args.stage, args.rating, args.comment)
    if args.dry_run:
        print(json.dumps(payload, indent=2))
        return 0
    print(send(payload))
    return 0


if __name__ == "__main__":
    sys.exit(main())
