import pygame
import os

pygame.font.init()
pygame.mixer.init()

PATH = '/home/nacho/repos/games/connect4/'

# variables used for pygame
GRID_WIDTH = GRID_HEIGHT = 800
SPACE = 100
WIN_WIDTH, WIN_HEIGHT = GRID_WIDTH, GRID_HEIGHT + SPACE
FPS = 60
SWIRL_SPEED = 100
COUNTER_RATIO = 9 # 66.66 pixels
COUNTER_WIDTH, COUNTER_HEIGHT = GRID_WIDTH/COUNTER_RATIO, GRID_HEIGHT/COUNTER_RATIO
OUTER_GAP = GRID_WIDTH/20.6 # 29 pixels
UPPER_GAP = GRID_HEIGHT/13.7 # 44 pixels
LOWER_GAP = GRID_HEIGHT/14.3 # 42 pixels
X_GAP = GRID_WIDTH/6 - OUTER_GAP/3 - COUNTER_WIDTH*7/6
Y_GAP = GRID_WIDTH/5 - UPPER_GAP/5 - LOWER_GAP/5 - COUNTER_HEIGHT*6/5
won = False

# board used for logic
BOARD_COLS, BOARD_ROWS = 7, 6
board = [['a' for c in range(BOARD_COLS)] for r in range(BOARD_ROWS)]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)
LIGHT_BLUE = (173, 216, 230)

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Connect 4')
BACKGROUND_COL = LIGHT_BLUE

# sounds
FART_SOUND = pygame.mixer.Sound(os.path.join(PATH, 'sounds', 'fart.wav'))
G_FART_SOUND = pygame.mixer.Sound(os.path.join(PATH, 'sounds', 'g_fart.wav'))
NI_HAO_SOUND = pygame.mixer.Sound(os.path.join(PATH, 'sounds', 'ni_hao.wav'))

# images
GRID_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'grid.png'))
GRID = pygame.transform.scale(GRID_IMAGE, (GRID_WIDTH, GRID_HEIGHT))
NORMAL_CITY_CREST_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'city_crest.png'))
NORMAL_CITY_CREST = pygame.transform.scale(NORMAL_CITY_CREST_IMAGE, (COUNTER_WIDTH, COUNTER_HEIGHT))
NEON_CITY_CREST_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'neon_city_crest.png'))
NEON_CITY_CREST = pygame.transform.scale(NEON_CITY_CREST_IMAGE, (COUNTER_WIDTH, COUNTER_HEIGHT))
SWIRL_0_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'swirl0.png'))
SWIRL_0 = pygame.transform.scale(SWIRL_0_IMAGE, (GRID_WIDTH/(COUNTER_RATIO - 2), GRID_HEIGHT/(COUNTER_RATIO - 2)))
SWIRL_1_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'swirl1.png'))
SWIRL_1 = pygame.transform.scale(SWIRL_1_IMAGE, (GRID_WIDTH/(COUNTER_RATIO - 2), GRID_HEIGHT/(COUNTER_RATIO - 2)))
SWIRL_2_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'swirl2.png'))
SWIRL_2 = pygame.transform.scale(SWIRL_2_IMAGE, (GRID_WIDTH/(COUNTER_RATIO - 2), GRID_HEIGHT/(COUNTER_RATIO - 2)))
SWIRL_3_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'swirl3.png'))
SWIRL_3 = pygame.transform.scale(SWIRL_3_IMAGE, (GRID_WIDTH/(COUNTER_RATIO - 2), GRID_HEIGHT/(COUNTER_RATIO - 2)))
SWIRL_4_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'swirl4.png'))
SWIRL_4 = pygame.transform.scale(SWIRL_4_IMAGE, (GRID_WIDTH/(COUNTER_RATIO - 2), GRID_HEIGHT/(COUNTER_RATIO - 2)))
SWIRL_5_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'swirl5.png'))
SWIRL_5 = pygame.transform.scale(SWIRL_5_IMAGE, (GRID_WIDTH/(COUNTER_RATIO - 2), GRID_HEIGHT/(COUNTER_RATIO - 2)))
HALF_SWIRL_WIDTH = SWIRL_0.get_width() / 2
HALF_SWIRL_HEIGHT = SWIRL_0.get_height() / 2
frame_index = 0
swirls = []
swirls.append(SWIRL_0)
swirls.append(SWIRL_1)
swirls.append(SWIRL_2)
swirls.append(SWIRL_3)
swirls.append(SWIRL_4)
swirls.append(SWIRL_5)

# PORTAL_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'portal_spritesheet.png')).convert_alpha()
# PORTAL = pygame.transform.scale(PORTAL_IMAGE, (GRID_WIDTH/(COUNTER_RATIO - 2), GRID_HEIGHT/(COUNTER_RATIO - 2)))
# swirl_scale = GRID_WIDTH/(COUNTER_RATIO - 2) # 1536 x 1024
# swirl_width = 512 * swirl_scale
# swirl_height = 512 * swirl_scale
# swirls_cols = 3 # PORTAL.get_width() // swirl_width
# swirls_rows = 2 # PORTAL.get_height() // swirl_height
# swirls = []
# for col in range(swirls_cols):
#     for row in range(swirls_rows):
#         swirl = pygame.Surface((swirl_width, swirl_height), pygame.SRCALPHA)
#         swirl.blit(PORTAL, (0, 0), (col * swirl_width, row * swirl_height, swirl_width, swirl_height))
#         swirls.append(swirl)

