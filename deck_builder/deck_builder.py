import pygame
import os
import random
import numpy as np

pygame.font.init()
pygame.mixer.init()

# variables
PATH = 'C:\\Users\\NathanFranklin\\Documents\\Nath\\Coding\\games\\deck_builder\\'

WIN_WIDTH = 1000
WIN_HEIGHT = 620
CARD_WIDTH = WIN_WIDTH/8
CARD_HEIGHT = WIN_HEIGHT/3
FPS = 60
MAX_CARDS_IN_HAND = 10
card_id_counter = 1

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

variables = []
player_hp = 'player_hp'
enemy_hp = 'enemy_hp'
gold = 'gold'
block = 'block'
shield = 'shield'
player_strength = 'player_strength'
enemy_strength = 'enemy_strength'
player_dexterity = 'player_dexterity'
enemy_dexterity = 'enemy_dexterity'
player_weak = 'player_weak'
enemy_weak = 'enemy_weak'
player_vulnerable = 'player_vulnerable'
enemy_vulnerable = 'enemy_vulnerable'
player_poison = 'player_poison'
enemy_poison = 'enemy_poison'
locked = 'locked' # could be tricky because it applies to a card, not a variable, and the rest are player variables
discard = 'discard' # could be tricky because it applies to a card, not a variable
exhaust = 'exhaust' # could be tricky because it applies to a card, not a variable
draw_card = 'draw_card'
player_energy = 'player_energy'
card_energy = 'card_energy'
variables.append(player_hp)
variables.append(enemy_hp)
variables.append(gold)
variables.append(block)
variables.append(shield)
variables.append(player_strength)
variables.append(player_dexterity)
variables.append(player_weak)
variables.append(player_vulnerable)
variables.append(player_poison)
variables.append(enemy_strength)
variables.append(enemy_dexterity)
variables.append(enemy_weak)
variables.append(enemy_vulnerable)
variables.append(enemy_poison)
variables.append(locked)
variables.append(discard)
variables.append(exhaust)
variables.append(draw_card)
variables.append(player_energy)
variables.append(card_energy)

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

# sounds...

def draw_end_turn_button():
    is_hovered = False
    colour = PINK
    hover_colour = WHITE
    font = pygame.font.Font(None, int(CARD_WIDTH/4))
    text_surface = font.render('End Turn', True, BLACK)
    rect = pygame.Rect(WIN_WIDTH - text_surface.get_width()*2, WIN_HEIGHT*3/5 - text_surface.get_height(), CARD_WIDTH, CARD_HEIGHT/3)
    
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
        self.hp = hp
        self.block = 0
        self.shield = 0
        self.strength = 0
        self.dexterity = 0
        self.weak = 0
        self.vulnerable = 0
        self.poison = 0
        self.energy = 0

class Player(Character):
    def __init__(self, hp, starter_deck):
        super().__init__(hp)
        self.gold = 50
        self.deck = starter_deck
        self.draw_pile = []
        self.active_hand = []
        self.discard_pile = []
        self.exhaust_pile = []
        self.floor_level = 1
        self.rect = pygame.Rect(WIN_WIDTH/9, WIN_HEIGHT/6, WIN_WIDTH*3/9, WIN_HEIGHT*2/6)
    
    def draw_player(self):
        pygame.draw.rect(WIN, GREEN, self.rect)

    def draw_energy(self):
        ENERGY_COORDS = (WIN_WIDTH*1/10, WIN_HEIGHT*3/5)
        pygame.draw.circle(WIN, YELLOW, ENERGY_COORDS, WIN_HEIGHT/20)
        font = pygame.font.Font(None, int(CARD_WIDTH/3))
        text_surface = font.render(str(self.energy), True, BLACK)
        text_rect = text_surface.get_rect(center=ENERGY_COORDS)
        WIN.blit(text_surface, text_rect)

class Enemy(Character):
    def __init__(self, hp, x_pos, y_pos, width, height):
        super().__init__(hp)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
    
    def draw_enemy(self):
        pygame.draw.rect(WIN, ORANGE, self.rect)

