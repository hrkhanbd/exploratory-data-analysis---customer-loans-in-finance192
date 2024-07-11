# Exploratory Data Analysis - Customer Loans in Finance

## Table of Contents
1. [Project Description](#project-description)
2. [Installation Instructions](#installation-instructions)
3. [Usage Instructions](#usage-instructions)
4. [File Structure](#file-structure)
5. [License](#license)

## Project Overview

The project involves performing exploratory data analysis on a loan portfolio for a large financial institution. Managing loans is a critical component of the business operations, and gaining a comprehensive understanding of the loan data is essential for making informed decisions about loan approvals and risk management.

The goal of this project is to use various statistical and data visualization techniques to uncover patterns, relationships, and anomalies in the loan data. This information will enable the business to make more informed decisions about loan approvals, pricing, and risk management.

By conducting exploratory data analysis on the loan data, the aim is to gain a deeper understanding of the risk and return associated with the business' loans. Ultimately, the project aims to improve the performance and profitability of the loan portfolio.

## Exploratory Data Analysis - Customer Loans in Finance

This notebook documents the process of performing Exploratory Data Analysis (EDA) on the customer loans dataset. The following tasks will be covered:

1. **Convert columns to the correct format**
2. **Create a class to get information from the DataFrame**
3. **Remove/impute missing values in the data**
4. **Perform transformation on skewed columns**
5. **Remove outliers from the data**
6. **Drop overly correlated columns**

### Task 1: Convert Columns to the Correct Format

We will start by converting columns to the correct format. This includes converting columns to numeric, datetime, or categorical types, and removing symbols.

### Task 2: Create a Class to Get Information from the DataFrame

Next, we will create a `DataFrameInfo` class to extract useful information from the DataFrame.

### Task 3: Calculating Projected Loss

Calculate the projected loss of the loans marked as **Charged Off**.

Calculate the loss in revenue these loans would have generated for the company if they had finished their term. Visualize the loss projected over the remaining term of these loans.

Calculate the percentage of charged off loans historically and the total amount that was paid towards these loans before being charged off.

To calculate the projected loss of the loans marked as **Charged Off**, we need to estimate the potential revenue that these loans would have generated if they had completed their term. The projected loss can be calculated based on the interest that would have been accrued over the remaining term.

### Task 4: Possible Loss

There are customers who are currently behind with their loan payments. This subset of customers represents a risk to company revenue.

- **What percentage do users in this bracket currently represent as a percentage of all loans?**
- **Calculate the total amount of customers in this bracket and how much loss the company would incur if their status was changed to Charged Off.**
- **What is the projected loss of these loans if the customers were to finish the full loan term?**

If customers late on payments converted to **Charged Off**, what percentage of total expected revenue do these customers and the customers who have already defaulted on their loan represent?

To address Task 4, we need to identify customers who are behind with their loan payments, calculate the potential losses if their status changes to **Charged Off**, and analyze the overall impact on the company's revenue.

### Task 5: Indicators of Loss

In this task, we will be analyzing the data to visualize the possible indicators that a customer will not be able to pay the loan.

We will compare columns that might be indicators against customers who have already stopped paying and customers who are currently behind on payments.

Here are some example columns that might indicate that a user might not pay the loan:

- **Does the grade of the loan have an effect on customers not paying?**
  - For example, we will analyze if customers with lower grades (e.g., D, E, F, G) are more likely to default compared to those with higher grades (e.g., A, B, C).
  
- **Is the purpose for the loan likely to have an effect?**
  - For instance, we will check if loans taken for certain purposes (e.g., debt consolidation, small business) have higher default rates compared to others (e.g., home improvement, vacation).
  
- **Does the home_ownership value contribute to the likelihood a customer won't pay?**
  - We will investigate if customers who rent or have a mortgage are more likely to default compared to those who own their homes outright.

To help identify which columns will be of interest, we will create a subset of these users.

We will make the analysis and determine the columns contributing to loans not being paid off and visualize any interesting indicators.

We will compare these indicators between loans already charged off and loans which could change to charged off to check if these same factors apply to loans which have the potential to change to "Charged Off".

## Installation Instructions

To run this project, ensure you have Python installed on your system. Additionally, you will need to install the following Python packages:

```sh
pip install pandas matplotlib seaborn python-dateutil


## Usage Instructions
1. Clone the repository to your local machine:
    ```bash
git clone https://github.com/hrkhanbd/exploratory-data-analysis---customer-loans-in-finance192.git
cd exploratory-data-analysis---customer-loans-in-finance192
    ```

2. Run Data Transformation and Analysis Scripts

#### Data Transformation:
- `data_transform.py`: Performs initial data transformations.
- `dataframe_info.py`: Extracts information and statistics from the DataFrame.
- `dataframe_transform.py`: Further transforms the DataFrame, handling missing values and outliers.

#### Data Analysis:
- `loan_data_analysis.py`: Combines various analysis steps including transformation, visualization, and correlation analysis.
- `plotter.py`: Contains functions to visualize different aspects of the data.
- `correlation_analysis.py`: Analyzes correlations between features in the dataset.

#### Standalone Analysis Scripts:
- `loan_analysis.py`: Script for summarizing the current state of loans and visualizing the results.
- `loan_loss_analysis.py`: Script for calculating and visualizing the percentage of charged-off loans.
- `loan_projected_loss_analysis.py`: Script for calculating and visualizing the projected loss of charged-off loans.
- `loan_risk_analysis.py`: Script for analyzing the potential loss due to customers behind on payments.
- `loan_indicators_analysis.py`: Script for analyzing and visualizing indicators of loan default.
  
3. Run the Jupyter Notebook:
Open EDA_Customers_loans.ipynb in Jupyter Notebook to interactively run the analysis and visualize the results

## File Structure

- `data_transform.py`: Contains the DataTransform class for initial data transformations.
- `dataframe_info.py`: Contains the DataFrameInfo class to extract statistics and information.
- `dataframe_transform.py`: Contains the DataFrameTransform class for advanced transformations.
- `loan_data_analysis.py`: Integrates data transformation and analysis processes.
- `plotter.py`: Contains functions for plotting and visualizing data.
- `correlation_analysis.py`: Contains the CorrelationAnalysis class to perform correlation analysis.
- `loan_analysis.py`: Script for summarizing the current state of loans and visualizing the results.
- `loan_loss_analysis.py`: Script for calculating and visualizing the percentage of charged-off loans.
- `loan_projected_loss_analysis.py`: Script for calculating and visualizing the projected loss of charged-off loans.
- `loan_risk_analysis.py`: Script for analyzing the potential loss due to customers behind on payments.
- `loan_indicators_analysis.py`: Script for analyzing and visualizing indicators of loan default.
- `EDA_Customer_loans.ipynb`: Jupyter Notebook for interactive analysis and visualization.
- `cleaned_loan_payments_no_correlated.csv`: Cleaned dataset used in the analysis.
- `README.md`: Documentation for the project.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.



