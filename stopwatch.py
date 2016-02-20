
'''
An Introduction to Interactive Programming in Python - week 3
Stopwatch
2015-Nov-24
Python 2.7
Chris
'''

# template for "Stopwatch: The Game"
import simplegui

# define global variables

width = 500
height = 500
interval = 100
cTick = 0
running = False
reset = False
a = 0
b = 0
c = 0
d = 0
cSto = 0
cCor = 0
result = str(cCor) + " // " + str(cSto)

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global a, b, c, d
    a = t // 60000
    b = (t // 10000) % 6
    c = (t // 1000) % 10
    d = t // 100 % 10
    return "%s:%s%s:%s" % (a, b, c, d)

# define event handlers for buttons; "Start", "Stop", "Reset"
def butHandSt():
    global running, reset
    if running == False:
        running = True
        butSt.set_text("STOP")
        reset = False
        timer.start()
    elif running == True:
        stopTimer()

def butHandRes():
    global cTick, cSto, cCor, reset
    cTick = 0
    reset = True
    stopTimer()


def stopTimer():
    global running, cCor, cSto, result, reset
    running = False
    butSt.set_text("START")
    timer.stop()
    if reset == False:
        if cTick // 100 % 10 == 0:
            cCor += 1
        cSto += 1
        result = str(cCor) + " // " + str(cSto)
        print result
    elif reset == True:
        cSto = 0
        cCor = 0
        result = str(cCor) + " // " + str(cSto)


# define event handler for timer with 0.1 sec interval
def onTick():
    global cTick
    cTick += interval
    print cTick

# define draw handler
def draw(canvas):
    canvas.draw_text(format(cTick), [width / 2, height / 2], 32, "white")
    canvas.draw_text(result, [width - 100, 50], 32, "red")

# create frame
frame = simplegui.create_frame("Home", width, height)
butSt = frame.add_button('START', butHandSt)
butReset = frame.add_button('Reset', butHandRes)

# register event handlers
timer = simplegui.create_timer(interval, onTick)
frame.set_draw_handler(draw)

# start frame
frame.start()

# Please remember to review the grading rubric
