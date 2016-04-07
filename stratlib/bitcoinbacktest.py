# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 13:06:56 2015

@author: Eunice
"""

if __name__ == '__main__':
    import sys
    sys.path.append("..")
    from pyalgotrade import bar
    from pyalgotrade import plotter
# 以上模块仅测试用
from pyalgotrade.broker.fillstrategy import DefaultStrategy
from pyalgotrade.broker.backtesting import TradePercentage
from pyalgotrade import strategy
from pyalgotrade.technical import macd
import matplotlib.pyplot as plt
from pyalgotrade.dataseries import SequenceDataSeries
from pyalgotrade.broker.backtesting import TradePercentage
from pyalgotrade.technical import bollinger
from pyalgotrade.technical import cross
from pyalgotrade.strategy.position import ShortPosition
from pyalgotrade.strategy.position import LongPosition

class bollinger_band(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, bollingerlength, numStdDev):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.getBroker().setFillStrategy(DefaultStrategy(None))
        self.getBroker().setCommission(TradePercentage(0))
        self.__instrument = instrument
        self.__bollingerlength = int(bollingerlength)
        self.__close = feed[instrument].getPriceDataSeries()
        numStdDev = float(numStdDev) / 10
        self.__longPos = []
        self.__macd=macd.MACD(self.__close,50,150,10)
        self.__bollinger = bollinger.BollingerBands(self.__macd, self.__bollingerlength, int(numStdDev))
        self.__UpperBand = self.__bollinger.getUpperBand()
        self.__LowerBand = self.__bollinger.getLowerBand()

        self.__position = SequenceDataSeries()
        self.__circ=5
    def getPrice(self):
        return self.__prices

    def getMACD(self):
        return self.__macd

    def getBollingerBands(self):
        return self.__bollinger

    def testCon(self):
        # record position
        #######################################################################
        if len(self.__longPos) > 0:
            self.__position.append(len(self.__longPos))
        elif len(self.__longPos)==0 :
            self.__position.append(0)
            #print(0)


    def getTest(self):
        return self.__position

    def onBars(self, bars):
        bar = bars[self.__instrument]
        lower = self.__bollinger.getLowerBand()[-1]
        upper = self.__bollinger.getUpperBand()[-1]
       # print(self.getActivePositions())
        if lower is None:
            return
        self.testCon()
        if len(self.__longPos)> 0:
            if self.exitLongSignal():
               for pos in self.__longPos:
                   pos.exitMarket()
        elif len(self.__longPos)<5 :
            if self.enterLongSignal():
                shares =1
               # self.__longPos.
                self.__longPos.append(self.enterLong(self.__instrument, shares))

    def enterLongSignal (self) :
        if self.__UpperBand[-1-self.__circ] is None:
            return False
        m1 = 0
        for i in range(self.__circ):
            if self.__macd[-i-1] <= self.__LowerBand[-i-2]:
                m1 += 1
        if m1 >= self.__circ-1 and cross.cross_above(self.__macd,self.__LowerBand)>0:
            return True
        else:
            return False

    def enterShortSignal(self) :
        if self.__UpperBand[-1-self.__circ] is None:
            return False
        m1 = 0
        for i in range(self.__circ):
            if self.__macd[-i-1] >= self.__UpperBand[-i-2]:
                m1 += 1
        if m1 >= self.__circ-1 and cross.cross_below(self.__macd,self.__UpperBand)>0:
            return True
        else:
            return False

    def exitLongSignal(self) :
        if self.__UpperBand[-1-self.__circ] is None:
            return False
        m1 = 0
        for i in range(self.__circ):
            if self.__macd[-i-1] >= self.__UpperBand[-i-2]:
                m1 += 1
        if m1 >= self.__circ-1 and cross.cross_below(self.__macd,self.__UpperBand)>0:
            return True
        else:
            return False

    def exitShortSignal(self):
        if self.__UpperBand[-1-self.__circ] is None:
            return False
        m1 = 0
        for i in range(self.__circ):
            if self.__macd[-i-1] <= self.__LowerBand[-i-2]:
                m1 += 1
        if m1 >= self.__circ-1 and cross.cross_above(self.__macd,self.__LowerBand)>0:
            return True
        else:
            return False


    def onEnterCanceled(self, position):
        if len(self.__longPos)>0:
            if self.__longPos[-1] == position:
                del self.__longPos[-1]
        #else:
            #assert(False)

    def onEnterOK(self,position):
        pass

    def onExitOk(self, position):
        if isinstance(position,LongPosition):
            self.__longPos = []
        else:
            assert(False)

    def onExitCanceled(self, position):
        position.exitMarket()

if __name__ == "__main__":
    strat = bollinger_band
    instrument = 'btc'
    market = 'SZ'
    date = '2016-03-11'
    #toDate ='20160101'
    frequency = bar.Frequency.SECOND
    paras = [300, 26]

    plot = True

    #############################################path set ############################33
    if frequency == bar.Frequency.MINUTE:
        path = "..\\histdata\\min\\"
    elif frequency == bar.Frequency.DAY:
        path = "..\\histdata\\day\\"
    elif frequency == bar.Frequency.SECOND:
        path = "..\\histdata\\tick\\"
    filepath = path +"btc_2016-02-25.csv"

    #############################################don't change ############################33
    from pyalgotrade.barfeed.csvfeed import GenericBarFeed


    barfeed = GenericBarFeed(frequency)
    barfeed.setDateTimeFormat('%Y-%m-%d %H:%M:%S')
    barfeed.addBarsFromCSV(instrument, filepath)
    strat = strat(barfeed, instrument, *paras)
    if plot:
        plt = plotter.StrategyPlotter(strat)

        position = strat.getTest()
        plt.getOrCreateSubplot("position").addDataSeries("position", position)
        plt.getOrCreateSubplot("macd").addDataSeries('macd',strat.getMACD())
        plt.getOrCreateSubplot("macd").addDataSeries("upper", strat.getBollingerBands().getUpperBand())
        plt.getOrCreateSubplot("macd").addDataSeries("middle", strat.getBollingerBands().getMiddleBand())
        plt.getOrCreateSubplot("macd").addDataSeries("lower", strat.getBollingerBands().getLowerBand())
        #position = strat.getTest()
        #plt.getOrCreateSubplot("position").addDataSeries("position", position)
        #plt.getOrCreateSubplot("macd").addDataSeries('macd2',strat.getMACD2())
    strat.run()

    if plot:
        plt.plot()
































