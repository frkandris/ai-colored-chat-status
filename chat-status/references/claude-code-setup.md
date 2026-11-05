# Enable status tracking in Claude Code

For Codex desktop, use the [global activation guide](global-activation.md). This file is read once, during setup; it is not needed on later turns.

## Requirements

- Claude desktop app (Code tab): nothing beyond the global instruction below. The app's own `get_session` and `set_session_title` tools rename the chat.
- Claude Code CLI (local): Claude Code **2.1.295+** with `claude` on PATH and an authenticated setup, Python **3.9+** (standard library only), and a persisted title (`/rename Your descriptive title`).

The CLI helper calls the documented non-interactive `/rename` command instead of writing session storage. It was smoke-tested with Claude Code 2.1.295, including a `CLAUDECODE=1` environment. Web/Cowork chats and remote-only sessions are out of scope.

## 1. Install the skill

From a clone of this repository:

```bash
mkdir -p ~/.claude/skills
cp -R chat-status ~/.claude/skills/
```

If the target already exists, back it up or deliberately replace it. You can install the same folder for Codex too.

## 2. Add the global instruction

Append this section to `~/.claude/CLAUDE.md`, preserving existing instructions:

```markdown
## Chat status

Title = one circle + space + existing title (replace any leading circle). 🔵 working · 🟠 blocked on my answer or approval · 🟣 ended, a confirmed automation on this chat reruns · 🟢 done. Priority 🟠>🔵>🟣>🟢. Rename only when the circle changes: final circle just before the last reply, 🔵 only for long or background work. Subagents never rename. Desktop app: set_session_title("self"), get_session("self") only if the title is unknown. CLI: load chat-status once per session.
```

The rules live in the instruction (about 470 characters), so the skill is not loaded on every turn. In the CLI the skill is still loaded once per session, because only a skill receives the `${CLAUDE_SESSION_ID}` substitution.

## 3. CLI only: set 🔵 with a hook

Optional, but it removes the turn-start rename from the model's work entirely. Add to `~/.claude/settings.json` (merge with existing `hooks`):

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/skills/chat-status/scripts/claude_code_status.py --from-hook --state running"
          }
        ]
      }
    ]
  }
}
```

The hook reads `session_id` from its stdin JSON, starts the rename in a detached process, and returns immediately without output, so it adds no prompt latency and no context. It does nothing in the Claude desktop app. The rename itself runs `claude --safe-mode`, which does not load hooks, so it cannot recurse.

## 4. Verify

Start a session, `/rename` it, and ask for a short task. The title should show 🔵 while working and 🟢 when finished; ask something that needs your answer to check 🟠.

## Disable

Remove the `## Chat status` section, the hook entry, and optionally `~/.claude/skills/chat-status`. Existing prefixes remain until the chats are renamed.

## References

- [Claude Code commands](https://code.claude.com/docs/en/commands): `/rename`, print-mode support, title limits.
- [CLI reference](https://code.claude.com/docs/en/cli-reference): `--resume`, `--safe-mode`, `--print`.
- [Hooks](https://code.claude.com/docs/en/hooks): `UserPromptSubmit` input and output.
- [Skills](https://code.claude.com/docs/en/skills): skill paths and session substitutions.
