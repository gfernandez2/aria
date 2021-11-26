# game.py
# Encapsulates game session data and functions

import json
import random

import globals as G

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

    # check for defeated status     
    def check_defeat(self):
        for p in self.gd['players'].values():
            if p['health'] > 0:
                return False

        return True

    def dump(self):
        print(self.gd)

