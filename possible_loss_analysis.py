# possible_loss_analysis.py

import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned CSV file
cleaned_csv_file_path = 'D:\\Aicore\\EDA_Project\\exploratory-data-analysis---customer-loans-in-finance192\\cleaned_loan_payments_no_correlated.csv'
df = pd.read_csv(cleaned_csv_file_path)

# Check if the required columns are present
required_columns = ['loan_status', 'loan_amount', 'term', 'int_rate', 'total_payment', 'total_rec_prncp', 'loan_status']
print("Columns in dataset:", df.columns)
for column in required_columns:
    if column not in df.columns:
        raise KeyError(f"The '{column}' column is missing from the dataset.")

# Identify customers behind on their loan payments (e.g., status 'Late (31-120 days)', 'Late (16-30 days)', etc.)
late_statuses = ['Late (31-120 days)', 'Late (16-30 days)', 'In Grace Period']
late_loans = df[df['loan_status'].isin(late_statuses)].copy()

# Calculate the percentage of these users as a percentage of all loans
total_loans = len(df)
late_loans_count = len(late_loans)
late_loans_percentage = (late_loans_count / total_loans) * 100

# Calculate the total amount of these loans
total_late_loans_amount = late_loans['loan_amount'].sum()

# Calculate the projected loss if these loans were to be charged off
late_loans.loc[:, 'projected_interest'] = late_loans.apply(
    lambda row: (row['loan_amount'] * row['int_rate'] / 100) / 12 * (row['term'] - (row['total_rec_prncp'] / row['loan_amount']) * row['term']), axis=1
)
total_projected_loss_if_charged_off = late_loans['projected_interest'].sum()

# Calculate the projected loss if these customers were to finish the full loan term
total_projected_loss_full_term = late_loans.apply(
    lambda row: (row['loan_amount'] * row['int_rate'] / 100) / 12 * row['term'], axis=1
).sum()

# Print the results
print(f"Total number of loans: {total_loans}")
print(f"Number of late loans: {late_loans_count}")
print(f"Percentage of late loans: {late_loans_percentage:.2f}%")
print(f"Total amount of late loans: ${total_late_loans_amount:,.2f}")
print(f"Projected loss if late loans were charged off: ${total_projected_loss_if_charged_off:,.2f}")
print(f"Projected loss if late loans were to finish the full loan term: ${total_projected_loss_full_term:,.2f}")

# Calculate the combined impact of already charged off loans and potentially defaulting loans
charged_off_loans = df[df['loan_status'] == 'Charged Off'].copy()
charged_off_total_loss = charged_off_loans['total_payment'].sum()
combined_loss_if_charged_off = charged_off_total_loss + total_projected_loss_if_charged_off
total_expected_revenue = df['loan_amount'].sum() + total_projected_loss_full_term
combined_loss_percentage = (combined_loss_if_charged_off / total_expected_revenue) * 100

# Print the combined impact
print(f"Combined loss (already charged off + potentially defaulting): ${combined_loss_if_charged_off:,.2f}")
print(f"Combined loss as a percentage of total expected revenue: {combined_loss_percentage:.2f}%")

# Visualize the combined impact with a pie chart
labels = ['Combined Loss', 'Remaining Revenue']
sizes = [combined_loss_if_charged_off, total_expected_revenue - combined_loss_if_charged_off]
colors = ['#FF5733', '#4CAF50']
explode = (0.1, 0)

plt.figure(figsize=(8, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')
plt.title('Combined Impact of Charged Off and Potentially Defaulting Loans on Total Revenue')
plt.show()

# Visualize the results with an annotated bar chart
categories = ['Total Loans', 'Late Loans', 'Late Loans Percentage', 'Late Loans Amount', 
              'Projected Loss if Charged Off', 'Projected Loss Full Term', 'Combined Loss', 'Combined Loss Percentage']
values = [total_loans, late_loans_count, late_loans_percentage, total_late_loans_amount, 
          total_projected_loss_if_charged_off, total_projected_loss_full_term, combined_loss_if_charged_off, combined_loss_percentage]

plt.figure(figsize=(14, 8))
bars = plt.bar(categories, values, color=['#4CAF50', '#FF5733', '#FFD700', '#4CAF50', '#FF5733', '#FFD700', '#FF5733', '#FFD700'])

# Annotate the bar chart with the values
for bar, value in zip(bars, values):
    yval = round(value, 2)
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{yval:,}', ha='center', va='bottom', fontsize=10)

plt.xlabel('Categories')
plt.ylabel('Values')
plt.title('Analysis of Late Loans and Potential Losses')
plt.xticks(rotation=45, ha='right')
plt.grid(True)
plt.tight_layout()
plt.show()
