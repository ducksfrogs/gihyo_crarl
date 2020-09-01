import re
import time
import requests
import lxml.html
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
collection = client.sk.ebook
collection.create_index('key', unique=True)


session = requests.Session()
response = session.get('https://gihyo.jp/dp')


html = lxml.html.fromstring(response.text)
html.make_links_absolute(base_url=response.url)


for a in html.cssselect('#listBook > li > a[itemprop = "url"]'):
    url = a.get('href')
    print(url)


response.url


def myfunc():
    yield "one"
    yield "two"
    yield  "three"


x = myfunc()


x.__next__()


x.__next__()


def myfunc(x:int):
    for x_ in range(x):
        yield x_*2
        



for i in myfunc(5):
    print(i)



