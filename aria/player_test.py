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
    print('Inflict damage=30 on player using move=claw')
    hit, dmg = p1.damage('claw', 30)
    if hit:
        print(f'Dealt {dmg} damage to player')
    else:
        print('Attack missed')
    print('Player info:')
    p1.dump()

    print('Attempt to use move=strike')
    move = p1.move_check('strike')
    if move:
        print('Move success')
    else:
        print('Failed to perform move')

    print('Player info:')
    p1.dump()

    print('Attempt to use move=maelstrom')
    move = p1.move_check('maelstrom')
    if move:
        print('Move success')
    else:
        print('Failed to perform move')

    print('Applying status move=growl')
    success = p1.apply_status('growl')
    if success:
        print('Move success')
    else:
        print('Move failure')

    print('Player info:')
    p1.dump()

    print('Applying move=heal')
    heal = p1.heal('heal')

    print(f'Healed {heal} hp')
    
    print('Player info:')
    p1.dump()

if __name__ == '__main__':
    main()
