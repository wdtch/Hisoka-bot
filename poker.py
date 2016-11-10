#!/usr/bin/python
# -*- coding: utf-8 -*-

from enum import IntEnum
import operator
import threading

from card import *


class Hands(IntEnum):

    """ポーカーの役を基本点に関連付けた列挙型"""
    high_cards = 0
    one_pair = 100
    two_pair = 200
    three_of_a_kind = 300
    straight = 400
    flush = 500
    fullhouse = 600
    four_of_a_kind = 700
    straight_flush = 800
    royal_straight_flush = 900


class Judge(object):

    """ポーカーの役判定に関する関数を集めた判定オブジェクト"""

    def __init__(self):
        self.strongest = 0

    def judge(self, hand):
        """受け取った手札の役を判定し、役に応じた点数を返す関数"""
        # 手札の役を判定
        # IntEnumの値 + (役の数字)を返す

        hand_sorted = sorted(hand, key=operator.attrgetter("rank"))

        # 強い役から順に判定していく
        self.strongest = hand_sorted[len(hand_sorted) - 1].rank

        # ロイヤルストレートフラッシュ
        if self._is_royal_straight_flush(hand_sorted):
            return Hands.royal_straight_flush
        # ストレートフラッシュ
        elif self._is_flush(hand_sorted) and self._is_straight(hand_sorted):
            return Hands.straight_flush + self.strongest
        # フォーカード
        elif self._is_four_of_a_kind(hand_sorted):
            return Hands.four_of_a_kind + self.strongest
        # フルハウス
        elif self._is_fullhouse(hand_sorted):
            return Hands.fullhouse + self.strongest
        # フラッシュ
        elif self._is_flush(hand_sorted):
            return Hands.flush + self.strongest
        # ストレート
        elif self._is_straight(hand_sorted):
            return Hands.straight + self.strongest
        # スリーカード
        elif self._is_three_of_a_kind(hand_sorted):
            return Hands.three_of_a_kind + self.strongest
        # ツーペア
        elif self._is_two_pair(hand_sorted):
            return Hands.two_pair + self.strongest
        # ワンペア
        elif self._is_one_pair(hand_sorted):
            return Hands.one_pair + self.strongest
        # 役なし
        else:
            return self.strongest

    def _is_flush(self, hand):
        """受け取った手札がフラッシュであるかどうかを判定する関数"""
        is_flush = True
        # 最初の札のマークをとってくる
        first_suit = hand[0].suit
        for c in hand[1:]:
            # ひとつでもマークの違う札があればFalseになる
            is_flush = is_flush & (first_suit == c.suit)
        return is_flush

    def _is_straight(self, hand):
        """受け取った手札がストレートであるかどうかを判定する関数"""
        is_straight = True
        first_rank = hand[0].rank
        if first_rank == 2:
            # 3から始まるenumerateで、2〜4枚目の数字とループ番号が等しいかを調べる
            for i, c in enumerate(hand[1:4], 3):
                # print("rank: {}".format(c.rank))
                # print("comparing with: {}".format(i))
                is_straight = is_straight & (c.rank == i)
            # 最後が6またはエースかどうかを調べる
            # 2, 3, 4, 5, 6またはA, 2, 3, 4, 5に合致するかどうか
            is_straight = is_straight & (
                (hand[4].rank == 6) or (hand[4].rank == 14))
        else:
            for i, c in enumerate(hand[1:], 1):
                # print("rank: {}".format(c.rank))
                # print("comparing with: {}".format(first_rank + i))
                is_straight = is_straight & (c.rank == (first_rank + i))
        return is_straight

    def _is_royal_straight_flush(self, hand):
        """受け取った手札がロイヤルストレートフラッシュであるかどうかを判定する関数"""
        is_royal = True
        is_royal = is_royal & self._is_flush(hand)
        is_royal = is_royal & self._is_straight(hand)
        is_royal = is_royal & (hand[4].rank == 14)
        is_royal = is_royal & (hand[3].rank == 13)
        return is_royal

    def _is_four_of_a_kind(self, hand):
        """受け取った手札がフォーカードであるかどうかを判定する関数"""
        if hand[0].rank == hand[1].rank == hand[2].rank == hand[3].rank:
            is_four = True
            self.strongest = hand[3].rank
        elif hand[1].rank == hand[2].rank == hand[3].rank == hand[4].rank:
            is_four = True
        else:
            is_four = False
        return is_four

    def _is_fullhouse(self, hand):
        """受け取った手札がフルハウスであるかどうかを判定する関数"""
        if (hand[0].rank == hand[1].rank == hand[2].rank) and (hand[3].rank == hand[4].rank):
            self.strongest = hand[0].rank
            is_fullhouse = True
        elif (hand[0].rank == hand[1].rank) and (hand[2].rank == hand[3].rank == hand[4].rank):
            self.strongest = hand[2].rank
            is_fullhouse = True
        else:
            is_fullhouse = False
        return is_fullhouse

    def _is_three_of_a_kind(self, hand):
        """受け取った手札がスリーカードであるかどうかを判定する関数"""
        if hand[0].rank == hand[1].rank == hand[2].rank:
            self.strongest = hand[0].rank
            is_three = True
        elif hand[1].rank == hand[2].rank == hand[3].rank:
            self.strongest = hand[1].rank
            is_three = True
        elif hand[2].rank == hand[3].rank == hand[4].rank:
            self.strongest = hand[2].rank
            is_three = True
        else:
            is_three = False
        return is_three

    def _is_two_pair(self, hand):
        """受け取った手札がツーペアであるかどうかを判定する関数"""
        if (hand[0].rank == hand[1].rank) and (hand[2].rank == hand[3].rank):
            self.strongest = max(hand[0].rank, hand[2].rank)
            is_two = True
        elif (hand[0].rank == hand[1].rank) and (hand[3].rank == hand[4].rank):
            self.strongest = max(hand[0].rank, hand[3].rank)
            is_two = True
        elif (hand[1].rank == hand[2].rank) and (hand[3].rank == hand[4].rank):
            self.strongest = max(hand[1].rank, hand[3].rank)
            is_two = True
        else:
            is_two = False
        return is_two

    def _is_one_pair(self, hand):
        """受け取った手札がワンペアであるかどうかを判定する関数"""
        if hand[0].rank == hand[1].rank:
            self.strongest = hand[0].rank
            is_one = True
        elif hand[1].rank == hand[2].rank:
            self.strongest = hand[1].rank
            is_one = True
        elif hand[2].rank == hand[3].rank:
            self.strongest = hand[2].rank
            is_one = True
        elif hand[3].rank == hand[4].rank:
            self.strongest = hand[3].rank
            is_one = True
        else:
            is_one = False
        return is_one


