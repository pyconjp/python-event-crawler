#!/usr/bin/env python

import requests

# keywords for event search
KEYWORDS = ('python', 'pycon', 'sphinx', 'ansible', 'django', 'pyramind')

def get_connpass_event(keywords, month):
    """
    get connpass events by keywords
    API reference: http://connpass.com/about/api/

    :param keywords: keywords for event search
    :param month: event month(e.g.: 201605)
    """
    payload = {
        'keyword_or': keywords,
        'count': 100,
        'ym': month,
    }
    r = requests.get('http://connpass.com/api/v1/event/', params=payload)
    responce = r.json()
    for event in responce['events']:
        print(event['title'])
        print(event['event_url'])
        print(event['started_at'])
        print(event['address'])

def get_connpass_event(keywords, month):
    """
    get atnd events by keywords
    API reference: http://api.atnd.org/#events-query

    :param keywords: keywords for event search
    :param month: event month(e.g.: 201605)
    """
    pass

def get_doorkeeper_event(keywords, month):
    """
    get doorkeeper events by keywords
    API reference: http://www.doorkeeperhq.com/developer/api

    :param keywords: keywords for event search
    :param month: event month(e.g.: 201605)
    """
    pass

def main():
    get_connpass_event(KEYWORDS, 201605)

if __name__ == '__main__':
    main()
