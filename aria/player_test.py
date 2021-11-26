#!/usr/bin/env python3

from player import player 

def main():
    print('Creating player name=John class=knight')
    p1 = player('Bobby', 'knight')
    print('Player info:')
    p1.dump()
    print('Adding 1000 xp')
    p1.xp_incr(1000)
    print('Adding 2000 xp')
    p1.xp_incr(2000)
    print('Adding 5000 xp')
    p1.xp_incr(5000)

    print('Player info:')
    p1.dump()
    print('Inflict damage=20 on player using move=claw')
    hit, dmg = p1.damage('claw', 20)
    if hit:
        print(f'Dealt {dmg} damage to player')
    else:
        print('Attack missed')
    print('Player info:')
    p1.dump()

    print('Attempt to use move=strike')
    move = p1.move('strike')
    if move:
        print('Move success')
    else:
        print('Failed to perform move')

    print('Player info:')
    p1.dump()

    print('Attempt to use move=strike')
    move = p1.move('strike')
    if move:
        print('Move success')
    else:
        print('Failed to perform move')


if __name__ == '__main__':
    main()
