# Claude Code CLI adapter

Read this only when the short rules in `SKILL.md` do not settle a case. Setup lives in [claude-code-setup.md](claude-code-setup.md).

## Invocation

Use the expanded literal values of `${CLAUDE_SKILL_DIR}` and `${CLAUDE_SESSION_ID}` (skill substitutions, not shell variables):

```bash
python3 /absolute/path/chat-status/scripts/claude_code_status.py --session-id <uuid> --state complete
```

- States: `running`, `waiting`, `scheduled`, `complete`. With the `UserPromptSubmit` hook installed, `running` is set automatically at turn start.
- Success prints nothing. `--dry-run` prints the proposed title as JSON without renaming.
- `--title 'User-confirmed name'` initializes a title only when none is persisted; it never overrides an existing one.

The helper reads title metadata from the exact UUID's transcript, strips leading circles, and runs `claude --safe-mode -p --resume <uuid> '/rename <title>'` with stdin closed, then verifies the saved title. No retry, no `--continue`, no direct transcript writes.

## Troubleshooting

| Error | Action |
| --- | --- |
| `No persisted title found` | Ask the user for a title, or have them run `/rename <title>`, then retry once. |
| `Expected exactly one local transcript` | The session is remote, or the UUID is wrong. Never guess another session; report once. |
| `requires Claude Code 2.1.295 or later` | Report once; the user must upgrade. |
| `did not confirm the requested title` | Report once and continue the task. An open UI may need a refresh to show a changed title. |

## Schedule evidence

Use the host's schedule tools or confirmed schedule metadata for the exact session; a reminder in prose is not a schedule.
