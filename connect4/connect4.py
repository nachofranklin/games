import pygame
import os
import random

pygame.font.init()
pygame.mixer.init()

PATH = '/home/nacho/repos/games/connect4/'

# variables used for pygame
GRID_WIDTH = GRID_HEIGHT = 800
SPACE = GRID_HEIGHT/8
WIN_WIDTH, WIN_HEIGHT = GRID_WIDTH, GRID_HEIGHT + SPACE
BUTTON_WIDTH, BUTTON_HEIGHT, DIFFICULTY_BUTTON_HEIGHT = WIN_WIDTH/2, WIN_HEIGHT/4, WIN_HEIGHT/6
FPS = 60
SWIRL_SPEED = 100
COUNTER_RATIO = 9 # 66.66 pixels
COUNTER_WIDTH, COUNTER_HEIGHT = GRID_WIDTH/COUNTER_RATIO, GRID_HEIGHT/COUNTER_RATIO
OUTER_GAP = GRID_WIDTH/20.6 # 29 pixels
UPPER_GAP = GRID_HEIGHT/13.7 # 44 pixels
LOWER_GAP = GRID_HEIGHT/14.3 # 42 pixels
X_GAP = GRID_WIDTH/6 - OUTER_GAP/3 - COUNTER_WIDTH*7/6
Y_GAP = GRID_WIDTH/5 - UPPER_GAP/5 - LOWER_GAP/5 - COUNTER_HEIGHT*6/5
counter_list = []
EASY = 60
MEDIUM = 70
HARD = 90
NATHAN = 100

# board used for logic
BOARD_COLS, BOARD_ROWS = 7, 6
board = [['a' for c in range(BOARD_COLS)] for r in range(BOARD_ROWS)]

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)
LIGHT_BLUE = (173, 216, 230)

# window
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

class Counters:
    def __init__(self, file_name, img_width = COUNTER_WIDTH, img_height = COUNTER_HEIGHT):
        global counter_list
        self.png = file_name + '.png'
        self.img_width = img_width
        self.img_height = img_height
        self.img = pygame.transform.scale(pygame.image.load(os.path.join(PATH, 'images', self.png)), (img_width, img_height))
        counter_list.append(self.img)

# should probably make it so that it iterates through all images in the folder (make a new folder) instead of creating the instance each time
Counters('city_crest')
Counters('neon_city_crest')
Counters('arsenal')
Counters('football')
Counters('constantine')
Counters('flower')
Counters('sunflower')
Counters('donut')
Counters('earth')
Counters('pokeball')
Counters('yin_yang')
Counters('beach_ball')
Counters('tube')
Counters('watermelon')
Counters('swansea')
Counters('brazil')
Counters('emoji')
Counters('boo')
Counters('creeper')
Counters('hylian_shield')
Counters('tri-force')
Counters('kirby')
Counters('witcher')
Counters('yoshi')
Counters('darts')
Counters('orange')
Counters('portal')
Counters('smash_ball')
Counters('vinyl')
Counters('disco_ball')
Counters('eye')
Counters('8ball')
Counters('cookie')
# kiwi centre
# lemon centre
# coin
# pizza
# basketball
# moon
# mario fireball

class Text:
    def __init__(self, x, y, text_width, text_height, text, text_colour=BLACK, text_size=64):
        self.rect = pygame.Rect(x, y, text_width, text_height)
        self.text = text
        self.text_colour = text_colour
        self.text_size = text_size
        self.font = pygame.font.Font(None, self.text_size)
    
    def blit_text(self, screen):
        text_surface = self.font.render(self.text, True, self.text_colour)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

