import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display

# Load the cleaned CSV file from the actual path provided
cleaned_csv_file_path = 'D:\\Aicore\\EDA_Project\\exploratory-data-analysis---customer-loans-in-finance192\\cleaned_loan_payments_no_correlated.csv'
df = pd.read_csv(cleaned_csv_file_path)

# Identify customers behind on their loan payments (late statuses)
late_statuses = ['Late (31-120 days)', 'Late (16-30 days)', 'In Grace Period']
late_loans = df[df['loan_status'].isin(late_statuses)].copy()

# Identify customers who have already stopped paying (charged off)
charged_off_loans = df[df['loan_status'] == 'Charged Off'].copy()

# Function to calculate relative rates for each indicator
def calculate_relative_rates(df, indicator):
    total_count = df[indicator].value_counts()
    late_count = late_loans[indicator].value_counts().reindex(total_count.index, fill_value=0)
    charged_off_count = charged_off_loans[indicator].value_counts().reindex(total_count.index, fill_value=0)
    relative_late_rate = (late_count / total_count) * 100
    relative_charged_off_rate = (charged_off_count / total_count) * 100
    return total_count, late_count, charged_off_count, relative_late_rate, relative_charged_off_rate

# Plotting function for verification status
def plot_verification_status_comparison(late_count, charged_off_count, relative_late_rate, relative_charged_off_rate):
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    ax2 = ax1.twinx()
    sns.barplot(x=late_count.index, y=late_count.values, ax=ax1, color='orange', label='Late Loans')
    sns.barplot(x=charged_off_count.index, y=charged_off_count.values, ax=ax1, color='salmon', label='Charged Off Loans')
    
    sns.lineplot(x=relative_late_rate.index, y=relative_late_rate.values, ax=ax2, color='blue', label='Late Rate (%)')
    sns.lineplot(x=relative_charged_off_rate.index, y=relative_charged_off_rate.values, ax=ax2, color='red', label='Charged Off Rate (%)')
    
    ax1.set_xlabel('Verification Status')
    ax1.set_ylabel('Count')
    ax2.set_ylabel('Rate (%)')
    plt.title('Effect of Verification Status on Loan Payment Status')
    
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Analyze verification status for late loans and charged off loans
indicator = 'verification_status'
total_count, late_count, charged_off_count, relative_late_rate, relative_charged_off_rate = calculate_relative_rates(df, indicator)

# Combine the data for easier analysis
verification_status_data = pd.DataFrame({
    'Total Count': total_count,
    'Late Count': late_count,
    'Charged Off Count': charged_off_count,
    'Relative Late Rate (%)': relative_late_rate,
    'Relative Charged Off Rate (%)': relative_charged_off_rate
}).fillna(0)

# Add indicator column for identification
verification_status_data['Indicator'] = indicator
verification_status_data['Value'] = verification_status_data.index

# Reorder columns for better readability
verification_status_data = verification_status_data[['Indicator', 'Value', 'Total Count', 'Late Count', 'Charged Off Count', 'Relative Late Rate (%)', 'Relative Charged Off Rate (%)']]

# Display the summary dataframe as a pop-up
display(verification_status_data)

# Plot the verification status comparison
plot_verification_status_comparison(late_count, charged_off_count, relative_late_rate, relative_charged_off_rate)

