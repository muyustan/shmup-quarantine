# A shoot'em up game

from constants import *
import sprites
import time

# initiate some variables
max_bullet = 15  # number of bullets which is allowed to be on screen at a moment
running = True  # game loop control variable

power_up_funcs = [

    sprites.Player.increase_HP,
    sprites.Player.activate_shield

]  # list for to-do fucntions

# initialize pygame and create window


player = sprites.Player()


# have to use this because, otherwise, for the first SPACE key pressing, the newest_bullet is not defined yet.
newest_bullet = sprites.Bullet(0, 0)

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

    while len(sprites.mobs) != 3:
        m = sprites.Mob()

    while len(sprites.meteors) != 5:
        m = sprites.Meteor()

    keystate = pygame.key.get_pressed()
    player.speedx = 0
    if keystate[pygame.K_RIGHT]:
        player.speedx += sprites.Player.SPEED
    if keystate[pygame.K_LEFT]:
        player.speedx -= sprites.Player.SPEED
    if keystate[pygame.K_SPACE] and player.rect.top - newest_bullet.rect.bottom > sprites.Bullet.HEIGHT + MARGIN and not len(sprites.bullets) >= max_bullet:
        newest_bullet = player.shoot()
    # BULLET_H refers to height of the bullet and margin refers to the minimum allowable margin between two consequent b
    # If there are more than 10 bullets at a time on the screen, then no more new bullets can be fired.
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

    for m in hits:
        # this is necessary, because, otherwise the shooting ability was stuck when player shoots a mob within the range of forbidden margin for continious fire. This is due to the fact that when you kill a sprite by sprite.kill(), sprite maintains its attributes.
        hits[m][0].rect.bottom = -1
        m.get_damage()

    hits = pygame.sprite.groupcollide(sprites.meteors, sprites.bullets, True, True)
    for m in hits:
        hits[m][0].rect.bottom = -1  # same reasoning as above.

    hits = pygame.sprite.spritecollide(player, sprites.mobs, True)
    hits += pygame.sprite.spritecollide(player, sprites.meteors, True, pygame.sprite.collide_circle) # instead of rectangular collison check, we do it based on sprite.radius attribute
    for m in hits:
        player.decrease_HP()
        if player.HP <= 0:
            running = False

    # Update

    sprites.all_sprites.update()

    # Draw / render
    # screen.fill(YELLOW)  # to debug any possible mistakes on bg placement
    screen.blit(bg_img, (0, 0))
    # this is my way to fill background with appropriate dimensions.
    screen.blit(bg_img, (bg_img.get_size()[0], 0))
    sprites.all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()


pygame.quit()
raise SystemExit  # to exit python
