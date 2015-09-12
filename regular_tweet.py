#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from apscheduler.schedulers.blocking import BlockingScheduler
import random
import auth


class RegularTweet(object):

    def __init__(self):
        self._f = open("random_tweet.txt")
        self.tweets = list(self._f.readlines())

    # 30分毎に定期ツイート
    # @b_scheduler.scheduled_job("interval", minutes=30)
    def regular_tweet(self):
        tweet = random.choice(self.tweets)
        print("Tweet: {0}".format(tweet))
        params = {"status": tweet}

        # OAuth認証でPOST methodを用いてツイートを投稿
        tweet_url = "https://api.twitter.com/1.1/statuses/update.json"
        req = auth.twitter.post(tweet_url, params=params)

        # レスポンスを確認
        if req.status_code == 200:
            print("Tweet Succeeded.")
        elif req.status_code == 403: # 重複したとき
            self.tweet_again() # リトライ
        else:
            print("Error: Status Code {0}".format(req.status_code))

    # ツイートが失敗した時のリトライ用メソッド
    def tweet_again(self):
        tweet = random.choice(self.tweets)
        params = {"status": tweet}

        # OAuth認証でPOST methodを用いてツイートを投稿
        tweet_url = "https://api.twitter.com/1.1/statuses/update.json"
        req = auth.twitter.post(tweet_url, params=params)

        # レスポンスを確認
        if req.status_code == 200:
            print("Retry - Tweet Succeeded.")
        else:
            print("Retry Failed - Status Code {0}".format(req.status_code))

# 単体実行時に30分毎に定期ツイートを実行
b_scheduler = BlockingScheduler()
reg = RegularTweet()

@b_scheduler.scheduled_job("interval", minutes=1)
def run():
    reg.regular_tweet()

if __name__ == '__main__':
    b_scheduler.start()