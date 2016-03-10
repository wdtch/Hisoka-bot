#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from apscheduler.schedulers.blocking import BlockingScheduler
import os
import random

import mytwitterlib


class RegularTweet(object):

    def __init__(self):
        with open("random_tweet.txt") as _f:
            self.tweets = list(_f.readlines())
        self.twitterlib = mytwitterlib.MyTwitterLib(os.getenv("CK"),
                                                    os.getenv("CS"),
                                                    os.getenv("AT"),
                                                    os.getenv("AS"))

    def regular_tweet(self):
        tweet = random.choice(self.tweets)
        # print("Tweet: {0}".format(tweet))
        status = self.twitterlib.tweet(tweet)

        # レスポンスを確認
        if status == 200:
            print("Regular Tweet Succeeded.")
        elif status == 403: # 重複したとき
            self.tweet_again() # リトライ
        else:
            print("Failed to tweet. Status code: {}".format(status))

    # ツイートが失敗した時のリトライ用メソッド
    def tweet_again(self):
        tweet = random.choice(self.tweets)
        status = self.twitterlib.tweet(tweet)

        # レスポンスを確認
        if status == 200:
            print("Retry - Regular Tweet Succeeded.")
        else:
            print("Retry Failed. Status Code: {}".format(status))

# 単体実行時に1分毎に定期ツイートを実行
b_scheduler = BlockingScheduler()
reg = RegularTweet()

@b_scheduler.scheduled_job("interval", minutes=1)
def run():
    reg.regular_tweet()

if __name__ == '__main__':
    b_scheduler.start()