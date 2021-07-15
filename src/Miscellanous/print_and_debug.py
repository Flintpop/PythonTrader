import datetime as dt
import pandas as pd
from src.WatchTower import send_email

# datas = [[1, '2021-06-16 00:20:00', 104.96, 119.6544]] the data has to be this way.


def os_path_fix():
    import platform
    current_os = platform.system()
    if current_os == 'Windows':
        string = "src/Output/"
    else:
        string = "../Output/"

    return string


class LogMaster:
    def __init__(self):
        self.logs_path = os_path_fix() + "logs.txt"
        self.trade_path = os_path_fix() + "TradeHistory.csv"
        try:
            self.trade_data = self.get_data()
        except Exception as e:
            print("An error occurred")
            print(e)
            self.init_trade_history()
            print("Trade history initialized")
            self.trade_data = self.get_data()

    @staticmethod
    def init_trade_history():
        df = pd.DataFrame(columns=['win_loss', 'trade_enter_time', 'trade_close_time', 'money_traded', 'result_money'])
        df.to_csv('TradeHistory.csv', index=False)

    def init_log(self):
        f = open(self.logs_path, "w+")
        f.write("File created at : " + str(dt.datetime.now()) + "\n\n")
        f.close()
        f = open(self.logs_path, "a")
        f.write("Logs initialized.\n")
        f.close()

    def add_log(self, words):
        try:
            if type(words) == str:
                word_print = words.replace("\n", "")
                word = words
            elif type(words) == bool:
                word_print = words
                word = "\n\n" + str(words)
            else:
                word_print = words
                word = words
            print(word_print)
            f = open(self.logs_path, "a")
            f.write(str(word))
            f.close()
        except Exception as e:
            print(e)
            f = open(self.logs_path, "a")
            f.write("\n\n" + str(e))
            f.close()

    def get_data(self):
        r = pd.read_csv(self.trade_path)
        return r

    def append_trade_history(self, list_of_results: list):
        self.trade_data = self.get_data()
        list_of_results = pd.DataFrame(data=list_of_results, columns=['win_loss', 'trade_enter_time',
                                                                      'trade_close_time', 'money_traded',
                                                                      'result_money'])
        frames = [self.trade_data, list_of_results]
        self.trade_data = pd.concat(frames, ignore_index=True)
        self.trade_data.to_csv(self.trade_path, index=False)
        return pd.read_csv(self.trade_path)


class PrintUser:
    def __init__(self, coin_obj):
        self.debug_file_path = os_path_fix() + "debug_file.txt"
        self.logs_path = os_path_fix() + "logs.txt"
        self.trade_path = os_path_fix() + "TradeHistory.csv"

        self.data = coin_obj.data
        self.data_range = coin_obj.data_range
        self.study_range = coin_obj.study_range
        
        self.logs = LogMaster()

    def actualize_data(self, coin):
        self.data = coin.data
        self.data_range = coin.data_range
        self.study_range = coin.study_range

    def debug_macd_trend_data(self, bull_indexes, bear_indexes, fake_bull, fake_bear):
        bearish_time = []
        bullish_time = []
        fake_bull_time = []
        fake_bear_time = []

        for i in range(len(bull_indexes)):
            date = PrintUser.get_time(self, bull_indexes[i] - 1)
            bullish_time.append(date)
        print("MACD cross bullish at : ")
        print(bullish_time)
        for i in range(len(fake_bull)):
            date = PrintUser.get_time(self, fake_bull[i] - 1)
            fake_bull_time.append(date)
        print("MACD fake bullish at : ")
        print(fake_bull_time)

        for i in range(len(bear_indexes)):
            date = PrintUser.get_time(self, bear_indexes[i] - 1)
            bearish_time.append(date)
        print("MACD cross bearish at : ")
        print(bearish_time)
        for i in range(len(fake_bear)):
            date = PrintUser.get_time(self, fake_bear[i] - 1)
            fake_bear_time.append(date)
        print("MACD fake bearish at : ")
        print(fake_bear_time)

    def print_date_list(self, indexes):
        time_debug = []
        for i in range(len(indexes)):
            date = PrintUser.get_time(self, indexes[i])
            time_debug.append(date)
        return str(time_debug)

    def debug_divergence_finder(self, indexes, i, word):
        string_one = PrintUser.get_time(self, indexes[i])
        string_two = PrintUser.get_time(self, indexes[i + 1])
        
        string = "\n\nDivergence for " + word + " at : " + str(string_one) + " and " + str(string_two)
        self.logs.add_log(string)

    def debug_trade_parameters(self, sl, tp, entry_price, entry_price_index, long):
        log = self.logs.add_log
        date = PrintUser.get_time(self, entry_price_index)

        log("\n\n\nIt is a long ? | " + str(long))
        log("\nThe enter price is : " + str(entry_price) + " at : " + str(date))
        log("\nThe stop loss is : " + str(sl))
        log("\nThe take profit is : " + str(tp))

    def get_time(self, index):
        time_print = self.data['open_date_time']
        index = index + self.data_range - self.study_range + 2
        try:
            res = time_print[index]
        except Exception as e:
            print(e)
            res = time_print[len(time_print) - 1]
        return res

    def debug_file(self):
        f = open(self.debug_file_path, "w+")
        f.write("File created at : " + str(dt.datetime.now()))
        f.close()

    @staticmethod
    def trade_type_string(long):
        if long:
            res = "long"
        else:
            res = "short"
        return res

    @staticmethod
    def win_loss_string(win):
        if win:
            res = "win"
        else:
            res = "loss"
        return res

    @staticmethod
    def send_result_email(long, win, entry_price, time_pos_hit, time_pos_open):
        won = PrintUser.win_loss_string(win)
        word = PrintUser.trade_type_string(long)

        send_email(f"<p>Trade completed !</p>"
                   f"<p>It is a {str(word)}, and the trade is {str(won)}</p>"
                   f"<p>The entry price is {str(entry_price)} at : {str(time_pos_open)}</p>"
                   f"<p>The trade was closed at {str(time_pos_hit)} </p>")


if __name__ == '__main__':
    a = LogMaster()
    a.add_log(0 > 1)
