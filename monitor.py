from webhook import sendAlert
import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook
from datetime import datetime

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}

proxyList = []
count = 0

with open('proxyList.txt') as f:
    for line in f:
        line = line.strip()
        line = line.split(':')
        proxyHTTP = line[0] + ':' + line[1]
        proxyList.append(proxyHTTP)
proxyListLength = len(proxyList)

while True:
    with open('productList.txt') as f:
        for line in f:
            line = line.strip()
            productURL = line

            proxies = {
                "http": "http://" + proxyList[count],
                "https": "http://" + proxyList[count],
            }

            count += 1
            if count == proxyListLength:
                count = 0

            response = requests.get(productURL, headers=headers)
            response.proxies = proxies
            print(response.proxies)
            soup = BeautifulSoup(response.text, 'html.parser')

            productName = soup.find('h1', attrs={'class', 'v-fw-regular'}).get_text()
            imageURL = soup.find('img', attrs={'class', 'primary-image'})['src']

            rawSKU = soup.find('div', attrs={'class': 'sku product-data'}).get_text().strip()
            sku = rawSKU.split('SKU:')[1]

            rawPrice = soup.find('div', attrs={'class': 'priceView-hero-price'}).get_text()
            price = rawPrice.split('Your')[0]

            ATC = 'https://api.bestbuy.com/click/-/' + sku + '/cart'

            availability = soup.find('button', attrs={'class': 'add-to-cart-button'}).get_text()

            if (availability == 'Add to Cart'):
                sendAlert(productURL, productName, price, sku, imageURL, ATC)
                print(productName + ' RESTOCKED')
            else:
                print(productName + ' OOS')