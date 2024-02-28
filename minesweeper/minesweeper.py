import pygame
import os
import random
import numpy as np

pygame.font.init()
pygame.mixer.init()

# variables
PATH = '/home/nacho/repos/games/minesweeper/'
GRID_WIDTH = GRID_HEIGHT = 700
GRID_ROWS = GRID_COLS = 10
no_of_bombs = 17

TOP_SECTION = GRID_HEIGHT / (GRID_ROWS - 2)
WIN_WIDTH = GRID_WIDTH
WIN_HEIGHT = GRID_HEIGHT + TOP_SECTION
TILE_WIDTH = GRID_WIDTH/GRID_COLS
TILE_HEIGHT = GRID_HEIGHT/GRID_ROWS
FPS = 60
grid = np.zeros((GRID_ROWS, GRID_COLS))
revealed = np.zeros((GRID_ROWS, GRID_COLS))
flag_counter = 0

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Minesweeper')

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)

# sounds
EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join(PATH, 'sounds', 'explosion.wav'))

# images
class Tiles:
    def __init__(self, row, col, img_width = TILE_WIDTH, img_height = TILE_HEIGHT):
        self.row = row
        self.col = col
        self.img_width = img_width
        self.img_height = img_height
        self.rect = pygame.Rect(col * TILE_WIDTH, row * TILE_HEIGHT + TOP_SECTION, TILE_WIDTH, TILE_HEIGHT)
        self.unopened_img = pygame.transform.scale(pygame.image.load(os.path.join(PATH, 'img', 'unopened_square.png')), (img_width, img_height))
        self.hovered_img = pygame.transform.scale(pygame.image.load(os.path.join(PATH, 'img', 'hover_unopened.png')), (img_width, img_height))
        self.flag_img = pygame.transform.scale(pygame.image.load(os.path.join(PATH, 'img', 'flag.png')), (img_width, img_height))
        self.is_hovered = False
        self.is_flagged = False
    
    def draw_tile(self, screen):
        if revealed[self.row][self.col] == 0:
            if self.is_flagged:
                self.img = self.flag_img
            else:
                if self.is_hovered:
                    self.img = self.hovered_img
                else:
                    self.img = self.unopened_img
            screen.blit(self.img, self.rect)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

tile_list = []
for row in range(GRID_ROWS):
    for col in range(GRID_COLS):
        tile_list.append(Tiles(row, col))

class Tile_results:
    def __init__(self, file_name, img_width = TILE_WIDTH, img_height = TILE_HEIGHT):
        self.png = file_name + '.png'
        self.img_width = img_width
        self.img_height = img_height
        self.img = pygame.transform.scale(pygame.image.load(os.path.join(PATH, 'img', self.png)), (img_width, img_height))

flag = Tile_results('flag')
flag_rect = pygame.Rect(GRID_WIDTH/2 - TILE_WIDTH/2, TOP_SECTION/2 - TILE_HEIGHT/2, TILE_WIDTH, TILE_HEIGHT)
radius = int(TILE_WIDTH/2)
circle_width = int(TILE_WIDTH/6)
bomb = Tile_results('ms_bomb')
zero = Tile_results('zero')
one = Tile_results('one')
two = Tile_results('two')
three = Tile_results('three')
four = Tile_results('four')
five = Tile_results('five')
six = Tile_results('six')
seven = Tile_results('seven')
eight = Tile_results('eight')

timer_text_pos = (WIN_WIDTH/4, TOP_SECTION/2)
flag_text_pos = (WIN_WIDTH*3/4, TOP_SECTION/2)
font_size = int(TOP_SECTION)

# function for timer and flag counter / total bombs
def draw_text(text, position, colour = BLUE, font_size = font_size, screen = WIN):
    font = pygame.font.Font(None, font_size)
    max_text_surface = font.render('100 / 100', True, colour)
    max_text_surface.fill(LIGHT_BLUE)
    max_text_rect = max_text_surface.get_rect()
    max_text_rect.center = position
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect()
    text_rect.center = position
    screen.blit(max_text_surface, max_text_rect) # blits a blue surface of the length of 100 / 100
    screen.blit(text_surface, text_rect) # blits the text we actually want

