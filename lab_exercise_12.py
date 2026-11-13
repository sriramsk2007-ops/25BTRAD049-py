"""
Lab Exercise 12 : Student Data Manager Using Files
Store, retrieve, search, update, delete and display student records in a text file.
Record format (one student per line, fields separated by '|'):
    USN|Name|Branch|Semester|CGPA
Usage : python student_manager.py          (interactive menu)
        python student_manager.py --demo   (scripted demonstration / tests)
"""
import os
import re
import sys

DATA_FILE = "students.txt"
DELIM = "|"
FIELDS = ("usn", "name", "branch", "semester", "cgpa")
USN_RE = re.compile(r"^\d{2}[A-Z]{3,6}\d{3}$")          # e.g. 25BTRAD049
NAME_RE = re.compile(r"^[A-Za-z][A-Za-z .'-]{1,49}$")


# ---------------------------------------------------------------- validation
def validate_usn(value):
    value = value.strip().upper()
    if not USN_RE.match(value):
        raise ValueError("USN must look like 25BTRAD049 (2 digits + letters + 3 digits)")
    return value

def validate_name(value):
    value = " ".join(value.split())
    if not NAME_RE.match(value):
        raise ValueError("Name must be 2-50 characters (letters, spaces, . ' - only)")
    return value.title()

def validate_branch(value):
    value = value.strip().upper()
    if not re.match(r"^[A-Z][A-Z -]{1,19}$", value):
        raise ValueError("Branch must be 2-20 letters, e.g. CSE-AIDE")
    return value

def validate_semester(value):
    if not str(value).strip().isdigit() or not 1 <= int(value) <= 8:
        raise ValueError("Semester must be a whole number from 1 to 8")
    return int(value)

def validate_cgpa(value):
    try:
        number = float(value)
    except ValueError:
        raise ValueError("CGPA must be a number") from None
    if not 0.0 <= number <= 10.0:
        raise ValueError("CGPA must be between 0 and 10")
    return round(number, 2)

VALIDATORS = {"usn": validate_usn, "name": validate_name, "branch": validate_branch,
              "semester": validate_semester, "cgpa": validate_cgpa}


# ------------------------------------------------------------ file handling
def load_all():
    """Read every valid record from the file (a missing file means no records yet)."""
    records = []
    if not os.path.exists(DATA_FILE):
        return records
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split(DELIM)
            if len(parts) != len(FIELDS):
                continue                       # skip blank / corrupted lines
            records.append(dict(zip(FIELDS, parts)))
    return records

def save_all(records):
    """Write to a temporary file first, then replace - protects against half-written data."""
    temp = DATA_FILE + ".tmp"
    with open(temp, "w", encoding="utf-8") as f:
        for r in records:
            f.write(DELIM.join(str(r[k]) for k in FIELDS) + "\n")
    os.replace(temp, DATA_FILE)


# ---------------------------------------------------------------- operations
def add_student(usn, name, branch, semester, cgpa):
    record = {"usn": validate_usn(usn), "name": validate_name(name),
              "branch": validate_branch(branch), "semester": validate_semester(semester),
              "cgpa": validate_cgpa(cgpa)}
    records = load_all()
    if any(r["usn"] == record["usn"] for r in records):
        raise ValueError(f"Duplicate USN {record['usn']} - record already exists")
    with open(DATA_FILE, "a", encoding="utf-8") as f:          # append mode
        f.write(DELIM.join(str(record[k]) for k in FIELDS) + "\n")
    return record

def search_students(keyword):
    """Exact USN match or case-insensitive partial name / branch match."""
    key = keyword.strip().lower()
    return [r for r in load_all()
            if key == r["usn"].lower() or key in r["name"].lower() or key == r["branch"].lower()]

def update_student(usn, **changes):
    usn = validate_usn(usn)
    records = load_all()
    for r in records:
        if r["usn"] == usn:
            for field, value in changes.items():
                if field == "usn" or field not in VALIDATORS:
                    raise ValueError(f"Field '{field}' cannot be updated")
                r[field] = VALIDATORS[field](value)
            save_all(records)
            return r
    raise KeyError(f"No student found with USN {usn}")

def delete_student(usn):
    usn = validate_usn(usn)
    records = load_all()
    kept = [r for r in records if r["usn"] != usn]
    if len(kept) == len(records):
        raise KeyError(f"No student found with USN {usn}")
    save_all(kept)

