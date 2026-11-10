#!/usr/bin/env python3
"""Offline structural and provenance checks for QCET report JSON. Never writes files."""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

from periods import month_bounds

WORKSTREAMS = {"MANAGEMENT", "IT_DX", "COMMUNICATIONS", "STATISTICS", "EDU_SUPPORT"}
REPORT_TYPES = {"monthly", "quarterly", "school_year", "annual_evaluation", "leadership_brief", "ad_hoc"}
RESULT_STATUS = {"completed", "in_progress", "blocked", "not_started", "cancelled"}
AGGREGATIONS = {"sum", "distinct_count", "last_value", "ratio", "not_additive"}
SOURCE_STATES = {"approved", "draft", "operational_record"}
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MONTH_PATTERN = re.compile(r"^\d{4}-\d{2}$")


def parse_date(value: Any, path: str, errors: list[str], nullable: bool = False) -> date | None:
    if value is None and nullable:
        return None
    if not isinstance(value, str) or not DATE_PATTERN.fullmatch(value):
        errors.append(f"{path}: expected YYYY-MM-DD")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"{path}: invalid calendar date {value!r}")
        return None


def required_str(item: dict, key: str, path: str, errors: list[str]) -> str | None:
    val = item.get(key)
    if not isinstance(val, str) or not val.strip():
        errors.append(f"{path}.{key}: nonempty string required")
        return None
    return val


def objects(value: Any, path: str, errors: list[str]) -> list[dict]:
    if not isinstance(value, list):
        errors.append(f"{path}: must be an array")
        return []
    out = []
    for i, element in enumerate(value):
        if not isinstance(element, dict):
            errors.append(f"{path}[{i}]: must be an object")
        else:
            out.append(element)
    return out


