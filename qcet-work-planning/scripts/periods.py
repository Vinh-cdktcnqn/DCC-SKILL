#!/usr/bin/env python3
"""Read-only QCET period splitter: month named YYYY-MM runs from 25th previous month through 24th current month."""
import argparse
import calendar
import json
from datetime import date, timedelta


def month_bounds(label: str):
    try:
        year_str, month_str = label.split("-")
        if len(year_str) != 4 or len(month_str) != 2 or not (year_str + month_str).isdigit():
            raise ValueError
        year, month = int(year_str), int(month_str)
        if not 1 <= month <= 12:
            raise ValueError
        end = date(year, month, 24)
        first_year, first_month = (year - 1, 12) if month == 1 else (year, month - 1)
        start = date(first_year, first_month, 25)
        return start, end
    except (ValueError, TypeError) as exc:
        raise ValueError("Month must be a valid YYYY-MM label") from exc


def split_weeks(start: date, end: date):
    if end < start:
        raise ValueError("End date precedes start date")
    out, day = [], start
    while day <= end:
        sunday = day + timedelta(days=6 - day.weekday())
        stop = min(sunday, end)
        out.append({"start": day.isoformat(), "end": stop.isoformat(),
                    "partial": day.weekday() != 0 or stop.weekday() != 6})
        day = stop + timedelta(days=1)
    return out


def build_period(label: str):
    start, end = month_bounds(label)
    return {"period_label": label, "period_start": start.isoformat(),
            "period_end": end.isoformat(), "days": (end-start).days + 1,
            "weeks": split_weeks(start, end)}


def main():
    parser = argparse.ArgumentParser(description="Print QCET 25-24 period and calendar weeks (read-only)")
    parser.add_argument("--month", required=True, help="Named work month YYYY-MM")
    args = parser.parse_args()
    try:
        print(json.dumps(build_period(args.month), indent=2, ensure_ascii=False))
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
