#!/usr/bin/python
# -*- coding: utf-8 -*-

#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from requests_oauthlib import OAuth1Session
import json
import re
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
import auth
import card


class AutoReply(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def get_reply(self):
        reply_url = "https://api.twitter.com/1.1/statuses/mentions_timeline.json"

        # ファイルをopenしてsince_idを読み込む
        # ファイルが存在しなかったとき(初めてプログラムが起動されたとき)は
        # 例外が送出されるので、since_idに空文字列をセット
        try:
            f = open("since_id.txt", "r")
            since_id = f.readline()
            f.close()
        except IOError:
            self.logger.error("since_id.txt does not exist.")
            # exit(1)
            since_id = ""

        # 最新50ツイートを読み込む
        if since_id == "":
            params = {"count": 50}
        else:
            params = {"count": 50, "since_id": since_id}

        # OAuth で GET
        req = auth.twitter.get(reply_url, params=params)

        if req.status_code == 200:
            # レスポンスはJSON形式なので parse する
            mentions = json.loads(req.text)

            # 最新ツイートの本文を表示、内容に応じてリプライを返す
            # 最新のツイートについてはそのIDを保存するのでループから分離
            if not mentions == []:
                latest_reply = mentions[0]
                self.logger.info("Got: {}".format(latest_reply["text"]))

                since_id = latest_reply["id_str"]  # 最新のリプライのIDを記録
                try:
                    f = open("since_id.txt", "w")
                    f.write(since_id)
                    f.close()
                except IOError:
                    self.logger.error("Failed to write since_id.")

                self._post_reply(latest_reply)  # 取得したリプライに対して自動返信

            else:
                self.logger.info("No reply gotten.")

            # 最新の次以降の各ツイートの本文を表示、内容に応じてリプライを返す
            for reply in mentions[1:]:
                self.logger.info("Got: {}".format(reply["text"]))
                self._post_reply(reply)  # 取得したリプライに対して自動返信

        else:
            # リプライを読み込めなかった場合
            self.logger.error("Error: {}".format(req.status_code))

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

        # おやすみもおはようと同様
        elif re.search(r"おやすみ", tweet["text"]):
            reply_text = "@" + tweet["user"]["screen_name"] + " おやすみ"
            params = {
                "status": reply_text, "in_reply_to_status_id": tweet["id_str"]}

        # 「占って」というリプライに対して占いを実行し、結果をリプライで返す
        elif re.search(r"占って", tweet["text"]):
            params = self.do_fortune()

        # 「ポーカー」というリプライに対してポーカーを実行
        elif re.search(r"ポーカー", tweet["text"]):
            params = self.do_poker(tweet["user"]["screen_name"])

        else:
            # ヒットしなければパラメータを表す変数をNoneにしてツイート動作を行わない
            params = None

        # OAuth認証でPOST methodを用いてツイートを投稿
        if params is not None:
            req = auth.twitter.post(tweet_url, params=params)

            if req.status_code == 200:
                self.logger.info("Reply Succeeded.")
            else:
                self.logger.error(
                    "Reply Failed - Status Code {0}".format(req.status_code))

    def do_fortune(self):
        faf = card.FourAceFortune()
        result = faf.fortune()

        if result == 0:
            reply_text += "@" + \
                tweet["user"]["screen_name"] + "you are very lucky!!!"
        elif result == 1:
            reply_text += "@" + tweet["user"]["screen_name"] + "you are lucky!"
        elif result == 2:
            reply_text += "@" + \
                tweet["user"]["screen_name"] + "you are not lucky or unlucky."
        elif result == 3:
            reply_text += "@" + \
                tweet["user"]["screen_name"] + "Perhaps you are unlucky..."
        elif result == 4:
            reply_text += "@" + \
                tweet["user"]["screen_name"] + "Something wrong."
        params = {
            "status": reply_text, "in_reply_to_status_id": tweet["id_str"]}

        return params

    def do_poker(self, player_id):
        # ポーカーを行うためのクラスインスタンスを生成(同時に最初の手札も生成)
        p = card.Poker()
        # プレイヤー側の最初の手札を文字列で取得
        player_hand = p.first_hand()

        # 最初の手札と、交換の有無を確認するリプライを送信


# 単体実行時に1分毎にリプライを取得、自動返信
b_scheduler = BlockingScheduler()
ar = AutoReply()


# @b_scheduler.scheduled_job("interval", minutes=1)
# def run():
#     ar.get_reply()

if __name__ == '__main__':
    # b_scheduler.add_job(run, "interval", minutes=1)
    # b_scheduler.start()
    ar.get_reply()
