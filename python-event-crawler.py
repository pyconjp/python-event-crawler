#!/usr/bin/env python

from datetime import datetime

import requests
from dateutil.relativedelta import relativedelta

# keywords for event search
KEYWORDS = ('python', 'pycon', 'sphinx', 'ansible',
            'django', 'pyramind', 'pydata')

def get_connpass_event(keywords, ym):
    """
    get connpass events by keywords
    API reference: http://connpass.com/about/api/

    :param keywords: keywords for event search
    :param ym: event ym(e.g.: 201605)
    """
    result = []
    payload = {
        'keyword_or': keywords,
        'count': 100,
        'ym': ym,
    }
    r = requests.get('http://connpass.com/api/v1/event/', params=payload)
    responce = r.json()
    for event in responce['events']:
        event_dict = {
            'title': event['title'],
            'url': event['event_url'],
            'date': event['started_at'],
            'address': event['address'],
        }
        result.append(event_dict)

    return result
      
def get_atnd_event(keywords, ym):
    """
    get atnd events by keywords
    API reference: http://api.atnd.org/#events-query

    :param keywords: keywords for event search
    :param ym: event ym(e.g.: 201605)
    """
    result = []
    payload = {
        'keyword_or': keywords,
        'count': 100,
        'ym': ym,
        'format': 'json',
    }
    r = requests.get('http://api.atnd.org/events/', params=payload)
    responce = r.json()
    for event in responce['events']:
        event_dict = {
            'title': event['event']['title'],
            'url': event['event']['event_url'],
            'date': event['event']['started_at'],
            'address': event['event']['address'],
        }
        result.append(event_dict)
      
    return result


def get_doorkeeper_event(keywords, ym):
    """
    get doorkeeper events by keywords
    API reference: http://www.doorkeeperhq.com/developer/api

    :param keywords: keywords for event search
    :param ym: event ym(e.g.: 201605)
    """
    result = []

    since = datetime(ym // 100, ym % 100, 1)
    until = since + relativedelta(months=+1)

    for keyword in keywords:
        payload = {
            'q': keyword,
            'since': since,
            'until': until,
        }
        r = requests.get('https://api.doorkeeper.jp/events/', params=payload)
        responce = r.json()
        for event in responce:
            event_dict = {
                'title': event['event']['title'],
                'url': event['event']['public_url'],
                'date': event['event']['starts_at'],
                'address': event['event']['address'],
            }
            result.append(event_dict)

    return result

def main():
    print(len(get_connpass_event(KEYWORDS, 201604)))
    print(len(get_atnd_event(KEYWORDS, 201604)))
    print(len(get_doorkeeper_event(KEYWORDS, 201604)))

if __name__ == '__main__':
    main()
