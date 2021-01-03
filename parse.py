import requests
import json


def get_btc_price():
    "Возвращает цену биткоина в USD и EUR"
    url = 'https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR&e=Coinbase&extraParams=your_app_name'
    r = requests.get(url).json()
    return r


def get_eth_xmr_zec_price():
    "Возвращает цену криптовалют в долларах"
    url = 'https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=XMR,ETH,ZEC&extraParams=your_app_name'
    r = requests.get(url).json()
    c = get_btc_price()['USD']
    for k in r.keys():
        r[k] = round(c/r[k], 2)

    return r


def get_dollar_price():
    "Возвращает цену USD в RUB и EUR"
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    r = requests.get(url).json()
    return {
        'RUB': r['Valute']['USD']['Value'],
        'EUR': round(r['Valute']['USD']['Value']*1/r['Valute']['EUR']['Value'], 4),
    }


if __name__ == "__main__":
    print(get_btc_price())
    print(get_eth_xmr_zec_price())
    print(get_dollar_price())