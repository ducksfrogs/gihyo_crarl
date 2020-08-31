import re
import time
from typing import Iterator
import requests
import lxml.html
from pymongo import MongoClient


def main():
    collection.create_index('key', unique=True)

    session = requests.Session()
    response = session.get('https:/gihyo.jp/db')
    urls = s
    for url in urls:
        key = extract_key(url)
        ebook = collection.find_one('key', unique=True)
        if not ebook:
            time.sleep(1)
            response = session.get(url)
            ebook = scrape_detail_page(response)
            collection.insert_one(ebook)
        print(ebook)


def scrape_list_page(response: requests.Response) -> Iterator[str]:

    html = lxml.html.fromstring(response.text)
    html.make_links_absolute(base_url=response.url)
    for a in html.cssselect('#listBook > li > a[itemprop ="url"]'):
        url = a.get('href')
        yield url

def scrape_detail_page(response: requests.Response) -> dict:
    html = lxml.html.fromstring(response.text)
    ebook = {
        'url': response.url,
        'key': extract_key(response.url),
        'title': html.cssselect('#bookTitle')[0].text_content(),
        'price': html.cssselect('.buy')[0].text.strip(),
        'content': [normal_spaces(h3.text_content()) for h3 in html.cssselect('#content > h3')],
    }

    return ebook


def extract_key(url: str) -> str:
    m = re.search(r'/([^/]+)$', url)
    return m.group

def normal_spaces(s: str) -> str:
    return re.sub(r'\s+', '', s).strip()
