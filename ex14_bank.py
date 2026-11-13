"""
Lab Exercise 14 : Bank Account System using OOP
Concepts        : Classes, objects, encapsulation, inheritance,
                  custom exceptions, transaction validation
"""
 
from datetime import datetime
 
 
# ---------------------------------------------------------------
# Custom exceptions - make error handling meaningful and readable
# ---------------------------------------------------------------
class BankError(Exception):
    """Base class for all banking related errors."""
 
 
class InvalidAmountError(BankError):
    """Raised when the amount is not a positive number."""
 
 
class InsufficientFundsError(BankError):
    """Raised when a withdrawal exceeds the available balance."""
 
 
class AccountInactiveError(BankError):
    """Raised when a transaction is tried on a closed account."""
 
 
# ---------------------------------------------------------------
# Class 1 : BankAccount  (encapsulation - balance is PRIVATE)
# ---------------------------------------------------------------
class BankAccount:
    MIN_BALANCE = 500          # class attribute: minimum balance to be maintained
    _next_txn_id = 1           # class attribute: auto-incrementing transaction id
 
    def __init__(self, acc_no, holder, opening_balance=0.0, pin="0000"):
        if opening_balance < 0:
            raise InvalidAmountError("Opening balance cannot be negative.")
        self.acc_no = acc_no                    # public
        self.holder = holder                    # public
        self.__balance = float(opening_balance) # private (name-mangled)
        self.__pin = str(pin)                   # private
        self.__active = True                    # private
        self.__history = []                     # private transaction log
        self._log("OPEN", opening_balance, "Account opened")
 
    # ----- private helpers (not meant to be used outside the class) -----
    def _log(self, kind, amount, note=""):
        entry = {
            "id": BankAccount._next_txn_id,
            "time": datetime.now().strftime("%H:%M:%S"),
            "type": kind,
            "amount": float(amount),
            "balance": self.__balance,
            "note": note,
        }
        BankAccount._next_txn_id += 1
        self.__history.append(entry)
 
    @staticmethod
    def _validate_amount(amount):
        """Transaction validation: amount must be a positive number."""
        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            raise InvalidAmountError(f"Amount must be a number, got {type(amount).__name__}.")
        if amount <= 0:
            raise InvalidAmountError("Amount must be greater than zero.")
 
    def _check_active(self):
        if not self.__active:
            raise AccountInactiveError("Account is closed. No transactions allowed.")
 
    def _check_pin(self, pin):
        if str(pin) != self.__pin:
            raise BankError("Incorrect PIN. Transaction denied.")
 
    # ----- public interface -----
    def deposit(self, amount):
        self._check_active()
        self._validate_amount(amount)
        self.__balance += amount
        self._log("DEPOSIT", amount)
        return self.__balance
 
    def withdraw(self, amount, pin):
        self._check_active()
        self._check_pin(pin)
        self._validate_amount(amount)
        if self.__balance - amount < self.MIN_BALANCE:
            raise InsufficientFundsError(
                f"Insufficient balance. Available: {self.__balance:.2f}, "
                f"requested: {amount:.2f}, minimum to maintain: {self.MIN_BALANCE}."
            )
        self.__balance -= amount
        self._log("WITHDRAW", amount)
        return self.__balance
 
    def get_balance(self):
        """Balance enquiry - read-only access to the private balance."""
        self._check_active()
        return self.__balance
 
    def mini_statement(self, last_n=5):
        return self.__history[-last_n:]
 
    def close(self):
        self.__active = False
 
    def _apply_internal_credit(self, amount, note):
        """Used only by the Bank class for transfers (protected by convention)."""
        self.__balance += amount
        self._log("TRANSFER-IN", amount, note)
 
    def __str__(self):
        return f"[{self.acc_no}] {self.holder:<10} | Balance: Rs. {self.__balance:>10,.2f}"
 
 
# ---------------------------------------------------------------
# Class 2 : SavingsAccount (inheritance + method extension)
# ---------------------------------------------------------------
class SavingsAccount(BankAccount):
    INTEREST_RATE = 4.0   # percent per annum
 
    def add_interest(self):
        interest = self.get_balance() * self.INTEREST_RATE / 100 / 12   # one month
        self.deposit(round(interest, 2))
        return round(interest, 2)
 
 
