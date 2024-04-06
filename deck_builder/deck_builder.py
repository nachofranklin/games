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
BASE_ENERGY = 3
turn = 1
screen_view = 'fight'
update = True
player_turn = True
DISPLAY_CARDS = 6 # determines how many cards in a row get shown when clicking on draw pile etc
current_enemies = []
list_of_all_cards = []
starter_deck = []
common_cards = []
uncommon_cards = []
rare_cards = []
curse_cards = []

# width and heights
WIN_WIDTH = 1200
WIN_HEIGHT = WIN_WIDTH*2/3
CARD_WIDTH = WIN_WIDTH/10 # 120
CARD_HEIGHT = WIN_HEIGHT/4
CHARACTER_WIDTH = ENEMY1_WIDTH =  WIN_WIDTH/3
CHARACTER_HEIGHT = ENEMY1_HEIGHT = WIN_HEIGHT/3
EFFECTS_WIDTH = EFFECTS_HEIGHT = WIN_WIDTH/27
ENERGY_WIDTH = ENERGY_HEIGHT = WIN_HEIGHT/20 # radius
DESCRIPTION_WIDTH = CARD_WIDTH*2/3*9 + CARD_WIDTH # 840
DESCRIPTION_HEIGHT = CARD_HEIGHT/8
DRAW_PILE_WIDTH = DRAW_PILE_HEIGHT = CARD_WIDTH*3/4
DISPLAY_GAP_WIDTH = (DESCRIPTION_WIDTH - CARD_WIDTH*DISPLAY_CARDS) / (DISPLAY_CARDS - 1)
DISPLAY_GAP_HEIGHT = WIN_HEIGHT/5 - CARD_HEIGHT/2

# x and y co-ordinates
# CARDS_X is a bit more complicated
CARDS_Y = WIN_HEIGHT*4/5 - CARD_HEIGHT/2
END_TURN_Y = CARDS_Y - CARD_HEIGHT + DRAW_PILE_HEIGHT
DESCRIPTION_X = WIN_WIDTH/2 - CARD_WIDTH/2 - CARD_WIDTH/3 - CARD_WIDTH*2/3*MAX_CARDS_IN_HAND/2 + CARD_WIDTH*2/3*1
DESCRIPTION_Y = WIN_HEIGHT*4/5 - CARD_HEIGHT/2 - CARD_HEIGHT/4
P1_X = DESCRIPTION_X
P1_Y = ENEMY1_Y = WIN_HEIGHT/9
ENEMY1_X = DESCRIPTION_X + DESCRIPTION_WIDTH - ENEMY1_WIDTH
# EFFECTS_Y = P1_Y + CHARACTER_HEIGHT # changed to match the enemy y position
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
ADDITIONAL_DRAW_IMG = image('drawing_cards')
DRAW_PILE = image('draw_pile', DRAW_PILE_WIDTH, DRAW_PILE_HEIGHT)
DISCARD_PILE = image('discard_pile', DRAW_PILE_WIDTH, DRAW_PILE_HEIGHT)
EXHAUST_PILE = image('tombstone', DRAW_PILE_WIDTH, DRAW_PILE_HEIGHT)
ENTIRE_DECK = image('entire_deck', DRAW_PILE_WIDTH, DRAW_PILE_HEIGHT)
ENERGY = image('sun', DRAW_PILE_WIDTH, DRAW_PILE_HEIGHT)
END_TURN_IMG = image('end_turn', DRAW_PILE_WIDTH, DRAW_PILE_HEIGHT)
PIRATE_BACKGROUND = image('pirate_background', WIN_WIDTH, WIN_HEIGHT)
ATTACK_INTENT = image('sword')
DEBUFF_INTENT = image('rum')
# POWER_UP_INTENT_IMG = image('')
CARD_STEAL_INTENT_IMG = image('card_thief')
ENERGY_STEAL_INTENT_IMG = image('sun_thief')
# CURSE_INTENT_IMG = image('')
STEERING_WHEEL_IMG = image('steering_wheel', DRAW_PILE_WIDTH * 1.5, DRAW_PILE_HEIGHT * 1.5)

# sounds
pass

