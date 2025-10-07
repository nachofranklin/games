import pygame
import os
import random
pygame.font.init()
pygame.mixer.init()

WIN_WIDTH, WIN_HEIGHT = 1200, 700
FPS = 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 80, 80
METEOR_WIDTH, METEOR_HEIGHT = 50, 50
VEL = 7
BULLET_VEL = 10
METEOR_VEL = 2
BORDER_WIDTH = 10
BORDER = pygame.Rect(WIN_WIDTH/2 - BORDER_WIDTH/2, 0, BORDER_WIDTH, WIN_HEIGHT)
BULLET_WIDTH, BULLET_HEIGHT = 24, 8
MAX_BULLETS = 3
MAX_METEORS = 1
BLUE_HIT = pygame.USEREVENT + 1
PINK_HIT = pygame.USEREVENT + 2
HEALTH_FONT = pygame.font.SysFont('comicsans', 60)
WINNER_FONT = pygame.font.SysFont('comicsans', 200)

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
EXPLOSION_MINI = pygame.transform.scale(EXPLOSION_IMAGE, (SPACESHIP_WIDTH*0.5, SPACESHIP_HEIGHT*0.5))
METEOR_IMAGE = pygame.image.load(os.path.join('images', 'meteor.png'))
METEOR = pygame.transform.scale(METEOR_IMAGE, (30, 30))

EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join('sound', 'explosion.wav'))
LASER_SOUND = pygame.mixer.Sound(os.path.join('sound', 'laser.wav'))
SHIP_EXPLODES_SOUND = pygame.mixer.Sound(os.path.join('sound', 'ship_explodes.wav'))

def draw_window(blue, pink, blue_bullets, pink_bullets, blue_health, pink_health, meteors):
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
    
    for meteor in meteors:
        WIN.blit(METEOR, (meteor.x, meteor.y))

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