def unique_ids(items: list[dict], group: str, errors: list[str]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for i, item in enumerate(items):
        key = "task_id" if group == "plan" else "id"
        ident = required_str(item, key, f"{group}[{i}]", errors)
        if ident is None:
            continue
        if ident in out:
            errors.append(f"{group}: duplicate {key} {ident!r}")
        out[ident] = item
    return out


def number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def check_workstream(item: dict, path: str, errors: list[str]) -> None:
    if item.get("workstream") not in WORKSTREAMS:
        errors.append(f"{path}.workstream: unknown workstream {item.get('workstream')!r}")


def check_evidence_links(refs: Any, path: str, evidence: dict, errors: list[str]) -> list[str]:
    if not isinstance(refs, list) or any(not isinstance(s, str) for s in refs):
        errors.append(f"{path}.evidence_ids: expected string array")
        return []
    if len(set(refs)) != len(refs):
        errors.append(f"{path}.evidence_ids: duplicate references")
    for ref in refs:
        if ref not in evidence:
            errors.append(f"{path}.evidence_ids: unknown evidence {ref!r}")
    return refs


def evidence_is_confirmed(ids: Any, evidence: dict, sources: dict) -> bool:
    return isinstance(ids, list) and len(ids) > 0 and all(
        isinstance(s, str) and s in evidence and
        evidence[s].get("verification") == "verified" and
        sources.get(evidence[s].get("source_id"), {}).get("state") in {"approved", "operational_record"} and
        bool(str(evidence[s].get("locator") or "").strip())
        for s in ids
    )


def validate(data: Any) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(data, dict):
        return ["root: expected JSON object"], warnings
    if data.get("schema_version") != "1.0":
        errors.append("schema_version: expected '1.0'")
    required_str(data, "report_id", "root", errors)
    required_str(data, "organization", "root", errors)
    kind = data.get("report_type")
    if kind not in REPORT_TYPES:
        errors.append(f"report_type: expected one of {sorted(REPORT_TYPES)}")
    if data.get("status") != "draft":
        errors.append("status: skill output/input must be 'draft'; approval is external")

    period = data.get("period")
    if not isinstance(period, dict):
        errors.append("period: object required")
        period = {}
    required_str(period, "label", "period", errors)
    start = parse_date(period.get("start"), "period.start", errors)
    end = parse_date(period.get("end"), "period.end", errors)
    cutoff = parse_date(period.get("data_cutoff"), "period.data_cutoff", errors)
    if start and end and start > end:
        errors.append("period: start must not exceed end")
    if start and end and cutoff and not start <= cutoff <= end:
        errors.append("period.data_cutoff: must fall inside reporting window")
    if kind == "monthly":
        label = period.get("month")
        if not isinstance(label, str) or not MONTH_PATTERN.fullmatch(label):
            errors.append("period.month: monthly report requires YYYY-MM")
        else:
            try:
                expected_start, expected_end = month_bounds(label)
                if (start and end) and (start != expected_start or end != expected_end):
                    reason = period.get("exception_reason")
                    if not isinstance(reason, str) or not reason.strip():
                        errors.append("period: monthly dates differ from 25-24; exception_reason required")
                    else:
                        warnings.append("period: nonstandard monthly range; confirm official exception authority")
            except ValueError as exc:
                errors.append(f"period.month: {exc}")
    elif period.get("month") is not None:
        warnings.append("period.month: ignored for non-monthly report; dates must come from instructions")

    source_items = objects(data.get("sources"), "sources", errors)
    sources = unique_ids(source_items, "sources", errors)
    for i, src in enumerate(source_items):
        path = f"sources[{i}]"
        required_str(src, "title", path, errors)
        required_str(src, "reference", path, errors)
        if src.get("state") not in SOURCE_STATES:
            errors.append(f"{path}.state: unknown state")
        parse_date(src.get("date"), f"{path}.date", errors, nullable=True)

    evidence_items = objects(data.get("evidence"), "evidence", errors)
    evidence = unique_ids(evidence_items, "evidence", errors)
    for i, ev in enumerate(evidence_items):
        path = f"evidence[{i}]"
        if ev.get("source_id") not in sources:
            errors.append(f"{path}.source_id: unknown source {ev.get('source_id')!r}")
        if ev.get("verification") not in {"verified", "pending"}:
            errors.append(f"{path}.verification: must be verified or pending")
        if not isinstance(ev.get("locator"), str) or not ev["locator"].strip():
            warnings.append(f"{path}.locator: missing exact page, row or record")
        if ev.get("verification") == "verified" and sources.get(ev.get("source_id"), {}).get("state") == "draft":
            warnings.append(f"{path}: verified flag cannot establish authority from a draft-only source")

    plan_items = objects(data.get("plan"), "plan", errors)
    plan = unique_ids(plan_items, "plan", errors)
    for i, item in enumerate(plan_items):
        path = f"plan[{i}]"
        check_workstream(item, path, errors)
        required_str(item, "description", path, errors)
        if item.get("owner") is None:
            warnings.append(f"{path}.owner: missing assigned person")
        if item.get("source_id") not in sources:
            errors.append(f"{path}.source_id: unknown source")
        due = parse_date(item.get("due_date"), f"{path}.due_date", errors, nullable=True)
        if end and due and due > end:
            warnings.append(f"{path}.due_date: beyond reporting period")

    result_items = objects(data.get("results"), "results", errors)
    results = unique_ids(result_items, "results", errors)
    deliverables = {}
    plan_results = set()
    for i, result in enumerate(result_items):
        path = f"results[{i}]"
        check_workstream(result, path, errors)
        required_str(result, "summary", path, errors)
        if result.get("status") not in RESULT_STATUS:
            errors.append(f"{path}.status: unknown status")
        when = parse_date(result.get("activity_date"), f"{path}.activity_date", errors, nullable=True)
        if start and end and when and not start <= when <= end:
            warnings.append(f"{path}.activity_date: outside reporting period")
        if cutoff and when and when > cutoff:
            warnings.append(f"{path}.activity_date: after data cutoff")
        task_id = result.get("task_id")
        if task_id is not None:
            if not isinstance(task_id, str) or not task_id:
                errors.append(f"{path}.task_id: must be nonempty string or null")
            elif task_id not in plan:
                warnings.append(f"{path}.task_id: no matching approved plan task ({task_id})")
            else:
                plan_results.add(task_id)
                if result.get("workstream") != plan[task_id].get("workstream"):
                    warnings.append(f"{path}.workstream: disagrees with plan task {task_id}")
        else:
            warnings.append(f"{path}: result outside registered plan; classify as extra-plan")
        if result.get("owner") is None:
            warnings.append(f"{path}.owner: unknown person")
        refs = check_evidence_links(result.get("evidence_ids"), path, evidence, errors)
        outs = objects(result.get("deliverables"), f"{path}.deliverables", errors)
        for j, output in enumerate(outs):
            opath = f"{path}.deliverables[{j}]"
            out_id = required_str(output, "id", opath, errors)
            required_str(output, "name", opath, errors)
            if out_id is not None:
                if out_id in deliverables:
                    errors.append(f"deliverables: duplicate id {out_id!r} across records")
                deliverables[out_id] = output
            qty = output.get("quantity")
            if qty is not None and (not number(qty) or qty < 0):
                errors.append(f"{opath}.quantity: must be nonnegative finite number or null")
            required_str(output, "unit", opath, errors)
        if result.get("status") == "completed" and not evidence_is_confirmed(refs, evidence, sources):
            warnings.append(f"{path}: completed result is NOT confirmed by verified authorized evidence")
        if result.get("status") == "completed" and not outs:
            warnings.append(f"{path}: completed result has no specified deliverable")
    for task_id in plan:
        if task_id not in plan_results:
            warnings.append(f"plan task {task_id}: no linked result (NOT evidence of non-performance)")

    metrics_items = objects(data.get("metrics"), "metrics", errors)
    unique_ids(metrics_items, "metrics", errors)
    for i, metric in enumerate(metrics_items):
        path = f"metrics[{i}]"
        check_workstream(metric, path, errors)
        required_str(metric, "label", path, errors)
        required_str(metric, "unit", path, errors)
        required_str(metric, "definition", path, errors)
        agg = metric.get("aggregation")
        if agg not in AGGREGATIONS:
            errors.append(f"{path}.aggregation: unknown aggregation")
        refs = check_evidence_links(metric.get("evidence_ids"), path, evidence, errors)
        value = metric.get("value")
        if value is not None and (not number(value) or value < 0):
            errors.append(f"{path}.value: expected nonnegative finite number or null")
        if value is None:
            warnings.append(f"{path}.value: no reported observation; do not replace with zero")
        if agg == "ratio":
            n, d = metric.get("numerator"), metric.get("denominator")
            if not number(n) or not number(d) or n < 0 or d <= 0:
                errors.append(f"{path}: ratio requires numerator >=0 and denominator >0")
            elif number(value) and abs(value - (n / d * 100)) > 0.1:
                errors.append(f"{path}.value: not equal to numerator/denominator * 100")
        elif metric.get("numerator") is not None or metric.get("denominator") is not None:
            warnings.append(f"{path}: numerator/denominator ignored unless aggregation is ratio")
        if agg == "distinct_count" and not metric.get("dedup_keys"):
            warnings.append(f"{path}: distinct_count requires a documented deduplication key for aggregation")
        if not evidence_is_confirmed(refs, evidence, sources):
            warnings.append(f"{path}: metric is not supported by fully verified authorized evidence")

    issue_items = objects(data.get("issues"), "issues", errors)
    unique_ids(issue_items, "issues", errors)
    for i, issue in enumerate(issue_items):
        path = f"issues[{i}]"
        required_str(issue, "description", path, errors)
        tid = issue.get("related_task_id")
        if tid is not None and tid not in plan:
            warnings.append(f"{path}.related_task_id: unknown plan task")
        parse_date(issue.get("due_date"), f"{path}.due_date", errors, nullable=True)
    actions = objects(data.get("next_actions"), "next_actions", errors)
    for i, action in enumerate(actions):
        path = f"next_actions[{i}]"
        required_str(action, "description", path, errors)
        if action.get("source_id") not in sources:
            errors.append(f"{path}.source_id: unknown source")
        parse_date(action.get("due_date"), f"{path}.due_date", errors, nullable=True)
    qs = data.get("open_questions")
    if not isinstance(qs, list) or any(not isinstance(q, str) for q in qs):
        errors.append("open_questions: expected array of strings")

    covered = {x.get("workstream") for x in (plan_items + result_items + metrics_items)}
    for workstream in sorted(WORKSTREAMS - covered):
        warnings.append(f"coverage: workstream {workstream} has no data; mark the gap explicitly")
    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate QCET reporting data (read-only)")
    parser.add_argument("input", help="JSON file to inspect")
    args = parser.parse_args(argv)
    try:
        content = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as exc:
        print(f"Cannot read {args.input}: {exc}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"INVALID JSON: {exc}")
        return 2
    errors, warnings = validate(content)
    for err in errors:
        print("ERROR: " + err)
    for warn in warnings:
        print("WARNING: " + warn)
    print(f"QCET_REPORT_CHECK errors={len(errors)} warnings={len(warnings)}")
    return 2 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
