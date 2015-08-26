#!/usr/bin/python
# -*- coding: utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler
import random
import logging
import auth

# class RegularTweet(object):
# """30分おきにランダムの定期ツイートを行うためのクラス"""

b_scheduler = BlockingScheduler()

# def __init__(self):
oauth = auth.Auth()

@b_scheduler.scheduled_job("interval", minutes=30)
def regular_tweet():
    f = open("random_tweet.txt")
    tweets = f.readlines()
    tweet = random.choice(tweets)
    params = {"status": tweet}

    # OAuth認証でPOST methodを用いてツイートを投稿
    tweet_url = "https://api.twitter.com/1.1/statuses/update.json"
    req = oauth.twitter.post(tweet_url, params=params)

    # レスポンスを確認
    if req.status_code == 200:
        logging.info("Tweet Succeeded.")
    else:
        logging.error("Status Code %d" % req.status_code)

# def start(self):
#     self.b_schedular.start()

if __name__ == '__main__':
    # reg = RegularTweet()
    # reg.start()
    b_scheduler.start()