def display(records):
    if not records:
        print("  (no records to show)")
        return
    line = "+-------------+-----------------------+------------+-----+-------+"
    print(line)
    print(f"| {'USN':<11} | {'NAME':<21} | {'BRANCH':<10} | {'SEM':<3} | {'CGPA':<5} |")
    print(line)
    for r in sorted(records, key=lambda x: x["usn"]):
        print(f"| {r['usn']:<11} | {r['name']:<21} | {r['branch']:<10} | "
              f"{r['semester']:<3} | {float(r['cgpa']):<5.2f} |")
    print(line)
    print(f"  {len(records)} record(s)")

def statistics():
    records = load_all()
    if not records:
        print("  No data for statistics.")
        return
    cgpas = [float(r["cgpa"]) for r in records]
    top = max(records, key=lambda r: float(r["cgpa"]))
    print(f"  Students: {len(records)} | Average CGPA: {sum(cgpas)/len(cgpas):.2f} | "
          f"Topper: {top['name']} ({top['cgpa']})")


# ------------------------------------------------------------ user interface
def ask(prompt, validator):
    """Keep asking until the input passes validation."""
    while True:
        try:
            return validator(input(prompt))
        except ValueError as err:
            print("  Invalid input:", err)

def menu():
    options = """
 ===== STUDENT DATA MANAGER =====
  1. Add student      4. Update student
  2. View all         5. Delete student
  3. Search           6. Statistics
  0. Exit"""
    while True:
        print(options)
        choice = input(" Choose an option: ").strip()
        try:
            if choice == "1":
                rec = add_student(ask(" USN      : ", validate_usn), ask(" Name     : ", validate_name),
                                  ask(" Branch   : ", validate_branch), ask(" Semester : ", validate_semester),
                                  ask(" CGPA     : ", validate_cgpa))
                print("  Saved:", rec["name"])
            elif choice == "2":
                display(load_all())
            elif choice == "3":
                display(search_students(input(" Enter USN / name / branch: ")))
            elif choice == "4":
                usn = ask(" USN to update: ", validate_usn)
                field = input(" Field (name/branch/semester/cgpa): ").strip().lower()
                update_student(usn, **{field: input(" New value: ")})
                print("  Record updated.")
            elif choice == "5":
                delete_student(input(" USN to delete: "))
                print("  Record deleted.")
            elif choice == "6":
                statistics()
            elif choice == "0":
                print(" Goodbye!")
                break
            else:
                print("  Please choose a number from the menu.")
        except (ValueError, KeyError) as err:
            print("  Error:", str(err).strip("'\""))


def demo():
    """Scripted run that exercises every operation, including invalid input."""
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    print(">> Add three students")
    add_student("25BTRAD049", "sriram satvik karanam", "cse-aide", 3, 8.9)
    add_student("25BTRAD101", "Ananya Rao", "CSE-AIDE", 3, 9.2)
    add_student("25BTRCS045", "Rahul Menon", "CSE", 3, 7.6)
    display(load_all())
    print("\n>> Try bad data (each must be rejected)")
    for bad in [("25BTRAD049", "Duplicate Guy", "CSE", 3, 8),
                ("ABC", "Wrong Usn", "CSE", 3, 8), ("25BTRAD150", "Asha K", "CSE", 9, 8),
                ("25BTRAD151", "Asha K", "CSE", 3, 11.5), ("25BTRAD152", "R2D2", "CSE", 3, 8)]:
        try:
            add_student(*bad)
        except ValueError as err:
            print("  Rejected:", err)
    print("\n>> Search 'rao', then search by USN 25BTRCS045")
    display(search_students("rao"))
    display(search_students("25BTRCS045"))
    print("\n>> Update Rahul's CGPA to 8.1 and semester to 4")
    update_student("25BTRCS045", cgpa=8.1, semester=4)
    display(search_students("Rahul"))
    print("\n>> Delete 25BTRAD101, then try deleting it again")
    delete_student("25BTRAD101")
    try:
        delete_student("25BTRAD101")
    except KeyError as err:
        print("  Error:", str(err).strip("'\""))
    display(load_all())
    statistics()
    print("\n>> Raw contents of", DATA_FILE)
    print(open(DATA_FILE).read())


if __name__ == "__main__":
    demo() if "--demo" in sys.argv else menu()
