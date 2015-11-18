# from unittest import TestCase
# import nose
import unittest
import copy
import operator
import card
import poker


class TestPoker(unittest.TestCase):

    def setUp(self):
        self.poker = poker.Poker()

    def tearDown(self):
        pass

    def test_change(self):
        """カード交換のテスト"""
        hand_before = copy.deepcopy(self.poker._player_hand)
        self.poker.change_and_judge(2, 4)
        print("")
        print(hand_before)
        print(self.poker._player_hand)
        self.assertTrue(hand_before.hand_list[0] == self.poker._player_hand.hand_list[0])
        self.assertTrue(hand_before.hand_list[1] != self.poker._player_hand.hand_list[1])
        self.assertTrue(hand_before.hand_list[2] == self.poker._player_hand.hand_list[2])
        self.assertTrue(hand_before.hand_list[3] != self.poker._player_hand.hand_list[3])
        self.assertTrue(hand_before.hand_list[4] == self.poker._player_hand.hand_list[4])


class TestJudgement(unittest.TestCase):

    def setUp(self):
        self.judge = poker.Judge()

    def tearDown(self):
        pass

    def test_judge_royalstraight1(self):
        """ロイヤルストレートフラッシュ(スペード)の判定テスト"""
        hand = [card.Card("spade", 13), card.Card("spade", 10), card.Card(
            "spade", 11), card.Card("spade", 12), card.Card("spade", 14)]
        result = self.judge.judge(hand)
        self.assertEqual(result, 900)

    def test_judge_royalstraight2(self):
        """ロイヤルストレートフラッシュ(クラブ)の判定テスト"""
        hand = [card.Card("club", 10), card.Card("club", 11), card.Card(
            "club", 12), card.Card("club", 13), card.Card("club", 14)]
        result = self.judge.judge(hand)
        self.assertEqual(result, 900)

    def test_judge_royalstraight3(self):
        """ロイヤルストレートフラッシュ(ダイヤ)の判定テスト"""
        hand = [card.Card("diamond", 10), card.Card("diamond", 13), card.Card(
            "diamond", 14), card.Card("diamond", 11), card.Card("diamond", 12)]
        result = self.judge.judge(hand)
        self.assertEqual(result, 900)

    def test_judge_royalstraight4(self):
        """ロイヤルストレートフラッシュ(ハート)の判定テスト"""
        hand = [card.Card("heart", 14), card.Card("heart", 11), card.Card(
            "heart", 13), card.Card("heart", 12), card.Card("heart", 10)]
        result = self.judge.judge(hand)
        self.assertEqual(result, 900)

    def test_straight_flush1(self):
        """ストレートフラッシュの判定テスト1"""
        hand = [card.Card("spade", 5), card.Card("spade", 7), card.Card(
            "spade", 9), card.Card("spade", 8), card.Card("spade", 6)]
        result = self.judge.judge(hand)
        self.assertEqual(result, 809)

    def test_straight_flush2(self):
        """ストレートフラッシュの判定テスト2"""
        hand = [card.Card("club", 10), card.Card("club", 12), card.Card(
            "club", 9), card.Card("club", 11), card.Card("club", 13)]
        result = self.judge.judge(hand)
        self.assertEqual(result, 813)

    def test_straight_flush3(self):
        """ストレートフラッシュの判定テスト3"""
        hand = [card.Card("spade", 2), card.Card("spade", 3), card.Card(
            "spade", 4), card.Card("spade", 5), card.Card("spade", 14)]
        result = self.judge.judge(hand)
        self.assertEqual(result, 814)

    def test_four_of_a_kind1(self):
        """フォーカードの判定テスト1"""
        hand = [card.Card("spade", 2), card.Card("club", 2), card.Card(
            "diamond", 4), card.Card("heart", 2), card.Card("diamond", 2)]
        result = self.judge.judge(hand)
        self.assertEqual(result, 702)

    def test_four_of_a_kind2(self):
        """フォーカードの判定テスト2"""
        hand = [card.Card("club", 6), card.Card("club", 9), card.Card(
            "diamond", 6), card.Card("spade", 6), card.Card("heart", 6)]
        result = self.judge.judge(hand)
        self.assertEqual(result, 706)

    def test_four_of_a_kind3(self):
        """フォーカードの判定テスト1"""
        hand = [card.Card("spade", 13), card.Card("club", 13), card.Card(
            "diamond", 13), card.Card("heart", 13), card.Card("diamond", 14)]
        result = self.judge.judge(hand)
        self.assertEqual(result, 713)

    def test_full_house1(self):
        """フルハウスの判定テスト1"""
        hand = [card.Card("spade", 13), card.Card("club", 13), card.Card(
            "diamond", 3), card.Card("heart", 3), card.Card("spade", 3)]
        result = self.judge.judge(hand)
        self.assertEqual(result, 603)

    def test_full_house2(self):
        """フルハウスの判定テスト2"""
        hand = [card.Card("diamond", 14), card.Card("club", 2), card.Card(
            "diamond", 2), card.Card("heart", 14), card.Card("spade", 14)]
        result = self.judge.judge(hand)
        self.assertEqual(result, 614)

    def test_full_house3(self):
        """フルハウスの判定テスト3"""
        hand = [card.Card("club", 12), card.Card("club", 13), card.Card(
            "diamond", 13), card.Card("heart", 13), card.Card("spade", 12)]
        result = self.judge.judge(hand)
        self.assertEqual(result, 613)

    def test_flush1(self):
        """フラッシュの判定テスト1"""
        hand = [card.Card("club", 6), card.Card("club", 13), card.Card(
            "club", 4), card.Card("club", 14), card.Card("club", 7)]
        result = self.judge.judge(hand)
        self.assertTrue(self.judge._is_flush(sorted(hand, key=operator.attrgetter("rank"))))
        self.assertEqual(result, 514)

    def test_flush2(self):
        """フラッシュの判定テスト2"""
        hand = [card.Card("spade", 12), card.Card("spade", 10), card.Card(
            "spade", 5), card.Card("spade", 2), card.Card("spade", 9)]
        result = self.judge.judge(hand)
        self.assertTrue(self.judge._is_flush(sorted(hand, key=operator.attrgetter("rank"))))
        self.assertEqual(result, 512)

    def test_flush3(self):
        """フラッシュの判定テスト3"""
        hand = [card.Card("diamond", 8), card.Card("diamond", 11), card.Card(
            "diamond", 3), card.Card("diamond", 14), card.Card("diamond", 5)]
        result = self.judge.judge(hand)
        self.assertTrue(self.judge._is_flush(sorted(hand, key=operator.attrgetter("rank"))))
        self.assertEqual(result, 514)

    def test_straight1(self):
        """ストレートの判定テスト1"""
        hand = [card.Card("diamond", 6), card.Card("diamond", 10), card.Card(
            "club", 8), card.Card("spade", 9), card.Card("club", 7)]
        result = self.judge.judge(hand)
        self.assertTrue(self.judge._is_straight(sorted(hand, key=operator.attrgetter("rank"))))
        self.assertEqual(result, 410)

    def test_straight2(self):
        """ストレートの判定テスト2"""
        hand = [card.Card("heart", 4), card.Card("heart", 14), card.Card(
            "club", 3), card.Card("spade", 5), card.Card("spade", 2)]
        result = self.judge.judge(hand)
        self.assertTrue(self.judge._is_straight(sorted(hand, key=operator.attrgetter("rank"))))
        self.assertEqual(result, 414)

    def test_straight3(self):
        """ストレートの判定テスト3"""
        hand = [card.Card("spade", 11), card.Card("diamond", 10), card.Card(
            "heart", 13), card.Card("spade", 14), card.Card("club", 12)]
        result = self.judge.judge(hand)
        self.assertTrue(self.judge._is_straight(sorted(hand, key=operator.attrgetter("rank"))))
        self.assertEqual(result, 414)

    def test_three_of_a_kind1(self):
        """スリーカードの判定テスト1"""
        hand = [card.Card("diamond", 6), card.Card("diamond", 10), card.Card(
            "club", 6), card.Card("spade", 6), card.Card("club", 7)]
        result = self.judge.judge(hand)
        self.assertEqual(result, 306)

    def test_three_of_a_kind2(self):
        """スリーカードの判定テスト2"""
        hand = [card.Card("spade", 9), card.Card("heart", 9), card.Card(
            "club", 9), card.Card("heart", 14), card.Card("spade", 4)]
        result = self.judge.judge(hand)
        self.assertEqual(result, 309)

    def test_three_of_a_kind3(self):
        """スリーカードの判定テスト3"""
        hand = [card.Card("heart", 14), card.Card("diamond", 10), card.Card(
            "club", 14), card.Card("diamond", 7), card.Card("spade", 14)]
        result = self.judge.judge(hand)
        self.assertEqual(result, 314)

    def test_two_pair1(self):
        """ツーペアの判定テスト1"""
        hand = [card.Card("heart", 6), card.Card("diamond", 2), card.Card(
            "club", 2), card.Card("spade", 8), card.Card("club", 8)]
        result = self.judge.judge(hand)
        self.assertEqual(result, 208)

    def test_two_pair2(self):
        """ツーペアの判定テスト2"""
        hand = [card.Card("heart", 4), card.Card("spade", 13), card.Card(
            "club", 6), card.Card("diamond", 13), card.Card("club", 4)]
        result = self.judge.judge(hand)
        self.assertEqual(result, 213)

    def test_two_pair3(self):
        """ツーペアの判定テスト3"""
        hand = [card.Card("diamond", 6), card.Card("club", 5), card.Card(
            "spade", 12), card.Card("heart", 6), card.Card("diamond", 5)]
        result = self.judge.judge(hand)
        self.assertEqual(result, 206)

    def test_one_pair1(self):
        """ワンペアの判定テスト1"""
        hand = [card.Card("club", 14), card.Card("diamond", 14), card.Card(
            "heart", 2), card.Card("club", 10), card.Card("spade", 9)]
        result = self.judge.judge(hand)
        self.assertEqual(result, 114)

    def test_one_pair2(self):
        """ワンペアの判定テスト2"""
        hand = [card.Card("spade", 5), card.Card("spade", 3), card.Card(
            "spade", 2), card.Card("club", 14), card.Card("spade", 3)]
        result = self.judge.judge(hand)
        self.assertEqual(result, 103)

    def test_one_pair3(self):
        """ワンペアの判定テスト3"""
        hand = [card.Card("diamond", 2), card.Card("diamond", 3), card.Card(
            "heart", 2), card.Card("heart", 4), card.Card("spade", 13)]
        result = self.judge.judge(hand)
        self.assertEqual(result, 102)

    def test_high_cards1(self):
        """役なしの判定テスト1"""
        hand = [card.Card("spade", 14), card.Card("diamond", 5), card.Card(
            "heart", 9), card.Card("club", 4), card.Card("spade", 6)]
        result = self.judge.judge(hand)
        self.assertEqual(result, 14)

    def test_high_cards2(self):
        """役なしの判定テスト2"""
        hand = [card.Card("heart", 12), card.Card("heart", 5), card.Card(
            "heart", 9), card.Card("spade", 7), card.Card("heart", 6)]
        result = self.judge.judge(hand)
        self.assertEqual(result, 12)

    def test_high_cards3(self):
        """役なしの判定テスト3"""
        hand = [card.Card("club", 10), card.Card("club", 12), card.Card(
            "club", 11), card.Card("diamond", 5), card.Card("club", 13)]
        result = self.judge.judge(hand)
        self.assertEqual(result, 13)

if __name__ == '__main__':
    # nose.main(argv=['nose', '-v'])
    unittest.main(argv=['nose', '-v'])