def win_swirls_horizontal(screen, row, col):
    global frame_index
    while frame_index < len(swirls):
        screen.blit(GRID, (0, SPACE))
        screen.blit(swirls[frame_index], (OUTER_GAP + (COUNTER_WIDTH + X_GAP) * col + COUNTER_WIDTH/2 - HALF_SWIRL_WIDTH, SPACE + UPPER_GAP + (COUNTER_HEIGHT + Y_GAP) * row + COUNTER_HEIGHT/2 - HALF_SWIRL_HEIGHT))
        screen.blit(swirls[frame_index], (OUTER_GAP + (COUNTER_WIDTH + X_GAP) * (col + 1) + COUNTER_WIDTH/2 - HALF_SWIRL_WIDTH, SPACE + UPPER_GAP + (COUNTER_HEIGHT + Y_GAP) * row + COUNTER_HEIGHT/2 - HALF_SWIRL_HEIGHT))
        screen.blit(swirls[frame_index], (OUTER_GAP + (COUNTER_WIDTH + X_GAP) * (col + 2) + COUNTER_WIDTH/2 - HALF_SWIRL_WIDTH, SPACE + UPPER_GAP + (COUNTER_HEIGHT + Y_GAP) * row + COUNTER_HEIGHT/2 - HALF_SWIRL_HEIGHT))
        screen.blit(swirls[frame_index], (OUTER_GAP + (COUNTER_WIDTH + X_GAP) * (col + 3) + COUNTER_WIDTH/2 - HALF_SWIRL_WIDTH, SPACE + UPPER_GAP + (COUNTER_HEIGHT + Y_GAP) * row + COUNTER_HEIGHT/2 - HALF_SWIRL_HEIGHT))
        pygame.display.update()
        pygame.time.delay(SWIRL_SPEED)
        frame_index += 1

def win_swirls_vertical(screen, row, col):
    global frame_index
    while frame_index < len(swirls):
        screen.blit(GRID, (0, SPACE))
        screen.blit(swirls[frame_index], (OUTER_GAP + (COUNTER_WIDTH + X_GAP) * col + COUNTER_WIDTH/2 - HALF_SWIRL_WIDTH, SPACE + UPPER_GAP + (COUNTER_HEIGHT + Y_GAP) * row + COUNTER_HEIGHT/2 - HALF_SWIRL_HEIGHT))
        screen.blit(swirls[frame_index], (OUTER_GAP + (COUNTER_WIDTH + X_GAP) * col + COUNTER_WIDTH/2 - HALF_SWIRL_WIDTH, SPACE + UPPER_GAP + (COUNTER_HEIGHT + Y_GAP) * (row + 1) + COUNTER_HEIGHT/2 - HALF_SWIRL_HEIGHT))
        screen.blit(swirls[frame_index], (OUTER_GAP + (COUNTER_WIDTH + X_GAP) * col + COUNTER_WIDTH/2 - HALF_SWIRL_WIDTH, SPACE + UPPER_GAP + (COUNTER_HEIGHT + Y_GAP) * (row + 2) + COUNTER_HEIGHT/2 - HALF_SWIRL_HEIGHT))
        screen.blit(swirls[frame_index], (OUTER_GAP + (COUNTER_WIDTH + X_GAP) * col + COUNTER_WIDTH/2 - HALF_SWIRL_WIDTH, SPACE + UPPER_GAP + (COUNTER_HEIGHT + Y_GAP) * (row + 3) + COUNTER_HEIGHT/2 - HALF_SWIRL_HEIGHT))
        pygame.display.update()
        pygame.time.delay(SWIRL_SPEED)
        frame_index += 1

def win_swirls_diagonal_pos(screen, row, col):
    global frame_index
    while frame_index < len(swirls):
        screen.blit(GRID, (0, SPACE))
        screen.blit(swirls[frame_index], (OUTER_GAP + (COUNTER_WIDTH + X_GAP) * col + COUNTER_WIDTH/2 - HALF_SWIRL_WIDTH, SPACE + UPPER_GAP + (COUNTER_HEIGHT + Y_GAP) * row + COUNTER_HEIGHT/2 - HALF_SWIRL_HEIGHT))
        screen.blit(swirls[frame_index], (OUTER_GAP + (COUNTER_WIDTH + X_GAP) * (col + 1) + COUNTER_WIDTH/2 - HALF_SWIRL_WIDTH, SPACE + UPPER_GAP + (COUNTER_HEIGHT + Y_GAP) * (row + 1) + COUNTER_HEIGHT/2 - HALF_SWIRL_HEIGHT))
        screen.blit(swirls[frame_index], (OUTER_GAP + (COUNTER_WIDTH + X_GAP) * (col + 2) + COUNTER_WIDTH/2 - HALF_SWIRL_WIDTH, SPACE + UPPER_GAP + (COUNTER_HEIGHT + Y_GAP) * (row + 2) + COUNTER_HEIGHT/2 - HALF_SWIRL_HEIGHT))
        screen.blit(swirls[frame_index], (OUTER_GAP + (COUNTER_WIDTH + X_GAP) * (col + 3) + COUNTER_WIDTH/2 - HALF_SWIRL_WIDTH, SPACE + UPPER_GAP + (COUNTER_HEIGHT + Y_GAP) * (row + 3) + COUNTER_HEIGHT/2 - HALF_SWIRL_HEIGHT))
        pygame.display.update()
        pygame.time.delay(SWIRL_SPEED)
        frame_index += 1

