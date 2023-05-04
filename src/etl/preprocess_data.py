import os
import pandas as pd


def preprocess_data(input_path, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    dfs = []  # A list to store the DataFrames
    files = sorted(os.listdir(input_path))
    n_files = len(files)
    n_chunks = 20
    chunk_size = n_files // n_chunks + 1

    for i in range(0, n_files, chunk_size):
        chunk_files = files[i : i + chunk_size]
        for filename in chunk_files:
            if filename.endswith(".csv"):
                filepath = os.path.join(input_path, filename)
                df = pd.read_csv(filepath)
                # Add the tic as a column in the DataFrame
                df["tic"] = os.path.splitext(filename)[0]
                # Rename columns
                df = df.rename(
                    columns={
                        "tic": "Symbol",
                        "datadate": "Date",
                        "open": "Open",
                        "high": "High",
                        "low": "Low",
                        "close": "Close",
                        "adjcp": "Adj Close",
                        "volume": "Volume",
                        "name": "Security Name",
                    }
                )
                # Convert date column to datetime
                df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")

                dfs.append(df)

        # Concatenate the DataFrames into a single DataFrame
        df_concat = pd.concat(dfs)

        # Save the preprocessed data to a structured format
        output_file = output_path.format(i // chunk_size)
        df_concat.to_parquet(output_file)

        # Clear the list of DataFrames
        dfs.clear()

    # Merge all the parquet files into a single parquet file
    # parquet_files = [
    #    f for f in os.listdir(os.path.dirname(output_path)) if f.endswith(".parquet")
    # ]
    # if len(parquet_files) > 1:
    #    dfs = []
    #    for file in parquet_files:
    #        file_path = os.path.join(os.path.dirname(output_path), file)
    #        df = pd.read_parquet(file_path)
    #        dfs.append(df)
    #    df_concat = pd.concat(dfs)
    #    df_concat.to_parquet(output_path)
    #    # Remove the intermediate parquet files
    #    for file in parquet_files:
    #        os.remove(os.path.join(os.path.dirname(output_path), file))

    ## Rename the final output file
    # final_output_file = output_path.replace("_{}", "")  # Remove the "_{}" placeholder
    # os.rename(output_path, final_output_file)


if __name__ == "__main__":
    input_path = "data/raw/stocks"
    output_path = "data/processed/stocks_{}.parquet"
    preprocess_data(input_path, output_path)
