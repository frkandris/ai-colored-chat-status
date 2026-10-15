# Claude Code adapter

The same `chat-status` skill runs in Codex desktop and Claude Code. Claude Code uses a bundled Python helper that invokes the documented non-interactive `/rename` command, rather than writing session storage directly.

## Requirements

- Local Claude Code **2.1.295+**, with `claude` available on PATH and an existing authenticated setup.
- Python **3.9+** (standard library only).
- A verified current session UUID and exactly one matching local transcript.
- A persisted descriptive title. If the title is unavailable, initialize it with `/rename Your descriptive title` and invoke `/chat-status` again.

The helper was smoke-tested with Claude Code **2.1.295**, including a `CLAUDECODE=1` environment. The upstream `/rename` command supports print mode from 2.1.205, but this adapter conservatively requires the tested version or later. A currently open UI may need a refresh to display a title changed by a separate CLI process. Web/Cowork chats and remote-only sessions are outside this adapter's scope.

## Install

From a clone of this repository:

```bash
mkdir -p ~/.claude/skills
cp -R chat-status ~/.claude/skills/
```

If the target already exists, back it up or deliberately replace it. Claude Code discovers personal skills under `~/.claude/skills`; Codex uses its own skill discovery directory. You can install the same folder in both.

Invoke in Claude Code:

```text
/chat-status
```

Or ask Claude Code to use the skill throughout your task.

## Agent workflow

The session UUID supplied by the main `SKILL.md` comes from Claude Code's documented `${CLAUDE_SESSION_ID}` substitution. The skill folder comes from `${CLAUDE_SKILL_DIR}`. Those are skill substitutions, not promises that shell environment variables of the same name exist. Use their expanded literal values.

Invoke the helper with the current session UUID and desired state. For example, replacing the two placeholders with their verified absolute path and UUID:

```bash
python3 /absolute/path/chat-status/scripts/claude_code_status.py \
  --session-id <current-session-uuid> --state running
```

States: `running`, `waiting`, `scheduled`, `complete`. `--dry-run` calculates the proposed title without invoking Claude. `--title 'User-confirmed name'` initializes a title only when no persisted title exists; it never overrides an existing descriptive title.

The helper locates only the exact UUID's transcript, reads title metadata, strips repeated leading status circles, and invokes `claude --safe-mode -p --resume <uuid> '/rename <title>'`. Safe mode avoids recursively loading skills and hooks. Child stdin is closed so shell input cannot accidentally become part of the title. After execution, the helper verifies the saved title; it makes no automatic retry on failure.

It preserves runtime guards and permissions. It never uses `--continue`, removes nesting guards, launches a model prompt, or directly edits transcripts. If the host rejects the command or the session cannot be resolved, continue the main task and report the unavailable status update once. Do not guess another session.

## Schedule evidence

Use the host's documented schedule tools or confirmed schedule metadata for the exact session; do not infer a future run from a reminder in prose.

## Enable on every turn

Append the following to `~/.claude/CLAUDE.md`, preserving existing instructions:

```markdown
## Chat status

Prefix this chat's title with exactly one status circle and a space; keep the rest of the title and replace an existing circle. 🔵 working · 🟡 blocked on my answer or approval · 🟣 run ended, a confirmed automation on this chat will run again · 🟢 done. Priority 🟡 > 🔵 > 🟣 > 🟢. Set 🔵 at turn start and the final circle just before the last reply. Subagents never rename. Claude desktop app: use `get_session`/`set_session_title` with "self". Claude Code CLI: invoke the chat-status skill once per session for the rename command.
```

The rules live in the instruction itself (about 550 characters), so the full skill is not loaded on every turn. In the CLI the skill is still needed once per session, because only a skill receives the `${CLAUDE_SESSION_ID}` substitution.

This instruction requests lifecycle updates; it does not create an independent hook listener. Remove this section to disable persistent tracking. Existing prefixes remain until renamed.

## References

- [Claude Code commands](https://code.claude.com/docs/en/commands): `/rename`, including print-mode support and title limits.
- [CLI reference](https://code.claude.com/docs/en/cli-reference): `--resume`, `--safe-mode`, and `--print`.
- [Skills documentation](https://code.claude.com/docs/en/skills): local skill paths and current-session substitutions.
