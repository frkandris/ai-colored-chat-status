# Chat Status

**Know which Codex chat is working, waiting, scheduled, or done—at a glance.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent-Skill-7c3aed)](chat-status/SKILL.md)
[![Codex desktop](https://img.shields.io/badge/Works_with-Codex_desktop-111827)](#requirements)

Chat Status is a small, instruction-only agent skill that adds a colored circle to your existing chat title. It preserves the title you chose and updates the prefix as work progresses.

```text
🔵 Fix the checkout bug
🟡 Review the deployment plan
🟣 Monitor tomorrow's release
🟢 Write the migration guide
```

## Status colors

| Circle | Status | When it appears |
| --- | --- | --- |
| 🔵 | **Running** | The agent is actively working or waiting for a running tool. |
| 🟡 | **Needs input** | Progress depends on your answer, approval, or access. |
| 🟣 | **Scheduled** | This run has ended and a confirmed, enabled future run is attached to this chat. |
| 🟢 | **Complete** | The requested work is finished and no future run is attached. |

A blocking dependency takes priority over active work. After a run ends, a verified future schedule takes priority over completion. An idle or interrupted agent is not automatically marked complete.

## Requirements

- **Codex desktop**, with `mcp__codex_app__list_threads` and `mcp__codex_app__set_thread_title` available to the agent.
- A local installation of this skill.
- For status tracking on every turn, the persistent instruction described below.

The instructions use the Agent Skills format, but renaming requires these Codex desktop tools. **Claude, Claude Code, and Codex CLI sessions without desktop title tools are not supported by this version.** There is no daemon, API key, browser extension, or runtime dependency.

## Quick start

### 1. Install the skill

Clone the repository and copy the skill into your user-level skills directory:

```bash
git clone https://github.com/frkandris/chat-status.git
mkdir -p ~/.agents/skills
cp -R chat-status/chat-status ~/.agents/skills/
```

If you already have a `chat-status` installation, back it up or deliberately replace it rather than creating a nested duplicate. The repository root is the package; the inner `chat-status/` folder is the installable skill.

Codex's [official skill documentation](https://learn.chatgpt.com/docs/build-skills) describes current discovery locations. Restart Codex if the skill does not appear.

### 2. Try it in a chat

```text
Use $chat-status during this task. Summarize the README in this repository.
```

The title should become 🔵 while the agent works, then 🟢 when it finishes. Explicit invocation applies to the current task; use global activation for ongoing tracking.

### 3. Enable it for every turn

Follow the [global activation guide](chat-status/references/global-activation.md) to add a short instruction to your Codex home `AGENTS.md`. The guide includes the exact snippet, path resolution, precedence rules, verification, and removal steps.

Installation alone does not guarantee the skill is loaded on every turn. Each enabled chat updates its own title as it runs.

## How it works

1. Read and identify the current chat's title through desktop tools.
2. Select a state from the actual task outcome and any verified schedule.
3. Replace existing leading status circles with exactly one circle and one space.
4. Preserve the descriptive title verbatim, including its language and other emoji.

For example, `🟡 🔵 Fix checkout` becomes `🟢 Fix checkout` when the work is complete. A user rename is preserved on the next update. Subagents do not rename their parent's chat.

The skill only changes chat titles. It does not create schedules, send notifications, or inspect external services merely to choose a color.

## Limitations

- Updates happen when the agent can act. This is **not real-time event synchronization**.
- Crashes, forced interruptions, unexpected approval prompts, or schedule changes made elsewhere can leave a prefix stale until another turn.
- If the current chat cannot be identified reliably, the skill leaves its title unchanged.
- Missing desktop tools cannot be supplied by installing a Markdown skill.
- Global activation does not install or enable the skill on another person's computer.

## Repository layout

```text
chat-status/
├── README.md
├── LICENSE
└── chat-status/
    ├── SKILL.md                       # Agent instructions
    ├── agents/openai.yaml             # English UI metadata
    └── references/global-activation.md
```

## Contributing

Issues and focused pull requests are welcome. Describe the environment, the expected title, and the observed result. Use fictional examples or redact private chat content.

Keep changes instruction-only unless a concrete capability requires code. Preserve the title, use verified state evidence, and avoid claiming support for tools the target environment does not expose. When changing lifecycle behavior, check active work, required input, completion, and a verified attached schedule.

## Origin and license

Created by [András Tóth](https://github.com/frkandris). This English edition is adapted from the `chat-status` skill in the STRT skills collection, source revision `3b0c4415280047249925da787cf33b9ee2689266` (2026-10-12). It retains the four-state lifecycle and title-preservation behavior, with English metadata and setup documentation.

Released under the [MIT License](LICENSE). This is an independent project and is not affiliated with or endorsed by OpenAI or Anthropic.
