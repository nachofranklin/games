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

# width and heights
WIN_WIDTH = 1200
WIN_HEIGHT = 800
CARD_WIDTH = WIN_WIDTH/8
CARD_HEIGHT = WIN_HEIGHT/3
CHARACTER_WIDTH = WIN_WIDTH/3
CHARACTER_HEIGHT = WIN_HEIGHT/3
EFFECTS_WIDTH = EFFECTS_HEIGHT = WIN_WIDTH/27
END_TURN_WIDTH = CARD_WIDTH
END_TURN_HEIGHT = CARD_HEIGHT/3
ENERGY_WIDTH = ENERGY_HEIGHT = WIN_HEIGHT/20 # radius
DESCRIPTION_WIDTH = WIN_WIDTH/2 - CARD_WIDTH/2 - CARD_WIDTH/3 - CARD_WIDTH*2/3*MAX_CARDS_IN_HAND/2 + CARD_WIDTH*2/3*1
DESCRIPTION_HEIGHT = WIN_HEIGHT*4/5 - CARD_HEIGHT/2 - CARD_HEIGHT/4

# x and y co-ordinates
P1_X = WIN_WIDTH/9
P1_Y = ENEMY1_Y = WIN_HEIGHT/9
ENEMY1_X = WIN_WIDTH*5/9
EFFECTS_Y = P1_Y + CHARACTER_HEIGHT
END_TURN_X = WIN_WIDTH - END_TURN_WIDTH*1.25
END_TURN_Y = WIN_HEIGHT*3/5 - END_TURN_HEIGHT*1.25
ENERGY_X = ENERGY_WIDTH*2
ENERGY_Y = WIN_HEIGHT*3/5 - ENERGY_HEIGHT*1.5
DESCRIPTION_X = CARD_WIDTH*2/3*10
DESCRIPTION_Y = CARD_HEIGHT/8

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

# images...
BLOCK_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'block.png'))
BLOCK = pygame.transform.scale(BLOCK_IMAGE, (EFFECTS_WIDTH, EFFECTS_HEIGHT))
SHIELD_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'shield.png'))
SHIELD = pygame.transform.scale(SHIELD_IMAGE, (EFFECTS_WIDTH, EFFECTS_HEIGHT))
STRENGTH_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'strength.png'))
STRENGTH = pygame.transform.scale(STRENGTH_IMAGE, (EFFECTS_WIDTH, EFFECTS_HEIGHT))
DEXTERITY_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'dexterity.png'))
DEXTERITY = pygame.transform.scale(DEXTERITY_IMAGE, (EFFECTS_WIDTH, EFFECTS_HEIGHT))
WEAK_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'weak.png'))
WEAK = pygame.transform.scale(WEAK_IMAGE, (EFFECTS_WIDTH, EFFECTS_HEIGHT))
VULNERABLE_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'vulnerable.png'))
VULNERABLE = pygame.transform.scale(VULNERABLE_IMAGE, (EFFECTS_WIDTH, EFFECTS_HEIGHT))
FRAIL_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'frail.png'))
FRAIL = pygame.transform.scale(FRAIL_IMAGE, (EFFECTS_WIDTH, EFFECTS_HEIGHT))
POISON_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'poison.png'))
POISON = pygame.transform.scale(POISON_IMAGE, (EFFECTS_WIDTH, EFFECTS_HEIGHT))
THORNS_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'thorns.png'))
THORNS = pygame.transform.scale(THORNS_IMAGE, (EFFECTS_WIDTH, EFFECTS_HEIGHT))
ADDITIONAL_ENERGY_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'energy.png'))
ADDITIONAL_ENERGY = pygame.transform.scale(ADDITIONAL_ENERGY_IMAGE, (EFFECTS_WIDTH, EFFECTS_HEIGHT))

