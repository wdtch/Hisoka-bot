#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from apscheduler.schedulers.blocking import BlockingScheduler
import random
import auth

b_scheduler = BlockingScheduler()
f = open("random_tweet.txt")
tweets = f.readlines().copy()

# 30分毎に定期ツイート
@b_scheduler.scheduled_job("interval", minutes=1)
def regular_tweet():
    tweet = random.choice(tweets)
    params = {"status": tweet}

    # OAuth認証でPOST methodを用いてツイートを投稿
    tweet_url = "https://api.twitter.com/1.1/statuses/update.json"
    req = auth.twitter.post(tweet_url, params=params)

    # レスポンスを確認
    if req.status_code == 200:
        print("Tweet Succeeded.")
    elif req.status_code == 403: # 重複？したとき
        tweet_again() # リトライ
    else:
        print("Error: Status Code {0}".format(req.status_code))

def tweet_again():
    tweet = random.choice(tweets)
    params = {"status": tweet}

    # OAuth認証でPOST methodを用いてツイートを投稿
    tweet_url = "https://api.twitter.com/1.1/statuses/update.json"
    req = auth.twitter.post(tweet_url, params=params)

    # レスポンスを確認
    if req.status_code == 200:
        print("Tweet Succeeded.")
    else:
        print("Error: Status Code {0}".format(req.status_code))

if __name__ == '__main__':
    b_scheduler.start()