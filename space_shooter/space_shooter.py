import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIN_WIDTH, WIN_HEIGHT = 1200, 700
FPS = 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 80, 80
VEL = 7
BULLET_VEL = 10
BORDER_WIDTH = 10
BORDER = pygame.Rect(WIN_WIDTH/2 - BORDER_WIDTH/2, 0, BORDER_WIDTH, WIN_HEIGHT)
BULLET_WIDTH, BULLET_HEIGHT = 24, 8
MAX_BULLETS = 3
BLUE_HIT = pygame.USEREVENT + 1
PINK_HIT = pygame.USEREVENT + 2
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)
LIGHT_BLUE = (173, 216, 230)

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Space Shooter')

BLUE_SPACESHIP_IMAGE = pygame.image.load(os.path.join('images', 'blue_spaceship.png'))
BLUE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(BLUE_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
PINK_SPACESHIP_IMAGE = pygame.image.load(os.path.join('images', 'pink_spaceship.png'))
PINK_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(PINK_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
SPACE_IMAGE = pygame.image.load(os.path.join('images', 'space.png'))
SPACE = pygame.transform.scale(SPACE_IMAGE, (WIN_WIDTH, WIN_HEIGHT))
EXPLOSION_IMAGE = pygame.image.load(os.path.join('images', 'explosion.png'))
EXPLOSION = pygame.transform.scale(EXPLOSION_IMAGE, (SPACESHIP_WIDTH*1.5, SPACESHIP_HEIGHT*1.5))

EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join('sound', 'explosion.wav'))
LASER_SOUND = pygame.mixer.Sound(os.path.join('sound', 'laser.wav'))

def draw_window(blue, pink, blue_bullets, pink_bullets, blue_health, pink_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER) # draw the border
    blue_health_text = HEALTH_FONT.render(f'Health: {blue_health}', 1, WHITE)
    pink_health_text = HEALTH_FONT.render(f'Health: {pink_health}', 1, WHITE)
    WIN.blit(blue_health_text, (10, 10))
    WIN.blit(pink_health_text, (WIN_WIDTH - pink_health_text.get_width() - 10, 10))
    WIN.blit(BLUE_SPACESHIP, (blue.x, blue.y))
    WIN.blit(PINK_SPACESHIP, (pink.x, pink.y))

    for bullet in blue_bullets:
        pygame.draw.rect(WIN, LIGHT_BLUE, bullet) # draw blue bullets
    for bullet in pink_bullets:
        pygame.draw.rect(WIN, PINK, bullet) # draw pink bullets

    pygame.display.update()

def blue_handling(keys_pressed, blue):
    if keys_pressed[pygame.K_a] and blue.x > 0: # LEFT
        blue.x -= VEL
    if keys_pressed[pygame.K_d] and blue.x < BORDER.x - SPACESHIP_WIDTH: # RIGHT
        blue.x += VEL
    if keys_pressed[pygame.K_w] and blue.y > 0: # UP
        blue.y -= VEL
    if keys_pressed[pygame.K_s] and blue.y < WIN_HEIGHT - SPACESHIP_HEIGHT: # DOWN
        blue.y += VEL

def pink_handling(keys_pressed, pink):
    if keys_pressed[pygame.K_LEFT] and pink.x > BORDER.x + BORDER_WIDTH: # LEFT
        pink.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and pink.x < WIN_WIDTH - SPACESHIP_WIDTH: # RIGHT
        pink.x += VEL
    if keys_pressed[pygame.K_UP] and pink.y > 0: # UP
        pink.y -= VEL
    if keys_pressed[pygame.K_DOWN] and pink.y < WIN_HEIGHT - SPACESHIP_HEIGHT: # DOWN
        pink.y += VEL

def bullet_handling(blue_bullets, pink_bullets, blue, pink):
    for bullet in blue_bullets:
        bullet.x += BULLET_VEL
        if pink.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PINK_HIT))
            blue_bullets.remove(bullet)
            EXPLOSION_SOUND.play()
        elif bullet.x > WIN_WIDTH:
            blue_bullets.remove(bullet)
    
    for bullet in pink_bullets:
        bullet.x -= BULLET_VEL
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            pink_bullets.remove(bullet)
            EXPLOSION_SOUND.play()
        elif bullet.x < 0:
            pink_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIN_WIDTH/2 - draw_text.get_width()/2, WIN_HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    blue = pygame.Rect(WIN_WIDTH/4 - SPACESHIP_WIDTH/2, WIN_HEIGHT/2 - SPACESHIP_HEIGHT/2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    pink = pygame.Rect(WIN_WIDTH*3/4 - SPACESHIP_WIDTH/2, WIN_HEIGHT/2 - SPACESHIP_HEIGHT/2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    blue_bullets = []
    pink_bullets = []
    blue_health, pink_health = 10, 10

    clock = pygame.time.Clock() # creates a clock, learn more about this
    run = True
    while run:
        clock.tick(FPS) # sets the refresh rate (frames per second)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()
            
            if event.type == BLUE_HIT:
                blue_health -= 1
            if event.type == PINK_HIT:
                pink_health -= 1

            if event.type == pygame.KEYDOWN: # checks if a button is pressed and triggers an event
                if event.key == pygame.K_CAPSLOCK and len(blue_bullets) < MAX_BULLETS and pink_health > 0:
                    bullet = pygame.Rect(blue.x + SPACESHIP_WIDTH, blue.y + SPACESHIP_HEIGHT/2 - BULLET_HEIGHT/2, BULLET_WIDTH, BULLET_HEIGHT)
                    blue_bullets.append(bullet)
                    LASER_SOUND.play()
                if event.key == pygame.K_KP_0 and len(pink_bullets) < MAX_BULLETS and blue_health > 0:
                    bullet = pygame.Rect(pink.x, pink.y + SPACESHIP_HEIGHT/2 - BULLET_HEIGHT/2, BULLET_WIDTH, BULLET_HEIGHT)
                    pink_bullets.append(bullet)
                    LASER_SOUND.play()

        keys_pressed = pygame.key.get_pressed()
        blue_handling(keys_pressed, blue)
        pink_handling(keys_pressed, pink)
        bullet_handling(blue_bullets, pink_bullets, blue, pink)
        draw_window(blue, pink, blue_bullets, pink_bullets, blue_health, pink_health)

        winner_text = ''
        if blue_health <= 0:
            winner_text = 'Pink Wins!'
            WIN.blit(EXPLOSION, (blue.x + SPACESHIP_WIDTH/2 - EXPLOSION.get_width()/2, blue.y + SPACESHIP_HEIGHT/2 - EXPLOSION.get_height()/2))
            pygame.display.update()
        if pink_health <= 0:
            winner_text = 'Blue Wins!'
            WIN.blit(EXPLOSION, (pink.x + SPACESHIP_WIDTH/2 - EXPLOSION.get_width()/2, pink.y + SPACESHIP_HEIGHT/2 - EXPLOSION.get_height()/2))
            pygame.display.update()
        if winner_text != '': # someone won
            draw_winner(winner_text)
            run = False

    main()

main()

# I can´t figure out how to stop bullets from queueing up during the winner text stage

# ideas...
# make the explosion get bigger with the tick speed
# add a big explosion sound for when the ship gets to zero health
# add in meteorites that enter at a random co-ordinate and have a random gradient that can damage players
# figure out how to edit the .wav sound clips, explosion.wav is too quiet and delayed
# make the winner text flash