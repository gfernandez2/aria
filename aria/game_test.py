#!/usr/bin/env python3

from game import game 
import random

def main():
    game_id = random.randint(1000000, 9999999)
    print(f'Initializing game with id={game_id}')
    g = game(game_id)
    print('Game data:')
    g.dump()

if __name__ == '__main__':
    main()
