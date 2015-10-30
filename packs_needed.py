"""Hearthstone simulations


All numbers taken from http://hearthstone.gamepedia.com/Card_pack_statistics"""

from pprint import pprint
import random
from collections import defaultdict

from collection import Collection
from collection import Pack


def simulate(runs=10000):
    common = 0
    rare = 0
    epic = 0
    legendary = 0
    for i in range(runs):
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


def main():
    c = Collection()
    packs_bougth = defaultdict(int)
    while not c.is_complete():
        set_name = random.choice(['classic', 'gvg', 'tgt'])
        packs_bougth[set_name] += 1
        c.open_pack(Pack(set_name))
        c.dissenchant_extras()
    pprint(packs_bougth)
    print sum(packs_bougth.values())


if __name__ == '__main__':
    main()