P1_COUNTER_TEXT = Text(WIN_WIDTH/2, SPACE/2, 0, 0, 'Player 1 select your counter', BLUE, int(GRID_HEIGHT/13))
P2_COUNTER_TEXT = Text(WIN_WIDTH/2, SPACE/2, 0, 0, 'Player 2 select your counter', WHITE, int(GRID_HEIGHT/13))
CPU_COUNTER_TEXT = Text(WIN_WIDTH/2, SPACE/2, 0, 0, 'Select CPU\'s counter', WHITE, int(GRID_HEIGHT/13))
P1_WINS_TEXT = Text(WIN_WIDTH/2, SPACE/2, 0, 0, 'Player 1 wins!', BLUE, int(GRID_HEIGHT/13))
P2_WINS_TEXT = Text(WIN_WIDTH/2, SPACE/2, 0, 0, 'Player 2 wins!', BLUE, int(GRID_HEIGHT/13))
CPU_WINS_TEXT = Text(WIN_WIDTH/2, SPACE/2, 0, 0, 'CPU wins!', BLUE, int(GRID_HEIGHT/13))

# blits all the counters on the screen based off of how many there are in total
def draw_counters(screen):
    counter_num = 0
    if len(counter_list) <= 25:
        total_col = 5
    elif len(counter_list) <= 36:
        total_col = 6
    elif len(counter_list) <= 49:
        total_col = 7
    else:
        print('too many counter options, can only have a max of 49')
    
    # blits the images spread out depending on how many counters there are
    if len(counter_list) % total_col > 0 and len(counter_list) % total_col < total_col / 2:
        total_row = round(len(counter_list) / total_col) + 1
    else:
        total_row = round(len(counter_list) / total_col)
    for r in range(total_row):
        for c in range(total_col):
            if counter_num < len(counter_list):
                x = GRID_WIDTH * (c + 1) / (total_col + 1) - COUNTER_WIDTH / 2
                y = GRID_HEIGHT * (r + 1) / (total_row + 1) - COUNTER_HEIGHT / 2 + SPACE
                screen.blit(counter_list[counter_num], (x, y))
                pygame.Rect(x, y, COUNTER_WIDTH, COUNTER_HEIGHT)
                counter_num += 1
            else:
                break

# where the winning swirls should be added
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

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# initialising the columns of a connect 4 board
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

# Function to check for a win
def check_win(player, counter, screen = WIN):
    global won
    global stage
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player):
                win_swirls_horizontal(screen, row, col)
                won = True

    # Check vertical
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if (board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player):
                win_swirls_vertical(screen, row, col)
                won = True

    # Check diagonal (positive slope)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player):
                win_swirls_diagonal_pos(screen, row, col)
                won = True

    # Check diagonal (negative slope)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player):
                win_swirls_diagonal_neg(screen, row, col)
                won = True

    if won:
        if player == 'p1':
            P1_WINS_TEXT.blit_text(screen)
        elif player == 'p2':
            P2_WINS_TEXT.blit_text(screen)
        elif player == 'cpu':
            CPU_WINS_TEXT.blit_text(screen)
        screen.blit(counter, (COUNTER_WIDTH*1.5, SPACE/2 - COUNTER_HEIGHT/2))
        screen.blit(counter, (GRID_WIDTH - COUNTER_WIDTH*2.5, SPACE/2 - COUNTER_HEIGHT/2))
        won = False
        stage = 5

class Button:
    def __init__(self, x, y, button_width, button_height, text, text_size=36, colour=WHITE, hover_colour=PINK, text_colour=BLACK):
        self.rect = pygame.Rect(x, y, button_width, button_height)
        self.text = text
        self.colour = colour
        self.hover_colour = hover_colour
        self.text_colour = text_colour
        self.font = pygame.font.Font(None, text_size)  # customize the font and size
        self.is_hovered = False

    def draw_button(self, screen):
        if self.is_hovered:
            pygame.draw.rect(screen, self.hover_colour, self.rect)
            pygame.draw.rect(screen, self.colour, self.rect, 10)  # Border
        else:
            pygame.draw.rect(screen, self.colour, self.rect)
            pygame.draw.rect(screen, self.hover_colour, self.rect, 10)  # Border
        self.draw_text(screen)

    def draw_text(self, screen):
        text_surface = self.font.render(self.text, True, self.text_colour)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

