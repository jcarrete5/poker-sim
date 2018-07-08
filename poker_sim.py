#!/usr/bin/env python3

"""
Simulates many games of poker for statistical purposes.

author: Jason R. Carrete
"""

import csv
from enum import Enum, auto, unique
from collections import Counter
from random import shuffle
from optparse import OptionParser

VERSION = '1.0.1'
LONG_STR = False  # Determines if string representations should be long rather than short


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


class OrderedEnum(Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


@unique
class Suit(Enum):
    SPADES = 0
    CLUBS = auto()
    HEARTS = auto()
    DIAMONDS = auto()

    def __str__(self):
        if LONG_STR:
            return self.name.lower()
        else:
            if self is Suit.SPADES:
                return '♠'
            elif self is Suit.CLUBS:
                return '♣'
            elif self is Suit.HEARTS:
                return '♥'
            elif self is Suit.DIAMONDS:
                return '♦'


@unique
class Rank(OrderedEnum):
    TWO = 2
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    TEN = auto()
    JACK = auto()
    QUEEN = auto()
    KING = auto()
    ACE = auto()

    def __str__(self):
        if LONG_STR:
            return self.name.lower()
        else:
            if self is Rank.TWO:
                return '2'
            elif self is Rank.THREE:
                return '3'
            elif self is Rank.FOUR:
                return '4'
            elif self is Rank.FIVE:
                return '5'
            elif self is Rank.SIX:
                return '6'
            elif self is Rank.SEVEN:
                return '7'
            elif self is Rank.EIGHT:
                return '8'
            elif self is Rank.NINE:
                return '9'
            elif self is Rank.TEN:
                return 'T'
            elif self is Rank.JACK:
                return 'J'
            elif self is Rank.QUEEN:
                return 'Q'
            elif self is Rank.KING:
                return 'K'
            elif self is Rank.ACE:
                return 'A'


class Card:
    def __init__(self, value):
        self._value = value
        self._suit = Suit(value % 4)
        self._rank = Rank(value // 4 + 2)

    @property
    def suit(self):
        return self._suit

    @property
    def rank(self):
        return self._rank

    @property
    def value(self):
        return self._value

    def __hash__(self):
        return 13 * self.value

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented

    def __ne__(self, other):
        if self.__class__ is other.__class__:
            return self.value != other.value
        return NotImplemented

    def __str__(self):
        fmt_str = "{rank} of {suit}" if LONG_STR else "{rank}{suit}"
        return fmt_str.format(rank=str(self.rank), suit=str(self.suit))


@static_vars(HIGH=0, PAIR=1000000, TWO_PAIR=2000000, SET=3000000, STRAIGHT=4000000, FLUSH=5000000,
             FULL=6000000, FOUR=7000000, STRAIGHT_FLUSH=8000000, ROYAL=9000000)
def value_hand(hand):
    """
    Gives the hand a score based on how strong it is. Higher scores
    mean stronger hands. Hands must contain 5 cards.

    :param hand: The hand being scored
    :type hand: list
    :return: The score of the hand
    :rtype: int
    """
    assert len(hand) == 5
    score = 0
    hand = sorted(hand, reverse=True)
    min_card, max_card = min(hand), max(hand)
    suits_in_hand = set(card.suit for card in hand)
    ranks_in_hand = set(card.rank for card in hand)

    def is_straight():
        """
        Determines if the hand is a straight

        :return: The kicker for the straight or -1 if there is no straight
        :rtype: int
        """
        min_rank, max_rank = min_card.rank, max_card.rank
        if max_card.rank == 12 and min_card.rank == 0:
            min_rank, max_rank = -1, hand[1].rank
        return len(ranks_in_hand) == 5 and max_rank - min_rank == 4

    # Check pair hands (pair, full house, ...)
    counter = Counter(card.rank for card in hand)
    most_common = counter.most_common(2)
    if most_common[0][1] == 3 and most_common[1][1] == 2:
        score = value_hand.FULL
    elif most_common[0][1] == 2 and most_common[1][1] == 2:
        score = value_hand.TWO_PAIR
    elif most_common[0][1] == 3 and most_common[1][1] == 1:
        score = value_hand.SET
    elif most_common[0][1] == 2 and most_common[1][1] == 1:
        score = value_hand.PAIR
    elif most_common[0][1] == 4 and most_common[1][1] == 1:
        score = value_hand.FOUR
    # Check for flush
    score = value_hand.FLUSH if len(suits_in_hand) == 1 and score < value_hand.FLUSH else score
    if score < value_hand.FLUSH:
        # Check for straight
        if is_straight():
            score = value_hand.STRAIGHT
    elif is_straight():  # Check for straight flush
        score = value_hand.STRAIGHT_FLUSH
    return score


def main():
    opt_parser = OptionParser(
        description="Simulates games of texas hold'em to see how they would play out",
        version=VERSION)
    opt_parser.add_option("-p", "--players", type='int', metavar="NUM_PLAYERS",
                          default=9, help="Specifies the number of players being dealt in [default: %default]")
    opt_parser.add_option("-s", "--simulations", type='int', metavar="NUM_SIMULATIONS",
                          default=1000, help="Specifies the number of simulations to run [default: %default]")
    opt_parser.add_option("-l", "--long", action='store_true',
                          default=False, help="Use long-winded string representations for the cards")
    opt_parser.add_option("-o", "--output", metavar="FILE", help="File to output results to")
    options, _ = opt_parser.parse_args()
    global LONG_STR
    LONG_STR = options.long

    def calc_winners(hole_cards, community):
        pass

    def play_game():
        # Construct deck
        deck = [Card(i) for i in range(52)]
        shuffle(deck)
        hole_cards = [[] for _ in range(options.players)]
        # Deal cards to players
        for _ in range(2):
            for player in range(options.players):
                hole_cards[player].append(deck.pop(0))
        # Deal community cards
        community = list()
        deck.pop(0)  # Burn
        community.append(deck.pop(0))
        community.append(deck.pop(0))
        community.append(deck.pop(0))
        deck.pop(0)  # Burn
        community.append(deck.pop(0))
        deck.pop(0)  # Burn
        community.append(deck.pop(0))
        # Get winning hands
        winners = calc_winners(hole_cards, community)
        # Write result of the game
        if options.output:
            with open(options.output, mode='w', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                row = ["{},{}".format(hand[0], hand[1]) for hand in hole_cards]
                row.insert(0, ','.join(map(str, community)))
                row.insert(0, ','.join(map(str, winners)))
                writer.writerow(row)
        else:
            print([(str(hand[0]), str(hand[1])) for hand in hole_cards])

    for _ in range(options.simulations):
        play_game()


if __name__ == '__main__':
    main()
