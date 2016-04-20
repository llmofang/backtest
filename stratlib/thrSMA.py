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

class thrSMA(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, short_l, mid_l, long_l, up_cum):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.getBroker().setFillStrategy(DefaultStrategy(None))
        self.getBroker().setCommission(TradePercentage(0.0008))
        self.__position = None
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__malength1 = int(short_l)
        self.__malength2 = int(mid_l)
        self.__malength3 = int(long_l)
        self.__circ = int(up_cum)
        self.__ma1 = ma.SMA(self.__prices, self.__malength1)
        self.__ma2 = ma.SMA(self.__prices, self.__malength2)
        self.__ma3 = ma.SMA(self.__prices, self.__malength3)
        self.__macd=macd.MACD(self.__prices,100,300,80)

    def getPrice(self):
        return self.__prices

    def getSMA(self):
        return self.__ma1,self.__ma2, self.__ma3

    def getMACD(self):
        return self.__macd

    def onEnterCanceled(self, position):
        self.__position = None

    def onEnterOK(self):
        pass

    def onExitOk(self, position):
        self.__position = None
        #self.info("long close")

    def onExitCanceled(self, position):
        self.__position.exitMarket()
        
    def buyCon1(self):
        if cross.cross_above(self.__ma1, self.__ma2) > 0:
            return True

    def buyCon2(self):
        m1 = 0
        m2 = 0
        for i in range(self.__circ):
            if self.__ma1[-i-1] > self.__ma3[-i-1]:
                m1 += 1
            if self.__ma2[-i-1] > self.__ma3[-i-1]:
                m2 += 1

        if m1 >= self.__circ and m2 >= self.__circ:
            return True
    
    def sellCon1(self):
        if cross.cross_below(self.__ma1, self.__ma2) > 0:
            return True
            

    def onBars(self, bars):
        # If a position was not opened, check if we should enter a long position.
        
        if self.__ma3[-1]is None:
            return 
            
        if self.__position is not None:
            if not self.__position.exitActive() and cross.cross_below(self.__ma1, self.__ma2) > 0:
                self.__position.exitMarket()
                #self.info("sell %s" % (bars.getDateTime()))
        
        if self.__position is None:
            if self.buyCon1() and self.buyCon2():
                shares = int(self.getBroker().getCash() * 0.2 / bars[self.__instrument].getPrice())
                self.__position = self.enterLong(self.__instrument, shares)
                print(bars[self.__instrument].getDateTime(), bars[self.__instrument].getPrice())
                #self.info("buy %s" % (bars.getDateTime()))
    
    
if __name__ == "__main__": 
    strat = thrSMA    
    instrument = '600085'
    market = 'SZ'
    date = '2016-03-02'
    #toDate ='20160101'
    frequency = bar.Frequency.SECOND
    paras = [150, 300, 450, 2]

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
        plt = plotter.StrategyPlotter(strat, True, True, True)
        ma1,ma2,ma3=strat.getSMA()
        plt.getInstrumentSubplot('indicator').addDataSeries("ma1", ma1)
        plt.getInstrumentSubplot('indicator').addDataSeries("ma2", ma2)
        plt.getInstrumentSubplot('indicator').addDataSeries("ma3", ma3)
        plt.getOrCreateSubplot("macd").addDataSeries('macd',strat.getMACD())
    strat.run()

    if plot:
        plt.plot()


        































