"""
Lab Exercise 8 : Contact Book using Lists and Dictionaries
Data structure used
-------------------
contacts : list of dict
    [{"name": "Asha Rao", "phone": "9876543210",
      "email": "asha@example.com", "category": "Friend"}, ...]
The phone number is treated as the unique key of a contact because two
different people can share the same name but never the same phone number.
"""
import re
FIELDS = ("name", "phone", "email", "category")
class ContactBook:
    def __init__(self):
        self.contacts = []          # list of dictionaries
    # ---------------------------------------------------------------
    # Validation helpers
    # ---------------------------------------------------------------
    @staticmethod
    def clean_phone(phone):
        return re.sub(r"[\s\-+]", "", phone.strip())
    @staticmethod
    def valid_phone(phone):
        """10 digits, first digit between 6 and 9 (Indian mobile numbers)."""
        return bool(re.fullmatch(r"[6-9]\d{9}", phone))
    @staticmethod
    def valid_email(email):
        """Email is optional; if given it must look like name@domain.ext"""
        return email == "" or bool(re.fullmatch(r"[\w.+-]+@[\w-]+(\.[\w-]+)+", email))
    # ---------------------------------------------------------------
    # ADD
    # ---------------------------------------------------------------
    def add_contact(self, name, phone, email="", category="Other"):
        name = name.strip().title()
        phone = self.clean_phone(phone)
        email = email.strip().lower()
        category = category.strip().title() or "Other"
        if not name:
            raise ValueError("Name cannot be empty.")
        if not self.valid_phone(phone):
            raise ValueError(f"Invalid phone number '{phone}' (need 10 digits starting 6-9).")
        if not self.valid_email(email):
            raise ValueError(f"Invalid email '{email}'.")
        if self.find_by_phone(phone):
            raise ValueError(f"A contact with phone {phone} already exists.")
        contact = {"name": name, "phone": phone, "email": email, "category": category}
        self.contacts.append(contact)
        return contact
    # ---------------------------------------------------------------
    # SEARCH
    # ---------------------------------------------------------------
    def find_by_phone(self, phone):
        phone = self.clean_phone(phone)
        for contact in self.contacts:
            if contact["phone"] == phone:
                return contact
        return None
    def search(self, query, field="name"):
        """Case-insensitive search. Returns a list of matching contacts."""
        if field not in FIELDS:
            raise ValueError(f"Search field must be one of {FIELDS}.")
        query = query.strip().lower()
        if field == "category":
            return [c for c in self.contacts if c["category"].lower() == query]
        return [c for c in self.contacts if query in c[field].lower()]
    # ---------------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------------
    def update_contact(self, phone, field, new_value):
        contact = self.find_by_phone(phone)
        if contact is None:
            raise KeyError(f"No contact found with phone {phone}.")
        if field not in FIELDS:
            raise ValueError(f"Field must be one of {FIELDS}.")
        new_value = new_value.strip()
        if field == "name":
            new_value = new_value.title()
            if not new_value:
                raise ValueError("Name cannot be empty.")
        elif field == "phone":
            new_value = self.clean_phone(new_value)
            if not self.valid_phone(new_value):
                raise ValueError(f"Invalid phone number '{new_value}'.")
            if self.find_by_phone(new_value):
                raise ValueError(f"Phone {new_value} already belongs to another contact.")
        elif field == "email":
            new_value = new_value.lower()
            if not self.valid_email(new_value):
                raise ValueError(f"Invalid email '{new_value}'.")
        else:
            new_value = new_value.title() or "Other"
        old_value = contact[field]
        contact[field] = new_value
        return old_value
    # ---------------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------------
    def delete_contact(self, phone):
        contact = self.find_by_phone(phone)
        if contact is None:
            raise KeyError(f"No contact found with phone {phone}.")
        self.contacts.remove(contact)
        return contact
    # ---------------------------------------------------------------
    # DISPLAY
    # ---------------------------------------------------------------
    def display(self, contacts=None, sort_by="name"):
        rows = self.contacts if contacts is None else contacts
        if not rows:
            print("No contacts to display.")
            return
        rows = sorted(rows, key=lambda c: (c[sort_by].lower(), c["name"].lower()))
        head = f"{'No.':<5}{'Name':<20}{'Phone':<13}{'Category':<12}Email"
        print(head)
        print("-" * 70)
        for i, c in enumerate(rows, start=1):
            print(f"{i:<5}{c['name']:<20}{c['phone']:<13}{c['category']:<12}{c['email'] or '-'}")
        print(f"\nTotal: {len(rows)} contact(s)")
    def group_by_category(self):
        groups = {}
        for c in self.contacts:
            groups.setdefault(c["category"], []).append(c["name"])
        return groups
# -------------------------------------------------------------------
# Menu driven program
# -------------------------------------------------------------------
def menu():
    book = ContactBook()
    options = """
===== CONTACT BOOK =====
1. Add contact        4. Delete contact
2. Search contact     5. Display all
3. Update contact     6. Exit
"""
    while True:
        print(options)
        choice = input("Enter choice: ").strip()
        try:
            if choice == "1":
                c = book.add_contact(input("Name: "), input("Phone: "),
                                     input("Email (optional): "), input("Category: "))
                print("Added:", c["name"])
            elif choice == "2":
                field = input("Search by (name/phone/email/category): ").strip().lower()
                book.display(book.search(input("Search text: "), field))
            elif choice == "3":
                old = book.update_contact(input("Phone of contact: "),
                                          input("Field to change: ").strip().lower(),
                                          input("New value: "))
                print("Updated. Old value was:", old)
            elif choice == "4":
                print("Deleted:", book.delete_contact(input("Phone of contact: "))["name"])
            elif choice == "5":
                book.display()
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
        except (ValueError, KeyError) as err:
            print("Error:", err)
if __name__ == "__main__":
    menu()
