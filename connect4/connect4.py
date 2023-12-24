import pygame
import os

pygame.font.init()
pygame.mixer.init()

PATH = '/home/nacho/repos/games/connect4/'
GRID_WIDTH = GRID_HEIGHT = 600
SPACE = 100
WIN_WIDTH, WIN_HEIGHT = GRID_WIDTH, GRID_HEIGHT + SPACE
FPS = 60
COUNTER_RATIO = 9 # 66.66 pixels
COUNTER_WIDTH, COUNTER_HEIGHT = GRID_WIDTH/COUNTER_RATIO, GRID_HEIGHT/COUNTER_RATIO
OUTER_GAP = GRID_WIDTH/20.6 # 29 pixels
UPPER_GAP = GRID_HEIGHT/13.7 # 44 pixels
LOWER_GAP = GRID_HEIGHT/14.3 # 42 pixels
X_GAP = GRID_WIDTH/6 - OUTER_GAP/3 - COUNTER_WIDTH*7/6
Y_GAP = GRID_WIDTH/5 - UPPER_GAP/5 - LOWER_GAP/5 - COUNTER_HEIGHT*6/5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)
LIGHT_BLUE = (173, 216, 230)

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Connect 4')
BACKGROUND_COL = LIGHT_BLUE

# images
GRID_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'grid.png'))
GRID = pygame.transform.scale(GRID_IMAGE, (GRID_WIDTH, GRID_HEIGHT))
NORMAL_CITY_CREST_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'city_crest.png'))
NORMAL_CITY_CREST = pygame.transform.scale(NORMAL_CITY_CREST_IMAGE, (COUNTER_WIDTH, COUNTER_HEIGHT))
NEON_CITY_CREST_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'neon_city_crest.png'))
NEON_CITY_CREST = pygame.transform.scale(NEON_CITY_CREST_IMAGE, (COUNTER_WIDTH, COUNTER_HEIGHT))

class Column:
    def __init__(self, x):
        self.rect = pygame.Rect(x, 0, COUNTER_WIDTH, WIN_HEIGHT)
        self.x = x
        self.is_hovered = False
        self.counter = 5

    def draw_hover_counter(self, screen, crest):
        pygame.draw.rect(WIN, BACKGROUND_COL, pygame.Rect(0, 0, WIN_WIDTH, SPACE)) # un-blits counter
        if self.is_hovered:
            screen.blit(crest, (self.x, SPACE - COUNTER_HEIGHT)) # blits the counter at the top
    
    def draw_actual_counter(self, screen, crest):
        self.is_hovered = False
        pygame.draw.rect(WIN, BACKGROUND_COL, pygame.Rect(0, 0, WIN_WIDTH, SPACE)) # un-blits counter
        screen.blit(crest, (self.x, SPACE + UPPER_GAP + (COUNTER_HEIGHT + Y_GAP) * self.counter))
        pygame.display.update()
        self.counter -= 1

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
columns = []
column0 = Column(OUTER_GAP + (COUNTER_WIDTH + X_GAP) * 0)
column1 = Column(OUTER_GAP + (COUNTER_WIDTH + X_GAP) * 1)
column2 = Column(OUTER_GAP + (COUNTER_WIDTH + X_GAP) * 2)
column3 = Column(OUTER_GAP + (COUNTER_WIDTH + X_GAP) * 3)
column4 = Column(OUTER_GAP + (COUNTER_WIDTH + X_GAP) * 4)
column5 = Column(OUTER_GAP + (COUNTER_WIDTH + X_GAP) * 5)
column6 = Column(OUTER_GAP + (COUNTER_WIDTH + X_GAP) * 6)
columns.append(column0)
columns.append(column1)
columns.append(column2)
columns.append(column3)
columns.append(column4)
columns.append(column5)
columns.append(column6)
    
class Player:
    def __init__(self):
        self.wins = 0

    def winner(self):
        self.wins += 1

# WIN.blit(NEON_CITY_CREST, (OUTER_GAP + (COUNTER_WIDTH + X_GAP) * 0, SPACE + UPPER_GAP + (COUNTER_HEIGHT + Y_GAP) * 0))
# WIN.blit(NORMAL_CITY_CREST, (OUTER_GAP + (COUNTER_WIDTH + X_GAP) * 6, SPACE + UPPER_GAP + (COUNTER_HEIGHT + Y_GAP) * 5))

def main():

    clock = pygame.time.Clock()
    p1_turn = True

    WIN.fill(BACKGROUND_COL)
    WIN.blit(GRID, (0, SPACE))
    pygame.display.update()

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()

            elif event.type == pygame.MOUSEMOTION:
                # hovers the counter over the top
                for col in columns:
                    if p1_turn:
                        if col.rect.collidepoint(event.pos) and col.is_hovered == False:
                            col.is_hovered = True
                            col.draw_hover_counter(WIN, NORMAL_CITY_CREST)
                            pygame.display.update()
                        elif col.rect.collidepoint(event.pos) == False and col.is_hovered == True:
                            col.is_hovered = False
                    elif p1_turn == False:
                        if col.rect.collidepoint(event.pos) and col.is_hovered == False:
                            col.is_hovered = True
                            col.draw_hover_counter(WIN, NEON_CITY_CREST)
                            pygame.display.update()
                        elif col.rect.collidepoint(event.pos) == False and col.is_hovered == True:
                            col.is_hovered = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for col in columns:
                    if col.is_clicked(pygame.mouse.get_pos()) and col.counter > -1:
                        if p1_turn:
                            col.draw_actual_counter(WIN, NORMAL_CITY_CREST)
                            p1_turn = False
                        elif p1_turn == False:
                            col.draw_actual_counter(WIN, NEON_CITY_CREST)
                            p1_turn = True

main()