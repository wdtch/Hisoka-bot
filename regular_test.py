#!/usr/bin/python
# -*- coding: utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler
b_scheduler = BlockingScheduler()

# 30分ごとに動かしたい(とりあえず確認しやすいように3分ごと)
@b_scheduler.scheled_job("interval", minutes=3)
def thirty_minutes_job():
    print("This job works every 3 minutes.")

b_scheduler.start()