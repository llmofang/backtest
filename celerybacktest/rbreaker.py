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

class rbreaker(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument,preclose,prehigh,prelow,p1,p2,p3,p4):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.getBroker().setFillStrategy(DefaultStrategy(None))
        self.getBroker().setCommission(TradePercentage(0.001))
        self.__instrument = instrument
        self.__longPos = []
        self.__shortPos = []
        self.__position = SequenceDataSeries()
        self.__prices= feed[instrument].getPriceDataSeries()
        self.__circ=5
        self.__lastLongPos=None
        self.__lastShortPos=None
        self.__barNum=0
        self.__ssetup=prehigh-p1*(preclose-prelow)
        self.__senter=((1+p2)/2)*(prehigh+preclose)-p2*prelow
        self.__benter=((1+p2)/2)*(prelow+preclose)-p2*prehigh
        self.__bsetup=prelow+p1*(prehigh-preclose)
        self.__bbreak=self.__ssetup+p3*(self.__ssetup-self.__bsetup)
        self.__sbreak=self.__bsetup-p3*(self.__ssetup-self.__bsetup)
        self.__moreSsetup=False
        self.__lessBsetup=False
        self.__couldsbreak=True
        self.__couldbbreak=True
        self.__p4=p4

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


    def getPrice(self):
        return self.__prices

    def getTest(self):
        return self.__position

    def onBars(self, bars):
        bar = bars[self.__instrument]
        if self.__prices[-1]>self.__ssetup:
            self.__moreSsetup=True
        else:
            self.__couldbbreak=True
        if self.__prices[-1]<self.__bsetup:
            self.__lessBsetup=True
        else:
            self.__couldsbreak=True
        dt=bars.getDateTime()
        h=dt.hour
        m=dt.minute
        if(h==14 and m>50):
            if len(self.__longPos)> 0:
                for item in self.__longPos:
                    if item[0]._Position__exitOrder is None:
                        item[0].exitMarket()
            if len(self.__shortPos)>0:
                for item in self.__shortPos:
                    if item[0]._Position__exitOrder is None:
                        item[0].exitMarket()
            return
        self.testCon()
        if len(self.__longPos)> 0:
            if self.exitLongSignal():
               for item in self.__longPos:
                   if item[0]._Position__exitOrder is None:
                        item[0].exitMarket()

        elif len(self.__shortPos)>0:
            if self.exitShortSignal():
                for item in self.__shortPos:
                    if item[0]._Position__exitOrder is None:
                        item[0].exitMarket()

        if self.enterLongSignal():
            for i in range(self.enterLongSignal()):
                shares = int(self.getBroker().getEquity() * 0.2 / bars[self.__instrument].getPrice())
           # self.__longPos.
                pos=self.enterLong(self.__instrument, shares)
                #pos.exitLimit(bars[self.__instrument].getPrice()*0.99)
                self.__longPos.append([pos,0])
            self.__lastLongPos=self.__barNum
            #print('long'+str(shares))

        if self.enterShortSignal():
            for i in range(self.enterShortSignal()):
                shares = int(self.getBroker().getEquity() * 0.2 / bars[self.__instrument].getPrice())
                pos=self.enterShort(self.__instrument, shares)
                #pos.exitLimit(bars[self.__instrument].getPrice()*1.01)
                self.__shortPos.append([pos,0])
            self.__lastShortPos=self.__barNum

    def enterLongSignal (self) :
        if len(self.__longPos)>=2:
            if self.__lessBsetup:
                if self.__prices[-1]<self.__benter:
                    return 1
            if self.__couldbbreak:
                if self.__prices[-1]>self.__bbreak:
                    return 1


    def enterShortSignal(self) :
        if len(self.__shortPos)<=2:
            if self.__moreSsetup:
               if self.__prices[-1]<self.__senter:
                   return 1
            if self.__couldsbreak:
                if self.__prices[-1]<self.__sbreak:
                    return 1

    def exitLongSignal(self) :
        for item in self.__longPos:
            print(item[1])
            if item[0].getReturn()>item[1]:
                item[1]=item[0].getReturn()
            if item[1]-item[0].getReturn()>self.__p4:
                self.__couldbbreak=False
                return 1

    def exitShortSignal(self):
        for item in self.__shortPos:
            if item[0].getReturn()>item[1]:
                item[1]=item[0].getReturn()
            if item[1]-item[0].getReturn()>self.__p4:
                self.__couldsbreak=False
                return 1


    def onEnterCanceled(self, position):
        if len(self.__longPos)>0:
            if self.__longPos[-1] == position:
                del self.__longPos[-1]
                self.__lastLongPos==None
        if len(self.__shortPos)>0:
            if self.__shortPos[-1] == position:
                del self.__shortPos[-1]
                self.__lastShortPos==None

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

    def getParams(self):
        return (self.__bbreak,self.__ssetup,self.__senter,self.__benter,self.__bsetup,self.__sbreak)

from pyalgotrade.barfeed.csvfeed import GenericBarFeed
from pyalgotrade import bar
from pyalgotrade import plotter
if __name__=='__main__':

    #date=['2016-02-29','2016-03-02','2016-03-11']

    path = "../histdata/tick/bak/"
    strat = rbreaker

    # date=['2016-02-29']
    # paras=[20.6,21.66,20.04,0.35,0.07,0.25]
    # instrument='300251'
    #close high low
    date=['2016-03-11']
    paras=[18.90,19.71,18.76,0.35,0.07,0.25,0.004]
    instrument='300251'

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
        #position = strat.getTest()
        #plt.getOrCreateSubplot("position").addDataSeries("position", position)
        #plt.getOrCreateSubplot("macd").addDataSeries('macd2',strat.getMACD2())
    strat.run()
    print(strat.getParams())
    if plot:
        plt.plot()






























