"""
Lab Exercise 15 : Library Management System
Concepts        : Classes, objects, inheritance, polymorphism,
                  availability tracking, issue / return logic, fines
"""
 
from datetime import date, timedelta
 
 
class LibraryError(Exception):
    """Base class for library related errors."""
 
 
# ---------------------------------------------------------------
# Base class : LibraryItem  (common attributes of everything we lend)
# ---------------------------------------------------------------
class LibraryItem:
    LOAN_DAYS = 14            # default loan period
    FINE_PER_DAY = 2          # Rs. per late day
 
    def __init__(self, item_id, title, copies=1):
        self.item_id = item_id
        self.title = title
        self.total_copies = copies
        self.available_copies = copies
 
    @property
    def is_available(self):
        return self.available_copies > 0
 
    def status(self):
        return "Available" if self.is_available else "Issued"
 
    def details(self):
        copies = f"{self.available_copies}/{self.total_copies}"
        return f"{self.item_id:<6}{self.title:<34}{self.kind():<10}{copies:<5} {self.status()}"
 
    def kind(self):
        return "Item"
 
 
# ---------------------------------------------------------------
# Derived classes : Book and Magazine (INHERITANCE)
# ---------------------------------------------------------------
class Book(LibraryItem):
    def __init__(self, item_id, title, author, copies=1):
        super().__init__(item_id, title, copies)
        self.author = author
 
    def kind(self):
        return "Book"
 
 
class Magazine(LibraryItem):
    LOAN_DAYS = 7              # method/attribute overriding: shorter loan period
    FINE_PER_DAY = 1
 
    def __init__(self, item_id, title, issue_no, copies=1):
        super().__init__(item_id, title, copies)
        self.issue_no = issue_no
 
    def kind(self):
        return "Magazine"
 
 
# ---------------------------------------------------------------
# Member class
# ---------------------------------------------------------------
class Member:
    MAX_ITEMS = 2
 
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.borrowed = {}          # item_id -> due_date
        self.fines_paid = 0
 
    def __str__(self):
        return f"{self.member_id} ({self.name})"
 
 
# ---------------------------------------------------------------
# Library class : controls the whole system
# ---------------------------------------------------------------
class Library:
    def __init__(self, name):
        self.name = name
        self.items = {}
        self.members = {}
        self.log = []
 
    # ----- set-up -----
    def add_item(self, item):
        self.items[item.item_id] = item
 
    def add_member(self, member):
        self.members[member.member_id] = member
 
    # ----- lookup helpers -----
    def _item(self, item_id):
        if item_id not in self.items:
            raise LibraryError(f"Item '{item_id}' does not exist in catalogue.")
        return self.items[item_id]
 
    def _member(self, member_id):
        if member_id not in self.members:
            raise LibraryError(f"Member '{member_id}' is not registered.")
        return self.members[member_id]
 
    # ----- core operations -----
    def issue_item(self, member_id, item_id, on_date):
        member, item = self._member(member_id), self._item(item_id)
        if item_id in member.borrowed:
            raise LibraryError(f"{member.name} already holds '{item.title}'.")
        if len(member.borrowed) >= Member.MAX_ITEMS:
            raise LibraryError(f"{member.name} reached the limit of {Member.MAX_ITEMS} items.")
        if not item.is_available:
            raise LibraryError(f"'{item.title}' is currently not available (all copies issued).")
        item.available_copies -= 1
        due = on_date + timedelta(days=item.LOAN_DAYS)
        member.borrowed[item_id] = due
        self.log.append((on_date, "ISSUE", member_id, item_id))
        return f"Issued '{item.title}' to {member.name}. Due on {due:%d-%b-%Y}."
 
    def return_item(self, member_id, item_id, on_date):
        member, item = self._member(member_id), self._item(item_id)
        if item_id not in member.borrowed:
            raise LibraryError(f"{member.name} has not borrowed '{item.title}'.")
        due = member.borrowed.pop(item_id)
        item.available_copies += 1
        late_days = max(0, (on_date - due).days)
        fine = late_days * item.FINE_PER_DAY
        member.fines_paid += fine
        self.log.append((on_date, "RETURN", member_id, item_id))
        if fine:
            return f"Returned '{item.title}' {late_days} day(s) late. Fine = Rs. {fine}."
        return f"Returned '{item.title}' on time. No fine."
 
    def search(self, keyword):
        keyword = keyword.lower()
        return [i for i in self.items.values() if keyword in i.title.lower()]
 
    def show_catalogue(self):
        print(f"  {'ID':<6}{'TITLE':<34}{'TYPE':<10}{'AVL':<5} STATUS")
        print("  " + "-" * 66)
        for item in self.items.values():
            print("  " + item.details())
 
 
