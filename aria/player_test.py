#!/usr/bin/env python3

from player import player 

def main():
    print("Creating player name=John class=knight")
    p1 = player('Bobby', 'knight')
    print("Player info:")
    p1.dump()
    print("Adding 1000 xp")
    p1.xp_incr(1000)
    print("Player info:")
    p1.dump()
    print("Inflict damage=20 on player using move=claw")
    p1.damage('claw', 20)
    print("Player info:")
    p1.dump()

if __name__ == '__main__':
    main()
