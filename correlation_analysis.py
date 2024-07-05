# correlation_analysis.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class CorrelationAnalysis:
    def __init__(self, df: pd.DataFrame, threshold: float = 0.9):
        self.df = df
        self.threshold = threshold

    def compute_correlation_matrix(self):
        numeric_df = self.df.select_dtypes(include=[np.number])
        return numeric_df.corr()

    def visualize_correlation_matrix(self, corr_matrix):
        plt.figure(figsize=(16, 12))
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', cbar=True, square=True)
        plt.title('Correlation Matrix')
        plt.tight_layout()
        plt.show()

    def identify_highly_correlated_columns(self, corr_matrix):
        correlated_columns = set()
        for i in range(len(corr_matrix.columns)):
            for j in range(i):
                if abs(corr_matrix.iloc[i, j]) > self.threshold:
                    colname = corr_matrix.columns[i]
                    correlated_columns.add(colname)
        return list(correlated_columns)

    def remove_highly_correlated_columns(self, correlated_columns):
        essential_columns = ['funded_amount', 'total_rec_prncp']  # Ensure these columns are not removed
        correlated_columns = [col for col in correlated_columns if col not in essential_columns]

        print("Columns before removing highly correlated columns:", self.df.columns)
        print("Highly correlated columns to be removed:", correlated_columns)
        
        self.df = self.df.drop(columns=correlated_columns)
        
        print("Columns after removing highly correlated columns:", self.df.columns)
        return self.df

    def explain_correlation_matrix(self, corr_matrix):
        explanation = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i):
                if abs(corr_matrix.iloc[i, j]) > self.threshold:
                    explanation.append(
                        f"Column '{corr_matrix.columns[i]}' is highly correlated with '{corr_matrix.columns[j]}' (correlation = {corr_matrix.iloc[i, j]:.2f})."
                    )
        return explanation

# Example usage
if __name__ == "__main__":
    # File paths
    original_csv_file_path = 'D:\\Aicore\\EDA_Project\\exploratory-data-analysis---customer-loans-in-finance192\\loan_payments.csv'
    cleaned_csv_file_path = 'D:\\Aicore\\EDA_Project\\exploratory-data-analysis---customer-loans-in-finance192\\cleaned_loan_payments.csv'

    # Load the CSV file
    df = pd.read_csv(cleaned_csv_file_path)

    # Initialize CorrelationAnalysis with the DataFrame and a correlation threshold
    threshold = 0.9
    correlation_analysis = CorrelationAnalysis(df, threshold)

    # Step 1: Compute the correlation matrix
    correlation_matrix = correlation_analysis.compute_correlation_matrix()

    # Step 2: Visualize the correlation matrix
    correlation_analysis.visualize_correlation_matrix(correlation_matrix)

    # Step 3: Identify highly correlated columns
    highly_correlated_columns = correlation_analysis.identify_highly_correlated_columns(correlation_matrix)
    print(f"Highly correlated columns (Threshold > {threshold}):\n", highly_correlated_columns)

    # Step 4: Explain the correlation matrix
    explanation = correlation_analysis.explain_correlation_matrix(correlation_matrix)
    for line in explanation:
        print(line)

    # Step 5: Remove highly correlated columns from the dataset
    cleaned_df = correlation_analysis.remove_highly_correlated_columns(highly_correlated_columns)

    # Save the cleaned DataFrame back to CSV
    cleaned_csv_output_file_path = 'D:\\Aicore\\EDA_Project\\exploratory-data-analysis---customer-loans-in-finance192\\cleaned_loan_payments_no_correlated.csv'
    cleaned_df.to_csv(cleaned_csv_output_file_path, index=False)
    print(f"Data with highly correlated columns removed saved to {cleaned_csv_output_file_path}")
