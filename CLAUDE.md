# Project Guidelines

## Skill Development

This repository maintains the **integration-backlog-monitor-v2** skill for managing SambaNova's integrations roadmap.

### Core Principles

1. **Official sources only** - Every fact must come from verified official sources listed in SKILL.md
2. **No invented information** - If something cannot be verified, mark it as unknown
3. **Version control** - All skill changes are tracked in git
4. **Golden rules** - Always read and apply the 8 golden rules in SKILL.md before making changes

### Before Making Changes

1. Check the "Golden rules" section in `.claude/skills/integration-backlog-monitor-v2/SKILL.md`
2. Verify all facts against official sources
3. Never use the em dash character (U+2014) in your text
4. If publishing changes, always read the artifact first with `Artifact action:"read"`

### Workflow Guidelines

- **Workflows A-F** in SKILL.md define how to make different types of changes
- Use subagents for large data fetches (Jira, docs repo, GitHub metrics)
- Always check the verification checklist before publishing
- Confirm with the user before creating/editing Jira issues or Confluence pages

### Scripts

The skill includes Python scripts for:
- `extract.py` - Extract guide metadata from docs repo
- `trending.py` - Collect trending tool metrics
- `build.py` - Build the data structure from all sources
- `gaps.py` - Analyze competitor integration gaps
- `inject.py` - Inject data into the HTML artifact

Always run scripts in order during a full refresh:
```bash
extract.py → trending.py → build.py → gaps.py → build.py → inject.py
```

### Commit Messages

Use clear, descriptive commit messages:
- Format: `<type>: <short description>`
- Types: `feat`, `fix`, `docs`, `refactor`, `chore`
- Example: `feat: add ragas integration to Q1 2027 roadmap`

### Before Pushing to GitHub

1. Verify all scripts and data files are included
2. Check that no sensitive information is in the repository
3. Ensure `.gitignore` covers work files and temporary data
4. Test that the skill still references the correct artifact URL

## Contact

- Owner: Gilvan Magalhaes (gilvan.magalhaes@sambanovasystems.com)
- Related Jira: CP-1521
- Artifact: https://claude.ai/artifact/MV2P1NUii2NkA5hMSXGbRL
