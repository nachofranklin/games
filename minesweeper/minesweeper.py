import pygame
import os
import random
import numpy as np
import pandas as pd
import ast

pygame.font.init()
pygame.mixer.init()

# changeable variables
PATH = f'C:{os.sep}Users{os.sep}Natha{os.sep}Documents{os.sep}code{os.sep}GitHub{os.sep}games{os.sep}minesweeper'
GRID_WIDTH = GRID_HEIGHT = 700
GRID_ROWS = GRID_COLS = 10
no_of_bombs = 17

# width and heights
TOP_SECTION = GRID_HEIGHT / (GRID_ROWS - 2)
WIN_WIDTH = GRID_WIDTH
WIN_HEIGHT = GRID_HEIGHT + TOP_SECTION
TILE_WIDTH = GRID_WIDTH/GRID_COLS
TILE_HEIGHT = GRID_HEIGHT/GRID_ROWS
BUTTON_WIDTH = WIN_WIDTH/2
BUTTON_HEIGHT = WIN_HEIGHT/9
CHANGE_USER_WIDTH = BUTTON_WIDTH
CHANGE_USER_HEIGHT = BUTTON_HEIGHT
TINY_SPACE = WIN_WIDTH/100
STATS_HEIGHT = WIN_HEIGHT - BUTTON_HEIGHT - WIN_HEIGHT/15 # win space less the home button

# x and y coordinates
BUTTON_X = WIN_WIDTH/2
NEW_GAME_Y = WIN_HEIGHT * 1/5
YOUR_STATS_Y = WIN_HEIGHT * 2/5
GLOBAL_STATS_Y = WIN_HEIGHT * 3/5
CHANGE_USER_Y = WIN_HEIGHT * 4/5
HOME_Y = WIN_HEIGHT - BUTTON_HEIGHT/2 - WIN_HEIGHT/30
USERNAME_Y = WIN_HEIGHT/13

# other variables
FPS = 60
grid = np.zeros((GRID_ROWS, GRID_COLS))
revealed = np.zeros((GRID_ROWS, GRID_COLS))
clicked = False
flag_counter = 0
flag_hovered = False
flag_clicked = False
game_over = False
timer_started = False
revealed_count = 0
timer_text_pos = (WIN_WIDTH/4, TOP_SECTION/2)
flag_text_pos = (WIN_WIDTH*3/4, TOP_SECTION/2)
font_size = int(TOP_SECTION)
PAGES = ['home', 'game', 'your_stats', 'global_stats', 'change_user']
PERSONAL_STATS = ['Games played', 'Games won', 'Games lost', 'Win rate', 'Best time', 'Average time', 'Longest win streak', 'Longest loss streak', 'Last game result']
GLOBAL_STATS = ['Top 10 Times', 'Best win rate', 'Fastest average time', 'Longest win streak', 'Longest loss streak', 'Total games played', 'Total games won', 'Total games lost'] # needs to show category, person and result
BUTTON_FONT_SIZE = int(WIN_WIDTH/16)
STATS_FONT_SIZE = int(WIN_WIDTH/16)
default_values = {
    "username": None,
    "play_history": '[]',
    "games_played": 0,
    "games_won": 0,
    "games_lost": 0,
    "win_rate": 0.0,
    "best_time": None,
    "avg_time": None,
    "longest_win_streak": 0,
    "longest_losing_streak": 0,
    "last_game_result": None,
    "last_to_play": "No",
}
change_user_box = pygame.Rect(WIN_WIDTH/2 - CHANGE_USER_WIDTH/2, WIN_HEIGHT/2 - CHANGE_USER_HEIGHT/2, CHANGE_USER_WIDTH, CHANGE_USER_HEIGHT)
change_user_active = False
BLANK_USERNAME = ''
USERNAME_PROMPT = 'Type username here...'
change_user_font = pygame.font.Font(None, BUTTON_FONT_SIZE)

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Minesweeper')

# csv to df
stats_df = pd.read_csv(os.path.join(PATH, 'minesweeper_statistics.csv'), delimiter=',')
stats_df.index = stats_df['username']

def get_user():
    user = 'Test1' # solves the issue of if someone changes user but closes it down before playing (as last_to_play would be 'No' for everyone)
    for c, r in stats_df.iterrows():
        if r['last_to_play'] == 'Yes':
            user = r['username']
            break
    return user