class Poker(object):

    """ポーカーを行うためのオブジェクト"""

    def __init__(self):
        super().__init__()
        self._deck = Deck(52)
        self._player_hand = Hand(5, self._deck)
        self._hisoka_hand = Hand(5, self._deck)
        self.judge = Judge()

    def first_hand_str(self):
        """最初の手札を文字列化して返す関数"""
        # 文字列化した手札を返す
        # reply.py側で交換するカードを引数にしてchange_and_judge関数を実行してもらう
        return " ".join(list(map(lambda t: "{0}:{1}".format(t[0], str(t[1])),
                                 zip(range(1, len(self._player_hand.hand_list)+1),
                                     self._player_hand.hand_list))))

    def change_and_judge(self, *nums):
        """プレイヤーの手札のうち交換するカードの番号を受取り、その番号の
           カードを交換したのち、手札の役を判定する関数
           判定関数に手札を渡し、返ってきた点数を結果表示関数に渡す"""
        # 1. 交換するカードの番号を受取る
        # 2. 交換を実行
        # 3. 役判定関数に渡す
        for num in nums:
            if 1 <= num <= 5:
                self._player_hand.change(num)

        result_p = self.judge.judge(self._player_hand)
        result_h = self.judge.judge(self._hisoka_hand)

        return self._result(result_p, result_h)

    def _result(self, result1, result2):
        """judge関数が生成した結果をもとに、カード一覧と、勝敗を表す文字列を返す"""
        ph_str = " ".join(map(str, self._player_hand.hand_list))
        hh_str = " ".join(map(str, self._hisoka_hand.hand_list))
        if result1 > result2:
            return ("player", ph_str, hh_str)
        elif result1 < result2:
            return ("hisoka", ph_str, hh_str)
        else:
            return ("draw", ph_str, hh_str)


class PokerThread(threading.Thread):
    """ポーカーを処理する際に作成するスレッド"""
    def __init__(self, replyobj, mention):
        super().__init__()
        self.replyobj = replyobj
        self.mention = mention

    def run(self):
        # 勝ったプレイヤーを表す文字列が返ってくる
        result = self.replyobj._play_poker(self.mention)

        if result is not None:
            if result[0] == "player":
                reply_text = "\n" + "キミの手札は\n" + result[1] + "\nで、" + \
                    "ボクの手札は\n" + result[2] + "\n" + "だから…キミの勝ち、だね♠"
            elif result[0] == "hisoka":
                reply_text = "\n" + "キミの手札は\n" + result[1] + "\nで、" + \
                    "ボクの手札は\n" + result[2] + "\n" + "だから…ボクの勝ち、だね♥"
            elif result[0] == "draw":
                reply_text = "\n" + "キミの手札は\n" + result[1] + "\nで、" + \
                    "ボクの手札は\n" + result[2] + "\n" + "だから…引き分け、だね♦"
            else:
                reply_text = "【中の人より】ポーカーでエラーが発生しました。ごめんなさい。"
            status_code = self.replyobj.twitterlib.reply(self.mention, reply_text)
            self.replyobj._handle_status(status_code)


def is_valid_changenum(char):
    if char in ["0", "1", "2", "3", "4", "5"]:
        return True
    else:
        return False

def get_changenum(mention):
    return list(set(filter(is_valid_changenum, list(mention))))


# テスト
if __name__ == '__main__':
    poker = Poker()
    poker.judge(poker._player_hand)

