"""
Lab Exercise 11 : Log File Reader Program
Reads a log file, counts ERROR / WARNING / INFO entries and summarises them.
Usage : python log_analyzer.py [path_to_log]      |  python log_analyzer.py --test
"""
import os
import re
import sys
import tempfile
from collections import Counter

LEVELS = ("ERROR", "WARNING", "INFO")
# \b = word boundary, so "ERRORS" or "INFORMATION" are NOT mis-counted
LEVEL_PATTERN = re.compile(r"\b(ERROR|WARNING|INFO)\b", re.IGNORECASE)


def analyze_log(path):
    """Scan the log once; return (counts, flagged_lines, total_lines, unclassified)."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Log file not found: {path}")
    if os.path.getsize(path) == 0:
        raise ValueError(f"Log file is empty: {path}")

    counts = Counter({level: 0 for level in LEVELS})
    flagged = {"ERROR": [], "WARNING": []}
    total = unclassified = 0

    with open(path, "r", encoding="utf-8", errors="replace") as log:
        for number, line in enumerate(log, start=1):
            line = line.strip()
            if not line:                      # ignore blank lines
                continue
            total += 1
            match = LEVEL_PATTERN.search(line)  # first keyword decides the level
            if match is None:
                unclassified += 1
                continue
            level = match.group(1).upper()
            counts[level] += 1
            if level in flagged:
                flagged[level].append((number, line))

    if total == 0:
        raise ValueError(f"Log file contains only blank lines: {path}")
    return counts, flagged, total, unclassified


def top_repeated_errors(error_lines, n=3):
    """Group identical error messages (timestamp removed) to spot recurring faults."""
    messages = Counter()
    for _, line in error_lines:
        text = re.split(r"\bERROR\b", line, maxsplit=1, flags=re.IGNORECASE)[-1]
        messages[text.strip(" :-")] += 1
    return messages.most_common(n)


def print_report(path, counts, flagged, total, unclassified):
    print("=" * 62)
    print(f" LOG ANALYSIS REPORT  -  {os.path.basename(path)}")
    print("=" * 62)
    print(f" Total log entries : {total}")
    print("-" * 62)
    print(f" {'LEVEL':<10}{'COUNT':>7}{'SHARE':>9}   GRAPH")
    for level in LEVELS:
        share = counts[level] * 100 / total
        bar = "#" * round(share / 4)
        print(f" {level:<10}{counts[level]:>7}{share:>8.1f}%   {bar}")
    if unclassified:
        print(f" {'OTHER':<10}{unclassified:>7}{unclassified*100/total:>8.1f}%")
    print("-" * 62)

    if flagged["ERROR"]:
        print(" ERROR lines (line no : message)")
        for number, line in flagged["ERROR"]:
            print(f"   [{number:>3}] {line}")
        print(" Most frequent errors:")
        for message, times in top_repeated_errors(flagged["ERROR"]):
            print(f"   {times} x {message}")
    ratio = counts["ERROR"] * 100 / total
    status = "CRITICAL - investigate now" if ratio >= 20 else \
             "ATTENTION - review errors" if counts["ERROR"] else "HEALTHY"
    print("-" * 62)
    print(f" System status : {status}  (error ratio {ratio:.1f}%)")
    print("=" * 62)


def run_tests():
    """Verify the counting logic against a log whose answer is known in advance."""
    sample = ("2026-01-01 INFO started\n2026-01-01 ERROR disk full\n\n"
              "2026-01-01 WARNING low memory\n2026-01-01 error: timeout\n"
              "no keyword here\n2026-01-01 INFORMATION only (no keyword)\n")
    with tempfile.TemporaryDirectory() as folder:
        good = os.path.join(folder, "t.log")
        with open(good, "w") as f:
            f.write(sample)
        counts, _, total, other = analyze_log(good)
        assert (counts["ERROR"], counts["WARNING"], counts["INFO"]) == (2, 1, 1)
        assert (total, other) == (6, 2)
        print("TEST 1 passed : counts ERROR=2 WARNING=1 INFO=1, total=6, other=2")

        empty = os.path.join(folder, "e.log")
        open(empty, "w").close()
        try:
            analyze_log(empty)
        except ValueError as err:
            print("TEST 2 passed : empty file ->", err.__class__.__name__)
        try:
            analyze_log(os.path.join(folder, "nope.log"))
        except FileNotFoundError as err:
            print("TEST 3 passed : missing file ->", err.__class__.__name__)

        # independent cross-check using a different method (substring search)
        alt = sum(1 for l in sample.splitlines() if "ERROR" in l.upper()
                  and "INFORMATION" not in l.upper())
        assert alt == counts["ERROR"]
        print("TEST 4 passed : result matches independent cross-check")


def main():
    if "--test" in sys.argv:
        run_tests()
        return
    path = sys.argv[1] if len(sys.argv) > 1 else input("Enter log file path: ").strip()
    try:
        print_report(path, *analyze_log(path))
    except FileNotFoundError as err:
        print("[ERROR]", err)
    except ValueError as err:
        print("[WARNING]", err)
    except PermissionError:
        print("[ERROR] Permission denied while reading", path)


if __name__ == "__main__":
    main()
