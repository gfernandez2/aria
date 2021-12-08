# Aria
A text-based multiplayer RPG utilizing a client-server architecture, written in Python.

Final Project assigment for [CSE 40771 Distributed Systems](https://distsys-fa21.github.io).

# Team Members
- Gerry Fernandez (gfernan2)
- Harry Snow (hsnow)

# Story
Reconnaissance reports from the garrison indicate that the **Holy Lyre** has been located 
deep in the clutches of an enemy dungeon, said to be in the control of a Demon King. 
Enemy control of the Holy Lyre risks the destruction of the world, adventurer. 
By **Sacred Order** of our **Queen of Sancta**, your orders are to 
infiltrate the dungeon, recover the **Holy Lyre**, and make it back safely.
May the protection of the goddess be with you.

# Features
- A text-based interface utilizing the `curses` library
- Radomized dungeon and enemy generation
- Player progression
- Player classes:
  - `knight` with moves `strike`, `guard`, and `multislash`
  - `mage` with moves `blast`, `miasma`, and `manastorm`
  - `healer` with moves `heal`, `enhance`, and `refresh`
  - `tank` with moves `bash`, `shield`, and `bastion`
- An ATB-like combat system

# Usage
- To run the server, run `python3 aria_server.py` without arguments.
- To run a client, run `python3 aria_client.py` without arguments. If there are issues with the interface,
it could be the case that your terminal window is too small.

# Start-Up Guide
- Upon connecting to the server with the client, the possible commands are:
  - `login <name> <class>`: request to join the pending game session with a chosen name and class.
  If you are the first player to join a pending game session, then you are made the party leader.
  - `start game`: request to start the game. This can only be made by the party leader.
  - `move <direction>`: request to move the party in a cardinal direction {`n`, `w`, `e`, `s`}.
  Only the party leader can request movement.
  - `action <move>`: request to execute a move from your moveset, which depends on the class you
  have chosen.

# Notice
- Due to an oversight in development, it seems that the client does not work on Windows or Linux.
It was developed on and works fine on MacOS, and so we encourage that the project be tested on MacOS for now.
If you know how to fix this issue, please let us know.