# randomises where the bombs are and counts the number of adjacent bombs in every tile
def add_bombs():
    bomb_positions = random.sample(range(GRID_ROWS * GRID_COLS), no_of_bombs)
    for position in bomb_positions:
        row, col = divmod(position, GRID_COLS)
        grid[row, col] = 8038 # 8038 = bomb

        # Update adjacent cells
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= row + i < GRID_ROWS and 0 <= col + j < GRID_COLS and grid[row + i][col + j] != 8038:
                    grid[row + i][col + j] += 1

# when a zero is clicked this will reveal all adjacent zeros and the next adjacent non zero values
def reveal_zeros(grid, revealed, row, col):
    if revealed[row][col]:
        return
    revealed[row][col] = 1

    if grid[row][col] == 0:
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_row, new_col = row + i, col + j
                if 0 <= new_row < GRID_ROWS and 0 <= new_col < GRID_COLS:
                    # revealed[new_row][new_col] = 1
                    if grid[new_row][new_col] == 0:
                        WIN.blit(zero.img, pygame.Rect(new_col * TILE_WIDTH, new_row * TILE_HEIGHT + TOP_SECTION, TILE_WIDTH, TILE_HEIGHT))
                    elif grid[new_row][new_col] == 1:
                        WIN.blit(one.img, pygame.Rect(new_col * TILE_WIDTH, new_row * TILE_HEIGHT + TOP_SECTION, TILE_WIDTH, TILE_HEIGHT))
                    elif grid[new_row][new_col] == 2:
                        WIN.blit(two.img, pygame.Rect(new_col * TILE_WIDTH, new_row * TILE_HEIGHT + TOP_SECTION, TILE_WIDTH, TILE_HEIGHT))
                    elif grid[new_row][new_col] == 3:
                        WIN.blit(three.img, pygame.Rect(new_col * TILE_WIDTH, new_row * TILE_HEIGHT + TOP_SECTION, TILE_WIDTH, TILE_HEIGHT))
                    elif grid[new_row][new_col] == 4:
                        WIN.blit(four.img, pygame.Rect(new_col * TILE_WIDTH, new_row * TILE_HEIGHT + TOP_SECTION, TILE_WIDTH, TILE_HEIGHT))
                    elif grid[new_row][new_col] == 5:
                        WIN.blit(five.img, pygame.Rect(new_col * TILE_WIDTH, new_row * TILE_HEIGHT + TOP_SECTION, TILE_WIDTH, TILE_HEIGHT))
                    elif grid[new_row][new_col] == 6:
                        WIN.blit(six.img, pygame.Rect(new_col * TILE_WIDTH, new_row * TILE_HEIGHT + TOP_SECTION, TILE_WIDTH, TILE_HEIGHT))
                    elif grid[new_row][new_col] == 7:
                        WIN.blit(seven.img, pygame.Rect(new_col * TILE_WIDTH, new_row * TILE_HEIGHT + TOP_SECTION, TILE_WIDTH, TILE_HEIGHT))
                    elif grid[new_row][new_col] == 8:
                        WIN.blit(eight.img, pygame.Rect(new_col * TILE_WIDTH, new_row * TILE_HEIGHT + TOP_SECTION, TILE_WIDTH, TILE_HEIGHT))
                    reveal_zeros(grid, revealed, new_row, new_col)

class Text:
    def __init__(self, x, y, text, text_colour=BLACK, text_size=font_size*2):
        self.rect = pygame.Rect(x, y, 0, 0)
        self.text = text
        self.text_colour = text_colour
        self.text_size = text_size
        self.font = pygame.font.Font(None, self.text_size)
    
    def blit_text(self, screen):
        text_surface = self.font.render(self.text, True, self.text_colour)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

