# loan_loss_analysis.py

import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned CSV file
cleaned_csv_file_path = 'D:\\Aicore\\EDA_Project\\exploratory-data-analysis---customer-loans-in-finance192\\cleaned_loan_payments_no_correlated.csv'
df = pd.read_csv(cleaned_csv_file_path)

# Check if the required columns are present
required_columns = ['loan_status', 'loan_amount', 'total_payment']
print("Columns in dataset:", df.columns)
for column in required_columns:
    if column not in df.columns:
        raise KeyError(f"The '{column}' column is missing from the dataset.")

# Filter loans that are marked as 'Charged Off'
charged_off_loans = df[df['loan_status'] == 'Charged Off']

# Calculate the percentage of charged off loans
total_loans = len(df)
charged_off_loans_count = len(charged_off_loans)
charged_off_percentage = (charged_off_loans_count / total_loans) * 100

# Calculate the total amount paid towards charged off loans before being charged off
total_paid_charged_off = charged_off_loans['total_payment'].sum()

# Print the results
print(f"Total number of loans: {total_loans}")
print(f"Number of charged off loans: {charged_off_loans_count}")
print(f"Percentage of charged off loans: {charged_off_percentage:.2f}%")
print(f"Total amount paid towards charged off loans: ${total_paid_charged_off:,.2f}")

# Visualize the percentage of charged off loans
labels = ['Charged Off', 'Others']
sizes = [charged_off_loans_count, total_loans - charged_off_loans_count]
colors = ['#FF5733', '#4CAF50']
explode = (0.1, 0)

plt.figure(figsize=(8, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')
plt.title('Percentage of Charged Off Loans')
plt.show()

