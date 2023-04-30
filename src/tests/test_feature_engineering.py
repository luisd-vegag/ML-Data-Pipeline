import unittest
from feature_engineering import feature_engineering

class TestFeatureEngineering(unittest.TestCase):
    def test_feature_engineering(self):
        input_path = 'data/processed/stocks.parquet'
        output_path = 'data/processed/stocks_fe.parquet'
        feature_engineering(input_path, output_path)

        # TODO: Add assertions to verify the correctness of the feature engineered data

