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
import mytwitterlib


mention_url = "https://api.twitter.com/1.1/statuses/mentions_timeline.json"
tweet_url = "https://api.twitter.com/1.1/statuses/update.json"


class AutoReply(object):

    def __init__(self):
        # self.logger = logging.getLogger(__name__)
        # self.logger.setLevel(logging.INFO)
        self.twitterlib = mytwitterlib.MyTwitterLib(
            auth.CK, auth.CS, auth.AT, auth.AS)

    def handle_mention(self):
        mentions = self.twitterlib.get_mentions(50)

        if mentions is None:
            print("Error code {}: Failed to get mentions.".format(req.status_code))
        elif mentions == []:
            print("No mentions gotten.")
        else:
            for mention in mentions:
                self._reply(mention)

    def _reply(self, mention):
        # 以下のre.search()は部分一致
        # 第一引数に書いた文字列がツイートに含まれれば、内容に応じたreply_textを構築してリプライで返す
        # いずれは反応語句とそれに対するリプライを対にした辞書かなんかをまとめたファイルを使いたい
        if re.search(r"おはよう", mention.text):
            # おはようを返す
            reply_text = "おはよう"
            self.twitterlib.reply(mention, reply_text)

        # おやすみもおはようと同様
        elif re.search(r"おやすみ", mention.text):
            reply_text = "おやすみ"
            self.twitterlib.reply(mention, reply_text)

        # 「占って」というリプライに対して占いを実行し、結果をリプライで返す
        elif re.search(r"占って", mention.text):
            reply_text = self._fortune(mention)
            self.twitterlib.reply(mention, reply_text)

        # 「ポーカー」というリプライに対してポーカーを実行
        elif re.search(r"ポーカー", mention.text):
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
                self.twitterlib.reply(mention, reply_text)

        else:
            # ヒットしなければリプライを送らない
            pass

    def _fortune(self, mention):
        faf = fortune.FourAceFortune()
        result = faf.fortune()

        if result == 0:
            reply_text = "you are very lucky!!!"
        elif result == 1:
            reply_text = "you are lucky!"
        elif result == 2:
            reply_text = "you are not lucky or unlucky."
        elif result == 3:
            reply_text = "Perhaps you are unlucky..."
        elif result == 4:
            reply_text = "Something wrong."

        return reply_text

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
        first_reply = "最初の手札は\n" + \
            first + "\n" + "です。"
        self.twitterlib.reply(mention, first_reply)

        # 1分後にメンションをチェック
        print("Waiting for deciding the card to change...")
        sleep(60)

        mentions = self.twitterlib.get_mentions(10)

        result = None

        # 各ツイートの本文を表示、内容を解析
        # 手札交換のフォーマットに則ったメンションがあれば交換を実行
        first_user_id = mention.user_id
        for got_mention in mentions:
            # ポーカーを要求した人と同一人物からのメンションを探す
            if got_mention.user_id == first_user_id:
                # "@[user_id] number"という形式のリプライを空白で区切って前を捨てる
                reply_text = got_mention.text.split()[1]
                # フォーマット(1〜5の数字が5文字以下)に合うかチェック
                if re.match(r"^[0-5]{1,5}$", reply_text):
                    # reply_textには、"13"のように交換したい手札の番号が連続して書かれている
                    # list(reply_text)で、"13"から["1", "3"]という1文字ずつのリストを作る
                    # map(int, ...)で、リストの各要素をint型に変換
                    # *list(...)で、int型の数字をばらしてポーカー関数に渡す
                    result = poker_player.change_and_judge(
                        *list(map(int, list(reply_text))))
                    break

        else:
            # リプライを読み込めなかった場合
            print(
                "Error code {}: Failed to get mentions.".format(req.status_code))

        return result


# @b_scheduler.scheduled_job("interval", minutes=1)
# def run():
#     ar.handle_mention()

if __name__ == '__main__':
    # 単体実行時にリプライを取得、自動返信
    # b_scheduler = BlockingScheduler()
    ar = AutoReply()
    ar.handle_mention()
