import curses
import os
import sys
from curses import wrapper

import network_client as net
import monster_art as art

# holds all dynamic windows
windows = []
win3 = None
# the live feed is scrollable, this holds it's current line
feedRow = 3
# holds the current xPos of the string being constructed on input
xPos = 5
# the input string
cmd = ""
# size of the terminal window
rows = 0
cols = 0
# maps class string sent from server to corresponding ascii art
enemyDict = {
                "slime":art.slime,
                "orc":art.orc,
                "goblin":art.goblin,
                "troll":art.troll,
                "golem":art.golem,
                "ghoul":art.ghoul,
                "lich":art.lich,
                "demon_king":art.demon_king
            }
# keeps track of how many enemies there are in a room (if it changes,
# we need to update the pictures
enemyCount = 0


def get_window_size():
    screen = curses.initscr()
    rows, cols = screen.getmaxyx()
    curses.endwin()
    return rows, cols


# initializes all curses windows
def launch_graphics(r, c):
    global rows, cols, win3
    rows = int(r)
    cols = int(c)

    # let's you see what you're typing
    curses.echo()
    
    # format: newwin(#rows, #cols, ycoord, xcoord)

    # winx - the "title" bar at the top 
    # this window is static 
    winx = curses.newwin(1, cols, 0, 0)
    winx.addstr(0, int(cols/2) - 10, "ARIA - DUNGEON ESCAPE")
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
    win1 = curses.newwin(int((5*rows)/6)-1, int(cols/3), 1, 0)
    win1.box()
    win1.refresh()
    win1b = win1.derwin(int((5*rows)/6)-3, int(cols/3)-2, 1, 1)
    win1b.addstr(0, 0, "LIVE FEED")
    win1b.scrollok(True)
    win1b.idlok(True)
    win1b.setscrreg(2, int((5*rows)/6)-5)
    win1b.refresh()

    # win2 - the player status area
    win2 = curses.newwin(int(rows/6), int(cols/3), int((5*rows)/6), int(cols/3))
    win2.box()
    win2.refresh()
    win2b = win2.derwin(int(rows/6)-2, int(cols/3)-2, 1, 1)
    win2b.addstr(0, 1, "PLAYER STATUS")
    # limit for smaller display size
    try:
        win2b.addstr(2, 1, "Level: ")
        win2b.addstr(3, 1, "HP: ")
        win2b.addstr(4, 1, "Keys: ")
    except:
        win2b.addstr(1, 1, "Level: ")
        win2b.addstr(2, 1, "HP: ")
        win2b.addstr(3, 1, "Keys: ")
    win2b.refresh()

    # win3 - graphics area
    win3 = curses.newwin(int((5*rows)/6)-1, int(2*cols/3), 1, int(cols/3))
    win3.box()
    win3.refresh()
    #win3b = win3.derwin(int((5*rows)/6)-3, int(2*cols/3)-2, 1, 1)
    #win3b.addstr(4, 10, art.aria)
    #win3b.refresh()

    # win4 - enemy status area
    win4 = curses.newwin(int(rows/6), int(cols/3), int((5*rows)/6), int(2*cols/3)) 
    win4.box()
    win4.refresh()
    win4b = win4.derwin(int(rows/6)-2, int(cols/3)-2, 1, 1)
    win4b.refresh()
    
    windows.append(win0b)
    windows.append(win1b)
    windows.append(win2b)
    # for the graphics (art), we will dynamically allocate and destroy windows inside
    # the "win3" block
    graphicsWindows = []
    #graphicsWindows.append(win3b)
    windows.append(graphicsWindows)
    windows.append(win4b)


def get_input():
    global xPos, cmd
    c = windows[0].getch(2, xPos)

    # default when no input
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

    # a-z and space
    elif (c >= 97 and c <= 122) or c == 32:
        cmd = cmd + chr(c)
        xPos += 1
        windows[0].clear()
        windows[0].addstr(2, 1, ">>> ")
        windows[0].addstr(2, 5, cmd)
        windows[0].refresh()
        return None
            

