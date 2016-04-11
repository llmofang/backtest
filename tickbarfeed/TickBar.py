# PyAlgoTrade
#
# Copyright 2011-2015 Gabriel Martin Becedillas Ruiz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""

import abc

from pyalgotrade import warninghelpers


class Frequency(object):

    """Enum like class for bar frequencies. Valid values are:

    * **Frequency.TRADE**: The bar represents a single trade.
    * **Frequency.SECOND**: The bar summarizes the trading activity during 1 second.
    * **Frequency.MINUTE**: The bar summarizes the trading activity during 1 minute.
    * **Frequency.HOUR**: The bar summarizes the trading activity during 1 hour.
    * **Frequency.DAY**: The bar summarizes the trading activity during 1 day.
    * **Frequency.WEEK**: The bar summarizes the trading activity during 1 week.
    * **Frequency.MONTH**: The bar summarizes the trading activity during 1 month.
    """

    # It is important for frequency values to get bigger for bigger windows.
    TRADE = -1
    SECOND = 1
    TICK=3
    MINUTE = 60
    HOUR = 60*60
    DAY = 24*60*60
    WEEK = 24*60*60*7
    MONTH = 24*60*60*31





class TickBar():
    # Optimization to reduce memory footprint.
    __slots__ = (
            'datetime','preclose','open','close','high','low','match','askPrice1','askPrice2','askPrice3','askPrice4','askPrice5','askPrice6','askPrice7','askPrice8','askPrice9','askPrice10','bidPrice1','bidPrice2','bidPrice3','bidPrice4','bidPrice5','bidPrice6','bidPrice7','bidPrice8','bidPrice9','bidPrice10','askVol1','askVol2','askVol3','askVol4','askVol5','askVol6','askVol7','askVol8','askVol9','askVol10','bidVol1','bidVol2','bidVol3','bidVol4','bidVol5','bidVol6','bidVol7','bidVol8','bidVol9','bidVol10','numTradesColName','volume','turnover','totalaskvol','totalbidvol','weightedavgaskprice','weightedavgbidprice','frequency'
    )

    def __init__(self,datetime,preclose,open,close,high,low,match,askPrice1,askPrice2,askPrice3,askPrice4,askPrice5,askPrice6,askPrice7,askPrice8,askPrice9,askPrice10,bidPrice1,bidPrice2,bidPrice3,bidPrice4,bidPrice5,bidPrice6,bidPrice7,bidPrice8,bidPrice9,bidPrice10,askVol1,askVol2,askVol3,askVol4,askVol5,askVol6,askVol7,askVol8,askVol9,askVol10,bidVol1,bidVol2,bidVol3,bidVol4,bidVol5,bidVol6,bidVol7,bidVol8,bidVol9,bidVol10,numTradesColName,volume,turnover,totalaskvol,totalbidvol,weightedavgaskprice,weightedavgbidprice,frequency):
        # if high < low:
        #     raise Exception("high < low on %s" % (dateTime))
        # elif high < open_:
        #     raise Exception("high < open on %s" % (dateTime))
        # elif high < close:
        #     raise Exception("high < close on %s" % (dateTime))
        # elif low > open_:
        #     raise Exception("low > open on %s" % (dateTime))
        # elif low > close:
        #     raise Exception("low > close on %s" % (dateTime))
        self.datetime = datetime
        self.preclose	=	preclose
        self.open	=	open
        self.close = close
        self.high	=	high
        self.low	=	low
        self.match	=	match
        self.askPrice1	=	askPrice1
        self.askPrice2	=	askPrice2
        self.askPrice3	=	askPrice3
        self.askPrice4	=	askPrice4
        self.askPrice5	=	askPrice5
        self.askPrice6	=	askPrice6
        self.askPrice7	=	askPrice7
        self.askPrice8	=	askPrice8
        self.askPrice9	=	askPrice9
        self.askPrice10	=	askPrice10
        self.bidPrice1	=	bidPrice1
        self.bidPrice2	=	bidPrice2
        self.bidPrice3	=	bidPrice3
        self.bidPrice4	=	bidPrice4
        self.bidPrice5	=	bidPrice5
        self.bidPrice6	=	bidPrice6
        self.bidPrice7	=	bidPrice7
        self.bidPrice8	=	bidPrice8
        self.bidPrice9	=	bidPrice9
        self.bidPrice10	=	bidPrice10
        self.askVol1	=	askVol1
        self.askVol2	=	askVol2
        self.askVol3	=	askVol3
        self.askVol4	=	askVol4
        self.askVol5	=	askVol5
        self.askVol6	=	askVol6
        self.askVol7	=	askVol7
        self.askVol8	=	askVol8
        self.askVol9	=	askVol9
        self.askVol10	=	askVol10
        self.bidVol1	=	bidVol1
        self.bidVol2	=	bidVol2
        self.bidVol3	=	bidVol3
        self.bidVol4	=	bidVol4
        self.bidVol5	=	bidVol5
        self.bidVol6	=	bidVol6
        self.bidVol7	=	bidVol7
        self.bidVol8	=	bidVol8
        self.bidVol9	=	bidVol9
        self.bidVol10	=	bidVol10
        self.numTradesColName	=	numTradesColName
        self.volume	=	volume
        self.turnover	=	turnover
        self.totalaskvol	=	totalaskvol
        self.totalbidvol	=	totalbidvol
        self.weightedavgaskprice	=	weightedavgaskprice
        self.weightedavgbidprice	=	weightedavgbidprice
        self.frequency=frequency


    def __setstate__(self, state):
        (self.datetime	,
        self.preclose	,
        self.open	,
        self.close,
        self.high	,
        self.low	,
        self.match	,
        self.askPrice1	,
        self.askPrice2	,
        self.askPrice3	,
        self.askPrice4	,
        self.askPrice5	,
        self.askPrice6	,
        self.askPrice7	,
        self.askPrice8	,
        self.askPrice9	,
        self.askPrice10	,
        self.bidPrice1	,
        self.bidPrice2	,
        self.bidPrice3	,
        self.bidPrice4	,
        self.bidPrice5	,
        self.bidPrice6	,
        self.bidPrice7	,
        self.bidPrice8	,
        self.bidPrice9	,
        self.bidPrice10	,
        self.askVol1	,
        self.askVol2	,
        self.askVol3	,
        self.askVol4	,
        self.askVol5	,
        self.askVol6	,
        self.askVol7	,
        self.askVol8	,
        self.askVol9	,
        self.askVol10	,
        self.bidVol1	,
        self.bidVol2	,
        self.bidVol3	,
        self.bidVol4	,
        self.bidVol5	,
        self.bidVol6	,
        self.bidVol7	,
        self.bidVol8	,
        self.bidVol9	,
        self.bidVol10	,
        self.numTradesColName	,
        self.volume	,
        self.turnover	,
        self.totalaskvol	,
        self.totalbidvol	,
        self.weightedavgaskprice	,
        self.weightedavgbidprice,
        self.frequency
         ) = state

    def __getstate__(self):
        return (
           self.datetime	,
            self.preclose	,
            self.open	,
            self.close,
            self.high	,
            self.low	,
            self.match	,
            self.askPrice1	,
            self.askPrice2	,
            self.askPrice3	,
            self.askPrice4	,
            self.askPrice5	,
            self.askPrice6	,
            self.askPrice7	,
            self.askPrice8	,
            self.askPrice9	,
            self.askPrice10	,
            self.bidPrice1	,
            self.bidPrice2	,
            self.bidPrice3	,
            self.bidPrice4	,
            self.bidPrice5	,
            self.bidPrice6	,
            self.bidPrice7	,
            self.bidPrice8	,
            self.bidPrice9	,
            self.bidPrice10	,
            self.askVol1	,
            self.askVol2	,
            self.askVol3	,
            self.askVol4	,
            self.askVol5	,
            self.askVol6	,
            self.askVol7	,
            self.askVol8	,
            self.askVol9	,
            self.askVol10	,
            self.bidVol1	,
            self.bidVol2	,
            self.bidVol3	,
            self.bidVol4	,
            self.bidVol5	,
            self.bidVol6	,
            self.bidVol7	,
            self.bidVol8	,
            self.bidVol9	,
            self.bidVol10	,
            self.numTradesColName	,
            self.volume	,
            self.turnover	,
            self.totalaskvol	,
            self.totalbidvol	,
            self.weightedavgaskprice	,
            self.weightedavgbidprice,
            self.frequency)

    def getFrequency(self):
        return self.frequency

    def getDateTime(self):
        return self.datetime

    def getPreClose(self):
        return self.preclose

    def getOpen(self, adjusted=False):
        return self.open

    def getClose(self,adjusted=False):
        return self.close

    def getHigh(self, adjusted=False):
        return self.high

    def getLow(self, adjusted=False):
        return self.low

    def getMatch(self):
        return self.match

    def getPrice(self):
        return self.match

    def getAskPrice1(self):
        return self.askPrice1

    def getAskPrice2(self):
        return self.askPrice2

    def getAskPrice3(self):
        return self.askPrice3

    def getAskPrice4(self):
        return self.askPrice4

    def getAskPrice5(self):
        return self.askPrice5

    def getAskPrice6(self):
        return self.askPrice6

    def getAskPrice7(self):
        return self.askPrice7

    def getAskPrice8(self):
        return self.askPrice8

    def getAskPrice9(self):
        return self.askPrice9

    def getAskPrice10(self):
        return self.askPrice10

    def getBidPrice1(self):
        return self.bidPrice1

    def getBidPrice2(self):
        return self.bidPrice2

    def getBidPrice3(self):
        return self.bidPrice3

    def getBidPrice4(self):
        return self.bidPrice4

    def getBidPrice5(self):
        return self.bidPrice5

    def getBidPrice6(self):
        return self.bidPrice6

    def getBidPrice7(self):
        return self.bidPrice7

    def getBidPrice8(self):
        return self.bidPrice8

    def getBidPrice9(self):
        return self.bidPrice9

    def getBidPrice10(self):
        return self.bidPrice10

    def getAskVol1(self):
        return self.askVol1

    def getAskVol2(self):
        return self.askVol2

    def getAskVol3(self):
        return self.askVol3

    def getAskVol4(self):
        return self.askVol4

    def getAskVol5(self):
        return self.askVol5

    def getAskVol6(self):
        return self.askVol6

    def getAskVol7(self):
        return self.askVol7

    def getAskVol8(self):
        return self.askVol8

    def getAskVol9(self):
        return self.askVol9

    def getAskVol10(self):
        return self.askVol10

    def getBidVol1(self):
        return self.bidVol1

    def getBidVol2(self):
        return self.bidVol2

    def getBidVol3(self):
        return self.bidVol3

    def getBidVol4(self):
        return self.bidVol4

    def getBidVol5(self):
        return self.bidVol5

    def getBidVol6(self):
        return self.bidVol6

    def getBidVol7(self):
        return self.bidVol7

    def getBidVol8(self):
        return self.bidVol8

    def getBidVol9(self):
        return self.bidVol9

    def getBidVol10(self):
        return self.bidVol10

    def getNumTradeColName(self):
        return self.numTradesColName

    def getVolume(self):
        return self.volume

    def getTurnOver(self):
        return self.turnover

    def getTotalAskVol(self):
        return self.totalaskvol

    def getTotalBidVol(self):
        return self.totalbidvol

    def getWeightedAvgAskPrice(self):
        return self.weightedavgaskprice

    def getWeightedAvgBidPrice(self):
        return self.weightedavgbidprice

