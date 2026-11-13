"""
Lab Exercise 13 : CSV-Based Payroll Management System
Reads employees.csv, computes gross salary and deductions, writes salary_summary.csv.
Usage : python payroll.py [employees.csv]   |   python payroll.py --test
Input columns : emp_id, name, department, designation, basic_salary, bonus (optional)
All amounts are MONTHLY, in Rs.  Rules below are simplified for lab use.
"""
import csv
import os
import sys
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP

# ------------------------------------------------------------ payroll rules
HRA_RATE = Decimal("0.20")        # House Rent Allowance  = 20% of basic
DA_RATE = Decimal("0.10")         # Dearness Allowance    = 10% of basic
TRANSPORT = Decimal("1600")       # fixed transport allowance
PF_RATE = Decimal("0.12")         # Provident Fund        = 12% of basic
PT_LIMIT, PT_AMOUNT = Decimal("15000"), Decimal("200")   # professional tax
# Monthly TDS slabs applied marginally: (upper limit of slab, rate)
TDS_SLABS = [(Decimal("25000"), Decimal("0")), (Decimal("50000"), Decimal("0.05")),
             (Decimal("100000"), Decimal("0.10")), (None, Decimal("0.20"))]
REQUIRED = ["emp_id", "name", "department", "designation", "basic_salary"]


def money(value):
    return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def calc_tds(gross):
    """Marginal slab tax: each slice of gross is taxed at its own rate."""
    tax, lower = Decimal("0"), Decimal("0")
    for upper, rate in TDS_SLABS:
        top = gross if upper is None else min(gross, upper)
        if top > lower:
            tax += (top - lower) * rate
        if upper is None or gross <= upper:
            break
        lower = upper
    return money(tax)

def calculate_salary(basic, bonus=Decimal("0")):
    hra, da = money(basic * HRA_RATE), money(basic * DA_RATE)
    gross = money(basic + hra + da + TRANSPORT + bonus)
    pf = money(basic * PF_RATE)
    pt = PT_AMOUNT if gross > PT_LIMIT else Decimal("0")
    tds = calc_tds(gross)
    deductions = pf + pt + tds
    return {"basic": money(basic), "hra": hra, "da": da, "transport": TRANSPORT,
            "bonus": money(bonus), "gross": gross, "pf": pf, "pt": pt, "tds": tds,
            "deductions": money(deductions), "net": money(gross - deductions)}


# ------------------------------------------------------------ file reading
def to_amount(text, label):
    try:
        value = Decimal(text.strip())
    except Exception:
        raise ValueError(f"{label} '{text}' is not a number") from None
    if value < 0:
        raise ValueError(f"{label} cannot be negative")
    return value

