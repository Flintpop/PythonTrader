import datetime as dt
import pandas as pd

from src.Miscellaneous.settings import Parameters


class Data:
    """
    This class initialize and download the latest plots from binance API.
    Several plots timeframe can be chosen.
    """
    def __init__(self, client, symbol, symbol_index):
        """
        Keep in memory several useful (and common to different strategies) attributes.
        Download the data and converts it to a "pandas.dataframe object".\n
        :param client: Binance API connect object : "Client(api_key, secret_key)"
        :param symbol: Trading pair symbol, i.e. : "BTCBUSD"
        :param symbol_index: Index of the list of the currently used trading pairs
        """
        settings = Parameters()
        self.symbol = symbol
        self.client = client
        self.interval_unit = settings.interval_unit

        self.data_range = settings.data_range
        self.study_range = settings.study_range
        self.n_plot_macd = settings.n_plot_macd[symbol_index]

        self.settings = settings

        self.data = self.download_data()

    def download_data(self):
        """
        Choose the correct timeframe relatively to the one in attribute chosen via settings object and download the
        latest data.\n
        :return: panda dataframe of the latest plots of a chosen symbol
        """
        if self.interval_unit == '1m':
            start_min = (self.data_range + 1)
            start_str = str(start_min) + ' minutes ago UTC'
        elif self.interval_unit == '5m':
            start_min = (self.data_range + 1) * 5
            start_str = str(start_min) + ' minutes ago UTC'
        elif self.interval_unit == '15m':
            start_min = (self.data_range + 1) * 15
            start_str = str(start_min) + ' minutes ago UTC'
        elif self.interval_unit == '30':
            start_min = (self.data_range + 1) * 30
            start_str = str(start_min) + ' minutes ago UTC'
        elif self.interval_unit == '1h':
            start_min = (self.data_range + 1)
            start_str = str(start_min) + ' hours ago UTC'
        elif self.interval_unit == '4h':
            start_min = (self.data_range + 1) * 4
            start_str = str(start_min) + ' hours ago UTC'
        else:
            raise ValueError("ERROR : Value of interval unit not specified in download_data in Data object function."
                  f"The value in question : {self.interval_unit}")

        data = self.download_raw_data_binance_api(start_str)

        return data

    def download_raw_data_binance_api(self, start_str):
        """
        Download directly the data in relationship to the start_str parameter. This parameter dictates the timeframe.\n
        :param start_str: Variable constructed via download_data of Data object.
        :return: pandas.DataFrame object of the latest plots.
        """
        data = pd.DataFrame(
            self.client.futures_historical_klines(symbol=self.symbol, start_str=start_str,
                                                  interval=self.interval_unit))

        data.columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'qav', 'num_trades',
                        'taker_base_vol', 'taker_quote_vol', 'is_best_match']
        data['open_date_time'] = [dt.datetime.fromtimestamp(x / 1000) for x in data.open_time]
        data = data[['open_date_time', 'open', 'high', 'low', 'close']]
        data['open'] = [float(x) for x in data['open']]
        data['high'] = [float(x) for x in data['high']]
        data['low'] = [float(x) for x in data['low']]
        data['close'] = [float(x) for x in data['close']]
        return data