YOU_LOSE_ONE = Text(GRID_WIDTH/2, TOP_SECTION + GRID_HEIGHT/2, 'You Lose', BLACK)
YOU_LOSE_TWO = Text(GRID_WIDTH/2, TOP_SECTION + GRID_HEIGHT/2, 'You Lose', PINK)
YOU_WIN = Text(GRID_WIDTH/2, TOP_SECTION + GRID_HEIGHT/2, 'You Win!!!', BLACK)

def you_lose(screen):
    EXPLOSION_SOUND.play()
    YOU_LOSE_ONE.blit_text(screen)
    pygame.display.update()
    pygame.time.delay(1000)
    YOU_LOSE_TWO.blit_text(screen)
    pygame.display.update()
    pygame.time.delay(1000)
    YOU_LOSE_ONE.blit_text(screen)
    pygame.display.update()
    pygame.time.delay(1000)
    YOU_LOSE_TWO.blit_text(screen)
    pygame.display.update()
    pygame.time.delay(1000)
    YOU_LOSE_ONE.blit_text(screen)
    pygame.display.update()

def you_win(screen):
    bomb_list = []
    for tile in tile_list:
        if grid[tile.row][tile.col] == 8038:
            bomb_list.append(tile)
    random.shuffle(bomb_list)
    YOU_WIN.blit_text(screen)
    pygame.display.update()
    pygame.time.delay(3000)
    for b in bomb_list:
        screen.blit(bomb.img, b.rect)
        YOU_WIN.blit_text(screen)
        EXPLOSION_SOUND.play()
        pygame.display.update()
        pygame.time.delay(750)

def start_timer(start_time):
    timer_seconds = (pygame.time.get_ticks() - start_time) / 1000
    minutes, seconds = divmod(timer_seconds, 60)
    formatted_time = "{:02}:{:02}".format(int(minutes), int(seconds))
    draw_text(f"{formatted_time}", timer_text_pos)
    pygame.display.update()

