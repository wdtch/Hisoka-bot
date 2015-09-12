#!/usr/bin/python
# -*- coding: utf-8 -*-

import random


class CardManager(object):
    """トランプのカードを取り扱うクラス"""

    def __init__(self):
        self._suits = ("spade", "club", "diamond", "heart")
        self._ranks = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
        # self.deck = self.generate_hand(52)
        self._ranks_f = (7, 8, 9, 10, 11, 12, 13, 14)

    def generate_card(self):
        """トランプのカード1枚を表すタプルを生成して返す"""
        card = (random.choice(self._suits), random.choice(self._ranks))
        return card

    def generate_hand(self, amount):
        """引数amountで指定された数のカードを生成し、それらをまとめて手札のリストとして返す"""
        count = 0
        hand = []
        while count < amount:
            card = self.generate_card()
            # 全く同じカードがあったときはもう一度カードを生成
            if card in hand:
                continue
            # 重複がなければ手札として採用
            else:
                hand.append(card)
                count += 1

        return hand

    def generate_card_f(self):
        """占い用のトランプのカード1枚を表すタプルを生成して返す"""
        card = (random.choice(self._suits), random.choice(self._ranks_f))
        return card

    def generate_hand_f(self, amount):
        """引数amountで指定された数のカードを生成し、それらをまとめて占い用の手札のリストとして返す"""
        count = 0
        hand = []
        while count < amount:
            card = self.generate_card_f()
            # 全く同じカードがあったときはもう一度カードを生成
            if card in hand:
                continue
            # 重複がなければ手札として採用
            else:
                hand.append(card)
                count += 1

        return hand

    def card_to_str(self, card):
        suit = card[0]
        card_str = ""
        # マーク部分
        if suit == "spade":
            card_str += "♠"
        elif suit == "club":
            card_str += "♣"
        elif suit == "diamond":
            card_str += "♦"
        elif suit == "heart":
            card_str += "♥"

        # 数字部分
        if card[1] == 11:
            card_str += "J"
        elif card[1] == 12:
            card_str += "Q"
        elif card[1] == 13:
            card_str += "K"
        elif card[1] == 14:
            card_str += "A"
        else:
            card_str += str(card[1])

        return card_str


class Poker(CardManager):

    def __init__(self):
        super().__init__()
        self.player_hand = self.generate_hand(5)
        self.hisoka_hand = self.generate_hand(5)

    def first_hand(self):
        player_hand_str = ""
        for card in self.player_hand:
            player_hand_str += self.card_to_str(card)
        return player_hand_str


class FourAceFortune(CardManager):

    def __init__(self):
        super().__init__()
        self._deck = self.generate_hand_f(32)
        self._spade_ace = ("spade", 14)
        self._club_ace = ("club", 14)
        self._diamond_ace = ("diamond", 14)
        self._heart_ace = ("heart", 14)

    def fortune(self):
        turn = 0
        ace_count = 0
        bad_fortune = False
        for _ in range(3):
            # print("--- Turn {} ---".format(turn))
            # ランダムに生成したデッキの上から13枚を取る
            hand = []
            for _ in range(13):
                hand.append(self._deck.pop(0))

            # デバッグ: 13枚の札を表示
            # print("--- first ---")
            # for card in hand:
            #     print(card)

            # エースを取り除く
            if self._spade_ace in hand:
                # 最初に現れたら不幸や災難がある
                if turn == 0:
                    bad_fortune = True
                    break
                hand.remove(self._spade_ace)
                ace_count += 1
            if self._club_ace in hand:
                hand.remove(self._club_ace)
                ace_count += 1
            if self._diamond_ace in hand:
                hand.remove(self._diamond_ace)
                ace_count += 1
            if self._heart_ace in hand:
                hand.remove(self._heart_ace)
                ace_count += 1

            # デバッグ: エースを取り除いた後の手札と、エースの枚数を表示
            # print("--- After Ace Removed ---")
            # for card in hand:
            #     print(card)
            # print("Ace count: {}".format(ace_count))

            # エースが全て揃ったらbreak
            if ace_count == 4:
                # print("break: ace_count = {}".format(ace_count))
                break

            # エース以外のカードをデッキに戻す
            for card in hand:
                self._deck.append(card)

            # デバッグ: シャッフル前のデッキを表示
            # print("deck before shuffle:")
            # for card in self._deck:
            #     print(card)

            # デッキをシャッフル(必要なのか…？)
            random.shuffle(self._deck)

            # デバッグ: シャッフル後のデッキを表示
            # print("deck after shuffle:")
            # for card in self._deck:
            #     print(card)

            # ターンを進める
            turn += 1
            # print("")

        return self._print_result(turn, bad_fortune)

    def _print_result(self, turn, bad_fortune):
        # if bad_fortune:
            # print("Be careful, you may meet with misfortune...")
            # return 4
        # else:
        if turn == 0:
            print("you are very lucky!!!")
            return 0
        elif turn == 1:
            print("you are lucky!")
            return 1
        elif turn == 2:
            print("you are not lucky or unlucky.")
            return 2
        elif turn == 3:
            print("Perhaps you are unlucky...")
            return 3
        else:
            print("Something wrong.")
            return 4


# テスト
if __name__ == '__main__':
    cm = CardManager()
    # print(cm.generate_card())
    # print(cm.generate_hand(5))
    # print(cm.generate_card_f())
    print(cm.card_to_str(("spade", 14)))
    print(cm.card_to_str(("spade", 11)))
    print(cm.card_to_str(("club", 4)))
    print(cm.card_to_str(("diamond", 12)))
    print(cm.card_to_str(("heart", 13)))

    # make a deck
    # print(cm.generate_hand(52))
    # for card in cm.generate_hand(52):
    #     print(card)

    # print("")

    # for card in cm.generate_hand_f(32):
    #     print(card)
    #     print(card["suit"])
    #     print(card["rank"])

    faf = FourAceFortune()
    # 1000回試行(なんかうまくいってない感)
    # v = 0
    # l = 0
    # n = 0
    # u = 0
    # e = 0
    # for _ in range(1000):
    #     num = faf.fortune()
    #     if num == 0:
    #         v += 1
    #     elif num == 1:
    #         l += 1
    #     elif num == 2:
    #         n += 1
    #     elif num == 3:
    #         u += 1
    #     elif num == 4:
    #         e += 1
    # print("Very lucky: {}".format(v))
    # print("Lucky: {}".format(l))
    # print("So-so: {}".format(n))
    # print("Unlucky: {}".format(u))
    # print("Error: {}".format(e))
    faf.fortune()