user = get_user()

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
        self.flag_img = pygame.transform.scale(pygame.image.load(os.path.join(PATH, 'img', 'flag_pink.png')), (img_width, img_height))
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
zero = Tile_results('zero_green')
one = Tile_results('one')
two = Tile_results('two')
three = Tile_results('three')
four = Tile_results('four')
five = Tile_results('five')
six = Tile_results('six')
seven = Tile_results('seven')
eight = Tile_results('eight')

def image(file_name, img_width, img_height):
    img = pygame.image.load(os.path.join(PATH, 'img', f'{file_name}.png'))
    scaled_img = pygame.transform.scale(img, (img_width, img_height))
    return scaled_img

BUTTON_IMG = image('blue_button_black', BUTTON_WIDTH, BUTTON_HEIGHT)
BUTTON_HOVERED_IMG = image('blue_button_white', BUTTON_WIDTH, BUTTON_HEIGHT)

class Button:
    def __init__(self, name, page, button_x, button_y, button_width=BUTTON_WIDTH, button_height=BUTTON_HEIGHT):
        self.name = name
        self.page = page
        self.button_x = button_x
        self.button_y = button_y
        self.button_width = button_width
        self.button_height = button_height
        self.button_img = BUTTON_IMG
        self.button_hovered_img = BUTTON_HOVERED_IMG
        self.rect = pygame.Rect(button_x - button_width/2, button_y - button_height/2, button_width, button_height)
        self.is_clicked = False
        self.is_hovered = False
        self.is_visible = False

    def draw_button(self):
        if self.is_visible:
            if self.is_hovered or self.is_clicked:
                WIN.blit(self.button_hovered_img, self.rect)
            elif self.is_hovered == False:
                WIN.blit(self.button_img, self.rect)
            self.blit_text()
    
    def blit_text(self):
        font = pygame.font.Font(None, BUTTON_FONT_SIZE)
        text_surface = font.render(self.name, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        WIN.blit(text_surface, text_rect)

home_button = Button('Home', 'home', BUTTON_X, HOME_Y)
new_game_button = Button('New Game', 'game', BUTTON_X, NEW_GAME_Y)
your_statistics_button = Button('Your Statistics', 'your_stats', BUTTON_X, YOUR_STATS_Y)
global_statistics_button = Button('Global Statistics', 'global_stats', BUTTON_X, GLOBAL_STATS_Y)
change_user_button = Button('Change User', 'change_user', BUTTON_X, CHANGE_USER_Y)

all_buttons = [obj for obj in globals().values() if isinstance(obj, Button)]

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

# functions

def draw_text(text, position, colour = BLUE, font_size = font_size, screen = WIN):
    """function for timer and flag counter / total bombs"""
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

def add_bombs():
    """randomises where the bombs are and counts the number of adjacent bombs in every tile"""
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
    """when a zero is clicked this will reveal all adjacent zeros and the next adjacent non zero values"""
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

def you_lose(screen):
    """performs the losing animation"""
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
    """performs the winning animation"""
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
    """formats and blits the timer for minesweeper in mins and seconds"""
    timer_seconds = (pygame.time.get_ticks() - start_time) / 1000
    minutes, seconds = divmod(timer_seconds, 60)
    formatted_time = "{:02}:{:02}".format(int(minutes), int(seconds))
    draw_text(f"{formatted_time}", timer_text_pos)
    pygame.display.update()

def mins_and_seconds(seconds: float):
    """converts seconds into a minutes and seconds format"""
    mins, secs = divmod(seconds, 60)
    formatted_time = "{}m {:04.1f}s".format(int(mins), secs)
    return formatted_time

def changing_username():
    """shows the username a user is typing out as they type it"""
    WIN.fill(LIGHT_BLUE)
    home_button.draw_button()
    pygame.draw.rect(WIN, BLUE if change_user_active else PINK, change_user_box, 5)
    txt_surface = change_user_font.render(user, True, BLACK)
    WIN.blit(txt_surface, (WIN_WIDTH/2 - txt_surface.get_width()/2, WIN_HEIGHT/2 - txt_surface.get_height()/2))
    change_user_box.w = max(CHANGE_USER_WIDTH, txt_surface.get_width() + 20)

def show_username(user, x=BUTTON_X, y=USERNAME_Y):
    """blits the current users username"""
    font = pygame.font.Font(None, int(BUTTON_FONT_SIZE))
    text_surface = font.render(user, True, BLACK)
    text_rect = text_surface.get_rect(center=pygame.Rect(x, y, 0, 0).center)
    WIN.blit(text_surface, text_rect)

def get_personal_stats_dict(user):
    """retreives stats from stats_df to determine certain best/worst statistics for the current user\n
    PERSONAL_STATS = ['Games played', 'Games won', 'Games lost', 'Win rate', 'Best time', 'Average time', 'Longest win streak', 'Longest losing streak', 'Last game result']"""
    personal_stats_dict = {d: None for d in PERSONAL_STATS}
    personal_stats_dict['Games played'] = stats_df.loc[user, 'games_played']
    personal_stats_dict['Games won'] = stats_df.loc[user, 'games_won']
    personal_stats_dict['Games lost'] = stats_df.loc[user, 'games_lost']
    personal_stats_dict['Win rate'] = f"{stats_df.loc[user, 'win_rate']}%"
    personal_stats_dict['Best time'] = f"{mins_and_seconds(stats_df.loc[user, 'best_time'])}"
    personal_stats_dict['Average time'] = f"{mins_and_seconds(stats_df.loc[user, 'avg_time'])}"
    personal_stats_dict['Longest win streak'] = stats_df.loc[user, 'longest_win_streak']
    personal_stats_dict['Longest loss streak'] = stats_df.loc[user, 'longest_losing_streak']
    personal_stats_dict['Last game result'] = stats_df.loc[user, 'last_game_result']
    return personal_stats_dict

def blit_personal_stats(personal_stats_dict, colour=BLACK):
    """blits each statistic from the personal_stats_dict"""
    font = pygame.font.Font(None, STATS_FONT_SIZE)
    x = WIN_WIDTH * 3/5
    index = 0
    for i in personal_stats_dict:
        y = STATS_HEIGHT * (index+1) / (len(personal_stats_dict)+1)
        index += 1
        desc_surface = font.render(f'{i} ', True, colour)
        desc_rect = desc_surface.get_rect()
        desc_rect.midright = (x, y)
        WIN.blit(desc_surface, desc_rect) # blits the stat description
        stat_surface = font.render(f'- {personal_stats_dict[i]}', True, colour)
        stat_rect = stat_surface.get_rect()
        stat_rect.midleft = (x, y)
        WIN.blit(stat_surface, stat_rect) # blits the stat

def get_global_stats_dict():
    """retreives stats from stats_df to determine certain best/worst statistics across all users\n
    GLOBAL_STATS = ['Top 10 Times', 'Best win rate', 'Fastest average time', 'Longest win streak', 'Longest loss streak', 'Total games played', 'Total games won', 'Total games lost']"""
    global_stats_dict = {d: None for d in GLOBAL_STATS}
    best_times_dict = get_best_times_dict()
    best_times_list = []
    for time, list in best_times_dict.items():
        for user in list:
            if len(best_times_list) < 10:
                best_times_list.append(f'{mins_and_seconds(time)} - {user}')
    global_stats_dict['Top 10 Times'] = best_times_list
    global_stats_dict['Best win rate'] = f"{stats_df['win_rate'].max()}% - {stats_df[stats_df['win_rate'] == stats_df['win_rate'].max()].index[0]}"
    global_stats_dict['Fastest average time'] = f"{mins_and_seconds(stats_df['avg_time'].min())} - {stats_df[stats_df['avg_time'] == stats_df['avg_time'].min()].index[0]}"
    global_stats_dict['Longest win streak'] = f"{stats_df['longest_win_streak'].max()} - {stats_df[stats_df['longest_win_streak'] == stats_df['longest_win_streak'].max()].index[0]}"
    global_stats_dict['Longest loss streak'] = f"{stats_df['longest_losing_streak'].max()} - {stats_df[stats_df['longest_losing_streak'] == stats_df['longest_losing_streak'].max()].index[0]}"
    global_stats_dict['Total games played'] = f"{stats_df['games_played'].sum()}"
    global_stats_dict['Total games won'] = f"{stats_df['games_won'].sum()}"
    global_stats_dict['Total games lost'] = f"{stats_df['games_lost'].sum()}"
    return global_stats_dict

def blit_global_stats(global_stats_dict, colour=BLACK):
    """blits each statistic from the global_stats_dict"""
    font = pygame.font.Font(None, STATS_FONT_SIZE)
    x = WIN_WIDTH * 3/5 # need to remove this as it's pointless
    index = 6 # will probably need to change this

    for i in global_stats_dict:
        if i == 'Top 10 Times':
            x = WIN_WIDTH/2
            y = STATS_HEIGHT * 1 / (len(global_stats_dict)+6)
            top10_surface = font.render(f'{i} / seconds', True, colour)
            top10_rect = top10_surface.get_rect()
            top10_rect.center = (x, y)
            WIN.blit(top10_surface, top10_rect) # blits the top 10 times str
            ranking = 1
            for time in global_stats_dict[i]: # this is just iterating through the list of 'fastest times - user'
                if ranking < (len(global_stats_dict[i])+1) / 2:
                    x = WIN_WIDTH * 1/4
                    y = STATS_HEIGHT * (ranking+1) / (len(global_stats_dict)+6)
                    top10_surface = font.render(f'{ranking}) {time}', True, colour)
                    top10_rect = top10_surface.get_rect()
                    top10_rect.center = (x, y)
                    WIN.blit(top10_surface, top10_rect) # blits the top 1st - 5th times on the left
                    ranking += 1
                else:
                    x = WIN_WIDTH * 3/4
                    y = STATS_HEIGHT * (ranking+1-5) / (len(global_stats_dict)+6)
                    top10_surface = font.render(f'{ranking}) {time}', True, colour)
                    top10_rect = top10_surface.get_rect()
                    top10_rect.center = (x, y)
                    WIN.blit(top10_surface, top10_rect) # blits the top 6th - 10th times on the right
                    ranking += 1
        else:
            x = WIN_WIDTH * 1/2
            y = STATS_HEIGHT * (index+1) / (len(global_stats_dict)+6)
            index += 1
            stat_surface = font.render(f'{i} - {global_stats_dict[i]}', True, colour)
            stat_rect = stat_surface.get_rect()
            stat_rect.center = (x, y)
            WIN.blit(stat_surface, stat_rect) # blits the stat

            # below comments is splitting it like personal stats but i don't think it looked as good (x = 4/7)
            # desc_surface = font.render(f'{i} ', True, colour)
            # desc_rect = desc_surface.get_rect()
            # desc_rect.midright = (x, y)
            # WIN.blit(desc_surface, desc_rect) # blits the stat description
            # stat_surface = font.render(f'- {global_stats_dict[i]}', True, colour)
            # stat_rect = stat_surface.get_rect()
            # stat_rect.midleft = (x, y)
            # WIN.blit(stat_surface, stat_rect) # blits the stat

def get_best_times_dict():
    """returns a dict of seconds taken: list(users), sorted quickest to slowest of all users"""
    times_dict = {}
    df = stats_df['play_history'].apply(ast.literal_eval)
    for user in stats_df['username']:
        for time in df[user]:
            if time == 'Fail':
                pass # if fail, skip
            elif time in times_dict:
                times_dict[time] += [user] # if the time already exists then add the user to the time
            else:
                times_dict[time] = [user] # if the time doesn't already exist then add the user: time
    best_times_dict = dict(sorted(times_dict.items())) # sorts the dict quickest to slowest
    return best_times_dict

def change_page(page):
    """blits all required elements when changing to a new page\n
    PAGES = ['home', 'game', 'your_stats', 'global_stats', 'change_user']"""
    global user
    hide_all_buttons()
    WIN.fill(LIGHT_BLUE)

    if page == 'home':
        new_game_button.is_visible = True
        your_statistics_button.is_visible = True
        global_statistics_button.is_visible = True
        change_user_button.is_visible = True
        new_game_button.draw_button()
        your_statistics_button.draw_button()
        global_statistics_button.draw_button()
        change_user_button.draw_button()
        show_username(user)

    elif page == 'game':
        new_game()
        for tile in tile_list:
            tile.is_flagged = False
            tile.is_hovered = False
            tile.draw_tile(WIN)
        WIN.blit(flag.img, flag_rect) # blits the top x/17 flag bit
        draw_text(f'{flag_counter} / {no_of_bombs}', flag_text_pos)

    elif page == 'your_stats':
        home_button.is_visible = True
        home_button.draw_button()
        blit_personal_stats(get_personal_stats_dict(user))

    elif page == 'global_stats':
        home_button.is_visible = True
        home_button.draw_button()
        blit_global_stats(get_global_stats_dict())

    elif page == 'change_user':
        stats_df.loc[stats_df['username'] == user, 'last_to_play'] = 'No'
        user = USERNAME_PROMPT
        home_button.is_visible = True
        changing_username()
        # need to check if they're a new player or not

    pygame.display.update()

def new_game():
    """resets everything and generates a new randomised minesweeper game"""
    global grid
    global revealed
    global flag_counter
    global flag_hovered
    global flag_clicked
    global game_over
    global timer_started
    global revealed_count

    grid = np.zeros((GRID_ROWS, GRID_COLS))
    revealed = np.zeros((GRID_ROWS, GRID_COLS))
    add_bombs()
    flag_counter = 0
    flag_hovered = False
    flag_clicked = False
    game_over = False
    timer_started = False
    revealed_count = 0

def hide_all_buttons():
    """sets all buttons visibily (is_visible) to False, awaiting them to be turned on afterwards where needed"""
    for b in all_buttons:
        b.is_visible = False
        b.is_hovered = False

def update_df(last_game='Fail'):
    """takes the value of the last game, either a str 'Fail' or an int of number of seconds taken to win and updates the stats_df"""
    global user
    if user not in stats_df['username']:
        default_values['username'] = user
        stats_df.loc[user] = default_values

    play_history = stats_df.loc[stats_df['username'] == user, 'play_history'].apply(ast.literal_eval) # this seems to work by converting all lists into a string either from getting the csv or adding a new user, then this way it only changes it to a list for the current row then it turns it back into a string and that seems to work
    updated_play_history = play_history[0].copy() # otherwise .iloc applies the append to everything in the column
    updated_play_history.append(last_game)
    stats_df.loc[stats_df['username'] == user, 'play_history'] = f'{updated_play_history}'
    stats_df.loc[stats_df['username'] == user, 'games_played'] += 1
    if last_game != 'Fail':
        stats_df.loc[stats_df['username'] == user, 'games_won'] += 1
    elif last_game == 'Fail':
        stats_df.loc[stats_df['username'] == user, 'games_lost'] += 1
    stats_df.loc[stats_df['username'] == user, 'win_rate'] = round(stats_df.loc[stats_df['username'] == user, 'games_won'] / stats_df.loc[stats_df['username'] == user, 'games_played'] * 100, 1)
    best_time = 100000
    total_time = 0
    for i in updated_play_history:
        if i == 'Fail':
            continue
        else:
            total_time += i
            if i < best_time:
                best_time = i
    if total_time == 0:
        stats_df.loc[stats_df['username'] == user, 'best_time'] = None
        stats_df.loc[stats_df['username'] == user, 'avg_time'] = None
    else:
        stats_df.loc[stats_df['username'] == user, 'best_time'] = best_time
        stats_df.loc[stats_df['username'] == user, 'avg_time'] = round(total_time / stats_df.loc[stats_df['username'] == user, 'games_won'], 1)
    longest_win_streak = 0
    longest_loss_streak = 0
    current_streak = 0
    current_type = None
    for i in updated_play_history:
        if i == 'Fail':
            if current_type == 'loss':
                current_streak += 1
                if current_streak > longest_loss_streak:
                    longest_loss_streak = current_streak
            else:
                current_type = 'loss'
                current_streak = 1
                if current_streak > longest_loss_streak:
                    longest_loss_streak = current_streak
        else:
            if current_type == 'win':
                current_streak += 1
                if current_streak > longest_win_streak:
                    longest_win_streak = current_streak
            else:
                current_type = 'win'
                current_streak = 1
                if current_streak > longest_win_streak:
                    longest_win_streak = current_streak
    stats_df.loc[stats_df['username'] == user, 'longest_win_streak'] = longest_win_streak
    stats_df.loc[stats_df['username'] == user, 'longest_losing_streak'] = longest_loss_streak
    if last_game == 'Fail':
        stats_df.loc[stats_df['username'] == user, 'last_game_result'] = last_game
    else:
        stats_df.loc[stats_df['username'] == user, 'last_game_result'] = mins_and_seconds(last_game)
    stats_df.loc[stats_df['username'] == user, 'last_to_play'] = 'Yes'

def update_csv():
    """overwrites the minesweeper_statistics.csv file with the stats_df data"""
    stats_df.to_csv(os.path.join(PATH, 'minesweeper_statistics.csv'), index=False)


def main():
    """plays minesweeper"""
    clock = pygame.time.Clock()
    global flag_counter
    global flag_hovered
    global flag_clicked
    global game_over
    global timer_started
    global revealed_count
    global user
    page = 'home'
    change_page(page)
    clicked = False
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if timer_started and game_over == False:
                    update_df()
                    update_csv()
                run = False
                exit()

            elif event.type == pygame.MOUSEMOTION:
                for b in all_buttons:
                    if b.is_visible:
                        # show if the button is being hovered over
                        if b.rect.collidepoint(event.pos) and b.is_hovered == False:
                            b.is_hovered = True
                            b.draw_button()
                            pygame.display.update()
                        elif b.rect.collidepoint(event.pos) == False and b.is_hovered:
                            b.is_hovered = False
                            b.draw_button()
                            pygame.display.update()

                if page == 'game':
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
                for b in all_buttons:
                    if b.is_visible and b.is_hovered and clicked == False:
                        clicked = True
                        if page == 'change_user' and (user == USERNAME_PROMPT or user == BLANK_USERNAME):
                            pass # doesn't allow a blank or prompt username
                        else:
                            page = b.page
                            change_page(page)
                
                if page == 'change_user':
                    if change_user_box.collidepoint(event.pos) and clicked == False:
                        clicked = True
                        global change_user_active
                        change_user_active = True # changes the colour of the border when clicked
                        if user == USERNAME_PROMPT:
                            user = BLANK_USERNAME # removes the prompt when the box is clicked
                        changing_username()
                    else:
                        clicked = True
                        change_user_active = False
                        changing_username()
                    pygame.display.update()

                elif page == 'game':
                    if game_over == False and clicked == False:
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
                                            update_df()
                                            game_over = True
                                            update_csv()
                                            home_button.is_visible = True
                                            home_button.draw_button()
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

            elif event.type == pygame.KEYDOWN:
                if change_user_active and page == 'change_user':
                    if event.key == pygame.K_RETURN:
                        if page == 'change_user' and (user == USERNAME_PROMPT or user == BLANK_USERNAME):
                            pass
                        else:
                            page = 'home' # Exit to home screen unless username is blank or prompt
                            change_page(page)
                    elif event.key == pygame.K_BACKSPACE:
                        user = user[:-1]
                        changing_username()
                    else:
                        if len(user) < 10:
                            user += event.unicode.upper()
                            changing_username()
                    pygame.display.flip()
            
            elif event.type == pygame.MOUSEBUTTONUP: # prevents one click doing multiple actions
                clicked = False

        # checking if you win
        if page == 'game':
            revealed_count = 0
            for tile in tile_list:
                if revealed[tile.row][tile.col] == 1:
                    revealed_count += 1
            if revealed_count == GRID_ROWS * GRID_COLS - no_of_bombs and game_over == False:
                end_time = pygame.time.get_ticks()
                total_seconds = round((end_time - start_time) / 1000, 1)
                update_df(total_seconds)
                you_win(WIN)
                game_over = True
                update_csv()
                home_button.is_visible = True
                home_button.draw_button()
                pygame.display.update()

            # starting/stopping the timer
            if timer_started and game_over == False:
                start_timer(start_time)

main()

# best scores (10x10 with 17 bombs)

# nathan - 1.17, 1.28, 1.30
# georgie - 0.00, 0.18
# ellie - 4.52
# almantas - 1.30

# i think if you change user to a new user and check stats before playing a game it crashes
# need to change it in case someone checks their stats while not having won a game
# maybe add in current win and loss streak to personal stats (changing the longest win streak to longest (current) win streak)