import threading
from qpython import qconnection
import numpy as np
class OrderHandler(threading.Thread):
    def __init__(self,host,port,sym):
        q_m=qconnection.QConnection(host=host,port=port,pandas=True)
        q_m.open()
        #TODO 换成订阅订单消息
        self.q.sync('.u.sub', np.string_('Market'), np.string_('' if self.sym == [] else self.sym))
    def run(self):
        pass

    def buy(self):
        pass

    def sell(self):
        pass

    def cancel(self):
        pass

