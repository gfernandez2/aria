import curses
import os
import sys
from curses import wrapper

import network_client as net
import monster_art as art

# holds all 5 dynamic windows
windows = []
# the live feed is scrollable, this holds it's current line
feedRow = 1
# holds the current xPos of the string being constructed on input
xPos = 5
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
    win0 = curses.newwin(int(rows/6), int(cols/3), int((5*rows)/6), 0) 
    win0.box()
    win0.refresh()
    win0b = win0.derwin(int(rows/6)-2, int(cols/3)-2, 1, 1)
    win0b.nodelay(True)
    win0b.addstr(2, 1, ">>> ")
    win0b.refresh()

    # win1 - the game feed
    # scrreg - top and bottom of scrolling region
    win1 = curses.newwin(int((5*rows)/6)-1, int(cols/2), 1, 0)
    win1.box()
    win1.refresh()
    win1b = win1.derwin(int((5*rows)/6)-3, int(cols/2)-2, 1, 1)
    win1b.addstr(0, 0, "LIVE FEED")
    win1b.scrollok(True)
    win1b.setscrreg(3, int((5*rows)/6)-5)
    win1b.refresh()

    # win2 - the player status area
    win2 = curses.newwin(int(rows/6), int(cols/3), int((5*rows)/6), int(cols/3))
    win2.box()
    win2.refresh()
    win2b = win2.derwin(int(rows/6)-2, int(cols/3)-2, 1, 1)
    win2b.addstr(0, 1, "PLAYER STATUS")
    win2b.addstr(2, 1, "Level: ")
    win2b.addstr(3, 1, "HP: ")
    win2b.addstr(4, 1, "Keys: ")
    win2b.refresh()

    # win3 - graphics area
    win3 = curses.newwin(int((5*rows)/6)-1, int(cols/2), 1, int(cols/2))
    win3.box()
    win3.refresh()
    win3b = win3.derwin(int((5*rows)/6)-3, int(cols/2)-2, 1, 1)
    win3b.addstr(14, 50, art.aria)
    win3b.refresh()

    # win4 - enemy status area
    win4 = curses.newwin(int(rows/6), int(cols/3), int((5*rows)/6), int(2*cols/3)) 
    win4.box()
    win4.refresh()
    win4b = win4.derwin(int(rows/6)-2, int(cols/3)-2, 1, 1)
    win4b.refresh()
    
    windows.append(win0b)
    windows.append(win1b)
    windows.append(win2b)
    windows.append(win3b)
    windows.append(win4b)


def get_input():
    global xPos, cmd
    c = windows[0].getch(2, xPos)

    if c == -1:
        return None
   
    # "enter" 
    elif c == 10:
        res = cmd
        cmd = ""
        xPos = 5    
        windows[0].clear()
        windows[0].addstr(2, 1, ">>> ")
        windows[0].refresh()    
        return res

    # "backspace"
    elif c == 127:
        if len(cmd) > 0:
            cmd = cmd[0:len(cmd)-1]
            xPos -= 1
            windows[0].clear()
            windows[0].addstr(2, 1, ">>> ")
            windows[0].addstr(2, 5, cmd)
            windows[0].refresh()
        return None

    # any other character
    # todo? ignore non a-z
    else:
        cmd = cmd + chr(c)
        xPos += 1
        windows[0].clear()
        windows[0].addstr(2, 1, ">>> ")
        windows[0].addstr(2, 5, cmd)
        windows[0].refresh()
        return None
            

def update_feed(s):
    global feedRow

    if s.count("\n") >= 2:
        feedRow += 2

    feedRow += 2
    if feedRow >= (5*rows/6)-5:
        feedRow -= 2
        windows[1].scroll(2)
    windows[1].addstr(feedRow, 0, str(s))
    windows[1].refresh()    


# placeholders, but general idea. values can be json fields, in an array, etc.
# important - even if only updating one value, server needs to send them all
def update_pStatus(s):
    line1 = "HP: " + str(s["curr_health"]) + "/" + str(s["max_health"])
    line2 = "Level: " + str(s["level"]) + "   XP: " + str(s["xp"])
    line3 = "Keys: " + str(s["keys"])
    windows[2].clear()
    windows[2].addstr(0, 1, "PLAYER STATUS")
    windows[2].addstr(2, 1, line1)
    windows[2].addstr(3, 1, line2)
    windows[2].addstr(4, 1, line3) 
    windows[2].refresh()    


# expects the name of the enemy from the server, will access the corresponding 
# art from local file
def update_graphics(s):

    if len(s) == 0:
        return

    enemyList = []
    for enemy in s:
        enemyList.append(enemy["class"])

    enemy = str(enemyList[0])

    windows[3].clear()
    if enemy == "golem":
        windows[3].addstr(1, 1, art.golem) 
    elif enemy == "orc":
        windows[3].addstr(1, 1, art.orc)
    elif enemy == "lich":
        windows[3].addstr(1, 1, art.lich)
    elif enemy == "ghoul":
        windows[3].addstr(1, 1, art.ghoul)
    elif enemy == "slime":
        windows[3].addstr(1, 1, art.slime)
    elif enemy == "goblin":
        windows[3].addstr(1, 1, art.goblin)
    elif enemy == "troll":
        windows[3].addstr(1, 1, art.troll)
    windows[3].refresh()


# i think it will need the name of the monster and its hp (and multiple for multiple monsters)
# similar to update player status
# placeholder/example access methodolgy
# todo: logic for when there's no enemy - should clear
def update_eStatus(s):

    line1 = ""
    line2 = ""
    line3 = ""

    for enemy in s:
        length = len(str(enemy["class"]))
        line1 += str(enemy["class"]) + (20-length)*" "
        length = len(str(enemy["name"]))
        line2 += str(enemy["name"]) + (20-length)*" "
        length = len("HP: " + str(enemy["curr_health"]) + "/" + str(enemy["max_health"]))
        line3 += "HP: " + str(enemy["curr_health"]) + "/" + str(enemy["max_health"]) + (20-length)*" "
    
    windows[4].clear()
    windows[4].addstr(0, 1, "ENEMY STATUS")
    windows[4].addstr(2, 1, line1)
    windows[4].addstr(3, 1, line2)
    windows[4].addstr(4, 1, line3)
    windows[4].refresh()