# updates the feed with broadcast messages from the server
def update_feed(s):
    global feedRow

    lines = s.split("\n")
    for line in lines:
        if feedRow < int((5*rows)/6)-5:
            windows[1].addstr(feedRow, 0, str(line))
            feedRow += 1
        else:
            windows[1].scroll(1)
            windows[1].addstr(int((5*rows)/6)-5, 0, str(line))
    try:
        windows[1].addstr(feedRow, 0, "\n")
        feedRow += 1
    except:
        windows[1].scroll(1)
       
    windows[1].refresh()


# gets the hp, level, and keys from server and displays in player status box
def update_pStatus(s):
    line1 = "HP: " + str(s["curr_health"]) + "/" + str(s["max_health"])
    line2 = "Level: " + str(s["level"]) + "   XP: " + str(s["xp"])
    line3 = "Keys: " + str(s["keys"])
    windows[2].clear()
    windows[2].addstr(0, 1, "PLAYER STATUS")
    try:
        windows[2].addstr(2, 1, line1)
        windows[2].addstr(3, 1, line2)
        windows[2].addstr(4, 1, line3) 
    except:
        windows[2].addstr(1, 1, line1)
        windows[2].addstr(2, 1, line2)
        windows[2].addstr(3, 1, line3) 
    windows[2].refresh()    


# expects the name of the enemy from the server, will access the corresponding 
# art from local file
def update_graphics(s):
    global enemyCount

    # if the number of enemies hasn't changed, don't need to update the graphics
    if len(s) == enemyCount:
        return

    # parse the number and class of enemies to display
    enemyList = []
    for enemy in s:
        enemyList.append(enemy["class"])

    # clear previous windows
    for window in windows[3]:
        window.clear()
        window.refresh()
        del window

    # create appropriate number/size windows
    if len(enemyList) == 2: 
        win3b_a = win3.derwin(int((5*rows)/6)-3, int(cols/3)-2, 1, 1)
        win3b_b = win3.derwin(int((5*rows)/6)-3, int(cols/3)-2, 1, int(cols/3))
        windows[3].append(win3b_a)
        windows[3].append(win3b_b)
    elif len(enemyList) == 3:
        win3b_a = win3.derwin(int((5*rows)/6)-3, int(2*cols/9)-2, 1, 1)
        win3b_b = win3.derwin(int((5*rows)/6)-3, int(2*cols/9)-2, 1, int(2*cols/9))
        win3b_c = win3.derwin(int((5*rows)/6)-3, int(2*cols/9)-2, 1, int(4*cols/9))
        windows[3].append(win3b_a)
        windows[3].append(win3b_b)
        windows[3].append(win3b_c)
    else:
        win3b = win3.derwin(int((5*rows)/6)-3, int(2*cols/3)-2, 1, 1)
        windows[3].append(win3b)

    enemyCount = len(s)
    
    # if all enemies have been defeated, return. there will now be one empty window
    if len(s) == 0:
        windows[3][0].refresh()
        return
     
    if len(enemyList) == 1:
        windows[3][0].addstr(1, 1, enemyDict[enemyList[0]])
        windows[3][0].refresh()

    elif len(enemyList) == 2:
        windows[3][0].addstr(1, 1, enemyDict[enemyList[0]])
        windows[3][1].addstr(1, 1, enemyDict[enemyList[1]])
        windows[3][0].refresh()
        windows[3][1].refresh()

    elif len(enemyList) == 3:
        windows[3][0].addstr(1, 1, enemyDict[enemyList[0]])
        windows[3][1].addstr(1, 1, enemyDict[enemyList[1]])
        windows[3][2].addstr(1, 1, enemyDict[enemyList[2]])
        windows[3][0].refresh()
        windows[3][1].refresh()
        windows[3][2].refresh()



# similar to update player status
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
    # particularly small displays will need to rely on feed region for enemy status data
    # when there three enemies
    try:
        windows[4].addstr(2, 1, line1)
        windows[4].addstr(3, 1, line2)
        windows[4].addstr(4, 1, line3)
    except:
        pass

    windows[4].refresh()

