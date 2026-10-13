#!/usr/bin/env python3
"""Update one verified Claude Code session using its documented /rename command."""

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import uuid
import unicodedata

STATES = {"running": "🔵", "waiting": "🟡", "scheduled": "🟣", "complete": "🟢"}
PREFIX = re.compile(r"^(?:[🔵🟡🟣🟢][\ufe0e\ufe0f]?\s*)+")


def title_for_state(title, state):
    description = PREFIX.sub("", title)
    if not description.strip():
        raise ValueError("The descriptive title is empty. Initialize it with /rename first.")
    result = STATES[state] + " " + description
    # Claude Code sanitizes and truncates names; refuse to silently change them.
    if len(result) > 200 or any(
        unicodedata.category(c) in ("Cc", "Cf") for c in result
    ):
        raise ValueError("The title exceeds 200 characters or contains invisible controls.")
    return result


def read_title(transcript, session_id):
    custom = None
    with transcript.open(encoding="utf-8") as stream:
        for line in stream:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue  # A running session may have a partially written last line.
            if not isinstance(row, dict) or row.get("sessionId") != session_id:
                continue
            if row.get("type") == "custom-title" and isinstance(row.get("customTitle"), str):
                custom = row["customTitle"]
    return custom


def find_transcript(session_id):
    config = Path(os.environ.get("CLAUDE_CONFIG_DIR", str(Path.home() / ".claude")))
    matches = list((config / "projects").glob("*/" + session_id + ".jsonl"))
    if len(matches) != 1:
        raise ValueError("Expected exactly one local transcript for the supplied session ID.")
    return matches[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session-id", required=True, help="Exact current session UUID")
    parser.add_argument("--state", required=True, choices=STATES)
    parser.add_argument("--title", help="User-confirmed title, only if no title metadata exists")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        session_id = str(uuid.UUID(args.session_id))
        transcript = find_transcript(session_id)
        current = read_title(transcript, session_id)
        if current is None and args.title is None:
            raise ValueError("No persisted title found. Run /rename <descriptive title> first.")
        desired = title_for_state(current if current is not None else args.title, args.state)
        if args.dry_run or desired == current:
            print(json.dumps({"title": desired, "changed": False, "dry_run": args.dry_run}))
            return 0
        version = subprocess.run(
            ["claude", "--version"], stdin=subprocess.DEVNULL,
            capture_output=True, text=True, timeout=10, check=True,
        )
        match = re.search(r"(\d+)\.(\d+)\.(\d+)", version.stdout)
        if not match or tuple(map(int, match.groups())) < (2, 1, 295):
            raise ValueError("This adapter requires Claude Code 2.1.295 or later.")
        # Safe mode avoids loading hooks/skills recursively. No model prompt,
        # permission bypass, environment guard removal, or direct transcript write.
        result = subprocess.run(
            ["claude", "--safe-mode", "-p", "--resume", session_id, "/rename " + desired],
            stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=30,
        )
        if result.returncode or read_title(transcript, session_id) != desired:
            raise ValueError("Claude Code did not confirm the requested title. No retry performed.")
        print(json.dumps({"title": desired, "changed": True}))
        return 0
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print("chat-status: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
