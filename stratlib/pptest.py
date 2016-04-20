import pp
import pyalgotrade
def backtest(stockcode,date,p1,p2,p3,p4):
    stockcode='300251'
    #date=['2016-02-29','2016-03-02','2016-03-11']
    date=['2016-03-02']
    path = "../histdata/tick/bak/"
    strat =bollinger_band_macd
    paras=[155,115,220,30]
    plot = True
   # barfeed = tickcsvfeed.TickBarFeed(bar.Frequency.SECOND)
    barfeed=pyalgotrade.barfeed.csvfeed.GenericBarFeed(pyalgotrade.bar.Frequency.SECOND)
    for d in date:
        filepath = path +'stock_'+ stockcode + "_"+d+".csv"
        barfeed.addBarsFromCSV(stockcode, filepath)
    barfeed.setDateTimeFormat('%Y-%m-%d %H:%M:%S')
    strat = strat(barfeed, stockcode, *paras)
    strat.run()
    cash=strat.getBroker()._Broker__cash
    tradeTimes=strat.getTradeTimes()
    return (p1,p2,p3,p4,cash,tradeTimes)


if __name__ == "__main__":
    ppservers=()
    job_server=pp.Server(ppservers=ppservers)
    print('start PP with',job_server.get_ncpus(),"workers")
    job1=job_server.submit(backtest,('300251','2016-03-02',155,115,220,30),(bollinger_band_macd,),('bollinger_band_macd','pyalgotrade',))
    print(job1())