import os
import pandas as pd
import dask.dataframe as dd
import gc
import multiprocessing


def process_symbol(symbol_df):
    # Calculate the rolling average of the trading volume
    symbol_df["vol_moving_avg"] = (
        symbol_df["Volume"].rolling(window=30, min_periods=1).mean()
    )

    # Calculate the rolling median of the adjusted closing price
    symbol_df["adj_close_rolling_med"] = (
        symbol_df["Adj Close"].rolling(window=30, min_periods=1).median()
    )

    return symbol_df


def feature_engineering(input_path, output_path, n_workers=4):
    os.makedirs(output_path, exist_ok=True)

    # Collect garbage and clear the memory cache
    gc.collect()

    # Get the paths of the Parquet files in the input directory
    files = [
        os.path.join(input_path, f)
        for f in os.listdir(input_path)
        if f.endswith(".parquet")
    ]

    for file in files:
        # Read the Parquet file into a Dask DataFrame
        ddf = dd.read_parquet(file, engine="pyarrow")

        # Apply the process_symbol function to each partition in parallel
        processed_ddf = ddf.map_partitions(process_symbol)

        # Save the feature engineered data to the same structured format
        output_file = os.path.join(output_path, os.path.basename(file))
        processed_ddf.to_parquet(output_file, compression="snappy", write_index=False)


if __name__ == "__main__":
    input_path = "data/processed"
    output_path = "data/processed_fe"
    num_cores = multiprocessing.cpu_count()
    feature_engineering(input_path, output_path, n_workers=num_cores)
