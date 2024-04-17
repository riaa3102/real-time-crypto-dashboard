import os
from dotenv import load_dotenv
import hopsworks
from hsfs.client.exceptions import RestAPIError
import pandas as pd
from datetime import datetime, timedelta
from src.utils.logger import configure_logger
from src.backend.CryptocurrencyDataFetcher import CryptocurrencyDataFetcher

load_dotenv()


class FeatureStoreManager:
    def __init__(self, feature_store_name="cryptocurrency_dashboard_featurestore"):
        self.logger = configure_logger(name='FeatureStoreManager', log_level="INFO")
        self.feature_store_name = feature_store_name
        self.project = self.login_to_hopsworks()
        self.feature_store = self.project.get_feature_store(name=self.feature_store_name)
        self.feature_group = None

    def login_to_hopsworks(self):
        self.logger.info("Logging in to Hopsworks.")
        project = hopsworks.login()
        self.logger.info("Logged in successfully.")
        return project

    def get_or_create_feature_group(self, feature_group_name="crypto_prices", description="Cryptocurrency Data"):
        try:
            self.feature_group = self.feature_store.get_feature_group(
                name=feature_group_name,
                # version=1,
            )
            self.logger.info(f"Feature group '{feature_group_name}' retrieved successfully.")
        except RestAPIError:
            self.logger.info(f"Feature group '{feature_group_name}' not found. Creating new one.")
            self.feature_group = self.feature_store.get_or_create_feature_group(
                name=feature_group_name,
                description=description,
                version=1,
                primary_key=['timestamp'],
                online_enabled=True,
            )

    def initialize_feature_group_with_data(self):
        self.logger.info("Initializing feature group with data.")
        fetcher = CryptocurrencyDataFetcher("BTCUSDT")
        today = datetime.today().strftime('%d-%m-%Y')
        yesterday = (datetime.today() - timedelta(days=1)).strftime('%d-%m-%Y')
        data = fetcher.fetch_cryptocurrency_data(yesterday, today)
        if data:
            self.store_feature_data(data)
            self.logger.info("Initial data populated successfully.")
        else:
            self.logger.error("Failed to fetch initial data for feature group initialization.")

    def store_feature_data(self, data):
        if self.feature_group:
            try:
                data_df = pd.DataFrame(data)
                self.feature_group.insert(data_df,
                                          # overwrite=False
                                          )
                self.logger.info("Data stored successfully in the feature group.")
            except Exception as e:
                self.logger.error(f"Error storing data in feature group: {str(e)}")
        else:
            self.logger.error("Feature group not found.")


# if __name__ == "__main__":
#     # Initialize the feature store manager
#     manager = FeatureStoreManager()
#     # Test creating or retrieving a feature group
#     manager.get_or_create_feature_group("crypto_prices_test", "Test group for crypto prices")
#     print(f"Feature group created or retrieved: {manager.feature_group.name}")
#     # Optionally, populate it with some test data
#     manager.initialize_feature_group_with_data()
