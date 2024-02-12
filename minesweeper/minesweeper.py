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
TOP_SECTION = GRID_HEIGHT / (GRID_ROWS - 2)
WIN_WIDTH = GRID_WIDTH
WIN_HEIGHT = GRID_HEIGHT + TOP_SECTION
FPS = 60
no_of_bombs = 17
grid = np.zeros((GRID_ROWS, GRID_COLS))
revealed = np.zeros((GRID_ROWS, GRID_COLS))
TILE_WIDTH = GRID_WIDTH/GRID_COLS
TILE_HEIGHT = GRID_HEIGHT/GRID_ROWS

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Minesweeper')

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 255, 0)

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
        # self.rect = pygame.Rect(col * TILE_WIDTH, row * TILE_HEIGHT + TOP_SECTION, TILE_WIDTH, TILE_HEIGHT)
        self.img = pygame.transform.scale(pygame.image.load(os.path.join(PATH, 'img', self.png)), (img_width, img_height))
        # self.is_hovered = False

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

def main():

    clock = pygame.time.Clock()
    WIN.fill(LIGHT_BLUE)
    for tile in tile_list:
        tile.draw_tile(WIN)
    # flag_rect = pygame.Rect(GRID_WIDTH/2 - TILE_WIDTH/2, TOP_SECTION/2 - TILE_HEIGHT/2, TILE_WIDTH, TILE_HEIGHT)
    WIN.blit(flag.img, flag_rect)
    # pygame.draw.circle(WIN, GREEN, (GRID_WIDTH/2, TOP_SECTION/2), radius, circle_width)
    pygame.display.update()
    add_bombs()
    clicked = False
    flag_hovered = False
    flag_clicked = False
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()

            elif event.type == pygame.MOUSEMOTION:
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
                if clicked == False:
                    clicked = True
                    # clicking on any tile
                    for tile in tile_list:
                        if tile.is_clicked(pygame.mouse.get_pos()):
                            if flag_clicked:
                                if tile.is_flagged == False:
                                    tile.is_flagged = True
                                elif tile.is_flagged == True:
                                    tile.is_flagged = False
                                tile.draw_tile(WIN)
                                pygame.display.update()
                            elif flag_clicked == False:
                                if tile.is_flagged == False:
                                    if grid[tile.row][tile.col] == 8038:
                                        WIN.blit(bomb.img, tile.rect)
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
                    if pygame.Rect(GRID_WIDTH/2 - TILE_WIDTH/2, TOP_SECTION/2 - TILE_HEIGHT/2, TILE_WIDTH, TILE_HEIGHT).collidepoint(event.pos) and flag_clicked == False and revealed[tile.row][tile.col] == 0:
                        flag_clicked = True
                        WIN.blit(flag.img, flag_rect)
                        pygame.draw.circle(WIN, GREEN, (GRID_WIDTH/2, TOP_SECTION/2), radius, circle_width)
                        pygame.display.update()
                    elif pygame.Rect(GRID_WIDTH/2 - TILE_WIDTH/2, TOP_SECTION/2 - TILE_HEIGHT/2, TILE_WIDTH, TILE_HEIGHT).collidepoint(event.pos) and flag_clicked == True and revealed[tile.row][tile.col] == 0:
                        flag_clicked = False
                        WIN.blit(flag.img, flag_rect)
                        pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONUP: # prevents one click doing multiple actions
                clicked = False

main()

# need to add in a clock element to time it
# need to add in win logic
# need to add in loss logic