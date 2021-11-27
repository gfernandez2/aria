# player.py
# Encapsulates player data and accessor functions

import json
import random
import time

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
            # self.pd['defeated'] = False
            
            # get class info
            class_info = G.CLASSES[pclass]

            # get base stats
            self.pd['stats'] = class_info['base']
            # 3 bonus stat rolls for variation
            self.stat_roll(3)

            # moves map mov to time last used (for cooldown check)
            self.pd['moves'] = dict()
            for move in class_info['moves']:
                self.pd['moves'][move] = 0

            # maps status effects (moves) to when they were most recently applied, as well as 
            # mod list [n, n, n, n, n, n] which is applied when status is reversed
            self.pd['status'] = dict()

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
            if self.pd['xp'] < G.LEVEL_THRESHOLDS[level] and level != prev_lvl:
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
    
    # Handler for phys/mag type moves
    # inflict damage on player
    # returns if hit landed or not, and dmg inflicted
    def damage(self, move, dmg):
        # get move info
        move_info = G.MOVES[move]
        
        # get chance hit lands
        # speed of player decreases this chance (percentage)
        chance = int(move_info['chance'] * (1 - (self.pd['stats'][5]/100) ))

        # determine if hit lands
        hit = random.choices([True, False], weights=[chance, 100-chance])[0]

        if not hit:
            return hit, 0

        # apply modifications to stats
        mod_stats = [max(0, sum(i)) for i in zip(self.pd['stats'], self.pd['mods'])]

        if move_info['type'] == 'physical':
            dmg = max(0, dmg - mod_stats[2]) # subtract def
        elif move_info['type'] == 'magic':
            dmg = max(0, dmg - mod_stats[4]) # subtract res

        self.pd['health'] = max(0, self.pd['health'] - dmg)

        return hit, dmg
    
    # Handler for status-type moves
    # applies status move buff/debuff to player
    # returns move success
    def apply_status(self, move):
        # get move info
        move_info = G.MOVES[move]
        
        # get chance hit lands
        # speed of player decreases this chance (percentage)
        chance = int(move_info['chance'] * (1 - (self.pd['stats'][5]/100) ))

        # determine if move succeeds
        hit = random.choices([True, False], weights=[chance, 100-chance])[0]

        if not hit:
            return hit

        base_mods = move_info['mod']
        new_mods = [0 for _ in range(len(self.pd['stats']))]
        scale = move_info['scale']

        for i in range(len(self.pd['stats'])):
            if base_mods[i] == 0:
                continue
            # calculate modifications based on respective base stat
            new_mods[i] = base_mods[i] * int(self.pd['stats'][i] * (scale/100))

        # apply new_mods to mods
        self.pd['mods'] = [sum(i) for i in zip(new_mods, self.pd['mods'])]

        # record status time and reversal array
        self.pd['status'][move] = dict()
        self.pd['status'][move]['time'] = time.time()
        self.pd['status'][move]['reverse'] = [-1 * i for i in new_mods]
        
        return hit

    # Handler for heal-type moves
    def heal(self, move):
        # get move info
        move_info = G.MOVES[move]

        # calculate heal amount based on HP stat
        heal_amt = int(self.pd['stats'][0] * (move_info['scale']/100))

        # apply heal amount, capped by HP stat
        self.pd['health'] = min(self.pd['stats'][0], self.pd['health'] + heal_amt)

        return heal_amt
    
    # attemps to use move in player's moveset
    # returns if cooldown check passes - implementation of move is in game.py
    def check_cooldown(self, move):
        curr = time.time()
        if curr - self.pd['moves'][move] > G.MOVES[move]['cooldown']:
            self.pd['moves'][move] = curr
            return True

        return False

    def dump(self):
        print(self.pd)


