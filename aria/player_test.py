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
    print(p1.damage('claw', 30))
    
    print('Player info:')
    p1.dump()

    print('Attempt to use move=strike')
    move, msg = p1.move_check('strike')
    print(msg)

    print('Attempt to use move=strike')
    move, msg = p1.move_check('strike')
    print(msg)

    print('Attempt to use move=Vairocana')
    move, msg = p1.move_check('Vairocana')
    print(msg)

    print('Attempt to use move=maelstrom')
    move, msg = p1.move_check('maelstrom')
    print(msg)

    print('Applying status move=growl')
    print(p1.apply_status('growl'))

    print('Player info:')
    p1.dump()

    print('Applying move=heal')
    print(p1.heal('heal'))

    print('Player info:')
    p1.dump()

if __name__ == '__main__':
    main()
