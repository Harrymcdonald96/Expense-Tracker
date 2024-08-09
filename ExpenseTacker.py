import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime, date
from collections import defaultdict

# Load environment variables from .env file
load_dotenv()

def get_exchange_rate(from_currency, to_currency):
    """Fetch the exchange rate from the API using from_currency and to_currency."""
    # Retrieve API key from environment
    api_key = os.getenv('EXCHANGE_RATE_API_KEY')
    # Construct the API request URL
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}"
    # Send request and receive response
    response = requests.get(url)
    data = response.json()
    # Check for successful API call
    if data['result'] == 'success':
        return data['conversion_rate']
    else:
        raise Exception("Failed to fetch exchange rates")

def convert_currency(amount, from_currency, to_currency):
    """Convert an amount from one currency to another using the exchange rate."""
    rate = get_exchange_rate(from_currency, to_currency)
    return amount * rate

def load_expenses():
    """Load expenses from a JSON file, converting date strings to date objects."""
    try:
        with open('expenses.json', 'r') as file:
            data = json.load(file)
            # Convert date strings to datetime.date objects for each expense
            for expense in data:
                if isinstance(expense['date'], str):
                    expense['date'] = datetime.strptime(expense['date'], '%Y-%m-%d').date()
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return an empty list if there's an error

expenses = load_expenses()

def save_expenses():
    """Save the current list of expenses to a JSON file."""
    with open('expenses.json', 'w') as file:
        # Convert datetime.date objects back to strings
        json.dump(expenses, file, indent=4, default=lambda x: x.strftime('%Y-%m-%d') if isinstance(x, date) else str(x))

def log_expense():
    """Collect expense data from the user and add it to the expense list."""
    print("\n--- Log New Expense ---")
    today = date.today()
    print(f"Date of Expense: {today.strftime('%Y-%m-%d')}")
    currency = choose_currency()

    # Validate and collect the expense amount
    while True:
        try:
            amount = float(input(f"Enter the expense amount ({currency}): "))
            if amount <= 0:
                print("Amount must be positive. Please enter a positive number.")
            else:
                break
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

    # Ask for currency conversion
    convert = input("Do you want to convert this amount to another currency? (yes/no): ").lower()
    while convert not in ['yes', 'no']:
        print("Invalid response. Please type 'yes' or 'no'.")
        convert = input("Do you want to convert this amount to another currency? (yes/no): ").lower()

    if convert == 'yes':
        to_currency = input("Enter the currency to convert to (USD, EUR, etc.): ")
        while to_currency not in ['USD', 'EUR', 'GBP', 'JPY']:
            print("Invalid currency. Please enter one of the supported currencies (USD, EUR, GBP, JPY).")
            to_currency = input("Enter the currency to convert to (USD, EUR, etc.): ")
        try:
            amount = convert_currency(amount, currency, to_currency)
            currency = to_currency
            print(f"Converted amount: {amount:.2f} {currency}")
        except Exception as e:
            print(str(e))
            return

    category = choose_category()
    frequency = choose_frequency()

    # Append the new expense to the list
    expenses.append({
        'date': today.isoformat(),
        'amount': amount,
        'currency': currency,
        'category': category,
        'frequency': frequency,
    })
    print("Expense added successfully!")
    save_expenses()

def choose_frequency():
    """Let the user choose the frequency of the expense."""
    frequencies = ['daily', 'weekly', 'monthly']
    print("Choose the frequency of the expense:")
    for i, freq in enumerate(frequencies, 1):
        print(f"{i}. {freq.title()}")
    while True:
        choice = input("Enter your choice: ")
        if choice.isdigit() and 1 <= int(choice) <= len(frequencies):
            return frequencies[int(choice) - 1]
        else:
            print("Invalid option, please choose again.")

def choose_currency():
    """Let the user select a currency for the expense."""
    currencies = ['USD', 'EUR', 'GBP', 'JPY']
    print("Choose a currency:")
    for i, currency in enumerate(currencies, 1):
        print(f"{i}. {currency}")
    while True:
        choice = input("Enter your choice: ")
        if choice.isdigit() and 1 <= int(choice) <= len(currencies):
            return currencies[int(choice) - 1]
        else:
            print("Invalid option, please choose a valid number between 1 and", len(currencies))

