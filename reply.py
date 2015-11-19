#!/usr/bin/python
# -*- coding: utf-8 -*-

#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import re
import random
from time import sleep
import auth
import fortune
import poker
import mytwitterlib


class AutoReply(object):

    def __init__(self):
        self.twitterlib = mytwitterlib.MyTwitterLib(
            auth.CK, auth.CS, auth.AT, auth.AS)

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
            self._handle_status(status_code)

        # おやすみもおはようと同様
        elif re.search(r"おやすみ", mention.text):
            with open("night.txt") as f:
                tweets = list(f.readlines())
            reply_text = random.choice(tweets)

            status_code = self.twitterlib.reply(mention, reply_text)
            self._handle_status(status_code)

        # 「占って」というリプライに対して占いを実行し、結果をリプライで返す
        elif re.search(r"占って|うらなって", mention.text):
            reply_text = self._fortune(mention)
            status_code = self.twitterlib.reply(mention, reply_text)
            self._handle_status(status_code)

        # 「ポーカー」というリプライに対してポーカーを実行
        elif re.search(r"ポーカー", mention.text):
            # 勝ったプレイヤーを表す文字列が返ってくる
            result = self._play_poker(mention)

            if result is not None:
                if result[0] == "player":
                    reply_text = "\n" + "キミの手札は\n" + result[1] + "\nで、" + \
                        "ボクの手札は\n" + result[2] + "\n" + "だから…キミの勝ち、だね♠"
                elif result[0] == "hisoka":
                    reply_text = "\n" + "キミの手札は\n" + result[1] + "\nで、" + \
                        "ボクの手札は" + result[2] + "\n" + "だから…ボクの勝ち、だね♥"
                elif result[0] == "draw":
                    reply_text = "\n" + "キミの手札は\n" + result[1] + "\nで、" + \
                        "ボクの手札は" + result[2] + "\n" + "だから…引き分け、だね♦"
                else:
                    reply_text = "ポーカーでエラーが発生しました。"
                status_code = self.twitterlib.reply(mention, reply_text)
                self._handle_status(status_code)

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
            first + "\n" + "だよ♦交換したい手札の数字をリプライで送ってね♦"
        status_code = self.twitterlib.reply(mention, first_reply)
        self._handle_status(status_code)

        # 1分半後にメンションをチェック
        sleep(90)

        mentions = self.twitterlib.get_mentions(10)

        result = None

        # 各ツイートの本文を表示、内容を解析
        # 手札交換のフォーマットに則ったメンションがあれば交換を実行
        first_user_id = mention.user_id
        for got_mention in mentions:
            # ポーカーを要求した人と同一人物からのメンションを探す
            if got_mention.user_id == first_user_id:
                # "@[user_id] number"という形式のリプライを空白で区切って前を捨てる
                cards_to_change = got_mention.text.split()[1]
                # フォーマット(1〜5の数字が5文字以下)に合うかチェック
                if re.match(r"^[0-5]{1,5}$", cards_to_change):
                    # cards_to_changeには、"13"のように交換したい手札の番号が連続して書かれている
                    # list(cards_to_change)で、"13"から["1", "3"]という1文字ずつのリストを作る
                    # map(int, ...)で、リストの各要素をint型に変換
                    # *list(...)で、int型の数字をばらしてポーカー関数に渡す
                    result = poker_player.change_and_judge(
                        *list(map(int, list(cards_to_change))))
                    break

        return result

    def _handle_status(self, code):
        """ステータスコードを受け取って、コードに応じたログを出力する"""
        if code == 200:
            print("Succeeded.")
        else:
            print("Error: Status code {}".format(code))


if __name__ == '__main__':
    # 単体実行時にリプライを取得、自動返信
    ar = AutoReply()
    ar.handle_mention()