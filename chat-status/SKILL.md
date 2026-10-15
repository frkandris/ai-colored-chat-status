---
name: chat-status
description: Keep one colored status circle (🔵 running, 🟡 needs input, 🟣 scheduled, 🟢 complete) at the start of the chat title. Use on every turn when chat status tracking is enabled.
---

# Chat status

Keep the existing title and prefix it with exactly one circle and a space. Strip only leading circles from `🔵 🟡 🟣 🟢` (with variation selectors and the following whitespace); change nothing else. Skip the update if the title already matches.

- 🔵 **Running** — actively working, or awaiting a running tool.
- 🟡 **Needs input** — progress is blocked on the user's answer, approval, or access.
- 🟣 **Scheduled** — this run ended and a confirmed, enabled automation attached to this chat will run again.
- 🟢 **Complete** — done, nothing blocking, no future run attached.

Priority: 🟡 > 🔵 > 🟣 > 🟢. Set 🔵 at turn start, 🟡 before a blocking question or approval request, and the final circle just before the last reply. A plan in prose ("check on Monday") is not a schedule; an idle or interrupted runtime is not completion. If the state or the current chat is uncertain, leave the title unchanged. Subagents never rename the parent chat. A failed update never stops the main task; report it once.

## How to rename

- **Codex desktop:** `mcp__codex_app__list_threads`, then `mcp__codex_app__set_thread_title` without `threadId`. Ambiguous chat or schedule evidence: [references/codex.md](references/codex.md).
- **Claude desktop app (Code tab):** `get_session("self")` for the title, then `set_session_title("self", ...)`. If the user declines a rename approval, do not retry that turn.
- **Claude Code CLI:** `python3 ${CLAUDE_SKILL_DIR}/scripts/claude_code_status.py --session-id ${CLAUDE_SESSION_ID} --state running|waiting|scheduled|complete`. Never guess another session. Title initialization, schedule evidence, troubleshooting: [references/claude-code.md](references/claude-code.md).
- **Anything else:** say once that automatic title updates are unavailable; never edit private application state.
