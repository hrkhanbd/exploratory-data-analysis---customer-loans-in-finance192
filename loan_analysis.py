# loan_analysis.py

import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned CSV file
cleaned_csv_file_path = 'D:\\Aicore\\EDA_Project\\exploratory-data-analysis---customer-loans-in-finance192\\cleaned_loan_payments_no_correlated.csv'
df = pd.read_csv(cleaned_csv_file_path)

# Check if the 'loan_amount' and 'total_payment' columns are present
print("Columns in dataset:", df.columns)
if 'loan_amount' not in df.columns:
    raise KeyError("The 'loan_amount' column is missing from the dataset.")
if 'total_payment' not in df.columns:
    raise KeyError("The 'total_payment' column is missing from the dataset.")

# Summarize the current state of the loans
total_funded = df['loan_amount'].sum()
total_recovered = df['total_payment'].sum()

# Calculate the percentage of loans recovered
recovered_percentage = (total_recovered / total_funded) * 100

# Print the summary
print(f"Total Loan Amount: ${total_funded:,.2f}")
print(f"Total Recovered Amount: ${total_recovered:,.2f}")
print(f"Percentage of Loans Recovered: {recovered_percentage:.2f}%")

# Visualize the current state of the loans
labels = ['Recovered', 'Outstanding']
sizes = [total_recovered, total_funded - total_recovered]
colors = ['#4CAF50', '#FF5733']
explode = (0.1, 0)

print("Sizes for pie chart:", sizes)

plt.figure(figsize=(8, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')
plt.title('Current State of Loan Recovery')
plt.show()

# Attempt to calculate the projected recovery in the next 6 months
print("Sample 'last_payment_date' values before conversion:")
print(df['last_payment_date'].head(10))  # Inspect the first 10 values for diagnosis

# Convert 'last_payment_date' to datetime format and suppress the warning
with pd.option_context('mode.chained_assignment', None):
    df['last_payment_date'] = pd.to_datetime(df['last_payment_date'], errors='coerce')

print("Sample 'last_payment_date' values after conversion:")
print(df['last_payment_date'].head(10))  # Inspect the first 10 values after conversion

if df['last_payment_date'].notna().sum() > 0:
    # Calculate the projected recovery if valid dates are available
    monthly_recovery_rate = total_recovered / (df['last_payment_date'].max() - df['last_payment_date'].min()).days * 30
    projected_recovery_6_months = monthly_recovery_rate * 6

    if projected_recovery_6_months < 0 or pd.isna(projected_recovery_6_months):
        projected_recovery_6_months = 0

    # Visualize the projected recovery
    labels = ['Recovered', 'Projected Recovery 6 Months', 'Outstanding']
    sizes = [total_recovered, projected_recovery_6_months, total_funded - total_recovered - projected_recovery_6_months]
    colors = ['#4CAF50', '#FFD700', '#FF5733']
    explode = (0.1, 0, 0)

    print("Sizes for projected recovery pie chart:", sizes)

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.title('Projected Loan Recovery in Next 6 Months')
    plt.show()
else:
    print("No valid 'last_payment_date' available for projections. Skipping the projected recovery visualization.")
