import curses
import os
import sys
from curses import wrapper

import network_client as net

# holds all 5 dynamic windows
windows = []
# the live feed is scrollable, this holds it's current line
feedRow = 3
# holds the current xPos of the string being constructed on input
xPos = 3
# the input string
cmd = ""
# size of the terminal window
rows = 0
cols = 0

def get_window_size():
	screen = curses.initscr()
	rows, cols = screen.getmaxyx()
	curses.endwin()
	return rows, cols


# initializes all curses windows
def launch_graphics(r, c):
	global rows, cols
	rows = int(r)
	cols = int(c)

	curses.echo()
	
	# format: newwin(#rows, #cols, ycoord, xcoord)

	# winx - the "title" bar at the top	
	# this window is static 
	# position of title is hardcoded atm (should be proportionally centered)
	winx = curses.newwin(1, cols, 0, 0)
	winx.addstr(0, int(cols/2) - 7, "DUNGEON ESCAPE")
	winx.refresh()

	# win0 - the player prompt
	# nodelay - sets getch() to non-blocking 
	win0 = curses.newwin(int(rows/6), int(cols/2), int((5*rows)/6)+2, 0) 
	win0.nodelay(True)

	# win1 - the game feed
	# scrreg - top and bottom of scrolling region
	win1 = curses.newwin(int((5*rows)/6)-1,int(cols/3), 1, 0)
	win1.addstr(1, 3, "LIVE FEED")
	win1.scrollok(True)
	win1.setscrreg(3, int((5*rows)/6)-2)
	win1.refresh()

	# win2 - the player status area
	win2 = curses.newwin(int(rows/6), int(cols/2), int((5*rows)/6)+2, int(cols/2)+2)

	# win3 - graphics area
	win3 = curses.newwin(int((4*rows)/6)-1, int((2*cols)/3), 1, int(cols/3)+2)

	# win4 - enemy status area
	win4 = curses.newwin(int(rows/6), int(cols/2), int((4*rows)/6)+2, int(cols/2)+2) 
	
	windows.append(win0)
	windows.append(win1)
	windows.append(win2)
	windows.append(win3)
	windows.append(win4)


def get_input():
	global xPos, cmd
	c = windows[0].getch(3, xPos)
	
	if c == 10:
		res = cmd
		cmd = ""
		xPos = 3	
		windows[0].clear()
		windows[0].refresh()	
		return res

	elif c == -1:
		return None

	# todo: handle backspace

	else:
		cmd = cmd + chr(c)
		xPos += 1
		windows[0].clear()
		windows[0].addstr(3, 3, cmd)
		windows[0].refresh()
		return None
			

# uses win1
def update_feed(s):
	global feedRow
	feedRow += 2
	if feedRow >= (5*rows/6)-1:
		feedRow -= 2
		windows[1].scroll(2)
	windows[1].addstr(feedRow, 3, str(s))
	windows[1].refresh()	


def update_pStatus(s):
	line1 = "HP: " + str(s["hp"])
	line2 = "Level: " + str(s["level"]) + "   " + "XP: " + str(s["xp"])
	line3 = "keys: " + str(s["keys"])
	windows[2].clear()
	windows[2].addstr(3, 3, line1)
	windows[2].addstr(4, 3, line2)
	windows[2].addstr(5, 3, line3) 
	windows[2].refresh()	


# for now just prints the string input
# todo: will need to access local graphics library
def update_graphics(s):
	windows[3].addstr(3, 3, str(s))
	windows[3].refresh()


# array of jsons? json of jsons?
def update_eStatus(s):
	

