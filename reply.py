#!/usr/bin/python
# -*- coding: utf-8 -*-

#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from requests_oauthlib import OAuth1Session
import json
import re
from apscheduler.schedulers.blocking import BlockingScheduler
import auth


class AutoReply(object):

    def __init__(self):
        self.since_id = ""

    def get_reply(self):
        reply_url = "https://api.twitter.com/1.1/statuses/mentions_timeline.json"
        # 最新50ツイートを読み込む
        if self.since_id == "":
            params = {"count": 50}
        else:
            params = {"count": 50, "since_id": self.since_id}

        # OAuth で GET
        req = auth.twitter.get(reply_url, params=params)

        if req.status_code == 200:
            # レスポンスはJSON形式なので parse する
            mentions = json.loads(req.text)

            # 最新ツイートの本文を表示、内容に応じてリプライを返す
            # 最新のツイートについてはそのIDを保存するのでループから分離
            if not mentions == []:
                latest_reply = mentions[0]
                print("Got: {}".format(latest_reply["text"]))
                self.since_id = latest_reply["id_str"]  # 最新のリプライのIDをセット
                self._post_reply(latest_reply)  # 取得したリプライに対して自動返信

            else:
                print("No reply gotten.")

            # 最新の次以降の各ツイートの本文を表示、内容に応じてリプライを返す
            for reply in mentions[1:]:
                print("Got: {}".format(reply["text"]))
                self._post_reply(reply)  # 取得したリプライに対して自動返信

        else:
            # エラーの場合
            print("Error: %d" % req.status_code)

    def _post_reply(self, tweet):
        tweet_url = "https://api.twitter.com/1.1/statuses/update.json"

        # 以下のre.search()は部分一致
        # 第一引数に書いた文字列がツイートに含まれれば、内容に応じたreply_textを構築してリプライで返す
        # いずれは反応語句とそれに対するリプライを対にした辞書かなんかをまとめたファイルを使いたい
        # 暫定的におはようとおやすみをベタ書きしてそれらに反応するようにする
        if re.search(r"おはよう", tweet["text"]):
            # おはようを返す
            reply_text = "@" + tweet["user"]["screen_name"] + " おはよう"
            params = {
                "status": reply_text, "in_reply_to_status_id": tweet["id_str"]}
        elif re.search(r"おやすみ", tweet["text"]):
            reply_text = "@" + tweet["user"]["screen_name"] + " おやすみ"
            params = {
                "status": reply_text, "in_reply_to_status_id": tweet["id_str"]}
        else:
            # ヒットしなければパラメータを表す変数をNoneにしてツイート動作を行わない
            params = None

        # OAuth認証でPOST methodを用いてツイートを投稿
        if params is not None:
            req = auth.twitter.post(tweet_url, params=params)

            if req.status_code == 200:
                print("Reply Succeeded.")
            else:
                print("Reply Failed - Status Code {0}".format(req.status_code))

# 単体実行時に1分毎にリプライを取得、自動返信
b_scheduler = BlockingScheduler()
ar = AutoReply()


@b_scheduler.scheduled_job("interval", minutes=1)
def run():
    ar.get_reply()

if __name__ == '__main__':
    b_scheduler.start()
