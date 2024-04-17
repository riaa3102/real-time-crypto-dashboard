import os
import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go
from src.backend.CryptocurrencyDataFetcher import CryptocurrencyDataFetcher
from src.backend.FeatureStoreManager import FeatureStoreManager
from src.utils.logger import configure_logger


class DashboardApp:
    def __init__(self):
        self.logger = configure_logger(name='DashboardApp', log_level="INFO")
        self.feature_store_manager = FeatureStoreManager()
        self.feature_store_manager.get_or_create_feature_group(feature_group_name="crypto_prices_")
        self.setup()

    @staticmethod
    def setup():
        st.set_page_config(page_title="Real-Time Cryptocurrency OHLC Dashboard", page_icon="💲", layout="wide")
        st.title("Real-Time Cryptocurrency OHLC Dashboard")

    def main(self):
        with st.form("data_input_form"):
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            with col1:
                symbol = st.selectbox('Select cryptocurrency symbol:', ["BTCUSDT", "ETHUSDT"], index=0)
            with col2:
                date_from = st.date_input("From date", datetime.today() - timedelta(days=1))
            with col3:
                date_to = st.date_input("To date", datetime.today())
            with col4:
                st.markdown('<style>div.row-widget.stButton>button{margin-top:13px;}</style>', unsafe_allow_html=True)
                submit_button = st.form_submit_button('Refresh Data')

            if submit_button:
                self.refresh_data(symbol, date_from, date_to)

        self.display_data(symbol)

    def refresh_data(self, symbol, date_from, date_to):
        fetcher = CryptocurrencyDataFetcher(symbol)
        data = fetcher.fetch_cryptocurrency_data(date_from.strftime("%d-%m-%Y"), date_to.strftime("%d-%m-%Y"))
        if data:
            self.feature_store_manager.store_feature_data(data)
            st.success('Data refreshed successfully!')
        else:
            st.error('Failed to fetch new data.')

    def get_ohlc_data(self, symbol):
        """
        Fetch OHLC data from the feature store for visualization.
        """
        try:
            ohlc_data_df = self.feature_store_manager.feature_group.read()
        except Exception as e:
            print("Failed to read using ArrowFlight, attempting fallback to Hive:", str(e))
            try:
                # Fallback to Hive reading
                ohlc_data_df = self.feature_store_manager.feature_group.read(
                    # {"arrow_flight_config": {"timeout": 900}},
                    read_options={"use_hive": True},
                )
            except Exception as ex:
                raise Exception("Failed to read data even with Hive fallback:", str(ex))
        return ohlc_data_df[ohlc_data_df['symbol'] == symbol]

    def display_data(self, symbol):
        ohlc_data_df = self.get_ohlc_data(symbol)
        col1, col2 = st.columns([0.6, 0.4], gap="small")
        with col1:
            st.header(f"OHLC Data for {symbol}")
            if not ohlc_data_df.empty:
                fig = go.Figure(data=go.Ohlc(x=ohlc_data_df['timestamp'],
                                             open=ohlc_data_df['open'],
                                             high=ohlc_data_df['high'],
                                             low=ohlc_data_df['low'],
                                             close=ohlc_data_df['close']))
                fig.update_layout(
                    xaxis_title='Time',
                    yaxis_title='Price',
                    xaxis_rangeslider_visible=False)
                st.plotly_chart(fig)
            else:
                st.write("No data available for the selected cryptocurrency symbol.")
        with col2:
            st.header("Detailed Data View")
            if not ohlc_data_df.empty:
                st.dataframe(ohlc_data_df)
            else:
                st.write("No data available for the selected cryptocurrency symbol.")


if __name__ == "__main__":
    app = DashboardApp()
    # ----------------------------------------------------------------
    # date_from = datetime.strptime("2024-04-10", "%Y-%m-%d")
    # date_to = datetime.strptime("2024-04-10", "%Y-%m-%d")
    # symbol = "BTCUSDT"
    # app.refresh_data(symbol, date_from, date_to)
    # # ----------------------------------------------------------------
    # data_df = app.get_ohlc_data(symbol)
    # # print(data_df.shape)
    # print(data_df.head())
    # # ----------------------------------------------------------------
    # exit()
    # ----------------------------------------------------------------
    app.main()
