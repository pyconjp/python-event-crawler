# python-event-crawler

* create python event list from event site(connpass, atnd and doorkeeper) for PyCon JP Blog
* sample: http://pyconjp.blogspot.jp/2016/04/python-event-201604.html

## How to use

```
$ git clone git@github.com:pyconjp/python-event-crawler.git
$ cd python-event-crawler
$ virtualenv env -p python3
$ . env/bin/activate
(env)$ pip install -r requirements.txt
(env)$ python python-event-crawler -h
Usage: python-event-crawler.py [-h] [ym]

positional arguments:
  ym          target year and month by 6 digits(default: 201605)

optional arguments:
  -h, --help  show this help message and exit
(env)$ python python-event-crawler 201605
<ul>
<li>4月1日(金) <a href="http://kabepy.connpass.com/event/29112/">Python ボルダリング部 #77</a> (東京都)</li>
<li>4月1日(金) <a href="http://pyky.connpass.com/event/28654/">Kivyドキュメント翻訳レビュー会01</a> (東京都)</li>
<li>4月2日(土) <a href="http://bitdonation.connpass.com/event/29646/">django x bitcoin もくもく会</a> (東京都)</li>
<li>4月2日(土) <a href="http://djangogirls-org.connpass.com/event/28561/">Pythonの基礎を学ぼう！ #3</a> (東京都)</li>
:
<li>4月26日(火) <a href="http://pymook.connpass.com/event/29274/">「Pythonエンジニア養成読本」読書会 07</a> (東京都)</li>
<li>4月30日(土) <a href="https://coedo-rails.doorkeeper.jp/events/41526">『Ruby on Rails チュートリアル』解説セミナー Railsパスポート優先受付 / GW集中セミナー</a> (東京都)</li>
</ul>
```
