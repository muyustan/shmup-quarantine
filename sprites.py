from constants import *

# create sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
mobs = pygame.sprite.Group()

# player sprite


class Player(pygame.sprite.Sprite):

    SPEED = 7

    def __init__(self):
        super().__init__()
        # pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((80, 100))
        self.image.fill(CYAN)
        pygame.draw.circle(self.image, RED, (40, 50), 15, 3)
        pygame.draw.rect(self.image, BLACK, (0, 0, 80, 100), 3)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 5
        self.speedx = 0
        self.HP = 3
        self.shield = False

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


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((MOB_W, MOB_H))
        self.image.fill(MAGENTA)
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.bottom = random.randint(-2 * self.rect.height, 0)

    def update(self):
        self.rect.y += 6
        if self.rect.top > HEIGHT:
            self.kill()

# Bullet sprite


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BULLET_W, BULLET_H))
        self.image.fill(RED)
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
