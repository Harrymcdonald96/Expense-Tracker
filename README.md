# Expense Tracker Application

## GIF Preview
![Expense Tracker Giph](screenshots/giphy (2).mp4)

## Demo Video
[Watch the demo video](https://www.youtube.com/watch?v=GqISyq6MJ2k)


## Overview

The Expense Tracker is a powerful tool designed to help users manage their personal finances by tracking daily expenses across various categories and currencies. It offers features such as currency conversion, expense categorization, and summarization of expenses over different periods.

## Features

- **Currency Conversion**: Convert expenses between different currencies using real-time exchange rates.
- **Expense Categorization**: Organize expenses into categories such as Food, Transport, and Entertainment.
- **Dynamic Summaries**: View summarized data of expenses on a daily, weekly, or monthly basis.
- **Persistence**: Expenses are saved and loaded from a local JSON file, ensuring data persistence across sessions.

- **Data Validation**: Robust input validation to ensure data integrity.

## Key Functions

- `get_exchange_rate(from_currency, to_currency)`: Fetches the real-time exchange rate between two currencies from an external API.
- `convert_currency(amount, from_currency, to_currency)`: Converts a specified amount from one currency to another.
- `load_expenses()`: Loads expenses from a JSON file into the application.
- `save_expenses()`: Saves current expenses into a JSON file.
- `log_expense()`: Interface to add a new expense, with input validation.
- `choose_frequency()`: Allows the user to select the frequency of expense logging.
- `choose_currency()`: Allows the user to select the currency for logging the expense.
- `choose_category()`: Allows the user to choose or add a new category for the expense.
- `group_expenses_by(expenses, period, frequency)`: Organizes expenses into groups based on the specified period.
- `currency_symbol(currency)`: Provides the currency symbol for display purposes.
- `display_spending_summary(expenses)`: Displays the spending summary for a given period.
- `display_summary()`: Provides a menu to choose the period for which the spending summary is displayed.
- `main_menu()`: Main menu of the application for navigating through the functionalities.

## Program Flow

- The program starts by loading any existing expenses from the JSON file.
- The main menu offers options to log a new expense, view expense summaries, or exit the program.
- When logging an expense, the user can specify the amount, currency, category, and whether to convert the amount to a different currency.
- Summaries can be viewed based on the day, week, or month, and they display the total spent in each category and currency.

## Running the Expense Tracker

To run the Expense Tracker, execute the following command from the terminal:
`python path_to_your_script.py`

# Entry point

- if **name** == "**main**":
  main_menu()
