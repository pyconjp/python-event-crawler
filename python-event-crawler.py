#!/usr/bin/env python

import argparse
from datetime import datetime
from operator import itemgetter

import requests
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse

# keywords for event search
KEYWORDS = ('python', 'pycon', 'sphinx', 'ansible',
            'django', 'pyramind', 'pydata')

# exclude keywords for event list
EX_WORDS = ('pepper', )

TOKYO_23KU = (
    '千代田区', '中央区', '港区', '新宿区', '文京区', '台東区', '墨田区',
    '江東区', '品川区', '目黒区', '大田区', '世田谷区', '渋谷区', '中野区',
    '杉並区', '豊島区', '北区', '荒川区', '板橋区', '練馬区', '足立区',
    '葛飾区', '江戸川区')

WEEKDAY = '月火水木金土日'


def _has_ex_words(title):
    title = title.lower()
    for ex_word in EX_WORDS:
        if ex_word in title:
            return True
    return False


def connpass_events(keywords, ym):
    """
    get connpass events by keywords
    API reference: https://connpass.com/about/api/

    :param keywords: keywords for event search
    :param ym: event ym(e.g.: 201605)
    """
    events = []
    payload = {
        'keyword_or': keywords,
        'count': 100,
        'ym': ym,
    }
    r = requests.get('https://connpass.com/api/v1/event/', params=payload)
    responce = r.json()
    for event in responce['events']:
        if not _has_ex_words(event['title']):
            event_dict = {
                'title': event['title'],
                'url': event['event_url'],
                'date': parse(event['started_at']),
                'address': event['address'],
            }
            events.append(event_dict)

    return events


def atnd_events(keywords, ym):
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


def doorkeeper_events(keywords, ym):
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
            if not _has_ex_words(event['event']['title']):
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
    """
    convert address to place

    >>> convert_place('東京都台東区浅草橋5-4-5')
    '東京'
    >>> convert_place('大阪府大阪市福島区福島5丁目')
    '大阪府大阪市'
    >>> convert_place('京都市中京区末丸町')
    '京都市'
    >>> convert_place('渋谷区千駄ヶ谷5-32')
    '東京'
    """

    place = address

    if address:
        if '東京都' in address:
            place = '東京'
        elif '市' in address:
            place = address[:address.find('市') + 1]
        if '区' in place:
            place = place[:place.find('区') + 1]
        if place in TOKYO_23KU:
            place = '東京'

    return place


def main(ym):
    """
    :param ym: target year and month with 6 digits(e.g.: 201605)
    """

    events = []
    events += connpass_events(KEYWORDS, ym)
    events += atnd_events(KEYWORDS, ym)
    events += doorkeeper_events(KEYWORDS, ym)

    print('<ul>')

    EVENT_HTML = '<li>{date_str} <a href="{url}">{title}</a> ({place})</li>'
    # sort by date
    events.sort(key=itemgetter('date'))
    for event in events:
        event['date_str'] = format_date(event['date'])
        event['place'] = convert_place(event['address'])
        print(EVENT_HTML.format(**event))

    print('</ul>')


if __name__ == '__main__':

    # default ym is current month
    next_month = datetime.now()
    default_ym = next_month.year * 100 + next_month.month

    help_text = 'target year and month by 6 digits(default: {:d})'
    parser = argparse.ArgumentParser()
    parser.add_argument("ym", type=int, nargs='?', default=default_ym,
                        help=help_text.format(default_ym))
    args = parser.parse_args()

    main(args.ym)
