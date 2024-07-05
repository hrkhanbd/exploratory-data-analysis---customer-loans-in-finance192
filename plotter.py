# plotter.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

class Plotter:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def plot_histogram(self, column: str):
        plt.figure(figsize=(10, 6))
        sns.histplot(self.df[column].dropna(), kde=True)
        plt.title(f'Histogram of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.show()

    def plot_histograms_grid(self, columns, title="Histograms"):
        n = len(columns)
        cols = 3
        rows = (n // cols) + (n % cols > 0)
        fig, axes = plt.subplots(rows, cols, figsize=(cols*6, rows*4))
        axes = axes.flatten()

        for i, column in enumerate(columns):
            sns.histplot(self.df[column].dropna(), kde=True, ax=axes[i])
            axes[i].set_title(f'{column}')
            axes[i].set_xlabel(column)
            axes[i].set_ylabel('Frequency')
            axes[i].tick_params(axis='x', rotation=45)
        
        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])
        
        fig.suptitle(title, fontsize=16)
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        plt.show()

    def plot_bar(self, column: str):
        plt.figure(figsize=(10, 6))
        sns.countplot(data=self.df, x=column)
        plt.title(f'Bar Plot of {column}')
        plt.xlabel(column)
        plt.ylabel('Count')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

    def plot_missing_values_heatmap(self):
        plt.figure(figsize=(12, 8))
        sns.heatmap(self.df.isnull(), cbar=False, cmap='viridis')
        plt.title('Heatmap of Missing Values')
        plt.tight_layout()
        plt.show()

    def plot_missing_values_comparison(self, original_df: pd.DataFrame):
        fig, axes = plt.subplots(1, 2, figsize=(20, 8))

        sns.heatmap(original_df.isnull(), cbar=False, cmap='viridis', ax=axes[0])
        axes[0].set_title('Original Missing Values')

        sns.heatmap(self.df.isnull(), cbar=False, cmap='viridis', ax=axes[1])
        axes[1].set_title('Missing Values After Removal')

        plt.tight_layout()
        plt.show()

    def plot_skewness_comparison(self, original_df: pd.DataFrame, transformed_df: pd.DataFrame, columns: list):
        n = len(columns)
        cols = 3
        rows = (n // cols) + (n % cols > 0)
        fig, axes = plt.subplots(rows, cols, figsize=(cols*6, rows*4))
        axes = axes.flatten()

        for i, column in enumerate(columns):
            sns.histplot(original_df[column].dropna(), kde=True, ax=axes[i])
            axes[i].set_title(f'Original {column}')
            axes[i].set_xlabel(column)
            axes[i].set_ylabel('Frequency')
            axes[i].tick_params(axis='x', rotation=45)

        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])
        
        fig.suptitle("Original Skewed Columns", fontsize=16)
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        plt.show()

        fig, axes = plt.subplots(rows, cols, figsize=(cols*6, rows*4))
        axes = axes.flatten()

        for i, column in enumerate(columns):
            sns.histplot(transformed_df[column].dropna(), kde=True, ax=axes[i])
            axes[i].set_title(f'Transformed {column}')
            axes[i].set_xlabel(column)
            axes[i].set_ylabel('Frequency')
            axes[i].tick_params(axis='x', rotation=45)

        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])
        
        fig.suptitle("Transformed Skewed Columns", fontsize=16)
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        plt.show()

    def plot_qq_plots(self, columns, title="QQ Plots"):
        n = len(columns)
        cols = 3
        rows = (n // cols) + (n % cols > 0)
        fig, axes = plt.subplots(rows, cols, figsize=(cols*6, rows*4))
        axes = axes.flatten()

        for i, column in enumerate(columns):
            stats.probplot(self.df[column].dropna(), dist="norm", plot=axes[i])
            axes[i].set_title(f'QQ Plot of {column}')
            axes[i].tick_params(axis='x', rotation=45)

        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])
        
        fig.suptitle(title, fontsize=16)
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        plt.show()

    def plot_boxplot(self, columns):
        n = len(columns)
        cols = 3
        rows = (n // cols) + (n % cols > 0)
        fig, axes = plt.subplots(rows, cols, figsize=(cols*6, rows*4))
        axes = axes.flatten()

        for i, column in enumerate(columns):
            sns.boxplot(x=self.df[column], ax=axes[i])
            axes[i].set_title(f'Box Plot of {column}')
            axes[i].set_xlabel(column)
            axes[i].tick_params(axis='x', rotation=45)

        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])

        plt.tight_layout()
        plt.show()

    def plot_boxplot_comparison(self, original_df: pd.DataFrame, cleaned_df: pd.DataFrame, columns):
        n = len(columns)
        cols = 2
        rows = (n // cols) + (n % cols > 0)
        fig, axes = plt.subplots(rows, cols, figsize=(cols*6, rows*4))
        axes = axes.flatten()

        for i, column in enumerate(columns):
            if i * 2 >= len(axes):
                break
            sns.boxplot(x=original_df[column], ax=axes[i * 2])
            axes[i * 2].set_title(f'Original {column}')
            axes[i * 2].set_xlabel(column)
            axes[i * 2].tick_params(axis='x', rotation=45)

            sns.boxplot(x=cleaned_df[column], ax=axes[i * 2 + 1])
            axes[i * 2 + 1].set_title(f'Cleaned {column}')
            axes[i * 2 + 1].set_xlabel(column)
            axes[i * 2 + 1].tick_params(axis='x', rotation=45)

        for j in range(i * 2 + 2, len(axes)):
            fig.delaxes(axes[j])

        plt.tight_layout()
        plt.show()
