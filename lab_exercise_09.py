"""
Lab Exercise 9 : Student Grading System using Dictionaries
Data structure used
-------------------
students : dict of dict   {student_name: {subject: marks}}
subjects : list           ordered subject names
Grade boundaries (percentage)         Grade  Points  Remark
    90 and above                        O      10    Outstanding
    80 to below 90                      A+      9    Excellent
    70 to below 80                      A       8    Very Good
    60 to below 70                      B+      7    Good
    50 to below 60                      B       6    Above Average
    40 to below 50                      C       5    Pass
    below 40                            F       0    Fail
Pass rule: a student must score at least 40 in EVERY subject. A student who
fails even one subject receives the overall grade F, whatever the average is.
"""
PASS_MARK = 40
MAX_MARKS = 100
def get_grade(percentage):
    """Convert a percentage into (grade, grade points, remark) using if/elif."""
    if percentage < 0 or percentage > 100:
        raise ValueError("Percentage must be between 0 and 100.")
    if percentage >= 90:
        return "O", 10, "Outstanding"
    elif percentage >= 80:
        return "A+", 9, "Excellent"
    elif percentage >= 70:
        return "A", 8, "Very Good"
    elif percentage >= 60:
        return "B+", 7, "Good"
    elif percentage >= 50:
        return "B", 6, "Above Average"
    elif percentage >= PASS_MARK:
        return "C", 5, "Pass"
    else:
        return "F", 0, "Fail"
class GradingSystem:
    def __init__(self, subjects):
        if not subjects:
            raise ValueError("At least one subject is required.")
        self.subjects = list(subjects)     # list
        self.students = {}                 # dict of dicts
    # ---------------------------------------------------------------
    # Store / update marks
    # ---------------------------------------------------------------
    def _check_mark(self, mark):
        if not isinstance(mark, (int, float)) or isinstance(mark, bool):
            raise ValueError("Marks must be a number.")
        if mark < 0 or mark > MAX_MARKS:
            raise ValueError(f"Marks must be between 0 and {MAX_MARKS}.")
    def add_student(self, name, marks):
        name = name.strip().title()
        if not name:
            raise ValueError("Student name cannot be empty.")
        if name in self.students:
            raise ValueError(f"Student '{name}' already exists.")
        if set(marks) != set(self.subjects):
            raise ValueError(f"Marks must be given for exactly: {', '.join(self.subjects)}.")
        for mark in marks.values():
            self._check_mark(mark)
        self.students[name] = dict(marks)
    def update_mark(self, name, subject, mark):
        name = name.strip().title()
        if name not in self.students:
            raise KeyError(f"Student '{name}' not found.")
        if subject not in self.subjects:
            raise KeyError(f"Subject '{subject}' not found.")
        self._check_mark(mark)
        old = self.students[name][subject]
        self.students[name][subject] = mark
        return old
    # ---------------------------------------------------------------
    # Calculations
    # ---------------------------------------------------------------
    def total(self, name):
        return sum(self.students[name].values())
    def percentage(self, name):
        return round(self.total(name) / (len(self.subjects) * MAX_MARKS) * 100, 2)
    def failed_subjects(self, name):
        return [s for s, m in self.students[name].items() if m < PASS_MARK]
    def result(self, name):
        """Return dict with total, percentage, grade, points, remark, status."""
        pct = self.percentage(name)
        failed = self.failed_subjects(name)
        if failed:
            grade, points, remark = "F", 0, "Fail"
            status = "FAIL"
        else:
            grade, points, remark = get_grade(pct)
            status = "PASS"
        return {"total": self.total(name), "percentage": pct, "grade": grade,
                "points": points, "remark": remark, "status": status, "failed": failed}
    def ranking(self):
        """Students sorted by percentage, highest first."""
        return sorted(self.students, key=lambda n: self.percentage(n), reverse=True)
    def subject_average(self, subject):
        return round(sum(m[subject] for m in self.students.values()) / len(self.students), 2)
    def grade_distribution(self):
        dist = {g: 0 for g in ("O", "A+", "A", "B+", "B", "C", "F")}
        for name in self.students:
            dist[self.result(name)["grade"]] += 1
        return dist
    def class_statistics(self):
        names = list(self.students)
        pcts = [self.percentage(n) for n in names]
        passed = sum(1 for n in names if self.result(n)["status"] == "PASS")
        return {"students": len(names),
                "class_average": round(sum(pcts) / len(pcts), 2),
                "highest": max(pcts), "lowest": min(pcts),
                "topper": self.ranking()[0],
                "pass_count": passed,
                "pass_percentage": round(passed / len(names) * 100, 2)}
    # ---------------------------------------------------------------
    # Display
    # ---------------------------------------------------------------
    def display_marks(self):
        short = [s[:7] for s in self.subjects]
        print(f"{'Student':<12}" + "".join(f"{s:>8}" for s in short))
        print("-" * (12 + 8 * len(short)))
        for name, marks in self.students.items():
            print(f"{name:<12}" + "".join(f"{marks[s]:>8}" for s in self.subjects))
    def display_results(self):
        if not self.students:
            print("No students recorded yet.")
            return
        print(f"{'Rank':<5}{'Student':<12}{'Total':>6}{'  %':>8}{'Grade':>7}{'GP':>4}  {'Result':<6} Remark")
        print("-" * 66)
        for rank, name in enumerate(self.ranking(), start=1):
            r = self.result(name)
            extra = f"  (failed: {', '.join(r['failed'])})" if r["failed"] else ""
            print(f"{rank:<5}{name:<12}{r['total']:>6}{r['percentage']:>8.2f}{r['grade']:>7}"
                  f"{r['points']:>4}  {r['status']:<6} {r['remark']}{extra}")
    def display_statistics(self):
        st = self.class_statistics()
        print(f"Students          : {st['students']}")
        print(f"Class average     : {st['class_average']}%")
        print(f"Highest / Lowest  : {st['highest']}% / {st['lowest']}%")
        print(f"Topper            : {st['topper']}")
        print(f"Pass percentage   : {st['pass_percentage']}% ({st['pass_count']} of {st['students']})")
        print("Subject averages  :", ", ".join(f"{s} {self.subject_average(s)}" for s in self.subjects))
        print("Grade distribution:")
        for g, n in self.grade_distribution().items():
            print(f"   {g:<3} {'#' * n:<10} {n}")
# -------------------------------------------------------------------
# Menu driven program
# -------------------------------------------------------------------
def menu():
    gs = GradingSystem(["Python", "Maths", "Physics", "English", "DS"])
    options = """
===== STUDENT GRADING SYSTEM =====
1. Add student marks     4. Show statistics
2. Update a mark         5. Exit
3. Show results
"""
    while True:
        print(options)
        choice = input("Enter choice: ").strip()
        try:
            if choice == "1":
                name = input("Student name: ")
                marks = {s: float(input(f"  {s} marks: ")) for s in gs.subjects}
                gs.add_student(name, marks)
                print("Student added.")
            elif choice == "2":
                old = gs.update_mark(input("Student: "), input("Subject: "), float(input("New marks: ")))
                print("Updated. Old marks were", old)
            elif choice == "3":
                gs.display_results()
            elif choice == "4":
                gs.display_statistics()
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
        except (ValueError, KeyError) as err:
            print("Error:", err)
if __name__ == "__main__":
    menu()
