---
name: chat-status
description: Status circle (🔵 running, 🟠 needs input, 🟣 scheduled, 🟢 complete) before the chat title. Load once per session; per-turn rules are in the global instruction.
---

# Chat status

Title = one circle + space + the existing title. Strip only leading circles (🔵🟠🟡🟣🟢, with variation selectors and whitespace); change nothing else.

- 🔵 Running: working, or awaiting a running tool.
- 🟠 Needs input: blocked on the user's answer, approval, or access.
- 🟣 Scheduled: run ended; a confirmed, enabled automation on this chat will run again.
- 🟢 Complete: done, nothing blocking, no future run.

Priority 🟠 > 🔵 > 🟣 > 🟢. Rename only when the circle changes: final circle just before the last reply, 🟠 before a blocking question, 🔵 only for long or background work. A plan in prose is not a schedule; an interrupted run is not completion. Unsure of state or chat: leave the title. Subagents never rename. A failed rename never stops the task; report it once.

## Rename

- **Codex desktop:** `mcp__codex_app__set_thread_title` without `threadId`; `mcp__codex_app__list_threads` only when the current title is unknown. Edge cases: [references/codex.md](references/codex.md).
- **Claude desktop app:** `set_session_title("self", …)`; `get_session("self")` only when the current title is unknown. If the user declines, do not retry that turn.
- **Claude Code CLI:** `python3 ${CLAUDE_SKILL_DIR}/scripts/claude_code_status.py --session-id ${CLAUDE_SESSION_ID} --state waiting|scheduled|complete` (also `running` if the hook is not installed). Silent on success. Troubleshooting: [references/claude-code.md](references/claude-code.md).
- **Anything else:** say once that title updates are unavailable; never edit private application state.
