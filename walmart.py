from webhook import sendWalmartAlert
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
    with open('walmartLinks.txt') as f:
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
            soup = BeautifulSoup(response.text, 'html.parser')

            productName = soup.find('h1', attrs={'class', 'prod-ProductTitle'}).get_text()
            imageURL = soup.find('img', attrs={'class', 'prod-hero-image-image'})['src']

            urlArray = productURL.split('/')
            arrayLength = len(urlArray)
            sku = urlArray[arrayLength - 1]

            rawPrice = soup.find('span', attrs={'class': 'price-characteristic'}).get_text()
            price = '$' + rawPrice

            ATC = 'https://affil.walmart.com/cart/addToCart?items=' + sku

            availability = soup.find('span', attrs={'class': 'spin-button-children'}).get_text()

            if (availability != 'Sold Out'):
                sendWalmartAlert(productURL, productName, price, sku, imageURL, ATC)
                print(productName + ' RESTOCKED')
            else:
                print(productName + ' OOS')