def draw_winner(text, colour):
    SHIP_EXPLODES_SOUND.play()
    for i in range(2):
        draw_text = WINNER_FONT.render(text, 1, colour)
        WIN.blit(draw_text, (WIN_WIDTH/2 - draw_text.get_width()/2, WIN_HEIGHT/2 - draw_text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(1000)
        draw_text = WINNER_FONT.render(text, 1, WHITE)
        WIN.blit(draw_text, (WIN_WIDTH/2 - draw_text.get_width()/2, WIN_HEIGHT/2 - draw_text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(1000)
    draw_text = WINNER_FONT.render(text, 1, colour)
    WIN.blit(draw_text, (WIN_WIDTH/2 - draw_text.get_width()/2, WIN_HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1000)

def meteor_handling(meteors, meteor_grad, blue, pink):
    for meteor in meteors:
        for grad in meteor_grad:
            meteor.x += grad[0]
            meteor.y += grad[1]

            if pink.colliderect(meteor):
                pygame.event.post(pygame.event.Event(PINK_HIT))
                pygame.event.post(pygame.event.Event(PINK_HIT))
                WIN.blit(EXPLOSION_MINI, (meteor.x + METEOR_WIDTH/2 - EXPLOSION_MINI.get_width()/2, meteor.y + METEOR_HEIGHT/2 - EXPLOSION_MINI.get_height()/2))
                pygame.display.update()
                meteors.remove(meteor)
                meteor_grad.remove(grad)
                EXPLOSION_SOUND.play()

            if blue.colliderect(meteor):
                pygame.event.post(pygame.event.Event(BLUE_HIT))
                pygame.event.post(pygame.event.Event(BLUE_HIT))
                WIN.blit(EXPLOSION_MINI, (meteor.x + METEOR_WIDTH/2 - EXPLOSION_MINI.get_width()/2, meteor.y + METEOR_HEIGHT/2 - EXPLOSION_MINI.get_height()/2))
                pygame.display.update()
                meteors.remove(meteor)
                meteor_grad.remove(grad)
                EXPLOSION_SOUND.play()
            
            if meteor.x <= -1 - METEOR_WIDTH:
                meteors.remove(meteor)
                meteor_grad.remove(grad)
            if meteor.x >= WIN_WIDTH + 1 + METEOR_WIDTH:
                meteors.remove(meteor)
                meteor_grad.remove(grad)
            if meteor.y <= -1 - METEOR_HEIGHT:
                meteors.remove(meteor)
                meteor_grad.remove(grad)
            if meteor.y >= WIN_HEIGHT + 1 + METEOR_HEIGHT:
                meteors.remove(meteor)
                meteor_grad.remove(grad)

def main():
    blue = pygame.Rect(WIN_WIDTH/4 - SPACESHIP_WIDTH/2, WIN_HEIGHT/2 - SPACESHIP_HEIGHT/2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    pink = pygame.Rect(WIN_WIDTH*3/4 - SPACESHIP_WIDTH/2, WIN_HEIGHT/2 - SPACESHIP_HEIGHT/2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    blue_bullets = []
    pink_bullets = []
    meteors = []
    meteor_grad = []
    blue_health, pink_health = 10, 10

    clock = pygame.time.Clock() # creates a clock, learn more about this
    run = True
    while run:
        clock.tick(FPS) # sets the refresh rate (frames per second)
        start_time = pygame.time.get_ticks()//1000
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
        meteor_handling(meteors, meteor_grad, blue, pink)
        draw_window(blue, pink, blue_bullets, pink_bullets, blue_health, pink_health, meteors)

        if start_time % 5 == 0 and len(meteors) < MAX_METEORS:
            meteor_x = random.randint(0, WIN_WIDTH)
            meteor_y = random.randint(0, WIN_HEIGHT)
            entry = random.randint(1, 4)
            if entry == 1: # top
                meteorite = pygame.Rect(meteor_x, 0 - METEOR_HEIGHT, METEOR_WIDTH, METEOR_HEIGHT)
                if meteor_x < WIN_WIDTH/2:
                    x_grad = METEOR_VEL
                else:
                    x_grad = -METEOR_VEL
                y_grad = METEOR_VEL
                meteors.append(meteorite)
                meteor_grad.append((x_grad, y_grad))
            elif entry == 2: # right
                meteorite = pygame.Rect(WIN_WIDTH + METEOR_WIDTH, meteor_y, METEOR_WIDTH, METEOR_HEIGHT)
                x_grad = -METEOR_VEL
                if meteor_y < WIN_HEIGHT/2:
                    y_grad = METEOR_VEL
                else:
                    y_grad = -METEOR_VEL
                meteors.append(meteorite)
                meteor_grad.append((x_grad, y_grad))
            elif entry == 3: # bottom
                meteorite = pygame.Rect(meteor_x, WIN_HEIGHT + METEOR_HEIGHT, METEOR_WIDTH, METEOR_HEIGHT)
                if meteor_x < WIN_WIDTH/2:
                    x_grad = METEOR_VEL
                else:
                    x_grad = -METEOR_VEL
                y_grad = -METEOR_VEL
                meteors.append(meteorite)
                meteor_grad.append((x_grad, y_grad))
            elif entry == 4: # left
                meteorite = pygame.Rect(0 - METEOR_WIDTH, meteor_y, METEOR_WIDTH, METEOR_HEIGHT)
                x_grad = METEOR_VEL
                if meteor_y < WIN_HEIGHT/2:
                    y_grad = METEOR_VEL
                else:
                    y_grad = -METEOR_VEL
                meteors.append(meteorite)
                meteor_grad.append((x_grad, y_grad))

        winner_text = ''
        if blue_health <= 0:
            winner_text = 'Pink Wins!'
            colour = PINK
            WIN.blit(EXPLOSION, (blue.x + SPACESHIP_WIDTH/2 - EXPLOSION.get_width()/2, blue.y + SPACESHIP_HEIGHT/2 - EXPLOSION.get_height()/2))
            pygame.display.update()
        if pink_health <= 0:
            winner_text = 'Blue Wins!'
            colour = LIGHT_BLUE
            WIN.blit(EXPLOSION, (pink.x + SPACESHIP_WIDTH/2 - EXPLOSION.get_width()/2, pink.y + SPACESHIP_HEIGHT/2 - EXPLOSION.get_height()/2))
            pygame.display.update()
        if winner_text != '': # someone won
            draw_winner(winner_text, colour)
            run = False

    main()

main()

# I can´t figure out how to stop bullets from queueing up during the winner text stage

# ideas...
# add in meteorites that enter at a random co-ordinate and have a random gradient that can damage players
# figure out how to edit the .wav sound clips, explosion.wav is too quiet and delayed
# figure out how to make the mini explosion image on a meteor hit last a few seconds