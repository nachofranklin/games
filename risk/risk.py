import pygame
import os
import random

pygame.font.init()
pygame.mixer.init()

# variables
PATH = 'C:\\Users\\Natha\\Documents\\code\\GitHub\\games\\risk\\'
FPS = 60
STARTING_TROOPS = 30

# width and heights
WIN_WIDTH = 1250
WIN_HEIGHT = WIN_WIDTH * 2/3
MAP_WIDTH = WIN_WIDTH * 4/5
MAP_HEIGHT = WIN_HEIGHT
BUTTON_WIDTH = WIN_WIDTH/6
BUTTON_HEIGHT = WIN_HEIGHT/9
BORDER_WIDTH = int(WIN_WIDTH/200)
TROOP_COUNT_FONT_SIZE = int(WIN_WIDTH/50)
PLAYER_TURN_FONT_SIZE = int(WIN_WIDTH/20)
BUTTON_FONT_SIZE = int(BUTTON_WIDTH*2/9)

# x and y co-ordinates
MAP_X = WIN_WIDTH/5
MAP_Y = 0
BUTTON_X = MAP_X/2
PLAYER_TURN_Y = WIN_HEIGHT * 1/8
END_TURN_Y = WIN_HEIGHT * 2/8
ATTACK_Y = WIN_HEIGHT * 3/8
BACK_Y = WIN_HEIGHT * 4/8
ONE_DICE_Y = WIN_HEIGHT * 5/8
TWO_DICE_Y = WIN_HEIGHT * 6/8
THREE_DICE_Y = WIN_HEIGHT * 7/8

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Risk')

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)

# images
def image(file_name, img_width, img_height):
    img = pygame.image.load(os.path.join(PATH, 'images', f'{file_name}.png'))
    scaled_img = pygame.transform.scale(img, (img_width, img_height))
    return scaled_img

GAME_BOARD = image('risk_map', MAP_WIDTH, MAP_HEIGHT)
BUTTON_IMG = image('blue_button_black', BUTTON_WIDTH, BUTTON_HEIGHT)
BUTTON_HOVERED_IMG = image('blue_button_white', BUTTON_WIDTH, BUTTON_HEIGHT)

# sounds
pass

# classes

class Player:
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour
        self.players_turn = False
        self.owned_territories = 0
        self.completed_continents = []
    
    def show_players_turn(self):
        if self.players_turn:
            text_surface = pygame.font.Font(None, PLAYER_TURN_FONT_SIZE).render(str(self.name), True, self.colour)
            
            # Calculate the position to centre the text on the territory
            text_x = (WIN_WIDTH - MAP_WIDTH) // 2 - text_surface.get_width() // 2
            text_y = PLAYER_TURN_Y - text_surface.get_height() // 2
            
            # Blit the text onto the main screen at the calculated position
            WIN.blit(text_surface, (text_x, text_y))

    # select different territories
    # choose to attack a territory
    def select_territory_to_att(self, target):
        max_troops_to_att_with = 0
        for nt in target.neighbouring_territories:
            if nt.owner == self.name:
                max_troops_to_att_with += nt.troop_count - 1

        if target.owner != self.name and max_troops_to_att_with >= 1:
            # add att button
            pass

        self.no_of_att_dice(target, max_troops_to_att_with)

    def no_of_att_dice(self, target, max_troops_to_att_with):
        # max_troops_to_att_with = 0
        # for nt in target.neighbouring_territories:
        #     if nt.owner == self.name:
        #         max_troops_to_att_with += nt.troop_count - 1
        
        if max_troops_to_att_with == 1:
            # add 1 dice button
            pass
        elif max_troops_to_att_with == 2:
            # add 1 and 2 dice button
            pass
        elif max_troops_to_att_with >= 3:
            # add 1, 2 and 3 dice button
            pass
        # add the back button

p1 = Player('P1', BLUE)
p2 = Player('P2', WHITE)
p3 = Player('P3', GREEN)
p4 = Player('P4', ORANGE)

players = [obj for obj in globals().values() if isinstance(obj, Player)]

