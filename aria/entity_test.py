#!/usr/bin/env python3

from entity import entity 

def main():
    print('Creating entity type=demon_king scale=10')
    e = entity('demon_king', 10)
    print('Entity info:')
    e.dump()
    print('Inflict damage=120 on entity using move=multislash')
    hit, dmg = e.damage('multislash', 120)
    if hit:
        print(f'Dealt {dmg} damage to entity')
    else:
        print('Attack missed')
    print('Entity info:')
    e.dump()

    print('Attempt to use move=Vairocana')
    move = e.move('Vairocana')
    if move:
        print('Move success')
    else:
        print('Failed to perform move')

    print('Entity info:')
    e.dump()

    print('Attempt to use move=Vairocana')
    move = e.move('Vairocana')
    if move:
        print('Move success')
    else:
        print('Failed to perform move')

if __name__ == '__main__':
    main()