# ---------------------------------------------------------------
# Test harness
# ---------------------------------------------------------------
def attempt(title, action):
    try:
        print(f"  [OK]      {title:<38} -> {action()}")
    except LibraryError as err:
        print(f"  [BLOCKED] {title:<38} -> {err}")
 
 
def main():
    lib = Library("Central Library")
    lib.add_item(Book("B101", "Python Crash Course", "Eric Matthes", copies=2))
    lib.add_item(Book("B102", "Introduction to Algorithms", "T. H. Cormen", copies=1))
    lib.add_item(Book("B103", "Artificial Intelligence", "Stuart Russell", copies=1))
    lib.add_item(Magazine("M201", "Data Science Monthly", issue_no=42, copies=1))
    lib.add_member(Member("S01", "Sriram"))
    lib.add_member(Member("S02", "Rahul"))
    lib.add_member(Member("S03", "Ananya"))
 
    day0 = date(2026, 10, 1)      # fixed date so the output is reproducible
 
    print("=" * 78)
    print(" 1. INITIAL CATALOGUE")
    print("=" * 78)
    lib.show_catalogue()
 
    print()
    print("=" * 78)
    print(" 2. ISSUING BOOKS")
    print("=" * 78)
    attempt("S01 issues B101", lambda: lib.issue_item("S01", "B101", day0))
    attempt("S02 issues B101 (2nd copy)", lambda: lib.issue_item("S02", "B101", day0))
    attempt("S03 issues B101 (no copies left)", lambda: lib.issue_item("S03", "B101", day0))
    attempt("S01 issues B102", lambda: lib.issue_item("S01", "B102", day0))
    attempt("S01 issues B103 (limit of 2 reached)", lambda: lib.issue_item("S01", "B103", day0))
    attempt("S03 issues M201 (magazine, 7 days)", lambda: lib.issue_item("S03", "M201", day0))
    attempt("S01 issues B101 again (duplicate)", lambda: lib.issue_item("S01", "B101", day0))
 
    print()
    print("=" * 78)
    print(" 3. INVALID REQUESTS")
    print("=" * 78)
    attempt("Unknown member S99", lambda: lib.issue_item("S99", "B103", day0))
    attempt("Unknown book B999", lambda: lib.issue_item("S02", "B999", day0))
 
    print()
    print("=" * 78)
    print(" 4. CATALOGUE AFTER ISSUING")
    print("=" * 78)
    lib.show_catalogue()
 
    print()
    print("=" * 78)
    print(" 5. RETURNING (ON TIME AND LATE)")
    print("=" * 78)
    attempt("S01 returns B101 on day 10 (on time)", lambda: lib.return_item("S01", "B101", day0 + timedelta(days=10)))
    attempt("S02 returns B101 on day 20 (6 late)", lambda: lib.return_item("S02", "B101", day0 + timedelta(days=20)))
    attempt("S03 returns M201 on day 12 (5 late)", lambda: lib.return_item("S03", "M201", day0 + timedelta(days=12)))
    attempt("S03 returns B103 (never borrowed)", lambda: lib.return_item("S03", "B103", day0 + timedelta(days=12)))
    attempt("S03 issues B103 (after returns)", lambda: lib.issue_item("S03", "B103", day0 + timedelta(days=13)))
 
    print()
    print("=" * 78)
    print(" 6. SEARCH AND FINAL STATUS")
    print("=" * 78)
    print("  Search 'python' ->", [b.title for b in lib.search("python")])
    print("  Search 'data'   ->", [b.title for b in lib.search("data")])
    print()
    lib.show_catalogue()
    print()
    print("  Fines collected :", {m.name: m.fines_paid for m in lib.members.values()})
    print("  Transactions    :", len(lib.log))
 
 
if __name__ == "__main__":
    main()
