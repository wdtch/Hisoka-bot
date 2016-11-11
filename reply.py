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
            _handle_status(status_code, "Ohayo")

        # おやすみもおはようと同様
        elif re.search(r"おやすみ", mention.text):
            with open("night.txt") as f:
                tweets = list(f.readlines())
            reply_text = random.choice(tweets)

            status_code = self.twitterlib.reply(mention, reply_text)
            _handle_status(status_code, "Oyasumi")

        # 「占って」というリプライに対して占いを実行し、結果をリプライで返す
        elif re.search(r"占って|うらなって", mention.text):
            reply_text = fortune._fortune()
            status_code = self.twitterlib.reply(mention, reply_text)
            _handle_status(status_code, "Fortune")

        # 「ポーカー」というリプライに対してポーカーを実行
        elif re.search(r"ポーカー", mention.text):
            pt = poker.PokerThread(self.twitterlib, mention)
            pt.start()
        else:
            # ヒットしなければリプライを送らない
            pass


def _handle_status(code, kind):
    """ステータスコードを受け取って、コードに応じたログを出力する"""
    if code == 200:
        print("Succeeded: {}.".format(kind))
    else:
        print("Error: Status code {} at {}".format(code, kind))


if __name__ == '__main__':
    # 単体実行時にリプライを取得、自動返信
    ar = AutoReply()
    ar.handle_mention()