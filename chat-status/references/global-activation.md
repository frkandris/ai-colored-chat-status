# Enable status tracking across Codex desktop chats

For Claude Code, use the separate [Claude Code activation guide](claude-code.md).

Installing the skill makes it discoverable. To request status updates on every root-agent turn, also add a persistent instruction to your Codex home `AGENTS.md` (normally `~/.codex/AGENTS.md`). Preserve existing instructions. If `CODEX_HOME` is set, use that directory instead.

The instruction carries the rules itself (about 500 characters), so the full `SKILL.md` is not re-read on every turn. Global instructions sit at the start of every context window; keep them short.

## Setup

1. Install the `chat-status` folder in a skill location recognized by your Codex installation. The current user-level location is `~/.agents/skills/chat-status`.
2. Resolve the absolute path to the installed `SKILL.md`:

   ```bash
   realpath ~/.agents/skills/chat-status/SKILL.md
   ```

3. Append the following section to your Codex home `AGENTS.md`. Replace `<installed-skill-absolute-path>` with the output from step 2, including `/SKILL.md`.

   ```markdown
   ## Chat status

   Prefix this chat's title with exactly one status circle and a space; keep the rest of the title and replace an existing circle. 🔵 working · 🟡 blocked on my answer or approval · 🟣 run ended, a confirmed automation on this chat will run again · 🟢 done. Priority 🟡 > 🔵 > 🟣 > 🟢. Set 🔵 at turn start and the final circle just before the last reply. Subagents never rename. Rename with the desktop title tools; for an unclear chat, title, or schedule, read <installed-skill-absolute-path> once.
   ```

4. If `AGENTS.override.md` exists in Codex home, it takes precedence over `AGENTS.md`. Add the section to the active instructions file while preserving its other contents.
5. Start a new chat, or reopen an existing chat if necessary, and ask for a short task. Confirm that the title shows 🔵 while working and 🟢 when finished. Ask a task requiring an answer to check 🟡. Test 🟣 only with a real, enabled automation attached to that chat.

Installing the skill or sharing its repository does not automatically configure other users' machines. Global activation means each chat updates its own title when it runs; it does not authorize bulk renaming of other chats.

## Disable

Remove only the chat-status section you added to the active global instructions file. Remove the installed skill folder if you also want to stop explicit invocation. Existing title prefixes remain until you rename those chats; removing the instructions does not run a cleanup operation.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Skill is missing from discovery | Confirm the folder contains `SKILL.md` in a recognized skill location; restart Codex if necessary. |
| Tracking works only when explicitly requested | Confirm the global instruction is loaded and points to the actual absolute file path. |
| Global instruction appears ignored | Check `CODEX_HOME`, `AGENTS.override.md`, and applicable project instructions. |
| Chat does not get renamed | Confirm the desktop exposes the thread listing and title update tools. Installing this skill cannot add those tools. |
| A circle remains after an interruption | Run another turn. The skill has no independent event listener to repair titles while the agent is stopped. |

See official documentation for [skill discovery](https://learn.chatgpt.com/docs/build-skills) and [global instruction precedence](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
