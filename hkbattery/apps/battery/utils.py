import requests


def exchange_rate(source, target):
    r = requests.get('https://currency-api.appspot.com/api/{0}/{1}.json'
                     .format(source, target))
    return r.json()['amount']
