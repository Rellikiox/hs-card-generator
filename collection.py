
from __future__ import division
from collections import defaultdict
import random

import utils

SETS = {
    'classic': {
        'c': 188,
        'r': 162,
        'e': 74,
        'l': 33
    },
    'gvg': {
        'c': 80,
        'r': 74,
        'e': 52,
        'l': 20
    },
    'tgt': {
        'c': 98,
        'r': 72,
        'e': 54,
        'l': 20
    }
}

CHANCE = [
    ('c', 0.7165),
    ('r', 0.2284),
    ('e', 0.0442),
    ('l', 0.0110)
]

GOLDEN_CHANCE = {
    'c': 0.0206,
    'r': 0.0554,
    'e': 0.0452,
    'l': 0.0731
}

DUST_VALUE = {
    'c': (5, 50),
    'r': (20, 100),
    'e': (100, 400),
    'l': (400, 1600)
}

MAX_COPIES = {
    'c': 2,
    'r': 2,
    'e': 2,
    'l': 1
}


class Collection(object):

    def __init__(self):
        self.cards = {
            set_name: {rarity: defaultdict(int) for rarity, amount in rarity_amounts.iteritems()}
            for set_name, rarity_amounts in SETS.iteritems()
        }
        self.dust = 0

    def open_pack(self, pack):
        for card in pack.cards:
            self.cards[pack.set_name][card.rarity].setdefault(card.index, []).append(card)

    def dissenchant_extras(self, keep_golden=False):
        for set_name, rarities in self.cards.iteritems():
            for rarity, cards in rarities.iteritems():
                for card_index, copies in cards.iteritems():
                    if len(copies) > MAX_COPIES[rarity]:
                        self.dust += self.dissenchant_extra_copies(copies, keep_golden)

    def dissenchant_extra_copies(self, copies, keep_golden):
        dust = 0
        max_copies = MAX_COPIES[copies[0].rarity]
        while len(copies) > max_copies:
            try:
                if keep_golden:
                    card = next(copy for copy in copies if not copy.golden)
                else:
                    card = next(copy for copy in copies if copy.golden)
            except StopIteration:
                card = copies[0]

            copies.remove(card)
            dust += card.dust_value()
        return dust


class Pack(object):

    def __init__(self, set_name):
        rolls = self.get_rolls()
        self.set_name = set_name
        self.cards = [Card(set_name, rarity) for rarity in rolls]

    def get_rolls(self):
        """Get 5 card random rarities

        You're guaranteed at least a rare. I'm not really sure how that's implemented,
        so if we get 5 commons we re-roll the last one"""
        rolls = [utils.weighted_choice(CHANCE) for i in range(5)]
        if all(roll == 'c' for roll in rolls):
            rolls[4] = utils.weighted_choice(CHANCE[1:])
        return rolls

    def __str__(self):
        return ', '.join([str(card) for card in self.cards])


class Card(object):

    def __init__(self, set_name, rarity):
        self.set_name = set_name
        self.rarity = rarity
        self.index = random.randint(0, SETS[set_name][self.rarity] - 1)
        # Try to upgrade to golden
        self.golden = GOLDEN_CHANCE[rarity] > random.random()

    def dust_value(self):
        return DUST_VALUE[self.rarity][1 if self.golden else 0]

    def __str__(self):
        return "{}{}{}".format(self.rarity, self.index, '*' if self.golden else '')