def update_p1_status():
    p1_status_effects = []
    if p1.block != 0:
        p1_status_effects.append({'image':BLOCK, 'number':p1.block})
    if p1.shield != 0:
        p1_status_effects.append({'image':SHIELD, 'number':p1.shield})
    if p1.strength != 0:
        p1_status_effects.append({'image':STRENGTH, 'number':p1.strength})
    if p1.dexterity != 0:
        p1_status_effects.append({'image':DEXTERITY, 'number':p1.dexterity})
    if p1.weak != 0:
        p1_status_effects.append({'image':WEAK, 'number':p1.weak})
    if p1.vulnerable != 0:
        p1_status_effects.append({'image':VULNERABLE, 'number':p1.vulnerable})
    if p1.frail != 0:
        p1_status_effects.append({'image':FRAIL, 'number':p1.frail})
    if p1.poison != 0:
        p1_status_effects.append({'image':POISON, 'number':p1.poison})
    if p1.thorns != 0:
        p1_status_effects.append({'image':THORNS, 'number':p1.thorns})
    if p1.additional_energy != 0:
        p1_status_effects.append({'image':ADDITIONAL_ENERGY, 'number':p1.additional_energy})
    
    status_counter = 0
    if len(p1_status_effects) > 0:
        for status in p1_status_effects:
            draw_status(status['image'], status['number'], status_counter, P1_X)
            status_counter +=1

def update_enemy_status(enemy, enemy_x):
    enemy_status_effects = []
    if enemy.block != 0:
        enemy_status_effects.append({'image':BLOCK, 'number':enemy.block})
    if enemy.shield != 0:
        enemy_status_effects.append({'image':SHIELD, 'number':enemy.shield})
    if enemy.strength != 0:
        enemy_status_effects.append({'image':STRENGTH, 'number':enemy.strength})
    if enemy.dexterity != 0:
        enemy_status_effects.append({'image':DEXTERITY, 'number':enemy.dexterity})
    if enemy.weak != 0:
        enemy_status_effects.append({'image':WEAK, 'number':enemy.weak})
    if enemy.vulnerable != 0:
        enemy_status_effects.append({'image':VULNERABLE, 'number':enemy.vulnerable})
    if enemy.frail != 0:
        enemy_status_effects.append({'image':FRAIL, 'number':enemy.frail})
    if enemy.poison != 0:
        enemy_status_effects.append({'image':POISON, 'number':enemy.poison})
    if enemy.thorns != 0:
        enemy_status_effects.append({'image':THORNS, 'number':enemy.thorns})
    
    status_counter = 0
    if len(enemy_status_effects) > 0:
        for status in enemy_status_effects:
            draw_status(status['image'], status['number'], status_counter, enemy_x)
            status_counter +=1

def draw_status(image, number, counter, character_x):
    font = pygame.font.Font(None, int(EFFECTS_WIDTH*2/3))
    text_surface = font.render(str(number), True, BLACK)
    rect = pygame.Rect(character_x + EFFECTS_WIDTH*counter, EFFECTS_Y, EFFECTS_WIDTH, EFFECTS_HEIGHT)
    text_rect = text_surface.get_rect(center=rect.center)

    WIN.blit(image, (character_x + EFFECTS_WIDTH*counter, EFFECTS_Y))
    WIN.blit(text_surface, text_rect)

