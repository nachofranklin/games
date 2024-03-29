import pygame
import os
import random
import numpy as np

pygame.font.init()
pygame.mixer.init()

# variables
PATH = '/home/nacho/repos/games/deck_builder/'

FPS = 60
MAX_CARDS_IN_HAND = 10
card_id_counter = 1
BASE_DRAW_CARDS = 5 # 5
list_of_all_cards = []
DISPLAY_CARDS = 6 # determines how many cards in a row get shown when clicking on draw pile etc
current_enemies = []

# width and heights
WIN_WIDTH = 1200
WIN_HEIGHT = 800 # might make it so that this is a fraction of win_width rather than a changeable value
CARD_WIDTH = WIN_WIDTH/10 # 120
CARD_HEIGHT = WIN_HEIGHT/4
CHARACTER_WIDTH = WIN_WIDTH/3
CHARACTER_HEIGHT = WIN_HEIGHT/3
EFFECTS_WIDTH = EFFECTS_HEIGHT = WIN_WIDTH/27
END_TURN_WIDTH = CARD_WIDTH
END_TURN_HEIGHT = CARD_HEIGHT/3
ENERGY_WIDTH = ENERGY_HEIGHT = WIN_HEIGHT/20 # radius
DESCRIPTION_WIDTH = CARD_WIDTH*2/3*9 + CARD_WIDTH # 840
DESCRIPTION_HEIGHT = CARD_HEIGHT/8
DRAW_PILE_WIDTH = DRAW_PILE_HEIGHT = CARD_WIDTH*3/4
DISPLAY_GAP_WIDTH = (DESCRIPTION_WIDTH - CARD_WIDTH*DISPLAY_CARDS) / (DISPLAY_CARDS - 1)
DISPLAY_GAP_HEIGHT = WIN_HEIGHT/5 - CARD_HEIGHT/2

# x and y co-ordinates
P1_X = WIN_WIDTH/9
P1_Y = ENEMY1_Y = WIN_HEIGHT/9
ENEMY1_X = WIN_WIDTH*5/9
EFFECTS_Y = P1_Y + CHARACTER_HEIGHT
# CARDS_X is a bit more complicated
CARDS_Y = WIN_HEIGHT*4/5 - CARD_HEIGHT/2
END_TURN_X = WIN_WIDTH - END_TURN_WIDTH*1.25
END_TURN_Y = WIN_HEIGHT*3/5 - END_TURN_HEIGHT*1.25
DESCRIPTION_X = WIN_WIDTH/2 - CARD_WIDTH/2 - CARD_WIDTH/3 - CARD_WIDTH*2/3*MAX_CARDS_IN_HAND/2 + CARD_WIDTH*2/3*1
DESCRIPTION_Y = WIN_HEIGHT*4/5 - CARD_HEIGHT/2 - CARD_HEIGHT/4
LEFT_BUTTON_X = DESCRIPTION_X/2 - DRAW_PILE_WIDTH/2
RIGHT_BUTTON_X = WIN_WIDTH - DESCRIPTION_X/2 - DRAW_PILE_WIDTH/2
TOP_BUTTON_Y = CARDS_Y
BOTTOM_BUTTON_Y = CARDS_Y + CARD_HEIGHT - DRAW_PILE_HEIGHT

rarity_types = []
common = 'common'
uncommon = 'uncommon'
rare = 'rare'
starter = 'starter'
curse = 'curse'
rarity_types.append(common)
rarity_types.append(uncommon)
rarity_types.append(rare)
rarity_types.append(starter)
rarity_types.append(curse)

card_types = []
attack = 'attack'
skill = 'skill'
power = 'power'
curse = 'curse'
card_types.append(attack)
card_types.append(skill)
card_types.append(power)
card_types.append(curse)

attack_options = []
select = 'select'
all = 'all'
rando = 'random'
attack_options.append(select)
attack_options.append(all)
attack_options.append(rando)

# screen_view
home = 'home'
map = 'map'
fight = 'fight'
reward = 'reward'
card_view = 'card_view'
shop = 'shop'
event = 'event'
death = 'death'
win = 'win'

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Nath\'s STS')

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
def image(file_name, img_width=EFFECTS_WIDTH, img_height=EFFECTS_HEIGHT):
    img = pygame.image.load(os.path.join(PATH, 'images', f'{file_name}.png'))
    scaled_img = pygame.transform.scale(img, (img_width, img_height))
    return scaled_img

