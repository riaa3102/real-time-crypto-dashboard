import requests
from datetime import datetime, timedelta
from src.utils.logger import configure_logger


class CryptocurrencyDataFetcher:
    def __init__(self, symbol='BTCUSDT'):
        self.symbol = symbol
        self.logger = configure_logger(name='CryptocurrencyDataFetcher', log_level="INFO")

    def fetch_data_for_day(self, day):
        self.logger.info(f"Fetching data for {self.symbol} on {day.strftime('%Y-%m-%d')}")
        all_data = []
        start_of_day = datetime.combine(day, datetime.min.time())
        end_of_day = datetime.combine(day, datetime.max.time())
        start_timestamp = int(start_of_day.timestamp() * 1000)
        end_timestamp = int(end_of_day.timestamp() * 1000)

        url = "https://api.binance.com/api/v3/klines"
        while start_timestamp < end_timestamp:
            params = {
                'symbol': self.symbol,
                'interval': '1m',
                'startTime': start_timestamp,
                'endTime': min(start_timestamp + 500 * 60000, end_timestamp)
            }
            response = requests.get(url, params=params)
            data = response.json()
            transformed_data = self.transform_to_ohlc(data)
            all_data.extend(transformed_data)
            if len(data) < 500:
                break
            start_timestamp += 500 * 60000

        self.logger.info(f"Finished fetching data for {day.strftime('%Y-%m-%d')}")
        return all_data

    def fetch_cryptocurrency_data(self, date_from, date_to):
        start_date = datetime.strptime(date_from, "%d-%m-%Y").date()
        end_date = datetime.strptime(date_to, "%d-%m-%Y").date()
        delta = timedelta(days=1)

        all_data = []
        current_date = start_date
        while current_date <= end_date:
            day_data = self.fetch_data_for_day(current_date)
            all_data.extend(day_data)
            current_date += delta

        return all_data

    def transform_to_ohlc(self, data):
        ohlc_data = []
        for entry in data:
            timestamp = entry[0]
            open_price = entry[1]
            high = entry[2]
            low = entry[3]
            close = entry[4]
            volume = entry[5]
            ohlc_data.append({
                "timestamp": datetime.utcfromtimestamp(timestamp / 1000).strftime("%Y-%m-%d %H:%M:%S"),
                "open": float(open_price),
                "high": float(high),
                "low": float(low),
                "close": float(close),
                "volume": float(volume),
                "symbol": self.symbol
            })
        self.logger.debug(f"Transformed data for {self.symbol} with entries: {len(ohlc_data)}")
        return ohlc_data


# if __name__ == "__main__":
#     fetcher = CryptocurrencyDataFetcher(symbol="BTCUSDT")
#     test_date = datetime.strptime("2024-04-10", "%Y-%m-%d")
#     day_data = fetcher.fetch_data_for_day(test_date)
#     print(f"Data fetched for {test_date.strftime('%Y-%m-%d')}: \n{day_data[:5]}")
