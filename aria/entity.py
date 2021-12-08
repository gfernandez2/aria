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
        self.stat_roll(int(scale*1.2))

        # maps move to time last used (for cooldown check)
        self.ed['moves'] = dict()
        for move in ent_info['moves']:
            self.ed['moves'][move] = 0

        # maps status effects (moves) to when they were most recently applied, as well as 
        # mod list [n, n, n, n, n, n] which is applied when status is reversed
        self.ed['status'] = dict()

        # initialize current health
        self.ed['health'] = self.ed['stats'][0]

        # status modifiers
        self.ed['mods'] = [0 for _ in range(len(self.ed['stats']))]

    # returns current stats (with mods applied)
    def get_stats(self):
        return [max(0, sum(i)) for i in zip(self.ed['stats'], self.ed['mods'])]

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

        # if HP increased, set health to new maximum
        self.ed['health'] = self.ed['stats'][0]
    
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
            return f"Move {move} on {self.ed['name']} missed!"

        # get status with mods applied         
        mod_stats = self.get_stats()

        if move_info['type'] == 'physical':
            dmg = max(0, dmg - mod_stats[2]) # subtract def
        elif move_info['type'] == 'magic':
            dmg = max(0, dmg - mod_stats[4]) # subtract res

        self.ed['health'] = max(0, self.ed['health'] - dmg)

        return f"Move {move} on {self.ed['name']} hit for {dmg} damage!"

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
            return f"Move {move} on {self.ed['name']} missed!"

        resp = f"Move {move} on {self.ed['name']} succeeded!\n"

        base_mods = move_info['mod']
        new_mods = [0 for _ in range(len(self.ed['stats']))]
        scale = move_info['scale']

        for i in range(len(self.ed['stats'])):
            if base_mods[i] == 0:
                continue
            # calculate modifications based on respective base stat
            new_mods[i] = base_mods[i] * int(self.ed['stats'][i] * (scale/100))

        # Augment resp based on stat effects of move
        for i in range(len(base_mods)):
            if base_mods[i] == 0:
                continue;

            resp += G.STATS[i] + ' '

            if base_mods[i] == 1:
                resp += f'up by {new_mods[i]}!\n'
            elif base_mods[i] == -1:
                resp += f'down by {-1*new_mods[i]}!\n'

        # remove last newline
        resp = resp[:-1]

        # apply new_mods to mods
        self.ed['mods'] = [sum(i) for i in zip(new_mods, self.ed['mods'])]

        # record status time and reversal array
        self.ed['status'][move] = dict()
        self.ed['status'][move]['time'] = time.time()
        self.ed['status'][move]['reverse'] = [-1 * i for i in new_mods]
        
        return resp

    # check if move can be performed
    # returns if check passes
    def move_check(self, move):
        # check if entity can use move
        if move not in G.ENEMIES[self.ed['class']]['moves']:
            return False, f'Move {move} cannot be used!'

        # cooldown check
        curr = time.time()
        if curr - self.ed['moves'][move] < G.MOVES[move]['cooldown']:
            return False, f'Move {move} still in cooldown!'

        self.ed['moves'][move] = curr
        return True, f'Move {move} can be used!'

    # looks at all currently active status effects
    # if duration is passed, status is removed and effects are reversed
    def status_check(self):
        curr = time.time()
        remove_list = []
        for status, info in self.ed['status'].items():
            # if duration is up
            if curr - info['time'] > G.MOVES[status]['duration']:
                # apply reversal to stat mods
                self.ed['mods'] = [sum(i) for i in zip(info['reverse'], self.ed['mods'])]
                # mark status for removal from dictionary
                remove_list.append(status)

        # remove status effects marked for removal
        for status in remove_list:
            del self.ed['status'][status]

    def dump(self):
        print(self.ed)

    def __repr__(self):
        string = json.dumps(self.ed)
        return string