# classes
class Card:
    def __init__(self, name, energy, rarity, type, short_description, long_description, picture=None, exhausts=False, player_hp=0, enemy_hp=0, block=0, shield=0, player_strength=0, enemy_strength=0, player_dexterity=0, enemy_dexterity=0, player_weak=0, enemy_weak=0, player_vulnerable=0, enemy_vulnerable=0, player_frail=0, enemy_frail=0, player_poison=0, enemy_poison=0, draw_extra_card=0, discard=0, exhaust_other_cards=0, thorns=0, locked=0, player_energy=0):
        global card_id_counter
        self.id = card_id_counter
        card_id_counter += 1
        self.name = name
        self.energy = energy
        self.rarity = rarity
        self.type = type
        self.picture = picture
        self.exhausts = exhausts
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
        self.exhaust_other_cards = exhaust_other_cards
        self.thorns = thorns
        self.locked = locked
        self.player_energy = player_energy
        self.colour = BLUE
        self.hover_colour = BLACK
        self.text_colour = WHITE
        self.font = pygame.font.Font(None, int(CARD_WIDTH/6))  # customize the font and size
        self.is_hovered = False
        self.is_selected = False
        self.short_description = short_description.format(player_hp=self.player_hp, enemy_hp=self.enemy_hp, block=self.block, shield=self.shield, player_strength=self.player_strength, enemy_strength=self.enemy_strength, player_dexterity=self.player_dexterity, enemy_dexterity=self.enemy_dexterity, player_weak=self.player_weak, enemy_weak=self.enemy_weak, player_vulnerable=self.player_vulnerable, enemy_vulnerable=self.enemy_vulnerable, player_frail=self.player_frail, enemy_frail=self.enemy_frail, player_poison=self.player_poison, enemy_poison=self.enemy_poison, draw_extra_card=self.draw_extra_card, discard=self.discard, exhaust_other_cards=self.exhaust_other_cards, thorns=self.thorns, locked=self.locked, player_energy=self.player_energy)
        self.long_description = long_description.format(player_hp=self.player_hp, enemy_hp=self.enemy_hp, block=self.block, shield=self.shield, player_strength=self.player_strength, enemy_strength=self.enemy_strength, player_dexterity=self.player_dexterity, enemy_dexterity=self.enemy_dexterity, player_weak=self.player_weak, enemy_weak=self.enemy_weak, player_vulnerable=self.player_vulnerable, enemy_vulnerable=self.enemy_vulnerable, player_frail=self.player_frail, enemy_frail=self.enemy_frail, player_poison=self.player_poison, enemy_poison=self.enemy_poison, draw_extra_card=self.draw_extra_card, discard=self.discard, exhaust_other_cards=self.exhaust_other_cards, thorns=self.thorns, locked=self.locked, player_energy=self.player_energy)
        self.sel_rect = pygame.Rect(WIN_WIDTH/2 - CARD_WIDTH/2 - CARD_WIDTH/3 - CARD_WIDTH*2/3/2 + CARD_WIDTH*2/3, CARDS_Y, CARD_WIDTH - 2, CARD_HEIGHT) # don't understand why this is necessary, but it seems to have fixed the sel.rect issue that occassionally popped up
        list_of_all_cards.append(self)
        if self.rarity == starter:
            starter_deck.append(self)
        elif self.rarity == uncommon:
            uncommon_cards.append(self)
        elif self.rarity == common:
            common_cards.append(self)
        elif self.rarity == rare:
            rare_cards.append(self)
        elif self.rarity == curse:
            curse_cards.append(self)
    
    def blit_card(self, position, cards_in_hand):
        x = WIN_WIDTH/2 - CARD_WIDTH/2 - CARD_WIDTH/3 - CARD_WIDTH*2/3*cards_in_hand/2 + CARD_WIDTH*2/3*position
        y = CARDS_Y
        self.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        if position == cards_in_hand: # if last card it has a bigger rect than the others
            self.sel_rect = pygame.Rect(x, y, CARD_WIDTH - 2, CARD_HEIGHT) # maybe try copying this to the init section to see if that fixes the error i sometimes get?
        else:
            self.sel_rect = pygame.Rect(x, y, CARD_WIDTH*2/3 - 2, CARD_HEIGHT)
        
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
        self.draw_energy_cost(x, y)

    def show_card(self, position):
        col_num = position % DISPLAY_CARDS
        row_num = position // DISPLAY_CARDS
        x = DESCRIPTION_X + DISPLAY_GAP_WIDTH*col_num + CARD_WIDTH*col_num
        y = DISPLAY_GAP_HEIGHT + CARD_HEIGHT*row_num + DISPLAY_GAP_HEIGHT*row_num
        self.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        pygame.draw.rect(WIN, self.colour, self.rect)
        pygame.draw.rect(WIN, self.hover_colour, self.rect, 8)  # Border
        self.draw_text()
        self.draw_energy_cost(x, y)

    def draw_text(self):
        text_surface = self.font.render(self.name, True, self.text_colour)
        text_rect = text_surface.get_rect(center=self.rect.center)
        WIN.blit(text_surface, text_rect)

    def draw_energy_cost(self, x, y, circle_colour=BLACK, text_colour=WHITE, radius=CARD_WIDTH/8):
        coords = (x + 3, y + 3)
        pygame.draw.circle(WIN, circle_colour, coords, radius)
        font = pygame.font.Font(None, int(CARD_WIDTH/4))
        text_surface = font.render(str(self.energy), True, text_colour)
        text_rect = text_surface.get_rect(center=coords)
        WIN.blit(text_surface, text_rect)
    
    def draw_description(self):
        desc_rect = pygame.Rect(WIN_WIDTH/2 - CARD_WIDTH/2 - CARD_WIDTH/3 - CARD_WIDTH*2/3*MAX_CARDS_IN_HAND/2 + CARD_WIDTH*2/3*1, WIN_HEIGHT*4/5 - CARD_HEIGHT/2 - CARD_HEIGHT/4, CARD_WIDTH*2/3*9 + CARD_WIDTH, CARD_HEIGHT/8)
        pygame.draw.rect(WIN, self.colour, desc_rect)
        text_surface = self.font.render(self.long_description, True, self.text_colour)
        text_rect = text_surface.get_rect(center=desc_rect.center)
        WIN.blit(text_surface, text_rect)

