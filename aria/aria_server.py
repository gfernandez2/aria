#!/usr/bin/env python3

# aria_server.py

import random
import socket
import select
import struct
import json
import time
import re

from game import game

HOST = ''
PORT = 0

# Network functions
def marshal(socket, message):
    length = str(len(message))
    combined = length + '!' + message
    socket.sendall(combined.encode('utf-8'))

def unmarshal(socket):
    buf = ''
    while '!' not in buf:
        d = sock.recv(1)
        d = d.decode('utf-8')
        buf += d

    length = buf[0:len(buf)-1]

    data = socket.recv(int(length))
    while(len(data) < int(length)):
        data += sock.recv(int(length))

    data = data.decode('utf-8')

    return data

def send_name(port, name):
    ''' Send UDP packet with server info to name server at http://catalog.cse.nd.edu:9097 '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addrinfo = socket.getaddrinfo('catalog.cse.nd.edu', 9097)
    host_info = addrinfo[0][4]

    info = {}
    info['type'] = 'game'
    info['owner'] = 'gfernan2'
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
    
    #send_name(s.getsockname()[1], 'aria') # update name server (first time)
    update_time = time.time() # use for timekeeping for sending name server update

    # accept loop
    while(True):

        # Additional game session logic could go here
        # - check for defeated enemies
        # - check player and enemy statuses

        curr_time = time.time()

        # update name server every min
        if (curr_time - update_time) > 60:
            #send_name(s.getsockname()[1], project_name)
            #print('Sent update to name server')
            update_time = time.time()

        read_list, write_list, err_list = select.select(sock_list, [], [], 0.5)

        # connection loop
        for so in read_list:

            #print('Processing socket', so.getsockname()[1])

            if so is s:
                conn, addr = so.accept()
                #so.setblocking(0)
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

                    player = g.gd['players'][so]

                    # Execute requested method
                    # Broadcast messages are handled internally - see game.py, player.py, entity.py
                    if request['method'] == 'login':
                        g.gd.add_player(so, request['name'], request['class'])
                
                    elif request['method'] == 'move':
                        if g.gd['players'][so]['leader'] == True:
                            g.move_party(request['arg'])
                
                    elif request['method'] == 'action':
                        g.execute_move(request['arg'], player)
                            
                # granular exception handling
                except KeyError as ex:
                    resp['result'] = 'failure'
                    resp['exception'] = 'KeyError'
                    resp['message'] = str(ex).strip("'")

                except re.error as ex:
                    resp['result'] = 'failure'
                    resp['exception'] = 're.error'
                    resp['message'] = str(ex).strip("'")

                except TypeError as ex:
                    resp['result'] = 'failure'
                    resp['exception'] = 'TypeError'
                    resp['message'] = str(ex).strip("'")

                except ValueError as ex:
                    resp['result'] = 'failure'
                    resp['exception'] = 'ValueError'
                    resp['message'] = str(ex).strip("'")


if __name__ == '__main__':
    main()
