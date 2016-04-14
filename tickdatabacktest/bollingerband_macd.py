#-*-coding:utf-8-*-
"""
Created on Tue Nov 03 13:06:56 2015

@author: Eunice
"""

if __name__ == '__main__':
    import sys
    sys.path.append("..")
    from pyalgotrade import bar
# 以上模块仅测试用
from pyalgotrade.broker.fillstrategy import DefaultStrategy
from pyalgotrade.broker.backtesting import TradePercentage
from pyalgotrade import strategy
from pyalgotrade.technical import macd
from pyalgotrade.dataseries import SequenceDataSeries
from pyalgotrade.broker.backtesting import TradePercentage
from pyalgotrade.technical import bollinger
from pyalgotrade.technical import cross
from pyalgotrade.strategy.position import ShortPosition
from pyalgotrade.strategy.position import LongPosition
from tickbarfeed import tickcsvfeed
#import pandas as pd
import numpy as np
from datetime import datetime
#from pyalgotrade import plotter

class bollinger_band(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument,longline,shortline,bollingerlength, numStdDev):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.getBroker().setFillStrategy(DefaultStrategy(None))
        self.getBroker().setCommission(TradePercentage(0.001))
        self.__instrument = instrument
        self.__bollingerlength = int(bollingerlength)
        self.__close = feed[instrument].getMatchDataSeries()
        numStdDev = float(numStdDev) / 10
        self.__longPos = []
        self.__shortPos = []
        self.__macd=macd.MACD(self.__close,shortline,longline,10)
        self.__bollinger = bollinger.BollingerBands(self.__macd, self.__bollingerlength, int(numStdDev))
        self.__UpperBand = self.__bollinger.getUpperBand()
        self.__LowerBand = self.__bollinger.getLowerBand()

        self.__position = SequenceDataSeries()
        self.__circ=5
        self.__lastLongPos=None
        self.__lastShortPos=None
        self.__barNum=0
        self.__macdMin=[]
        self.__macdMax=[]
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

        if self.__macd[-1] is None:
            #print (self.__macd[-1])
            return
        if self.__macd[-1]>self.__macdMax:
            self.__macdMax=self.__macd[-1]
        if self.__macd[-1]<=self.__macdMin:
            self.__macdMin=self.__macd[-1]
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
                shares = int(self.getBroker().getEquity() * 0.2 / bars[self.__instrument].getMatch())
           # self.__longPos.
                self.__longPos.append(self.enterLong(self.__instrument, shares))
            self.__lastLongPos=self.__barNum
            #print('long'+str(shares))

        elif self.enterShortSignal():
            for i in range(self.enterShortSignal()):
                shares = int(self.getBroker().getEquity() * 0.2 / bars[self.__instrument].getMatch())
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
            if self.__macd[-i-1] <= self.__LowerBand[-i-2]:
                m1 += 1
        if m1 >= self.__circ-1 and cross.cross_above(self.__macd,self.__LowerBand)>0:
            if self.__macd[-1]>0:
                return 0
            else:
                if self.__macdMin==self.__macd[-1] :
                    return 2
                else:
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
            if self.__macd[-i-1] >= self.__UpperBand[-i-2]:
                m1 += 1
        if m1 >= self.__circ-1 and cross.cross_below(self.__macd,self.__UpperBand)>0:
            if self.__macd[-1]<0:
                return 0
            else:
                if self.__macdMax==self.__macd[-1]:
                    return 2
                else:
                    return 1
        else:
            return 0

    def exitLongSignal(self) :
        if self.__UpperBand[-1-self.__circ] is None:
            return False
        m1 = 0
        for i in range(self.__circ):
            if self.__macd[-i-1] >= self.__UpperBand[-i-2]:
                m1 += 1
        if m1 >= self.__circ-1 and cross.cross_below(self.__macd,self.__UpperBand)>0:
            return True
        elif self.__macd[-1]>=self.__UpperBand[-1] and self.__macdMax==self.__macd[-1]:
            return True
        elif self.__macd[-1]*1.001>=self.__UpperBand[-1] and self.__macd[-1]>-0.1:
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
        elif self.__macd[-1]<=self.__LowerBand[-1] and self.__macdMin==self.__macd[-1]:
            return True
        elif self.__macd[-1]<=self.__LowerBand[-1]*1.001 and self.__macd[-1]<0.11:
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
import itertools
from pyalgotrade.optimizer import local
from pyalgotrade import bar
#from stratlib import bollinger_band_macd
from pyalgotrade.barfeed.csvfeed import GenericBarFeed
from pyalgotrade.barfeed import yahoofeed
def parameters_generator():
    instrument=['002099']
    longLine=list(range(150,250))
    shortLine=list(range(50,100))
    bollingerLenth=list(range(150,250))
    stddev=list(range(20,35))
    return itertools.product(instrument,longLine,shortLine,bollingerLenth,stddev)

if __name__=='__main__':
    instrument='002099'
    stockcode='002099'
    date='2016-02-26'
    path = "../histdata/tick/"
    filepath = path +'stock_'+ stockcode + "_"+date+"_tick.csv"
    barfeed = tickcsvfeed.TickBarFeed(bar.Frequency.SECOND)
    barfeed.addBarsFromCSV(instrument, filepath)
    barfeed.setDateTimeFormat('%Y-%m-%d %H:%M:%S')
    local.run(bollinger_band,barfeed,parameters_generator())






























