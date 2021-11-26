# entity.py
# used for instantiating entities (enemies)
# similar to player.py, but with stripped down functionality

import json
import random
import time

import globals as G

class entity:

    # etype = enemy type
    # scale = scaling with player level; this value will be average lvl of party
    def __init__(self, etype, scale=5):
        # initialize player data
        self.ed = dict()
        self.ed['defeated'] = False
        self.ed['class'] = etype
            
        # get class info
        ent_info = G.ENEMIES[etype]

        # get base stats
        self.ed['name'] = random.choice(ent_info['name'])
        self.ed['stats'] = ent_info['base']
        # bonus stat rolls
        self.stat_roll(scale*2)

        # moves map mov to time last used (for cooldown check)
        self.ed['moves'] = dict()
        for move in ent_info['moves']:
            self.ed['moves'][move] = 0

        # initialize current health
        self.ed['health'] = self.ed['stats'][0]

        # status modifiers
        self.ed['mods'] = [0 for _ in range(len(self.ed['stats']))]

    # initiaite stat up k times, depending on class stat spread probability
    def stat_roll(self, k):
        # get stat spread
        stat_spread = G.ENEMIES[self.ed['class']]['spread']
        # k times, each stat has chance to incr by 1 based on stat spread
        for _ in range(k):
            for i in range(len(self.ed['stats'])):
                chance = stat_spread[i]
                incr = random.choices([1, 0], weights=[100, 100-chance])[0]
                self.ed['stats'][i] += incr
    
    # inflict damage on entity
    # returns if hit landed or not
    def damage(self, move, dmg):
        # get move info
        move = G.MOVES[move]
        
        # get chance hit lands
        # speed of entity decreases this chance (percentage)
        chance = int(move['chance'] * (1 - (self.ed['stats'][5]/100) ))

        # apply modifications to stats
        mod_stats = [sum(i) for i in zip(self.ed['stats'], self.ed['mods'])]

        if move['type'] == 'physical':
            dmg = max(0, dmg - mod_stats[2]) # subtract def
        elif move['type'] == 'magic':
            dmg = max(0, dmg - mod_stats[4]) # subtract res

        hit = random.choices([True, False], weights=[chance, 100-chance])[0]
        
        if hit:
            self.ed['health'] = max(0, self.ed['health'] - dmg)

        return hit, dmg

    # attemps to use move in entity's moveset
    # returns if cooldown check passes - implementation of move is in game.py
    def move(self, move):
        curr = time.time()
        if curr - self.ed['moves'][move] > G.MOVES[move]['cooldown']:
            self.ed['moves'][move] = curr
            return True

        return False


    def dump(self):
        print(self.ed)


