#!/usr/bin/env python3

from entity import entity 

def main():
    print('Creating entity type=demon_king scale=10')
    e = entity('demon_king', 10)
    print('Entity info:')
    e.dump()
    print('Inflict damage=120 on entity using move=multislash')
    print(e.damage('multislash', 120))

    print('Entity info:')
    e.dump()

    print('Attempt to use move=Vairocana')
    move, msg = e.move_check('Vairocana')
    print(msg)

    print('Entity info:')
    e.dump()

    print('Attempt to use move=strike')
    move, msg = e.move_check('strike')
    print(msg)

    print('Applying status move=miasma')
    print(e.apply_status('miasma'))

    print('Entity info:')
    e.dump()

if __name__ == '__main__':
    main()
