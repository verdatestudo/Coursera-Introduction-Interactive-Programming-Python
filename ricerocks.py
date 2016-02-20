
'''
An Introduction to Interactive Programming in Python - week 8
RiceRocks
2015-Dec-19
Python 2.7
Chris
'''

# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
timerSpeed = 3000.0
rockLimit = 12
started = False
explosion_group = set([])

# globals for physics etc - can change to improve gameplay
friction = 1 - 0.01
accel = 0.2
shipTurnSpeed = 0.1
intRockSpeed = 5


class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
ship_thrust_sound.set_volume(0.3)
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
#my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.vel[0] *= friction
        self.vel[1] *= friction
        self.angle += self.angle_vel
        if self.thrust == True:
            self.vel[0] += angle_to_vector(self.angle)[0] * accel
            self.vel[1] += angle_to_vector(self.angle)[1] * accel

    def turn(self, direction, onOff):
        if onOff == True:
            if direction == "left":
                self.angle_vel = -shipTurnSpeed
            elif direction == "right":
                self.angle_vel = shipTurnSpeed
        elif onOff == False:
            self.angle_vel = 0
        else:
            print "error"

    def thrustOnOff(self, onOff):
        self.thrust = onOff
        if onOff == True:
            self.image_center[0] += 90
            ship_thrust_sound.play()
        elif onOff == False:
            self.image_center[0] -= 90
            ship_thrust_sound.rewind()

    def shoot(self):
        #global a_missile
        point_at = angle_to_vector(self.angle)
        pos = list(self.pos)
        vel = list(self.vel)
        for i in range(2):
            pos[i] += point_at[i] * self.radius
            vel[i] += point_at[i] * 5
        missile_group.add(Sprite(pos, vel, self.angle, 0, missile_image, missile_info, missile_sound))
        #missile.sound()

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        if self.animated == True:
            self.image_center[0] = 64 + (self.age * 128)
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        # stick this and ship code in its own function to avoid duplicate?
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        '''
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        '''
        self.angle += self.angle_vel
        self.age += 1
        if self.age >= self.lifespan:
            return True

    def collide(self, other_object):
        return dist(self.pos, other_object.pos) <= self.radius + other_object.radius


def groupCollide(group, other_object):
#otherobj = sprite, group = SET grp of Sprites
    for item in list(group):
        if item.collide(other_object) == True:
            group.remove(item)
            explosion_group.add(Sprite(other_object.pos, [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound))
            return True
        #self, pos, vel, ang, ang_vel, image, info, sound = None):

def groupGroupCollide(group1, group2):
    global score, rockSpeed
    for item in list(group1):
        if groupCollide(group2, item) == True:
            group1.remove(item)
            score += 1
            if score % 5 == 0:
                rockSpeed += 1


def draw(canvas):
    global time, lives, started, rockLimit

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text("Lives:" + str(lives), [10,20], 23, "red")
    canvas.draw_text("Score:" + str(score), [WIDTH-100,20], 23, "yellow")

    # draw ship and sprites
    my_ship.draw(canvas)
#   a_rock.draw(canvas)
#    a_missile.draw(canvas)
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)
    process_sprite_group(canvas, explosion_group)

    if groupCollide(rock_group, my_ship) == True:
        lives -= 1

    groupGroupCollide(rock_group, missile_group)

    if lives <= 0:
        started = False
        soundtrack.pause()

    # update ship and sprites
    my_ship.update()
#   a_rock.update()
#    a_missile.update()

    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
        timer.stop()
        for rock in list(rock_group):
            rock_group.remove(rock)
    else:
        timer.start()

def process_sprite_group(canvas, group):
    for item in list(group):
        item.draw(canvas)
        if item.update() == True:
            group.remove(item)

def click(pos):
    global started, lives, score, time, rockSpeed
    if started == False:
        started = True
        lives = 3
        score = 0
        time = 0
        rockSpeed = intRockSpeed
        soundtrack.rewind()
        soundtrack.play()

def keydown(key):
    #global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrustOnOff(True)
    if key == simplegui.KEY_MAP["left"]:
        my_ship.turn("left", True)
    if key == simplegui.KEY_MAP["right"]:
        my_ship.turn("right", True)
    if key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()

def keyup(key):
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrustOnOff(False)
    if key == simplegui.KEY_MAP["left"]:
        my_ship.turn("left", False)
    if key == simplegui.KEY_MAP["right"]:
        my_ship.turn("right", False)

# timer handler that spawns a rock
def rock_spawner():
    if len(rock_group) < rockLimit:
        rockNew = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
        for x in range(2):
            rockNew.vel[x] = random.randrange(-rockSpeed, rockSpeed)
        rockNew.angle_vel = (random.random() - 0.5) * 0.25
        rockNew.pos[0] = random.randrange(0, WIDTH)
        rockNew.pos[1] = random.randrange(0, HEIGHT)
        if rockNew.collide(my_ship) == False:
            rock_group.add(rockNew)

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
# ship _init__(self, pos, vel, angle, image, info):
# sprite __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
rock_group = set([])
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
missile_group = set([])
# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(timerSpeed, rock_spawner)

# get things rolling
timer.start()
frame.start()
