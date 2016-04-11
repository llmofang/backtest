import datetime

from dateutil import parser
from pyalgotrade.barfeed import membf
from pyalgotrade.utils import csvutils

from pyalgotrade import bar
from pyalgotrade import dataseries
from tickbarfeed import TickBarDataSeries
from tickbarfeed import TickBar


class BarFeed(membf.BarFeed):
    def _init_(self,frequency=bar.Frequency.SECOND,maxLen=dataseries.DEFAULT_MAX_LEN):
        membf.BarFeed.__init__(self,frequency,maxLen)
        self.__barFilter=None
        self.__dailyTime=datetime.time(0,0,0)

    def getDailyBarTime(self):
        return self.__dailyTime

    def setDailyBarTime(self, time):
        self.__dailyTime = time

    def getBarFilter(self):
        return self.__barFilter

    def setBarFilter(self, barFilter):
        self.__barFilter = barFilter

    def createDataSeries(self, key, maxLen):
        ret = TickBarDataSeries.TickBarDataSeries(maxLen)
        return ret

    def addBarsFromCSV(self, instrument, path, rowParser):
        # Load the csv file
        loadedBars = []
        reader = csvutils.FastDictReader(open(path, "r"), fieldnames=rowParser.getFieldNames(), delimiter=rowParser.getDelimiter())
        for row in reader:
            bar_ = rowParser.parseBar(row)
            if bar_ is not None and (self.__barFilter is None or self.__barFilter.includeBar(bar_)):
                loadedBars.append(bar_)

        self.addBarsFromSequence(instrument, loadedBars)

    def getNextBars(self):
        # All bars must have the same datetime. We will return all the ones with the smallest datetime.
        smallestDateTime = self.peekDateTime()

        if smallestDateTime is None:
            return None

        # Make a second pass to get all the bars that had the smallest datetime.
        ret = {}
        for instrument, bars in self.__bars.items():
            nextPos = self.__nextPos[instrument]
            if nextPos < len(bars) and bars[nextPos].getDateTime() == smallestDateTime:
                ret[instrument] = bars[nextPos]
                self.__nextPos[instrument] += 1

            if self.__currDateTime==smallestDateTime:
                t=smallestDateTime+datetime.timedelta(seconds=1)
                ret[instrument].datetime=t
                #raise Exception("Duplicate bars found for %s on %s" % (list(ret.keys()), smallestDateTime))
        #if self.__currDateTime is not None:
            #t1=parser.parse(self.__currDateTime)
            #t2=parser.parse(smallestDateTime)
            #if t1>= t2:

                #t=parser.parse(smallestDateTime).strptime(smallestDateTime,'%Y-%m-%d %H:%M:%S')+datetime.timedelta(seconds=1)
                #smallestDateTime=t.strftime('%Y-%m-%d %H:%M:%S')
                #ret[instrument].datetime=smallestDateTime
        self.__currDateTime = smallestDateTime
        return bar.Bars(ret)




class RowParser(object):
    def parseBar(self, csvRowDict):
        raise NotImplementedError()

    def getFieldNames(self):
        raise NotImplementedError()

    def getDelimiter(self):
        raise NotImplementedError()


