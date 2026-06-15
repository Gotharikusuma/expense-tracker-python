import json
import os
from datetime import datetime
import matplotlib.pyplot as plt


# ---------------- FILE NAME ----------------
# Fixed file name for data persistence
FILE_NAME = "expenses.json"


# ---------------- LOAD EXPENSES ----------------
# Load existing expense records from JSON file
def load_expenses():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


# ---------------- SAVE EXPENSES ----------------
def save_expenses(expenses):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=4)


# ---------------- ADD EXPENSE ----------------
# Get expense amount from user
def add_expense(expenses):
    try:
        amount = float(input("Enter expense amount: ").strip()) # Get expense amount from user

        if amount <= 0:    # Validate amount
            print("Amount must be greater than 0.")
            return
        
        # Get expense category
        category = input(
            "Enter category: "
        ).strip().title()

        # Get date from user or use today's date
        date = input(
            "Enter date (YYYY-MM-DD) or press Enter for today: "
        ).strip()

        # Use current date if no date is entered
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        else:
            try:
                date_obj = datetime.strptime(date, "%Y-%m-%d")

                # Always save in YYYY-MM-DD format
                date = date_obj.strftime("%Y-%m-%d")

            except ValueError:
                print("Invalid date format! Please use YYYY-MM-DD")
                return

        # Add expense record to the list
        expenses.append({
            "amount": amount,
            "category": category,
            "date": date
        })

        # Save updated expense list to file
        save_expenses(expenses)
        print(f"Expense saved in file: {FILE_NAME}")

    except ValueError:
        print("Invalid amount!")


# ---------------- DISPLAY TABLE ----------------
def display_expenses(expenses):
    # Check if there are any expense records
    if not expenses:
        print("No expenses found.")
        return

    # Display table header
    print("\n" + "=" * 70)
    print(f"{'No':<5}{'Amount':<15}{'Category':<25}{'Date':<15}")
    print("=" * 70)

    # Display each expense record with serial number
    for i, exp in enumerate(expenses, start=1):
        print(
            f"{i:<5}"
            f"{exp['amount']:<14.2f}"
            f"{exp['category']:<25}"
            f"{exp['date']:<15}"
        )

    # Display table footer
    print("=" * 70)


# ---------------- SUMMARY ----------------
def view_summary(expenses):
    # Check if expense records are available
    if not expenses:
        print("No data found.")
        return
    
    # Calculate total overall spending
    total = sum(exp["amount"] for exp in expenses)

    print("\n===== EXPENSE SUMMARY =====")
    print(f"Total Overall Spending: {total:.2f}")

    # Category-wise Summary
    category_totals = {}
    for exp in expenses:
        category = exp["category"]
        category_totals[category] = (
            category_totals.get(category, 0) + exp["amount"]
        )

    # Display spending for each category
    print("\nCategory-wise Spending:")
    for category, amount in category_totals.items():
        print(f"{category}: {amount:.2f}")

    # Display available categories
    print("\nAvailable Categories:")
    for category in category_totals:
        print(f"- {category}")

    # Search category
    while True:
        search_category = input(
            "\nEnter category to check spending "
            "(or press Enter to skip): "
        ).strip().title()

        if not search_category:
            break

        if search_category in category_totals:
            print(
                f"Total spent on {search_category}: "
                f"{category_totals[search_category]:.2f}"
            )
            break
        else:
            print(
                "Category not found! "
                "Please enter a valid category."
            )

    # Daily Summary
    daily_totals = {}
    for exp in expenses:
        daily_totals[exp["date"]] = (
            daily_totals.get(exp["date"], 0) + exp["amount"]
        )

    # Calculate daily spending totals
    print("\nDaily Spending:")
    for date, amount in sorted(daily_totals.items()):
        print(f"{date}: {amount:.2f}")

    # Monthly Summary
    monthly_totals = {}
    for exp in expenses:
        month = exp["date"][:7]
        monthly_totals[month] = (
            monthly_totals.get(month, 0) + exp["amount"]
        )

    print("\nMonthly Spending:")
    for month, amount in sorted(monthly_totals.items()):
        print(f"{month}: {amount:.2f}")

# ---------------- DELETE ----------------
def delete_expense(expenses):
    # Check if there are any expenses to delete
    if not expenses:
        print("No expenses to delete.")
        return

    # Display all expenses with serial numbers
    display_expenses(expenses)

    try:
        index = int(input("Enter number to delete: ")) - 1  # Get expense number from user

        if 0 <= index < len(expenses):    # Validate selected expense number
            removed = expenses.pop(index)   # Remove the selected expense
            save_expenses(expenses)
            print(f"Deleted {removed['amount']}")
        else:
            print("Invalid choice!")

    except ValueError:
        print("Invalid input!")

# ---------------- UPDATE EXPENSE ----------------
def update_expense(expenses):
    # Check if there are any expenses to update
    if not expenses:
        print("No expenses available.")
        return

    display_expenses(expenses)  # Display all expenses with serial numbers

    try:
        index = int(input("Enter expense number to update: ")) - 1   # Get expense number to update

        if 0 <= index < len(expenses):  # Get expense number to update
            exp = expenses[index]

            print("\nLeave blank to keep current value.")

            amount = input(
                f"Amount (current: {exp['amount']}): "    # Get updated values from user
            ).strip()

            category = input(
                f"Category (current: {exp['category']}): "
            ).strip()

            date = input(
                f"Date (current: {exp['date']}): "
            ).strip()

            if amount:                # Update amount if user enters a new value
                exp["amount"] = float(amount)

            if category:              # Update category if user enters a new value
                exp["category"] = category.title()

            if date:                  # Validate and update date
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                    exp["date"] = date
                except ValueError:
                    print("Invalid date format!")
                    return

            save_expenses(expenses)   # Save updated expenses to file
            print("Expense updated successfully!")

        else:
            print("Invalid expense number!")

    except ValueError:
        print("Invalid input!")

# ---------------- CHART ----------------
def show_chart(expenses):
    if not expenses:  # Check if expense records are available
        print("No data available.")
        return

    # Calculate daily spending totals
    daily_totals = {}

    for exp in expenses:
        date = exp["date"]
        daily_totals[date] = (
            daily_totals.get(date, 0) + exp["amount"]
        )

    # Sort dates
    dates = sorted(daily_totals.keys())
    amounts = [daily_totals[date] for date in dates]

    plt.plot(             # Plot daily spending trend using a line chart
        dates,
        amounts,
        marker="o"
    )

    # Plot daily spending trend using a line chart
    plt.title("Daily Expense Trend") 
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.grid(True)               # Display grid for better readability

    plt.xticks(rotation=45)      # Display grid for better readability
    plt.tight_layout()           # Adjust layout for proper spacing
    plt.show()                   # Display the chart

# ---------------- MAIN ----------------
def main():
    expenses = load_expenses()

    print("\n===== EXPENSE TRACKER =====")
    print(f"File used: {FILE_NAME}")
    print(f"Loaded {len(expenses)} records")

    while True:
        print("\n1. Add Expense")
        print("2. View Summary")
        print("3. View All")
        print("4. Delete")
        print("5. Update")
        print("6. Chart")
        print("7. Exit\n")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_summary(expenses)
        elif choice == "3":
            display_expenses(expenses)
        elif choice == "4":
            delete_expense(expenses)
        elif choice == "5":
            update_expense(expenses)
        elif choice == "6":
            show_chart(expenses)
        elif choice == "7":
            print("Exit successful!")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()