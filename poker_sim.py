#!/usr/bin/env python3

"""
Simulates many games of poker for statistical purposes.

author: Jason R. Carrete
"""

import csv
from random import shuffle
from optparse import OptionParser

VERSION = '1.0.1'
LONG_STR = False


class Card:
    """
    Cards are represented as numbers in the range [0, 51]
    """

    _suit_to_str = ('clubs', 'hearts', 'spades', 'diamonds')
    _suit_to_unicode = ('♣', '♥', '♠', '♦')
    _rank_to_str = ('two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king',
                    'ace')

    def __init__(self, value):
        self.value = value
        self.suit = value % 4
        self.rank = value // 4

    def suit_str(self):
        """
        :return: A string representation of the suit of this card.
        :rtype: str
        """
        return self._suit_to_str[self.suit]

    def unicode_suit(self):
        """
        :return: A unicode representation of the suit of this card. (♣, ♥, ♠, ♦)
        :rtype: str
        """
        return self._suit_to_unicode[self.suit]

    def rank_str(self):
        """
        :return: A string representation of the rank of this card.
        :rtype: str
        """
        return self._rank_to_str[self.rank]

    def short_rank_str(self):
        """
        :return: A single character representation of this card rank.
        :rtype: str
        """
        if self.rank <= 7:
            return str(self.rank + 2)
        else:
            return self.rank_str().upper()[0]

    def __hash__(self):
        return 13 * self.rank + 57 * self.suit

    def __lt__(self, other):
        return self.rank < other.rank

    def __le__(self, other):
        return self.rank <= other.rank

    def __eq__(self, other):
        return self.rank == other.rank

    def __ne__(self, other):
        return self.rank != other.rank

    def __gt__(self, other):
        return self.rank > other.rank

    def __ge__(self, other):
        return self.rank >= other.rank

    def __int__(self):
        return self.value

    def __str__(self):
        if not LONG_STR:
            return "{rank}{suit}".format(rank=self.short_rank_str(), suit=self.unicode_suit())
        else:
            return "{rank} of {suit}".format(rank=self.rank_str(), suit=self.suit_str())

    def __repr__(self):
        return "{suit}_{rank}".format(suit=self.suit_str(), rank=self.rank_str())


def compare_hand(hand1, hand2):
    """
    Compares two 5-card poker hands to see which is the better of the two

    :param hand1:
    :type hand1: list
    :param hand2:
    :type hand2: list
    :return: ``hand1`` if ``hand1`` is better than ``hand2``, ``hand2`` if ``hand2`` is
        better than ``hand1`` or both if they are equally strong
    :rtype: list
    """
    pass


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

    # Construct deck
    deck = [Card(i) for i in range(52)]

    def calc_winners(hole_cards, community):
        pass

    def play_game():
        nonlocal deck
        shuffle(deck)
        hole_cards = [[] for _ in range(options.players)]
        # Deal cards to players
        for _ in range(2):
            for player in range(options.players):
                hole_cards[player].append(deck.pop(0))
        # Deal community cards
        burn = list()
        community = list()
        burn.append(deck.pop(0))
        community.append(deck.pop(0))
        community.append(deck.pop(0))
        community.append(deck.pop(0))
        burn.append(deck.pop(0))
        community.append(deck.pop(0))
        burn.append(deck.pop(0))
        community.append(deck.pop(0))
        winning_hands = calc_winners(hole_cards, community)
        if options.output:
            with open(options.output, mode='w', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                row = ["{},{}".format(hand[0], hand[1]) for hand in hole_cards]
                row.insert(0, ','.join(map(str, community)))
                row.insert(0, ','.join(map(str, winning_hands)))
                writer.writerow(row)
        else:
            print([(str(hand[0]), str(hand[1])) for hand in hole_cards])
        deck = deck + burn + community + [card for hand in hole_cards for card in hand]

    for _ in range(options.simulations):
        play_game()


if __name__ == '__main__':
    main()