def read_employees(path):
    """Return (valid_rows, rejected_rows). Raises for missing/empty/bad-header files."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV file not found: {path}")
    valid, rejected, seen = [], [], set()
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("CSV file is empty")
        headers = [h.strip().lower() for h in reader.fieldnames]
        missing = [c for c in REQUIRED if c not in headers]
        if missing:
            raise ValueError("Missing column(s): " + ", ".join(missing))
        for row_no, raw in enumerate(reader, start=2):      # row 1 is the header
            row = {(k or "").strip().lower(): (v or "").strip() for k, v in raw.items()}
            try:
                blanks = [c for c in ("emp_id", "name", "department") if not row[c]]
                if blanks:
                    raise ValueError("missing " + ", ".join(blanks))
                if row["emp_id"] in seen:
                    raise ValueError(f"duplicate emp_id {row['emp_id']}")
                row["basic"] = to_amount(row["basic_salary"], "basic_salary")
                row["bonus"] = to_amount(row.get("bonus") or "0", "bonus")
                if row["basic"] == 0:
                    raise ValueError("basic_salary must be above zero")
                seen.add(row["emp_id"])
                valid.append(row)
            except ValueError as err:
                rejected.append((row_no, err))
    if not valid and not rejected:
        raise ValueError("CSV file has a header but no employee rows")
    return valid, rejected


# ------------------------------------------------------------ reporting
def process(path, out_path="salary_summary.csv"):
    employees, rejected = read_employees(path)
    results = []
    for e in employees:
        results.append({**e, **calculate_salary(e["basic"], e["bonus"])})

    print("=" * 99)
    print(f" PAYROLL REGISTER - {os.path.basename(path)}  (amounts in Rs. per month)")
    print("=" * 99)
    print(f" {'ID':<6}{'NAME':<18}{'DEPT':<12}{'BASIC':>10}{'GROSS':>12}"
          f"{'PF':>10}{'PT':>6}{'TDS':>10}{'DEDUCT.':>11}{'NET PAY':>11}")
    print("-" * 98)
    for r in results:
        print(f" {r['emp_id']:<6}{r['name']:<18}{r['department']:<12}{r['basic']:>10,.2f}"
              f"{r['gross']:>12,.2f}{r['pf']:>10,.2f}{r['pt']:>6,.0f}{r['tds']:>10,.2f}"
              f"{r['deductions']:>11,.2f}{r['net']:>11,.2f}")
    print("-" * 98)

    total = lambda key: sum((r[key] for r in results), Decimal("0"))
    print(f" Employees processed : {len(results)}    Rows rejected : {len(rejected)}")
    print(f" Total gross  : Rs. {total('gross'):>12,.2f}")
    print(f" Total deduct.: Rs. {total('deductions'):>12,.2f}")
    print(f" Total net pay: Rs. {total('net'):>12,.2f}   "
          f"(average Rs. {money(total('net') / len(results)):,.2f})")
    best = max(results, key=lambda r: r["net"])
    least = min(results, key=lambda r: r["net"])
    print(f" Highest net  : {best['name']} (Rs. {best['net']:,.2f})")
    print(f" Lowest net   : {least['name']} (Rs. {least['net']:,.2f})")

    dept = defaultdict(lambda: [0, Decimal("0"), Decimal("0")])
    for r in results:
        d = dept[r["department"]]
        d[0] += 1; d[1] += r["gross"]; d[2] += r["net"]
    print("\n DEPARTMENT-WISE SUMMARY")
    print(f" {'Department':<14}{'Staff':>6}{'Gross (Rs.)':>16}{'Net (Rs.)':>16}")
    for name, (count, gross, net) in sorted(dept.items()):
        print(f" {name:<14}{count:>6}{gross:>16,.2f}{net:>16,.2f}")

    if rejected:
        print("\n REJECTED ROWS (not paid - please correct the CSV)")
        for row_no, err in rejected:
            print(f"   Row {row_no}: {err}")

    cols = ["emp_id", "name", "department", "basic", "hra", "da", "transport", "bonus",
            "gross", "pf", "pt", "tds", "deductions", "net"]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(cols)
        for r in results:
            writer.writerow([r[c] for c in cols])
    print(f"\n Summary written to {out_path}")
    return results


def run_tests():
    """Hand-calculated check: basic 40,000 and no bonus."""
    s = calculate_salary(Decimal("40000"))
    assert s["hra"] == Decimal("8000.00") and s["da"] == Decimal("4000.00")
    assert s["gross"] == Decimal("53600.00")            # 40000+8000+4000+1600
    assert s["pf"] == Decimal("4800.00") and s["pt"] == Decimal("200")
    assert s["tds"] == Decimal("1610.00")               # 1250 (25k-50k @5%) + 360 (3.6k @10%)
    assert s["net"] == Decimal("46990.00")              # 53600 - 4800 - 200 - 1610
    print("TEST 1 passed : basic 40,000 -> gross 53,600.00, deductions 6,610.00, net 46,990.00")
    low = calculate_salary(Decimal("10000"))
    assert low["gross"] == Decimal("14600.00") and low["pt"] == 0 and low["tds"] == 0
    print("TEST 2 passed : low salary -> no professional tax, no TDS")
    for bad, label in (("abc", "text"), ("-5", "negative")):
        try:
            to_amount(bad, "basic_salary")
        except ValueError:
            print(f"TEST 3 passed : {label} salary rejected")
    try:
        read_employees("no_such_file.csv")
    except FileNotFoundError:
        print("TEST 4 passed : missing file handled")


if __name__ == "__main__":
    if "--test" in sys.argv:
        run_tests()
    else:
        file_path = sys.argv[1] if len(sys.argv) > 1 else "employees.csv"
        try:
            process(file_path)
        except (FileNotFoundError, ValueError) as err:
            print("[ERROR]", err)