# ---------------------------------------------------------------
# Class 3 : Bank (manages many accounts - composition)
# ---------------------------------------------------------------
class Bank:
    def __init__(self, name):
        self.name = name
        self.__accounts = {}
 
    def open_account(self, account):
        if account.acc_no in self.__accounts:
            raise BankError("Account number already exists.")
        self.__accounts[account.acc_no] = account
 
    def find(self, acc_no):
        if acc_no not in self.__accounts:
            raise BankError(f"Account {acc_no} not found.")
        return self.__accounts[acc_no]
 
    def transfer(self, src_no, dst_no, amount, pin):
        src, dst = self.find(src_no), self.find(dst_no)
        src.withdraw(amount, pin)        # re-uses all validation rules
        # withdraw() already logged a WITHDRAW entry; credit the receiver
        dst._apply_internal_credit(amount, f"From {src_no}")
 
    def total_deposits(self):
        return sum(a.get_balance() for a in self.__accounts.values())
 
 
# ---------------------------------------------------------------
# Test harness - tries a transaction and reports PASS / BLOCKED
# ---------------------------------------------------------------
def attempt(title, action):
    try:
        result = action()
        print(f"  [OK]      {title:<42} -> {result}")
    except BankError as err:
        print(f"  [BLOCKED] {title:<42} -> {type(err).__name__}: {err}")
    except Exception as err:                       # unexpected errors
        print(f"  [ERROR]   {title:<42} -> {type(err).__name__}: {err}")
 
 
def main():
    bank = Bank("PyBank")
    a1 = SavingsAccount("SB1001", "Sriram", 10000, pin="1234")
    a2 = BankAccount("CA2002", "Rahul", 2500, pin="4321")
    bank.open_account(a1)
    bank.open_account(a2)
 
    print("=" * 78)
    print(" 1. ROUTINE TRANSACTIONS")
    print("=" * 78)
    print(a1)
    print(a2)
    attempt("Deposit 5000 into SB1001", lambda: a1.deposit(5000))
    attempt("Withdraw 2000 from SB1001 (PIN ok)", lambda: a1.withdraw(2000, "1234"))
    attempt("Balance enquiry SB1001", lambda: a1.get_balance())
    attempt("Add monthly interest to SB1001", lambda: a1.add_interest())
    attempt("Transfer 1000 SB1001 -> CA2002", lambda: bank.transfer("SB1001", "CA2002", 1000, "1234"))
    attempt("Balance enquiry CA2002", lambda: a2.get_balance())
 
    print()
    print("=" * 78)
    print(" 2. INVALID TRANSACTION TESTS")
    print("=" * 78)
    attempt("Deposit negative amount (-300)", lambda: a1.deposit(-300))
    attempt("Deposit zero", lambda: a1.deposit(0))
    attempt("Deposit text 'abc'", lambda: a1.deposit("abc"))
    attempt("Withdraw with wrong PIN", lambda: a1.withdraw(100, "0000"))
    attempt("Withdraw negative amount", lambda: a1.withdraw(-50, "1234"))
 
    print()
    print("=" * 78)
    print(" 3. INSUFFICIENT BALANCE TESTS")
    print("=" * 78)
    attempt("Withdraw 50000 from SB1001", lambda: a1.withdraw(50000, "1234"))
    attempt("Withdraw 3200 from CA2002 (min bal rule)", lambda: a2.withdraw(3200, "4321"))
    attempt("Transfer 99999 SB1001 -> CA2002", lambda: bank.transfer("SB1001", "CA2002", 99999, "1234"))
    attempt("Transfer to unknown account ZZ9999", lambda: bank.transfer("SB1001", "ZZ9999", 10, "1234"))
 
    print()
    print("=" * 78)
    print(" 4. DATA PROTECTION (ENCAPSULATION) DEMO")
    print("=" * 78)
    attempt("Direct read  a1.__balance", lambda: a1.__balance)
    attempt("Name-mangled access (not recommended)", lambda: a1._BankAccount__balance)
    print("  Safe, supported way ->  a1.get_balance() =", a1.get_balance())
 
    print()
    print("=" * 78)
    print(" 5. CLOSED ACCOUNT TEST")
    print("=" * 78)
    print(f"  Total deposits held by {bank.name}: Rs. {bank.total_deposits():,.2f}")
    a2.close()
    attempt("Deposit into closed account CA2002", lambda: a2.deposit(100))
 
    print()
    print("=" * 78)
    print(" 6. MINI STATEMENT OF SB1001")
    print("=" * 78)
    print(f"  {'ID':<4}{'TYPE':<14}{'AMOUNT':>12}{'BALANCE':>14}  NOTE")
    for t in a1.mini_statement(10):
        print(f"  {t['id']:<4}{t['type']:<14}{t['amount']:>12,.2f}{t['balance']:>14,.2f}  {t['note']}")
 
 
 
if __name__ == "__main__":
    main()
