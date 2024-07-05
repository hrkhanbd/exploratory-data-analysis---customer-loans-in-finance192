# loan_projected_loss_analysis.py

import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned CSV file
cleaned_csv_file_path = 'D:\\Aicore\\EDA_Project\\exploratory-data-analysis---customer-loans-in-finance192\\cleaned_loan_payments_no_correlated.csv'
df = pd.read_csv(cleaned_csv_file_path)

# Check if the required columns are present
required_columns = ['loan_status', 'loan_amount', 'term', 'int_rate', 'total_payment']
print("Columns in dataset:", df.columns)
for column in required_columns:
    if column not in df.columns:
        raise KeyError(f"The '{column}' column is missing from the dataset.")

# Filter loans that are marked as 'Charged Off'
charged_off_loans = df[df['loan_status'] == 'Charged Off'].copy()

# Calculate the remaining term for each charged off loan
charged_off_loans.loc[:, 'remaining_term'] = charged_off_loans['term'] - charged_off_loans['total_payment'] / (charged_off_loans['loan_amount'] / charged_off_loans['term'])

# Calculate the projected interest that would have been earned if the loan had completed its term
charged_off_loans.loc[:, 'projected_interest'] = charged_off_loans.apply(
    lambda row: (row['loan_amount'] * row['int_rate'] / 100) / 12 * row['remaining_term'], axis=1
)

# Calculate the total projected loss
total_projected_loss = charged_off_loans['projected_interest'].sum()

# Print the results
print(f"Total projected loss from charged off loans: ${total_projected_loss:,.2f}")

# Visualize the projected loss over the remaining term of the charged off loans
plt.figure(figsize=(10, 6))
plt.hist(charged_off_loans['projected_interest'], bins=30, color='#FF5733', edgecolor='black')
plt.title('Distribution of Projected Loss from Charged Off Loans')
plt.xlabel('Projected Loss ($)')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# Visualize the total projected loss
labels = ['Projected Loss', 'Others']
sizes = [total_projected_loss, charged_off_loans['loan_amount'].sum() - total_projected_loss]
colors = ['#FF5733', '#4CAF50']
explode = (0.1, 0)

plt.figure(figsize=(8, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')
plt.title('Total Projected Loss from Charged Off Loans')
plt.show()