class AttackCard(Card):
    def __init__(self, name, energy, rarity, type, enemy_select, short_description, long_description, picture=None, exhausts=False, player_hp=0, enemy_hp=0, block=0, shield=0, player_strength=0, enemy_strength=0, player_dexterity=0, enemy_dexterity=0, player_weak=0, enemy_weak=0, player_vulnerable=0, enemy_vulnerable=0, player_frail=0, enemy_frail=0, player_poison=0, enemy_poison=0, draw_extra_card=0, discard=0, exhaust_other_cards=0, thorns=0, locked=0, player_energy=0):
        super().__init__(name, energy, rarity, type, short_description, long_description, picture, exhausts, player_hp, enemy_hp, block, shield, player_strength, enemy_strength, player_dexterity, enemy_dexterity, player_weak, enemy_weak, player_vulnerable, enemy_vulnerable, player_frail, enemy_frail, player_poison, enemy_poison, draw_extra_card, discard, exhaust_other_cards, thorns, locked, player_energy)
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
test = Card('Test', 0, starter, power, 'test', 'test', exhausts=True, player_dexterity=2, player_vulnerable=2, player_strength=1, player_poison=4)


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
        # intentions
        self.attack_intent = False
        self.attack_actual = 0
        self.block_intent = False
        self.block_actual = 0
        self.debuff_intent = False
        self.power_up_intent = False
        self.energy_steal_intent = False
        self.card_steal_intent = False
        self.curse_intent = False

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
        if self.additional_energy + self.temp_additional_energy != 0:
            status_effects.append({'image':ADDITIONAL_ENERGY, 'number':self.additional_energy + self.temp_additional_energy})
        if self.new_turn_additional_draw + self.temp_additional_draw != 0:
            status_effects.append({'image':ADDITIONAL_DRAW_IMG, 'number':self.new_turn_additional_draw + self.temp_additional_draw})
        
        status_counter = 0
        if len(status_effects) > 0:
            for status in status_effects:
                self.draw_status(status['image'], status['number'], status_counter)
                status_counter +=1
    
    def draw_status(self, image, number, counter):
        font = pygame.font.Font(None, int(EFFECTS_WIDTH*2/3))
        text_surface = font.render(str(number), True, BLACK)
        rect = pygame.Rect(self.x_pos + EFFECTS_WIDTH*counter, self.y_pos + self.height, EFFECTS_WIDTH, EFFECTS_HEIGHT)
        text_rect = text_surface.get_rect(center=rect.center)

        WIN.blit(image, (self.x_pos + EFFECTS_WIDTH*counter, self.y_pos + self.height))
        WIN.blit(text_surface, text_rect)

    def reduce_status(self):
        # once i've finished my turn then everything needs to -1 for the enemy
        if self.block > 0:
            self.block = 0
        if self.shield > 0:
            shield = self.shield # not sure if i need to split this into two steps, test later
            self.block = shield
            self.shield = 0
        if self.weak > 0:
            self.weak -= 1
        if self.vulnerable > 0:
            self.vulnerable -= 1
        if self.frail > 0:
            self.frail -= 1
        if self.poison > 0:
            self.poison -= 1
        if self.temp_additional_energy < 0:
            self.temp_additional_energy += 1
        if self.temp_additional_energy > 0:
            self.temp_additional_energy -= 1
        if self.temp_additional_draw < 0:
            self.temp_additional_draw += 1
        if self.temp_additional_draw > 0:
            self.temp_additional_draw -= 1

    def reset_status(self):
        self.reset_intent()
        # current_enemies = []
        # at the end of battle i'll need to reset everything back to base levels so that p1 is ready and that enemy is ready in case i face it twice
        pass

    def reset_intent(self):
        self.attack_intent = False
        self.block_intent = False
        self.debuff_intent = False
        self.power_up_intent = False
        self.energy_steal_intent = False
        self.card_steal_intent = False
        self.curse_intent = False

    def base_dmg_plus_strength(self, base_dmg, strength):
        if base_dmg + strength < 0:
            return 0
        else:
            return base_dmg + strength
        
    def base_block_plus_dexterity(self, base_block, dexterity):
        if base_block + dexterity < 0:
            return 0
        else:
            return base_block + dexterity

