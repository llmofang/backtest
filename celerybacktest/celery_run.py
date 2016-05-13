from celery_test import func

if __name__ == "__main__":
    stockcodes=['300251',]
    date=['2016-03-11',]
    p1=list(range(50,700,50))
    p2=list(range(10,100,10))
    p3=list(range(50,750,50))
    p4=list(range(1,5,1))
    func(stockcodes,date,18.90,19.71,18.76,p1,p2,p3,p4)
