import os
import pandas as pd

def feature_engineering(input_path, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = pd.read_parquet(input_path)
    # Calculate the rolling average of the trading volume for each stock and ETF
    df['vol_moving_avg'] = df.groupby('Symbol')['Volume'].rolling(window=30, min_periods=1).mean().reset_index(0, drop=True)
    # Calculate the rolling median of the adjusted closing price for each stock and ETF
    df['adj_close_rolling_med'] = df.groupby('Symbol')['Adj Close'].rolling(window=30, min_periods=1).median().reset_index(0, drop=True)
    # Save the feature engineered data to the same structured format
    df.to_parquet(output_path)

if __name__ == '__main__':
    input_path = 'data/processed/
