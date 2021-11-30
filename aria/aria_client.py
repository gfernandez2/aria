import curses
import os
import socket
import sys
import select
import time
from curses import wrapper

import network_client as net
import graphics as g


def main(stdscr):

	# connect to game server	
	socket = net.connect(sys.argv[1], sys.argv[2])
	sockArr = []
	sockArr.append(socket)

	# launch curses window
	rows, cols = g.get_window_size()
	g.launch_graphics(rows, cols)

	ackArr = []

	# main loop
	# we do three things on each loop iteration:
	#
	# 1. listen for messages from the game server
	#	 we listen using "select," which we make (virtually) non-blocking by
	#	 giving it a really short timeout. if there is a socket waiting to be
	# 	 read, we do so, and perform the appropriate logic.
	#
	# 2. listen for keyboard input
	#	 we set getch() as non-blocking, and construct a string. after "return"
	# 	 is detected, we perform the appropriate logic.
	while True:

		r, w, e = select.select(sockArr, [], [], 0.05)

		for sock in r:
			data = net.recv(sock)

			try:
				act = data["type"]
			except:
				# dosomething
				pass

			if act == "update":
				if data["window"] == "pStatus":
					g.update_pStatus(data)# split by fields?

				elif data["window"] == "eStatus":
					g.update_eStatus(data)
				
				elif data["window"] = "graphics":
					#dosomething
					pass

			elif act == "broadcast":
				g.update_feed(data["message"]) 

					
		res = g.get_input()
		if res is not None:
			# todo: try
			net.send(socket, str(res))

				
	
	# need a clean disconnect sequence
	#res = net.send(socket, "disconnect")
	curses.endwin()


curses.wrapper(main)
