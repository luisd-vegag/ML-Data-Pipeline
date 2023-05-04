import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


def process_parquet_file(file_path):
    data = pd.read_parquet(file_path)
    data.dropna(inplace=True)  # Drop rows with NaN values
    X = data[["vol_moving_avg", "adj_close_rolling_med"]]
    y = data["Volume"]
    return train_test_split(X, y, test_size=0.2, random_state=42)


def train_model(input_path, output_path):
    model = RandomForestRegressor(n_estimators=100, random_state=42)

    for dirpath, _, _ in os.walk(input_path):
        if "part.0.parquet" in os.listdir(dirpath):
            file_path = os.path.join(dirpath, "part.0.parquet")
            X_train, X_test, y_train, y_test = process_parquet_file(file_path)

            # Train the model incrementally
            model.fit(X_train, y_train)

    # Evaluate the model using the last read file
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean absolute error: {mae:.2f}")
    print(f"Mean squared error: {mse:.2f}")

    # Save the trained model
    joblib.dump(model, output_path)


if __name__ == "__main__":
    input_path = "data/processed_fe"
    output_path = "models/random_forest_regressor.pkl"
    train_model(input_path, output_path)
