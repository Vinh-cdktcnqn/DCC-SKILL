#!/usr/bin/env python3
"""Offline, read-only structural validation of QCET Work Planning JSON. Exit 0 = no ERROR, 2 = invalid plan."""
import argparse
from collections import Counter, defaultdict
from datetime import date, timedelta
import json
from pathlib import Path
import sys

from periods import month_bounds

GROUPS = {"MANAGEMENT", "IT_DX", "COMMUNICATIONS", "STATISTICS", "EDU_SUPPORT"}
LEVELS = ("year", "month", "week", "day")
TASK_STATES = {"planned", "in_progress", "blocked", "done", "canceled"}
PLAN_STATES = {"draft", "reviewed", "approved", "archived"}


def check_plan(data):
    errors, warnings = [], []

    def err(code, msg):
        errors.append({"code": code, "message": msg})

    def warn(code, msg):
        warnings.append({"code": code, "message": msg})

    if not isinstance(data, dict):
        return [{"code": "ROOT", "message": "Expected an object"}], []
    if data.get("schema_version") != "1.0":
        err("SCHEMA", "schema_version must be 1.0")
    if data.get("status") not in PLAN_STATES:
        err("PLAN_STATUS", "Invalid status")
    if data.get("status") == "approved":
        warn("AUTHORITY", "approved must be evidenced by a real human decision; validator cannot verify it")

    starts = ends = None
    try:
        starts, ends = date.fromisoformat(data["period_start"]), date.fromisoformat(data["period_end"])
        if ends < starts:
            err("PERIOD", "period_end precedes period_start")
    except (ValueError, TypeError, KeyError):
        err("PERIOD", "period_start/period_end must be ISO dates")

    label = data.get("period_label")
    if label is not None:
        try:
            expected_start, expected_end = month_bounds(label)
            if (starts, ends) != (expected_start, expected_end):
                err("MONTH_25_24", f"{label} must be {expected_start} to {expected_end}")
        except ValueError:
            err("MONTH_LABEL", "period_label must be YYYY-MM")

    sources = data.get("source_register", [])
    if not isinstance(sources, list):
        err("SOURCE_REGISTER", "source_register must be a list")
        sources = []
    ref_ids = [s.get("ref") for s in sources if isinstance(s, dict)]
    if len(ref_ids) != len(set(ref_ids)):
        err("SOURCE_DUP", "Duplicate source reference")
    valid_refs = set(ref_ids)
    duties = data.get("duties", [])
    if not isinstance(duties, list):
        err("DUTIES", "duties must be a list")
        duties = []
    duty_map = {}
    for d in duties:
        if not isinstance(d, dict) or not d.get("id"):
            err("DUTY", "A duty must have id")
            continue
        if d["id"] in duty_map:
            err("DUTY_DUP", f"Duplicate duty {d['id']}")
        duty_map[d["id"]] = d
        if d.get("position_group") not in GROUPS:
            err("DUTY_GROUP", f"Invalid group for {d['id']}")
        if d.get("source_ref") not in valid_refs:
            err("DUTY_SOURCE", f"Unknown source for {d['id']}")

    tasks = data.get("tasks", [])
    if not isinstance(tasks, list):
        return errors + [{"code": "TASKS", "message": "tasks must be a list"}], warnings
    task_map = {}
    for task in tasks:
        if not isinstance(task, dict) or not isinstance(task.get("id"), str) or not task["id"]:
            err("TASK", "Each task needs a non-empty string id")
            continue
        tid = task["id"]
        if tid in task_map:
            err("TASK_DUP", f"Duplicate task id {tid}")
        task_map[tid] = task
    groups_in_month = set()
    hours_by_owner = defaultdict(float)

    for tid, task in task_map.items():
        level = task.get("level")
        group = task.get("position_group")
        if level not in LEVELS:
            err("LEVEL", f"{tid}: invalid level")
            continue
        if group not in GROUPS:
            err("GROUP", f"{tid}: invalid group")
        if level == "month":
            groups_in_month.add(group)
        if task.get("duty_id") not in duty_map:
            err("DUTY_REF", f"{tid}: unknown duty_id")
        elif group != duty_map[task["duty_id"]].get("position_group"):
            err("DUTY_GROUP_MISMATCH", f"{tid}: group differs from duty catalog")
        if task.get("source_ref") not in valid_refs:
            err("SOURCE_REF", f"{tid}: unknown source_ref")
        if not isinstance(task.get("title"), str) or not task["title"].strip():
            err("TITLE", f"{tid}: missing task title")
        if not isinstance(task.get("deliverable"), str) or not task["deliverable"].strip():
            err("DELIVERABLE", f"{tid}: missing deliverable")
        if not isinstance(task.get("acceptance_criteria"), str) or not task["acceptance_criteria"].strip():
            err("ACCEPTANCE", f"{tid}: missing acceptance criteria")
        if not task.get("owner"):
            warn("OWNER_UNCONFIRMED", f"{tid}: owner not confirmed")
        if task.get("status") not in TASK_STATES:
            err("TASK_STATUS", f"{tid}: invalid status")
        if task.get("status") == "done" and not task.get("evidence_ref"):
            err("EVIDENCE", f"{tid}: done without evidence_ref")
        try:
            begin, finish = date.fromisoformat(task["start"]), date.fromisoformat(task["end"])
            if finish < begin:
                err("DATE_ORDER", f"{tid}: end before start")
            if starts and ends and (begin < starts or finish > ends):
                err("PERIOD_OUTSIDE", f"{tid}: outside plan period")
        except (ValueError, TypeError, KeyError):
            err("DATE", f"{tid}: invalid start/end")
            continue
        parent_id = task.get("parent_id")
        if parent_id is not None:
            parent = task_map.get(parent_id)
            if not parent:
                err("PARENT", f"{tid}: missing parent {parent_id}")
            elif parent.get("level") in LEVELS:
                if LEVELS.index(level) != LEVELS.index(parent["level"]) + 1:
                    err("PARENT_LEVEL", f"{tid}: {parent['level']} cannot contain {level}")
                try:
                    pstart, pend = date.fromisoformat(parent["start"]), date.fromisoformat(parent["end"])
                    if begin < pstart or finish > pend:
                        err("CHILD_OUTSIDE", f"{tid}: outside its parent")
                except (TypeError, KeyError, ValueError):
                    pass
                if (group != parent.get("position_group") or task.get("duty_id") != parent.get("duty_id")):
                    err("PARENT_SCOPE", f"{tid}: duty/group mismatch with parent")
        elif level not in ("year", "month"):
            err("ORPHAN", f"{tid}: {level} needs parent")
        if level == "week":
            if starts is not None and ends is not None:
                expected_begin = max(starts, begin - timedelta(days=begin.weekday()))
                expected_finish = min(ends, finish + timedelta(days=6 - finish.weekday()))
                if begin != expected_begin or finish != expected_finish:
                    err("WEEK_BOUNDS", f"{tid}: must use Monday-Sunday intersection with month")
        if level == "day" and begin != finish:
            err("DAY_BOUNDS", f"{tid}: day must start and end on same date")
        for field in ("hours_planned", "hours_actual"):
            val = task.get(field)
            if val is not None:
                if level != "day":
                    err("HOURS_LEVEL", f"{tid}: {field} allowed only for day")
                if isinstance(val, bool) or not isinstance(val, (int, float)) or val < 0:
                    err("HOURS_VALUE", f"{tid}: {field} must be a nonnegative number or null")
        if level == "day" and task.get("owner") and isinstance(task.get("hours_planned"), (int, float)) and not isinstance(task.get("hours_planned"), bool):
            hours_by_owner[task["owner"]] += task["hours_planned"]
            if task["hours_planned"] > 8:
                warn("DAY_OVER_8H", f"{tid}: planned >8h; verify schedule or overtime")

    if label is not None:
        for group in sorted(GROUPS - groups_in_month):
            warn("COVERAGE", f"Monthly plan missing group {group}; justify or include real work")
    for target in data.get("capacity_targets", []):
        if not isinstance(target, dict):
            err("CAPACITY", "capacity_targets entry must be object")
            continue
        owner = target.get("owner")
        planned = target.get("target_hours")
        if not owner or isinstance(planned, bool) or not isinstance(planned, (int, float)) or planned < 0:
            err("CAPACITY", "capacity target requires owner and nonnegative target_hours")
            continue
        if target.get("source_ref") not in valid_refs:
            err("CAPACITY_SOURCE", f"Capacity target for {owner} has no valid source")
        if label is not None:
            warn("CAPACITY_MONTH", f"{owner}: do not compare one month against annual capacity {planned}")
        else:
            diff = planned - hours_by_owner.get(owner, 0)
            if abs(diff) > 0.01:
                warn("CAPACITY_GAP", f"{owner}: {diff:+.2f} hours short of target (negative means over); never auto-fill")
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description="Validate QCET plan JSON (read-only)")
    parser.add_argument("file", help="Path to existing UTF-8 JSON file")
    args = parser.parse_args()
    try:
        data = json.loads(Path(args.file).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "errors": [{"code": "READ", "message": str(exc)}], "warnings": []}, ensure_ascii=False))
        return 2
    errors, warnings = check_plan(data)
    print(json.dumps({"ok": not errors, "errors": errors, "warnings": warnings,
                      "summary": {"error_count": len(errors), "warning_count": len(warnings), "task_count": len(data.get("tasks", [])) if isinstance(data, dict) and isinstance(data.get("tasks", []), list) else None}}, ensure_ascii=False, indent=2))
    return 2 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
