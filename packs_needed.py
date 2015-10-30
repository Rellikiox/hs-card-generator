"""Hearthstone simulations


All numbers taken from http://hearthstone.gamepedia.com/Card_pack_statistics"""

from __future__ import division
import random


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


class Collection(object):

    def __init__(self):
        self.cards = {
            set_name: {rarity: list(amount) for rarity, amount in rarity_amounts.iteritems()}
            for set_name, rarity_amounts in SETS.iteritems()
        }


class Pack(object):

    def __init__(self, set_name):
        rolls = self.get_rolls()
        self.cards = [Card(set_name, rarity) for rarity in rolls]

    def get_rolls(self):
        """Get 5 card random rarities

        You're guaranteed at least a rare. I'm not really sure how that's implemented,
        so if we get 5 commons we re-roll the last one"""
        rolls = [weighted_choice(CHANCE) for i in range(5)]
        if all(roll == 'c' for roll in rolls):
            rolls[4] = weighted_choice(CHANCE[1:])
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

    def __str__(self):
        return "{}{}{}".format(self.rarity, self.index, '*' if self.golden else '')


def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w > r:
            return c
        upto += w
    assert False, "Shouldn't get here"


def main():
    common = 0
    rare = 0
    epic = 0
    legendary = 0
    for i in range(100000):
        pack = Pack('classic')
        for card in pack.cards:
            if card.rarity == 'c':
                common += 1
            elif card.rarity == 'r':
                rare += 1
            elif card.rarity == 'e':
                epic += 1
            elif card.rarity == 'l':
                legendary += 1
    print common, rare, epic, legendary
    total = common + rare + epic + legendary
    print common / total, rare / total, epic / total, legendary / total


if __name__ == '__main__':
    main()
