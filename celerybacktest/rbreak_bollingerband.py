# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 13:06:56 2015

@author: Eunice
"""


# 以上模块仅测试用
from pyalgotrade.broker.fillstrategy import DefaultStrategy
from pyalgotrade.broker.backtesting import TradePercentage
from pyalgotrade import strategy
from pyalgotrade.technical import macd
#import matplotlib.pyplot as plt
from pyalgotrade.dataseries import SequenceDataSeries
from pyalgotrade.broker.backtesting import TradePercentage
from pyalgotrade.technical import bollinger
from pyalgotrade.technical import cross
from pyalgotrade.strategy.position import ShortPosition
from pyalgotrade.strategy.position import LongPosition
import numpy as np
from datetime import datetime

class rbreak_bollingerband(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument,longLine,shortLine, bollingerlength, numStdDev):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.getBroker().setFillStrategy(DefaultStrategy(None))
        self.getBroker().setCommission(TradePercentage(0.0008))
        self.__instrument = instrument
        self.__bollingerlength = int(bollingerlength)
        self.__close = feed[instrument].getPriceDataSeries()
        numStdDev = float(numStdDev) / 10
        self.__longPos = []
        self.__shortPos = []
        self.__macd=macd.MACD(self.__close,shortLine,longLine,10)
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
        self.__tradeTimes=0
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

        dt=bars.getDateTime()
        h=dt.hour
        m=dt.minute
        if(h==14 and m>50):
            if len(self.__longPos)> 0:
                for pos in self.__longPos:
                    if pos._Position__exitOrder is None:
                        pos.exitMarket()
            if len(self.__shortPos)>0:
                for pos in self.__shortPos:
                    if pos._Position__exitOrder is None:
                        pos.exitMarket()
            return
        if lower is None or upper is None:
            return
        self.testCon()
        if len(self.__longPos)> 0:

            if self.exitLongSignal():
               for pos in self.__longPos:
                   if pos._Position__exitOrder is None:
                        pos.exitMarket()

        elif len(self.__shortPos)>0:

            if self.exitShortSignal():
                for pos in self.__shortPos:
                    if pos._Position__exitOrder is None:
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
        self.__tradeTimes=self.__tradeTimes+1
        if isinstance(position,LongPosition):
            self.__longPos = []
        elif isinstance(position,ShortPosition):
            self.__shortPos = []
        else:
            assert(False)

    def onExitCanceled(self, position):
        position.exitMarket()

    def getTradeTimes(self):
        return self.__tradeTimes


# if __name__ == "__main__":
#     strat = bollinger_band
#     instrument = '300251'
#     market = 'SZ'
#     date = ['2016-02-29','2016-03-02','2016-03-11']
#     #toDate ='20160101'
#     frequency = bar.Frequency.SECOND
#     if frequency == bar.Frequency.MINUTE:
#         path = "..\\histdata\\min\\bak\\"
#     elif frequency == bar.Frequency.DAY:
#         path = "..\\histdata\\day\\bak\\"
#     elif frequency == bar.Frequency.SECOND:
#         path = "..\\histdata\\tick\\bak\\"
#    # filepath = path +'stock_'+ instrument + "_"+date+".csv"
#     from pyalgotrade.barfeed.csvfeed import GenericBarFeed
#     ticker=open(path +'stock_'+ instrument + "_3days.csv", 'a')
#     for p1 in range(150,400,5):
#        for p2 in range(50,300,5):
#            for p3 in range(150,400,5):
#                for p4 in range(20,40,5):
#                 if p1<=p2:
#                     break
#                 paras = [p1,p2,p3,p4]
#                 barfeed = GenericBarFeed(frequency)
#                 barfeed.setDateTimeFormat('%Y-%m-%d %H:%M:%S')
#                 for d in date:
#                     filepath = path +'stock_'+ instrument + "_"+d+".csv"
#                     barfeed.addBarsFromCSV(instrument, filepath)
#                 strat1 = strat(barfeed, instrument, *paras)
#                 strat1.run()
#                 print(p1,p2,p3,p4,strat1.getBroker()._Broker__cash)
#                 ticker.write(str(p1))
#                 ticker.write(',')
#                 ticker.write(str(p2))
#                 ticker.write(',')
#                 ticker.write(str(p3))
#                 ticker.write(',')
#                 ticker.write(str(p4))
#                 ticker.write(',')
#                 ticker.write(str(strat1.getBroker()._Broker__cash))
#                 ticker.write('\n')
#                 del strat1
#     ticker.close()



from pyalgotrade.barfeed.csvfeed import GenericBarFeed
from pyalgotrade import bar
from pyalgotrade import plotter
if __name__=='__main__':
    instrument='300251'
    #date=['2016-02-29','2016-03-02','2016-03-11']
    date=['2016-02-25']
    path = "../histdata/tick/bak/"
    strat = bollinger_band
    paras=[220,150,220,30]
    plot = True
   # barfeed = tickcsvfeed.TickBarFeed(bar.Frequency.SECOND)
    barfeed=GenericBarFeed(bar.Frequency.SECOND)
    for d in date:
        filepath = path +'stock_'+ instrument + "_"+d+".csv"
        barfeed.addBarsFromCSV(instrument, filepath)
    barfeed.setDateTimeFormat('%Y-%m-%d %H:%M:%S')
    strat = strat(barfeed, instrument, *paras)
    if plot:
        plt = plotter.StrategyPlotter(strat)
        position = strat.getTest()
        plt.getOrCreateSubplot("position").addDataSeries("position", position)
        plt.getOrCreateSubplot("macd").addDataSeries('macd',strat.getMACD())
       # plt.getOrCreateSubplot("macd").addDataSeries("upper", strat.getBollingerBands().getUpperBand())
        plt.getOrCreateSubplot("macd").addDataSeries("middle", strat.getBollingerBands().getMiddleBand())
        #plt.getOrCreateSubplot("macd").addDataSeries("lower", strat.getBollingerBands().getLowerBand())
        #position = strat.getTest()
        #plt.getOrCreateSubplot("position").addDataSeries("position", position)
        #plt.getOrCreateSubplot("macd").addDataSeries('macd2',strat.getMACD2())
    strat.run()

    if plot:
        plt.plot()


#**********************************pyalgotrade optimize******************************************
# import itertools
# from pyalgotrade.optimizer import local
# from pyalgotrade import bar
# #from stratlib import bollinger_band_macd
# from pyalgotrade.barfeed.csvfeed import GenericBarFeed
# from pyalgotrade import logger
#
# def parameters_generator():
#     instrument=['002099']
#     longLine=list(range(150,300,10))
#     shortLine=list(range(50,110,10))
#     bl=list(range(150,300,10))
#     sd=list(range(20,40,5))
#     p1=list(range(1,20))
#     p2=list(range(1,10))
#     return itertools.product(instrument,longLine,shortLine,bl,sd,p1,p2)
#
# if __name__=='__main__':
#     instrument='002099'
#     stockcode='002099'
#     date=['2016-02-29']
#     path = "../histdata/tick/bak/"
#     logger.file_log='bollinger_band_macd_002099_backtest_3days.log'
#    # barfeed = tickcsvfeed.TickBarFeed(bar.Frequency.SECOND)
#     barfeed=GenericBarFeed(bar.Frequency.SECOND)
#     for d in date:
#         filepath = path +'stock_'+ stockcode + "_"+d+".csv"
#         barfeed.addBarsFromCSV(instrument, filepath)
#     barfeed.setDateTimeFormat('%Y-%m-%d %H:%M:%S')
#     local.run(bollinger_band,barfeed,parameters_generator(),workerCount=8)
































