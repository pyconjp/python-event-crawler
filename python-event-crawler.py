#!/usr/bin/env python

from datetime import datetime
from operator import itemgetter

import requests
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse

# keywords for event search
KEYWORDS = ('python', 'pycon', 'sphinx', 'ansible',
            'django', 'pyramind', 'pydata')

WEEKDAY = ('月','火','水','木','金','土','日')

def get_connpass_event(keywords, ym):
    """
    get connpass events by keywords
    API reference: http://connpass.com/about/api/

    :param keywords: keywords for event search
    :param ym: event ym(e.g.: 201605)
    """
    events = []
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
            'date': parse(event['started_at']),
            'address': event['address'],
        }
        events.append(event_dict)

    return events
      
def get_atnd_event(keywords, ym):
    """
    get atnd events by keywords
    API reference: http://api.atnd.org/#events-query

    :param keywords: keywords for event search
    :param ym: event ym(e.g.: 201605)
    """
    events = []
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
            'date': parse(event['event']['started_at']),
            'address': event['event']['address'],
        }
        events.append(event_dict)
      
    return events


def get_doorkeeper_event(keywords, ym):
    """
    get doorkeeper events by keywords
    API reference: http://www.doorkeeperhq.com/developer/api

    :param keywords: keywords for event search
    :param ym: event ym(e.g.: 201605)
    """
    events = []

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
                'date': parse(event['event']['starts_at']),
                'address': event['event']['address'],
            }
            events.append(event_dict)

    return events


def format_date(date):
    """
    convert date to date string(e.g.: 4月5日(火))
    """
    weekday = WEEKDAY[date.weekday()]
    date_str = '{:d}月{:d}日({})'.format(date.month, date.day, weekday)

    return date_str


def convert_place(address):
    place = address

    return place

def main():

    events = []
    #events = get_connpass_event(KEYWORDS, 201604)
    events.extend(get_atnd_event(KEYWORDS, 201604))
    #events.extend(get_doorkeeper_event(KEYWORDS, 201604))
    # sort by date
    events.sort(key=itemgetter('date'))
    print('<ul>')
    for event in events:
        date_str = format_date(event['date'])
        place = convert_place(event['address'])
        print('<li>{0} <a href="{url}">{title}</a> ({1})</li>'.format(date_str, place, **event))
    print('</ul>')
      
if __name__ == '__main__':
    main()
