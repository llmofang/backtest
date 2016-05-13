import sys
sys.path.append("..")

import pyalgotrade
from stratlib.bollinger_band_macd import bollinger_band
from rbreaker import rbreaker
from celery_config import app
from pyalgotrade.barfeed.csvfeed import GenericBarFeed
@app.task
def backtest(stockcode,date,preclose,prehigh,prelow,p1,p2,p3,p4):
    stockcode=stockcode
    #date=['2016-02-29','2016-03-02','2016-03-11']
    path = "../histdata/tick/bak/"
    strat =rbreaker
    paras=[preclose,prehigh,prelow,p1,p2,p3,p4]
    plot = True
   # barfeed = tickcsvfeed.TickBarFeed(bar.Frequency.SECOND)
    barfeed=GenericBarFeed(pyalgotrade.bar.Frequency.SECOND)
    dstr=''
    for d in date:
        filepath = path +'stock_'+ stockcode + "_"+d+".csv"
        barfeed.addBarsFromCSV(stockcode, filepath)
        dstr=dstr+'_'+d
    barfeed.setDateTimeFormat('%Y-%m-%d %H:%M:%S')
    strat = strat(barfeed, stockcode, *paras)
    strat.run()
    cash=strat.getBroker()._Broker__cash
    #tradeTimes=strat.getTradeTimes()
    ticker=open(path +'stock_'+ stockcode+'_' + dstr+".csv", 'a')
    ticker.write(str(p1))
    ticker.write(',')
    ticker.write(str(p2))
    ticker.write(',')
    ticker.write(str(p3))
    ticker.write(',')
    ticker.write(str(p4))
    ticker.write(',')
    ticker.write(str(cash))
    ticker.write(',')
    #ticker.write(str(tradeTimes))

    ticker.write('\n')
    ticker.close()
    del strat
    #return ( stockcode,date,p1,p2,p3,p4,cash,tradeTimes)
    return ( stockcode,date,p1,p2,p3,p4,cash)

def func(stockcode,date,preclose,prehigh,prelow,p1,p2,p3,p4):
    for sc in stockcode:
        for pa1 in p1:
            for pa2 in p2:
                for pa3 in p3:
                    for pa4 in p4:
                        # if pa1<=pa2:
                        #     break
                        #print(pa1,pa2,pa3,pa4)
                        backtest.delay(sc,date,preclose,prehigh,prelow,pa1/1000,pa2/1000,pa3/1000,pa4/1000)

if __name__ == "__main__":
    stockcodes=['300251',]
    date=['2016-02-29',]
    p1=list(range(150,250,10))
    p2=list(range(100,200,10))
    p3=list(range(150,250,10))
    p4=list(range(20,40,5))
    func(stockcodes,date,p1,p2,p3,p4)
