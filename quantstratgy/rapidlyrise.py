from pyalgotrade import strategy
from pyalgotrade.broker.fillstrategy import DefaultStrategy
from pyalgotrade.broker.backtesting import TradePercentage
from tickbarfeed import tickcsvfeed
from pyalgotrade import plotter
from pyalgotrade import bar
import numpy as np
class rapidlyrise(strategy.BacktestingStrategy):
    def __init__(self,feed,instrument):
        strategy.BacktestingStrategy.__init__(self,feed)
        self.getBroker().setFillStrategy(DefaultStrategy(None))
        self.getBroker().setCommission(TradePercentage(0.0008))
        self.__instrument = instrument
        self.__shortPos=[]
        self.__longPos=[]
        # self.__askprices=feed[instrument].getAskPrices()
        # self.__bidprices=feed[instrument].getBidPrices()
        # self.__askvols=feed[instrument].getAskVols()
        # self.__bidvols=feed[instrument].getBidVols()
        # self.__lastAskPrices=feed[instrument].getLastAskPrices()
        # self.__preAskPrices=feed[instrument].getPreAskPrices()
        # self.__lastAskVols=feed[instrument].getLastAskVols()
        # self.__preAskVols=feed[instrument].getPreAskVols()
        # self.__lastBidPrices=feed[instrument].getLastBidPrices()
        # self.__preBidPrices=feed[instrument].getPreBidPrices()
        # self.__lastBidVols=feed[instrument].getLastBidVols()
        # self.__preBidVols=feed[instrument].getPreBidVols()
        self.__match=feed[instrument].getMatchDataSeries()
        self.__prebar=None
        self.__lastbar=None
        self.__upspeedArr=[]
        self.__downspeedArr=[]
        self.__averageAskVol=[]
        self.__averageBidVol=[]
        self.__upmotion=[]
        self.__downmotion=[]
        self.__volArr=[]
        self.__bidaskVol=[]
        self.__statusArr=[]
        self.__motionscore=[]
    def enterLongSignal(self):
        pass

    def calAskVol(self, price, preprice,volume,prevolume):
        upwardvol=0
        if price[0]>preprice[9]:
            for i in range(10):
                upwardvol=upwardvol+prevolume[i]
        elif price[0]<preprice[0]:
            pass
        else:
            for i in range(10):
                 if price[0]==preprice[i]:
                     for j in range(0,i):
                        upwardvol=upwardvol+prevolume[j]
                     if(volume[i]>prevolume[i]):
                        upwardvol=upwardvol+volume[i]-prevolume[i]
                     break

        return upwardvol

    def calBidVol(self, price, preprice,volume,prevolume):
        downwardvol=0
        if price[0]<preprice[9]:
            for i in range(10):
                downwardvol=downwardvol+prevolume[i]
        elif price[0]>preprice[0]:
            pass
        else:
            for i in range(10):
                if price[0]==preprice[i]:
                    for j in range(0,i):
                        downwardvol=downwardvol+prevolume[j]
                    if(volume[i]>prevolume[i]):
                        downwardvol=downwardvol+volume[i]-prevolume[i]
                    break
        return downwardvol

    def calSpeed(self,type):
        l=60
        uparr=self.__upspeedArr[-l:]
        downarr=self.__downspeedArr[-l:]
        uptotalvol=np.sum(uparr)
        if uptotalvol==0:
            return 0
        downtotalvol=np.sum(downarr)
        if downtotalvol==0:
            return 0
        if type=='up':
            last=np.average(uparr[-3:])
        if type=='down':
            last=np.average(downarr[-3:])
        speed=last/(uptotalvol/len(uparr)+downtotalvol/len(downarr))
        #print(speed)
        return speed

    def enterLongSignal(self):
        l=60
        if len(self.__upspeedArr)<l:
            return False
        #print( 'up',self.calSpeed(self.__upspeedArr[-10:]))
        if self.calSpeed('up')>7:
            return True

    def enterShortSignal(self):
        l=60
        if len(self.__downspeedArr)<l:
            return False
        #print( 'down',self.calSpeed(self.__downspeedArr[-10:]))
        if self.calSpeed('down')>7:
            return True
    def drop0(self,arr):
        for item in arr:
            if item==0:
                arr.remove(item)
        return arr

    def calMotion(self,speedArr,avergeVol):
        upspeedArr=self.drop0(speedArr[-10:])
        if np.average(avergeVol[-10])==0:
            return 0
        m30=np.sum(upspeedArr)/(np.average(avergeVol[-10])*len(speedArr))
        upspeedArr10=self.drop0(speedArr[-4:])
        m10=np.sum(upspeedArr10)/(np.average(avergeVol[-10])*len(upspeedArr10))
        m3=speedArr[-1]/np.average(avergeVol[-10])
        return (m30+m10+m3)/3

    def getSpeedvol(self):
        return self.__upspeedArr,self.__downspeedArr

    def getUpMotion(self):
        return self.__upmotion

    def getDownMotion(self):
        return self.__downmotion
    def getVolArr(self):
        return self.__volArr

    def getBidAskVols(self):
        return self.__bidaskVol

    def getMotionScore(self):
        return self.__motionscore

    def onBars(self, bars):
        self.__prebar=self.__lastbar
        prebar=self.__prebar
        self.__lastbar=bars.getBar(instrument)
        lastbar=self.__lastbar
        if prebar is None:
            return
        diff=self.__lastbar.volume-self.__prebar.volume
        if diff>1000000:
            diff=0
        self.__volArr.append(diff)
        lastAskPrices=[lastbar.askPrice1,lastbar.askPrice2,lastbar.askPrice3,lastbar.askPrice4,lastbar.askPrice5,lastbar.askPrice6,lastbar.askPrice7,lastbar.askPrice8,lastbar.askPrice9,lastbar.askPrice10]
        preAskPrices=[prebar.askPrice1,prebar.askPrice2,prebar.askPrice3,prebar.askPrice4,prebar.askPrice5,prebar.askPrice6,prebar.askPrice7,prebar.askPrice8,prebar.askPrice9,prebar.askPrice10]
        lastAskVols=[lastbar.askVol1,lastbar.askVol2,lastbar.askVol3,lastbar.askVol4,lastbar.askVol5,lastbar.askVol6,lastbar.askVol7,lastbar.askVol8,lastbar.askVol9,lastbar.askVol10]
        preAskVols=[prebar.askVol1,prebar.askVol2,prebar.askVol3,prebar.askVol4,prebar.askVol5,prebar.askVol6,prebar.askVol7,prebar.askVol8,prebar.askVol9,prebar.askVol10]
        askvol=self.calAskVol(lastAskPrices,preAskPrices,lastAskVols,preAskVols)
        self.__averageAskVol.append(np.average(lastAskVols))
        lastBidPrices=[lastbar.bidPrice1,lastbar.bidPrice2,lastbar.bidPrice3,lastbar.bidPrice4,lastbar.bidPrice5,lastbar.bidPrice6,lastbar.bidPrice7,lastbar.bidPrice8,lastbar.bidPrice9,lastbar.bidPrice10]
        preBidPrices=[prebar.bidPrice1,prebar.bidPrice2,prebar.bidPrice3,prebar.bidPrice4,prebar.bidPrice5,prebar.bidPrice6,prebar.bidPrice7,prebar.bidPrice8,prebar.bidPrice9,prebar.bidPrice10]
        lastBidVols=[lastbar.bidVol1,lastbar.bidVol2,lastbar.bidVol3,lastbar.bidVol4,lastbar.bidVol5,lastbar.bidVol6,lastbar.bidVol7,lastbar.bidVol8,lastbar.bidVol9,lastbar.bidVol10]
        preBidVols=[prebar.bidVol1,prebar.bidVol2,prebar.bidVol3,prebar.bidVol4,prebar.bidVol5,prebar.bidVol6,prebar.bidVol7,prebar.bidVol8,prebar.bidVol9,prebar.bidVol10]
        bidvol=self.calBidVol(lastBidPrices,preBidPrices,lastBidVols,preBidVols)
        self.__averageBidVol.append(lastBidVols)
        self.__bidaskVol.append((np.sum(lastAskVols)+np.sum(lastBidVols))/10)
        #print(lastAskPrices,preAskPrices,lastAskVols,preAskVols,askvol)
        self.__upspeedArr.append(askvol)
        self.__downspeedArr.append(bidvol)
        if len(self.__upspeedArr)<10:
            self.__upmotion.append(0)
            self.__downmotion.append(0)
        else:
            self.__upmotion.append(self.calMotion(self.__upspeedArr,self.__averageAskVol))
            self.__downmotion.append(self.calMotion(self.__downspeedArr,self.__averageBidVol))


        if len(self.__match)>2:
            if self.__match[-1]>self.__match[-2]:
                self.__statusArr.append(1)
            elif self.__match[-1]==self.__match[-2]:
                self.__statusArr.append(0)
            else:
                self.__statusArr.append(-1)
        if len(self.__statusArr)<20:
            self.__motionscore.append(np.sum(self.__statusArr)*np.sum(np.abs(self.__statusArr)))
        else:
            self.__motionscore.append(np.sum(self.__statusArr[-20])*np.sum(np.abs(self.__statusArr[-20])))
        if self.enterLongSignal():
            shares = int(self.getBroker().getEquity() * 0.05 / bars[self.__instrument].getPrice())
            self.__longPos.append(self.enterLong(self.__instrument, shares))

        if self.enterShortSignal():
            shares = int(self.getBroker().getEquity() * 0.05 / bars[self.__instrument].getPrice())
            self.__shortPos.append(self.enterShort(self.__instrument, shares))