class Card:
    def __init__(self, name, energy, rarity, type, impacts, num, short_description, long_description, picture=None, impacts2=None, num2=0, impacts3=None, num3=0):
        global card_id_counter
        self.id = card_id_counter
        card_id_counter += 1
        self.name = name
        self.energy = energy
        self.rarity = rarity
        self.type = type
        self.impacts = impacts
        self.num = num
        self.impacts2 = impacts2
        self.num2 = num2
        self.impacts3 = impacts3
        self.num3 = num3
        self.short_description = short_description.format(num=self.num, num2=self.num2, num3=self.num3)
        self.long_description = long_description.format(num=self.num, num2=self.num2, num3=self.num3)
        self.picture = picture
        self.colour = BLUE
        self.hover_colour = BLACK
        self.text_colour = WHITE
        self.font = pygame.font.Font(None, int(CARD_WIDTH/6))  # customize the font and size
        self.is_hovered = False
    
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
    def __init__(self, name, energy, rarity, enemy_select, impacts, num, short_description, long_description, picture=None, impacts2=None, num2=0, impacts3=None, num3=0):
        super().__init__(name, energy, rarity, type, impacts, num, short_description, long_description, picture, impacts2, num2, impacts3, num3)
        self.type = attack
        self.enemy_select = enemy_select

punch = AttackCard('Punch', 1, starter, select, enemy_hp, 5, 'Deal {num} dmg.', 'Punch for {num} base damage')
punch2 = AttackCard('Punch', 1, starter, select, enemy_hp, 5, 'Deal {num} dmg.', 'Punch for {num} base damage')
punch3 = AttackCard('Punch', 1, starter, select, enemy_hp, 5, 'Deal {num} dmg.', 'Punch for {num} base damage')
punch4 = AttackCard('Punch', 1, starter, select, enemy_hp, 5, 'Deal {num} dmg.', 'Punch for {num} base damage')
punch5 = AttackCard('Punch', 1, starter, select, enemy_hp, 5, 'Deal {num} dmg.', 'Punch for {num} base damage')
parry = Card('Parry', 1, starter, skill, block, 4, 'Gain {num} block.', 'Gain {num} block')
parry2 = Card('Parry', 1, starter, skill, block, 4, 'Gain {num} block.', 'Gain {num} block')
parry3 = Card('Parry', 1, starter, skill, block, 4, 'Gain {num} block.', 'Gain {num} block')
parry4 = Card('Parry', 1, starter, skill, block, 4, 'Gain {num} block.', 'Gain {num} block')
parry5 = Card('Parry', 1, starter, skill, block, 4, 'Gain {num} block.', 'Gain {num} block')
jab = AttackCard('Jab', 0, starter, select, enemy_hp, 3, 'Deal {num} dmg.\nApply {num2} vulnerable.', 'Jab for {num} base damage and apply {num2} vulnerable', None, enemy_vulnerable, 1)

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

p1 = Player(60, starter_deck)
enemy1 = Enemy(20, WIN_WIDTH*5/9, WIN_HEIGHT/6, WIN_WIDTH*3/9, WIN_HEIGHT*2/6)

def main():

    clock = pygame.time.Clock()
    WIN.fill(LIGHT_BLUE)
    p1.draw_player()
    enemy1.draw_enemy()
    pygame.display.update()
    clicked = False
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
                    elif card.sel_rect.collidepoint(event.pos) == False and card.is_hovered == True:
                        card.is_hovered = False
                        desc_rect = pygame.Rect(WIN_WIDTH/2 - CARD_WIDTH/2 - CARD_WIDTH/3 - CARD_WIDTH*2/3*MAX_CARDS_IN_HAND/2 + CARD_WIDTH*2/3*1, WIN_HEIGHT*4/5 - CARD_HEIGHT/2 - CARD_HEIGHT/4, CARD_WIDTH*2/3*10, CARD_HEIGHT/8)
                        pygame.draw.rect(WIN, LIGHT_BLUE, desc_rect)
                        pygame.display.update()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if clicked == False:
                    clicked = True

            elif event.type == pygame.MOUSEBUTTONUP: # prevents one click doing multiple actions
                clicked = False
        
        if stage == 1:
            p1.energy = 3
            p1.draw_energy()
            draw_end_turn_button()
            p1.draw_pile = p1.deck
            random.shuffle(p1.draw_pile)
            for i in range(5):
                p1.active_hand.append(p1.draw_pile.pop())
            j = 1
            for i in p1.active_hand:
                i.draw_card(j, len(p1.active_hand))
                j += 1
            pygame.display.update()
            stage = 2

main()


# need to create a starting deck

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
# add in somewhere to show remaining energy
# add in an end turn button
# add in something that shows what the enemy is about to do next

# problems

# each card only has one instance, so three strike cards all count as the same card instance (problem when doing things like self.is_hovered)
# because cards overlap, so do the rects, need to find a way to redraw the rects maybe?