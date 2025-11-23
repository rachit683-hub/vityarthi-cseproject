# Import necessary libraries
import pandas as pd
import os

# Define constants for file management and categories
DATA_DIR = 'data'
CSV_FILE_NAME = 'expenses.csv'
CSV_FILE_PATH = os.path.join(DATA_DIR, CSV_FILE_NAME)
CSV_COLUMNS = ['Date', 'Category', 'Amount']
CATEGORIES = {
    1: 'Groceries',
    2: 'Rent/Mortgage',
    3: 'Utilities',
    4: 'Transportation',
    5: 'Entertainment',
    6: 'Income',
    7: 'Other'
}

def ensure_data_directory_and_file():
    """Ensures the data directory exists and the CSV file is initialized with headers."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CSV_FILE_PATH):
        pd.DataFrame(columns=CSV_COLUMNS).to_csv(CSV_FILE_PATH, index=False)
        print(f"Ensured data directory '{DATA_DIR}' exists and '{CSV_FILE_NAME}' is initialized.")

def load_expenses():
    """Loads expenses from CSV, ensuring correct columns and handling of missing file."""
    ensure_data_directory_and_file()
    try:
        df = pd.read_csv(CSV_FILE_PATH)
        # Ensure all CSV_COLUMNS are present, add if missing with NaN values
        for col in CSV_COLUMNS:
            if col not in df.columns:
                df[col] = pd.NA
        # Reorder columns to match CSV_COLUMNS order
        df = df[CSV_COLUMNS]
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=CSV_COLUMNS)
    return df

def save_expenses(df):
    """Saves the DataFrame to the CSV file."""
    ensure_data_directory_and_file()
    df.to_csv(CSV_FILE_PATH, index=False)

def record_expense_income():
    """Records a new expense or income entry."""
    print("\nSelect Category:")
    for num, cat in CATEGORIES.items():
        print(f"  {num}: {cat}")

    while True:
        try:
            category_choice = int(input("Enter category number: "))
            if category_choice in CATEGORIES:
                category = CATEGORIES[category_choice]
                break
            else:
                print("Invalid category number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    while True:
        try:
            amount_str = input("Enter amount (e.g., 50.75 or -20 for income): ")
            amount = float(amount_str)
            break
        except ValueError:
            print("Invalid amount. Please enter a number.")

    date = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    new_entry = pd.DataFrame([{'Date': date, 'Category': category, 'Amount': amount}])

    df = load_expenses()
    df = pd.concat([df, new_entry], ignore_index=True)
    save_expenses(df)
    print("✅ Expense/Income recorded successfully.")

def calculate_category_spending(df):
    """Calculates total spending/income per category."""
    # Filter for valid numeric amounts and ensure 'Category' column exists
    expenses_df = df.dropna(subset=['Amount', 'Category']).copy()

    # Convert 'Amount' to numeric, handling potential errors
    expenses_df['Amount'] = pd.to_numeric(expenses_df['Amount'], errors='coerce')
    expenses_df = expenses_df.dropna(subset=['Amount']) # Drop rows where Amount couldn't be converted

    # Separate expenses (positive amount) and income (negative amount) for more accurate reporting if needed
    # For category spending, we sum all amounts by category, income categories will sum negatively.
    category_totals = expenses_df.groupby('Category')['Amount'].sum()

    return category_totals

def calculate_monthly_spending(df):
    """Calculates total spending/income per month."""
    df_copy = df.copy()
    df_copy['Date'] = pd.to_datetime(df_copy['Date'])
    df_copy['Month'] = df_copy['Date'].dt.to_period('M')
    monthly_totals = df_copy.groupby('Month')['Amount'].sum()
    return monthly_totals

def display_reports(df):
    """Displays various financial reports."""
    if df.empty:
        print("No data to generate reports. Please record some expenses/income first.")
        return

    # 1. Category Breakdown
    category_totals = calculate_category_spending(df)
    print("\n--- Category Spending Breakdown ---")
    if not category_totals.empty:
        for category, total in category_totals.items():
            print(f"{category}: Rs {total:.2f}")
    else:
        print("No category data available.")

    # 2. Monthly Breakdown
    monthly_totals = calculate_monthly_spending(df)
    print("\n--- Monthly Spending Breakdown ---")
    if not monthly_totals.empty:
        for month, total in monthly_totals.items():
            print(f"{month.strftime('%Y-%m')}: Rs {total:.2f}")
    else:
        print("No monthly data available.")

    # 3. Overall Summary
    overall_total = df['Amount'].sum()
    print("\n--- Overall Summary ---")
    print(f"Total Balance: Rs {overall_total:.2f}")

def analysis_workflow():
    """Manages the analysis and reporting process."""
    df = load_expenses()
    if df.empty:
        print("No expenses recorded yet. Please record some first.")
        return

    print("\n--- Running Expense Analysis ---")
    display_reports(df)

def main():
    """Main function to run the Expense Analyzer System."""
    print("===================================================")
    print("  Welcome to the Modular Expense Analyzer System  ")
    print("      All amounts are recorded and displayed in Rupees (Rs)   ")
    print("===================================================")

    ensure_data_directory_and_file() # Ensure setup on start

    while True:
        print("\n--- Expense Analyzer Menu ---")
        print("1. Record New Expense/Income")
        print("2. Run Analysis & View Reports")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            record_expense_income()

        elif choice == '2':
            analysis_workflow()

        elif choice == '3':
            print("Exiting Expense Analyzer. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == '__main__':
    main()
