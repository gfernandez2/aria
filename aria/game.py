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
        # if full, reject
        if len(self.gd['players']) == 4:
            return self.broadcast('Player {name} can\'t join! There are currently 4 players in the party.\n')

        self.gd['players'][socket] = player(name, pclass)
        
        # test if first player, set to leader
        if len(self.gd['players']) == 1:
            self.gd['players'][socket].pd['leader'] = True

        return self.broadcast(f'Player {name} successfully joined the party. Welcome!\n')


    def remove_player(self, socket):
        del self.gd['players'][socket]
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
        resp = dict()
        resp['msg_type'] = "announce"

        # cannot move if enemies at current location
        if self.gd['enemies']:
            return self.broadcast('Your party cannot move! There are enemies still present in the room.\n')

        curr_loc = self.gd['location']
        mod_loc = [0, 0] # stores modifications to make to location
        direction = direction.lower()
        if direction == 'n' and 0 <= curr_loc[0] - 1:
            mod_loc[0] -= 1
        elif direction == 'w' and 0 <= curr_loc[1] - 1:
            mod_loc[1] -= 1
        elif direction == 'e' and curr_loc[1] + 1 < G.DUNGEON_SIZE:
            mod_loc[1] += 1
        elif direction == 's' and curr_loc[0] + 1 < G.DUNGEON_SIZE:
            mod_loc[1] += 1
        else:
            return self.broadcast('There\'s no door there! Confused, your party stays where it is.\n')

        new_loc = [sum(i) for i in zip(curr_loc, mod_loc)]

        if self.gd['dungeon'][new_loc[0]][new_loc[1]]['boss'] == True and self.gd['keys'] < G.KEYS_REQUIRED:
            return self.broadcast('You cannot go there just yet! You must collect more keys from enemies.\n')

        self.gd['location'] = new_loc

        # spawn enemies at new location
        self.spawn_enemies()

        return self.broadcast('Your party cautiously walks into the neighboring room.\n')

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

    # attempts to execute move
    # requester - player or entity obj
    # for now, single targets are chosen at random
    def execute_move(self, move, requester):
        # check if move can be executed
        proceed, msg = requester.move_check(move)
        if not proceed:
            return self.broadcast(msg)

        # unique handling of Vairocana - evokes random move from globals.py
        if move == 'Vairocana':
            while move == 'Vairocana':
                move = random.choice(G.MOVES.keys())
            targets = players
        else:
            # get move info
            mi = G.MOVES[move]
            targets = []
            players = self.gd['players'].values()
            enemies = self.gd['enemies']

            # determine target
            # self targets are only status-type moves
            if mi['target'] == 'self':
                return requester.apply_status(move)
            elif mi['target'] == 'single':
                if mi['side'] == 'player':
                    targets.append(random.choice(players))
                elif mi['side'] == 'enemy':
                    targets.append(random.choice(enemies))
            elif mi['target'] == 'all':
                if mi['side'] == 'player':
                    targets = players
                elif mi['side'] == 'enemy':
                    targets = enemies

        # apply move onto target(s)
        mtype = mi['type']
        scale = mi['scale']
        stats = requester.get_stats()
        resp = ''
        for target in targets:
            if mtype == 'physical':
                msg = target.damage(move, int(stats[1] * (scale/100)))
            elif mtype == 'magic':
                msg = target.damage(move, int(stats[3] * (scale/100)))
            elif mtype == 'status':
                msg = target.apply_status(move)
            elif mtype == 'heal':
                msg = target.heal(move)
            
            resp += msg + '\n'

        # remove last newline
        resp = resp[:-1]

        return self.broadcast(resp)

    # checks for enemies that are defeated
    # removes defeated enemies and awards players xp
    # xp calculated by:
    # random int from [ (sum of enemy stats), (sum of enemy stats) * speed stat of player]
    def check_enemies(self):
        removal = []
        # check for defeated enemies
        for enemy in self.gd['enemies']:
            #print('Test')
            if enemy.ed['health'] == 0:
                #print('Defeated enemy detected')
                removal.append(enemy)
                stat_sum = sum(enemy.ed['stats'])
                # distribute xp reward
                for player in self.gd['players'].values():
                    pstats = player.get_stats()
                    player.xp_incr(random.randint(stat_sum, stat_sum * pstats[5]))

        # remove enemies
        for enemy in removal:
            self.gd['enemies'].remove(enemy)

    # check for defeated status     
    def check_defeat(self):
        for p in self.gd['players'].values():
            if p.get_health() > 0:
                return False

        return True

    # simple broadcast for a live feed message
    # message assumed to be a string
    def broadcast(self, message):
        resp = dict()
        resp['msg_type'] = 'broadcast'
        resp['msg'] = message
        payload = json.dumps(resp)
        # send message to all player sockets
        for socket in self.gd['players'].keys():
            try:
                length = str(len(payload))
                combined = length + '!' + payload
                socket.sendall(combined.encode('utf-8'))
            except Exception:
                continue

        return resp

    def dump(self):
        return self.gd
