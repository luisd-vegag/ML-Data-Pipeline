import os
import pandas as pd

def preprocess_data(input_path, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = pd.read_csv(input_path)
    # Rename columns
    df = df.rename(columns={'tic': 'Symbol', 'datadate': 'Date', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'adjcp': 'Adj Close', 'volume': 'Volume', 'name': 'Security Name'})
    # Convert date column to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
    # Save the preprocessed data to a structured format
    df.to_parquet(output_path)

if __name__ == '__main__':
    input_path = 'data/raw/Data/Stocks'
    output_path = 'data/processed/stocks.parquet'
    preprocess_data(input_path, output_path)