ONE_PLAYER_BUTTON = Button(WIN_WIDTH/2 - BUTTON_WIDTH/2, WIN_HEIGHT/3 - BUTTON_HEIGHT/2, BUTTON_WIDTH, BUTTON_HEIGHT, '1 Player Game', int(WIN_WIDTH/12))
TWO_PLAYER_BUTTON = Button(WIN_WIDTH/2 - BUTTON_WIDTH/2, WIN_HEIGHT*2/3 - BUTTON_HEIGHT/2, BUTTON_WIDTH, BUTTON_HEIGHT, '2 Player Game', int(WIN_WIDTH/12))
EASY_BUTTON = Button(WIN_WIDTH/2 - BUTTON_WIDTH/2, WIN_HEIGHT/5 - DIFFICULTY_BUTTON_HEIGHT/2, BUTTON_WIDTH, DIFFICULTY_BUTTON_HEIGHT, 'Easy', int(WIN_WIDTH/12), WHITE, LIGHT_BLUE)
MEDIUM_BUTTON = Button(WIN_WIDTH/2 - BUTTON_WIDTH/2, WIN_HEIGHT*2/5 - DIFFICULTY_BUTTON_HEIGHT/2, BUTTON_WIDTH, DIFFICULTY_BUTTON_HEIGHT, 'Medium', int(WIN_WIDTH/12), WHITE, LIGHT_BLUE)
HARD_BUTTON = Button(WIN_WIDTH/2 - BUTTON_WIDTH/2, WIN_HEIGHT*3/5 - DIFFICULTY_BUTTON_HEIGHT/2, BUTTON_WIDTH, DIFFICULTY_BUTTON_HEIGHT, 'Hard', int(WIN_WIDTH/12), WHITE, LIGHT_BLUE)
NATHAN_BUTTON = Button(WIN_WIDTH/2 - BUTTON_WIDTH/2, WIN_HEIGHT*4/5 - DIFFICULTY_BUTTON_HEIGHT/2, BUTTON_WIDTH, DIFFICULTY_BUTTON_HEIGHT, 'Nathan', int(WIN_WIDTH/12), WHITE, LIGHT_BLUE)
buttons = []
buttons.append(ONE_PLAYER_BUTTON)
buttons.append(TWO_PLAYER_BUTTON)
difficulty_buttons = []
difficulty_buttons.append(EASY_BUTTON)
difficulty_buttons.append(MEDIUM_BUTTON)
difficulty_buttons.append(HARD_BUTTON)
difficulty_buttons.append(NATHAN_BUTTON)

