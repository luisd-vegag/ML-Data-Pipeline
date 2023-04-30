import unittest
from preprocess_data import preprocess_data

class TestPreprocessData(unittest.TestCase):
    def test_preprocess_data(self):
        input_path = 'data/raw/Data/Stocks'
        output_path = 'data/processed/stocks.parquet'
        preprocess_data(input_path, output_path)

        # TODO: Add assertions to verify the correctness of the processed data
