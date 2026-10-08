# Integration Roadmap Skill

This repository contains the **integration-backlog-monitor** skill for maintaining SambaNova's Integrations Roadmap artifact (epic CP-1521).

## Overview

The Integration Backlog Monitor skill provides tools to:
- Refresh Jira, docs, and radar data
- Edit and add content to the integrations roadmap
- Add new data sources while keeping existing templates
- Use only official sources (no invented information)

## Quick Start

The skill is available at: https://claude.ai/customize/skills/id/plugin_01BMr4bAmKNAQSpWnsCxDtTq

To use it, invoke the skill when you need to:
- Update, refresh, or fix the integrations roadmap page
- Edit the kanban board, timeline, catalog, or stack rank
- Manage the radar (trending tools, competitor gaps)
- Maintain the integration backlog

## Repository Structure

```
.
├── .claude/
│   └── skills/
│       └── integration-backlog-monitor/
│           └── SKILL.md          # Skill definition and workflows
├── README.md                      # This file
├── .gitignore                     # Git ignore rules
└── CLAUDE.md                      # Project guidelines
```

## Key Documentation

See `.claude/skills/integration-backlog-monitor/SKILL.md` for:
- Golden rules for maintaining the roadmap
- Official data sources and how to access them
- Page architecture and components
- Workflow procedures (A-F)
- Script reference for full refresh operations

## Development

### Adding a New Data Source
1. Confirm with the user which official source and what question it answers
2. Fetch it into `$WORK/<source>.json`
3. Update `build.py` with the new key
4. Document the snapshot date and formula changes

### Updating Roadmap Metadata
Update the `PLAN` dictionary in `build.py` for new slotted tickets with: `(slug, category, [modes], iface, door)`

## Official Sources

- **Jira**: Epic CP-1521 and child tickets
- **Docs**: `sambanova/docs` repo, `origin/main`
- **Live**: docs.sambanova.ai
- **GitHub metrics**: shields.io (stars, commits, releases, contributors)
- **Competitors**: Cerebras, Groq, Together, Fireworks, Novita, xAI, DeepSeek

## Related Links

- **Artifact**: https://claude.ai/artifact/MV2P1NUii2NkA5hMSXGbRL
- **Jira Epic**: CP-1521
- **Docs Repo**: https://github.com/sambanova/docs

## Version History

See git commits for change history and version tracking.

---

Maintained by: Gilvan Magalhaes  
Last updated: 2026-10-08
