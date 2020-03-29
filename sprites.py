from constants import *

# create sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
mobs = pygame.sprite.Group()
meteors = pygame.sprite.Group()
lifebars = pygame.sprite.Group()


class Lifebar(pygame.sprite.Sprite):

    HEIGHT = 10
    MARGIN = 8

    def __init__(self, sprite):
        super().__init__()
        self.sprite = sprite
        self.single_bar_w = sprite.rect.width // sprite.HP
        self.width = self.single_bar_w * sprite.HP
        self.image = pygame.Surface((self.width, self.HEIGHT))
        # for j in range(sprite.HP):
        #     pygame.draw.rect(self.image, GREEN, (j * self.single_bar_w, 0, self.single_bar_w, self.HEIGHT), 0)
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = sprite.rect.centerx
        self.rect.bottom = sprite.rect.top - self.MARGIN

    def update(self):
        self.rect.centerx = self.sprite.rect.centerx
        self.rect.bottom = self.sprite.rect.top - self.MARGIN

    def redraw(self):
        self.width = self.single_bar_w * self.sprite.HP
        self.image = pygame.Surface((self.width, self.HEIGHT))
        # for j in range(self.sprite.HP):
        #     pygame.draw.rect(self.image, GREEN, (j * self.single_bar_w, 0, self.single_bar_w, self.HEIGHT), 0)
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()


# player sprite


class Player(pygame.sprite.Sprite):

    SPEED = 7

    def __init__(self):
        super().__init__()
        # pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((80, 100))
        # self.image.fill(CYAN)
        self.image = player_img
        # pygame.draw.circle(self.image, RED, (40, 50), 15, 3)
        # pygame.draw.rect(self.image, BLACK, (0, 0, 80, 100), 3)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 5
        self.speedx = 0
        self.HP = 3
        self.shield = False
        all_sprites.add(self)

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        return bullet  # I need this to set the margin in continious fire.

    def change_color(self):
        pass

    def increase_HP(self):
        if self.HP <= 2:
            self.HP += 1
            print("+1 HP", "Current HP:", self.HP)
        else:
            print("HP IS AT MAX", "--", "Current HP:", self.HP)

    def decrease_HP(self):
        if not self.shield:
            self.HP -= 1
            print("-1 HP", "--", "Current HP:", self.HP)
        else:
            self.shield = False
            print("Shield protected you!")

    def activate_shield(self):
        self.shield = True
        print("Shield Activated!")


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = meteor_img
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.bottom = random.randint(-2 * self.rect.height, 0)
        self.speedy = random.randint(3, 7)
        all_sprites.add(self)
        meteors.add(self)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = mob_img
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.bottom = random.randint(-2 * self.rect.height, 0)
        self.speedy = random.randint(1, 5)
        self.speedx = 0
        self.HP = 10
        all_sprites.add(self)
        mobs.add(self)
        self.lifebar = Lifebar(self)
        lifebars.add(self.lifebar)
        all_sprites.add(self.lifebar)

    def update(self):
        self.speedx = random.randint(-4, 4)
        self.rect.left += self.speedx
        self.rect.centery += self.speedy
        if self.rect.bottom > 300:
            self.speedy = 0
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <= 0:
            self.rect.left = 0

    def get_damage(self):
        self.HP -= 1
        self.lifebar.redraw()
        if self.HP <= 0:
            self.kill()
            self.lifebar.kill()
            print("Enemy destroyed!")

# Bullet sprite


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # self.image = pygame.Surface((BULLET_W, BULLET_H))
        # self.image.fill(RED)
        self.image = laser_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedx = 0
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill it if it moves away from the screen
        if self.rect.bottom < 0:
            self.kill()  # built in method of pygame.sprite


# powerup sprite


class PowerUp(pygame.sprite.Sprite):

    SPEEDY = 8

    def __init__(self):
        super().__init__()
        self.type = random.randint(0, 1)  # [0,1] integer
        if self.type == 0:  # HP power up
            self.image = pygame.Surface((POWERUP_W, POWERUP_H))
            self.image.fill(GREEN)
            self.rect = self.image.get_rect()
            self.rect.left = random.randint(0, WIDTH - self.rect.width)
            # self.rect.centerx = player.rect.centerx #debug
            self.rect.bottom = 0
        elif self.type == 1:  # shield
            self.image = pygame.Surface((POWERUP_W, POWERUP_H))
            self.image.fill(BLUE)
            self.rect = self.image.get_rect()
            self.rect.left = random.randint(0, WIDTH - self.rect.width)
            # self.rect.centerx = player.rect.centerx # debug
            self.rect.bottom = 0
        else:
            pass

    def update(self):
        self.rect.y += self.SPEEDY
        if self.rect.top > HEIGHT:
            self.kill()
