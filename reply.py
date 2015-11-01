#!/usr/bin/python
# -*- coding: utf-8 -*-

#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from requests_oauthlib import OAuth1Session
import json
import re
import logging
from time import sleep
from apscheduler.schedulers.blocking import BlockingScheduler
import auth
import card
import fortune
import poker
# import mytwitterlib


mention_url = "https://api.twitter.com/1.1/statuses/mentions_timeline.json"
tweet_url = "https://api.twitter.com/1.1/statuses/update.json"


class AutoReply(object):

    def __init__(self):
        # self.logger = logging.getLogger(__name__)
        # self.logger.setLevel(logging.INFO)
        # self.twitterlib = mytwitterlib.MyTwitterLib(
            # auth.CK, auth.CS, auth.AT, auth.AS)
        pass

    def handle_mention(self):
        # ファイルをopenしてsince_idを読み込む
        # ファイルが存在しなかったとき(初めてプログラムが起動されたとき)は
        # 例外が送出されるので、since_idに空文字列をセット
        try:
            f = open("since_id.txt", "r")
            since_id = f.readline()
            f.close()
        except IOError:
            print("since_id.txt does not exist.")
            # exit(1)
            since_id = ""

        # 最新50ツイートを読み込む
        if since_id == "":
            params = {"count": 50}
        else:
            params = {"count": 50, "since_id": since_id}

        # OAuth で GET
        req = auth.twitter.get(mention_url, params=params)

        if req.status_code == 200:
            # レスポンスはJSON形式なので parse する
            mentions = json.loads(req.text)

            # 最新ツイートの本文を表示、内容に応じてリプライを返す
            # 最新のツイートについてはそのIDを保存するのでループから分離
            if not mentions == []:
                latest_mention = mentions[0]
                print("Got: {}".format(latest_mention["text"]))

                since_id = latest_mention["id_str"]  # 最新のリプライのIDを記録
                try:
                    f = open("since_id.txt", "w")
                    f.write(since_id)
                    f.close()
                except IOError:
                    print("Failed to write since_id.")

                self._reply(latest_mention)  # 取得したリプライに対して自動返信

            else:
                print("No mentions gotten.")

            # 最新の次以降の各ツイートの本文を表示、内容に応じてリプライを返す
            for mention in mentions[1:]:
                print("Got: {}".format(mention["text"]))
                self._reply(mention)  # 取得したリプライに対して自動返信

        else:
            # リプライを読み込めなかった場合
            print(
                "Failed to get mentions. Error code: {}".format(req.status_code))

    def _reply(self, mention):
        # 以下のre.search()は部分一致
        # 第一引数に書いた文字列がツイートに含まれれば、内容に応じたreply_textを構築してリプライで返す
        # いずれは反応語句とそれに対するリプライを対にした辞書かなんかをまとめたファイルを使いたい
        if re.search(r"おはよう", mention["text"]):
            # おはようを返す
            reply_text = "@" + mention["user"]["screen_name"] + " おはよう"
            params = {
                "status": reply_text, "in_reply_to_status_id": mention["id_str"]}

        # おやすみもおはようと同様
        elif re.search(r"おやすみ", mention["text"]):
            reply_text = "@" + mention["user"]["screen_name"] + " おやすみ"
            params = {
                "status": reply_text, "in_reply_to_status_id": mention["id_str"]}

        # 「占って」というリプライに対して占いを実行し、結果をリプライで返す
        elif re.search(r"占って", mention["text"]):
            params = self._fortune(mention)

        # 「ポーカー」というリプライに対してポーカーを実行
        elif re.search(r"ポーカー", mention["text"]):
            # 勝ったプレイヤーを表す文字列が返ってくる
            print("play poker.")
            result = self._play_poker(mention)
            print("result: {}".format(result))
            if result is not None:
                if result[0] == "player":
                    reply_text = "\n" + "you: " + result[1] + "\n" + \
                        "hisoka: " + result[2] + "\n" + "You win!"
                elif result[0] == "hisoka":
                    reply_text = "\n" + "you: " + result[1] + "\n" + \
                        "hisoka: " + result[2] + "\n" + "You lose!"
                elif result[0] == "draw":
                    reply_text = "\n" + "you: " + result[1] + "\n" + \
                        "hisoka: " + result[2] + "\n" + "Draw!"
                else:
                    reply_text = "something wrong."
                params = {
                    "status": "@" + mention["user"]["screen_name"] + reply_text, "in_reply_to_status_id": mention["id_str"]}
            else:
                params = None

        else:
            # ヒットしなければパラメータを表す変数をNoneにしてツイート動作を行わない
            params = None

        self._post_tweet(params)

    def _post_tweet(self, params):
        # OAuth認証でPOST methodを用いてツイートを投稿
        if params is not None:
            req = auth.twitter.post(tweet_url, params=params)

            if req.status_code == 200:
                print("Reply Succeeded.")
            else:
                print(
                    "Reply Failed - Status Code {0}".format(req.status_code))

    def _fortune(self, mention):
        faf = fortune.FourAceFortune()
        result = faf.fortune()

        if result == 0:
            reply_text = "@" + \
                mention["user"]["screen_name"] + " you are very lucky!!!"
        elif result == 1:
            reply_text = "@" + \
                mention["user"]["screen_name"] + " you are lucky!"
        elif result == 2:
            reply_text = "@" + \
                mention["user"]["screen_name"] + \
                " you are not lucky or unlucky."
        elif result == 3:
            reply_text = "@" + \
                mention["user"]["screen_name"] + " Perhaps you are unlucky..."
        elif result == 4:
            reply_text = "@" + \
                mention["user"]["screen_name"] + " Something wrong."
        params = {
            "status": reply_text, "in_reply_to_status_id": mention["id_str"]}

        return params

    def _play_poker(self, mention):
        """ポーカーの開始を要求するメンションを受け取り、ポーカーを行う
           リプライの宛先やパラメータを構成するのに引数のmentionを用いる
           最初の手札をリプライで送信し、n分後にメンションを読み込む
           ポーカーを要求したアカウントと同じものがあれば、手札の交換フォーマットに
           沿った形式かどうかをチェックし、合っていればその数字に応じて手札を交換
           沿っていなければ無視する
           交換後の手札を用いてポーカーを行い、勝敗を記したテキストを含むパラメータを返す"""
        poker_player = poker.Poker()

        # 最初の手札を送信
        first = poker_player.first_hand_str()
        first_reply = "@" + \
            mention["user"]["screen_name"] + " 最初の手札は\n" + \
            first + "\n" + "です。"
        params = {
            "status": first_reply, "in_reply_to_status_id": mention["id_str"]}
        self._post_tweet(params)

        # 1分後にメンションをチェック
        print("Waiting...")
        sleep(60)
        # since_idを取得
        try:
            print("since_id found.")
            f = open("since_id.txt", "r")
            since_id = f.readline()
            f.close()
        except IOError:  # 発生しないはず
            print("Poker: since_id.txt does not exist.")
            # exit(1)
            since_id = ""

        # 最新10ツイートを読み込む
        if since_id == "":
            params = {"count": 10}
        else:
            params = {"count": 10, "since_id": since_id}

        # OAuthでGET
        req = auth.twitter.get(mention_url, params=params)

        result = None
        if req.status_code == 200:
            # レスポンスはJSON形式なので parse する
            mentions = json.loads(req.text)

            # 各ツイートの本文を表示、内容を解析
            # 手札交換のフォーマットに則ったメンションがあれば交換を実行
            user_id = mention["user"]["screen_name"]
            for got_mention in mentions:
                # ポーカーを要求した人と同一人物からのメンションを探す
                if got_mention["user"]["screen_name"] == user_id:
                    # "@[user_id] number"という形式のリプライを空白で区切って前を捨てる
                    reply_text = got_mention["text"].split()[1]
                    # フォーマット(1〜5の数字が5文字以下)に合うかチェック
                    if re.match(r"^[0-5]{1,5}$", reply_text):
                        result = poker_player.change_and_judge(
                            *list(map(int, list(reply_text))))
                        break

        else:
            # リプライを読み込めなかった場合
            print(
                "Failed to get mentions. Error code: {}".format(req.status_code))

        return result


# @b_scheduler.scheduled_job("interval", minutes=1)
# def run():
#     ar.handle_mention()

if __name__ == '__main__':
    # 単体実行時にリプライを取得、自動返信
    # b_scheduler = BlockingScheduler()
    ar = AutoReply()
    ar.handle_mention()
