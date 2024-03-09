import sys
import pygame as pg


REFRESH_RATE = 100

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

#Colours:
BLACK = (0, 0 , 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (127, 127, 127)
AQUA_BLUE = (0,255,255)

GRAVITY = 20 # Simulates gravity, not real earth gravity, 9.81
ACCELERATION_MULTIPLIER = 1.5 # Used to scale acceleration so the projectile is at a pace the user can see 
PROJECTILE_RADIUS = 12
INITIAL_PROJECTILE_POSITION = (WINDOW_WIDTH/2, WINDOW_HEIGHT - PROJECTILE_RADIUS - 3) #(640, 705)
TIME_MULTIPLIER = 8 # Used to scale time so the projectile is at a pace the user can see

