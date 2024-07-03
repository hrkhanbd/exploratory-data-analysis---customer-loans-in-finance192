# dataframe_info.py

import pandas as pd

class DataFrameInfo:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def describe_columns(self):
        return self.df.dtypes

    def extract_statistics(self):
        numeric_cols = self.df.select_dtypes(include='number')
        numeric_cols = numeric_cols.drop(columns=['id', 'member_id'], errors='ignore')
        statistics = {
            'median': numeric_cols.median(),
            'std': numeric_cols.std(),
            'mean': numeric_cols.mean()
        }
        return pd.DataFrame(statistics)

    def count_distinct_values(self):
        categorical_cols = self.df.select_dtypes(include='category')
        return categorical_cols.nunique()

    def shape(self):
        return self.df.shape

    def null_values_count(self):
        null_count = self.df.isnull().sum()
        null_percentage = (self.df.isnull().mean() * 100).round(2)
        return pd.DataFrame({'null_count': null_count, 'null_percentage': null_percentage})

    def head(self, n=5):
        return self.df.head(n)

    def tail(self, n=5):
        return self.df.tail(n)

    def unique_values(self, column_name):
        if column_name in self.df.columns:
            return self.df[column_name].unique()
        else:
            raise ValueError(f"Column {column_name} does not exist in the DataFrame")
