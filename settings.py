import pygame as pg
from test import AnimationSprite
vec = pg.math.Vector2


# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

# game settings
WIDTH = 1280
HEIGHT = 720
FPS = 60
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Menu")
TITLE = "Made By Scott and Cooper"
BGCOLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#WALL_IMG = 'tileGreen_39.png'

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 150
PLAYER_ROT_SPEED = 200
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 10)


# Gun settings
BULLET_IMG = 'bullet.png'
BULLET_SPEED = 300
BULLET_LIFETIME = 500
BULLET_RATE = 250
KICKBACK = 0
GUN_SPREAD = 0
BULLET_DAMAGE = 25

# Mob settings
MOB_IMG = 'zombie1_hold.png'
MOB_SPEEDS = [50, 60, 55, 70]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 1
MOB_KNOCKBACK = 2
AVOID_RADIUS = 50


