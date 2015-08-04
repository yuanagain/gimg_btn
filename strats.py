""" Adjusts weights of analysts according to past performance, with parameters for learning """
import pyalgotrade
import numpy as np
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.tools import yahoofinance
from time import gmtime, strftime

from players import Analyst, Organization

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
        self.setUseAdjustedValues(True)

    def onBars(self, bars):
        if (self.first_pass == False): return
        weights = self.analyst.weights
        for instr in self.instruments:
            price = bars[instr].getClose()
            quantity = int(1000000 * weights[instr] / price)
            self.marketOrder(instr, quantity)
        self.first_pass = False

class OrgStrat(strategy.BacktestingStrategy):
    def __init__(self, feed, organization):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.first_pass = True
        self.organization = organization
        self.setUseAdjustedValues(True)

    def onBars(self, bars):
        if (self.first_pass == False): return
        weights = self.organization.get_weights()
        print self.organization.weights
        for instr in weights:
            price = bars[instr].getClose()
            quantity = int(1000000 * weights[instr] / price)
            self.marketOrder(instr, quantity)
        self.first_pass = False

def main1(plot):
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

    if plot:
        plt.plot()

def main(plot):
    al1 = Analyst('Ivy Kang')
    al1.assign_weight('cmg', 0.673)
    al1.assign_weight('aapl', 0.215)

    al2 = Analyst('Charlie Brown')
    al2.assign_weight('cmg', 0.420)
    al2.assign_weight('orcl', 0.130)
    al2.assign_weight('bk', 0.32)
    al2.assign_weight('bk', 0.40)
    al2.assign_weight('cmg', 0.30)

    org = Organization()
    org.add_analyst(al1)
    org.add_analyst(al2)

    # Download the bars.
    feed = yahoofinance.build_feed(org.get_weights().keys(), 2014, 2015, ".instr_data")

    strat = OrgStrat(feed, org)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)

    if plot:
        plt = plotter.StrategyPlotter(strat, True, False, True)

    strat.run()

    if plot:
        plt.plot()

class Epoch(object):
    def __init__(self, start_time):
        self.start_time = 0

def main0():
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

