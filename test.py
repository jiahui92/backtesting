from backtesting import Backtest, Strategy
from backtesting.lib import crossover, Sequence
from backtesting.test import SMA, GOOG
import pandas_datareader as pdr
import pandas as pd
import numpy

def BOLL(arr: pd.Series, type: str) -> pd.Series:
    """
    Returns `n`-period simple moving average of array `arr`.
    20天、平均数、方差
    """
    list = pd.Series(arr).rolling(20)
    mean = list.mean()
    var = list.var()
    if type == 'high': return mean + var
    if type == 'low': return mean - var
    if type == 'middle': return mean
    return mean

def willCrossover(series1: Sequence, series2: Sequence) -> bool:
    try:
        if series1[-3] > series2[-3] or series1[-2] > series2[-2]: return False
        diff3 = series2[-3] - series1[-3]
        diff2 = series2[-2] - series1[-2]
        # diff1 = series2[-1] - series1[-1]
        return diff3 > diff2 and series1[-2] + (diff3 - diff2) > series2[-2]
        # return diff3 > diff2 and series1[-2] + (diff3 - diff2) > series2[-2] and crossover(series1, series2)
    except IndexError:
        return False


class SmaCross(Strategy):
    def init(self):
        closePrice = self.data.Close
        self.ma1 = self.I(SMA, closePrice, 5, plot=True)
        self.ma2 = self.I(SMA, closePrice, 10, plot=True)
        # self.ma3 = self.I(SMA, closePrice, 60)
        self.boll1 = self.I(BOLL, closePrice, 'low')
        self.boll2 = self.I(BOLL, closePrice, 'middle')
        self.boll3 = self.I(BOLL, closePrice, 'high')

    def next(self):
        # if crossover(self.ma1, self.ma2):
        # if crossover(self.ma1, self.ma2) and self.data.Close[-1] / self.boll1[-1] < 1.1:
        if crossover(self.ma1, self.ma2) and self.data.Close[-1] / self.boll1[-1] < 1.1 and self.boll3[-1] / self.data.Close[-1] > 1.05: # MA5上穿MA10 and 靠近boll.bottom and 距离boll.high比较大
            self.buy()
        elif crossover(self.ma2, self.ma1):
            # self.sell() # 做空
            self.position.close() # 卖掉仓位

# https://finance.yahoo.com/quote/600036.SS/history?period1=1640980800&period2=1672603199&interval=1d&frequency=1d&filter=history
# data = pdr.get_data_yahoo('600036.SS', '1/1/2022', '1/1/2023')
data = pd.read_csv('./data/600036.SS.csv', index_col="Date", parse_dates=True, skiprows=lambda x: False)
data = data[-1300:-1050] #2018
# data = data[-1050:-800] #2019
# data = data[-750:-550] #2020
# data = data[-500:-300] #2021
# data = data[-283:-22] #2022
bt = Backtest(data, SmaCross, cash=100_000, commission=.0025,
              exclusive_orders=True)
stats = bt.run()
bt.plot()

print(stats['_trades'])
