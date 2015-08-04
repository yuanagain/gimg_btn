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


class HoldStratA(strategy.BacktestingStrategy):
    def __init__(self, feed, analyst):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.instruments = analyst.get_instruments()
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

class HoldStratB(strategy.BacktestingStrategy):
    def __init__(self, feed, organization):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.first_pass = True
        self.organization = organization
        self.setUseAdjustedValues(True)

    def onBars(self, bars):
        if (self.first_pass == False): return
        weights = self.organization.get_weights()

        for instr in weights:
            price = bars[instr].getClose()
            quantity = int(1000000 * weights[instr] / price)
            self.marketOrder(instr, quantity)
        self.first_pass = False

class OrgStrat(strategy.BacktestingStrategy):
    def __init__(self, feed, organization, update = "geometric"):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.first_pass = True
        self.organization = organization
        self.setUseAdjustedValues(True)
        self.update = update
        self.first_pass = True

    def onBars(self, bars):
        if first_pass:
            return
        weights = self.organization.get_weights()
        if self.update == "geometric":
            self.geometric_update()
        broker = self.getBroker()

        for instr in weights:
            price = bars[instr].getClose()
            notion = int(1000000 * weights[instr] / price)
            current_holdings = broker.getShares(instr)

            order = notion - current_holdings
            self.marketOrder(instr, order)

    def geometric_update(self, bar):
        """Updates confidence in each analyst based on performance at the last epoch """
        # learning factor
        gamma = 0.5

        for analyst in self.organization.analysts:
            # evalute analyst performance in last epoch
            print 1
            # adjust confidence in analyst

def eval_analyst_performance(analyst, bar, bar):
    """Evaluates analyst's performance in a given interval"""


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

    strat = HoldStratA(feed, al1)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)

    if plot:
        plt = plotter.StrategyPlotter(strat, True, False, True)

    strat.run()

    if plot:
        plt.plot()

if __name__ == "__main__":
    main(True)