class Player(Character):
    def __init__(self, hp, starter_deck):
        super().__init__(hp)
        self.x_pos = P1_X
        self.y_pos = P1_Y
        self.height = CHARACTER_HEIGHT
        self.energy = 3 + self.additional_energy + self.temp_additional_energy
        # self.new_turn_draw_cards = BASE_DRAW_CARDS + self.new_turn_additional_draw + self.temp_additional_draw
        self.deck = starter_deck
        self.draw_pile = []
        self.active_hand = []
        self.discard_pile = []
        self.exhaust_pile = []
        self.floor_level = 1
        self.rect = pygame.Rect(self.x_pos, self.y_pos, CHARACTER_WIDTH, self.height)

    def new_turn_draw_cards(self):
        return BASE_DRAW_CARDS + self.new_turn_additional_draw + self.temp_additional_draw

    def new_turn_energy(self):
        return BASE_ENERGY + self.additional_energy + self.temp_additional_energy
    
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
            if enemy.block < round(self.base_dmg_plus_strength(card.enemy_hp, self.strength) * VULNERABLE_MULTIPLIER * WEAK_MULTIPLIER):
                enemy.hp -= round(self.base_dmg_plus_strength(card.enemy_hp, self.strength) * VULNERABLE_MULTIPLIER * WEAK_MULTIPLIER) - enemy.block
                enemy.block = 0
            else:
                enemy.block -= round(self.base_dmg_plus_strength(card.enemy_hp, self.strength) * VULNERABLE_MULTIPLIER * WEAK_MULTIPLIER)
        
        if card.block >= 1:
            self.block += round(self.base_block_plus_dexterity(card.block, self.dexterity) * FRAIL_MULTIPLIER)
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

    def draw_card(self, how_many):
        for i in range(how_many):
            if len(self.draw_pile) == 0 and len(self.discard_pile) == 0:
                continue # should this be break?
            else:
                if len(self.draw_pile) == 0:
                    self.shuffle_discard_pile()
                self.active_hand.append(self.draw_pile[0])
                self.draw_pile.remove(self.draw_pile[0])

    def shuffle_discard_pile(self):
        for i in range(len(self.discard_pile)):
            self.draw_pile.append(self.discard_pile[0])
            self.discard_pile.remove(self.discard_pile[0])
        random.shuffle(self.draw_pile)

