#!/usr/bin/env python3

# aria_server.py

import random
import socket
import select
import struct
import json
import time
import re
import os
import traceback
import sys
import pwd

from game import game

# Network functions
def marshal(socket, message):
    length = str(len(message))
    combined = length + '!' + message
    socket.sendall(combined.encode('utf-8'))

def unmarshal(socket):
    buf = ''
    while '!' not in buf:
        d = socket.recv(1)
        d = d.decode('utf-8')
        buf += d

    length = buf[0:len(buf)-1]
    data = socket.recv(int(length))
    while(len(data) < int(length)):
        data += socket.recv(int(length))

    data = data.decode('utf-8')

    return data

def send_name(port, name):
    ''' Send UDP packet with server info to name server at http://catalog.cse.nd.edu:9097 '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addrinfo = socket.getaddrinfo('catalog.cse.nd.edu', 9097)
    host_info = addrinfo[0][4]

    info = {}
    info['type'] = 'game'
    info['owner'] = pwd.getpwuid(os.getuid())[0]
    info['port'] = port
    info['project'] = name

    message = json.dumps(info).encode('utf-8')

    sock.sendto(message, host_info)

def main():
    # initialize game
    game_id = random.randint(1000000, 9999999)
    g = game(game_id)

    # socket creation
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.setblocking(0)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    s.bind(('', 0))
    s.listen()
    print('Listening on port', s.getsockname()[1])

    sock_list = [s] # list for select operation (concurrency)
    
    send_name(s.getsockname()[1], 'aria-game') # update name server (first time)
    update_time = time.time() # use for timekeeping for sending name server update


    # conditions used to reset server once a game session has been forked
    new_game = False
    forked = False
    start = False

    # accept loop
    while(True):

        if new_game:
            # re-initialize game
            game_id = random.randint(1000000, 9999999)
            g = game(game_id)
            new_game = False

        curr_time = time.time()

        # update name server every min
        if (curr_time - update_time) > 60:
            send_name(s.getsockname()[1], 'aria-game')
            #print('Sent update to name server')
            update_time = time.time()

        read_list, write_list, err_list = select.select(sock_list, [], [], 0.5)

        # connection loop
        for so in read_list:

            if so is s and not start:
                conn, addr = so.accept()
                print("connection")
                sock_list.append(conn)

            else:
                resp = {'result' : 'success'}

                try:
                    # Get request JSON
                    client_request = unmarshal(so)
                    if client_request is None: # connection closed by client
                        so.close()
                        g.remove_player(so)
                        sock_list.remove(so)
                        continue

                    # Attempt to parse JSON
                    request = json.loads(client_request)
                    #print(request)
                    
                    try:
                        player = g.gd['players'][so]
                    except:
                        pass 


                    # Execute requested method
                    # Broadcast messages are handled internally - see game.py, player.py, entity.py
                    if request['method'] == 'login':
                        #print("login")
                        g.add_player(so, request['name'], request['class'])
                
                    elif request['method'] == 'move' and start:
                        #print("move")
                        if g.gd['players'][so].pd['leader'] == True: # only leader allowed to request movement of party
                            g.move_party(request['arg'])
                
                    elif request['method'] == 'action' and start:
                        #print("action")
                        g.execute_move(request['arg'], player)	

                    elif request['method'] == 'start':
                        #print("start")
                        if g.gd['players'][so].pd['leader'] == True and forked == False: # only leader allowed to start game session (once)
                            # fork
                            pid = os.fork()
                            
                            # parent - reset game session
                            if pid > 0:
                                for sock in g.gd['players'].keys():
                                    sock_list.remove(sock)
                                del g
                                new_game = True
                            
                            # child - continue playing game session
                            else:
                                start = True
                                forked = True
                                g.broadcast('The game has started. Best of luck, adventurers!\n')
                                sock_list = g.gd['players'].keys()
                                enemy_move_time = time.time()
                    else:
                        continue


                except Exception as ex:
                    #traceback.print_exception(*sys.exc_info())
                    continue

            # Additional game session logic (if game has started)
            if start:
                # - upate difficulty scale (based on average level of the party)
                g.scale()

                # - check for defeated enemies and players
                # - if leader is defeated, new leader is chosen
                g.check_enemies()
                g.check_players()

                # - check player and enemy status (effects)
                check_list = list(g.gd['players'].values()) + g.gd['enemies']
                for entity in check_list:
                    entity.status_check()

                # - send updates on player and enemy status
                g.update_player_status()
                g.update_enemy_status()

                # win check
                if g.gd['win'] == True:
                    g.broadcast('The final boss has been vanquished. Congratulations, and thank you for playing!\n')
                    time.sleep(5)
                    for x in sock_list:
                        x.close()
                    return 

                # defeat check
                if g.check_defeat() == True:
                    g.broadcast('By the goddess, all players have been defeated. Who will save us now?\n')
                    time.sleep(5)
                    for x in sock_list:
                        x.close()
                    return

                # enemy movement - choose random enemy and random move, attempt to execute
                if (time.time() - enemy_move_time) > random.choice(range(20, 30)) and g.gd['enemies']:
                    enemy_to_move = random.choice(g.gd['enemies'])
                    random_move = random.choice(list(enemy_to_move.ed['moves'].keys()))
                    g.execute_move(random_move, enemy_to_move)
                    enemy_move_time = time.time()


if __name__ == '__main__':
    main()
