""" Adjusts weights of analysts according to past performance, with parameters for learning """
import pyalgotrade
import numpy as np
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.tools import yahoofinance
from time import gmtime, strftime

from weights import Analyst, Organization

from pyalgotrade import strategy
from pyalgotrade import plotter
from pyalgotrade.technical import vwap
from pyalgotrade.stratanalyzer import sharpe


class HoldStrat(strategy.BacktestingStrategy):
    def __init__(self, feed, instruments, analyst):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.instruments = instruments
        self.first_pass = True
        self.analyst = analyst

    def onBars(self, bars):
        if (self.first_pass == False): return
        weights = self.analyst.weights
        for instr in self.instruments:
            price = bars[instr].getClose()
            quantity = 1000000 * weights[instr] / price
            self.marketOrder(instr, quantity)
        self.first_pass = False
        # shares = self.getBroker().getShares(self.__instrument)
        # price = bars[self.__instrument].getClose()
        # notional = shares * price

        # if price > vwap * (1 + self.__threshold) and notional < 1000000:
        #     self.marketOrder(self.__instrument, 100)
        # elif price < vwap * (1 - self.__threshold) and notional > 0:
        #     self.marketOrder(self.__instrument, -100)

def main(plot):
    al1 = Analyst('Ivy Kang')
    al1.assign_weight('bk', 0.473)
    al1.assign_weight('cmg', 0.215)
    al1.assign_weight('aapl', 0.180)
    instruments = []
    for key in al1.weights:
        instruments.append(key)

    # Download the bars.
    feed = yahoofinance.build_feed(instruments, 2014, 2015, ".instr_data")

    strat = HoldStrat(feed, instruments, al1)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)

    if plot:
        plt = plotter.StrategyPlotter(strat, True, False, True)

    strat.run()
    al1.status()

    if plot:
        plt.plot()



class Epoch(object):
    def __init__(self, start_time):
        self.start_time = 0

def main2():
    """Tests functionality of classes"""
    instruments = ['cmg', 'aapl', 'orcl', 'bk']
    feed = yahoofinance.build_feed(instruments, 2011, 2012, "instr_data")
    al1 = Analyst('Ivy Kang')
    al1.assign_weight('cmg', 0.673)
    al1.assign_weight('aapl', 0.215)

    al2 = Analyst('Charlie Brown')
    al2.assign_weight('cmg', 0.420)
    al2.assign_weight('orcl', 0.130)
    al2.assign_weight('bk', 0.32)

if __name__ == "__main__":
    main(True)

