import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

business_list = []


def extract(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup.find_all('div', {'class': 'row businessCapsule--mainRow'})


def transform(articles):
    for item in articles:
        name = item.find('h2', {'class': 'businessCapsule--name text-h2'}).text
        address = item.find('span', {'itemprop': 'address'}).text.strip().replace('\n', '')
        try:
            website = item.find('a', {'target': '_blank'})['href']
        except:
            website = ''
        try:
            phone = item.find('span', {'class': 'business--telephoneNumber'}).text.strip()
        except:
            phone = ''
        business = {
            'name': name,
            'address': address,
            'website': website,
            'phone': phone
        }
        business_list.append(business)
    return


def load():
    df = pd.DataFrame(business_list)
    df.to_csv('coffee-shops-london.csv', index=False)


for x in range(1, 9):
    print(f'Getting page {x}')
    articles = extract(
        f'https://www.yell.com/ucs/UcsSearchAction.do?scrambleSeed=540269558&keywords=cafes+%26+coffee+shops&location=london&pageNum={x}')
    transform(articles)
    time.sleep(5)

load()
print('Saved to CSV')