class TickRowParser(RowParser):
    def __init__(self,columnNames,dateTimeFormat,dailyBarTime,frequency,timezone):
        self.__dateTimeFormat=dateTimeFormat
        self.__dailyBarTime=dailyBarTime
        self.__frequency=frequency
        self.__timezone=timezone
        self.haveAdjClose=False
        #TODO column names
        self.timeColName=columnNames['nTime']
        self.nActionDayColName=columnNames['nActionDay']
        self.preCloseColName=columnNames['nPreClose']
        self.nOpenColName=columnNames['nOpen']
        self.nHighColName=columnNames['nHigh']
        self.nLowColName=columnNames['nLow']
        self.nMatchColName=columnNames['nMatch']
        self.nAskPrice1ColName=columnNames['nAskPrice1']
        self.nAskPrice2ColName=columnNames['nAskPrice2']
        self.nAskPrice3ColName=columnNames['nAskPrice3']
        self.nAskPrice4ColName=columnNames['nAskPrice4']
        self.nAskPrice5ColName=columnNames['nAskPrice5']
        self.nAskPrice6ColName=columnNames['nAskPrice6']
        self.nAskPrice7ColName=columnNames['nAskPrice7']
        self.nAskPrice8ColName=columnNames['nAskPrice8']
        self.nAskPrice9ColName=columnNames['nAskPrice9']
        self.nAskPrice10ColName=columnNames['nAskPrice10']
        self.nAskVol1ColName=columnNames['nAskVol1']
        self.nAskVol2ColName=columnNames['nAskVol2']
        self.nAskVol3ColName=columnNames['nAskVol3']
        self.nAskVol4ColName=columnNames['nAskVol4']
        self.nAskVol5ColName=columnNames['nAskVol5']
        self.nAskVol6ColName=columnNames['nAskVol6']
        self.nAskVol7ColName=columnNames['nAskVol7']
        self.nAskVol8ColName=columnNames['nAskVol8']
        self.nAskVol9ColName=columnNames['nAskVol9']
        self.nAskVol10ColName=columnNames['nAskVol10']
        self.nBidPrice1ColName=columnNames['nBidPrice1']
        self.nBidPrice2ColName=columnNames['nBidPrice2']
        self.nBidPrice3ColName=columnNames['nBidPrice3']
        self.nBidPrice4ColName=columnNames['nBidPrice4']
        self.nBidPrice5ColName=columnNames['nBidPrice5']
        self.nBidPrice6ColName=columnNames['nBidPrice6']
        self.nBidPrice7ColName=columnNames['nBidPrice7']
        self.nBidPrice8ColName=columnNames['nBidPrice8']
        self.nBidPrice9ColName=columnNames['nBidPrice9']
        self.nBidPrice10ColName=columnNames['nBidPrice10']
        self.nBidVol1ColName=columnNames['nBidVol1']
        self.nBidVol2ColName=columnNames['nBidVol2']
        self.nBidVol3ColName=columnNames['nBidVol3']
        self.nBidVol4ColName=columnNames['nBidVol4']
        self.nBidVol5ColName=columnNames['nBidVol5']
        self.nBidVol6ColName=columnNames['nBidVol6']
        self.nBidVol7ColName=columnNames['nBidVol7']
        self.nBidVol8ColName=columnNames['nBidVol8']
        self.nBidVol9ColName=columnNames['nBidVol9']
        self.nBidVol10ColName=columnNames['nBidVol10']
        self.nNumTradesColName=columnNames['nNumTrades']
        self.iVolumeColName=columnNames['iVolume']
        self.iTurnoverColName=columnNames['iTurnover']
        self.nTotalBidVolColName=columnNames['nTotalBidVol']
        self.nTotalAskVolColName=columnNames['nTotalAskVol']
        self.nWeightedAvgBidPriceColName=columnNames['nWeightedAvgBidPrice']
        self.nWeightedAvgAskPriceColName=columnNames['nWeightedAvgAskPrice']


    def _parseDate(self,nDate,nTime):
        #TODO
        if len(nTime)==8 :
            nTime='0'+nTime
        nTime=nTime[:-3]
        DateTime=nDate+nTime
        return parser.parse(DateTime).strftime('%Y-%m-%d %H:%M:%S')

    def _parseTime(self,nDate,time):
        time=time[3:-11]
        time=str(nDate)+" "+time
        return  parser.parse(time)

    def getDelimiter(self):
        return ','

    def getFieldNames(self):
        # It is expected for the first row to have the field names.
        return None

    def barsHaveAdjClose(self):
        return self.haveAdjClose
    #TODO
    def parseBar(self, csvRowDict):
        datetime = self._parseTime(csvRowDict[self.nActionDayColName],csvRowDict[self.timeColName])
        preclose = float(csvRowDict[self.preCloseColName])/10000
        open = float(csvRowDict[self.nOpenColName])/10000
        close=float(csvRowDict[self.nOpenColName])/10000
        high = float(csvRowDict[self.nHighColName])/10000
        low = float(csvRowDict[self.nLowColName])/10000
        match = float(csvRowDict[self.nMatchColName])/10000
        askPrice1=float(csvRowDict[self.nAskPrice1ColName])/10000
        askPrice2=float(csvRowDict[self.nAskPrice2ColName])/10000
        askPrice3=float(csvRowDict[self.nAskPrice3ColName])/10000
        askPrice4=float(csvRowDict[self.nAskPrice4ColName])/10000
        askPrice5=float(csvRowDict[self.nAskPrice5ColName])/10000
        askPrice6=float(csvRowDict[self.nAskPrice6ColName])/10000
        askPrice7=float(csvRowDict[self.nAskPrice7ColName])/10000
        askPrice8=float(csvRowDict[self.nAskPrice8ColName])/10000
        askPrice9=float(csvRowDict[self.nAskPrice9ColName])/10000
        askPrice10=float(csvRowDict[self.nAskPrice10ColName])/10000
        askVol1=float(csvRowDict[self.nAskVol1ColName])
        askVol2=float(csvRowDict[self.nAskVol2ColName])
        askVol3=float(csvRowDict[self.nAskVol3ColName])
        askVol4=float(csvRowDict[self.nAskVol4ColName])
        askVol5=float(csvRowDict[self.nAskVol5ColName])
        askVol6=float(csvRowDict[self.nAskVol6ColName])
        askVol7=float(csvRowDict[self.nAskVol7ColName])
        askVol8=float(csvRowDict[self.nAskVol8ColName])
        askVol9=float(csvRowDict[self.nAskVol9ColName])
        askVol10=float(csvRowDict[self.nAskVol10ColName])
        bidPrice1=float(csvRowDict[self.nBidPrice1ColName])/10000
        bidPrice2=float(csvRowDict[self.nBidPrice2ColName])/10000
        bidPrice3=float(csvRowDict[self.nBidPrice3ColName])/10000
        bidPrice4=float(csvRowDict[self.nBidPrice4ColName])/10000
        bidPrice5=float(csvRowDict[self.nBidPrice5ColName])/10000
        bidPrice6=float(csvRowDict[self.nBidPrice6ColName])/10000
        bidPrice7=float(csvRowDict[self.nBidPrice7ColName])/10000
        bidPrice8=float(csvRowDict[self.nBidPrice8ColName])/10000
        bidPrice9=float(csvRowDict[self.nBidPrice9ColName])/10000
        bidPrice10=float(csvRowDict[self.nBidPrice10ColName])/10000
        bidVol1=float(csvRowDict[self.nBidVol1ColName])
        bidVol2=float(csvRowDict[self.nBidVol2ColName])
        bidVol3=float(csvRowDict[self.nBidVol3ColName])
        bidVol4=float(csvRowDict[self.nBidVol4ColName])
        bidVol5=float(csvRowDict[self.nBidVol5ColName])
        bidVol6=float(csvRowDict[self.nBidVol6ColName])
        bidVol7=float(csvRowDict[self.nBidVol7ColName])
        bidVol8=float(csvRowDict[self.nBidVol8ColName])
        bidVol9=float(csvRowDict[self.nBidVol9ColName])
        bidVol10=float(csvRowDict[self.nBidVol10ColName])
        numTradesColName=float(csvRowDict[self.nNumTradesColName])
        volume=float(csvRowDict[self.iVolumeColName])
        turnover=float(csvRowDict[self.iTurnoverColName])
        totalbidvol=float(csvRowDict[self.nTotalBidVolColName])
        totalaskvol=float(csvRowDict[self.nTotalAskVolColName])
        weightedavgbidprice=float(csvRowDict[self.nWeightedAvgBidPriceColName])/10000
        weightedavgaskprice=float(csvRowDict[self.nWeightedAvgAskPriceColName])/10000

        return TickBar.TickBar(datetime, preclose, open,close, high, low, match, askPrice1, askPrice2, askPrice3, askPrice4, askPrice5, askPrice6, askPrice7, askPrice8, askPrice9, askPrice10, bidPrice1, bidPrice2, bidPrice3, bidPrice4, bidPrice5, bidPrice6, bidPrice7, bidPrice8, bidPrice9, bidPrice10, askVol1, askVol2, askVol3, askVol4, askVol5, askVol6, askVol7, askVol8, askVol9, askVol10, bidVol1, bidVol2, bidVol3, bidVol4, bidVol5, bidVol6, bidVol7, bidVol8, bidVol9, bidVol10, numTradesColName, volume, turnover, totalaskvol, totalbidvol, weightedavgaskprice, weightedavgbidprice, self.__frequency)


