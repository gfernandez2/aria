#!/usr/bin/env python3

import curses
import os
import socket
import sys
import select
import time
import json
import pwd
import http.client

from curses import wrapper

import network_client as net
import graphics as g


def main(stdscr):
    #screen = curses.initscr()

    '''
    # connect to game server    
    socket = net.connect(sys.argv[1], sys.argv[2])
    sockArr = []
    sockArr.append(socket) 
    ''' 
    # connect to game server
    c = http.client.HTTPConnection("catalog.cse.nd.edu", 9097)
    c.connect()
    c.request("GET", "/query.json")
    response = c.getresponse()
    c.close()
    
    matches = []
    try:
        for item in json.loads(response.read()):
            if "project" in str(item):
                if item['type'] == "game" and "aria" in str(item['project']):
                    matches.append([item['address'], item['port'], item['lastheardfrom']])
    except:
        print("not found")
        return
    
    matches.sort(key=lambda x: x[2], reverse=True)
    socket = net.connect(matches[0][0], matches[0][1])
    sockArr = []
    sockArr.append(socket)
    
    # launch curses window
    rows, cols = g.get_window_size()
    g.launch_graphics(rows, cols)

    # client logical clock
    clock = -1
    
    # valid classes
    classes = ["knight", "mage", "healer", "tank"]
 
    # get username and class, and login to game
    while True:
        res = g.get_input()
        if res:
            if len(res.split()) == 3:
                if str(res.split()[0]) == "login" and len(res.split()[1]) < 10 and str(res.split()[2]) in classes: 
                    net.send_login(socket, str(res))
                    break

    # main loop
    # we do two things on each loop iteration:
    #
    # 1. listen for messages from the game server
    #    we listen using "select," which we make (virtually) non-blocking by
    #    giving it a really short timeout. if there is a socket waiting to be
    #    read, we do so, and perform the appropriate logic.
    #
    # 2. listen for keyboard input
    #    we set getch() as non-blocking, and construct a string. after "return"
    #    is detected, we perform the appropriate logic.
    while True:

        r = select.select(sockArr, [], [], 0.01)[0]

        for sock in r:        
            data = net.recv(sock)
            data = json.loads(data)

            resp = data["msg_type"]
                
            if resp == "update":
                if data["field"] == "pStatus":
                    g.update_pStatus(data["values"])                 
                   
                elif data["field"] == "eStatus":
                    g.update_eStatus(data["values"])
                    g.update_graphics(data["values"])             
        
            elif resp == "broadcast":
                if int(data["clock"]) > clock: 
                    g.update_feed(data["msg"]) 
                    clock = int(data["clock"])
                    
        res = g.get_input()
        if res:
            net.send(socket, str(res))
                   
    curses.endwin()

#if __name__ == "__main__":
#    main()
curses.wrapper(main)

