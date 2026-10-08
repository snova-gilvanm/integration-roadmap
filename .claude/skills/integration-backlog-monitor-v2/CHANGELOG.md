# Changelog

Versions of the `integration-backlog-monitor` skill for the Integrations Roadmap artifact
(https://claude.ai/artifact/MV2P1NUii2NkA5hMSXGbRL). Newest first.

## 2.1.0 (2026-10-08)

Page
- "What the labels mean" legend on the Maintenance tab, hover explanations on every label (`TIP`),
  a live worked score example and a per-asset "How this score was calculated" table.
- "Create in Jira" pop-up: drafts the ticket from the asset's template (editable), creates it with
  the viewer's Atlassian connector (new capability tool `createJiraIssue`), and handles each error code.
  Viewers without the connector keep "Approve for Jira" ("Approved, not in Jira yet").
- Jira checklists: tickets get `- [ ]` checkboxes grouped by stage (To do, In progress, In review,
  Before closing). The page reads them live (second watch, ADF), shows "Checklist d of n" and flags
  "Checklist behind" when the status is ahead of the checklist.
- Team proposals hide themselves once a labelled ticket with the same title exists for the asset;
  otherwise they note the open ticket.
- Fallback when `D.maint` is missing; legend cadence texts read from the data.

Skill
- New golden rule 9: every label on the Maintenance tab has a plain-language explanation.
- Scripts moved out of SKILL.md into `scripts/` (SKILL.md 732 to 188 lines).
- `build.py`: `MAINT_TEMPLATES`, `MAINT_STAGES`, `TPL_OF_KIND`, `tpl` per asset, checklist parsing
  from descriptions (`parse_chk`), term-llm linked to CP-3181.
- Workflow G2 (create tickets) and G4 updated, new G6 (change a template); verification checklist
  covers templates, rule 9 and stubbed connector tests.

Data
- CP-3181 "term-llm maintenance, Oct 2026" created from the upstream template; 14 labelled tickets.

## 2.0.0 (2026-10-06)

- Maintenance tab: KPI tiles, queue (Jira tickets labelled `maintenance` plus proposals),
  inferred asset inventory with tiers, cadences (critical 2, high 3, medium 6, low 12 months),
  score (criticality 40, exposure 30, urgency 30), six-month schedule.
- `D.maint` data block, ticket fields `labels`, `itype`, `ownerOff`, collections `mprop` and `mexp`.
- Live Jira overlay adds tickets missing from the snapshot.
- Maintenance identified only by the Jira label `maintenance` (13 tickets labelled on 2026-10-06).
- Workflow G (maintenance). Renamed to `integration-backlog-monitor-v2`; v1 disabled.

## 1.x

- Original skill by Gilvan Magalhaes: Overview, Board, Timeline, Catalog, Stack rank, Radar,
  How it works; full refresh pipeline (extract, trending, build, gaps, inject).