class Enemy(Character):
    def __init__(self, name, hp, starting_block, x_pos, y_pos, width, height, death_strength=False):
        super().__init__(hp)
        global turn
        self.name = name
        self.block = starting_block
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.death_strength = death_strength # if true then when an enemy dies it will apply -2 str and self.death_str = False
        self.has_block = False
        self.ran_num = random.randint(1, 100)
    
    def draw_enemy(self):
        pygame.draw.rect(WIN, ORANGE, self.rect)

    def enemy_attack(self, base_dmg, confidence_multiplier=1):
        if p1.vulnerable >= 1:
            VULNERABLE_MULTIPLIER = 1.5
        else:
            VULNERABLE_MULTIPLIER = 1
        if self.weak >= 1:
            WEAK_MULTIPLIER = 0.75
        else:
            WEAK_MULTIPLIER = 1

        return round(self.base_dmg_plus_strength(base_dmg, self.strength) * VULNERABLE_MULTIPLIER * WEAK_MULTIPLIER * confidence_multiplier)
    
    def enemy_dmg_dealt(self, base_dmg, confidence_multiplier=1):
        if p1.block < self.enemy_attack(base_dmg, confidence_multiplier):
            p1.hp -= self.enemy_attack(base_dmg, confidence_multiplier) - p1.block
            p1.block = 0
        else:
            p1.block -= self.enemy_attack(base_dmg, confidence_multiplier)
    
    def enemy_block(self, base_block):
        if self.frail >= 1:
            FRAIL_MULTIPLIER = 0.75
        else:
            FRAIL_MULTIPLIER = 1
        
        return round(self.base_block_plus_dexterity(base_block, self.dexterity) * FRAIL_MULTIPLIER)
    
    def block_checker(self):
        if self.block > 0:
            self.has_block = True
        else:
            self.has_block = False

    def draw_intention(self, image, counter):
        WIN.blit(image, (self.x_pos + EFFECTS_WIDTH*counter, self.y_pos - EFFECTS_HEIGHT)) # always blit the image

        if image == ATTACK_INTENT:
            num = self.attack_actual
        elif image == BLOCK:
            num = self.block_actual
        if image == ATTACK_INTENT or image == BLOCK: # only blit the number for att or block
            font = pygame.font.Font(None, int(EFFECTS_WIDTH*2/3))
            text_surface = font.render(str(num), True, BLACK)
            rect = pygame.Rect(self.x_pos + EFFECTS_WIDTH*counter, self.y_pos - EFFECTS_HEIGHT, EFFECTS_WIDTH, EFFECTS_HEIGHT)
            text_rect = text_surface.get_rect(center=rect.center)
            WIN.blit(text_surface, text_rect)

    def enemy_moveset(self):
        if self.hp > 0: # if still alive
            if self.name == 'confidence':
                self.confidence_enemy_turns()
            elif self.name == 'less_draw':
                self.less_draw_enemy_turns()
            elif self.name == 'less_energy':
                self.less_energy_enemy_turns()
            elif self.name == 'weak_death':
                self.weak_death_enemy_turns()
            elif self.name == 'vulnerable_death':
                self.vulnerable_death_enemy_turns()
            elif self.name == 'frail_death':
                self.frail_death_enemy_turns()

    def show_enemy_intention(self): # will need to update the enemy intention first
        counter = 0
        if self.attack_intent == True:
            self.draw_intention(ATTACK_INTENT, counter)
            counter += 1
        if self.block_intent == True:
            self.draw_intention(BLOCK, counter)
            counter += 1
        if self.debuff_intent == True:
            self.draw_intention(DEBUFF_INTENT, counter)
            counter += 1
        # if self.power_up_intent == True:
        #     self.draw_intention(XXXXX, counter) # need to get images for all of these things
        #     counter += 1
        if self.energy_steal_intent == True:
            self.draw_intention(ENERGY_STEAL_INTENT_IMG, counter)
            counter += 1
        if self.card_steal_intent == True:
            self.draw_intention(CARD_STEAL_INTENT_IMG, counter)
            counter += 1
        # if self.curse_intent == True:
        #     self.draw_intention(XXXXX, counter)
        #     counter += 1

    def enemy_intentions(self):
        if self.hp > 0: # if still alive
            if self.name == 'confidence':
                self.confidence_enemy_intent()
            elif self.name == 'less_draw':
                self.less_draw_enemy_intent()
            elif self.name == 'less_energy':
                self.less_energy_enemy_intent()
            elif self.name == 'weak_death':
                self.weak_death_enemy_intent()
            elif self.name == 'vulnerable_death':
                self.vulnerable_death_enemy_intent()
            elif self.name == 'frail_death':
                self.frail_death_enemy_intent()
    
    def confidence_enemy_turns(self):
        if self.has_block == False:
            self.enemy_dmg_dealt(4, 0.5) # cowardice
        elif self.has_block:
            self.enemy_dmg_dealt(4, 2) # confidence
        self.block += self.enemy_block(3)

    def confidence_enemy_intent(self):
        self.attack_intent = True
        if self.has_block == False:
            self.attack_actual = self.enemy_attack(4, 0.5) # cowardice
        elif self.has_block:
            self.attack_actual = self.enemy_attack(4, 2) # confidence
        self.block_intent = True
        self.block_actual = self.enemy_block(3)

    def less_draw_enemy_turns(self):
        if turn == 1:
            p1.new_turn_additional_draw -= 1
        elif p1.new_turn_draw_cards() > 4:
            p1.new_turn_additional_draw -= 1
        else:
            if self.ran_num <= 50:
                self.enemy_dmg_dealt(6) # 6 hp
                self.block += self.enemy_block(5) # 5 block
            else:
                if p1.temp_additional_draw == 0:
                    p1.temp_additional_draw -= 2 # it updates before p1 turn to be only -1
                else:
                    p1.temp_additional_draw -= 1 # # this means it will only ever be able to reduce cards drawn by 2

    def less_draw_enemy_intent(self):
        if turn == 1:
            self.card_steal_intent = True
        elif p1.new_turn_draw_cards() > 4:
            self.card_steal_intent = True
        else:
            if self.ran_num <= 50:
                self.attack_intent = True
                self.attack_actual = self.enemy_attack(6)
                self.block_intent = True
                self.block_actual = self.enemy_block(5)
            else:
                self.card_steal_intent = True

    def less_energy_enemy_turns(self):
        if turn == 1:
            p1.additional_energy -= 1
        elif p1.energy > 2:
            p1.additional_energy -= 1
        else:
            if self.ran_num <= 50:
                self.enemy_dmg_dealt(6) # 6 hp
                self.block += self.enemy_block(5) # 5 block
            else:
                if p1.temp_additional_energy == 0:
                    p1.temp_additional_energy -= 2 # it updates before p1 turn to be only -1
                else:
                    p1.temp_additional_energy -= 1 # this means it will only ever be able to reduce energy by 2

    def less_energy_enemy_intent(self):
        if turn == 1:
            self.energy_steal_intent = True
        elif p1.energy > 2:
            self.energy_steal_intent = True
        else:
            if self.ran_num <= 50:
                self.attack_intent = True
                self.attack_actual = self.enemy_attack(6)
                self.block_intent = True
                self.block_actual = self.enemy_block(5)
            else:
                self.energy_steal_intent = True
    
    def weak_death_enemy_turns(self):
        if self.ran_num <= 50:
            self.enemy_dmg_dealt(7) # 7 hp
        else:
            p1.weak += 2

    def weak_death_enemy_intent(self):
        if self.ran_num <= 50:
            self.attack_intent = True
            self.attack_actual = self.enemy_attack(7)
        else:
            self.debuff_intent = True

    def vulnerable_death_enemy_turns(self):
        if self.ran_num <= 50:
            self.enemy_dmg_dealt(6) # 6 hp
        else:
            p1.vulnerable += 2

    def vulnerable_death_enemy_intent(self):
        if self.ran_num <= 50:
            self.attack_intent = True
            self.attack_actual = self.enemy_attack(6)
        else:
            self.debuff_intent = True

    def frail_death_enemy_turns(self):
        if self.ran_num <= 50:
            self.enemy_dmg_dealt(5) # 5 hp
        else:
            p1.frail += 2

    def frail_death_enemy_intent(self):
        if self.ran_num <= 50:
            self.attack_intent = True
            self.attack_actual = self.enemy_attack(5)
        else:
            self.debuff_intent = True

