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
import numpy as np
from datetime import datetime

class bollinger_band(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, bollingerlength, numStdDev):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.getBroker().setFillStrategy(DefaultStrategy(None))
        self.getBroker().setCommission(TradePercentage(0.0008))
        self.__instrument = instrument
        self.__bollingerlength = int(bollingerlength)
        self.__close = feed[instrument].getPriceDataSeries()
        numStdDev = float(numStdDev) / 10
        self.__longPos = []
        self.__shortPos = []
        self.__bollinger = bollinger.BollingerBands(self.__close, self.__bollingerlength, int(numStdDev))
        self.__UpperBand = self.__bollinger.getUpperBand()
        self.__LowerBand = self.__bollinger.getLowerBand()
        self.__position = SequenceDataSeries()
        self.__circ=5
        self.__lastLongPos=None
        self.__lastShortPos=None
        self.__barNum=0
    def getPrice(self):
        return self.__prices

    def getBollingerBands(self):
        return self.__bollinger

    def testCon(self):
        # record position
        #######################################################################
        if len(self.__longPos) > 0:
            self.__position.append(len(self.__longPos))
        if len(self.__shortPos)>0 :
            #print(self.__shortPos.getShares())
            self.__position.append(-len(self.__shortPos))
        elif len(self.__longPos)==0 and len(self.__shortPos)==0:
            self.__position.append(0)
            #print(0)


    def getTest(self):
        return self.__position

    def onBars(self, bars):
        bar = bars[self.__instrument]
        lower = self.__bollinger.getLowerBand()[-1]
        upper = self.__bollinger.getUpperBand()[-1]
        self.__barNum=self.__barNum+1
       # print(self.getActivePositions())

        if lower is None or upper is None:
            return
        self.testCon()
        if len(self.__longPos)> 0:

            if self.exitLongSignal():
               for pos in self.__longPos:
                   pos.exitMarket()

        elif len(self.__shortPos)>0:

            if self.exitShortSignal():
                for pos in self.__shortPos:
                   pos.exitMarket()

        if self.enterLongSignal():
            for i in range(self.enterLongSignal()):
                shares = int(self.getBroker().getEquity() * 0.2 / bars[self.__instrument].getPrice())
           # self.__longPos.
                self.__longPos.append(self.enterLong(self.__instrument, shares))
            self.__lastLongPos=self.__barNum
            #print('long'+str(shares))

        elif self.enterShortSignal():
            for i in range(self.enterShortSignal()):
                shares = int(self.getBroker().getEquity() * 0.2 / bars[self.__instrument].getPrice())
                self.__shortPos.append(self.enterShort(self.__instrument, shares))
            self.__lastShortPos=self.__barNum
            #print('short'+str(shares))

    def enterLongSignal (self) :
        if self.__lastLongPos is not None:
            if self.__barNum-self.__lastLongPos<60:
                return 0
        if self.__UpperBand[-1-self.__circ] is None:
            return 0
        m1 = 0
        for i in range(self.__circ):
            if self.__close[-i-1] <= self.__LowerBand[-i-2]:
                m1 += 1
        if m1 >= self.__circ-1 and cross.cross_above(self.__close,self.__LowerBand)>0:
                 return 1
        else:
            return 0

    def enterShortSignal(self) :
        if self.__lastShortPos is not None:
            if self.__barNum-self.__lastShortPos<60:
                return 0
        if self.__UpperBand[-1-self.__circ] is None:
            return 0
        m1 = 0
        for i in range(self.__circ):
            if self.__close[-i-1] >= self.__UpperBand[-i-2]:
                m1 += 1
        if m1 >= self.__circ-1 and cross.cross_below(self.__close,self.__UpperBand)>0:
            return 1
        else:
            return 0

    def exitLongSignal(self) :
        if self.__UpperBand[-1-self.__circ] is None:
            return False
        m1 = 0
        for i in range(self.__circ):
            if self.__close[-i-1] >= self.__UpperBand[-i-2]:
                m1 += 1
        if m1 >= self.__circ-1 and cross.cross_below(self.__close,self.__UpperBand)>0:
            return True
        else:
            return False

    def exitShortSignal(self):
        if self.__UpperBand[-1-self.__circ] is None:
            return False
        m1 = 0
        for i in range(self.__circ):
            if self.__close[-i-1] <= self.__LowerBand[-i-2]:
                m1 += 1
        if m1 >= self.__circ-1 and cross.cross_above(self.__close,self.__LowerBand)>0:
            return True
        else:
            return False


    def onEnterCanceled(self, position):
        if self.__longPos[-1] == position:
            del self.__longPos[-1]
            self.__lastLongPos==None
        elif self.__shortPos[-1] == position:
            del self.__shortPos[-1]
            self.__lastShortPos==None
        else:
            assert(False)

    def onEnterOK(self,position):
        pass

    def onExitOk(self, position):
        if isinstance(position,LongPosition):
            self.__longPos = []
        elif isinstance(position,ShortPosition):
            self.__shortPos = []
        else:
            assert(False)

    def onExitCanceled(self, position):
        position.exitMarket()

if __name__ == "__main__":
    strat = bollinger_band
    instrument = '600016'
    market = 'SZ'
    date = '2016-03-11'
    #toDate ='20160101'
    frequency = bar.Frequency.SECOND
    paras = [450, 28]

    plot = True

    #############################################path set ############################33
    if frequency == bar.Frequency.MINUTE:
        path = "..\\histdata\\min\\"
    elif frequency == bar.Frequency.DAY:
        path = "..\\histdata\\day\\"
    elif frequency == bar.Frequency.SECOND:
        path = "..\\histdata\\tick\\"
    filepath = path +'stock_'+ instrument + "_"+date+".csv"

    #############################################don't change ############################33
    from pyalgotrade.barfeed.csvfeed import GenericBarFeed


    barfeed = GenericBarFeed(frequency)
    barfeed.setDateTimeFormat('%Y-%m-%d %H:%M:%S')
    barfeed.addBarsFromCSV(instrument, filepath)
    strat = strat(barfeed, instrument, *paras)
    if plot:
        plt = plotter.StrategyPlotter(strat)
        plt.getInstrumentSubplot(instrument).addDataSeries("upper", strat.getBollingerBands().getUpperBand())
        plt.getInstrumentSubplot(instrument).addDataSeries("middle", strat.getBollingerBands().getMiddleBand())
        plt.getInstrumentSubplot(instrument).addDataSeries("lower", strat.getBollingerBands().getLowerBand())
        position = strat.getTest()
        plt.getOrCreateSubplot("position").addDataSeries("position", position)
        #position = strat.getTest()
        #plt.getOrCreateSubplot("position").addDataSeries("position", position)
        #plt.getOrCreateSubplot("macd").addDataSeries('macd2',strat.getMACD2())
    strat.run()

    if plot:
        plt.plot()
































