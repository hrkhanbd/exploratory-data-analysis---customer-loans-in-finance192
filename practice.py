# db_utils.py

import yaml
from sqlalchemy import create_engine
import pandas as pd

class RDSDatabaseConnector:
    """
    A class used to connect to and extract data from an RDS database.
    """

    def __init__(self, credentials):
        """
        Initializes the RDSDatabaseConnector with database connection parameters.
        
        :param credentials: A dictionary containing the database credentials.
        """
        self.host = credentials['RDS_HOST']
        self.database = credentials['RDS_DATABASE']
        self.user = credentials['RDS_USER']
        self.password = credentials['RDS_PASSWORD']
        self.port = credentials['RDS_PORT']
        self.engine = self.create_engine()

    def create_engine(self):
        """
        Initializes a SQLAlchemy engine using the provided credentials.
        
        :return: A SQLAlchemy engine object.
        """
        connection_string = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        engine = create_engine(connection_string)
        return engine

    def load_data(self, table_name):
        """
        Loads data from the specified table in the database.
        
        :param table_name: The name of the table to query.
        :return: A Pandas DataFrame containing the table data.
        """
        query = f"SELECT * FROM {table_name}"
        with self.engine.connect() as connection:
            data = pd.read_sql(query, connection)
        return data

    def save_to_csv(self, dataframe, file_path):
        """
        Saves the DataFrame to a CSV file.
        
        :param dataframe: The Pandas DataFrame to save.
        :param file_path: The file path where the CSV file will be saved.
        """
        dataframe.to_csv(file_path, index=False)

    def load_from_csv(self, file_path):
        """
        Loads data from a CSV file into a Pandas DataFrame.
        
        :param file_path: The file path of the CSV file.
        :return: A Pandas DataFrame containing the data from the CSV file.
        """
        dataframe = pd.read_csv(file_path)
        print(f"Data shape: {dataframe.shape}")
        print("Data sample:")
        print(dataframe.head())
        return dataframe

def load_credentials(file_path):
    """
    Loads the database credentials from a YAML file.
    
    :param file_path: The path to the YAML file containing the credentials.
    :return: A dictionary with the credentials.
    """
    with open(file_path, 'r') as file:
        credentials = yaml.safe_load(file)
    return credentials

# Example usage
if __name__ == "__main__":
    # Use the actual file path for the credentials.yaml file
    credentials = load_credentials('D:\\Aicore\\EDA_Project\\exploratory-data-analysis---customer-loans-in-finance192\\credentials.yaml')
    db_connector = RDSDatabaseConnector(credentials)
    
    # Load data from the loan_payments table
    data = db_connector.load_data('loan_payments')
    print(data.head())  # Print the first few rows of the DataFrame
    
    # Save the data to a CSV file in the specified directory
    csv_file_path = 'D:\\Aicore\\EDA_Project\\exploratory-data-analysis---customer-loans-in-finance192\\loan_payments.csv'
    db_connector.save_to_csv(data, csv_file_path)
    print(f"Data saved to {csv_file_path}")
    
    # Load data from the CSV file
    loaded_data = db_connector.load_from_csv(csv_file_path)