# character instances
p1 = Player(60, starter_deck)
small_fights = []
boss_fights = []
main_boss_fights = []
confidence_enemy_1 = Enemy('confidence', 10, 3, ENEMY1_X, ENEMY1_Y + CHARACTER_HEIGHT/2, CHARACTER_WIDTH/3, CHARACTER_HEIGHT/2)
confidence_enemy_2 = Enemy('confidence', 10, 3, ENEMY1_X + CHARACTER_WIDTH/3, ENEMY1_Y, CHARACTER_WIDTH/3, CHARACTER_HEIGHT/2)
confidence_enemy_3 = Enemy('confidence', 10, 3, ENEMY1_X + CHARACTER_WIDTH*2/3, ENEMY1_Y + CHARACTER_HEIGHT/2, CHARACTER_WIDTH/3, CHARACTER_HEIGHT/2)
small_fights.append([confidence_enemy_1, confidence_enemy_2, confidence_enemy_3])
less_draw_enemy = Enemy('less_draw', 25, 0, ENEMY1_X, ENEMY1_Y, CHARACTER_WIDTH/2, CHARACTER_HEIGHT)
less_energy_enemy = Enemy('less_energy', 25, 0, ENEMY1_X + CHARACTER_WIDTH/2, ENEMY1_Y, CHARACTER_WIDTH/2, CHARACTER_HEIGHT)
small_fights.append([less_draw_enemy, less_energy_enemy])
weak_death_enemy = Enemy('weak_death', 10, 5, ENEMY1_X, ENEMY1_Y + CHARACTER_HEIGHT/2, CHARACTER_WIDTH/3, CHARACTER_HEIGHT/2, death_strength=True)
vulnerable_death_enemy = Enemy('vulnerable_death', 15, 5, ENEMY1_X + CHARACTER_WIDTH/3, ENEMY1_Y, CHARACTER_WIDTH/3, CHARACTER_HEIGHT/2, death_strength=True)
frail_death_enemy = Enemy('frail_death', 20, 5, ENEMY1_X + CHARACTER_WIDTH*2/3, ENEMY1_Y + CHARACTER_HEIGHT/2, CHARACTER_WIDTH/3, CHARACTER_HEIGHT/2, death_strength=True)
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
        self.is_hovered = False

    def draw_button(self):
        WIN.blit(self.image, self.rect)
        if self.name == 'energy_button':
            p1.draw_energy()
        elif self.name == 'draw_pile_button' or self.name == 'discard_pile_button' or self.name == 'exhaust_pile_button' or self.name == 'entire_deck_button':
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
end_turn_button = Button('end_turn_button', END_TURN_IMG, RIGHT_BUTTON_X, END_TURN_Y)
pile_buttons = []
pile_buttons.append(draw_pile_button)
pile_buttons.append(discard_pile_button)
pile_buttons.append(exhaust_pile_button)
pile_buttons.append(entire_deck_button)


