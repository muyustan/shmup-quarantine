# all imports and constant definitions
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>
import pygame
import random
import sys
import os
import platform
# from pathlib import Path

# to solve the issues of the screen resolution in Windows OS.

if platform.system() == "Windows":
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()
else:
    pass


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# define constants
WIDTH = 700  # make sure WIDTH % 2 = 0
HEIGHT = 960  # make sure HEIGHT % 2 = 0
FPS = 60
NUM_METEORS = 10
NUM_MOBS = 4
BULLET_SPEED = 10
METEOR_SPEED_MULTIPLIER = 1
POWERUP_SPEED = 4
PLAYER_SPEED = 9
MARGIN = 10
MAX_BULLET = 50  # number of bullets which is allowed to be on screen at a moment

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
GRAY = (127, 127, 127)

# other constants
FONT = pygame.font.match_font('arial')

# setups

pygame.init()
pygame.mixer.init()  # sound system init
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHMUP - QUARANTINE")
clock = pygame.time.Clock()


# directories

# img_dir = os.path.join(os.path.dirname(__file__), "img")
# sound_dir = os.path.join(os.path.dirname(__file__), "sound")

# root_dir = Path(__file__).parent.resolve()
# img_dir = root_dir / "img"
# sound_dir = root_dir / "sound"

img_dir = resource_path("img")
sound_dir = resource_path("sound")

# Load all game sounds

pygame.mixer.music.load(os.path.join(sound_dir, 'FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.1)

shoot_sound = pygame.mixer.Sound(os.path.join(sound_dir, "cheuw.wav"))
shoot_sound.set_volume(0.3)

expl_meteor_sound_list = []
for sound_file in ["expl_meteor_1.wav"]:  # a sound effect will be chosen from this list.
    expl_meteor_sound_list.append(pygame.mixer.Sound(os.path.join(sound_dir, sound_file)))
    expl_meteor_sound_list[-1].set_volume(0.3)

# Load all game graphics

bg_img = pygame.image.load(os.path.join(img_dir, "starfield.png")).convert()

player_img = pygame.image.load(os.path.join(img_dir, "playerShip1_orange.png")).convert()
player_img.set_colorkey(BLACK)
# I found out that using set_colorkey() is faster than using conver_alpha()

laser_img = pygame.image.load(os.path.join(img_dir, "laserRed05.png")).convert()
laser_img.set_colorkey(BLACK)


mob_img_list = []
for image_file in ["enemyBlack5.png", "enemyBlue4.png", "enemyGreen3.png", "enemyRed2.png", "enemyBlack1.png"]:
    mob_img_list.append(pygame.image.load(os.path.join(img_dir, image_file)).convert())
    mob_img_list[-1].set_colorkey(BLACK)

life_img = pygame.image.load(os.path.join(img_dir, "pill_red.png")).convert()
life_img.set_colorkey(BLACK)

shield_img = pygame.image.load(os.path.join(img_dir, "powerupBlue_shield.png")).convert()
shield_img.set_colorkey(BLACK)

meteor_dict = {  # "name" : [pygame_image, point]

    "tiny1_gray": [pygame.image.load(os.path.join(img_dir, "meteorBrown_tiny1.png")).convert_alpha(), 10],
    "tiny2_brown": [pygame.image.load(os.path.join(img_dir, "meteorGrey_tiny2.png")).convert_alpha(), 10],
    "small1_gray": [pygame.image.load(os.path.join(img_dir, "meteorGrey_small1.png")).convert_alpha(), 5],
    "small2_brown": [pygame.image.load(os.path.join(img_dir, "meteorBrown_small2.png")).convert_alpha(), 5],
    "med1_gray": [pygame.image.load(os.path.join(img_dir, "meteorGrey_med1.png")).convert_alpha(), 3],
    "med1_brown": [pygame.image.load(os.path.join(img_dir, "meteorBrown_med1.png")).convert_alpha(), 3],
    "big1_gray": [pygame.image.load(os.path.join(img_dir, "meteorGrey_big1.png")).convert_alpha(), 1],
    "big3_gray": [pygame.image.load(os.path.join(img_dir, "meteorGrey_big3.png")).convert_alpha(), 1],
    "big1_brown": [pygame.image.load(os.path.join(img_dir, "meteorBrown_big1.png")).convert_alpha(), 1],

}
