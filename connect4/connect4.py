import pygame
import os

pygame.font.init()
pygame.mixer.init()

PATH = '/home/nacho/repos/games/connect4/'

# variables used for pygame
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

# board used for logic
BOARD_COLS, BOARD_ROWS = 7, 6
for r in range(BOARD_ROWS):
    board = [[0] * BOARD_COLS] * (r+1)

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
    def __init__(self, x, col):
        self.rect = pygame.Rect(x, 0, COUNTER_WIDTH, WIN_HEIGHT)
        self.x = x
        self.col = col
        self.row_counter = 5
        self.is_hovered = False

    def draw_hover_counter(self, screen, crest):
        pygame.draw.rect(WIN, BACKGROUND_COL, pygame.Rect(0, 0, WIN_WIDTH, SPACE)) # un-blits counter
        if self.is_hovered:
            screen.blit(crest, (self.x, SPACE - COUNTER_HEIGHT)) # blits the counter at the top
    
    def draw_actual_counter(self, screen, crest, player):
        self.is_hovered = False
        pygame.draw.rect(WIN, BACKGROUND_COL, pygame.Rect(0, 0, WIN_WIDTH, SPACE)) # un-blits counter at the top
        screen.blit(crest, (self.x, SPACE + UPPER_GAP + (COUNTER_HEIGHT + Y_GAP) * self.row_counter))
        pygame.display.update()
        board[self.row_counter][self.col] = player
        self.row_counter -= 1

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
columns = []
column0 = Column(OUTER_GAP + (COUNTER_WIDTH + X_GAP) * 0, 0)
column1 = Column(OUTER_GAP + (COUNTER_WIDTH + X_GAP) * 1, 1)
column2 = Column(OUTER_GAP + (COUNTER_WIDTH + X_GAP) * 2, 2)
column3 = Column(OUTER_GAP + (COUNTER_WIDTH + X_GAP) * 3, 3)
column4 = Column(OUTER_GAP + (COUNTER_WIDTH + X_GAP) * 4, 4)
column5 = Column(OUTER_GAP + (COUNTER_WIDTH + X_GAP) * 5, 5)
column6 = Column(OUTER_GAP + (COUNTER_WIDTH + X_GAP) * 6, 6)
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

# Function to check for a win
def check_win(player):
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if (
                board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3] == player
            ):
                return True

    # Check vertical
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if (
                board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] == player
            ):
                return True

    # Check diagonal (positive slope)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if (
                board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == player
            ):
                return True

    # Check diagonal (negative slope)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if (
                board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == player
            ):
                return True

    return False

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
                    if col.is_clicked(pygame.mouse.get_pos()) and col.row_counter > -1:
                        if p1_turn:
                            col.draw_actual_counter(WIN, NORMAL_CITY_CREST, 'p1')
                            p1_turn = False
                        elif p1_turn == False:
                            col.draw_actual_counter(WIN, NEON_CITY_CREST, 'p2')
                            p1_turn = True

main()