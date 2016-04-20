from celery import Celery
import requests
app = Celery('celery_blog',bloker='redis://localhost:6379/0')

@app.task
def fetch_url(url):
     resp = requests.get(url)
     print(resp.status_code)

def func(urls):
     for url in urls:
       fetch_url.delay(url)

if __name__ == "__main__":
     func(["http://oneapm.com", "http://jd.com", "https://taobao.com", "http://baidu.com", "http://news.oneapm.com"])