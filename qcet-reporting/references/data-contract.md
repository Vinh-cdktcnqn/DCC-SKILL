# JSON report input v1.0

Example: `examples/report-2026-11.synthetic.json`. All person names, numbers and evidence in the example are **synthetic**; nothing is evidence of QCET activity.

Top-level object:

- `schema_version`: "1.0".
- `report_id`: stable nonempty ID.
- `report_type`: `monthly|quarterly|school_year|annual_evaluation|leadership_brief|ad_hoc`.
- `organization`: label of reporting unit.
- `period`: `{label, start, end, data_cutoff, month, exception_reason}`. `month` must be `YYYY-MM` for monthly and null for other report types. If no exception, monthly range is exactly 25 of the prior month through 24 of the stated month. `exception_reason` explicitly justifies overridden official dates; not proof by itself.
- `status`: `draft` only for data processed by this skill. Do not set approval from automated validation.
- `sources`: `[{id,title,state,reference,date}]`, state in `approved|draft|operational_record`; `reference` must be a locator, never an actual secret.
- `evidence`: `[{id,source_id,locator,verification,note}]`, verification `verified|pending`. Evidence `verified` is a claim from the data owner, not a status that scripts establish automatically.
- `plan`: `[{task_id,workstream,description,owner,due_date,source_id}]`. Workstreams `MANAGEMENT|IT_DX|COMMUNICATIONS|STATISTICS|EDU_SUPPORT`; owner may be null.
- `results`: `[{id,task_id,workstream,owner,summary,status,activity_date,evidence_ids,deliverables}]`. `task_id` may be null for extra-plan results. Status `completed|in_progress|blocked|not_started|cancelled`; deliverables `[{id,name,quantity,unit}]`. `quantity` may be null; do not assume missing = zero.
- `metrics`: `[{id,label,workstream,value,unit,aggregation,numerator,denominator,evidence_ids,definition}]`. `aggregation` = `sum|distinct_count|last_value|ratio|not_additive`. Use null numerator/denominator except ratio. `ratio.value` is a percentage 0..100 calculated from numerator and denominator. Null value signifies unknown, not zero.
- `issues`: `[{id,description,related_task_id,owner,requested_decision,due_date}]`.
- `next_actions`: `[{description,owner,due_date,source_id}]`.
- `open_questions`: array of strings.

### Key checks

- Unique IDs for sources, evidence, plan, result, deliverables and metrics; all cross-references must exist.
- Dates are real ISO dates; start <= end; cutoff inside period; activity dates should belong to the window (out-of-period results are WARNINGS, not silently dropped).
- A completed result without traceable, verified evidence is NOT a confirmed achievement. A `draft`-only source does not independently verify completion.
- Distinguish `plan` from `results`, `deliverables`, `metrics`, and the document itself.
- Metric percentages require compatible numerator and denominator, denominator > 0, and math consistency.
- Missing approved source or missing workstream coverage creates a warning; no automatic invented records.

## Script interface

`python scripts/validate_report.py PATH`: prints errors/warnings to stdout; exit code 0 if no errors, 2 on invalid report or malformed JSON, 1 on filesystem/usage error. It is read-only.

`python scripts/draft_report.py PATH`: validates first; prints a conservative Markdown draft to stdout, never to a file; exit code 2 for validation errors. Unverified results/metrics go under a pending-evidence section. If saving a file is desired, obtain user permission to redirect stdout or use an explicitly authorized output tool.

`python scripts/periods.py --month YYYY-MM`: emits the operational period and ISO weeks, read-only.

Scripts use Python 3.9+ and the standard library only. Successful validation does NOT establish that the underlying source data is true.