# sounds...

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

    def draw_hp(self):
        font = pygame.font.Font(None, int(CARD_WIDTH/3))
        text_surface = font.render(f'{self.hp}/{self.max_hp}', True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        WIN.blit(text_surface, text_rect)

class Player(Character):
    def __init__(self, hp, starter_deck):
        super().__init__(hp)
        self.gold = 50
        self.additional_energy = 0
        self.temp_additional_energy = 0
        self.energy = 3 + self.additional_energy + self.temp_additional_energy
        self.new_turn_additional_draw = 0
        self.temp_additional_draw = 0
        self.new_turn_draw_cards = 5 + self.new_turn_additional_draw + self.temp_additional_draw
        self.deck = starter_deck
        self.draw_pile = []
        self.active_hand = []
        self.discard_pile = []
        self.exhaust_pile = []
        self.floor_level = 1
        self.rect = pygame.Rect(P1_X, P1_Y, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    
    def draw_player(self):
        pygame.draw.rect(WIN, GREEN, self.rect)

    def draw_energy(self):
        ENERGY_COORDS = (ENERGY_X, ENERGY_Y)
        pygame.draw.circle(WIN, YELLOW, ENERGY_COORDS, ENERGY_WIDTH)
        font = pygame.font.Font(None, int(CARD_WIDTH/3))
        text_surface = font.render(str(self.energy), True, BLACK)
        text_rect = text_surface.get_rect(center=ENERGY_COORDS)
        WIN.blit(text_surface, text_rect)

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

class Card:
    def __init__(self, name, energy, rarity, type, short_description, long_description, picture=None, player_hp=0, enemy_hp=0, block=0, shield=0, player_strength=0, enemy_strength=0, player_dexterity=0, enemy_dexterity=0, player_weak=0, enemy_weak=0, player_vulnerable=0, enemy_vulnerable=0, player_frail=0, enemy_frail=0, player_poison=0, enemy_poison=0, draw_extra_card=0, discard=0, exhaust=0, thorns=0, locked=0, player_energy=0):
        global card_id_counter
        self.id = card_id_counter
        card_id_counter += 1
        self.name = name
        self.energy = energy
        self.rarity = rarity
        self.type = type
        self.short_description = short_description
        self.long_description = long_description
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
    
    def draw_card(self, position, cards_in_hand):
        self.rect = pygame.Rect(WIN_WIDTH/2 - CARD_WIDTH/2 - CARD_WIDTH/3 - CARD_WIDTH*2/3*cards_in_hand/2 + CARD_WIDTH*2/3*position, WIN_HEIGHT*4/5 - CARD_HEIGHT/2, CARD_WIDTH, CARD_HEIGHT)
        if position == cards_in_hand: # if last card it has a bigger rect than the others
            self.sel_rect = pygame.Rect(WIN_WIDTH/2 - CARD_WIDTH/2 - CARD_WIDTH/3 - CARD_WIDTH*2/3*cards_in_hand/2 + CARD_WIDTH*2/3*position, WIN_HEIGHT*4/5 - CARD_HEIGHT/2, CARD_WIDTH - 2, CARD_HEIGHT)
        else:
            self.sel_rect = pygame.Rect(WIN_WIDTH/2 - CARD_WIDTH/2 - CARD_WIDTH/3 - CARD_WIDTH*2/3*cards_in_hand/2 + CARD_WIDTH*2/3*position, WIN_HEIGHT*4/5 - CARD_HEIGHT/2, CARD_WIDTH*2/3 - 2, CARD_HEIGHT)
        
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

    def draw_text(self):
        text_surface = self.font.render(self.name, True, self.text_colour)
        text_rect = text_surface.get_rect(center=self.rect.center)
        text_surface2 = self.font.render(str(self.energy), True, self.text_colour)
        text_rect2 = text_surface2.get_rect(topleft=self.rect.topleft)
        WIN.blit(text_surface, text_rect)
        WIN.blit(text_surface2, text_rect2)
    
    def draw_description(self):
        desc_rect = pygame.Rect(WIN_WIDTH/2 - CARD_WIDTH/2 - CARD_WIDTH/3 - CARD_WIDTH*2/3*MAX_CARDS_IN_HAND/2 + CARD_WIDTH*2/3*1, WIN_HEIGHT*4/5 - CARD_HEIGHT/2 - CARD_HEIGHT/4, CARD_WIDTH*2/3*10, CARD_HEIGHT/8)
        pygame.draw.rect(WIN, self.colour, desc_rect)
        text_surface = self.font.render(self.long_description, True, self.text_colour)
        text_rect = text_surface.get_rect(center=desc_rect.center)
        WIN.blit(text_surface, text_rect)

class AttackCard(Card):
    def __init__(self, name, energy, rarity, type, enemy_select, short_description, long_description, picture=None, player_hp=0, enemy_hp=0, block=0, shield=0, player_strength=0, enemy_strength=0, player_dexterity=0, enemy_dexterity=0, player_weak=0, enemy_weak=0, player_vulnerable=0, enemy_vulnerable=0, player_frail=0, enemy_frail=0, player_poison=0, enemy_poison=0, draw_extra_card=0, discard=0, exhaust=0, thorns=0, locked=0, player_energy=0):
        super().__init__(name, energy, rarity, type, short_description, long_description, picture, player_hp, enemy_hp, block, shield, player_strength, enemy_strength, player_dexterity, enemy_dexterity, player_weak, enemy_weak, player_vulnerable, enemy_vulnerable, player_frail, enemy_frail, player_poison, enemy_poison, draw_extra_card, discard, exhaust, thorns, locked, player_energy)
        self.type = attack
        self.enemy_select = enemy_select

punch = AttackCard('Punch', 1, starter, attack, select, 'Deal {num} dmg.', 'Punch for {num} base damage', enemy_hp=5)
punch2 = AttackCard('Punch', 1, starter, attack, select, 'Deal {num} dmg.', 'Punch for {num} base damage', enemy_hp=5)
punch3 = AttackCard('Punch', 1, starter, attack, select, 'Deal {num} dmg.', 'Punch for {num} base damage', enemy_hp=5)
punch4 = AttackCard('Punch', 1, starter, attack, select, 'Deal {num} dmg.', 'Punch for {num} base damage', enemy_hp=5)
punch5 = AttackCard('Punch', 1, starter, attack, select, 'Deal {num} dmg.', 'Punch for {num} base damage', enemy_hp=5)
parry = Card('Parry', 1, starter, skill, 'Gain {num} block.', 'Gain {num} block', block=4)
parry2 = Card('Parry', 1, starter, skill, 'Gain {num} block.', 'Gain {num} block', block=4)
parry3 = Card('Parry', 1, starter, skill, 'Gain {num} block.', 'Gain {num} block', block=4)
parry4 = Card('Parry', 1, starter, skill, 'Gain {num} block.', 'Gain {num} block', block=4)
parry5 = Card('Parry', 1, starter, skill, 'Gain {num} block.', 'Gain {num} block', block=4)
jab = AttackCard('Jab', 0, starter, attack, select, 'Deal {num} dmg.\nApply {num2} vulnerable.', 'Jab for {num} base damage and apply {num2} vulnerable', enemy_hp=3, enemy_vulnerable=2)
test = Card('Test', 0, starter, power, 'test', 'test', player_dexterity=2, player_vulnerable=2, player_strength=1, player_poison=4)

starter_deck = []
# starter_deck.extend([punch] * 5)
# starter_deck.extend([parry] * 5)
# starter_deck.extend([jab] * 1)
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

p1 = Player(60, starter_deck)
enemy1 = Enemy(20, 3, ENEMY1_X, ENEMY1_Y, CHARACTER_WIDTH, CHARACTER_HEIGHT)
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

def card_played(card, player, enemy): # do i need it to say player here or can i replace it with p1?
    if enemy.vulnerable >= 1:
        VULNERABLE_MULTIPLIER = 1.5
    else:
        VULNERABLE_MULTIPLIER = 1
    if player.weak >= 1:
        WEAK_MULTIPLIER = 0.75
    else:
        WEAK_MULTIPLIER = 1
    if player.frail >= 1:
        FRAIL_MULTIPLIER = 0.75
    else:
        FRAIL_MULTIPLIER = 1

    player.energy -= card.energy
    player.hp -= card.player_hp

    if card.enemy_hp >= 1:
        if enemy.block < round((card.enemy_hp + player.strength) * VULNERABLE_MULTIPLIER * WEAK_MULTIPLIER):
            enemy.hp -= round((card.enemy_hp + player.strength) * VULNERABLE_MULTIPLIER * WEAK_MULTIPLIER) - enemy.block
            enemy.block = 0
        else:
            enemy.block -= round((card.enemy_hp + player.strength) * VULNERABLE_MULTIPLIER * WEAK_MULTIPLIER)
    
    if card.block >= 1:
        player.block += round((card.block + player.dexterity) * FRAIL_MULTIPLIER)
    player.shield += card.shield
    player.strength += card.player_strength
    enemy.strength -= card.enemy_strength
    player.dexterity += card.player_dexterity
    enemy.dexterity -= card.enemy_dexterity
    player.weak += card.player_weak
    enemy.weak += card.enemy_weak
    player.vulnerable += card.player_vulnerable
    enemy.vulnerable += card.enemy_vulnerable
    player.poison += card.player_poison
    enemy.poison += card.enemy_poison
    # card.draw_extra_card
    # card.discard
    # card.exhaust
    player.thorns += card.thorns
    # card.locked
    # card.player_energy
    card.is_selected = False

def main():

    clock = pygame.time.Clock()
    WIN.fill(LIGHT_BLUE)
    p1.draw_player()
    current_enemies = []
    for enemy in small_fights[2]:
        current_enemies.append(enemy)
    for enemy in current_enemies:
        enemy.draw_enemy()
    pygame.display.update()
    clicked = False
    a_card_selected = False
    update = False
    stage = 1
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()

            elif event.type == pygame.MOUSEMOTION:
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
                                    card_played(card, p1, enemy)
                                    a_card_selected = False
                                    p1.discard_pile.append(p1.active_hand.remove(card))
                                    update = True
                                
                                elif (card.type == skill or card.type == power) and p1.rect.collidepoint(event.pos): # if skill or power card selected and selects player
                                    card_played(card, p1, enemy)
                                    a_card_selected = False
                                    p1.discard_pile.append(p1.active_hand.remove(card))
                                    update = True

            elif event.type == pygame.MOUSEBUTTONUP: # prevents one click doing multiple actions
                if clicked == True:
                    clicked = False

        if update == True:
            WIN.fill(LIGHT_BLUE)
            p1.draw_player()
            p1.draw_hp()
            p1.draw_energy()
            for enemy in current_enemies:
                enemy.draw_enemy()
                enemy.draw_hp()
                update_enemy_status(enemy, enemy.x_pos)
                if enemy.hp <= 0 and enemy.death_strength == True: # if p1 kills an enemy that reduces p1 str on death
                    p1.strength -= 2
                    enemy.death_strength = False
            draw_end_turn_button()
            update_p1_status()
            card_pos = 1
            for card in p1.active_hand:
                card.draw_card(card_pos, len(p1.active_hand))
                card_pos += 1
            pygame.display.update()
            update = False
        
        if stage == 1:
            p1.draw_hp()
            for enemy in current_enemies:
                enemy.draw_enemy()
                enemy.draw_hp()
                update_enemy_status(enemy, enemy.x_pos)
            p1.energy = 3
            p1.draw_energy()
            draw_end_turn_button()
            p1.draw_pile = p1.deck
            random.shuffle(p1.draw_pile)
            for i in range(p1.new_turn_draw_cards):
                p1.active_hand.append(p1.draw_pile.pop())
            card_pos = 1
            for card in p1.active_hand:
                card.draw_card(card_pos, len(p1.active_hand))
                card_pos += 1
            pygame.display.update()
            stage = 2

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

# to do

# add in a draw pile button to see what's left in the draw pile
# same for discard and exhaust pile
# same for a whole deck button
# add in a player image and rect, along with hp, block and other effects
# add in the same for an enemy
# add in an end turn button (currently doesn't do anything)
# add in something that shows what the enemy is about to do next
# add in something to show all status effects
# add logic that kills an enemy when hp goes to 0 or below
# add logic that kills the player when hp goes to 0 or below
# create set variables for width/height/x/y for end turn button and energy
# then move them so that they're not getting obscured
# change the update status into the character class

# problems

# can't figure out how to update the card colour when hovered
# the cards aren´t actually central when blit. Add 1/3 of a card width to the x, but needs to stay as it is if there's only one card