def win_swirls_diagonal_neg(screen, row, col):
    global frame_index
    while frame_index < len(swirls):
        screen.blit(GRID, (0, SPACE))
        screen.blit(swirls[frame_index], (OUTER_GAP + (COUNTER_WIDTH + X_GAP) * col + COUNTER_WIDTH/2 - HALF_SWIRL_WIDTH, SPACE + UPPER_GAP + (COUNTER_HEIGHT + Y_GAP) * row + COUNTER_HEIGHT/2 - HALF_SWIRL_HEIGHT))
        screen.blit(swirls[frame_index], (OUTER_GAP + (COUNTER_WIDTH + X_GAP) * (col + 1) + COUNTER_WIDTH/2 - HALF_SWIRL_WIDTH, SPACE + UPPER_GAP + (COUNTER_HEIGHT + Y_GAP) * (row - 1) + COUNTER_HEIGHT/2 - HALF_SWIRL_HEIGHT))
        screen.blit(swirls[frame_index], (OUTER_GAP + (COUNTER_WIDTH + X_GAP) * (col + 2) + COUNTER_WIDTH/2 - HALF_SWIRL_WIDTH, SPACE + UPPER_GAP + (COUNTER_HEIGHT + Y_GAP) * (row - 2) + COUNTER_HEIGHT/2 - HALF_SWIRL_HEIGHT))
        screen.blit(swirls[frame_index], (OUTER_GAP + (COUNTER_WIDTH + X_GAP) * (col + 3) + COUNTER_WIDTH/2 - HALF_SWIRL_WIDTH, SPACE + UPPER_GAP + (COUNTER_HEIGHT + Y_GAP) * (row - 3) + COUNTER_HEIGHT/2 - HALF_SWIRL_HEIGHT))
        pygame.display.update()
        pygame.time.delay(SWIRL_SPEED)
        frame_index += 1

class Column:
    def __init__(self, x, col):
        self.rect = pygame.Rect(x, 0, COUNTER_WIDTH, WIN_HEIGHT)
        self.x = x
        self.col = col
        self.row_counter = 5
        self.is_hovered = False

    def draw_hover_counter(self, screen, crest):
        pygame.draw.rect(screen, BACKGROUND_COL, pygame.Rect(0, 0, WIN_WIDTH, SPACE)) # un-blits counter
        if self.is_hovered:
            screen.blit(crest, (self.x, SPACE - COUNTER_HEIGHT)) # blits the counter at the top
    
    def draw_actual_counter(self, screen, crest, player):
        self.is_hovered = False
        pygame.draw.rect(screen, BACKGROUND_COL, pygame.Rect(0, 0, WIN_WIDTH, SPACE)) # un-blits counter at the top
        screen.blit(crest, (self.x, SPACE + UPPER_GAP + (COUNTER_HEIGHT + Y_GAP) * self.row_counter))
        pygame.display.update()
        board[self.row_counter][self.col] = player
        self.row_counter -= 1

        if check_win(player):
            print(f"{player.upper()} wins!")

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
    global won
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player):
                win_swirls_horizontal(WIN, row, col)
                won = True

    # Check vertical
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if (board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player):
                win_swirls_vertical(WIN, row, col)
                won = True

    # Check diagonal (positive slope)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player):
                win_swirls_diagonal_pos(WIN, row, col)
                won = True

    # Check diagonal (negative slope)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player):
                win_swirls_diagonal_neg(WIN, row, col)
                won = True

def main():

    clock = pygame.time.Clock()
    global frame_index
    global won
    won = False
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
                if won == False:
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
                if won == False:
                    for col in columns:
                        if col.is_clicked(pygame.mouse.get_pos()) and col.row_counter > -1:
                            if p1_turn:
                                # G_FART_SOUND.play()
                                col.draw_actual_counter(WIN, NORMAL_CITY_CREST, 'p1')
                                p1_turn = False
                            elif p1_turn == False:
                                # NI_HAO_SOUND.play()
                                col.draw_actual_counter(WIN, NEON_CITY_CREST, 'p2')
                                p1_turn = True

        check_win('p1')
        check_win('p2')
        if frame_index >= len(swirls):
            frame_index = 0

main()

# choose your counter and sound
# highlight the winning 4 in a row
# get a winning sound
# add in a play again button when the game is won
# correct the position of the swirls