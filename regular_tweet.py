#!/usr/bin/python
# -*- coding: utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler
import random
import auth

b_scheduler = BlockingScheduler()

@b_scheduler.scheduled_job("interval", minutes=1)
def regular_tweet():
    f = open("random_tweet.txt")
    tweets = f.readlines()
    tweet = random.choice(tweets)
    params = {"status": tweet}

    # OAuth認証でPOST methodを用いてツイートを投稿
    tweet_url = "https://api.twitter.com/1.1/statuses/update.json"
    req = auth.twitter.post(tweet_url, params=params)

    # レスポンスを確認
    if req.status_code == 200:
        print("Tweet Succeeded.")
    else:
        print("Error: Status Code %d" % req.status_code)

if __name__ == '__main__':
    b_scheduler.start()