def choose_category():
    """Allow the user to select or add a new category for the expense."""
    categories = ['Food', 'Transport', 'Entertainment']
    print("Choose a category:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")
    print(f"{len(categories) + 1}. Add new category")
    while True:
        choice = input("Enter your choice: ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(categories):
                return categories[choice - 1]
            elif choice == len(categories) + 1:
                new_category = input("Enter the name of the new category: ")
                categories.append(new_category)
                print(f"New category '{new_category}' added.")
                return new_category
            else:
                print("Invalid option, please choose again.")
        except ValueError:
            print("Please enter a number.")

def group_expenses_by(expenses, period, frequency):
    """Organize expenses into groups based on the specified period and frequency."""
    grouped = defaultdict(list)
    for expense in expenses:
        if expense['frequency'] == frequency:
            # Convert string dates to datetime.date objects before formatting
            expense_date = expense['date']
            if isinstance(expense_date, str):
                expense_date = datetime.strptime(expense_date, '%Y-%m-%d').date()
            if period == 'day':
                key = expense_date
            elif period == 'week':
                key = expense_date.strftime('%Y-W%U')
            elif period == 'month':
                key = expense_date.strftime('%Y-%m')
            grouped[key].append(expense)
    return grouped

def currency_symbol(currency):
    """Return the symbol for the currency or the currency code in uppercase if not predefined."""
    symbols = {'USD': '$', 'GBP': '£', 'EUR': '€', 'JPY': '¥'}
    return symbols.get(currency.upper(), currency.upper())

def display_spending_summary(expenses):
    """Display a summary of spending for the given expenses on a particular day, week, or month."""
    if not expenses:
        print("No expenses logged.")
        return
    currency_totals = defaultdict(lambda: defaultdict(float))
    for exp in expenses:
        currency_totals[exp['currency']][exp['category']] += exp['amount']
        currency_totals[exp['currency']]['Total'] += exp['amount']
    for currency, amounts in currency_totals.items():
        expense_date = expenses[0]['date']
        formatted_date = expense_date.strftime('%Y-%m-%d') if isinstance(expense_date, date) else expense_date
        symbol = currency_symbol(currency)
        print(f"\nDay: {formatted_date}")
        print(f"(Total spent {currency.upper()}): {symbol}{amounts['Total']:.2f}")
        for category, amount in amounts.items():
            if category != 'Total':
                print(f"{category}: {symbol}{amount:.2f}")

def display_summary():
    """Prompt the user to choose the frequency of the summary (daily, weekly, monthly) and display the corresponding summary."""
    print("\n--- Overall Spending Summary ---")
    print("Choose the frequency for the summary:")
    print("1. Daily")
    print("2. Weekly")
    print("3. Monthly")
    freq_choice = input("Enter your choice: ")
    freq_map = {'1': 'daily', '2': 'weekly', '3': 'monthly'}
    frequency = freq_map.get(freq_choice, 'daily')
    if frequency == 'daily':
        print("\n--- Daily Summary ---")
        for day, day_expenses in group_expenses_by(expenses, 'day', frequency).items():
            display_spending_summary(day_expenses)
    elif frequency == 'weekly':
        print("\n--- Weekly Summary ---")
        for week, week_expenses in group_expenses_by(expenses, 'week', frequency).items():
            display_spending_summary(week_expenses)
    elif frequency == 'monthly':
        print("\n--- Monthly Summary ---")
        for month, month_expenses in group_expenses_by(expenses, 'month', frequency).items():
            display_spending_summary(month_expenses)
    print("\nReturn to Main Menu...")

def main_menu():
    """Main menu for navigating through the application's functionalities."""
    while True:
        print("\n--- Main Menu ---")
        print("1. Log an Expense")
        print("2. View Expense Summary")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            log_expense()
        elif choice == '2':
            display_summary()
        elif choice == '3':
            print("Thank you for using the Expense Tracker. Goodbye!")
            save_expenses()
            break
        else:
            print("Invalid option, please choose again.")

# The main entry point for the application
if __name__ == "__main__":
    main_menu()
