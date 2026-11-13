"""
Attendance Tracker  -  Python Programming (Unit 3 Mini Project)
Data structures used
--------------------
students   : list   -> ordered list of student names
class_dates: list   -> ordered list of dates on which classes were held
attendance : dict   -> {student_name: {date: status}}
                       status is "P" (Present), "A" (Absent) or "L" (Late)
Late is counted as attended when percentages are calculated.
"""
VALID_STATUS = {"P": "Present", "A": "Absent", "L": "Late"}
DEFAULT_THRESHOLD = 75.0
class AttendanceTracker:
    def __init__(self):
        self.students = []        # list of names
        self.class_dates = []     # list of dates (strings)
        self.attendance = {}      # dict of dicts
    # ---------------------------------------------------------------
    # 1. Adding students and class dates
    # ---------------------------------------------------------------
    def add_student(self, name):
        name = name.strip().title()
        if not name:
            raise ValueError("Student name cannot be empty.")
        if name in self.attendance:
            raise ValueError(f"Student '{name}' already exists.")
        self.students.append(name)
        self.attendance[name] = {}
        return name
    def add_class_date(self, date):
        date = date.strip()
        if not date:
            raise ValueError("Date cannot be empty.")
        if date in self.class_dates:
            raise ValueError(f"Class date '{date}' already exists.")
        self.class_dates.append(date)
    # ---------------------------------------------------------------
    # 2. Marking and updating attendance
    # ---------------------------------------------------------------
    def mark_attendance(self, name, date, status):
        """Add a new record OR update an existing one."""
        name = name.strip().title()
        status = status.strip().upper()
        if name not in self.attendance:
            raise KeyError(f"Student '{name}' not found.")
        if date not in self.class_dates:
            raise KeyError(f"Date '{date}' is not a recorded class date.")
        if status not in VALID_STATUS:
            raise ValueError("Status must be P, A or L.")
        old = self.attendance[name].get(date)
        self.attendance[name][date] = status
        return "added" if old is None else f"updated ({old} -> {status})"
    def mark_whole_class(self, date, status_map):
        """status_map = {name: status}; students not listed are marked P."""
        for name in self.students:
            self.mark_attendance(name, date, status_map.get(name, "P"))
    # ---------------------------------------------------------------
    # 3. Calculations
    # ---------------------------------------------------------------
    def counts(self, name):
        record = self.attendance[name]
        present = sum(1 for s in record.values() if s == "P")
        late = sum(1 for s in record.values() if s == "L")
        absent = sum(1 for s in record.values() if s == "A")
        return present, late, absent
    def percentage(self, name):
        name = name.strip().title()
        if name not in self.attendance:
            raise KeyError(f"Student '{name}' not found.")
        present, late, absent = self.counts(name)
        total = present + late + absent
        if total == 0:
            return 0.0
        return round((present + late) / total * 100, 2)
    def below_threshold(self, threshold=DEFAULT_THRESHOLD):
        """Return list of (name, percentage) below the threshold."""
        result = []
        for name in self.students:
            pct = self.percentage(name)
            if pct < threshold:
                result.append((name, pct))
        return sorted(result, key=lambda item: item[1])
    # ---------------------------------------------------------------
    # 4. Display
    # ---------------------------------------------------------------
    def display_records(self):
        if not self.students:
            print("No students recorded yet.")
            return
        name_w = max(len("Student"), max(len(s) for s in self.students)) + 2
        header = "Student".ljust(name_w)
        for d in self.class_dates:
            header += d.center(7)
        header += "  Att%".rjust(8)
        print(header)
        print("-" * len(header))
        for name in self.students:
            row = name.ljust(name_w)
            for d in self.class_dates:
                row += self.attendance[name].get(d, "-").center(7)
            row += f"{self.percentage(name):7.2f}%"
            print(row)
    def display_summary(self, threshold=DEFAULT_THRESHOLD):
        print(f"{'Student':<14}{'P':>3}{'L':>3}{'A':>3}{'Total':>7}{'Att%':>9}  Status")
        print("-" * 52)
        for name in self.students:
            p, l, a = self.counts(name)
            pct = self.percentage(name)
            flag = "OK" if pct >= threshold else "LOW - SHORTAGE"
            print(f"{name:<14}{p:>3}{l:>3}{a:>3}{p + l + a:>7}{pct:>8.2f}%  {flag}")
        low = self.below_threshold(threshold)
        print(f"\nStudents below {threshold:.0f}%: ", end="")
        print(", ".join(f"{n} ({p}%)" for n, p in low) if low else "None")
    def class_average(self):
        if not self.students:
            return 0.0
        return round(sum(self.percentage(s) for s in self.students) / len(self.students), 2)
# -------------------------------------------------------------------
# Interactive menu
# -------------------------------------------------------------------
def menu():
    tracker = AttendanceTracker()
    options = """
===== ATTENDANCE TRACKER =====
1. Add student
2. Add class date
3. Mark / update attendance
4. Display attendance records
5. Show attendance summary
6. Students below threshold
7. Exit
"""
    while True:
        print(options)
        choice = input("Enter choice: ").strip()
        try:
            if choice == "1":
                print("Added:", tracker.add_student(input("Student name: ")))
            elif choice == "2":
                tracker.add_class_date(input("Date (e.g. 01-Oct): "))
                print("Class date added.")
            elif choice == "3":
                n = input("Student name: ")
                d = input("Date: ")
                s = input("Status (P/A/L): ")
                print("Record", tracker.mark_attendance(n, d, s))
            elif choice == "4":
                tracker.display_records()
            elif choice == "5":
                tracker.display_summary()
            elif choice == "6":
                t = float(input("Threshold %: "))
                for n, p in tracker.below_threshold(t):
                    print(f"{n}: {p}%")
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
        except (ValueError, KeyError) as err:
            print("Error:", err)
if __name__ == "__main__":
    menu()
