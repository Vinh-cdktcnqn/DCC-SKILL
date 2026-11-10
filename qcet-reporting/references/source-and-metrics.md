# Data provenance, reconciliation and metric discipline

## Source register

For each file/site/table record capture `source_id`, exact title, issuer or owner, state (`approved`, `draft`, `operational_record`), document date, available URI or file path, extraction location (page/row/log record) and retrieved-on date. Follow legal access restrictions. A named source with no accessible content is NOT evidence.

Evidence records reference source IDs and a location. An evidence check marked `verified` means a person or properly authorized process checked the underlying content and period; the agent must NOT set it from mere appearance. For report claims, treat verified evidence linked to a draft-only source as provisional. If conflicting counts occur, show each with attribution, then list a reconciliation action.

## Numeric rules

1. Define metric, unit, exact counting universe, inclusive date bounds, overlap rule and provenance before calculating.
2. `sum`: allowed only for nonoverlapping additive observations with the same unit and method (e.g. separate completed events).
3. `distinct_count`: needs stable deduplication keys; never sum staff-level distinct-user totals as Center distinct users without dedup keys.
4. `last_value`: a point-in-time snapshot (e.g. active accounts, storage consumption, number of cameras); do not add monthly snapshots.
5. `ratio`: numerator and denominator must be present, denominator > 0, same scope and compatible periods; report percentage = numerator / denominator * 100. Do not average separate percentages without valid weights.
6. `not_additive`: publish as an explicitly described observation; no total.
7. Missing and zero are different. `0` requires an explicit verified observation; missing numbers are null and must not be displayed as zero.
8. If data collected after the reporting cutoff describes an earlier event, mark source date and event date separately. A cumulative figure from last year is not current-year results.
9. Avoid double counting source outputs shared by teams or channels. Use unique deliverable IDs and separate overall total from workstream subcounts.
10. Avoid unsupported comparative adjectives (increased, improved, safe, fully achieved) without a verified baseline, agreed target or documented incident-free period.

## Decision rule for a numeric claim

- Data + period + unit + verified and traceable source: report as observed, citing source.
- Data but verification pending: include only as a preliminary observation in a labeled pending-data section.
- Conflicting data: do not pick a winner without a documented reconciliation step.
- No source/definition/period: omit the numeric claim from the main results and list required evidence.

## Staff contributions versus Center totals

Individual contributions can support the Center's achievement narrative. The Center total must be computed from deduplicated events/IDs, not by blindly adding attributed individual reports. Work done by multiple staff is one Center product unless the recording standard says otherwise.

## Report integrity

End with a traceability ledger: claim or metric -> exact source -> period -> verification -> status. Surface coverage gaps for every workstream. Mark review state as `DRAFT`; only authorized users may change approval status.
