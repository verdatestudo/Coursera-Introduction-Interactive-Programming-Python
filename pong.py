# Implementation of classic arcade game Pong

'''
An Introduction to Interactive Programming in Python - week 4
Pong
2015-Nov-11
Python 2.7
Chris
'''

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2
paddle1_vel = [0, 0]
paddle2_vel = [0, 0]
paddle_def_vel = 12
padCushion = 20
score = [0, 0]

ball_vel = [0, 0]
ball_pos = [0, 0]

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    rndSpd = random.randrange(4, 7)
    rndSpd2 = random.randrange(-8, 8)
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [rndSpd, rndSpd2]
    if direction == "LEFT":
        ball_vel = ball_vel
    elif direction == "RIGHT":
        ball_vel = [-ball_vel[0], ball_vel[1]]
    else:
        print "error"

# define event handlers

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score  # these are ints
    d = random.choice(["LEFT", "RIGHT"])
    paddle1_vel = [0, 0]
    paddle2_vel = [0, 0]
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    spawn_ball(d)
    score = [0, 0]

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel

    canvas.draw_text(str(score[0]), (185, 40), 40, "Blue")
    canvas.draw_text(str(score[1]), (400, 40), 40, "Green")
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball

    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    if ball_pos[0] - BALL_RADIUS - PAD_WIDTH <= 0:
        if ball_pos[1] >= paddle1_pos - padCushion and ball_pos[1] <= paddle1_pos + PAD_HEIGHT + padCushion:
            ball_vel[0] = -ball_vel[0] * 1.1
        else:
            spawn_ball("LEFT")
            score[1] += 1
    if ball_pos[0] + BALL_RADIUS + PAD_WIDTH >= WIDTH:
        if ball_pos[1] >= paddle2_pos - padCushion and ball_pos[1] <= paddle2_pos + PAD_HEIGHT + padCushion:
            ball_vel[0] = -ball_vel[0] * 1.1
        else:
            spawn_ball("RIGHT")
            score[0] += 1
    if ball_pos[1] - BALL_RADIUS <= 0:
        ball_vel[1] = -ball_vel[1]
    if ball_pos[1] + BALL_RADIUS >= HEIGHT:
        ball_vel[1] = -ball_vel[1]

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "red", "white")

    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel[1]
    paddle2_pos += paddle2_vel[1]

    if paddle1_pos <= 0:
        paddle1_vel[1] = 0
        paddle1_pos = 0
    if paddle1_pos + PAD_HEIGHT >= HEIGHT:
        paddle1_vel[1] = 0
        paddle1_pos = HEIGHT - PAD_HEIGHT
    if paddle2_pos <= 0:
        paddle2_vel[1] = 0
        paddle2_pos = 0
    if paddle2_pos + PAD_HEIGHT >= HEIGHT:
        paddle2_vel[1] = 0
        paddle2_pos = HEIGHT - PAD_HEIGHT

    # draw paddles
    canvas.draw_line((HALF_PAD_WIDTH, paddle1_pos), (HALF_PAD_WIDTH, paddle1_pos+PAD_HEIGHT), PAD_WIDTH, 'White')
    canvas.draw_line((WIDTH - HALF_PAD_WIDTH, paddle2_pos), (WIDTH - HALF_PAD_WIDTH, paddle2_pos+PAD_HEIGHT), PAD_WIDTH, 'White')

    # determine whether paddle and ball collide

    # draw scores

def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] = paddle_def_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] = -paddle_def_vel
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = paddle_def_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = -paddle_def_vel

def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] = 0
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] = 0
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = 0
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = 0

def restart_handler():
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
butRestart = frame.add_button('Restart', restart_handler)

# start frame
new_game()
frame.start()
