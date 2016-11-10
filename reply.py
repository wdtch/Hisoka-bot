#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import re
import random
from time import sleep

import fortune
import poker
import mytwitterlib


class AutoReply(object):

    def __init__(self):
        self.twitterlib = mytwitterlib.MyTwitterLib(os.getenv("CK"),
                                                    os.getenv("CS"),
                                                    os.getenv("AT"),
                                                    os.getenv("AS"))

    def handle_mention(self):
        """メンションを解析し、自動リプライを実行"""
        mentions = self.twitterlib.get_mentions(50)

        if mentions is None:
            print("Failed to get mentions.")
        elif mentions == []:
            print("No mentions gotten.")
        else:
            for mention in mentions:
                self._reply(mention)

    def _reply(self, mention):
        """受け取ったメンションの内容に応じて自動的にリプライを送信する"""

        # 以下のre.search()は部分一致
        # 第一引数に書いた文字列がツイートに含まれれば、内容に応じたreply_textを構築してリプライで返す

        # おはようを返す
        if re.search(r"おはよう", mention.text):
            with open("morning.txt") as f:
                tweets = list(f.readlines())
            reply_text = random.choice(tweets)

            status_code = self.twitterlib.reply(mention, reply_text)
            self._handle_status(status_code, "Ohayo")

        # おやすみもおはようと同様
        elif re.search(r"おやすみ", mention.text):
            with open("night.txt") as f:
                tweets = list(f.readlines())
            reply_text = random.choice(tweets)

            status_code = self.twitterlib.reply(mention, reply_text)
            self._handle_status(status_code, "Oyasumi")

        # 「占って」というリプライに対して占いを実行し、結果をリプライで返す
        elif re.search(r"占って|うらなって", mention.text):
            reply_text = self._fortune(mention)
            status_code = self.twitterlib.reply(mention, reply_text)
            self._handle_status(status_code, "Fortune")

        # 「ポーカー」というリプライに対してポーカーを実行
        elif re.search(r"ポーカー", mention.text):
            pt = poker.PokerThread(self, mention)
            pt.start()
        else:
            # ヒットしなければリプライを送らない
            pass

    def _fortune(self, mention):
        """占いを実行し、結果を表す文を返す"""
        faf = fortune.FourAceFortune()
        result = faf.fortune()

        if result == 0:
            reply_text = "占いの結果は…すごくラッキーみたいだよ♥"
        elif result == 1:
            reply_text = "占いの結果は…今日はラッキーな日みたいだね♦"
        elif result == 2:
            reply_text = "占いの結果は…今日はまあまあってとこかな♣"
        elif result == 3:
            reply_text = "占いの結果は…あんまりよくないね♠今日はちょっと気をつけたほうがいいかもね…♠"
        elif result == 4:
            reply_text = "占いでエラーが発生しました。"

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
        first_reply = "キミの最初の手札は\n" + \
            first + "\n" + "だよ♦交換したい手札の番号をリプライで送ってね♦"
        status_code = self.twitterlib.reply(mention, first_reply)
        self._handle_status(status_code, "Poker")

        # 5分間30秒ごとにメンションをチェック
        for _ in range(10):
            mentions = self.twitterlib.get_mentions(10, record=False)
            # 各ツイートの本文を表示、内容を解析
            # 手札交換のフォーマットに則ったメンションがあれば交換を実行
            first_user_id = mention.user_id
            for got_mention in mentions:
                # ポーカーを要求した人と同一人物からのメンションを探す
                if got_mention.user_id == first_user_id and re.search(r"[0-6]", got_mention.text):
                    return poker_player.change_and_judge(list(map(int, poker.get_changenum(got_mention.text))))

            sleep(30)

        return poker_player.change_and_judge([])

    def _handle_status(self, code, kind):
        """ステータスコードを受け取って、コードに応じたログを出力する"""
        if code == 200:
            print("Succeeded: {}.".format(kind))
        else:
            print("Error: Status code {} at {}".format(code, kind))


if __name__ == '__main__':
    # 単体実行時にリプライを取得、自動返信
    ar = AutoReply()
    ar.handle_mention()