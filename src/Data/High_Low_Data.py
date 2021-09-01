from src.Data.Indicators import Indicators
from src.Data.data import Data
from src.Data.data_detection_algorithms import Core


class HighLowHistory(Indicators):
    def __init__(self, client, symbol):
        super().__init__(client, symbol)

        self.long = None

        self.bull_indexes, self.bear_indexes, self.fake_bull_indexes, self.fake_bear_indexes = \
            self.macd_trend_data()

        self.list_r = self.high_low_finder_v2()

        self.high_local, self.high_prices_indexes = self.list_r[0], self.list_r[1]
        self.high_wicks, self.high_wicks_indexes = self.list_r[2], self.list_r[3]
        self.high_macd, self.high_macd_indexes = self.list_r[4], self.list_r[5]

        self.low_local, self.low_prices_indexes = self.list_r[6], self.list_r[7]
        self.low_wicks, self.low_wicks_indexes = self.list_r[8], self.list_r[9]
        self.low_macd, self.low_macd_indexes = self.list_r[10], self.list_r[11]

    def macd_trend_data(self):
        last_macd_hist = self.data["Hist"].tail(self.study_range).values

        bull_indexes = []
        bear_indexes = []
        fake_bull = []
        fake_bear = []

        macd_trend = last_macd_hist[0]
        fake_macd_trend = macd_trend
        successive_hist_macd_bear = 0
        successive_hist_macd_bull = 0

        for i in range(self.study_range - 1):  # Fake bear and bull indexes
            if last_macd_hist[i] > 0 and fake_macd_trend < 0:
                fake_bull.append(i)
                fake_macd_trend = last_macd_hist[i]
            elif last_macd_hist[i] < 0 and fake_macd_trend > 0:
                fake_bear.append(i)
                fake_macd_trend = last_macd_hist[i]

            if last_macd_hist[i] > 0 and macd_trend < 0:  # Bull and bear indexes
                successive_hist_macd_bear = 0
                # croise bullish
                if successive_hist_macd_bull > self.n_plot_macd - 1:
                    # croise avec 4 macd hist plot
                    bull_indexes.append(i - self.n_plot_macd)
                    macd_trend = last_macd_hist[i - self.n_plot_macd]
                    successive_hist_macd_bull = 0
                else:
                    successive_hist_macd_bull += 1
            elif last_macd_hist[i] < 0 and macd_trend > 0:
                successive_hist_macd_bull = 0
                # croise bearish
                if successive_hist_macd_bear > self.n_plot_macd - 1:
                    bear_indexes.append(i - self.n_plot_macd)
                    macd_trend = last_macd_hist[i - self.n_plot_macd]
                    successive_hist_macd_bear = 0
                else:
                    successive_hist_macd_bear += 1
            else:
                successive_hist_macd_bear = 0
                successive_hist_macd_bull = 0

        return bull_indexes, bear_indexes, fake_bull, fake_bear

    def high_low_finder_v2(self):
        # TODO: Reduce the number of lines in high_low_finder_v2 using the latest Detector algorithms

        list_of_high_low = [[], [], [], [], [], [], [], [], [], [], [], []]

        prices = self.data['close'].tail(self.study_range).values  # Gotta find a workaround to avoid the last unclosed
        # candle.
        macd = self.data['Hist'].tail(self.study_range).values
        highs = self.data['high'].tail(self.study_range).values
        lows = self.data['low'].tail(self.study_range).values

        # list_data = [prices, highs, macd]

        lim_bull = len(self.bull_indexes)
        lim_bear = len(self.bear_indexes)

        j = 0
        while j < lim_bull:
            # high prices and macd

            temp_high_low, temp_index = Core.finder(j, self.bear_indexes, self.bull_indexes, prices, True)
            list_of_high_low[0].append(temp_high_low)
            list_of_high_low[1].append(temp_index)

            temp_high_low, temp_index = Core.finder(j, self.bear_indexes, self.bull_indexes, highs, True)
            list_of_high_low[2].append(temp_high_low)
            list_of_high_low[3].append(temp_index)

            temp_high_low, temp_index = Core.finder(j, self.bear_indexes, self.bull_indexes, macd, True)
            list_of_high_low[4].append(temp_high_low)
            list_of_high_low[5].append(temp_index)

            j += 1

        j = 0
        while j < lim_bear:
            # Low prices and macd

            temp_high_low, temp_index = Core.finder(j, self.bull_indexes, self.bear_indexes, prices, False)
            list_of_high_low[6].append(temp_high_low)
            list_of_high_low[7].append(temp_index)

            temp_high_low, temp_index = Core.finder(j, self.bull_indexes, self.bear_indexes, lows, False)
            list_of_high_low[8].append(temp_high_low)
            list_of_high_low[9].append(temp_index)

            temp_high_low, temp_index = Core.finder(j, self.bull_indexes, self.bear_indexes, macd, False)
            list_of_high_low[10].append(temp_high_low)
            list_of_high_low[11].append(temp_index)

            j += 1

        return list_of_high_low

    def macd_line_checker(self, index, long):
        last_macd_data = self.data['MACD'].tail(self.study_range - 1).values

        res = True
        i = 0
        a, b = Core.switcher(long, self.bull_indexes, self.bear_indexes)

        start = Core.macd_cross_detection(a, index)
        end = Core.macd_cross_detection(b, start)

        length = end - start

        while res and i < length:
            res = not Core.comparator_numbers(long, last_macd_data[i + start], 0)
            i += 1

        return res

    def indicators_init(self):
        self.ema_trend = self.ema(600)
        self.ema_fast = self.ema(150)

        self.macd()

        self.bull_indexes, self.bear_indexes, self.fake_bull_indexes, self.fake_bear_indexes = \
            self.macd_trend_data()

        self.list_r = self.high_low_finder_v2()

        self.high_local, self.high_prices_indexes = self.list_r[0], self.list_r[1]
        self.high_wicks, self.high_wicks_indexes = self.list_r[2], self.list_r[3]
        self.high_macd, self.high_macd_indexes = self.list_r[4], self.list_r[5]

        self.low_local, self.low_prices_indexes = self.list_r[6], self.list_r[7]
        self.low_wicks, self.low_wicks_indexes = self.list_r[8], self.list_r[9]
        self.low_macd, self.low_macd_indexes = self.list_r[10], self.list_r[11]

    def update_data(self):
        self.data = Data.download_data(self)
        self.indicators_init()