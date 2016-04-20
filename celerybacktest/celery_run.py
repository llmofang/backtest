from celery_test import func

if __name__ == "__main__":
    stockcodes=['300251',]
    date=['2016-02-29',]
    p1=list(range(150,250,10))
    p2=list(range(50,100,10))
    p3=list(range(150,250,10))
    p4=list(range(20,40,5))
    func(stockcodes,date,p1,p2,p3,p4)