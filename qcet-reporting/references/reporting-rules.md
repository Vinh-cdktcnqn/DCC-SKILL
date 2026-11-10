# Operational reporting rules

## Cadences

| Mode | Interval rule | Required view |
|---|---|---|
| Monthly | Month M = 25 of M-1 to 24 of M, inclusive, unless governing template overrides | Planned versus completed; 5 workstreams; evidence, risks and next period |
| Quarterly | Use period from the official reporting calendar or order; never guess quarter boundaries | De-duplicated multi-month totals plus trend and decisions |
| School year | Require approved year bounds and scope | Full-period performance, core functions, outcomes, evidence and next-year improvement |
| Annual personnel/collective evaluation | Use form and year prescribed by official instruction, which may differ from school year | Individual versus collective outputs; source-backed strengths and realistic improvements |
| Leadership brief | Meeting purpose and cutoff explicitly stated | 3-6 verified key points; 1-3 management decisions sought |
| Ad hoc | Use directive's dates | Specific question answered by dated evidence |

Monthly 11/2026 = 2026-10-25 through 2026-11-24. A report due later does not extend its result window. A November 2026 briefing covering October work may use a completely different window if the school's directive says so; retain the directive's period.

## Core workflow

1. Lock the report period and cutoff, including a source for any calendar exception.
2. List incoming approved tasks (from a plan, directive or authorized assignment), separated from recurring functions.
3. Collect outcomes from source documents and logs; classify completed, in progress, blocked, cancelled, unknown.
4. Compare planned tasks with outcomes and evidence. Use distinct IDs and avoid collapsing tasks by matching titles alone.
5. Group by MANAGEMENT, IT_DX, COMMUNICATIONS, STATISTICS, EDU_SUPPORT.
6. Highlight measurable outcomes, significant extra-plan activities, pending work, bottlenecks and management decisions.
7. Check conclusions against every evidence record; explicitly identify all important unknowns.

## Three distinct quantities

- A duty is an ongoing responsibility, often spanning an entire year and many activities.
- An activity/task is a discrete unit of work performed under a duty and may yield several outputs.
- A deliverable is an artifact or service outcome. A monthly report is one deliverable that summarizes numerous management activities, not "12 duties" or "12 management tasks" by virtue of 12 reports.

Do not turn the 1,904-hour planning benchmark mentioned in some VTVL exercises into a factual actual-hours claim. Actual hours require time records or confirmed logs for the reporting period.

## Reporting obligations by workstream

- MANAGEMENT: directives received, planning and coordination, issue escalation, follow-up to Principal, cross-unit management, workload oversight. Separate management report count from management action count.
- IT_DX: infrastructure/network/server, cybersecurity/backups, system support, accounts, digital transformation and AI services. Distinguish incident count from supported-person count, machine count and blocked-IP count.
- COMMUNICATIONS: approved/published articles, scripts, photography, videos, banners, distribution. Separate unique article vs channel post vs share; publishing dates and channels matter.
- STATISTICS: collection/verification, dashboards, source reliability, reporting timeliness; daily timekeeping dashboard is employee/staff attendance for the Principal unless the current official source says otherwise.
- EDU_SUPPORT: library operations, digital learning material collection, staff/faculty support and student learning service. Avoid exposing private reader or student records.

## Interaction with qcet-work-planning

Cross-reference the previous plan through stable `plan.task_id` identifiers. If no usable task IDs exist, produce a mapping table of proposed matches, and label them unconfirmed. Never overwrite plan data when finalizing a report. Reporting is a distinct approval lifecycle.
