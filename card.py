#!/usr/bin/python
# -*- coding: utf-8 -*-

import random


class Card(object):

    """トランプのカード1枚を表すオブジェクト"""

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        card_str = ""

        # マーク部分
        if self.suit == "spade":
            card_str += "♠"
        elif self.suit == "club":
            card_str += "♣"
        elif self.suit == "diamond":
            card_str += "♦"
        elif self.suit == "heart":
            card_str += "♥"

        # 数字部分
        if self.rank == 11:
            card_str += "J"
        elif self.rank == 12:
            card_str += "Q"
        elif self.rank == 13:
            card_str += "K"
        elif self.rank == 14:
            card_str += "A"
        else:
            card_str += str(self.rank)

        return card_str

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return self.__dict__ != other.__dict__


class CardManager(object):

    """トランプのカードを汎用的に取り扱うクラス"""

    def __init__(self):
        self._suits = ("spade", "club", "diamond", "heart")
        self._ranks = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
        self._ranks_f = (7, 8, 9, 10, 11, 12, 13, 14)

    def _generate_card(self):
        """トランプのカード1枚を生成して返す"""
        card = Card(random.choice(self._suits), random.choice(self._ranks))
        return card

    def generate_cards(self, amount):
        """引数amountで指定された数のカードを生成し、それらをまとめて手札のリストとして返す"""
        count = 0
        hand = []
        while count < amount:
            card = self._generate_card()
            # 全く同じカードがあったときはもう一度カードを生成
            if card in hand:
                continue
            # 重複がなければ手札として採用
            else:
                hand.append(card)
                count += 1

        return hand

    def _generate_card_f(self):
        """占い用のトランプのカード1枚を生成して返す"""
        card = Card(random.choice(self._suits), random.choice(self._ranks_f))
        return card

    def generate_cards_f(self, amount):
        """引数amountで指定された数のカードを生成し、それらをまとめて占い用の手札のリストとして返す"""
        count = 0
        hand = []
        while count < amount:
            card = self._generate_card_f()
            # 全く同じカードがあったときはもう一度カードを生成
            if card in hand:
                continue
            # 重複がなければ手札として採用
            else:
                hand.append(card)
                count += 1

        return hand


class Deck(CardManager):

    def __init__(self, num, for_fortune=False):
        super().__init__()
        if for_fortune:
            self.deck = self.generate_cards_f(num)
        else:
            self.deck = self.generate_cards(num)

    def draw(self):
        """デッキの先頭からカードを1枚ドロー"""
        return self.deck.pop()

    def return_card(self, card):
        self.deck.append(card)

    def shuffle(self):
        random.shuffle(self.deck)


class Hand(object):

    """n枚の手札を表すオブジェクト"""

    def __init__(self, num, deck):
        self.deck = deck
        self.hand_list = [self.deck.draw() for _ in range(num)]

    def __str__(self):
        return " ".join(map(str, self.hand_list))

    def __iter__(self):
        return iter(self.hand_list)

    def change(self, pos):
        """posで指定された番目のカードを交換する"""
        self.hand_list[pos - 1] = self.deck.draw()

    def remove(self, card):
        self.hand_list.remove(card)


# テスト
if __name__ == '__main__':
    # cm = CardManager()
    # print(cm.generate_card())
    # print(cm.generate_hand(5))
    # print(cm.generate_card_f())
    print(Card("spade", 14))
    print(Card("spade", 11))
    print(Card("club", 4))
    print(Card("diamond", 12))
    print(Card("heart", 13))
    # print("")