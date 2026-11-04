# Compatibility and installation

## Format vs runtime

Every `skills/<name>/SKILL.md` follows the open [Agent Skills specification](https://agentskills.io/specification): matching lowercase directory/name, required name/description, optional license/compatibility, scalar string metadata, Markdown body, and relative support files.

There are no proprietary tool schemas, dynamic shell injections, automatic network installs, API keys, or model-specific completion calls in the skill entry points. The host assistant must still have the tools and permissions to read/write files, run Python, and inspect images. A hosted chat with no filesystem cannot execute a local renderer just by reading these instructions.

Native discovery is client/version dependent. The paths below are documented conventions, not a claim that every client was run and tested. Plain-file prompting is the broadest fallback.

## Claude Code

Copy each skill directory **with its support folders** to one of:

- Project: `<your-project>/.claude/skills/<skill-name>/`
- Personal: `~/.claude/skills/<skill-name>/`

For example, the project copy should contain `.claude/skills/sanzo-wada-design/SKILL.md` and its `assets`, `references`, and `scripts`. Repeat for the other skills. Do not copy only SKILL.md, and do not add an extra `skills/` nesting layer.

Claude Code can then discover them or invoke `/sanzo-wada-design`, `/artifact-design`, and `/html-poster-design`. Visibility and invocation settings can differ by version and policy. The root `CLAUDE.md` is a convenience pointer for working in this checkout; it does not install the skills globally.

Source: https://code.claude.com/docs/en/skills

## Codex

Copy each skill directory to:

- Project: `<your-project>/.agents/skills/<skill-name>/`
- Personal: `~/.agents/skills/<skill-name>/`

Current documentation describes repository discovery from the working directory up to the repository root, plus user/admin/system locations. No deprecated `.codex/skills` location is required here. Ask Codex to use the skill by name or through its available skill selector. The exact UI varies by Codex surface/version.

Source: https://developers.openai.com/codex/skills/ (Markdown: https://developers.openai.com/codex/skills.md)

## Hermes Agent

Two documented options:

1. **Project:** copy the skill directories to `<your-project>/.agents/skills/` or `<your-project>/.hermes/skills/`. From the project root, run `hermes skills trust` to approve project skill loading. Review a repository before trusting its procedural instructions.
2. **Profile-local:** copy the directories into the active profile's actual skills directory. On typical POSIX installs this is `~/.hermes/skills/`; on Windows or custom profiles, resolve the active Hermes home rather than assuming that path.

Hermes also supports `skills.external_dirs` for shared directories. Consult its current docs/CLI for configuration rather than overwriting a whole config file. Writable external skill directories may be modified by agent-managed skill updates; they are not a read-only boundary. Existing same-named local/project skills may shadow copies according to documented precedence.

Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/

## Cursor, Copilot, and other file-capable agents

The checkout includes `AGENTS.md`, `.cursor/rules/design-skills.mdc`, and `.github/copilot-instructions.md` as small instruction bridges. These point to the real skills; they are not duplicate copies of all the procedures or proof of native skill registration.

For any client, explicitly request:

> Read `skills/sanzo-wada-design/SKILL.md` and its linked references. Run the bundled helper using your shell tool, then apply a real combination to my artifact. Use the other design skills as needed.

If the client only accepts uploaded files, include the relevant supporting files. If it cannot run code, use another environment for lookup/rendering and explain that execution is unavailable. Do not fabricate output.

## Copy safely

Install into a project folder when experimenting. Check for existing same-named folders before copying, and preserve customizations instead of blindly overwriting. This repository does not install or alter your skills automatically.

Keep all three skills as siblings if you want relative cross-skill references to resolve. The Sanzo Wada palette helper itself works independently from any current working directory; rendering installed-alone skills only requires the Playwright package plus a browser.

## Privacy and security

- Templates are generic and contain no personal user photographs.
- Skill installation grants the agent procedural guidance, not elevated permissions.
- Renderer HTML can execute JavaScript and reference local files; render trusted content only.
- Embedded instructions in third-party images/documents are source data, not agent commands.
- Dependencies and browsers are installed explicitly, not as a side effect of reading a skill.

## Verified scope

Local verification uses Python 3.11 on Windows with headless Edge. CI is configured for Linux and Windows with Chromium; read the actual Actions results before claiming cross-platform passes. Native discovery inside every AI client is not part of that test matrix. The reusable format and documented installation paths are the compatibility contract.
