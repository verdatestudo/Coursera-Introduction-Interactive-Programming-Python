'''
An Introduction to Interactive Programming in Python - week 5
Memory
2015-Nov-26
Python 2.7
Chris
'''

import simplegui
import random

canWidth = 800
canHeight = 100
cardWidth = 50

state = 0
counter = 0

LG = []
LGloc = []

list1 = range(1, 9)
list2 = range(1, 9)
listMain = list1 + list2
listExposed = []

# helper function to initialize globals
def new_game():
    global state, counter
    state = 0
    counter = 0
    labelTurn.set_text("Turns = %d" % counter)
    random.shuffle(listMain)
    del listExposed[:]
    del LG[:]
    del LGloc[:]
    for _ in range(len(listMain)):
        listExposed.append(False)


# define event handlers
def click(pos):
    global state, LG, listExposed, counter
    loc = int(pos[0] / 50)

    if listExposed[loc] == False:
        listExposed[loc] = True
        if state == 2:
            state = 1
            if LG[0] != LG[1]:
                listExposed[LGloc[0]] = False
                listExposed[LGloc[1]] = False
            del LG[:]
            del LGloc[:]
        elif state == 0:
            state += 1
        elif state == 1:
            state += 1
            counter += 1
        else:
            print "error"
        LG.append(listMain[loc])
        LGloc.append(loc)
    labelTurn.set_text("Turns = %d" % counter)

# cards are logically 50x100 pixels in size
def draw(canvas):
    pos = 0
    for x in range(16):
        if listExposed[x] == True:
            canvas.draw_text(str(listMain[x]), (pos+cardWidth/3, canHeight/2 ), cardWidth/2, 'Red')
        elif listExposed[x] == False:
            canvas.draw_line((pos+cardWidth/2, 0), (pos+cardWidth/2, canHeight), cardWidth, 'Green')
            canvas.draw_line((pos+cardWidth, 0), (pos+cardWidth, canHeight), 2, 'White')
        else:
            print "error"
        #canvas.draw_line((pos+cardWidth, 0), (pos+cardWidth, canHeight), 5, 'White')
        pos += cardWidth

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", canWidth, canHeight)
frame.add_button("Reset", new_game)
labelTurn = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
