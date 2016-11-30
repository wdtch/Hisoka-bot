#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading

from apscheduler.schedulers.blocking import BlockingScheduler

import followback
import regular_tweet
import reply

b_scheduler = BlockingScheduler()
reg_man = regular_tweet.RegularTweet()
reply_man = reply.AutoReply()

def run_followback():
    followback.followback()

def run_reply():
    reply_man.handle_mention()

def run_regular_tweet():
    reg_man.regular_tweet()

def check_threadnum():
    print("{} threads are active.".format(threading.active_count()))

if __name__ == '__main__':
    b_scheduler.add_job(run_reply, "interval", id="run_reply", seconds=60)
    b_scheduler.add_job(check_threadnum, "interval", id="check_threadnum", seconds=90)
    b_scheduler.add_job(run_regular_tweet, "interval", id="run_regular_tweet", minutes=30)
    b_scheduler.add_job(run_followback, "interval", id="run_followback", minutes=5)
    b_scheduler.start()