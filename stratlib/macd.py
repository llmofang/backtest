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
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross
from pyalgotrade.technical import macd
import matplotlib.pyplot as plt
from pyalgotrade.dataseries import SequenceDataSeries

class thrSMA(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, fast, slow, signal, up_cum):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.getBroker().setFillStrategy(DefaultStrategy(None))
        self.getBroker().setCommission(TradePercentage(0.0008))
        self.__longPos = None
        self.__shortPos = None
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__macd=macd.MACD(self.__prices,fast,slow,signal)
        self.__range=0
        self.__circ = int(up_cum)
        self.__position = SequenceDataSeries()
    def getPrice(self):
        return self.__prices

    def getMACD(self):
        return self.__macd

    def testCon(self):

        # record position
        #######################################################################
        if self.__longPos is not None:
            self.__position.append(1)
        if self.__shortPos is not None:
            self.__position.append(-1)
        elif self.__longPos is None and self.__shortPos is None:
            self.__position.append(0)


    def getTest(self):
        return self.__position

    def onEnterCanceled(self, position):
        if self.__longPos == position:
            self.__longPos = None
        elif self.__shortPos == position:
            self.__shortPos = None
        else:
            assert(False)

    def onEnterOK(self):
        pass

    def onExitOk(self, position):
        if self.__longPos == position:
            self.__longPos = None
        elif self.__shortPos == position:
            self.__shortPos = None
        else:
            assert(False)

    def onExitCanceled(self, position):
        position.exitMarket()
        
    def buyCon1(self):
        if self.__macd[-1] < -self.__range:
            #print(self.__macd[-1])
            return True
        else:
            return False

    def buyCon2(self):
        if  self.__macd[-1-self.__circ] is None:
            return False
        m1 = 0
        for i in range(self.__circ):
            if self.__macd[-i-1] > self.__macd[-i-2]:
                m1 += 1
        if m1 >= self.__circ:
            return True
        else:
            return False

    def exitLongCon1(self):
        if self.__macd[-1]>0:
            return True
        else:
            return False

    def exitLongCon2(self):
        if  self.__macd[-1-self.__circ] is None:
            return False
        m1 = 0
        for i in range(self.__circ):
            if self.__macd[-i-1] < self.__macd[-i-2]:
                m1 += 1
        if m1 >= self.__circ:
            return True
        else:
            return False

    def exitShortCon1(self):
        if self.__macd[-1]<0:
            return True
        else:
            return False

    def exitShortCon2(self):
        if  self.__macd[-1-self.__circ] is None:
            return False
        m1 = 0
        for i in range(self.__circ):
            if self.__macd[-i-1] > self.__macd[-i-2]:
                m1 += 1
        if m1 >= self.__circ:
            return True
        else:
            return False

    def sellCon1(self):
        if self.__macd[-1] >self.__range:
            return True
        else:
            return False

    def sellCon2(self):
        if  self.__macd[-1-self.__circ] is None:
            return False
        m1 = 0
        for i in range(self.__circ):
            if self.__macd[-i-1] < self.__macd[-i-2]:
                m1 += 1
        if m1 >= self.__circ:
            return True
        else:
            return False

    def onBars(self, bars):
        # If a position was not opened, check if we should enter a long position.
        if self.__macd[-1]is None:
            return
        self.__range=self.__prices[0]*0.004

        self.testCon()
        if self.__longPos is not None:

            if self.exitLongSignal():
                self.__longPos.exitMarket()

        elif self.__shortPos is not None:

            if self.exitShortSignal():
                self.__shortPos.exitMarket()

        elif self.__longPos is None and self.__shortPos is None:
            if self.enterLongSignal():
                shares = int(self.getBroker().getEquity() * 0.2 / bars[self.__instrument].getPrice())
                self.__longPos = self.enterLong(self.__instrument, shares)

            elif self.enterShortSignal():
                shares = int(self.getBroker().getEquity() * 0.2 / bars[self.__instrument].getPrice())
                self.__shortPos = self.enterShort(self.__instrument, shares)


    def enterLongSignal(self) :
        if self.buyCon1() and self.buyCon2():
            return True
        else:
            return False

    def enterShortSignal(self) :
        if self.sellCon1() and self.sellCon2():
            return True
        else:
            return False

    def exitLongSignal(self) :
        if self.exitLongCon1() and self.exitLongCon2() and not self.__longPos.exitActive():
            return True
        else:
            return False

    def exitShortSignal(self):
        if self.exitShortCon1() and self.exitShortCon2() and not self.__shortPos.exitActive():
            return True
        else:
            return False
    
if __name__ == "__main__": 
    strat = thrSMA    
    instrument = '600547'
    market = 'SZ'
    date = '2016-03-11'
    #toDate ='20160101'
    frequency = bar.Frequency.SECOND
    paras = [150, 450, 500, 4]

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
        plt.getOrCreateSubplot("macd").addDataSeries('macd',strat.getMACD())
        plt.getOrCreateSubplot("signal").addDataSeries('signal',strat.getMACD().getSignal())
        position = strat.getTest()
        plt.getOrCreateSubplot("position").addDataSeries("position", position)
        #plt.getOrCreateSubplot("macd").addDataSeries('macd2',strat.getMACD2())
    strat.run()
    
    if plot:
        plt.plot()
        































