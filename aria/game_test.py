#!/usr/bin/env python3

from game import game
from entity import entity
import random
import time

def main():
    # Initialize game
    game_id = random.randint(1000000, 9999999)
    print(f'Initializing game with id={game_id}')
    g = game(game_id)
    print('Game data:')
    gd = g.dump()
    print(gd)

    # Add players
    # for testing uses strings instead of socket objects
    print('Adding players')
    g.add_player('player1', 'Alice', 'knight')
    g.add_player('player2', 'Bobby', 'mage')
    g.add_player('player3', 'Candice', 'healer')
    g.add_player('player4', 'Dan', 'tank')

    players = g.get_players()

    print('Spawning enemies')
    for _ in range(10):
        g.spawn_enemies()
    print('Game data:')
    gd = g.dump()
    print(gd['enemies'])

    print('Leveling players')
    for player in players.values():
        player.xp_incr(50000)

    print('Game data:')
    gd = g.dump()
    print(gd['players'])

    print('Executing move=miasma from player2')
    success = g.execute_move('miasma', players['player2'])
    if not success:
        print('Move success')
    else:
        print('Move failure')
    print('Game data:')
    gd = g.dump()
    print(gd['enemies'])
    
    print('Executing move=multislash from player1:')
    success = g.execute_move('multislash', players['player1'])
    if not success:
        print('Move success')
    else:
        print('Move failure')

    print('Game data:')
    gd = g.dump()
    print(gd['enemies'])

    print('Executing move=manastorm from player2:')
    success = g.execute_move('manastorm', players['player2'])
    if not success:
        print('Move success')
    else:
        print('Move failure')

    print('Game data:')
    gd = g.dump()
    print(gd['enemies'])

    print('Checking defeated enemies')
    g.check_enemies()

    print('Game data:')
    gd = g.dump()
    print(gd['players'])
    print(gd['enemies'])







if __name__ == '__main__':
    main()
