from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

class StockMarketData(BaseModel):
    vol_moving_avg: float
    adj_close_rolling_med: float

@app.post('/predict')
def predict(data: StockMarketData):
    # Load the trained model
    model = joblib.load('path/to/trained/model.pkl')

    # Create a Pandas DataFrame from the input data
    input_data = pd.DataFrame([{
        'vol_moving_avg': data.vol_moving_avg,
        'adj_close_rolling_med': data.adj_close_rolling_med
    }])

    # Make predictions using the trained model
    predictions = model.predict(input_data)

    # Return the predicted value
    return int(predictions[0])