# functions
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

def all_enemies_defeated(enemies):
    for enemy in enemies:
        if enemy.hp > 0:
            return False
    return True

def updates():
    # global current_enemies # don't think this is needed
    global turn
    global screen_view
    global update
    WIN.blit(PIRATE_BACKGROUND, (0, 0))
    # enemy stuff
    if all_enemies_defeated(current_enemies):
        turn = 1
        screen_view = reward
    for enemy in current_enemies:
        if enemy.hp <= 0 and enemy.death_strength == True: # if p1 kills an enemy that reduces p1 str on death
            p1.strength -= 2
            enemy.death_strength = False
        if enemy.hp > 0:
            enemy.draw_enemy()
            enemy.draw_hp()
            enemy.update_status()
            if player_turn: # stops it from resetting block to zero and then checking it at the end of the turn
                enemy.block_checker()
            enemy.reset_intent()
            enemy.enemy_intentions() # works out enemy intentions
            enemy.show_enemy_intention() # blits intentions on screen
    # p1 stuff
    if p1.hp <= 0:
        pygame.time.delay(3000)
        screen_view = death # not actually got anything for this yet
    else:
        p1.draw_player()
        p1.draw_hp()
        p1.update_status()
    # cards
    card_pos = 1
    for card in p1.active_hand:
        card.blit_card(card_pos, len(p1.active_hand))
        card_pos += 1
    # buttons
    if end_turn_button.is_hovered:
        WIN.blit(STEERING_WHEEL_IMG, (RIGHT_BUTTON_X + DRAW_PILE_WIDTH/2 - DRAW_PILE_WIDTH*1.5/2, END_TURN_Y + DRAW_PILE_HEIGHT/2 - DRAW_PILE_HEIGHT*1.5/2))
    for button in pile_buttons:
        button.draw_button()
    energy_button.draw_button()
    end_turn_button.draw_button()
    pygame.display.update()
    update = False



