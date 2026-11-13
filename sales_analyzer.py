"""
Sales Data Analyzer  -  Python Programming (Unit 3 Mini Project)
Data structures used
--------------------
products : list  -> ordered list of product names
sales    : dict  -> {product_name: {"price": float, "quantity": int}}
"""
class SalesAnalyzer:
    def __init__(self):
        self.products = []   # list of names
        self.sales = {}      # dict of dicts
    # ---------------------------------------------------------------
    # 1. Adding / updating records
    # ---------------------------------------------------------------
    def add_product(self, name, price, quantity=0):
        name = name.strip().title()
        if not name:
            raise ValueError("Product name cannot be empty.")
        if name in self.sales:
            raise ValueError(f"Product '{name}' already exists.")
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.products.append(name)
        self.sales[name] = {"price": float(price), "quantity": int(quantity)}
    def record_sale(self, name, quantity):
        """Add units sold to an existing product."""
        name = name.strip().title()
        if name not in self.sales:
            raise KeyError(f"Product '{name}' not found.")
        if quantity <= 0:
            raise ValueError("Quantity sold must be positive.")
        self.sales[name]["quantity"] += int(quantity)
    def set_quantity(self, name, quantity):
        """Overwrite the quantity (used to correct a wrong entry)."""
        name = name.strip().title()
        if name not in self.sales:
            raise KeyError(f"Product '{name}' not found.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.sales[name]["quantity"] = int(quantity)
    def update_price(self, name, price):
        name = name.strip().title()
        if name not in self.sales:
            raise KeyError(f"Product '{name}' not found.")
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        self.sales[name]["price"] = float(price)
    # ---------------------------------------------------------------
    # 2. Calculations
    # ---------------------------------------------------------------
    def revenue(self, name):
        item = self.sales[name]
        return item["price"] * item["quantity"]
    def revenue_by_product(self):
        return {name: self.revenue(name) for name in self.products}
    def total_sales(self):
        return sum(self.revenue_by_product().values())
    def total_units(self):
        return sum(item["quantity"] for item in self.sales.values())
    def best_selling_by_quantity(self):
        """Return list of product(s) with the highest units sold (handles ties)."""
        if not self.products:
            return []
        top = max(self.sales[p]["quantity"] for p in self.products)
        return [p for p in self.products if self.sales[p]["quantity"] == top]
    def best_by_revenue(self):
        if not self.products:
            return []
        rev = self.revenue_by_product()
        top = max(rev.values())
        return [p for p in self.products if rev[p] == top]
    def ranking(self):
        """Products sorted by revenue, highest first."""
        rev = self.revenue_by_product()
        return sorted(rev.items(), key=lambda kv: kv[1], reverse=True)
    def share_percent(self, name):
        total = self.total_sales()
        return round(self.revenue(name) / total * 100, 2) if total else 0.0
    def compare(self, a, b):
        a, b = a.strip().title(), b.strip().title()
        for n in (a, b):
            if n not in self.sales:
                raise KeyError(f"Product '{n}' not found.")
        ra, rb = self.revenue(a), self.revenue(b)
        if ra == rb:
            verdict = f"{a} and {b} earned the same revenue."
        else:
            win, lose = (a, b) if ra > rb else (b, a)
            diff = abs(ra - rb)
            verdict = f"{win} out-earned {lose} by Rs. {diff:,.2f}."
        return verdict
    def performance_label(self, name):
        """Top / Average / Low based on comparison with mean revenue."""
        if not self.products:
            return "N/A"
        mean = self.total_sales() / len(self.products)
        r = self.revenue(name)
        if r >= 1.25 * mean:
            return "Top performer"
        if r < 0.75 * mean:
            return "Low performer"
        return "Average"
    # ---------------------------------------------------------------
    # 3. Display
    # ---------------------------------------------------------------
    def display_table(self):
        if not self.products:
            print("No products recorded yet.")
            return
        w = max(len("Product"), max(len(p) for p in self.products)) + 2
        head = f"{'Product':<{w}}{'Price':>10}{'Qty':>7}{'Revenue':>14}{'Share':>9}"
        print(head)
        print("-" * len(head))
        for p in self.products:
            item = self.sales[p]
            print(f"{p:<{w}}{item['price']:>10,.2f}{item['quantity']:>7}"
                  f"{self.revenue(p):>14,.2f}{self.share_percent(p):>8.2f}%")
        print("-" * len(head))
        print(f"{'TOTAL':<{w}}{'':>10}{self.total_units():>7}{self.total_sales():>14,.2f}{'100.00%':>9}")
    def summary(self):
        if not self.products:
            print("No data to summarise.")
            return
        self.display_table()
        print()
        print("Highest selling (units)  :", ", ".join(self.best_selling_by_quantity()),
              f"({self.sales[self.best_selling_by_quantity()[0]]['quantity']} units)")
        print("Highest revenue          :", ", ".join(self.best_by_revenue()),
              f"(Rs. {self.revenue(self.best_by_revenue()[0]):,.2f})")
        print("\nRanking by revenue:")
        for rank, (p, r) in enumerate(self.ranking(), start=1):
            print(f"  {rank}. {p:<14} Rs. {r:>12,.2f}   [{self.performance_label(p)}]")
# -------------------------------------------------------------------
# Interactive menu
# -------------------------------------------------------------------
def menu():
    app = SalesAnalyzer()
    options = """
===== SALES DATA ANALYZER =====
1. Add product
2. Record sale (add units)
3. Correct quantity
4. Update price
5. Show sales table
6. Full summary
7. Compare two products
8. Exit
"""
    while True:
        print(options)
        choice = input("Enter choice: ").strip()
        try:
            if choice == "1":
                app.add_product(input("Name: "), float(input("Price: ")), int(input("Qty sold: ")))
            elif choice == "2":
                app.record_sale(input("Name: "), int(input("Units sold: ")))
            elif choice == "3":
                app.set_quantity(input("Name: "), int(input("New quantity: ")))
            elif choice == "4":
                app.update_price(input("Name: "), float(input("New price: ")))
            elif choice == "5":
                app.display_table()
            elif choice == "6":
                app.summary()
            elif choice == "7":
                print(app.compare(input("First product: "), input("Second product: ")))
            elif choice == "8":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
        except (ValueError, KeyError) as err:
            print("Error:", err)
if __name__ == "__main__":
    menu()
