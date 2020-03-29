import pygame
import random
import os

# define constants
WIDTH = 700
HEIGHT = 960
FPS = 60
BULLET_SPEED = 10
METEOR_SPEED_MULTIPLIER = 1
POWERUP_SPEED = 4
PLAYER_SPEED = 9
MARGIN = 10

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)

# setups

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHMUP - QUARANTINE")
clock = pygame.time.Clock()

img_dir = os.path.join(os.path.dirname(__file__), "img")

# Load all game graphics
""" either one of the methods will do the job """
# bg_img = pygame.image.load(os.path.join(img_dir, "virus2.png")).convert()
# bg_img.set_colorkey(WHITE)
bg_img = pygame.image.load(os.path.join(img_dir, "starfield.png")).convert_alpha()
player_img = pygame.image.load(os.path.join(img_dir, "playerShip1_blue.png")).convert_alpha()
laser_img = pygame.image.load(os.path.join(img_dir, "laserRed05.png")).convert_alpha()
meteor_img = pygame.image.load(os.path.join(img_dir, "meteorGrey_med1.png")).convert_alpha()
mob_img = pygame.image.load(os.path.join(img_dir, "enemyBlack5.png")).convert_alpha()
life_img = pygame.image.load(os.path.join(img_dir, "pill_red.png")).convert_alpha()
shield_img = pygame.image.load(os.path.join(img_dir, "powerupBlue_shield.png")).convert_alpha()
