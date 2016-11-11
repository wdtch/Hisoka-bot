#!/usr/bin/python
# -*- coding: utf-8 -*-

from card import *


class FourAceFortune(CardManager):

    def __init__(self):
        super().__init__()
        self.deck = Deck(32, True)
        self.spade_ace = Card("spade", 14)
        self.club_ace = Card("club", 14)
        self.diamond_ace = Card("diamond", 14)
        self.heart_ace = Card("heart", 14)

    def fortune(self):
        turn = 0
        ace_count = 0
        for _ in range(3):
            # print("--- Turn {} ---".format(turn))

            hand = Hand(13, self.deck)
            # デバッグ: デッキ13枚を表示
            # print("--- first ---")
            # print(*hand)

            # エースを取り除く
            if self.spade_ace in hand:
                # 最初に現れたら不幸や災難がある
                # if turn == 0:
                #     isbad_fortune = True
                #     break
                hand.remove(self.spade_ace)
                ace_count += 1
            if self.club_ace in hand:
                hand.remove(self.club_ace)
                ace_count += 1
            if self.diamond_ace in hand:
                hand.remove(self.diamond_ace)
                ace_count += 1
            if self.heart_ace in hand:
                hand.remove(self.heart_ace)
                ace_count += 1

            # デバッグ: エースを取り除いた後の手札と、エースの枚数を表示
            # print("--- After Ace Removed ---")
            # print(*hand)
            # print("Ace count: {}".format(ace_count))

            # エースが全て揃ったらbreak
            if ace_count == 4:
                # print("break: ace_count = {}".format(ace_count))
                break

            # エース以外のカードをデッキに戻す
            for card in hand:
                self.deck.return_card(card)

            # デバッグ: シャッフル前のデッキを表示
            # print("deck before shuffle:")
            # print(*self.deck.deck)

            # デッキをシャッフル(必要なのか…？)
            self.deck.shuffle()

            # デバッグ: シャッフル後のデッキを表示
            # print("deck after shuffle:")
            # print(*self.deck.deck)

            # ターンを進める
            turn += 1
            # print("")

        return self._print_result(turn)

    def _print_result(self, turn):
        if turn == 0:
            # print("you are very lucky!!!")
            return 0
        elif turn == 1:
            # print("you are lucky!")
            return 1
        elif turn == 2:
            # print("you are not lucky or unlucky.")
            return 2
        elif turn == 3:
            # print("Perhaps you are unlucky...")
            return 3
        else:
            # print("Something wrong.")
            return 4


def _fortune():
    """占いを実行し、結果を表す文を返す"""
    faf = FourAceFortune()
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

# テスト
if __name__ == '__main__':
    # 1000回試行
    v = 0
    l = 0
    n = 0
    u = 0
    e = 0
    for _ in range(10000):
        faf = FourAceFortune()
        num = faf.fortune()
        if num == 0:
            v += 1
        elif num == 1:
            l += 1
        elif num == 2:
            n += 1
        elif num == 3:
            u += 1
        elif num == 4:
            e += 1
    print("Very lucky: {}".format(v))
    print("Lucky: {}".format(l))
    print("So-so: {}".format(n))
    print("Unlucky: {}".format(u))
    print("Error: {}".format(e))