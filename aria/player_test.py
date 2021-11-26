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
    hit, dmg = p1.damage('claw', 20)
    if hit:
        print(f"Dealt {dmg} damage to player")
    else:
        print("Attack missed")
    print("Player info:")
    p1.dump()

if __name__ == '__main__':
    main()
