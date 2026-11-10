#!/usr/bin/env python3
"""Render a conservative markdown skeleton from verified QCET JSON; stdout only."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

from validate_report import WORKSTREAMS, evidence_is_confirmed, validate

DISPLAY = {
    "MANAGEMENT": "Management / Director / Deputy Director",
    "IT_DX": "IT and digital transformation",
    "COMMUNICATIONS": "Communications",
    "STATISTICS": "Statistics and dashboards",
    "EDU_SUPPORT": "Education and library support",
}


def safe(value: Any, empty: str = "UNCONFIRMED") -> str:
    text = str(value).strip() if value is not None else ""
    return text.replace("|", "/").replace("\n", " ") if text else empty


def refs(ids: Any, evidence: dict) -> str:
    if not ids:
        return "none"
    return "; ".join(f"{x} ({safe(evidence.get(x, {}).get('source_id'))}: {safe(evidence.get(x, {}).get('locator'))})" for x in ids)


def format_number(value: Any) -> str:
    if value is None:
        return "NO DATA"
    if isinstance(value, float):
        return f"{value:,.2f}".rstrip("0").rstrip(".")
    return str(value)


def render(data: dict) -> str:
    errors, warnings = validate(data)
    if errors:
        raise ValueError("Invalid input: " + "; ".join(errors))
    period = data["period"]
    sources = {s["id"]: s for s in data["sources"]}
    evidence = {e["id"]: e for e in data["evidence"]}
    plan = {p["task_id"]: p for p in data["plan"]}
    confirmed = [r for r in data["results"] if r["status"] == "completed" and evidence_is_confirmed(r["evidence_ids"], evidence, sources)]
    unconfirmed = [r for r in data["results"] if r["status"] == "completed" and r not in confirmed]
    active = [r for r in data["results"] if r["status"] != "completed"]
    verified_metrics = [m for m in data["metrics"] if m["value"] is not None and evidence_is_confirmed(m["evidence_ids"], evidence, sources)]
    other_metrics = [m for m in data["metrics"] if m not in verified_metrics]
    lines = [
        f"# {safe(data['organization'])} - report draft ({safe(period['label'])})",
        "",
        "**DRAFT - NOT APPROVED. The input marks evidence verified, but this script does not authenticate any external sources.**",
        *( ["**SYNTHETIC FIXTURE: NEVER SUBMIT AS QCET RESULTS.**"] if str(data.get("report_id", "")).startswith("SYNTHETIC-") else [] ),
        f"**Period:** {period['start']} to {period['end']} (inclusive); **data cutoff:** {period['data_cutoff']}",
        "",
        "## 1. Scope and evidence-marked performance",
        "",
        f"Evidence-marked completed result records: **{len(confirmed)}**. This is a count of result records, not the number of duties, unique tasks, deliverables, staff hours or reports.",
        "",
    ]
    for stream in ["MANAGEMENT", "IT_DX", "COMMUNICATIONS", "STATISTICS", "EDU_SUPPORT"]:
        lines += [f"### {DISPLAY[stream]}", ""]
        records = [r for r in confirmed if r["workstream"] == stream]
        if records:
            for r in records:
                outs = ", ".join(f"{safe(d['name'])} ({format_number(d.get('quantity'))} {safe(d.get('unit'))})" for d in r["deliverables"]) or "No specified output"
                lines.append(f"- {safe(r['summary'])} | task {safe(r.get('task_id'))} | owner {safe(r.get('owner'))}; output: {outs}; evidence: {refs(r.get('evidence_ids'), evidence)}")
        else:
            lines.append("- No verified completed result in this reporting input (not equivalent to no work performed).")
        lines.append("")
    lines += ["## 2. Metrics marked verified in supplied data", "", "| Metric | Value | Unit | Definition | Evidence |", "|---|---:|---|---|---|"]
    if verified_metrics:
        for m in verified_metrics:
            lines.append(f"| {safe(m['label'])} | {format_number(m['value'])} | {safe(m['unit'])} | {safe(m['definition'])} | {refs(m['evidence_ids'], evidence)} |")
    else:
        lines.append("| No verified KPI | - | - | - | - |")
    lines += ["", "## 3. Plan-versus-actual reconciliation", "", "| Planned task | Workstream | Result link | Status | Evidence |", "|---|---|---|---|---|"]
    for p in data["plan"]:
        matches = [r for r in data["results"] if r.get("task_id") == p["task_id"]]
        if not matches:
            lines.append(f"| {safe(p['task_id'])}: {safe(p['description'])} | {safe(p['workstream'])} | No linked record | UNKNOWN, not assumed failed | - |")
        else:
            for r in matches:
                state = r["status"]
                if state == "completed" and not evidence_is_confirmed(r["evidence_ids"], evidence, sources):
                    state = "completed CLAIM - UNVERIFIED"
                lines.append(f"| {safe(p['task_id'])}: {safe(p['description'])} | {safe(p['workstream'])} | {safe(r['id'])} | {safe(state)} | {refs(r['evidence_ids'], evidence)} |")
    lines += ["", "## 4. Extra-plan items and work in progress", ""]
    extra = [r for r in data["results"] if not r.get("task_id") or r.get("task_id") not in plan]
    for r in extra + [r for r in active if r not in extra]:
        lines.append(f"- {safe(r['summary'])}; status {safe(r['status'])}; owner {safe(r['owner'])}; evidence {refs(r.get('evidence_ids'), evidence)}")
    if not extra and not active:
        lines.append("- No extra-plan or in-progress items reported.")
    lines += ["", "## 5. Issues requiring coordination / decision", ""]
    if not data["issues"]:
        lines.append("- None supplied; no claim that all issues are resolved.")
    for issue in data["issues"]:
        lines.append(f"- {safe(issue['description'])}; owner {safe(issue.get('owner'))}; decision {safe(issue.get('requested_decision'))}; target {safe(issue.get('due_date'))}")
    lines += ["", "## 6. Next period actions", ""]
    if not data["next_actions"]:
        lines.append("- Not provided.")
    for action in data["next_actions"]:
        lines.append(f"- {safe(action['description'])}; owner {safe(action.get('owner'))}; due {safe(action.get('due_date'))}; source {safe(action.get('source_id'))}")
    lines += ["", "## 7. Pending verification and data gaps", ""]
    for r in unconfirmed:
        lines.append(f"- Claimed complete, unverified: {safe(r['summary'])} ({safe(r['id'])}).")
    for m in other_metrics:
        lines.append(f"- Unverified or missing metric: {safe(m['label'])} ({safe(m['id'])}); value {format_number(m['value'])}.")
    for q in data["open_questions"]:
        lines.append(f"- {safe(q)}")
    for w in warnings:
        lines.append(f"- Validation warning: {w}")
    if not unconfirmed and not other_metrics and not data["open_questions"] and not warnings:
        lines.append("- No data gaps identified by the structural checker; human source review is still required.")
    lines += ["", "## 8. Source register", "", "| ID | Title | State | Location |", "|---|---|---|---|"]
    for s in data["sources"]:
        lines.append(f"| {safe(s['id'])} | {safe(s['title'])} | {safe(s['state'])} | {safe(s['reference'])} |")
    lines += ["", "**END OF NON-PUBLISHED DRAFT. Human source verification and approval required.**", ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Print conservative QCET Markdown report to stdout (read-only)")
    parser.add_argument("input", help="JSON report file")
    args = parser.parse_args(argv)
    try:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"INVALID JSON: {exc}", file=sys.stderr)
        return 2
    try:
        print(render(data))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
