from pyalgotrade import dataseries


class TickBarDataSeries(dataseries.SequenceDataSeries):
    def __init__(self,maxLen=dataseries.DEFAULT_MAX_LEN):
        dataseries.SequenceDataSeries.__init__(self,maxLen)
        self.datetimeDS	=	dataseries.SequenceDataSeries(maxLen)
        self.precloseDS	=	dataseries.SequenceDataSeries(maxLen)
        self.openDS	=	dataseries.SequenceDataSeries(maxLen)
        self.highDS	=	dataseries.SequenceDataSeries(maxLen)
        self.lowDS	=	dataseries.SequenceDataSeries(maxLen)
        self.matchDS	=	dataseries.SequenceDataSeries(maxLen)
        self.askPrice1DS	=	dataseries.SequenceDataSeries(maxLen)
        self.askPrice2DS	=	dataseries.SequenceDataSeries(maxLen)
        self.askPrice3DS	=	dataseries.SequenceDataSeries(maxLen)
        self.askPrice4DS	=	dataseries.SequenceDataSeries(maxLen)
        self.askPrice5DS	=	dataseries.SequenceDataSeries(maxLen)
        self.askPrice6DS	=	dataseries.SequenceDataSeries(maxLen)
        self.askPrice7DS	=	dataseries.SequenceDataSeries(maxLen)
        self.askPrice8DS	=	dataseries.SequenceDataSeries(maxLen)
        self.askPrice9DS	=	dataseries.SequenceDataSeries(maxLen)
        self.askPrice10DS	=	dataseries.SequenceDataSeries(maxLen)
        self.bidPrice1DS	=	dataseries.SequenceDataSeries(maxLen)
        self.bidPrice2DS	=	dataseries.SequenceDataSeries(maxLen)
        self.bidPrice3DS	=	dataseries.SequenceDataSeries(maxLen)
        self.bidPrice4DS	=	dataseries.SequenceDataSeries(maxLen)
        self.bidPrice5DS	=	dataseries.SequenceDataSeries(maxLen)
        self.bidPrice6DS	=	dataseries.SequenceDataSeries(maxLen)
        self.bidPrice7DS	=	dataseries.SequenceDataSeries(maxLen)
        self.bidPrice8DS	=	dataseries.SequenceDataSeries(maxLen)
        self.bidPrice9DS	=	dataseries.SequenceDataSeries(maxLen)
        self.bidPrice10DS	=	dataseries.SequenceDataSeries(maxLen)
        self.askVol1DS	=	dataseries.SequenceDataSeries(maxLen)
        self.askVol2DS	=	dataseries.SequenceDataSeries(maxLen)
        self.askVol3DS	=	dataseries.SequenceDataSeries(maxLen)
        self.askVol4DS	=	dataseries.SequenceDataSeries(maxLen)
        self.askVol5DS	=	dataseries.SequenceDataSeries(maxLen)
        self.askVol6DS	=	dataseries.SequenceDataSeries(maxLen)
        self.askVol7DS	=	dataseries.SequenceDataSeries(maxLen)
        self.askVol8DS	=	dataseries.SequenceDataSeries(maxLen)
        self.askVol9DS	=	dataseries.SequenceDataSeries(maxLen)
        self.askVol10DS	=	dataseries.SequenceDataSeries(maxLen)
        self.bidVol1DS	=	dataseries.SequenceDataSeries(maxLen)
        self.bidVol2DS	=	dataseries.SequenceDataSeries(maxLen)
        self.bidVol3DS	=	dataseries.SequenceDataSeries(maxLen)
        self.bidVol4DS	=	dataseries.SequenceDataSeries(maxLen)
        self.bidVol5DS	=	dataseries.SequenceDataSeries(maxLen)
        self.bidVol6DS	=	dataseries.SequenceDataSeries(maxLen)
        self.bidVol7DS	=	dataseries.SequenceDataSeries(maxLen)
        self.bidVol8DS	=	dataseries.SequenceDataSeries(maxLen)
        self.bidVol9DS	=	dataseries.SequenceDataSeries(maxLen)
        self.bidVol10DS	=	dataseries.SequenceDataSeries(maxLen)
        self.numTradesColNameDS	=	dataseries.SequenceDataSeries(maxLen)
        self.volumeDS	=	dataseries.SequenceDataSeries(maxLen)
        self.turnoverDS	=	dataseries.SequenceDataSeries(maxLen)
        self.totalaskvolDS	=	dataseries.SequenceDataSeries(maxLen)
        self.totalbidvolDS	=	dataseries.SequenceDataSeries(maxLen)
        self.weightedavgaskpriceDS	=	dataseries.SequenceDataSeries(maxLen)
        self.weightedavgbidpriceDS	=	dataseries.SequenceDataSeries(maxLen)

    def append(self,bar):
         self.appendWithDateTime(bar.getDateTime(), bar)

    def appendWithDateTime(self, dateTime, bar):
        assert(dateTime is not None)
        assert (bar is not None)
        dataseries.SequenceDataSeries.appendWithDateTime(self,dateTime,bar)
        self.precloseDS.appendWithDateTime(dateTime,bar.getPreClose())
        self.openDS.appendWithDateTime(dateTime, bar.getOpen())
        self.highDS.appendWithDateTime(dateTime, bar.getHigh())
        self.lowDS.appendWithDateTime(dateTime,bar.getLow())
        self.matchDS.appendWithDateTime(dateTime,bar.getMatch())
        self.askPrice1DS.appendWithDateTime(dateTime,bar.getAskPrice1())
        self.askPrice2DS.appendWithDateTime(dateTime,bar.getAskPrice2())
        self.askPrice3DS.appendWithDateTime(dateTime,bar.getAskPrice3())
        self.askPrice4DS.appendWithDateTime(dateTime,bar.getAskPrice4())
        self.askPrice5DS.appendWithDateTime(dateTime,bar.getAskPrice5())
        self.askPrice6DS.appendWithDateTime(dateTime,bar.getAskPrice6())
        self.askPrice7DS.appendWithDateTime(dateTime,bar.getAskPrice7())
        self.askPrice8DS.appendWithDateTime(dateTime,bar.getAskPrice8())
        self.askPrice9DS.appendWithDateTime(dateTime,bar.getAskPrice9())
        self.askPrice10DS.appendWithDateTime(dateTime,bar.getAskPrice10())
        self.bidPrice1DS.appendWithDateTime(dateTime,bar.getBidPrice1())
        self.bidPrice2DS.appendWithDateTime(dateTime,bar.getBidPrice2())
        self.bidPrice3DS.appendWithDateTime(dateTime,bar.getBidPrice3())
        self.bidPrice4DS.appendWithDateTime(dateTime,bar.getBidPrice4())
        self.bidPrice5DS.appendWithDateTime(dateTime,bar.getBidPrice5())
        self.bidPrice6DS.appendWithDateTime(dateTime,bar.getBidPrice6())
        self.bidPrice7DS.appendWithDateTime(dateTime,bar.getBidPrice7())
        self.bidPrice8DS.appendWithDateTime(dateTime,bar.getBidPrice8())
        self.bidPrice9DS.appendWithDateTime(dateTime,bar.getBidPrice9())
        self.bidPrice10DS.appendWithDateTime(dateTime,bar.getBidPrice10())
        self.askVol1DS.appendWithDateTime(dateTime,bar.getAskVol1())
        self.askVol2DS.appendWithDateTime(dateTime,bar.getAskVol2())
        self.askVol3DS.appendWithDateTime(dateTime,bar.getAskVol3())
        self.askVol4DS.appendWithDateTime(dateTime,bar.getAskVol4())
        self.askVol5DS.appendWithDateTime(dateTime,bar.getAskVol5())
        self.askVol6DS.appendWithDateTime(dateTime,bar.getAskVol6())
        self.askVol7DS.appendWithDateTime(dateTime,bar.getAskVol7())
        self.askVol8DS.appendWithDateTime(dateTime,bar.getAskVol8())
        self.askVol9DS.appendWithDateTime(dateTime,bar.getAskVol9())
        self.askVol10DS.appendWithDateTime(dateTime,bar.getAskVol10())
        self.bidVol1DS.appendWithDateTime(dateTime,bar.getBidVol1())
        self.bidVol2DS.appendWithDateTime(dateTime,bar.getBidVol2())
        self.bidVol3DS.appendWithDateTime(dateTime,bar.getBidVol3())
        self.bidVol4DS.appendWithDateTime(dateTime,bar.getBidVol4())
        self.bidVol5DS.appendWithDateTime(dateTime,bar.getBidVol5())
        self.bidVol6DS.appendWithDateTime(dateTime,bar.getBidVol6())
        self.bidVol7DS.appendWithDateTime(dateTime,bar.getBidVol7())
        self.bidVol8DS.appendWithDateTime(dateTime,bar.getBidVol8())
        self.bidVol9DS.appendWithDateTime(dateTime,bar.getBidVol9())
        self.bidVol10DS.appendWithDateTime(dateTime,bar.getBidVol10())
        self.numTradesColNameDS.appendWithDateTime(dateTime,bar.getNumTradeColName())
        self.volumeDS.appendWithDateTime(dateTime,bar.getVolume())
        self.turnoverDS.appendWithDateTime(dateTime,bar.getTurnOver())
        self.totalaskvolDS.appendWithDateTime(dateTime,bar.getTotalAskVol())
        self.totalbidvolDS.appendWithDateTime(dateTime,bar.getTotalBidVol())
        self.weightedavgaskpriceDS.appendWithDateTime(dateTime,bar.getWeightedAvgAskPrice())
        self.weightedavgbidpriceDS.appendWithDateTime(dateTime,bar.getWeightedAvgBidPrice())

    def getPreOpenDataSeries(self):
        return self.precloseDS

    def getOpenDataSeries(self):
        return self.openDS

    def gethighDataSeries(self):
        return self.highDS

    #如要取得bar中的序列在这添加方法

    def getMatchDataSeries(self):
        return self.matchDS