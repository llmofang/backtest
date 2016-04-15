import itertools
from pyalgotrade.optimizer import local
from pyalgotrade import bar
from stratlib import bollinger_band_macd
from pyalgotrade.barfeed.csvfeed import GenericBarFeed
def parameters_generator():
    instrument=['002099']
    longLine=list(range(150,250,5))
    shortLine=list(range(50,100,5))
    bollingerLenth=list(range(150,250,5))
    stddev=list(range(20,35))
    return itertools.product(instrument,longLine,shortLine,bollingerLenth,stddev)

if __name__=='__main__':
    instrument='002099'
    stockcode='002099'
    date=['2016-02-29','2016-03-02','2016-03-11']
    path = "../histdata/tick/bak/"

   # barfeed = tickcsvfeed.TickBarFeed(bar.Frequency.SECOND)
    barfeed=GenericBarFeed(bar.Frequency.SECOND)
    for d in date:
        filepath = path +'stock_'+ stockcode + "_"+d+".csv"
        barfeed.addBarsFromCSV(instrument, filepath)
    barfeed.setDateTimeFormat('%Y-%m-%d %H:%M:%S')
    local.run(bollinger_band_macd.bollinger_band,barfeed,parameters_generator())