# player.py
# Encapsulates player data and accessor functions

import json
import random

import globals as G

class player:

    def __init__(self, name, pclass, player_data=None):
        # initialize player data
        self.pd = dict()
        if player_data:
            self.pd = player_data
        else:
            self.pd['name'] = name
            self.pd['xp'] = 0
            self.pd['level'] = 1
            self.pd['class'] = pclass
            self.pd['defeated'] = False
            
            # get class info
            class_info = G.CLASSES[pclass]

            # get base stats
            self.pd['stats'] = class_info['base']
            # 3 bonus stat rolls for variation
            self.stat_roll(3)

            # initialize current health
            self.pd['health'] = self.pd['stats'][0]

            # status modifiers
            self.pd['mods'] = [0 for _ in range(len(self.pd['stats']))]

            # inventory - 2 free potions
            self.pd['items'] = {'potions' : 2}
            self.pd['weapon'] = None

    # increment player xp by n
    def xp_incr(self, n):
        self.pd['xp'] += n
        return self.level_check()

    # sets level according to player xp
    def level_check(self):
        prev_lvl = self.pd['level']
        for level in sorted(G.LEVEL_THRESHOLDS.keys()):
            # level up
            if self.pd['xp'] < G.LEVEL_THRESHOLDS[level]:
                print(f"Player {self.pd['name']} has reached level {level}")
                self.pd['level'] = level
                # get current health ratio
                hp_scale = self.pd['health']/self.pd['stats'][0]
                # stat roll for each level gained
                self.stat_roll(level - prev_lvl)
                # scale health
                self.pd['health'] = int(hp_scale * self.pd['stats'][0])
                return True

        return False

    # initiaite stat up k times, depending on class stat spread probability
    def stat_roll(self, k):
        # get stat spread
        stat_spread = G.CLASSES[self.pd['class']]['spread']
        # k times, each stat has chance to incr by 1 based on stat spread
        for _ in range(k):
            for i in range(len(self.pd['stats'])):
                chance = stat_spread[i]
                incr = random.choices([1, 0], weights=[100, 100-chance])[0]
                self.pd['stats'][i] += incr
    
    # inflict damage on player
    # returns if hit landed or not, and dmg inflicted
    def damage(self, move, dmg):
        # get move info
        move = G.MOVES[move]
        
        # get chance hit lands
        # speed of player decreases this chance (percentage)
        chance = int(move['chance'] * (1 - (self.pd['stats'][5]/100) ))

        # apply modifications to stats
        mod_stats = [sum(i) for i in zip(self.pd['stats'], self.pd['mods'])]

        if move['type'] == 'physical':
            dmg = max(0, dmg - mod_stats[2]) # subtract def
        elif move['type'] == 'magic':
            dmg = max(0, dmg - mod_stats[4]) # subtract res

        hit = random.choices([True, False], weights=[chance, 100-chance])
        
        if hit:
            self.pd['health'] = max(0, self.pd['health'] - dmg)

        return hit, dmg


    def dump(self):
        print(self.pd)


