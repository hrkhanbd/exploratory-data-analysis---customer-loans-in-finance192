# loan_data_analysis.py

import pandas as pd
from data_transform import DataTransform
from dataframe_info import DataFrameInfo
from plotter import Plotter
from dataframe_transform import DataFrameTransform
from correlation_analysis import CorrelationAnalysis

# File paths
original_csv_file_path = 'D:\\Aicore\\EDA_Project\\exploratory-data-analysis---customer-loans-in-finance192\\loan_payments.csv'
transformed_csv_file_path = 'D:\\Aicore\\EDA_Project\\exploratory-data-analysis---customer-loans-in-finance192\\transformed_loan_payments.csv'
cleaned_csv_file_path = 'D:\\Aicore\\EDA_Project\\exploratory-data-analysis---customer-loans-in-finance192\\cleaned_loan_payments.csv'
skewness_transformed_csv_file_path = 'D:\\Aicore\\EDA_Project\\exploratory-data-analysis---customer-loans-in-finance192\\skewness_transformed_loan_payments.csv'
outliers_removed_csv_file_path = 'D:\\Aicore\\EDA_Project\\exploratory-data-analysis---customer-loans-in-finance192\\outliers_removed_loan_payments.csv'

# Load the original CSV file
df = pd.read_csv(original_csv_file_path)

# Columns to exclude from transformations
exclude_columns = ['id', 'member_id']

# Initialize DataTransform with the DataFrame
transformer = DataTransform(df)

# Apply transformations, excluding specified columns
transformed_df = transformer.apply_transformations()

# Save the transformed DataFrame back to CSV
transformed_df.to_csv(transformed_csv_file_path, index=False)
print(f"Transformed data saved to {transformed_csv_file_path}")

# Creating an instance of DataFrameInfo with the transformed DataFrame
df_info = DataFrameInfo(transformed_df)

# Example usage
print("Column Descriptions:\n", df_info.describe_columns())
print("\nStatistics:\n", df_info.extract_statistics())
print("\nDistinct Values Count in Categorical Columns:\n", df_info.count_distinct_values())
print("\nDataFrame Shape:\n", df_info.shape())
print("\nNULL Values Count:\n", df_info.null_values_count())
print("\nHead:\n", df_info.head())
print("\nTail:\n", df_info.tail())
print("\nUnique Values in 'loan_status':\n", df_info.unique_values('loan_status'))

# Initialize DataFrameTransform with the transformed DataFrame
df_transform = DataFrameTransform(transformed_df)

# Get missing values summary and drop columns with more than 50% missing values
cleaned_df = df_transform.drop_missing_values(threshold=50)

# Impute missing values intelligently
imputed_df = df_transform.intelligent_impute_missing_values(skew_threshold=1)

# Check for remaining NULL values
final_missing_summary = df_transform.missing_values_summary()
print("\nFinal Missing Values Summary:\n", final_missing_summary)

# Save the cleaned DataFrame back to CSV
imputed_df.to_csv(cleaned_csv_file_path, index=False)
print(f"Cleaned data saved to {cleaned_csv_file_path}")

# Load the original and cleaned CSV files for comparison
original_df = pd.read_csv(original_csv_file_path)
cleaned_df = pd.read_csv(cleaned_csv_file_path)

# Initialize DataFrameInfo to check the initial state of the original DataFrame
original_df_info = DataFrameInfo(original_df)

# Check initial NULL values summary in the original DataFrame
initial_missing_summary = original_df_info.null_values_count()
print("\nInitial Missing Values Summary (Original Data):\n", initial_missing_summary)

# Initialize DataFrameInfo to check the state of the cleaned DataFrame
cleaned_df_info = DataFrameInfo(cleaned_df)

# Check final NULL values summary in the cleaned DataFrame
final_missing_summary = cleaned_df_info.null_values_count()
print("\nFinal Missing Values Summary (Cleaned Data):\n", final_missing_summary)

# Initialize Plotter with the cleaned DataFrame
plotter = Plotter(cleaned_df)

# Plot visualizations
plotter.plot_histogram('loan_amount')
plotter.plot_bar('loan_status')
plotter.plot_missing_values_heatmap()

# Plot comparison of missing values before and after removal
plotter.plot_missing_values_comparison(original_df=original_df)

# Step 1: Identify skewed columns in the cleaned data
skew_threshold = 1  # You can adjust this threshold as needed
df_transform_cleaned = DataFrameTransform(cleaned_df)
skewed_columns = df_transform_cleaned.identify_skewed_columns(skew_threshold)
print(f"\nSkewed Columns (Threshold > {skew_threshold}):\n", skewed_columns)

# Initialize Plotter to visualize skewed columns
plotter = Plotter(cleaned_df)

# Visualize skewed columns using QQ plots
if not skewed_columns.empty:
    plotter.plot_qq_plots(skewed_columns.index, title="Original Skewed Columns QQ Plots")
else:
    print("No skewed columns found with the given threshold.")

