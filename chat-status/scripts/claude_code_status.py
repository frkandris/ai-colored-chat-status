#!/usr/bin/env python3
"""Update one verified Claude Code session using its documented /rename command."""

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import uuid
import unicodedata

STATES = {"running": "🔵", "waiting": "🟠", "scheduled": "🟣", "complete": "🟢"}
# 🟡 was the "waiting" circle before 2026-11; still stripped so old titles migrate.
PREFIX = re.compile(r"^(?:[🔵🟠🟡🟣🟢][︎️]?\s*)+")
MIN_VERSION = (2, 1, 295)


def config_dir():
    return Path(os.environ.get("CLAUDE_CONFIG_DIR", str(Path.home() / ".claude")))


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
    matches = list((config_dir() / "projects").glob("*/" + session_id + ".jsonl"))
    if len(matches) != 1:
        raise ValueError("Expected exactly one local transcript for the supplied session ID.")
    return matches[0]


def check_version():
    """Require a tested Claude Code version; cache the result per binary path and mtime."""
    binary = shutil.which("claude")
    if not binary:
        raise ValueError("claude is not on PATH.")
    key = binary + ":" + str(os.stat(binary).st_mtime_ns)
    cache = Path(os.environ.get("XDG_CACHE_HOME", str(Path.home() / ".cache"))) / "chat-status-version"
    try:
        if cache.read_text(encoding="utf-8") == key:
            return
    except OSError:
        pass
    version = subprocess.run(
        [binary, "--version"], stdin=subprocess.DEVNULL,
        capture_output=True, text=True, timeout=10, check=True,
    )
    match = re.search(r"(\d+)\.(\d+)\.(\d+)", version.stdout)
    if not match or tuple(map(int, match.groups())) < MIN_VERSION:
        raise ValueError("This adapter requires Claude Code 2.1.295 or later.")
    try:
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(key, encoding="utf-8")
    except OSError:
        pass


def update(session_id, state, title=None, dry_run=False):
    session_id = str(uuid.UUID(session_id))
    transcript = find_transcript(session_id)
    current = read_title(transcript, session_id)
    if current is None and title is None:
        raise ValueError("No persisted title found. Run /rename <descriptive title> first.")
    desired = title_for_state(current if current is not None else title, state)
    if dry_run:
        print(json.dumps({"title": desired, "changed": desired != current, "dry_run": True}, ensure_ascii=False))
        return
    if desired == current:
        return
    check_version()
    # Safe mode avoids loading hooks/skills recursively. No model prompt,
    # permission bypass, environment guard removal, or direct transcript write.
    result = subprocess.run(
        ["claude", "--safe-mode", "-p", "--resume", session_id, "/rename " + desired],
        stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=30,
    )
    if result.returncode or read_title(transcript, session_id) != desired:
        raise ValueError("Claude Code did not confirm the requested title. No retry performed.")


def from_hook(state):
    """Hook mode: read the session ID from the hook's stdin JSON, rename in a detached
    child, and return at once. Prints nothing: UserPromptSubmit stdout enters the context.
    Skipped in the Claude desktop app, which renames through its own session tools."""
    if os.environ.get("CLAUDE_CODE_DESKTOP_APP_VERSION"):
        return 0
    try:
        session_id = str(uuid.UUID(json.load(sys.stdin)["session_id"]))
    except (ValueError, KeyError, TypeError):
        return 0
    subprocess.Popen(
        [sys.executable, os.path.abspath(__file__), "--session-id", session_id, "--state", state],
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session-id", help="Exact current session UUID")
    parser.add_argument("--state", required=True, choices=STATES)
    parser.add_argument("--title", help="User-confirmed title, only if no title metadata exists")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--from-hook", action="store_true", help="Read session_id from hook stdin JSON")
    args = parser.parse_args()
    if args.from_hook:
        return from_hook(args.state)
    if not args.session_id:
        parser.error("--session-id is required")
    try:
        update(args.session_id, args.state, args.title, args.dry_run)
        return 0
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print("chat-status: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
