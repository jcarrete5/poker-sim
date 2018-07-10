#!/usr/bin/env python3

from poker_sim import Suit, Rank, Card, value_hand
from unittest import TestCase, main


class ValueHandTestCase(TestCase):
    def test_high_card_valuation(self):
        hand = [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.NINE),
            Card(Suit.CLUBS, Rank.TEN),
            Card(Suit.CLUBS, Rank.EIGHT),
            Card(Suit.HEARTS, Rank.QUEEN)
        ]
        self.assertEqual(value_hand(hand), 572846)

    def test_pair_valuation(self):
        hand = [
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.HEARTS, Rank.THREE),
            Card(Suit.HEARTS, Rank.TWO),
            Card(Suit.DIAMONDS, Rank.TEN),
            Card(Suit.CLUBS, Rank.TEN)
        ]
        self.assertEqual(value_hand(hand), 1030032)

    def test_two_pair_valuation(self):
        hand = [
            Card(Suit.SPADES, Rank.JACK),
            Card(Suit.HEARTS, Rank.JACK),
            Card(Suit.DIAMONDS, Rank.EIGHT),
            Card(Suit.HEARTS, Rank.FOUR),
            Card(Suit.CLUBS, Rank.FOUR)
        ]
        self.assertEqual(value_hand(hand), 2002220)

    def test_set_valuation(self):
        hand = [
            Card(Suit.SPADES, Rank.JACK),
            Card(Suit.SPADES, Rank.FOUR),
            Card(Suit.DIAMONDS, Rank.EIGHT),
            Card(Suit.HEARTS, Rank.FOUR),
            Card(Suit.CLUBS, Rank.FOUR)
        ]
        self.assertEqual(value_hand(hand), 3000946)

    def test_straight_valuation(self):
        hand = [
            Card(Suit.CLUBS, Rank.EIGHT),
            Card(Suit.DIAMONDS, Rank.NINE),
            Card(Suit.HEARTS, Rank.TEN),
            Card(Suit.HEARTS, Rank.SEVEN),
            Card(Suit.HEARTS, Rank.SIX)
        ]
        self.assertEqual(value_hand(hand), 4000010)

    def test_flush_valuation(self):
        hand = [
            Card(Suit.HEARTS, Rank.EIGHT),
            Card(Suit.HEARTS, Rank.NINE),
            Card(Suit.HEARTS, Rank.JACK),
            Card(Suit.HEARTS, Rank.SEVEN),
            Card(Suit.HEARTS, Rank.SIX)
        ]
        self.assertEqual(value_hand(hand), 5448944)

    def test_full_house_valuation(self):
        hand = [
            Card(Suit.HEARTS, Rank.SIX),
            Card(Suit.SPADES, Rank.SIX),
            Card(Suit.CLUBS, Rank.SIX),
            Card(Suit.HEARTS, Rank.SEVEN),
            Card(Suit.DIAMONDS, Rank.SEVEN)
        ]
        self.assertEqual(value_hand(hand), 6000091)

    def test_four_of_a_kind_valuation(self):
        hand = [
            Card(Suit.CLUBS, Rank.TWO),
            Card(Suit.DIAMONDS, Rank.TWO),
            Card(Suit.SPADES, Rank.TWO),
            Card(Suit.HEARTS, Rank.TWO),
            Card(Suit.HEARTS, Rank.SIX)
        ]
        self.assertEqual(value_hand(hand), 7000034)

    def test_straight_flush_valuation(self):
        hand = [
            Card(Suit.HEARTS, Rank.EIGHT),
            Card(Suit.HEARTS, Rank.NINE),
            Card(Suit.HEARTS, Rank.JACK),
            Card(Suit.HEARTS, Rank.TEN),
            Card(Suit.HEARTS, Rank.QUEEN)
        ]
        self.assertEqual(value_hand(hand), 8000012)

    def test_royal_flush_valuation(self):
        hand = [
            Card(Suit.HEARTS, Rank.TEN),
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.HEARTS, Rank.JACK),
            Card(Suit.HEARTS, Rank.QUEEN),
            Card(Suit.HEARTS, Rank.ACE)
        ]
        self.assertEqual(value_hand(hand), 9000000)


if __name__ == '__main__':
    main()