if __name__ == "__main__":
    strat = rapidlyrise
    instrument = '600604'
    market = 'SZ'
    date = '2016-05-05'
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
    #filepath = path +'stock_'+ instrument + "_"+date+"_tick.csv"
    filepath=path+date+'_'+instrument+'_tick.csv'
    #############################################don't change ############################33
    from pyalgotrade.barfeed.csvfeed import GenericBarFeed


    barfeed = tickcsvfeed.TickBarFeed(bar.Frequency.SECOND)
    barfeed.setDateTimeFormat('%Y-%m-%d %H:%M:%S')
    barfeed.addBarsFromCSV(instrument, filepath)
    strat = strat(barfeed, instrument)
    if plot:
        plt = plotter.StrategyPlotter(strat)
        plt.getOrCreateSubplot("motion").addDataSeries("upmotion", strat.getUpMotion())
        plt.getOrCreateSubplot("motion").addDataSeries("downmotion", strat.getDownMotion())
        plt.getOrCreateSubplot("Volume").addDataSeries('volume',strat.getVolArr())
        plt.getOrCreateSubplot("Volume").addDataSeries('askbid',strat.getBidAskVols())
        plt.getOrCreateSubplot('motionscore').addDataSeries('motionscore',strat.getMotionScore())
    strat.run()
    up,down=strat.getSpeedvol()
    #print(up,down)
    if plot:
        plt.plot()