BLOCK = image('block')
SHIELD = image('shield')
STRENGTH = image('strength')
DEXTERITY = image('dexterity')
WEAK = image('weak')
VULNERABLE = image('vulnerable')
FRAIL = image('frail')
POISON = image('poison')
THORNS = image('thorns')
ADDITIONAL_ENERGY = image('energy')
DRAW_PILE = image('draw_pile', DRAW_PILE_WIDTH, DRAW_PILE_HEIGHT)
DISCARD_PILE = image('discard_pile', DRAW_PILE_WIDTH, DRAW_PILE_HEIGHT)
EXHAUST_PILE = image('tombstone', DRAW_PILE_WIDTH, DRAW_PILE_HEIGHT)
ENTIRE_DECK = image('entire_deck', DRAW_PILE_WIDTH, DRAW_PILE_HEIGHT)
ENERGY = image('sun', DRAW_PILE_WIDTH, DRAW_PILE_HEIGHT)
PIRATE_BACKGROUND = image('pirate_background', WIN_WIDTH, WIN_HEIGHT)

# sounds
pass

# classes
class Card:
    def __init__(self, name, energy, rarity, type, short_description, long_description, picture=None, player_hp=0, enemy_hp=0, block=0, shield=0, player_strength=0, enemy_strength=0, player_dexterity=0, enemy_dexterity=0, player_weak=0, enemy_weak=0, player_vulnerable=0, enemy_vulnerable=0, player_frail=0, enemy_frail=0, player_poison=0, enemy_poison=0, draw_extra_card=0, discard=0, exhaust=0, thorns=0, locked=0, player_energy=0):
        global card_id_counter
        self.id = card_id_counter
        card_id_counter += 1
        self.name = name
        self.energy = energy
        self.rarity = rarity
        self.type = type
        self.picture = picture
        self.player_hp = player_hp
        self.enemy_hp = enemy_hp
        self.block = block
        self.shield = shield
        self.player_strength = player_strength
        self.enemy_strength = enemy_strength
        self.player_dexterity = player_dexterity
        self.enemy_dexterity = enemy_dexterity
        self.player_weak = player_weak
        self.enemy_weak = enemy_weak
        self.player_vulnerable = player_vulnerable
        self.enemy_vulnerable = enemy_vulnerable
        self.player_frail = player_frail
        self.enemy_frail = enemy_frail
        self.player_poison = player_poison
        self.enemy_poison = enemy_poison
        self.draw_extra_card = draw_extra_card
        self.discard = discard
        self.exhaust = exhaust
        self.thorns = thorns
        self.locked = locked
        self.player_energy = player_energy
        self.colour = BLUE
        self.hover_colour = BLACK
        self.text_colour = WHITE
        self.font = pygame.font.Font(None, int(CARD_WIDTH/6))  # customize the font and size
        self.is_hovered = False
        self.is_selected = False
        self.short_description = short_description.format(player_hp=self.player_hp, enemy_hp=self.enemy_hp, block=self.block, shield=self.shield, player_strength=self.player_strength, enemy_strength=self.enemy_strength, player_dexterity=self.player_dexterity, enemy_dexterity=self.enemy_dexterity, player_weak=self.player_weak, enemy_weak=self.enemy_weak, player_vulnerable=self.player_vulnerable, enemy_vulnerable=self.enemy_vulnerable, player_frail=self.player_frail, enemy_frail=self.enemy_frail, player_poison=self.player_poison, enemy_poison=self.enemy_poison, draw_extra_card=self.draw_extra_card, discard=self.discard, exhaust=self.exhaust, thorns=self.thorns, locked=self.locked, player_energy=self.player_energy)
        self.long_description = long_description.format(player_hp=self.player_hp, enemy_hp=self.enemy_hp, block=self.block, shield=self.shield, player_strength=self.player_strength, enemy_strength=self.enemy_strength, player_dexterity=self.player_dexterity, enemy_dexterity=self.enemy_dexterity, player_weak=self.player_weak, enemy_weak=self.enemy_weak, player_vulnerable=self.player_vulnerable, enemy_vulnerable=self.enemy_vulnerable, player_frail=self.player_frail, enemy_frail=self.enemy_frail, player_poison=self.player_poison, enemy_poison=self.enemy_poison, draw_extra_card=self.draw_extra_card, discard=self.discard, exhaust=self.exhaust, thorns=self.thorns, locked=self.locked, player_energy=self.player_energy)
        list_of_all_cards.append(self)
    
    def draw_card(self, position, cards_in_hand):
        self.rect = pygame.Rect(WIN_WIDTH/2 - CARD_WIDTH/2 - CARD_WIDTH/3 - CARD_WIDTH*2/3*cards_in_hand/2 + CARD_WIDTH*2/3*position, CARDS_Y, CARD_WIDTH, CARD_HEIGHT)
        if position == cards_in_hand: # if last card it has a bigger rect than the others
            self.sel_rect = pygame.Rect(WIN_WIDTH/2 - CARD_WIDTH/2 - CARD_WIDTH/3 - CARD_WIDTH*2/3*cards_in_hand/2 + CARD_WIDTH*2/3*position, CARDS_Y, CARD_WIDTH - 2, CARD_HEIGHT)
        else:
            self.sel_rect = pygame.Rect(WIN_WIDTH/2 - CARD_WIDTH/2 - CARD_WIDTH/3 - CARD_WIDTH*2/3*cards_in_hand/2 + CARD_WIDTH*2/3*position, CARDS_Y, CARD_WIDTH*2/3 - 2, CARD_HEIGHT)
        
        if self.is_hovered:
            pygame.draw.rect(WIN, self.hover_colour, self.rect)
            pygame.draw.rect(WIN, self.colour, self.rect, 8)  # Border
        else:
            pygame.draw.rect(WIN, self.colour, self.rect)
            pygame.draw.rect(WIN, self.hover_colour, self.rect, 8)  # Border
        
        if self.is_selected:
            pygame.draw.rect(WIN, self.hover_colour, self.rect)
            pygame.draw.rect(WIN, self.colour, self.rect, 8)  # Border
        else:
            pygame.draw.rect(WIN, self.colour, self.rect)
            pygame.draw.rect(WIN, self.hover_colour, self.rect, 8)  # Border
        self.draw_text()

    def show_card(self, position):
        col_num = position % DISPLAY_CARDS
        row_num = position // DISPLAY_CARDS
        self.rect = pygame.Rect(DESCRIPTION_X + DISPLAY_GAP_WIDTH*col_num + CARD_WIDTH*col_num, DISPLAY_GAP_HEIGHT + CARD_HEIGHT*row_num + DISPLAY_GAP_HEIGHT*row_num, CARD_WIDTH, CARD_HEIGHT)
        pygame.draw.rect(WIN, self.colour, self.rect)
        pygame.draw.rect(WIN, self.hover_colour, self.rect, 8)  # Border
        self.draw_text()

    def draw_text(self):
        text_surface = self.font.render(self.name, True, self.text_colour)
        text_rect = text_surface.get_rect(center=self.rect.center)
        text_surface2 = self.font.render(str(self.energy), True, self.text_colour)
        text_rect2 = text_surface2.get_rect(topleft=self.rect.topleft)
        WIN.blit(text_surface, text_rect)
        WIN.blit(text_surface2, text_rect2)
    
    def draw_description(self):
        desc_rect = pygame.Rect(WIN_WIDTH/2 - CARD_WIDTH/2 - CARD_WIDTH/3 - CARD_WIDTH*2/3*MAX_CARDS_IN_HAND/2 + CARD_WIDTH*2/3*1, WIN_HEIGHT*4/5 - CARD_HEIGHT/2 - CARD_HEIGHT/4, CARD_WIDTH*2/3*9 + CARD_WIDTH, CARD_HEIGHT/8)
        pygame.draw.rect(WIN, self.colour, desc_rect)
        text_surface = self.font.render(self.long_description, True, self.text_colour)
        text_rect = text_surface.get_rect(center=desc_rect.center)
        WIN.blit(text_surface, text_rect)