class Bars(object):

    """A group of :class:`Bar` objects.

    :param barDict: A map of instrument to :class:`Bar` objects.
    :type barDict: map.

    .. note::
        All bars must have the same datetime.
    """

    def __init__(self, barDict):
        if len(barDict) == 0:
            raise Exception("No bars supplied")

        # Check that bar datetimes are in sync
        firstDateTime = None
        firstInstrument = None
        for instrument, currentBar in barDict.items():
            if firstDateTime is None:
                firstDateTime = currentBar.getDateTime()
                firstInstrument = instrument
            elif currentBar.getDateTime() != firstDateTime:
                raise Exception("Bar data times are not in sync. %s %s != %s %s" % (
                    instrument,
                    currentBar.getDateTime(),
                    firstInstrument,
                    firstDateTime
                ))

        self.__barDict = barDict
        self.__dateTime = firstDateTime

    def __getitem__(self, instrument):
        """Returns the :class:`pyalgotrade.bar.Bar` for the given instrument.
        If the instrument is not found an exception is raised."""
        return self.__barDict[instrument]

    def __contains__(self, instrument):
        """Returns True if a :class:`pyalgotrade.bar.Bar` for the given instrument is available."""
        return instrument in self.__barDict

    def items(self):
        return list(self.__barDict.items())

    def keys(self):
        return list(self.__barDict.keys())

    def getInstruments(self):
        """Returns the instrument symbols."""
        return list(self.__barDict.keys())

    def getDateTime(self):
        """Returns the :class:`datetime.datetime` for this set of bars."""
        return self.__dateTime

    def getBar(self, instrument):
        """Returns the :class:`pyalgotrade.bar.Bar` for the given instrument or None if the instrument is not found."""
        return self.__barDict.get(instrument, None)
