#!/usr/bin/env python3

"""
Simulates games of poker for statistical purposes.

author: Jason R. Carrete
"""

import csv
from functools import total_ordering
from itertools import combinations
from enum import Enum, auto, unique
from collections import Counter, namedtuple
from random import shuffle
from optparse import OptionParser

VERSION = '1.2.0'
LONG_STR = False  # Determines if string representations should be long rather than short


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate


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


@total_ordering
@unique
class Rank(Enum):
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

    def __hash__(self):
        return 13 * self.value

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def __str__(self):
        if LONG_STR:
            return self.name.lower()
        else:
            if self is Rank.TEN:
                return 'T'
            elif self is Rank.JACK:
                return 'J'
            elif self is Rank.QUEEN:
                return 'Q'
            elif self is Rank.KING:
                return 'K'
            elif self is Rank.ACE:
                return 'A'
            else:
                return str(self.value)


@total_ordering
class Card:
    @static_vars(card_pool={})
    def __new__(cls, suit, rank):
        if (suit, rank) in Card.__new__.card_pool:
            return Card.__new__.card_pool[(suit, rank)]
        else:
            card = super().__new__(cls)
            card._suit = suit
            card._rank = rank
            Card.__new__.card_pool[(suit, rank)] = card
            return card

    @property
    def suit(self):
        return self._suit

    @property
    def rank(self):
        return self._rank

    def __hash__(self):
        return self.suit.value * 13 + self.rank.value * 97

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.suit is other.suit and self.rank is other.rank
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.rank < other.rank
        return NotImplemented

    def __str__(self):
        fmt_str = "{rank} of {suit}" if LONG_STR else "{rank}{suit}"
        return fmt_str.format(rank=str(self.rank), suit=str(self.suit))


@static_vars(HIGH=0, PAIR=1000000, TWO_PAIR=2000000, SET=3000000, STRAIGHT=4000000, FLUSH=5000000,
             FULL=6000000, FOUR=7000000, STRAIGHT_FLUSH=8000000, ROYAL=9000000, K=14)
def value_hand(hand):
    """
    Gives the hand a score based on how strong it is. Higher scores
    mean stronger hands. Hands must contain 5 cards.

    Helpful link for ranking hands http://www.mathcs.emory.edu/~cheung/Courses/170/Syllabus/10/pokerValue.html

    :param hand: The hand being scored
    :return: The score of the hand
    :rtype: int
    """
    assert len(hand) == 5
    score = 0
    hand = sorted(hand)
    suits_in_hand = set(card.suit for card in hand)
    ranks_in_hand = set(card.rank for card in hand)

    def is_straight():
        if len(ranks_in_hand) < 5:
            return False
        max_rank_value, min_rank_value = hand[-1].rank.value, hand[0].rank.value
        if {Rank.TWO, Rank.ACE} < ranks_in_hand:
            max_rank_value, min_rank_value = hand[-2].rank.value, Rank.TWO.value - 1
        return len(ranks_in_hand) == 5 and max_rank_value - min_rank_value == 4

    # Check pair hands (pair, full house, ...)
    counter = Counter(card.rank for card in hand)
    RankCount = namedtuple('RankCount', 'rank, count')
    rank_counts = [RankCount(e[0], e[1]) for e in counter.most_common()]
    if rank_counts[0].count == 3 and rank_counts[1].count == 2:  # Full house
        score = value_hand.FULL\
            + value_hand.K * rank_counts[0].rank.value\
            + rank_counts[1].rank.value
    elif rank_counts[0].count == 2 and rank_counts[1].count == 2:  # Two pair
        high_pair_value = max(rank_counts[0].rank.value, rank_counts[1].rank.value)
        low_pair_value = min(rank_counts[0].rank.value, rank_counts[1].rank.value)
        score = value_hand.TWO_PAIR\
            + value_hand.K**2 * high_pair_value\
            + value_hand.K * low_pair_value\
            + rank_counts[2].rank.value
    elif rank_counts[0].count == 3 and rank_counts[1].count == 1:  # Three of a kind
        high_kicker_value = max(rank_counts[1].rank.value, rank_counts[2].rank.value)
        low_kicker_value = min(rank_counts[1].rank.value, rank_counts[2].rank.value)
        score = value_hand.SET\
            + value_hand.K**2 * rank_counts[0].rank.value\
            + value_hand.K * high_kicker_value\
            + low_kicker_value
    elif rank_counts[0].count == 2 and rank_counts[1].count == 1:  # One pair
        kickers = sorted(ranks_in_hand - {rank_counts[0].rank}, reverse=True)
        score = value_hand.PAIR\
            + value_hand.K**3 * rank_counts[0].rank.value\
            + value_hand.K**2 * kickers[0].value\
            + value_hand.K * kickers[1].value\
            + kickers[2].value
    elif rank_counts[0].count == 4 and rank_counts[1].count == 1:  # Four of a kind
        score = value_hand.FOUR\
            + value_hand.K * rank_counts[0].rank.value\
            + rank_counts[1].rank.value
    # Check for flush
    if len(suits_in_hand) == 1:
        score = max(value_hand.FLUSH, score)
        # Check for straight_flush
        if is_straight():
            score = value_hand.STRAIGHT_FLUSH
            # Check for royal flush
            if min(ranks_in_hand) is Rank.TEN:
                score = value_hand.ROYAL
            else:
                score += Rank.FIVE.value if {Rank.TWO, Rank.ACE} < ranks_in_hand else max(ranks_in_hand).value
        else:
            score += sum(14**i * hand[i].rank.value for i in range(len(hand)))
    elif is_straight():  # Check for straight
        score = value_hand.STRAIGHT\
                + (Rank.FIVE.value if {Rank.TWO, Rank.ACE} < ranks_in_hand else max(ranks_in_hand).value)
    elif score < value_hand.PAIR:
        # High card is best hand
        score = sum(14**i * hand[i].rank.value for i in range(len(hand)))
    return score


def best_five_card_hand(card_list):
    return max(({'five_card_hand': c, 'value': value_hand(c)} for c in combinations(card_list, 5)),
               key=lambda x: x['value'])


def winning_hands(hole_cards, community):
    best_hands = [
        {'hole_cards': player_hole_cards, **best_five_card_hand(player_hole_cards + community)}
        for player_hole_cards in hole_cards
    ]
    best_hands.sort(key=lambda hand: hand['value'], reverse=True)
    return [hand for hand in best_hands if hand['value'] == best_hands[0]['value']]


def main():
    # TODO switch to argparse
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

    def play_game():
        # Construct deck
        deck = [Card(suit, rank) for suit in Suit for rank in Rank]
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
        winners = winning_hands(hole_cards, community)
        # Write result of the game
        if options.output:
            with open(options.output, mode='a', encoding='utf-8', newline='\n') as outfile:
                writer = csv.writer(outfile)
                row = [",".join(map(str, sorted(hand))) for hand in hole_cards]
                row.insert(0, ",".join(map(str, sorted(community))))
                row.insert(0, ";".join((",".join(map(str, sorted(hand['hole_cards']))) for hand in winners)))
                writer.writerow(row)
        else:
            print(list(map(str, community)), end=' - ')
            print([(str(hand[0]), str(hand[1])) for hand in hole_cards])
            print("Winners: ", list(list(map(str, sorted(hand['hole_cards']))) for hand in winners))

    for _ in range(options.simulations):
        play_game()


if __name__ == '__main__':
    main()
