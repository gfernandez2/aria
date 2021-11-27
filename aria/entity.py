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
        # self.ed['defeated'] = False
        self.ed['class'] = etype
            
        # get class info
        ent_info = G.ENEMIES[etype]

        # get base stats
        self.ed['name'] = random.choice(ent_info['name'])
        self.ed['stats'] = ent_info['base']
        # bonus stat rolls
        self.stat_roll(scale*2)

        # map move to time last used (for cooldown check)
        self.ed['moves'] = dict()
        for move in ent_info['moves']:
            self.ed['moves'][move] = 0

        # maps status effects to when they were first applied, as well as 
        # mod list [0, 0, 0, 0, 0, 0] which is applied when status is reversed
        self.ed['status'] = dict()

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
    
    # Handler for phys/mag type moves
    # inflict damage on player
    # returns if hit landed or not, and dmg inflicted
    def damage(self, move, dmg):
        # get move info
        move_info = G.MOVES[move]
        
        # get chance hit lands
        # speed of player decreases this chance (percentage)
        chance = int(move_info['chance'] * (1 - (self.ed['stats'][5]/100) ))

        # determine if hit lands
        hit = random.choices([True, False], weights=[chance, 100-chance])[0]

        if not hit:
            return hit, 0

        # apply modifications to stats
        mod_stats = [max(0, sum(i)) for i in zip(self.ed['stats'], self.ed['mods'])]

        if move_info['type'] == 'physical':
            dmg = max(0, dmg - mod_stats[2]) # subtract def
        elif move_info['type'] == 'magic':
            dmg = max(0, dmg - mod_stats[4]) # subtract res

        self.ed['health'] = max(0, self.ed['health'] - dmg)

        return hit, dmg

    # Handler for status-type moves
    # applies status move buff/debuff to player
    # returns move success
    def apply_status(self, move):
        # get move info
        move_info = G.MOVES[move]
        
        # get chance hit lands
        # speed of player decreases this chance (percentage)
        chance = int(move_info['chance'] * (1 - (self.ed['stats'][5]/100) ))

        # determine if move succeeds
        hit = random.choices([True, False], weights=[chance, 100-chance])[0]

        if not hit:
            return hit

        base_mods = move_info['mod']
        new_mods = [0 for _ in range(len(self.ed['stats']))]
        scale = move_info['scale']

        for i in range(len(self.ed['stats'])):
            if base_mods[i] == 0:
                continue
            # calculate modifications based on respective base stat
            new_mods[i] = base_mods[i] * int(self.ed['stats'][i] * (scale/100))

        # apply new_mods to mods
        self.ed['mods'] = [sum(i) for i in zip(new_mods, self.ed['mods'])]

        # record status time and reversal array
        self.ed['status'][move] = dict()
        self.ed['status'][move]['time'] = time.time()
        self.ed['status'][move]['reverse'] = [-1 * i for i in new_mods]
        
        return hit

    # attemps to use move in entity's moveset
    # returns if cooldown check passes - implementation of move is in game.py
    def check_cooldown(self, move):
        curr = time.time()
        if curr - self.ed['moves'][move] > G.MOVES[move]['cooldown']:
            self.ed['moves'][move] = curr
            return True

        return False


    def dump(self):
        print(self.ed)


