import os
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime

class ExpenseTracker:
    def __init__(self, file_name="expenses.json"):
        self.file_name = file_name
        self.expenses = self.load_expenses()

    def load_expenses(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                return json.load(file)
        return []

    def save_expenses(self):
        with open(self.file_name, 'w') as file:
            json.dump(self.expenses, file, indent=4)

    def add_expense(self, amount, category, date):
        self.expenses.append({
            "amount": amount,
            "category": category,
            "date": date
        })
        self.save_expenses()

    def view_expenses(self):
        for expense in self.expenses:
            print(f"Date: {expense['date']}, Category: {expense['category']}, Amount: ${expense['amount']}")

    def generate_report(self):
        categories = {}
        for expense in self.expenses:
            category = expense['category']
            amount = float(expense['amount'])
            categories[category] = categories.get(category, 0) + amount

        # Visualization
        plt.figure(figsize=(8, 6))
        plt.bar(categories.keys(), categories.values(), color='skyblue')
        plt.xlabel('Categories')
        plt.ylabel('Amount ($)')
        plt.title('Expenses by Category')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('report.png')  # Save plot to a file
        print("Report saved as 'report.png'")




if __name__ == "__main__":
    tracker = ExpenseTracker()

    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Generate Report")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            amount = input("Enter amount: ")
            category = input("Enter category: ")
            date = input("Enter date (YYYY-MM-DD): ")
            try:
                datetime.strptime(date, "%Y-%m-%d")
                tracker.add_expense(amount, category, date)
                print("Expense added successfully!")
            except ValueError:
                print("Invalid date format!")

        elif choice == "2":
            tracker.view_expenses()

        elif choice == "3":
            tracker.generate_report()

        elif choice == "4":
            break

        else:
            print("Invalid choice, please try again!")
