# A shoot'em up game

from configurations import *
import sprites

# user defined functions


def draw_text(surface, text, size, color, pos):
    x, y = pos
    font = pygame.font.Font(FONT, size)
    text_surface = font.render(text, True, color, None)
    text_rect = text_surface.get_rect()
    text_rect.topright = (x, y)
    surface.blit(text_surface, text_rect)


# initiate some variables

running = True  # game loop control variable

power_up_funcs = [

    sprites.Player.increase_HP,
    sprites.Player.activate_shield

]  # list for to-do fucntions

# initialize pygame and create window


player = sprites.Player()

# have to use this because, otherwise, for the first SPACE key pressing, the newest_bullet is not defined yet.
newest_bullet = sprites.Bullet(0, 0)

# set the music !!!
pygame.mixer.music.play(loops=-1)  # just repeat it

# Game loop
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        else:
            pass

    while len(sprites.mobs) != NUM_MOBS:
        m = sprites.Mob()

    while len(sprites.meteors) != NUM_METEORS:
        m = sprites.Meteor()

    keystate = pygame.key.get_pressed()
    player.speedx = 0
    if keystate[pygame.K_RIGHT]:
        player.speedx += sprites.Player.SPEED
    if keystate[pygame.K_LEFT]:
        player.speedx -= sprites.Player.SPEED
    if (keystate[pygame.K_SPACE] or keystate[pygame.K_UP]) and (player.rect.top - newest_bullet.rect.bottom) > (sprites.Bullet.HEIGHT + MARGIN) and not (len(sprites.bullets) >= MAX_BULLET):
        newest_bullet = player.shoot()
    # MARGIN refers to the minimum allowable margin between two consequent b
    # If there are more than MAX_BULLET number of bullets at a time on the screen, then no more new bullets can be fired.
    if keystate[pygame.K_ESCAPE]:
        running = False
    if random.randint(0, 1000000) > 999000:  # to randomize the process
        power_up = sprites.PowerUp()
        sprites.all_sprites.add(power_up)
        sprites.powerups.add(power_up)

    hits = pygame.sprite.spritecollide(player, sprites.powerups, True)
    for pu in hits:
        power_up_funcs[pu.type](player)

    hits = pygame.sprite.groupcollide(
        sprites.mobs, sprites.bullets, False, True)

    for mob in hits:
        # this is necessary, because, otherwise the shooting ability was stuck when player shoots a mob within the range of forbidden margin for continious fire. This is due to the fact that when you kill a sprite by sprite.kill(), sprite maintains its attributes.
        hits[mob][0].rect.bottom = -1
        mob.get_damage()

    hits = pygame.sprite.groupcollide(sprites.meteors, sprites.bullets, True, True)

    for meteor in hits:
        random.choice(expl_meteor_sound_list).play()
        hits[meteor][0].rect.bottom = -1  # same reasoning as above.
        player.score += meteor.points

    hits = pygame.sprite.spritecollide(player, sprites.mobs, True)
    hits += pygame.sprite.spritecollide(player, sprites.meteors, True, pygame.sprite.collide_circle)  # instead of rectangular collison check, we do it based on sprite.radius attribute
    for m in hits:
        player.decrease_HP()
        if player.HP <= 0:
            running = False

    # Update

    sprites.all_sprites.update()

    # Draw / render
    screen.blit(bg_img, (0, 0))
    # this is my way to fill background with appropriate dimensions.
    screen.blit(bg_img, (bg_img.get_size()[0], 0))
    sprites.all_sprites.draw(screen)
    draw_text(screen, f"SCORE: {player.score}", 26, BLUE, (WIDTH, 0))
    # *after* drawing everything, flip the display
    pygame.display.flip()


pygame.quit()
raise SystemExit  # to exit python
