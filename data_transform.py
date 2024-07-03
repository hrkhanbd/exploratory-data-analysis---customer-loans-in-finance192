# data_transform.py

import pandas as pd
from dateutil import parser

class DataTransform:
    """
    A class to perform data transformations on a Pandas DataFrame.
    """

    def __init__(self, dataframe: pd.DataFrame):
        """
        Initializes the DataTransform class with a DataFrame.

        :param dataframe: The Pandas DataFrame to transform.
        """
        self.dataframe = dataframe

    def convert_to_numeric(self, column_name: str):
        """
        Converts a column to numeric format.

        :param column_name: The name of the column to convert.
        """
        if column_name not in ['id', 'member_id']:
            self.dataframe[column_name] = pd.to_numeric(self.dataframe[column_name], errors='coerce')

    def convert_to_datetime(self, column_name: str):
        """
        Converts a column to datetime format using the dateutil parser.
        Keeps the original format 'Mon-YY' after conversion.

        :param column_name: The name of the column to convert.
        """
        def parse_date(x):
            if pd.isnull(x):
                return x
            try:
                return parser.parse(x, dayfirst=False, yearfirst=True).strftime('%b-%y')
            except Exception:
                return x

        self.dataframe[column_name] = self.dataframe[column_name].apply(parse_date)

    def convert_to_categorical(self, column_name: str):
        """
        Converts a column to categorical format.

        :param column_name: The name of the column to convert.
        """
        if column_name not in ['id', 'member_id']:
            self.dataframe[column_name] = self.dataframe[column_name].astype('category')

    def remove_symbols(self, column_name: str, symbols: str):
        """
        Removes specified symbols from a column.

        :param column_name: The name of the column to process.
        :param symbols: A string of symbols to remove.
        """
        if column_name not in ['id', 'member_id']:
            self.dataframe[column_name] = self.dataframe[column_name].replace(symbols, '', regex=True)

    def convert_term_to_numeric(self):
        """
        Converts the 'term' column to numeric format after removing the 'months' string.
        """
        self.dataframe['term'] = self.dataframe['term'].str.extract('(\d+)').astype(float)

    def apply_transformations(self):
        """
        Apply transformations to the DataFrame based on the data dictionary.
        """
        # Numeric columns
        numeric_columns = [
            'loan_amount', 'funded_amount', 'funded_amount_inv', 'int_rate', 'instalment', 'annual_inc',
            'dti', 'delinq_2yrs', 'inq_last_6mths', 'mths_since_last_delinq', 'mths_since_last_record',
            'open_accounts', 'total_accounts', 'out_prncp', 'out_prncp_inv', 'total_payment', 'total_payment_inv',
            'total_rec_prncp', 'total_rec_int', 'total_rec_late_fee', 'recoveries', 'collection_recovery_fee',
            'last_payment_amount', 'collections_12_mths_ex_med', 'mths_since_last_major_derog'
        ]
        for column in numeric_columns:
            self.convert_to_numeric(column)

        # Convert 'term' column to numeric
        self.convert_term_to_numeric()

        # Datetime columns
        datetime_columns = [
            'issue_date', 'earliest_credit_line', 'last_payment_date', 'next_payment_date', 'last_credit_pull_date'
        ]
        for column in datetime_columns:
            self.convert_to_datetime(column)

        # Categorical columns
        categorical_columns = [
            'grade', 'sub_grade', 'employment_length', 'home_ownership', 'verification_status', 'loan_status',
            'payment_plan', 'purpose', 'policy_code', 'application_type'
        ]
        for column in categorical_columns:
            self.convert_to_categorical(column)

        # Remove symbols from specific columns
        symbol_columns = ['id', 'member_id']
        for column in symbol_columns:
            self.remove_symbols(column, '[^a-zA-Z0-9]')

        return self.dataframe

# Example usage
if __name__ == "__main__":
    # Load the CSV file
    csv_file_path = 'D:\\Aicore\\EDA_Project\\exploratory-data-analysis---customer-loans-in-finance192\\loan_payments.csv'
    df = pd.read_csv(csv_file_path)

    # Initialize DataTransform with the DataFrame
    transformer = DataTransform(df)

    # Apply transformations
    transformed_df = transformer.apply_transformations()

    # Save the transformed DataFrame back to CSV (if needed!)
    transformed_csv_file_path = 'D:\\Aicore\\EDA_Project\\exploratory-data-analysis---customer-loans-in-finance192\\transformed_loan_payments.csv'
    transformed_df.to_csv(transformed_csv_file_path, index=False)
    print(f"Transformed data saved to {transformed_csv_file_path}")


