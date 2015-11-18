#!/usr/bin/python
# -*- coding: utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler
import regular_tweet
import reply

b_scheduler = BlockingScheduler()
reg_man = regular_tweet.RegularTweet()
reply_man = reply.AutoReply()

def run_reply():
    reply_man.handle_mention()

def run_regular_tweet():
    reg_man.regular_tweet()

if __name__ == '__main__':
    b_scheduler.add_job(run_reply, "interval", id="run_reply", seconds=90)
    b_scheduler.add_job(run_regular_tweet, "interval", id="run_regular_tweet", minutes=30)
    b_scheduler.start()