class Territory:
    def __init__(self, name, continent, neighbouring_territories, territory_x, territory_y, territory_width, territory_height):
        self.name = name
        self.continent = continent
        self.neighbouring_territories = neighbouring_territories
        self.territory_x = territory_x / 1000 * MAP_WIDTH + MAP_X
        self.territory_y = territory_y / 1000 * MAP_HEIGHT + MAP_Y
        self.territory_width = territory_width / 1000 * MAP_WIDTH
        self.territory_height = territory_height / 1000 * MAP_HEIGHT
        self.troop_count = 1
        self.owner = None
        self.is_selected = False
        self.sel_rect = pygame.Rect(self.territory_x, self.territory_y, self.territory_width, self.territory_height) # might need to make these self.
    
    def add_troops(self, count):
        self.troop_count += count

    def remove_troops(self, count):
        self.troop_count = max(0, self.troop_count - count)

    def change_owner(self, new_owner):
        self.owner = new_owner

    def draw_circle(self):
        circle_surface = pygame.Surface((self.territory_width, self.territory_height), pygame.SRCALPHA)
        
        pygame.draw.circle(
            circle_surface, 
            self.owner.colour, 
            (self.territory_width // 2, self.territory_height // 2),  # center of the territory
            min(self.territory_width, self.territory_height) // 3,  # radius based on territory size
            BORDER_WIDTH
        )
        
        WIN.blit(circle_surface, (self.territory_x, self.territory_y))
    
    def draw_troop_count(self):
        text_surface = pygame.font.Font(None, TROOP_COUNT_FONT_SIZE).render(str(self.troop_count), True, self.owner.colour)
        
        text_x = self.territory_x + (self.territory_width - text_surface.get_width()) // 2
        text_y = self.territory_y + (self.territory_height - text_surface.get_height()) // 2
        
        WIN.blit(text_surface, (text_x, text_y))

# North America
alaska = Territory('Alaska', 'North America', ['Northwest Territory', 'Alberta', 'Kamchatka'], 48, 114, 53, 81)
northwest_territory = Territory('Northwest Territory', 'North America', ['Alaska', 'Alberta', 'Ontario', 'Greenland'], 107, 124, 136, 56)
greenland = Territory('Greenland', 'North America', ['Northwest Territory', 'Ontario', 'Quebec', 'Iceland'], 297, 61, 100, 110)
alberta = Territory('Alberta', 'North America', ['Alaska', 'Northwest Territory', 'Ontario', 'Western United States'], 126, 193, 69, 80)
ontario = Territory('Ontario', 'North America', ['Alberta', 'Northwest Territory', 'Western United States', 'Eastern United States', 'Greenland', 'Quebec'], 196, 199, 58, 78)
quebec = Territory('Quebec', 'North America', ['Ontario', 'Eastern United States', 'Greenland'], 259, 209, 68, 89)
western_united_states = Territory('Western United States', 'North America', ['Alberta', 'Ontario', 'Eastern United States', 'Central America'], 123, 287, 69, 100)
eastern_united_states = Territory('Eastern United States', 'North America', ['Ontario', 'Quebec', 'Western United States', 'Central America'], 209, 318, 81, 90)
central_america = Territory('Central America', 'North America', ['Eastern United States', 'Western United States', 'Venezuela'], 134, 414, 70, 102)

# South America
venezuela = Territory('Venezuela', 'South America', ['Central America', 'Peru', 'Brazil'], 206, 517, 93, 51)
peru = Territory('Peru', 'South America', ['Venezuela', 'Brazil', 'Argentina'], 194, 592, 72, 105)
brazil = Territory('Brazil', 'South America', ['Venezuela', 'Peru', 'Argentina', 'North Africa'], 267, 573, 99, 145)
argentina = Territory('Argentina', 'South America', ['Peru', 'Brazil'], 235, 721, 60, 169)

# Europe
iceland = Territory('Iceland', 'Europe', ['Greenland', 'Great Britain', 'Scandinavia'], 402, 179, 49, 51)
scandinavia = Territory('Scandinavia', 'Europe', ['Iceland', 'Ukraine', 'Northern Europe', 'Great Britain'], 476, 143, 64, 108)
ukraine = Territory('Ukraine', 'Europe', ['Afghanistan', 'Ural', 'Southern Europe', 'Northern Europe', 'Scandinavia', 'Middle East'], 546, 157, 91, 225)
great_britain = Territory('Great Britain', 'Europe', ['Iceland', 'Western Europe', 'Northern Europe', 'Scandinavia'], 378, 242, 63, 112)
northern_europe = Territory('Northern Europe', 'Europe', ['Great Britain', 'Scandinavia', 'Ukraine', 'Southern Europe', 'Western Europe'], 462, 290, 72, 80)
western_europe = Territory('Western Europe', 'Europe', ['Great Britain', 'Southern Europe', 'Northern Europe', 'North Africa'], 397, 370, 68, 117)
southern_europe = Territory('Southern Europe', 'Europe', ['Western Europe', 'Northern Europe', 'Ukraine', 'Egypt', 'North Africa', 'Middle East'], 471, 375, 69, 95)

# Africa
north_africa = Territory('North Africa', 'Africa', ['Brazil', 'Western Europe', 'Southern Europe', 'Egypt', 'East Africa', 'Congo'], 409, 511, 94, 159)
egypt = Territory('Egypt', 'Africa', ['Southern Europe', 'Middle East', 'East Africa', 'North Africa'], 504, 523, 78, 62)
east_africa = Territory('East Africa', 'Africa', ['Egypt', 'Middle East', 'Madagascar', 'Congo', 'North Africa', 'South Africa'], 550, 597, 70, 89)
congo = Territory('Congo', 'Africa', ['North Africa', 'East Africa', 'South Africa'], 501, 687, 64, 67)
south_africa = Territory('South Africa', 'Africa', ['Congo', 'East Africa', 'Madagascar'], 504, 774, 94, 116)
madagascar = Territory('Madagascar', 'Africa', ['East Africa', 'South Africa'], 608, 801, 51, 99)

# Asia
ural = Territory('Ural', 'Asia', ['Ukraine', 'Siberia', 'China', 'Afghanistan'], 658, 170, 53, 120)
siberia = Territory('Siberia', 'Asia', ['Ural', 'Yakutsk', 'Irkutsk', 'Mongolia', 'China'], 712, 101, 59, 138)
yakutsk = Territory('Yakutsk', 'Asia', ['Siberia', 'Kamchatka', 'Irkutsk'], 774, 93, 64, 84)
kamchatka = Territory('Kamchatka', 'Asia', ['Yakutsk', 'Irkutsk', 'Mongolia', 'Japan', 'Alaska'], 846, 92, 93, 127)
irkutsk = Territory('Irkutsk', 'Asia', ['Siberia', 'Yakutsk', 'Kamchatka', 'Mongolia'], 772, 196, 53, 91)
mongolia = Territory('Mongolia', 'Asia', ['Irkutsk', 'Kamchatka', 'China', 'Siberia', 'Japan'], 771, 304, 93, 83)
japan = Territory('Japan', 'Asia', ['Mongolia', 'Kamchatka'], 881, 271, 50, 133)
afghanistan = Territory('Afghanistan', 'Asia', ['Ukraine', 'Ural', 'China', 'India', 'Middle East'], 638, 310, 73, 119)
china = Territory('China', 'Asia', ['Afghanistan', 'Ural', 'Siberia', 'Mongolia', 'Siam', 'India'], 730, 392, 124, 82)
middle_east = Territory('Middle East', 'Asia', ['Southern Europe', 'Ukraine', 'Afghanistan', 'India', 'East Africa', 'Egypt'], 583, 436, 89, 149)
india = Territory('India', 'Asia', ['Middle East', 'China', 'Siam', 'Afghanistan'], 679, 475, 93, 122)
siam = Territory('Siam', 'Asia', ['India', 'China', 'Indonesia'], 773, 501, 66, 115)

# Australia
indonesia = Territory('Indonesia', 'Australia', ['Siam', 'New Guinea', 'Western Australia'], 768, 658, 93, 98)
new_guinea = Territory('New Guinea', 'Australia', ['Indonesia', 'Western Australia', 'Eastern Australia'], 863, 624, 78, 84)
western_australia = Territory('Western Australia', 'Australia', ['Indonesia', 'New Guinea', 'Eastern Australia'], 823, 764, 70, 122)
eastern_australia = Territory('Eastern Australia', 'Australia', ['New Guinea', 'Western Australia'], 897, 739, 75, 151)

all_territories = [obj for obj in globals().values() if isinstance(obj, Territory)]

class Button:
    def __init__(self, name, button_x, button_y, button_width=BUTTON_WIDTH, button_height=BUTTON_HEIGHT):
        self.name = name
        self.button_x = button_x
        self.button_y = button_y
        self.button_width = button_width
        self.button_height = button_height
        self.button_img = BUTTON_IMG
        self.button_hovered_img = BUTTON_HOVERED_IMG
        self.rect = pygame.Rect(button_x - button_width/2, button_y - button_height/2, button_width, button_height)
        self.is_clicked = False
        self.is_hovered = False

    def draw_button(self):
        if self.is_hovered == False:
            WIN.blit(self.button_img, self.rect)
        elif self.is_hovered == True:
            WIN.blit(self.button_hovered_img, self.rect)
        self.blit_text()
    
    def blit_text(self):
        font = pygame.font.Font(None, BUTTON_FONT_SIZE)
        text_surface = font.render(self.name, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        WIN.blit(text_surface, text_rect)

# end turn, attack, 1 dice, 2 dice, 3 dice, back
end_turn_button = Button('End Turn', BUTTON_X, END_TURN_Y)
attack_button = Button('Attack', BUTTON_X, ATTACK_Y)
back_button = Button('Back', BUTTON_X, BACK_Y)
one_dice_button = Button('1 Dice', BUTTON_X, ONE_DICE_Y)
two_dice_button = Button('2 Dice', BUTTON_X, TWO_DICE_Y)
three_dice_button = Button('3 Dice', BUTTON_X, THREE_DICE_Y)

all_buttons = [obj for obj in globals().values() if isinstance(obj, Button)]

# functions

def randomise_territories():
    random.shuffle(all_territories)

    for i, territory in enumerate(all_territories):
        player = players[i % len(players)]  # Select player in a round-robin manner
        territory.change_owner(player)  # Assign territory to player
        player.owned_territories += 1
        
def randomise_troop_placement():
    for player in players:
        remaining_troops = STARTING_TROOPS - player.owned_territories
        player_territories = []
        for t in all_territories:
            if t.owner == player:
                player_territories.append(t)
        while remaining_troops > 0:
            selected_territory = random.choice(player_territories)
            selected_territory.add_troops(1)
            remaining_troops -= 1

def new_game_setup():
    randomise_territories()
    randomise_troop_placement()

new_game_setup()
print(f'{egypt.name}\'s owner is {egypt.owner.name} with {egypt.troop_count} troops')
print(f'{ontario.name}\'s owner is {ontario.owner.name} with {ontario.troop_count} troops')
print(f'{great_britain.name}\'s owner is {great_britain.owner.name} with {great_britain.troop_count} troops')
p2.players_turn = True
        
def main():

    clock = pygame.time.Clock()
    clicked = False
    run = True
    WIN.blit(GAME_BOARD, (MAP_X, MAP_Y))
    for player in players:
        player.show_players_turn()
    for t in all_territories:
        t.draw_circle()
        t.draw_troop_count()
    for b in all_buttons:
        b.draw_button()
    pygame.display.update()
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()

            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Print the x and y coordinates to the console
                print(f'Mouse coordinates: X={mouse_x}, Y={mouse_y}')

                for territory in all_territories:
                    if territory.sel_rect.collidepoint(event.pos):
                        # print(territory.name)
                        pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass

            elif event.type == pygame.MOUSEBUTTONUP: # prevents one click doing multiple actions
                if clicked == True:
                    clicked = False

        # non button clicking code


main()