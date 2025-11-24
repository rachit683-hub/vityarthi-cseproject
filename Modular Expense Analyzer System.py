import os
from datetime import datetime
# --- System Configuration ---
# Directory where data is stored
DATA_DIR = 'data'
# The name of the main expense data file
CSV_FILE_NAME = 'expenses.csv'
# Full path to the data file
CSV_FILE_PATH = os.path.join(DATA_DIR, CSV_FILE_NAME)

# --- Data Structure and Categories ---
# The columns required in the CSV file
CSV_COLUMNS = ['Date', 'Category', 'Amount']

# Predefined categories for user selection
CATEGORIES = {
    1: 'Groceries',
    2: 'Rent/Mortgage',
    3: 'Utilities',
    4: 'Transportation',
    5: 'Entertainment',
    6: 'Income',         # Used for tracking deposits/income
    7: 'Other'
}

# --- Initial Data Setup ---
# Initialize the CSV file with headers if it doesn't exist
def setup_data_file():
    """Creates the data directory and the CSV file with headers if they don't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CSV_FILE_PATH):
        try:
            with open(CSV_FILE_PATH, 'w') as f:
                f.write(','.join(CSV_COLUMNS) + '\n')
            print(f"Created initial data file at: {CSV_FILE_PATH}")
            return True # Return success status
        except IOError as e:
            print(f"Error creating file: {e}")
            return False # Return failure status
    return True

# Run setup when imported (Kept this for the original file's behavior,
# but will manage it in main_app.py for better control)
setup_data_file()
import pandas as pd

def load_data():
    """
    Loads expense data from the CSV file. (Error Handling Strategy: File Not Found)

    Returns:n        pd.DataFrame: DataFrame of expense records.
    """
    try:
        # Load the CSV, setting 'Date' as index and parsing dates
        df = pd.read_csv(
            CSV_FILE_PATH,
            index_col='Date',
            parse_dates=True,
            header=0
        )

        # Validation: Check if the required columns are present
        # Check against CSV_COLUMNS[1:] because 'Date' is now the index
        if not all(col in df.columns for col in CSV_COLUMNS[1:]):
            print("Error: CSV file is missing required columns (Category, Amount).")
            # If the header exists but is wrong, return empty to prevent errors
            return pd.DataFrame()

        # Basic cleanup: remove rows with any missing values
        df.dropna(inplace=True);
        return df

    except FileNotFoundError:
        # If file not found, call setup_data_file() and try to load an empty DataFrame
        print(f"Data file not found at {CSV_FILE_PATH}. Attempting to create it...")
        if setup_data_file():
             print("File created successfully. Returning empty DataFrame.")
        else:
             print("File creation failed. Returning empty DataFrame.")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        print("CSV file is empty or only contains headers. Returning empty DataFrame.")
        return pd.DataFrame()
    except Exception as e:
        print(f"An error occurred while loading data: {e}")
        return pd.DataFrame()


def save_expense(date, category, amount):
    """
    Appends a new expense record to the CSV file. (Reliability NFR)

    Args:
        date (str): Date of the expense (YYYY-MM-DD).
        category (str): Category of the expense.
        amount (float): Amount of the expense.
    """
    # Create a Pandas Series for the new entry
    new_entry = pd.Series({'Date': date, 'Category': category, 'Amount': amount})

    # Format the data for appending
    data_to_save = new_entry.to_frame().T
    # This date formatting is slightly redundant if date_str is already 'YYYY-MM-DD',
    # but safe to keep for consistency with load_data index parsing.
    data_to_save['Date'] = pd.to_datetime(data_to_save['Date']).dt.strftime('%Y-%m-%d')

    try:
        # Append to CSV without header and index (Reliability)
        data_to_save.to_csv(
            CSV_FILE_PATH,
            mode='a',
            header=False,
            index=False
        )
        print("\n✅ Expense recorded successfully.")
    except Exception as e:
        print(f"Error saving data: {e}")

import pandas as pd
import numpy as np

def calculate_category_spending(df: pd.DataFrame):
    """
    Aggregates total spending per category using Pandas groupby.

    Args:
        df (pd.DataFrame): Expense DataFrame.

    Returns:
        pd.Series: Total spending per category.
    """
    if df.empty:
        return pd.Series()

    # Use df.copy() for safety since we're modifying the column
    temp_df = df.copy()
    temp_df['Amount'] = pd.to_numeric(temp_df['Amount'], errors='coerce').fillna(0)

    # Separate expenses (negative amounts) from income (positive amounts)
    # Retain 'Category' column for grouping
    expense_df = temp_df[temp_df['Amount'] < 0].copy()

    if expense_df.empty:
        return pd.Series()

    # Group by Category and sum the absolute values of expenses
    category_totals = expense_df.groupby('Category')['Amount'].sum().abs()

    return category_totals


def calculate_monthly_trends(df: pd.DataFrame):
    """
    Calculates total monthly spending (resampling) and separates expense/income trends.

    Args:
        df (pd.DataFrame): Expense DataFrame.

    Returns:
        pd.DataFrame: Monthly total expenses and income.
    """
    if df.empty:
        return pd.DataFrame()

    # Use df.copy() for safety since we might set a new index
    temp_df = df.copy()

    # Ensure Date is the index and it's a DatetimeIndex
    if not isinstance(temp_df.index, pd.DatetimeIndex):
        # Assuming 'Date' column exists if index is not DatetimeIndex
        if 'Date' in temp_df.columns:
            temp_df = temp_df.set_index('Date')
        else:
            print("Error: DataFrame index is not DatetimeIndex and 'Date' column is missing.")
            return pd.DataFrame()

    # Resample the DataFrame monthly ('M'), summing the amounts
    # Separate Expense (negative) and Income (positive)
    temp_df['Amount'] = pd.to_numeric(temp_df['Amount'], errors='coerce').fillna(0)

    monthly_expenses = temp_df[temp_df['Amount'] < 0]['Amount'].resample('M').sum().abs().fillna(0)
    monthly_income = temp_df[temp_df['Amount'] > 0]['Amount'].resample('M').sum().fillna(0)

    # Combine into one DataFrame for easy plotting
    monthly_summary = pd.DataFrame({
        'Expenses': monthly_expenses,
        'Income': monthly_income
    })

    return monthly_summary
import pandas as pd
import numpy as np

def get_summary_statistics(df: pd.DataFrame):
    """
    Calculates key statistical measures for expenses using NumPy. (Performance NFR)

    Args:
        df (pd.DataFrame): Expense DataFrame.

    Returns:
        dict: A dictionary of summary statistics.
    """
    if df.empty:
        return {}

    # Use a copy to ensure 'Amount' column is clean for analysis
    temp_df = df.copy()
    temp_df['Amount'] = pd.to_numeric(temp_df['Amount'], errors='coerce').fillna(0)

    # Isolate expenses (negative values) and convert to absolute values
    expenses = temp_df[temp_df['Amount'] < 0]['Amount'].abs().values

    if len(expenses) == 0:
        return {"Note": "No expense records found for statistical analysis."}

    # Use NumPy for fast, vectorized statistical calculations (Performance NFR)
    stats = {
        'Total Expenses': np.sum(expenses),
        'Number of Transactions': len(expenses),
        'Mean Daily Expense': np.mean(expenses),
        'Median Daily Expense': np.median(expenses),
        'Std. Dev. of Expense': np.std(expenses), # Volatility of spending
        '75th Percentile': np.percentile(expenses, 75)
    }

    return stats
import matplotlib.pyplot as plt
import pandas as pd

def plot_category_spending(category_totals: pd.Series):
    """
    Generates a bar chart of spending by category. (Usability NFR)
    """
    if category_totals.empty:
        print("No category data to plot.")
        return

    plt.figure(figsize=(10, 6))

    # Bar Chart (Matplotlib)
    category_totals.sort_values(ascending=False).plot(
        kind='bar',
        color='skyblue'
    )

    # Formatting (Usability NFR)
    plt.title('Total Spending by Category')
    plt.xlabel('Category')
    plt.ylabel('Total Amount Spent ($)')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    #

#[Image of a bar chart showing spending by category]
 # Diagram added for instructive value


def plot_monthly_trends(monthly_summary: pd.DataFrame):
    """
    Generates a line chart showing monthly expenses and income.
    """
    if monthly_summary.empty or monthly_summary.sum().sum() == 0:
        print("No monthly trend data to plot.")
        return

    plt.figure(figsize=(12, 6))

    # Line Chart (Matplotlib)
    monthly_summary.plot(kind='line', ax=plt.gca(), marker='o')

    # Formatting (Usability NFR)
    plt.title('Monthly Income vs. Expenses Trend')
    plt.xlabel('Date')
    plt.ylabel('Amount ($)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Type')
    plt.tight_layout()
    plt.show()
    #  # Diagram added for instructive value
from datetime import datetime
def get_user_choice():
    """
    Displays the main menu and gets a valid user choice.
    """
    print("\n--- Expense Analyzer Menu ---")
    print("1. Record New Expense/Income")
    print("2. Run Analysis & View Reports")
    print("3. Exit")

    while True:
        try:
            choice = input("Enter your choice (1-3): ")
            if choice in ['1', '2', '3']:
                return choice
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            return '3'

def get_new_expense_data():
    """
    Prompts user for date, category, and amount. (Error Handling Strategy: Input Validation)

    Returns:
        tuple: (date_str, category_name, amount) or None
    """
    date_str = input(f"Enter Date (YYYY-MM-DD, default today: {datetime.now().strftime('%Y-%m-%d')}): ")
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')

    # 1. Get Category
    print("\nSelect Category:")
    for num, cat in CATEGORIES.items():
        print(f"  {num}: {cat}")

    while True:
        try:
            cat_choice = input("Enter category number: ")
            if not cat_choice.isdigit():
                print("Invalid input. Please enter a number.")
                continue

            cat_choice = int(cat_choice)
            category_name = CATEGORIES.get(cat_choice)
            if category_name:
                break
            else:
                print("Invalid category number.")
        except ValueError:
            # This should not be hit with the improved check
            print("Invalid input. Please enter a number.")

    # 2. Get Amount (Validation)
    while True:
        try:
            amount_input = input("Enter Amount (use NEGATIVE for expense, POSITIVE for income): ")
            amount = float(amount_input)
            if amount == 0:
                 print("Amount cannot be zero. Please re-enter.")
            else:
                break
        except ValueError:
            # Error Handling Strategy: Catches non-numeric input
            print("Invalid input. Please enter a numerical amount.")

    return date_str, category_name, amount

def display_stats(stats: dict):
    """Displays the summary statistics in a readable format."""
    print("\n--- Summary Statistics ---")
    if "Note" in stats:
        print(stats["Note"])
        return

    for key, value in stats.items():
        if key in ['Total Expenses', 'Mean Daily Expense', 'Median Daily Expense', 'Std. Dev. of Expense', '75th Percentile']:
            # Use locale-aware formatting for large numbers
            print(f"  {key:<25}: ${value:,.2f}")
        else:
            print(f"  {key:<25}: {value}")
    print("--------------------------")

def record_expense_workflow():
    """Handles the user workflow for recording a new expense."""
    data = get_new_expense_data()
    if data:
        date, category, amount = data
        # Data is saved immediately (Reliability NFR)
        save_expense(date, category, amount)

def analysis_workflow():
    """Handles the user workflow for running analysis and viewing reports."""
    # Load data from CSV
    df = load_data()

    if df.empty:
        print("\nCannot run analysis. Data file is empty or failed to load.")
        return

    print("\n--- Running Expense Analysis ---")

    # 1. Category Breakdown - Removed .copy() as calculator functions handle their copies
    category_totals = calculate_category_spending(df)
    print("\nCategory Spending Table:")
    print(category_totals.sort_values(ascending=False).to_string(float_format="${:,.2f}".format))

    # 2. Statistical Analysis - Removed .copy()
    stats = get_summary_statistics(df)
    display_stats(stats)

    # 3. Monthly Trends - Removed .copy()
    monthly_summary = calculate_monthly_trends(df)

    # 4. Visualizations
    plot_category_spending(category_totals)
    plot_monthly_trends(monthly_summary)

    print("Analysis complete.")


def main():
    """Main function controlling the logical workflow of the system."""
    print("===================================================")
    print("  Welcome to the Modular Expense Analyzer System  ")
    print("===================================================")

    # Ensure the data file and directory are set up on startup
    setup_data_file()

    while True:
        choice = get_user_choice()

        if choice == '1':
            record_expense_workflow()

        elif choice == '2':
            analysis_workflow()

        elif choice == '3':
            print("\nThank you for using the Expense Analyzer. Goodbye!")
            break

if __name__ == '__main__':
    main()
