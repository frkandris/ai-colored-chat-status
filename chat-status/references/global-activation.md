# Enable status tracking across Codex desktop chats

Installing the skill makes it discoverable. To request status updates on every root-agent turn, also add a persistent instruction to your Codex home `AGENTS.md` (normally `~/.codex/AGENTS.md`). Preserve existing instructions. If `CODEX_HOME` is set, use that directory instead.

## Setup

1. Install the `chat-status` folder in a skill location recognized by your Codex installation. The current user-level location is `~/.agents/skills/chat-status`.
2. Resolve the absolute path to the installed `SKILL.md`:

   ```bash
   realpath ~/.agents/skills/chat-status/SKILL.md
   ```

3. Append the following section to your Codex home `AGENTS.md`. Replace `<installed-skill-absolute-path>` with the output from step 2, including `/SKILL.md`.

   ```markdown
   ## Codex desktop chat status

   The user has enabled chat-status tracking in all Codex desktop chats. In every root-agent turn, including scheduled turns, read and follow the chat-status SKILL.md at <installed-skill-absolute-path> when desktop thread-title tools are available. This authorizes updating the calling chat's status prefix without asking again; preserve the descriptive title. Subagents must not rename the parent chat.
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