class AttackCard(Card):
    def __init__(self, name, energy, rarity, type, enemy_select, short_description, long_description, picture=None, player_hp=0, enemy_hp=0, block=0, shield=0, player_strength=0, enemy_strength=0, player_dexterity=0, enemy_dexterity=0, player_weak=0, enemy_weak=0, player_vulnerable=0, enemy_vulnerable=0, player_frail=0, enemy_frail=0, player_poison=0, enemy_poison=0, draw_extra_card=0, discard=0, exhaust=0, thorns=0, locked=0, player_energy=0):
        super().__init__(name, energy, rarity, type, short_description, long_description, picture, player_hp, enemy_hp, block, shield, player_strength, enemy_strength, player_dexterity, enemy_dexterity, player_weak, enemy_weak, player_vulnerable, enemy_vulnerable, player_frail, enemy_frail, player_poison, enemy_poison, draw_extra_card, discard, exhaust, thorns, locked, player_energy)
        self.type = attack
        self.enemy_select = enemy_select

# card instances
punch = AttackCard('Punch', 1, starter, attack, select, 'Deal {enemy_hp} dmg.', 'Punch for {enemy_hp} base damage', enemy_hp=5)
punch2 = AttackCard('Punch', 1, starter, attack, select, 'Deal {enemy_hp} dmg.', 'Punch for {enemy_hp} base damage', enemy_hp=5)
punch3 = AttackCard('Punch', 1, starter, attack, select, 'Deal {enemy_hp} dmg.', 'Punch for {enemy_hp} base damage', enemy_hp=5)
punch4 = AttackCard('Punch', 1, starter, attack, select, 'Deal {enemy_hp} dmg.', 'Punch for {enemy_hp} base damage', enemy_hp=5)
punch5 = AttackCard('Punch', 1, starter, attack, select, 'Deal {enemy_hp} dmg.', 'Punch for {enemy_hp} base damage', enemy_hp=5)
parry = Card('Parry', 1, starter, skill, 'Gain {block} block.', 'Gain {block} block', block=4)
parry2 = Card('Parry', 1, starter, skill, 'Gain {block} block.', 'Gain {block} block', block=4)
parry3 = Card('Parry', 1, starter, skill, 'Gain {block} block.', 'Gain {block} block', block=4)
parry4 = Card('Parry', 1, starter, skill, 'Gain {block} block.', 'Gain {block} block', block=4)
parry5 = Card('Parry', 1, starter, skill, 'Gain {block} block.', 'Gain {block} block', block=4)
jab = AttackCard('Jab', 0, starter, attack, select, 'Deal {enemy_hp} dmg.\nApply {enemy_vulnerable} vulnerable.', 'Jab for {enemy_hp} base damage and apply {enemy_vulnerable} vulnerable', enemy_hp=3, enemy_vulnerable=2)
test = Card('Test', 0, starter, power, 'test', 'test', player_dexterity=2, player_vulnerable=2, player_strength=1, player_poison=4)