def main():

    clock = pygame.time.Clock()
    global frame_index
    global won
    global stage
    won = False
    p1_turn = True
    difficulty = 0
    stage = 0 # 0 = 1p or 2p game, 1 = p1 selects counter, 2 = p2 selects counter, 3 = draw connect4 board, 4 = plays the game
    # 5 = win message, 6 = cpu difficulty, 7 = player picks counter, 8 = cpu picks counter, 9 = randoms who goes first and draws connect4 board

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()

            elif event.type == pygame.MOUSEMOTION:
                # shows which button is being hovered over
                if stage == 0:
                    for b in buttons:
                        if b.rect.collidepoint(event.pos) and b.is_hovered == False:
                            b.is_hovered = True
                            b.draw_button(WIN)
                            pygame.display.update()
                        elif b.rect.collidepoint(event.pos) == False and b.is_hovered == True:
                            b.is_hovered = False
                            b.draw_button(WIN)
                            pygame.display.update()
                if stage == 6:
                    for b in difficulty_buttons:
                        if b.rect.collidepoint(event.pos) and b.is_hovered == False:
                            b.is_hovered = True
                            b.draw_button(WIN)
                            pygame.display.update()
                        elif b.rect.collidepoint(event.pos) == False and b.is_hovered == True:
                            b.is_hovered = False
                            b.draw_button(WIN)
                            pygame.display.update()

                # hovers the counter over the top
                if won == False and stage == 4:
                    for col in columns:
                        if p1_turn:
                            if col.rect.collidepoint(event.pos) and col.is_hovered == False:
                                col.is_hovered = True
                                col.draw_hover_counter(WIN, p1_counter)
                                pygame.display.update()
                            elif col.rect.collidepoint(event.pos) == False and col.is_hovered == True:
                                col.is_hovered = False
                        elif p1_turn == False:
                            if col.rect.collidepoint(event.pos) and col.is_hovered == False:
                                col.is_hovered = True
                                col.draw_hover_counter(WIN, p2_counter)
                                pygame.display.update()
                            elif col.rect.collidepoint(event.pos) == False and col.is_hovered == True:
                                col.is_hovered = False
                            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if stage == 0:
                    if ONE_PLAYER_BUTTON.is_clicked(pygame.mouse.get_pos()):
                        stage = 6
                    elif TWO_PLAYER_BUTTON.is_clicked(pygame.mouse.get_pos()):
                        stage = 1
                if stage == 6:
                    if EASY_BUTTON.is_clicked(pygame.mouse.get_pos()):
                        difficulty = EASY
                        stage = 7
                    elif MEDIUM_BUTTON.is_clicked(pygame.mouse.get_pos()):
                        difficulty = MEDIUM
                        stage = 7
                    elif HARD_BUTTON.is_clicked(pygame.mouse.get_pos()):
                        difficulty = HARD
                        stage = 7
                    elif NATHAN_BUTTON.is_clicked(pygame.mouse.get_pos()):
                        difficulty = NATHAN
                        stage = 7
                
                if stage == 1 or stage == 2 or stage == 7 or stage == 8:
                    # figures out how to arrange the number of counters on screen
                    counter_num = 0
                    if len(counter_list) <= 25:
                        total_col = 5
                    elif len(counter_list) <= 36:
                        total_col = 6
                    elif len(counter_list) <= 49:
                        total_col = 7
                    else:
                        print('too many counter options, can only have a max of 49')
                    # creates rects depending on how many counters there are and stores the selected counter
                    if len(counter_list) % total_col > 0 and len(counter_list) % total_col < total_col / 2:
                        total_row = round(len(counter_list) / total_col) + 1
                    else:
                        total_row = round(len(counter_list) / total_col)

                    if stage == 1:
                        for r in range(total_row):
                            for c in range(total_col):
                                if counter_num < len(counter_list):
                                    x = GRID_WIDTH * (c + 1) / (total_col + 1) - COUNTER_WIDTH / 2
                                    y = GRID_HEIGHT * (r + 1) / (total_row + 1) - COUNTER_HEIGHT / 2 + SPACE
                                    if pygame.Rect(x, y, COUNTER_WIDTH, COUNTER_HEIGHT).collidepoint(pygame.mouse.get_pos()):
                                        p1_counter = counter_list[counter_num]
                                        del counter_list[counter_num]
                                        p1_turn = False
                                        stage = 2
                                        WIN.fill(PINK)
                                        P2_COUNTER_TEXT.blit_text(WIN)
                                        draw_counters(WIN)
                                        pygame.display.update()
                                    counter_num += 1
                                else:
                                    break
                    if stage == 2:
                        for r in range(total_row):
                            for c in range(total_col):
                                if counter_num < len(counter_list):
                                    x = GRID_WIDTH * (c + 1) / (total_col + 1) - COUNTER_WIDTH / 2
                                    y = GRID_HEIGHT * (r + 1) / (total_row + 1) - COUNTER_HEIGHT / 2 + SPACE
                                    if pygame.Rect(x, y, COUNTER_WIDTH, COUNTER_HEIGHT).collidepoint(pygame.mouse.get_pos()):
                                        p2_counter = counter_list[counter_num]
                                        p1_turn = True
                                        stage = 3
                                    counter_num += 1
                                else:
                                    break

                    if stage == 7:
                        for r in range(total_row):
                            for c in range(total_col):
                                if counter_num < len(counter_list):
                                    x = GRID_WIDTH * (c + 1) / (total_col + 1) - COUNTER_WIDTH / 2
                                    y = GRID_HEIGHT * (r + 1) / (total_row + 1) - COUNTER_HEIGHT / 2 + SPACE
                                    if pygame.Rect(x, y, COUNTER_WIDTH, COUNTER_HEIGHT).collidepoint(pygame.mouse.get_pos()):
                                        p1_counter = counter_list[counter_num]
                                        del counter_list[counter_num]
                                        stage = 8
                                    counter_num += 1
                                else:
                                    break
                    if stage == 8:
                        for r in range(total_row):
                            for c in range(total_col):
                                if counter_num < len(counter_list):
                                    x = GRID_WIDTH * (c + 1) / (total_col + 1) - COUNTER_WIDTH / 2
                                    y = GRID_HEIGHT * (r + 1) / (total_row + 1) - COUNTER_HEIGHT / 2 + SPACE
                                    if pygame.Rect(x, y, COUNTER_WIDTH, COUNTER_HEIGHT).collidepoint(pygame.mouse.get_pos()):
                                        p2_counter = counter_list[counter_num] # cpu counter = p2_counter
                                        stage = 9
                                    counter_num += 1
                                else:
                                    break

                if won == False and stage == 4:
                    for col in columns:
                        if col.is_clicked(pygame.mouse.get_pos()) and col.row_counter > -1:
                            if p1_turn:
                                # G_FART_SOUND.play()
                                col.draw_actual_counter(WIN, p1_counter, 'p1')
                                p1_turn = False
                            elif p1_turn == False and difficulty == 0: # the 2 player version
                                # NI_HAO_SOUND.play()
                                col.draw_actual_counter(WIN, p2_counter, 'p2')
                                p1_turn = True
        if stage == 0:
            WIN.fill(BACKGROUND_COL)
            ONE_PLAYER_BUTTON.draw_button(WIN)
            TWO_PLAYER_BUTTON.draw_button(WIN)
            pygame.display.update()
        
        if stage == 1:
            WIN.fill(BACKGROUND_COL)
            P1_COUNTER_TEXT.blit_text(WIN)
            draw_counters(WIN)
            pygame.display.update()

        if stage == 3:
            WIN.fill(BACKGROUND_COL)
            WIN.blit(GRID, (0, SPACE))
            pygame.display.update()
            stage += 1
        
        if (stage == 4 or stage == 5) and difficulty == 0: # 2 player game
            check_win('p1', p1_counter)
            check_win('p2', p2_counter)
            if frame_index >= len(swirls):
                frame_index = 0
        
        if stage == 4 and difficulty != 0 and won == False: # vs cpu
            check_win('p1', p1_counter)
            check_win('cpu', p2_counter)
            if p1_turn == False and stage == 4:
                col = random.choice(columns)
                col.draw_actual_counter(WIN, p2_counter, 'cpu')
                p1_turn = True
        
        if stage == 5 and difficulty != 0: # vs cpu
            check_win('p1', p1_counter)
            check_win('cpu', p2_counter)
            if frame_index >= len(swirls):
                frame_index = 0
        
        if stage == 6:
            WIN.fill(PINK)
            EASY_BUTTON.draw_button(WIN)
            MEDIUM_BUTTON.draw_button(WIN)
            HARD_BUTTON.draw_button(WIN)
            NATHAN_BUTTON.draw_button(WIN)
            pygame.display.update()

        if stage == 7:
            WIN.fill(BACKGROUND_COL)
            P1_COUNTER_TEXT.blit_text(WIN)
            draw_counters(WIN)
            pygame.display.update()
        
        if stage == 8:
            WIN.fill(PINK)
            CPU_COUNTER_TEXT.blit_text(WIN)
            draw_counters(WIN)
            pygame.display.update()
        
        if stage == 9:
            WIN.fill(BACKGROUND_COL)
            WIN.blit(GRID, (0, SPACE))
            pygame.display.update()
            p1_turn = random.choice([True, False]) # randomises who goes first
            stage = 4

main()

# choose your counter and sound
# get a winning sound
# add in a play again button when the game is won
# create a cpu
# add in a delay between buttons being able to be pressed so that there's no accidental clicking twice
# finish doing the maximin coding, see https://www.youtube.com/watch?v=MMLtza3CZFM&ab_channel=KeithGalli
# edit the neon city crest image