class TickBarFeed(BarFeed):
    def __init__(self,frequency,timezone=None,maxLen=dataseries.DEFAULT_MAX_LEN):
        BarFeed._init_(self,frequency,maxLen)
        self._timezone=timezone
        self.dateTimeFormat= "%Y-%m-%d %H:%M:%S"
        self.barsHaveAdjClose=False
        #TODO
        self.columnNames={
            "nTime":"time",
            'nPreClose':'nPreClose',
            "nOpen":"nOpen",
            "nHigh":"nHigh",
            "nLow":"nLow",
            "nMatch":"nMatch",
            'nActionDay':'nActionDay',
            "nAskPrice1":"nAskPrice1",
            "nAskPrice2":"nAskPrice2",
            "nAskPrice3":"nAskPrice3",
            "nAskPrice4":"nAskPrice4",
            "nAskPrice5":"nAskPrice5",
            "nAskPrice6":"nAskPrice6",
            "nAskPrice7":"nAskPrice7",
            "nAskPrice8":"nAskPrice8",
            "nAskPrice9":"nAskPrice9",
            "nAskPrice10":"nAskPrice10",
            "nAskVol1":"nAskVol1",
            "nAskVol2":"nAskVol2",
            "nAskVol3":"nAskVol3",
            "nAskVol4":"nAskVol4",
            "nAskVol5":"nAskVol5",
            "nAskVol6":"nAskVol6",
            "nAskVol7":"nAskVol7",
            "nAskVol8":"nAskVol8",
            "nAskVol9":"nAskVol9",
            "nAskVol10":"nAskVol10",
            "nBidPrice1":"nBidPrice1",
            "nBidPrice2":"nBidPrice2",
            "nBidPrice3":"nBidPrice3",
            "nBidPrice4":"nBidPrice4",
            "nBidPrice5":"nBidPrice5",
            "nBidPrice6":"nBidPrice6",
            "nBidPrice7":"nBidPrice7",
            "nBidPrice8":"nBidPrice8",
            "nBidPrice9":"nBidPrice9",
            "nBidPrice10":"nBidPrice10",
            "nBidVol1":"nBidVol1",
            "nBidVol2":"nBidVol2",
            "nBidVol3":"nBidVol3",
            "nBidVol4":"nBidVol4",
            "nBidVol5":"nBidVol5",
            "nBidVol6":"nBidVol6",
            "nBidVol7":"nBidVol7",
            "nBidVol8":"nBidVol8",
            "nBidVol9":"nBidVol9",
            "nBidVol10":"nBidVol10",
            "nNumTrades":"nNumTrades",
            "iVolume":"iVolume",
            "iTurnover":"iTurnover",
            "nTotalBidVol":"nTotalBidVol",
            "nTotalAskVol":"nTotalAskVol",
            "nWeightedAvgBidPrice":"nWeightedAvgBidPrice",
            "nWeightedAvgAskPrice":"nWeightedAvgAskPrice"

        }
        self.setDailyBarTime(None)

    def setColumnName(self,col,name):
        self.columnNames[col]=name

    def setDateTimeFormat(self,dateTimeFormat):
        self.dateTimeFormat=dateTimeFormat

    def barsHaveAdjClose(self):
        return self.haveAdjClose




    def addBarsFromCSV(self, instrument, path, timezone=None):
        if timezone is None:
            timezone = self._timezone

        rowParser = TickRowParser(self.columnNames, self.dateTimeFormat, self.getDailyBarTime(), self.getFrequency(), timezone)
        BarFeed.addBarsFromCSV(self, instrument, path, rowParser)

