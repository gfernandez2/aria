import curses
import os
import socket
import sys
import select
import time
import json
from curses import wrapper

import network_client as net
import graphics as g


def main(stdscr):
    #screen = curses.initscr()
    # connect to game server    
    socket = net.connect(sys.argv[1], sys.argv[2])
    sockArr = []
    sockArr.append(socket)

    # launch curses window
    rows, cols = g.get_window_size()
    g.launch_graphics(rows, cols)

    ackArr = []
  
    while True:
        res = g.get_input()
        if res is not None:
            net.send_login(socket, str(res))
            break

    # main loop
    # we do three things on each loop iteration:
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

            try:
                resp = data["msg_type"]
            except:
                # dosomething
                pass
           
            if resp == "update":
                if data["field"] == "pStatus":
                    g.update_pStatus(data["values"])# split by fields?
                 
                elif data["field"] == "eStatus":
                    g.update_eStatus(data["values"])
                    g.update_graphics(data["values"])
                
            
            elif resp == "broadcast":
                g.update_feed(data["msg"]) 

                    
        res = g.get_input()
        if res is not None:
            net.send(socket, str(res))
        
    
    # need a clean disconnect sequence
    #res = net.send(socket, "disconnect")
    curses.endwin()

#if __name__ == "__main__":
#    main()
curses.wrapper(main)

