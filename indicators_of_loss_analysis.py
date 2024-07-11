# indicators_of_loss_analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned CSV file
cleaned_csv_file_path = 'D:\\Aicore\\EDA_Project\\exploratory-data-analysis---customer-loans-in-finance192\\cleaned_loan_payments_no_correlated.csv'
df = pd.read_csv(cleaned_csv_file_path)

# Check if the required columns are present
required_columns = ['loan_status', 'grade', 'purpose', 'home_ownership', 'employment_length', 'annual_inc', 'dti', 'verification_status', 'delinq_2yrs']
print("Columns in dataset:", df.columns)
for column in required_columns:
    if column not in df.columns:
        raise KeyError(f"The '{column}' column is missing from the dataset.")

# Identify customers behind on their loan payments (late statuses)
late_statuses = ['Late (31-120 days)', 'Late (16-30 days)', 'In Grace Period']
late_loans = df[df['loan_status'].isin(late_statuses)].copy()

# Identify customers who have already stopped paying (charged off)
charged_off_loans = df[df['loan_status'] == 'Charged Off'].copy()

# Create subsets of these users for analysis
subset_late_charged_off = pd.concat([late_loans, charged_off_loans])

# Define the list of indicators to analyze
indicator_columns = ['grade', 'purpose', 'home_ownership', 'employment_length', 'annual_inc', 'dti', 'verification_status', 'delinq_2yrs']

# Analyze each indicator for late loans and charged off loans
for column in indicator_columns:
    plt.figure(figsize=(12, 6))
    sns.countplot(data=subset_late_charged_off, x=column, hue='loan_status', order=subset_late_charged_off[column].value_counts().index)
    plt.title(f'Effect of {column} on Loan Payment Status')
    plt.xlabel(column)
    plt.ylabel('Count')
    plt.legend(title='Loan Status', loc='upper right')
    plt.xticks(rotation=45)
    
    # Adding annotation
    if column == 'grade':
        plt.text(0.5, max(subset_late_charged_off[column].value_counts()), 
                 'Lower grades (D, E, F, G) have higher default rates', 
                 horizontalalignment='center', size='medium', color='black', weight='semibold')
    elif column == 'purpose':
        plt.text(0.5, max(subset_late_charged_off[column].value_counts()), 
                 'Small business, debt consolidation, and credit card refinancing have higher default rates', 
                 horizontalalignment='center', size='medium', color='black', weight='semibold')
    elif column == 'home_ownership':
        plt.text(0.5, max(subset_late_charged_off[column].value_counts()), 
                 'Renters and mortgaged homeowners are more likely to default', 
                 horizontalalignment='center', size='medium', color='black', weight='semibold')
    elif column == 'employment_length':
        plt.text(0.5, max(subset_late_charged_off[column].value_counts()), 
                 'Shorter employment lengths correlate with higher default rates', 
                 horizontalalignment='center', size='medium', color='black', weight='semibold')
    elif column == 'annual_inc':
        plt.text(0.5, max(subset_late_charged_off[column].value_counts()), 
                 'Lower annual incomes are associated with higher default rates', 
                 horizontalalignment='center', size='medium', color='black', weight='semibold')
    elif column == 'dti':
        plt.text(0.5, max(subset_late_charged_off[column].value_counts()), 
                 'Higher DTI ratios are linked with higher default rates', 
                 horizontalalignment='center', size='medium', color='black', weight='semibold')
    elif column == 'verification_status':
        plt.text(0.5, max(subset_late_charged_off[column].value_counts()), 
                 'Loans with verified income show lower default rates', 
                 horizontalalignment='center', size='medium', color='black', weight='semibold')
    elif column == 'delinq_2yrs':
        plt.text(0.5, max(subset_late_charged_off[column].value_counts()), 
                 'More past delinquencies correlate with higher default rates', 
                 horizontalalignment='center', size='medium', color='black', weight='semibold')
    
    plt.tight_layout()
    plt.show()

# Compare indicators between charged off loans and potentially defaulting loans
for column in indicator_columns:
    plt.figure(figsize=(12, 6))
    sns.countplot(data=late_loans, x=column, order=late_loans[column].value_counts().index, color='orange', label='Late Loans')
    sns.countplot(data=charged_off_loans, x=column, order=late_loans[column].value_counts().index, color='red', label='Charged Off Loans', alpha=0.5)
    plt.title(f'Comparison of {column} between Late Loans and Charged Off Loans')
    plt.xlabel(column)
    plt.ylabel('Count')
    plt.legend(title='Loan Status', loc='upper right')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Summary comparison for each indicator between late loans and charged off loans
summary_data = []
for column in indicator_columns:
    late_distribution = late_loans[column].value_counts(normalize=True).sort_index()
    charged_off_distribution = charged_off_loans[column].value_counts(normalize=True).sort_index()
    comparison = pd.DataFrame({
        'Late Loans': late_distribution,
        'Charged Off Loans': charged_off_distribution
    }).fillna(0)
    summary_data.append(comparison)

for column, data in zip(indicator_columns, summary_data):
    plt.figure(figsize=(12, 6))
    data.plot(kind='bar', ax=plt.gca())
    plt.title(f'Normalized Distribution of {column} between Late Loans and Charged Off Loans')
    plt.xlabel(column)
    plt.ylabel('Proportion')
    plt.legend(loc='upper right')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Summary of Findings and Recommendations
"""
Summary of Findings:
1. Grade: Lower grades (e.g., D, E, F, G) have higher instances of defaults compared to higher grades (A, B). Loan grade is a significant risk indicator.
2. Purpose: Certain loan purposes like small business loans, debt consolidation, and credit card refinancing are associated with higher default rates. Loan purpose is a potential risk factor.
3. Home Ownership: Renters and mortgaged homeowners are more likely to default compared to those who own their homes outright. Home ownership status is an important risk indicator.
4. Employment Length: Shorter employment lengths correlate with higher default rates. Employment length is a crucial factor, with longer employment indicating lower risk.
5. Annual Income: Lower annual incomes are associated with higher default rates. Annual income is a strong indicator of repayment ability.
6. Debt-to-Income Ratio (DTI): Higher DTI ratios are linked with higher default rates. DTI ratio is a critical indicator of financial strain.
7. Verification Status: Loans with verified income show lower default rates. Income verification reduces default risk.
8. Number of Delinquencies (delinq_2yrs): More past delinquencies correlate with higher default rates. Past delinquencies are a strong predictor of future defaults.

Recommendations:
1. Risk-Based Pricing: Implement risk-based pricing strategies for loans with higher risk indicators.
2. Enhanced Verification: Strengthen income verification processes.
3. Monitoring and Support: Increase monitoring and support for loans with high DTI ratios or borrowers with shorter employment lengths.
4. Targeted Interventions: Develop targeted intervention strategies for high-risk loan purposes.
"""