def main():

    clock = pygame.time.Clock()
    global flag_counter
    WIN.fill(LIGHT_BLUE)
    for tile in tile_list:
        tile.draw_tile(WIN)
    WIN.blit(flag.img, flag_rect)
    draw_text(f'{flag_counter} / {no_of_bombs}', flag_text_pos)
    pygame.display.update()
    add_bombs()
    clicked = False
    flag_hovered = False
    flag_clicked = False
    game_over = False
    timer_started = False
    revealed_count = 0
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()

            elif event.type == pygame.MOUSEMOTION:
                if game_over == False:
                    # shows which tile is being hovered over
                    for tile in tile_list:
                        if tile.rect.collidepoint(event.pos) and tile.is_hovered == False and tile.is_flagged == False and revealed[tile.row][tile.col] == 0: # if you're hovering over it and you weren't before
                            tile.is_hovered = True # it's hovered now
                            tile.draw_tile(WIN) # draw the hovered version
                            pygame.display.update()
                        elif tile.rect.collidepoint(event.pos) == False and tile.is_hovered == True and tile.is_flagged == False and revealed[tile.row][tile.col] == 0: # if you're not hovering over the square but you were before
                            tile.is_hovered = False # now it's not hovered
                            tile.draw_tile(WIN) # draw the normal version
                            pygame.display.update()
                    
                    # hovering over the flag at the top
                    if pygame.Rect(GRID_WIDTH/2 - TILE_WIDTH/2, TOP_SECTION/2 - TILE_HEIGHT/2, TILE_WIDTH, TILE_HEIGHT).collidepoint(event.pos) and flag_hovered == False and flag_clicked == False:
                        flag_hovered = True
                        WIN.blit(flag.img, flag_rect)
                        pygame.draw.circle(WIN, PINK, (GRID_WIDTH/2, TOP_SECTION/2), radius, circle_width)
                        pygame.display.update()
                    elif pygame.Rect(GRID_WIDTH/2 - TILE_WIDTH/2, TOP_SECTION/2 - TILE_HEIGHT/2, TILE_WIDTH, TILE_HEIGHT).collidepoint(event.pos) == False and flag_hovered == True and flag_clicked == False:
                        flag_hovered = False
                        WIN.blit(flag.img, flag_rect)
                        pygame.display.update()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if clicked == False and game_over == False:
                    clicked = True
                    # clicking on any tile
                    for tile in tile_list:
                        if tile.is_clicked(pygame.mouse.get_pos()) and revealed[tile.row][tile.col] == 0:
                            if flag_clicked:
                                if tile.is_flagged == False:
                                    tile.is_flagged = True
                                    flag_counter += 1
                                elif tile.is_flagged == True:
                                    tile.is_flagged = False
                                    flag_counter -= 1
                                tile.draw_tile(WIN)
                                draw_text(f'{flag_counter} / {no_of_bombs}', flag_text_pos)
                                pygame.display.update()
                            elif flag_clicked == False:
                                if timer_started == False:
                                    timer_started = True
                                    start_time = pygame.time.get_ticks()
                                if tile.is_flagged == False:
                                    if grid[tile.row][tile.col] == 8038:
                                        WIN.blit(bomb.img, tile.rect)
                                        you_lose(WIN)
                                        game_over = True
                                    elif grid[tile.row][tile.col] == 0:
                                        WIN.blit(zero.img, tile.rect)
                                        reveal_zeros(grid, revealed, tile.row, tile.col) # if it's a zero, this will reveal everything connected until it hits a number
                                    elif grid[tile.row][tile.col] == 1:
                                        WIN.blit(one.img, tile.rect)
                                    elif grid[tile.row][tile.col] == 2:
                                        WIN.blit(two.img, tile.rect)
                                    elif grid[tile.row][tile.col] == 3:
                                        WIN.blit(three.img, tile.rect)
                                    elif grid[tile.row][tile.col] == 4:
                                        WIN.blit(four.img, tile.rect)
                                    elif grid[tile.row][tile.col] == 5:
                                        WIN.blit(five.img, tile.rect)
                                    elif grid[tile.row][tile.col] == 6:
                                        WIN.blit(six.img, tile.rect)
                                    elif grid[tile.row][tile.col] == 7:
                                        WIN.blit(seven.img, tile.rect)
                                    elif grid[tile.row][tile.col] == 8:
                                        WIN.blit(eight.img, tile.rect)

                                    revealed[tile.row][tile.col] = 1 # records that it's been revealed
                                    pygame.display.update()

                    # clicking the flag at the top
                    if pygame.Rect(GRID_WIDTH/2 - TILE_WIDTH/2, TOP_SECTION/2 - TILE_HEIGHT/2, TILE_WIDTH, TILE_HEIGHT).collidepoint(event.pos) and flag_clicked == False:
                        flag_clicked = True
                        WIN.blit(flag.img, flag_rect)
                        pygame.draw.circle(WIN, GREEN, (GRID_WIDTH/2, TOP_SECTION/2), radius, circle_width)
                        pygame.display.update()
                    elif pygame.Rect(GRID_WIDTH/2 - TILE_WIDTH/2, TOP_SECTION/2 - TILE_HEIGHT/2, TILE_WIDTH, TILE_HEIGHT).collidepoint(event.pos) and flag_clicked == True:
                        flag_clicked = False
                        WIN.blit(flag.img, flag_rect)
                        pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONUP: # prevents one click doing multiple actions
                clicked = False

        # checking if you win
        revealed_count = 0
        for tile in tile_list:
            if revealed[tile.row][tile.col] == 1:
                revealed_count += 1
        if revealed_count == GRID_ROWS * GRID_COLS - no_of_bombs and game_over == False:
            you_win(WIN)
            game_over = True

        # starting/stopping the timer
        if timer_started and game_over == False:
            start_timer(start_time)

main()

# best scores (10x10 with 17 bombs)

# nathan - 1.17, 1.28, 1.30
# georgie - 0.00, 0.18
# ellie - 4.52
# almantas - 1.30