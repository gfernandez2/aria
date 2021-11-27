# game.py
# Encapsulates game session data and functions

import json
import random

import globals as G
from player import player
from entity import entity

class game:

    def __init__(self, game_id, game_data=None):
        if game_data:
            self.gd = game_data
        else:
            self.gd = dict()
            self.gd['id'] = game_id
            self.gd['players'] = dict() # maps socket to player object
            
            # dungeon generation
            self.gd['dungeon'] = [[dict({'boss' : False}) for i in range(G.DUNGEON_SIZE)] for j in range(G.DUNGEON_SIZE)]
            self.generate_dungeon()

            # party location generation - can't be same as boss room
            # [row, col]
            # please let me know how to make this more readable
            self.gd['location'] = [random.randrange(0, G.DUNGEON_SIZE), random.randrange(0, G.DUNGEON_SIZE)]
            while self.gd['dungeon'][self.gd['location'][0]][self.gd['location'][1]]['boss'] == True:
                self.gd['location'] = [random.randrange(0, G.DUNGEON_SIZE), random.randrange(0, G.DUNGEON_SIZE)]
            
            self.gd['keys'] = 0 # keys necessary to access boss room 
            self.scale() # set scaling factor for dungeon difficulty

            self.gd['enemies'] = [] # holds enemies at current location

    def add_player(self, socket, name, pclass):
        # TODO: loading pre-existing player data
        if len(self.gd['players']) == 4:
            return False

        self.gd['players'][socket] = player(name, pclass)
        return True

    def generate_dungeon(self):
        for i in range(G.DUNGEON_SIZE):
            for j in range(G.DUNGEON_SIZE):
                self.gd['dungeon'][i][j]['difficulty'] = random.choices([1, 2, 3], weights=[75, 15, 10])[0]

        # set boss room location
        self.gd['dungeon'][random.randrange(0, G.DUNGEON_SIZE)][random.randrange(0, G.DUNGEON_SIZE)]['boss'] = True
                
    # sets scaling factor to average lvl of players
    def scale(self):
        if self.gd['players']:
            lvl_sum = sum(p['level'] for p in self.gd['players'].values())
            self.gd['scale'] = lvl_sum/len(self.gd['players'])
        else:
            self.gd['scale'] = 1

    # attempt to move party to new room
    # dir - n, w, e, s
    def move_party(self, direction):
        # cannot move if enemies at current location
        if self.gd['enemies']:
            return False

        curr_loc = self.gd['location']
        mod_loc = [0, 0] # stores modifications to make to location
        direction = direction.lower()
        if direction == 'n':
            if 0 <= curr_loc[0] - 1:
                mod_loc[0] -= 1
        elif direction == 'w':
            if 0 <= curr_loc[1] - 1:
                mod_loc[1] -= 1
        elif direction == 'e':
            if curr_loc[1] + 1 < G.DUNGEON_SIZE:
                mod_loc[1] += 1
        elif direction == 's':
            if curr_loc[0] + 1 < G.DUNGEON_SIZE:
                moc_loc[1] += 1
        else:
            return False

        new_loc = [sum(i) for i in zip(curr_loc, mod_loc)]

        if self.gd['dungeon'][new_loc[0]][new_loc[1]]['boss'] == True and self.gd['keys'] < G.KEYS_REQUIRED:
            return False

        self.gd['location'] = new_loc

        # spawn enemies at new location
        self.spawn_enemies()

        return True

    def spawn_enemies(self):
        curr_loc = self.gd['location']
        curr_room = self.gd['dungeon'][curr_loc[0]][curr_loc[1]]

        boss = curr_room['boss']

        if boss:
            e = entity('demon_king', self.gd['scale'])
            self.gd['enemies'].append(e)
        else:
            difficulty = curr_room['difficulty'] 

            # enemy spawning becomes more frequent with difficulty scaling
            spawn_rate = G.SPAWN_RATE
            spawn_rate += min(100 - spawn_rate, int(self.gd['scale']/10))
            
            # construct enemy pool
            # list of [name, rate] pairs
            possible_enemies = [[e, f['rate']] for e,f in sorted(G.ENEMIES.items()) if f['difficulty'] <= difficulty]
            enemy_names = [i[0] for i in possible_enemies]
            enemy_rates = [i[1] for i in possible_enemies]

            # spawn enemies
            for _ in range(difficulty):
                will_spawn = random.choices([True, False], weights=[spawn_rate, 100 - spawn_rate])[0]
                if will_spawn:
                    chosen_enemy = random.choices(enemy_names, weights=enemy_rates)[0]
                    e = entity(chosen_enemy, self.gd['scale'])
                    self.gd['enemies'].append(e)

    # attempts to execute move requested by socket
    def move(self, socket, move):

    # check for defeated status     
    def check_defeat(self):
        for p in self.gd['players'].values():
            if p['health'] > 0:
                return False

        return True

    def dump(self):
        print(self.gd)