starter_deck = []
starter_deck.append(punch)
starter_deck.append(punch2)
starter_deck.append(punch3)
starter_deck.append(punch4)
starter_deck.append(punch5)
starter_deck.append(parry)
starter_deck.append(parry2)
starter_deck.append(parry3)
starter_deck.append(parry4)
starter_deck.append(parry5)
starter_deck.append(jab)
starter_deck.append(test)


class Character:
    def __init__(self, hp):
        self.max_hp = hp
        self.hp = self.max_hp
        self.block = 0
        self.shield = 0
        self.strength = 0
        self.dexterity = 0
        self.weak = 0
        self.vulnerable = 0
        self.frail = 0
        self.poison = 0
        self.thorns = 0
        self.additional_energy = 0
        self.temp_additional_energy = 0
        self.new_turn_additional_draw = 0
        self.temp_additional_draw = 0
        self.gold = 50

    def draw_hp(self):
        font = pygame.font.Font(None, int(CARD_WIDTH/3))
        text_surface = font.render(f'{self.hp}/{self.max_hp}', True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        WIN.blit(text_surface, text_rect)
    
    def update_status(self):
        status_effects = []
        if self.block != 0:
            status_effects.append({'image':BLOCK, 'number':self.block})
        if self.shield != 0:
            status_effects.append({'image':SHIELD, 'number':self.shield})
        if self.strength != 0:
            status_effects.append({'image':STRENGTH, 'number':self.strength})
        if self.dexterity != 0:
            status_effects.append({'image':DEXTERITY, 'number':self.dexterity})
        if self.weak != 0:
            status_effects.append({'image':WEAK, 'number':self.weak})
        if self.vulnerable != 0:
            status_effects.append({'image':VULNERABLE, 'number':self.vulnerable})
        if self.frail != 0:
            status_effects.append({'image':FRAIL, 'number':self.frail})
        if self.poison != 0:
            status_effects.append({'image':POISON, 'number':self.poison})
        if self.thorns != 0:
            status_effects.append({'image':THORNS, 'number':self.thorns})
        if self.additional_energy != 0:
            status_effects.append({'image':ADDITIONAL_ENERGY, 'number':self.additional_energy})
        
        status_counter = 0
        if len(status_effects) > 0:
            for status in status_effects:
                self.draw_status(status['image'], status['number'], status_counter)
                status_counter +=1
    
    def draw_status(self, image, number, counter):
        font = pygame.font.Font(None, int(EFFECTS_WIDTH*2/3))
        text_surface = font.render(str(number), True, BLACK)
        rect = pygame.Rect(self.x_pos + EFFECTS_WIDTH*counter, EFFECTS_Y, EFFECTS_WIDTH, EFFECTS_HEIGHT)
        text_rect = text_surface.get_rect(center=rect.center)

        WIN.blit(image, (self.x_pos + EFFECTS_WIDTH*counter, EFFECTS_Y))
        WIN.blit(text_surface, text_rect)

class Player(Character):
    def __init__(self, hp, starter_deck):
        super().__init__(hp)
        self.x_pos = P1_X
        self.y_pos = P1_Y
        self.energy = 3 + self.additional_energy + self.temp_additional_energy
        self.new_turn_draw_cards = BASE_DRAW_CARDS + self.new_turn_additional_draw + self.temp_additional_draw
        self.deck = starter_deck
        self.draw_pile = []
        self.active_hand = []
        self.discard_pile = []
        self.exhaust_pile = []
        self.floor_level = 1
        self.rect = pygame.Rect(self.x_pos, self.y_pos, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    
    def draw_player(self):
        pygame.draw.rect(WIN, GREEN, self.rect)

    def draw_energy(self):
        ENERGY_COORDS = (LEFT_BUTTON_X + DRAW_PILE_WIDTH/2, TOP_BUTTON_Y + DRAW_PILE_HEIGHT/2)
        font = pygame.font.Font(None, int(CARD_WIDTH/3))
        text_surface = font.render(str(self.energy), True, BLACK)
        text_rect = text_surface.get_rect(center=ENERGY_COORDS)
        WIN.blit(text_surface, text_rect)
    
    def draw_number_of_cards(self, linked_list_of_cards, x, y, colour=LIGHT_BLUE, radius=DRAW_PILE_WIDTH/6):
        coords = (x, y)
        pygame.draw.circle(WIN, colour, coords, radius)
        font = pygame.font.Font(None, int(CARD_WIDTH/4))
        text_surface = font.render(str(len(linked_list_of_cards)), True, BLACK)
        text_rect = text_surface.get_rect(center=coords)
        WIN.blit(text_surface, text_rect)
    
    def card_played(self, card, enemy):
        if enemy.vulnerable >= 1:
            VULNERABLE_MULTIPLIER = 1.5
        else:
            VULNERABLE_MULTIPLIER = 1
        if self.weak >= 1:
            WEAK_MULTIPLIER = 0.75
        else:
            WEAK_MULTIPLIER = 1
        if self.frail >= 1:
            FRAIL_MULTIPLIER = 0.75
        else:
            FRAIL_MULTIPLIER = 1

        self.energy -= card.energy
        self.hp -= card.player_hp

        if card.enemy_hp >= 1:
            if enemy.block < round((card.enemy_hp + self.strength) * VULNERABLE_MULTIPLIER * WEAK_MULTIPLIER):
                enemy.hp -= round((card.enemy_hp + self.strength) * VULNERABLE_MULTIPLIER * WEAK_MULTIPLIER) - enemy.block
                enemy.block = 0
            else:
                enemy.block -= round((card.enemy_hp + self.strength) * VULNERABLE_MULTIPLIER * WEAK_MULTIPLIER)
        
        if card.block >= 1:
            self.block += round((card.block + self.dexterity) * FRAIL_MULTIPLIER)
        self.shield += card.shield
        self.strength += card.player_strength
        enemy.strength -= card.enemy_strength
        self.dexterity += card.player_dexterity
        enemy.dexterity -= card.enemy_dexterity
        self.weak += card.player_weak
        enemy.weak += card.enemy_weak
        self.vulnerable += card.player_vulnerable
        enemy.vulnerable += card.enemy_vulnerable
        self.poison += card.player_poison
        enemy.poison += card.enemy_poison
        # card.draw_extra_card
        # card.discard
        # card.exhaust
        self.thorns += card.thorns
        # card.locked
        # card.player_energy
        card.is_selected = False

class Enemy(Character):
    def __init__(self, hp, starting_block, x_pos, y_pos, width, height, death_strength=False):
        super().__init__(hp)
        self.is_enemy_turn = False
        self.enemy_turn = 1
        self.block = starting_block
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.death_strength = death_strength # if true then when an enemy dies it will apply -2 str and self.death_str = False
    
    def draw_enemy(self):
        pygame.draw.rect(WIN, ORANGE, self.rect)
    
    def enemy_dmg_dealt(self, base_dmg, confidence_multiplier=1):
        if p1.vulnerable >= 1:
            VULNERABLE_MULTIPLIER = 1.5
        else:
            VULNERABLE_MULTIPLIER = 1
        if self.weak >= 1:
            WEAK_MULTIPLIER = 0.75
        else:
            WEAK_MULTIPLIER = 1

        if p1.block < round((base_dmg + self.strength) * VULNERABLE_MULTIPLIER * WEAK_MULTIPLIER * confidence_multiplier):
            p1.hp -= round((base_dmg + self.strength) * VULNERABLE_MULTIPLIER * WEAK_MULTIPLIER * confidence_multiplier) - p1.block
            p1.block = 0
        else:
            p1.block -= round((base_dmg + self.strength) * VULNERABLE_MULTIPLIER * WEAK_MULTIPLIER * confidence_multiplier)
    
    def enemy_block(self, base_block):
        if self.frail >= 1:
            FRAIL_MULTIPLIER = 0.75
        else:
            FRAIL_MULTIPLIER = 1
        
        self.block += round((base_block + self.dexterity) * FRAIL_MULTIPLIER)
    
    def confidence_enemy_turns(self):
        if self.hp > 0: # if still alive
            if self.block == 0:
                self.enemy_dmg_dealt(5, 0.5) # cowardice
            elif self.block >= 1:
                self.enemy_dmg_dealt(5, 2) # confidence
            self.block = self.enemy_block(5)
            self.is_enemy_turn = False
    
    def less_draw_enemy_turns(self):
        if self.hp > 0:
            if self.enemy_turn == 1:
                p1.new_turn_additional_draw += -1
            elif p1.new_turn_draw_cards > 4:
                p1.new_turn_additional_draw += -1
            else:
                ran_num = random.randint(1, 100)
                if ran_num <= 50:
                    self.enemy_dmg_dealt(6) # 6 hp
                    self.enemy_block(5) # 5 block
                else:
                    p1.temp_additional_draw += -1
            self.enemy_turn += 1
            self.is_enemy_turn = False

    def less_energy_enemy_turns(self):
        if self.hp > 0:
            if self.enemy_turn == 1:
                p1.additional_energy += -1
            elif p1.energy > 2:
                p1.additional_energy += -1
            else:
                ran_num = random.randint(1, 100)
                if ran_num <= 50:
                    self.enemy_dmg_dealt(6) # 6 hp
                    self.enemy_block(5) # 5 block
                else:
                    p1.temp_additional_energy += -1
            self.enemy_turn += 1
            self.is_enemy_turn = False
    
    def weak_death_enemy_turns(self):
        if self.hp > 0:
            ran_num = random.randint(1, 100)
            if ran_num <= 50:
                self.enemy_dmg_dealt(7) # 7 hp
            else:
                p1.weak += 2

    def vulnerable_death_enemy_turns(self):
        if self.hp > 0:
            ran_num = random.randint(1, 100)
            if ran_num <= 50:
                self.enemy_dmg_dealt(6) # 6 hp
            else:
                p1.vulnerable += 2

    def frail_death_enemy_turns(self):
        if self.hp > 0:
            ran_num = random.randint(1, 100)
            if ran_num <= 50:
                self.enemy_dmg_dealt(5) # 5 hp
            else:
                p1.frail += 2

# character instances
p1 = Player(60, starter_deck)
enemy1 = Enemy(20, 3, ENEMY1_X, ENEMY1_Y, CHARACTER_WIDTH, CHARACTER_HEIGHT) # test enemy
small_fights = []
boss_fights = []
main_boss_fights = []
confidence_enemy_1 = Enemy(15, 3, ENEMY1_X, ENEMY1_Y + CHARACTER_HEIGHT/2, CHARACTER_WIDTH/3, CHARACTER_HEIGHT/2)
confidence_enemy_2 = Enemy(15, 3, ENEMY1_X + CHARACTER_WIDTH/3, ENEMY1_Y, CHARACTER_WIDTH/3, CHARACTER_HEIGHT/2)
confidence_enemy_3 = Enemy(15, 3, ENEMY1_X + CHARACTER_WIDTH*2/3, ENEMY1_Y + CHARACTER_HEIGHT/2, CHARACTER_WIDTH/3, CHARACTER_HEIGHT/2)
small_fights.append([confidence_enemy_1, confidence_enemy_2, confidence_enemy_3])
less_draw_enemy = Enemy(25, 0, ENEMY1_X, ENEMY1_Y, CHARACTER_WIDTH/2, CHARACTER_HEIGHT)
less_energy_enemy = Enemy(25, 0, ENEMY1_X + CHARACTER_WIDTH/2, ENEMY1_Y, CHARACTER_WIDTH/2, CHARACTER_HEIGHT)
small_fights.append([less_draw_enemy, less_energy_enemy])
weak_death_enemy = Enemy(10, 5, ENEMY1_X, ENEMY1_Y + CHARACTER_HEIGHT/2, CHARACTER_WIDTH/3, CHARACTER_HEIGHT/2, death_strength=True)
vulnerable_death_enemy = Enemy(15, 5, ENEMY1_X + CHARACTER_WIDTH/3, ENEMY1_Y, CHARACTER_WIDTH/3, CHARACTER_HEIGHT/2, death_strength=True)
frail_death_enemy = Enemy(20, 5, ENEMY1_X + CHARACTER_WIDTH*2/3, ENEMY1_Y + CHARACTER_HEIGHT/2, CHARACTER_WIDTH/3, CHARACTER_HEIGHT/2, death_strength=True)
small_fights.append([weak_death_enemy, vulnerable_death_enemy, frail_death_enemy])


class Button:
    def __init__(self, name, image, button_x, button_y, button_width=DRAW_PILE_WIDTH, button_height=DRAW_PILE_HEIGHT, linked_list=[]):
        self.name = name
        self.image = image
        self.button_x = button_x
        self.button_y = button_y
        self.button_width = button_width
        self.button_height = button_height
        self.rect = pygame.Rect(button_x, button_y, button_width, button_height)
        self.linked_list = linked_list
        self.is_clicked = False

    def draw_button(self):
        WIN.blit(self.image, self.rect)
        if self.name == 'energy_button':
            p1.draw_energy()
        else:
            p1.draw_number_of_cards(self.linked_list, self.button_x, self.button_y)

    def show_cards(self):
        card_number = 0
        current_list = []
        for card in self.linked_list:
            current_list.append(card.id)
        if self.name == 'draw_pile_button': # if looking at the draw pile then sort the list (to hide seeing what's next)
            current_list = sorted(current_list)

        WIN.fill(LIGHT_BLUE)
        for button in pile_buttons:
            button.draw_button()
        energy_button.draw_button()

        for card_id in current_list:
            for card in list_of_all_cards:
                if card_id == card.id:
                    card.show_card(card_number)
                    card_number += 1
        
        pygame.display.update()

# button instances
draw_pile_button = Button('draw_pile_button', DRAW_PILE, LEFT_BUTTON_X, BOTTOM_BUTTON_Y, linked_list=p1.draw_pile)
discard_pile_button = Button('discard_pile_button', DISCARD_PILE, RIGHT_BUTTON_X, BOTTOM_BUTTON_Y, linked_list=p1.discard_pile)
exhaust_pile_button = Button('exhaust_pile_button', EXHAUST_PILE, RIGHT_BUTTON_X, TOP_BUTTON_Y, linked_list=p1.exhaust_pile)
energy_button = Button('energy_button', ENERGY, LEFT_BUTTON_X, TOP_BUTTON_Y)
entire_deck_button = Button('entire_deck_button', ENTIRE_DECK, WIN_WIDTH - DESCRIPTION_X/2 - DRAW_PILE_WIDTH/2, WIN_HEIGHT - CARDS_Y - CARD_HEIGHT, linked_list=p1.deck)
pile_buttons = []
pile_buttons.append(draw_pile_button)
pile_buttons.append(discard_pile_button)
pile_buttons.append(exhaust_pile_button)
pile_buttons.append(entire_deck_button)


# functions
def draw_end_turn_button():
    is_hovered = False
    colour = PINK
    hover_colour = WHITE
    font = pygame.font.Font(None, int(CARD_WIDTH/4))
    text_surface = font.render('End Turn', True, BLACK)
    rect = pygame.Rect(END_TURN_X, END_TURN_Y, END_TURN_WIDTH, END_TURN_HEIGHT)

    if is_hovered:
        pygame.draw.rect(WIN, hover_colour, rect)
        pygame.draw.rect(WIN, colour, rect, 4)  # Border
    else:
        pygame.draw.rect(WIN, colour, rect)
        pygame.draw.rect(WIN, hover_colour, rect, 4)  # Border
        
    text_rect = text_surface.get_rect(center=rect.center)
    WIN.blit(text_surface, text_rect)

def randomise_fight(enemy_level):
    global current_enemies
    if enemy_level == 'small':
        fights = small_fights
    elif enemy_level == 'boss':
        fights = boss_fights
    elif enemy_level == 'main_boss':
        fights = main_boss_fights
    
    fight_no = random.randint(0, len(fights) - 1)

    for enemy in fights[fight_no]:
        current_enemies.append(enemy)

def main():

    clock = pygame.time.Clock()
    global current_enemies
    screen_view = fight
    new_fight = True
    update = True
    clicked = False
    a_card_selected = False
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()

            elif event.type == pygame.MOUSEMOTION:
                for card in p1.active_hand:
                    if card.sel_rect.collidepoint(event.pos) and card.is_hovered == False: # threw up an error 2 times - AttributeError: 'Card' object has no attribute 'sel_rect'
                        card.is_hovered = True
                        card.draw_description()
                        pygame.display.update()
                    elif card.sel_rect.collidepoint(event.pos) == False and card.is_hovered:
                        card.is_hovered = False
                        desc_rect = pygame.Rect(DESCRIPTION_X, DESCRIPTION_Y, DESCRIPTION_WIDTH, DESCRIPTION_HEIGHT)
                        pygame.draw.rect(WIN, LIGHT_BLUE, desc_rect)
                        pygame.display.update()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for card in p1.active_hand:
                    if card.is_hovered and clicked == False: # clicking on a card
                        clicked = True
                        update = True
                        if card.is_selected == False and a_card_selected == False: # if no card selected, then select it
                            card.is_selected = True
                            a_card_selected = True
                        elif card.is_selected and a_card_selected: # if a card is selected, then unselect it
                            card.is_selected = False
                            a_card_selected = False
                    
                    for enemy in current_enemies:
                        if card.is_selected and (enemy.rect.collidepoint(event.pos) or p1.rect.collidepoint(event.pos)):
                            if p1.energy - card.energy < 0:
                                card.is_selected = False
                                a_card_selected = False
                                update = True
                            else:
                                if card.type == attack and enemy.rect.collidepoint(event.pos): # if attack card selected and selects enemy
                                    p1.card_played(card, enemy)
                                    a_card_selected = False
                                    p1.discard_pile.append(card)
                                    p1.active_hand.remove(card)
                                    update = True
                                
                                elif (card.type == skill or card.type == power) and p1.rect.collidepoint(event.pos): # if skill or power card selected and selects player
                                    p1.card_played(card, enemy)
                                    a_card_selected = False
                                    p1.discard_pile.append(card)
                                    p1.active_hand.remove(card)
                                    update = True

                for button in pile_buttons:
                    if button.rect.collidepoint(event.pos):
                        clicked = True
                        if button.is_clicked == False:
                            for b in pile_buttons:
                                b.is_clicked = False # allows you to switch between different buttons indefinitely without it closing
                            button.is_clicked = True
                            button.show_cards()

                        elif button.is_clicked: # if we click the button and it was already clicked...
                            button.is_clicked = False
                            update = True # go back to in game screen

            elif event.type == pygame.MOUSEBUTTONUP: # prevents one click doing multiple actions
                if clicked == True:
                    clicked = False

        if screen_view == fight:
            if new_fight == True:
                randomise_fight('small')
                for card in p1.deck:
                    p1.draw_pile.append(card)
                random.shuffle(p1.draw_pile)
                for i in range(p1.new_turn_draw_cards):
                    p1.active_hand.append(p1.draw_pile.pop())
                new_fight = False

            elif update == True:
                WIN.blit(PIRATE_BACKGROUND, (0, 0))
                # p1 stuff
                p1.draw_player()
                p1.draw_hp()
                p1.update_status()
                # enemy stuff
                for enemy in current_enemies:
                    enemy.draw_enemy()
                    enemy.draw_hp()
                    enemy.update_status()
                    if enemy.hp <= 0 and enemy.death_strength == True: # if p1 kills an enemy that reduces p1 str on death
                        p1.strength -= 2
                        enemy.death_strength = False
                # cards
                card_pos = 1
                for card in p1.active_hand:
                    card.draw_card(card_pos, len(p1.active_hand))
                    card_pos += 1
                # buttons
                draw_end_turn_button()
                for button in pile_buttons:
                    button.draw_button()
                energy_button.draw_button()
                pygame.display.update()
                update = False

main()

# the main deck needs...
# a few decks shuffled together
# maybe keep the rarities separate (but each shuffled), then can do a % chance what rarity card is drawn

# a deck for shop items...
# same as above with rarities separated but shuffled

# need to come up with...
# enemies
# enemy movesets
# events
# mini bosses
# bosses
# a reason to win

# screen_view = home, map, battle, reward, card_view, shop, event, death, win

# to do

# move the p1 and enemy starting positions so that they're in line with 10 cards drawn
# add in an end turn button (currently doesn't do anything)
# add in something that shows what the enemy is about to do next
# add logic that kills an enemy when hp goes to 0 or below
# add logic that kills the player when hp goes to 0 or below
# make the hp into a health bar which goes blue with block (like sts), meaning i'll have to remove the block from the current list
# find a few different pirate themed background images for fights to happen in
# figure out how to show fixed enemy abilities (like the stregth debuff on death enemy) (maybe above the enemy?)
# create a list of different screen views so that i can say if in screen x then be able to do this, should stop past rects from being able to be clicked
# blit in the name of the lists when looking at draw/discard/etc piles (could have it show in the same place as card desc?)
# blit in something that says cards order is hidden on draw pile list

# problems

# can't figure out how to update the card colour when hovered
# solved i think (just not actioned) - everything that had an interactable rect on the screen before still allows you to interact with it when looking at the draw/discard/etc piles
# keep getting errors on the sel_rect, but not sure why, plus it seems to be random? (maybe to do with jab/test not being able to be the last of the 5 cards?)