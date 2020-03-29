from constants import *

# create sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
mobs = pygame.sprite.Group()
meteors = pygame.sprite.Group()
lifebars = pygame.sprite.Group()

# Lifebar sprite


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
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()


# Player sprite


class Player(pygame.sprite.Sprite):

    SPEED = PLAYER_SPEED

    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.height / 2)  # this radius attribute is needed to use circular collision check.
        # pygame.draw.circle(self.image, GRAY, self.rect.center, self.radius, 3)
        # YOU HAVE TO DRAW THE CIRCLE BEFORE YOU MOVE THE SELF.IMAGE, BECAUSE OTHERWISE, THE SELF.RECT.CENTER COORDINATES WILL NOT BE RELATIVE TO THE SELF.IMAGE SURFACE, LIKE BELOW:
        # pygame.draw.circle(self.image, YELLOW, (self.rect.width // 2, self.rect.height // 2), self.radius, 3)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 15  # to make it appear at a little bit higher on the screen.
        self.HP = 300
        self.shield = False
        self.score = 0
        all_sprites.add(self)

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        shoot_sound.play()
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        return bullet  # I need this to set the margin in continious fire.

    def change_color(self):
        pass

    def increase_HP(self):
        if self.HP <= 2:
            self.HP += 1
            print("HP UP!", "Current HP:", self.HP)
        else:
            print("HP ALREADY MAX!", "--", "Current HP:", self.HP)

    def decrease_HP(self):
        if not self.shield:
            self.HP -= 1
            print("HP DOWN!", "--", "Current HP:", self.HP)
        else:
            self.shield = False
            print("Shield protected you!")

    def activate_shield(self):
        self.shield = True
        print("Shield Activated!")

# Meteor sprite


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image, self.points = random.choice(list(meteor_dict.values()))
        self.image_copy = self.image.copy()  # we have to make a copy of image to use in rotations.
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .95 / 2)
        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.bottom = random.randint(-2 * self.rect.height, 0)
        self.speedx = random.randint(-2, 2)
        self.speedy = random.randint(2, 7) * METEOR_SPEED_MULTIPLIER
        self.theta = 0
        self.dtheta = random.randint(-3, 3)  # degrees per frame
        # self.dtheta = 2
        # finally, add the object to the related groups
        all_sprites.add(self)
        meteors.add(self)

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT:
            self.kill()
        if self.rect.right <= 0:
            self.kill()
        if self.rect.left >= WIDTH:
            self.kill()

    def rotate(self):
        self.theta = (self.theta + self.dtheta) % 360
        self.image = pygame.transform.rotate(self.image_copy, self.theta)
        _center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = _center
        # pygame.draw.circle(self.image, BLUE, (self.rect.width // 2, self.rect.height // 2), self.radius, 3)
        # these 3 lines above basically makes sure that rectangle also keeps track of the rotation.

# Mob sprite


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = mob_img
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.bottom = random.randint(-2 * self.rect.height, 0)
        self.speedy = random.randint(1, 2)
        self.speedx = 0
        while self.speedx == 0:
            self.speedx = random.randint(-2, 2)
        self.HP = 10
        all_sprites.add(self)
        mobs.add(self)
        self.lifebar = Lifebar(self)
        self.first = True
        self.bottom_limit = random.randint(int(self.rect.height * 1.2), HEIGHT / 2)
        lifebars.add(self.lifebar)
        all_sprites.add(self.lifebar)

    def update(self):
        self.rect.left += self.speedx
        self.rect.centery += self.speedy
        if self.rect.bottom >= self.bottom_limit:
            self.speedy *= -1
            self.first = False
        if self.rect.top <= 30 and not self.first:
            self.speedy *= -1
            self.bottom_limit = random.randint(int(self.rect.height * 1.2), HEIGHT / 2)
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
            self.speedx *= -1
        if self.rect.left <= 0:
            self.rect.left = 0
            self.speedx *= -1

    def get_damage(self):
        self.HP -= 1
        self.lifebar.redraw()
        if self.HP <= 0:
            self.kill()
            self.lifebar.kill()
            print("Enemy destroyed!")

# Bullet sprite


class Bullet(pygame.sprite.Sprite):

    HEIGHT = laser_img.get_size()[1]
    SPEED = BULLET_SPEED

    def __init__(self, x, y):
        super().__init__()
        self.image = laser_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedx = 0
        self.speedy = -1 * Bullet.SPEED

    def update(self):
        self.rect.y += self.speedy
        # kill it if it moves away from the screen
        if self.rect.bottom < 0:
            self.kill()  # built in method of pygame.sprite


# PowerUp sprite


class PowerUp(pygame.sprite.Sprite):

    SPEED = POWERUP_SPEED

    def __init__(self):
        super().__init__()
        self.type = random.randint(0, 1)  # [0,1] integer
        if self.type == 0:  # life
            self.image = life_img
            self.rect = self.image.get_rect()
            self.rect.left = random.randint(0, WIDTH - self.rect.width)
            self.rect.bottom = 0
        elif self.type == 1:  # shield
            self.image = shield_img
            self.rect = self.image.get_rect()
            self.rect.left = random.randint(0, WIDTH - self.rect.width)
            self.rect.bottom = 0
        else:
            pass

    def update(self):
        self.rect.y += self.SPEED
        if self.rect.top > HEIGHT:
            self.kill()