def main():

    clock = pygame.time.Clock()
    global current_enemies
    global turn
    global screen_view
    global update
    global player_turn
    new_fight = True
    new_turn = True
    enemy_level = 'small'
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
                if screen_view == fight:
                    for card in p1.active_hand:
                        if card.sel_rect.collidepoint(event.pos) and card.is_hovered == False:
                            card.is_hovered = True
                            card.draw_description()
                            pygame.display.update()
                        elif card.sel_rect.collidepoint(event.pos) == False and card.is_hovered:
                            card.is_hovered = False
                            desc_rect = pygame.Rect(DESCRIPTION_X, DESCRIPTION_Y, DESCRIPTION_WIDTH, DESCRIPTION_HEIGHT)
                            pygame.draw.rect(WIN, LIGHT_BLUE, desc_rect)
                            pygame.display.update()

                    if end_turn_button.rect.collidepoint(event.pos) and end_turn_button.is_hovered == False:
                        end_turn_button.is_hovered = True
                        update = True
                    elif end_turn_button.rect.collidepoint(event.pos) == False and end_turn_button.is_hovered == True:
                        end_turn_button.is_hovered = False
                        update = True
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if screen_view == fight:
                    # selecting cards
                    if player_turn:
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
                                            if card.exhausts:
                                                p1.exhaust_pile.append(card)
                                            else:
                                                p1.discard_pile.append(card)
                                            p1.active_hand.remove(card)
                                            update = True
                                        
                                        elif (card.type == skill or card.type == power) and p1.rect.collidepoint(event.pos): # if skill or power card selected and selects player
                                            p1.card_played(card, enemy)
                                            a_card_selected = False
                                            if card.exhausts:
                                                p1.exhaust_pile.append(card)
                                            else:
                                                p1.discard_pile.append(card)
                                            p1.active_hand.remove(card)
                                            update = True
                    
                    # clicking end turn button
                    if end_turn_button.rect.collidepoint(event.pos):
                        for i in range(len(p1.active_hand)):
                            p1.discard_pile.append(p1.active_hand[0])
                            p1.active_hand.remove(p1.active_hand[0])
                        player_turn = False
                        for enemy in current_enemies:
                            enemy.block_checker()
                            enemy.reduce_status()
                        updates()

                if screen_view != card_view:
                    # selecting the draw/discard/exhaust/deck pile
                    current_screen_view = screen_view # saves what the screen was before going to screen_view
                if screen_view == fight or screen_view == card_view or screen_view == map or screen_view == reward or screen_view == shop or screen_view == event:
                    if player_turn:
                        for button in pile_buttons:
                            if button.rect.collidepoint(event.pos):
                                clicked = True
                                if button.is_clicked == False:
                                    for b in pile_buttons:
                                        b.is_clicked = False # allows you to switch between different buttons indefinitely without it closing
                                    button.is_clicked = True
                                    screen_view = card_view
                                    button.show_cards()

                                elif button.is_clicked: # if we click the button and it was already clicked...
                                    button.is_clicked = False
                                    screen_view = current_screen_view # go back to the last screen you were on
                                    update = True # go back to in game screen

            elif event.type == pygame.MOUSEBUTTONUP: # prevents one click doing multiple actions
                if clicked == True:
                    clicked = False

        if screen_view == fight:
            if new_fight == True:
                randomise_fight(enemy_level)
                for card in p1.deck:
                    p1.draw_pile.append(card)
                random.shuffle(p1.draw_pile)
                new_fight = False

            elif new_turn == True:
                p1.draw_card(p1.new_turn_draw_cards())
                p1.energy = p1.new_turn_energy()
                for enemy in current_enemies:
                    enemy.ran_num = random.randint(1, 100)
                new_turn = False
                update = True

            elif update == True:
                updates()
            
            elif player_turn == False: # enemies turn
                for enemy in current_enemies:
                    pygame.time.delay(1000)
                    enemy.enemy_moveset()
                    updates()
                turn += 1
                p1.reduce_status() # because this reduces status straight away i'll need to set the effects to +1 more than i wanted if that status is at 0
                new_turn = True
                player_turn = True

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

# make the hp into a health bar which goes blue with block (like sts), meaning i'll have to remove the block from the current list
# find a few different pirate themed background images for fights to happen in
# figure out how to show fixed enemy abilities (like the stregth debuff on death enemy)
# blit in the name of the lists when looking at draw/discard/etc piles (could have it show in the same place as card desc?)
# blit in something that says cards order is hidden on draw pile list
# do the rewards logic
# do the logic for reset status
# write logic for things like poison and all other status effects to actually do something
# add in something so that when you hover over a status effect it will tell you the effect
# to do the above i might need to turn the images into it's own class

# problems

# can't figure out how to update the card colour when hovered