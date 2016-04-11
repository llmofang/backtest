from tickbarfeed.tickcsvfeed import TickBarFeed

from pyalgotrade import strategy
from tickbarfeed import TickBar


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info(bar.getDateTime())

if __name__ == "__main__":
    # Load the yahoo feed from the CSV file
    frequency = TickBar.Frequency.SECOND

    feed = TickBarFeed(frequency)
    #读取的数据 datetime不能重复 datetime 是由nactionday+ntime 组成 确保datetime是唯一的
    feed.addBarsFromCSV("000738", "../histdata/tick/stock_2016-02-26_tick2_processed.csv")

    # Evaluate the strategy with the feed's bars.
    myStrategy = MyStrategy(feed, "000738")
    myStrategy.run()