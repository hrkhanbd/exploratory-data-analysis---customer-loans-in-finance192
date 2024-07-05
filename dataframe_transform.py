# dataframe_transform.py

import pandas as pd
import numpy as np

class DataFrameTransform:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def drop_missing_values(self, threshold: float = 50):
        missing_percent = self.df.isnull().mean() * 100
        cols_to_drop = missing_percent[missing_percent > threshold].index
        print("Columns before dropping missing values:", self.df.columns)
        self.df = self.df.drop(columns=cols_to_drop)
        print("Columns after dropping missing values:", self.df.columns)
        return self.df

    def intelligent_impute_missing_values(self, skew_threshold: float = 1):
        numeric_cols = self.df.select_dtypes(include='number').columns
        for col in numeric_cols:
            if col not in ['id', 'member_id']:
                if abs(self.df[col].skew()) > skew_threshold:
                    self.df[col] = self.df[col].fillna(self.df[col].median())
                else:
                    self.df[col] = self.df[col].fillna(self.df[col].mean())
        return self.df

    def missing_values_summary(self):
        null_count = self.df.isnull().sum()
        null_percentage = (self.df.isnull().mean() * 100).round(2)
        return pd.DataFrame({'null_count': null_count, 'null_percentage': null_percentage})

    def identify_skewed_columns(self, skew_threshold: float = 1):
        numeric_cols = self.df.select_dtypes(include='number')
        skewed_cols = numeric_cols.apply(lambda x: x.skew()).abs()
        skewed_cols = skewed_cols.drop(index=['id', 'member_id'], errors='ignore')
        return skewed_cols[skewed_cols > skew_threshold]

    def transform_skewed_columns(self, skew_threshold: float = 1):
        skewed_cols = self.identify_skewed_columns(skew_threshold)
        for col in skewed_cols.index:
            self.df[col] = self.df[col].apply(lambda x: np.log1p(x) if x > 0 else x)
        return self.df

    def remove_outliers(self, columns, method='IQR'):
        """Removes outliers from specified columns using the given method."""
        if method == 'IQR':
            for col in columns:
                if col not in ['id', 'member_id']:
                    Q1 = self.df[col].quantile(0.25)
                    Q3 = self.df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    self.df = self.df[(self.df[col] >= lower_bound) & (self.df[col] <= upper_bound)]
        return self.df
