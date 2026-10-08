# integration-roadmap

Version-controlled home of the **Integrations Roadmap** artifact and the Claude skill that maintains it.

- Artifact (claude.ai, owner Gilvan Magalhaes): https://claude.ai/artifact/MV2P1NUii2NkA5hMSXGbRL
- Jira epic: CP-1521

## Layout

```
integration-backlog-monitor-v2/   the skill (what gets installed)
  SKILL.md                        instructions Claude follows
  CHANGELOG.md                    what changed in each version
  scripts/                        refresh pipeline: extract, trending, build, gaps, inject
artifact/index.html               the last published page (snapshot for diffs and tests)
tests/check_build.py              regression check: build.py must reproduce the page's maintenance data
```

## Making a change

1. Branch, edit the skill (and `artifact/index.html` if the page changed).
2. Run `python3 tests/check_build.py`.
3. Add an entry to `integration-backlog-monitor-v2/CHANGELOG.md` and bump the version line in `SKILL.md`
   (major: breaking data or workflow change; minor: new feature; patch: fixes and wording).
4. Open a PR; tag the merge `vX.Y.Z`.

## Releasing the skill

Package the folder and hand the file to whoever manages the organization's plugins:

```
zip -r integration-backlog-monitor-v2.skill integration-backlog-monitor-v2 -x '*/__pycache__/*'
```

The installed skill name stays `integration-backlog-monitor-v2` so each release replaces it in place.
Keep the old `integration-backlog-monitor` (v1) disabled.

## After publishing the page

Copy the published page into `artifact/index.html` (ask Claude to read the artifact and give you the file)
and commit it with the matching changelog entry, so the repo always mirrors what is live.
