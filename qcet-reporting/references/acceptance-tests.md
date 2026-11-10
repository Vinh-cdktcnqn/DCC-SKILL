# Acceptance matrix and human review

| Requirement | Check |
|---|---|
| Period | 11/2026 normalizes to 2026-10-25..2026-11-24 inclusive; explicit exception is labeled. |
| Completeness | All four operational VTVL groups plus MANAGEMENT have an evidence status or clearly stated gap. |
| Traceability | Every confirmed result and KPI has identified verified source evidence with page/row/log location. |
| Plan comparison | Stable IDs link approved planned work to evidence; unmatched records are separated. |
| Counts | Tasks, activities, deliverables and reports are never conflated; unique IDs prevent duplicate output claims. |
| Staff vs Center | Individual contributions do not double-count Center totals. |
| Metrics | No summing snapshots, percentages or overlapping distinct people; denominator documented. |
| Source conflicts | Contradictions remain visible with source/date and an owner for reconciliation when available. |
| Status | `DRAFT`, not `approved`; user reviews content and authorizes changes. |
| Privacy | No private student lists, credentials or sensitive account data unnecessarily exported. |
| Next actions | Each management action has either a sourced owner/deadline or an explicit open question. |
| Exports | Local scripts are read-only; publication and edits need explicit authorization. |

Offline smoke tests:

```text
python scripts/periods.py --month 2026-11
python scripts/validate_report.py examples/report-2026-11.synthetic.json
python scripts/draft_report.py examples/report-2026-11.synthetic.json
python -m unittest discover -s tests -v
```

Manual review questions: Do report numbers cover exactly this period? Are approvals real? Does each source allow a reviewer to reopen it? Have previous-year stats been accidentally reused? Is a staff attendance dashboard misclassified as student attendance? Have IT and digital learning support disappeared behind admissions promotion? Do data gaps remain explicit?
