# QCET Reporting v1.0

An evidence-based reporting skill for the Digital and Communications Center, Quy Nhon College of Engineering and Technology (QCET). The skill is designed to work alone or next to `qcet-work-planning`.

**The skill does not include any genuine school records, student/personnel data, login credentials, or approved school templates.** The example is clearly synthetic and must not be reported as real performance.

## What it does

- Drafts Center monthly, quarterly, school-year and ad hoc reports in Vietnamese.
- Keeps five reporting views: MANAGEMENT plus four VTVL groups (IT/DX, communications, statistics, education support).
- Reconciles plan tasks, operational results, deliverables and verifiable evidence.
- Separates verified-looking input from unverified/pending figures and documents open questions.
- Guards against double counting deliverables, people, management activities and report products.
- Treats monthly period M as 25th of preceding month to 24th of M unless an official directive overrides it.
- Prints a draft report to stdout and validates the structure with offline, standard-library Python 3 scripts.

## Files

- `SKILL.md` - primary workflow and non-mutation rules for agents.
- `references/center-scope.md` - Center's functional workstreams, reused as a domain starting point from qcet-work-planning.
- `references/reporting-rules.md` - operational cadence, scope, reconciliation and cross-skill handoff.
- `references/source-and-metrics.md` - data lineage, metric aggregation and verified claims.
- `references/report-templates.md` - flexible forms for monthly, quarterly, annual, evaluation and briefings.
- `references/data-contract.md` - input data format and invariant checks.
- `references/acceptance-tests.md` - quality and acceptance checklist.
- `references/openmausbot.md` - compatibility and repository references.
- `scripts/periods.py` - date and week calculations.
- `scripts/validate_report.py` - offline structural and consistency validation.
- `scripts/draft_report.py` - conservative Markdown scaffold from JSON, printed to stdout.
- `examples/report-2026-11.synthetic.json` - safe demonstrator input, all information fake.
- `tests/` - test suite (no external Python dependency).
- `agents/openai.yaml` - optional display metadata for engines that recognize it.

## OpenMausBot import via GitHub

OpenMausBot's bot Skills UI currently accepts a GitHub repository URL, a skill-folder URL or an SKILL.md URL (and certain skills.sh URLs). **It does not accept `skill.zip` in that GitHub URL input.**

1. Extract `skill.zip` to a folder named `qcet-reporting`.
2. Upload only the extracted skill folder to a GitHub repository under your control. This package contains no real private school data.
3. In OpenMausBot, choose the desired bot -> Settings -> Skills. Paste a URL such as:
   `https://github.com/YOUR-ACCOUNT/YOUR-REPO/tree/main/qcet-reporting`
4. Import; inspect SKILL.md and any warning; only then enable the imported skill. Set bot approvals to Ask (not Full access), and restrict local-computer and connected-app privileges separately.
5. Give the bot an officially sourced Center plan plus results and evidence, then request a DRAFT report. Neither a repository import nor this skill automatically grants access to Google Drive/Sheets or school files.

If you do not want public GitHub hosting, ask your OpenMausBot engine to read the local skill folder. For Claude Code, a commonly supported user location on Windows is `%USERPROFILE%\.claude\skills\qcet-reporting`; for Codex, project-level `.agents\skills\qcet-reporting` is recommended. Whether your OpenMausBot bot detects the native skill depends on its provider and runtime; confirm in the bot's Skills list. Do not assume a ZIP has been installed simply by unpacking it somewhere.

## Windows offline verification

Open PowerShell, change directory to `qcet-reporting`, and run:

```powershell
python scripts\periods.py --month 2026-11
python scripts\validate_report.py examples\report-2026-11.synthetic.json
python scripts\draft_report.py examples\report-2026-11.synthetic.json
python -m unittest discover -s tests -v
```

Python 3.9+ recommended. Scripts do not access the network, mutate school data or save report files. `draft_report.py` creates a **technical English Markdown scaffold** for inspection; the bot using this skill must localize its final management report to professional Vietnamese and follow any official template.

## Safe first-run prompt

```text
Use qcet-reporting to draft the Center's November 2026 operational report covering 25 Oct to 24 Nov 2026. Source only the approved Center work plan and actual logs I provide, cover MANAGEMENT, IT_DX, COMMUNICATIONS, STATISTICS and EDU_SUPPORT, reconcile plan IDs and evidence, and produce professional Vietnamese. Mark all unknown figures and owners, identify duplicated metrics and conflicting sources, and return the draft plus a verification ledger. Read only; no saves, email, Sheet updates or publishing.
```

## Reporting dependencies

To produce a real report, supply the school-approved report form (if any), a documented period, current Center function/assignment information, approved plan, evidence-backed work logs, statistic definitions and the person authorized to review. Historical 2025-2026 figures should not be silently reused in reporting for 2026-2027. Annual personnel/collective ratings are never inferred by the skill.

## Verification and known limitations

`validate_report.py` checks structure, period and selected consistency rules. Its PASS does **not** prove that the evidence truly exists, that a figure is correct or that the report is legally approved. The Markdown skeleton's use of 'verified' refers only to flags within the supplied JSON; an authorized human must inspect sources. The tool does not log in to services, create live dashboards, publish documents or run in the background.

OpenMausBot code references checked from `milind-soni/OpenMausBot` in the earlier planning-skill build (2026-11-09):
- `server/routes/bot-skills.ts`
- `server/skill-folder.ts`
- `src/components/bot-settings/SkillsSection.tsx`
- `docs/headless-cli.md`

Skill version: 1.0.0. This is a standalone, nonofficial QCET internal-workflow proposal, not a school-issued procedure.
