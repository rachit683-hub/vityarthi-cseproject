# vityarthi-cseproject-
Overview of the Project
The Modular Expense Analyzer System is a financial tracking tool that manages user financial data (expenses and income) in a CSV file. It provides a simple, menu-driven command-line interface for data entry and offers powerful analytical capabilities using Pandas and NumPy for calculations and Matplotlib for generating visualizations (charts). A key feature is its ability to handle data in Rupees (Rs) and separate expenses (negative amounts) from income (positive amounts) for accurate trend analysis.

Features:-  The system offers the following core functionalities:
Data Persistence:- Stores all financial records in a secure, structured CSV file (data/expenses.csv) ensuring data is saved between sessions (Reliability NFR).
Expense/Income Recording:- Allows users to easily record new transactions, prompting for date, category, and amount, with built-in input validation for amounts and category choice.
Comprehensive Reporting:- 1. Calculates and displays a Category Spending Table showing total expenditure per category.
                          2. Generates Summary Statistics (Total Expenses, Mean, Median, Standard Deviation) using NumPy (Performance NFR).
                          3. Calculates Monthly Trends for both expenses and income.
Data Visualization: Automatically generates two types of charts (Usability NFR):  A Bar Chart showing total spending by category.

Type	                              |          Technology/Tool	      |              Purpose
Language	                          |             Python 3+	          |  Core programming language
Data Analysis	                      |             Pandas	            |  Data loading, manipulation, aggregation (groupby, resample), and CSV handling
Numerical/Statistics	              |             NumPy	              |  High-performance, vectorized calculation of summary statistics (mean, median, std. dev.)
Visualization	                      |             Matplotlib	        |  Generating bar charts and line charts for reports
File Handling	                      |             os module	          |  Managing the data directory and file paths
Save the Code: Save the provided code into a file named, for example, main_app.py.

Install Dependencies: The project requires Pandas, NumPy, and Matplotlib. Open your terminal or command prompt and run:
pip install pandas numpy matplotlib
Run the Application: Execute the Python script from your terminal:
python main_app.py
Note: Upon first run, it will automatically create the data directory and the expenses.csv file.
Instructions for Testing
To test the core features, follow these steps:

Record Data:
Select option 1. Record New Expense/Income.
Enter a Date (e.g., 2023-11-01).
Choose a Category number (e.g., 1 for Groceries).
Enter a negative Amount for an expense (e.g., -500).
Repeat the process, entering a positive Amount for income (Category 6, e.g., 20000). Record at least a few transactions across different categories and months.
Run Analysis:
Select option 2. Run Analysis & View Reports.
Verify Console Output:
Check the Category Spending Table to ensure expenses are summed correctly.
Review the Summary Statistics for accuracy.

Verify Charts:
Confirm that the Bar Chart appears and correctly reflects the spending totals.
Confirm that the Line Chart appears and shows the monthly trends for both Income and Expenses.