# Step 2: Transform skewed columns to reduce skewness
df_transform_cleaned.transform_skewed_columns(skew_threshold)

# Access the transformed DataFrame
transformed_skewed_df = df_transform_cleaned.df

# Save the transformed DataFrame after skewness reduction
transformed_skewed_df.to_csv(skewness_transformed_csv_file_path, index=False)
print(f"Skewness transformed data saved to {skewness_transformed_csv_file_path}")

# Step 4: Visualize the results of the transformations using QQ plots
transformed_skewed_df = pd.read_csv(skewness_transformed_csv_file_path)
plotter = Plotter(transformed_skewed_df)

# Visualize the transformed skewed columns using QQ plots
if not skewed_columns.empty:
    plotter.plot_qq_plots(skewed_columns.index, title="Transformed Skewed Columns QQ Plots")
else:
    print("No skewed columns found with the given threshold.")

# Plot comparison of skewness before and after transformation using histograms
if not skewed_columns.empty:
    plotter.plot_skewness_comparison(original_df=cleaned_df, transformed_df=transformed_skewed_df, columns=skewed_columns.index)
else:
    print("No skewed columns found with the given threshold.")

# Additional Steps: Remove Outliers and Re-visualize

# Step 1: Visualize data to identify outliers
numeric_columns = cleaned_df.select_dtypes(include='number').columns.difference(exclude_columns)
plotter.plot_boxplot(numeric_columns)

# Step 2: Remove outliers
df_no_outliers = df_transform_cleaned.remove_outliers(numeric_columns)

# Save the DataFrame with outliers removed back to CSV
df_no_outliers.to_csv(outliers_removed_csv_file_path, index=False)
print(f"Data with outliers removed saved to {outliers_removed_csv_file_path}")

# Step 3: Re-visualize the data to ensure outliers are removed
plotter_no_outliers = Plotter(df_no_outliers)
plotter_no_outliers.plot_boxplot(numeric_columns)

# Side-by-Side Comparison of Outliers Before and After Cleaning
plotter.plot_boxplot_comparison(original_df=cleaned_df, cleaned_df=df_no_outliers, columns=numeric_columns)

# Continue with further analysis

# Step 1: Identify skewed columns in the cleaned data without outliers
df_transform_cleaned_no_outliers = DataFrameTransform(df_no_outliers)
skewed_columns_no_outliers = df_transform_cleaned_no_outliers.identify_skewed_columns(skew_threshold)
print(f"\nSkewed Columns After Outlier Removal (Threshold > {skew_threshold}):\n", skewed_columns_no_outliers)

# Visualize skewed columns using QQ plots
if not skewed_columns_no_outliers.empty:
    plotter_no_outliers.plot_qq_plots(skewed_columns_no_outliers.index, title="Skewed Columns QQ Plots After Outlier Removal")
else:
    print("No skewed columns found with the given threshold.")

# Step 2: Transform skewed columns to reduce skewness after outlier removal
df_transform_cleaned_no_outliers.transform_skewed_columns(skew_threshold)

# Access the transformed DataFrame
transformed_skewed_df_no_outliers = df_transform_cleaned_no_outliers.df

# Save the transformed DataFrame after skewness reduction
transformed_skewed_df_no_outliers.to_csv(skewness_transformed_csv_file_path, index=False)
print(f"Skewness transformed data after outlier removal saved to {skewness_transformed_csv_file_path}")

# Step 4: Visualize the results of the transformations using QQ plots after outlier removal
plotter_transformed_skewed_no_outliers = Plotter(transformed_skewed_df_no_outliers)

# Visualize the transformed skewed columns using QQ plots
if not skewed_columns_no_outliers.empty:
    plotter_transformed_skewed_no_outliers.plot_qq_plots(skewed_columns_no_outliers.index, title="Transformed Skewed Columns QQ Plots After Outlier Removal")
else:
    print("No skewed columns found with the given threshold.")

# Plot comparison of skewness before and after transformation using histograms
if not skewed_columns_no_outliers.empty:
    plotter_transformed_skewed_no_outliers.plot_skewness_comparison(original_df=df_no_outliers, transformed_df=transformed_skewed_df_no_outliers, columns=skewed_columns_no_outliers.index)
else:
    print("No skewed columns found with the given threshold.")

# Correlation Analysis

# Initialize CorrelationAnalysis with the cleaned DataFrame and a correlation threshold
threshold = 0.9
correlation_analysis = CorrelationAnalysis(df_no_outliers, threshold)

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
cleaned_df_no_correlated = correlation_analysis.remove_highly_correlated_columns(highly_correlated_columns)

# Save the cleaned DataFrame back to CSV
cleaned_csv_output_file_path = 'D:\\Aicore\\EDA_Project\\exploratory-data-analysis---customer-loans-in-finance192\\cleaned_loan_payments_no_correlated.csv'
cleaned_df_no_correlated.to_csv(cleaned_csv_output_file_path, index=False)
print(f"Data with highly correlated columns removed saved to {cleaned_csv_output_file_path}")
