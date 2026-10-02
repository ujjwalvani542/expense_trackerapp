import csv
import os

CSV_FILE = "expenses.csv"
FIELDNAMES = ["DATE", "CATEGORY", "AMOUNT"]


def load_expenses():
    """Loads expenses from CSV if the file exists."""
    expenses = []
    if os.path.exists(CSV_FILE):
        
    
            with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    expenses.append({
                        "DATE": row["DATE"],
                        "CATEGORY": row["CATEGORY"],
                        "AMOUNT": float(row["AMOUNT"])
                    })
       
    return expenses


def save_expenses(expenses):
    """Overwrites CSV with the current list of expenses."""
    try:
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(expenses)
    except Exception as e:
        print(f"Error saving to CSV: {e}")


# Initialize data on startup
expense_list = load_expenses()

print("== WELCOME TO EXPENSE TRACKER ==")
print(f"Loaded {len(expense_list)} saved record(s) from '{CSV_FILE}'.")

while True:
    print("\n== MENU ==")
    print("1. ADD EXPENSE")
    print("2. VIEW ALL EXPENSES")
    print("3. DELETE AN EXPENSE")
    print("4. CATEGORY BREAKDOWN & BUDGET ALERT")
    print("5. EXIT")

    choice = input("PLEASE ENTER YOUR CHOICE (1-5): ")

    # 1. ADD EXPENSE
    if choice == '1':
        date = input("ENTER THE DATE (YYYY-MM-DD): ")
        category = input("ENTER CATEGORY (e.g., Food, Travel, Rent): ")
        try:
            amount = float(input("ENTER THE AMOUNT (₹): "))
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
        except ValueError:
            print("Invalid input! Please enter a numerical value for amount.")
            continue

        new_expense = {
            "DATE": date,
            "CATEGORY": category,
            "AMOUNT": amount
        }
        
        expense_list.append(new_expense)
        save_expenses(expense_list)
        print("=== EXPENSE ADDED & SAVED TO CSV ===")

    # 2. VIEW ALL EXPENSES
    elif choice == '2':
        if not expense_list:
            print("No expenses recorded yet.")
        else:
            print("\n--- YOUR RECORDED EXPENSES ---")
            total_spent = 0.0
            for idx, item in enumerate(expense_list, start=1):
                print(f"#{idx} | Date: {item['DATE']} | Category: {item['CATEGORY']} | Amount: ₹{item['AMOUNT']:.2f}")
                total_spent += item['AMOUNT']
            print(f"Total Expenditure: ₹{total_spent:.2f}")

    # 3. DELETE AN EXPENSE
    elif choice == '3':
        if not expense_list:
            print("No expenses available to delete.")
        else:
            for idx, item in enumerate(expense_list, start=1):
                print(f"#{idx}: {item['CATEGORY']} - ₹{item['AMOUNT']:.2f} ({item['DATE']})")
            
            try:
                del_idx = int(input("ENTER THE EXPENSE NUMBER TO DELETE: "))
                if 1 <= del_idx <= len(expense_list):
                    removed = expense_list.pop(del_idx - 1)
                    save_expenses(expense_list)
                    print(f"=== EXPENSE #{del_idx} ({removed['CATEGORY']} - ₹{removed['AMOUNT']:.2f}) DELETED & FILE UPDATED ===")
                else:
                    print("Invalid expense number.")
            except ValueError:
                print("Please enter a valid integer number.")

    # 4. CATEGORY BREAKDOWN & BUDGET ALERT
    elif choice == '4':
        if not expense_list:
            print("Not enough data. Add some expenses first.")
        else:
            category_totals = {}
            grand_total = 0.0

            for item in expense_list:
                cat = item['CATEGORY']
                amt = item['AMOUNT']
                category_totals[cat] = category_totals.get(cat, 0.0) + amt
                grand_total += amt

            print("\n--- SPENDING ANALYTICS & ALERTS ---")
            print(f"Grand Total: ₹{grand_total:.2f}\n")

            for cat, total in category_totals.items():
                percentage = (total / grand_total) * 100
                print(f"• {cat}: ₹{total:.2f} ({percentage:.1f}%)")
                if percentage > 40 and len(category_totals) > 1:
                    print(f"  [!] High Spend Alert: {cat} accounts for more than 40% of your budget.")

    # 5. EXIT
    elif choice == '5':
        print("All data is safely saved in expenses.csv. Goodbye!")
        break

    else:
        print("Invalid choice! Please select a valid option from 1 to 5.")
