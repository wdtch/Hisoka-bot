#!/usr/bin/python
# -*- coding: utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler
import regular_tweet
import reply

b_scheduler = BlockingScheduler()
reg_man = regular_tweet.RegularTweet()
reply_man = reply.AutoReply()

@b_scheduler.scheduled_job("interval", minutes=30)
def run_regular_tweet():
    reg_man.regular_tweet()

@b_scheduler.scheduled_job("interval", minutes=1)
def run_reply():
    reply_man.get_reply()

if __name__ == '__main__':
    b_scheduler.start()