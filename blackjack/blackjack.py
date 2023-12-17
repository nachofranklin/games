import pygame
import os
import random
pygame.font.init()
pygame.mixer.init()

# Variables
PATH = '/home/nacho/repos/games/blackjack/'
WIN_WIDTH, WIN_HEIGHT = 1200, 800
CARD_WIDTH, CARD_HEIGHT = 140, 200
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 80
FPS = 60
player_win_count = 0
dealer_win_count = 0

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)
LIGHT_BLUE = (173, 216, 230)

# Screen
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Blackjack')

# Sounds
DRAW_CARD_SOUND = pygame.mixer.Sound(os.path.join(PATH, 'sounds', 'card_flip.wav'))
FART_SOUND = pygame.mixer.Sound(os.path.join(PATH, 'sounds', 'fart.wav'))
CHA_CHING_SOUND = pygame.mixer.Sound(os.path.join(PATH, 'sounds', 'cha_ching.wav'))
FIREWORKS_SOUND = pygame.mixer.Sound(os.path.join(PATH, 'sounds', 'fireworks.wav'))

# Images
CARD_BACK_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'card_back.png'))
CARD_BACK = pygame.transform.scale(CARD_BACK_IMAGE, (CARD_WIDTH, CARD_HEIGHT))
ROULETTE_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'roulette.png'))
ROULETTE = pygame.transform.scale(ROULETTE_IMAGE, (WIN_WIDTH, WIN_HEIGHT))
BACKGROUND = ROULETTE
CONFETTI_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'confetti.png'))
frame_scale = 2
CONFETTI_SCALED = pygame.transform.scale(CONFETTI_IMAGE, (CONFETTI_IMAGE.get_width() * frame_scale, CONFETTI_IMAGE.get_height() * frame_scale))
FIREWORKS_IMAGE = pygame.image.load(os.path.join(PATH, 'images', 'fireworks.png'))
fireworks_scale = 4
FIREWORKS_SCALED = pygame.transform.scale(FIREWORKS_IMAGE, (FIREWORKS_IMAGE.get_width() * fireworks_scale, FIREWORKS_IMAGE.get_height() * fireworks_scale))
fireworks_scale_small = 2
FIREWORKS_SCALED_SMALL = pygame.transform.scale(FIREWORKS_IMAGE, (FIREWORKS_IMAGE.get_width() * fireworks_scale_small, FIREWORKS_IMAGE.get_height() * fireworks_scale_small))

# Breaking down the confetti spritesheet into a list of images
confetti = []
frame_width = 512 * frame_scale
frame_height = 512 * frame_scale
rows = CONFETTI_SCALED.get_height() // frame_height
columns = CONFETTI_SCALED.get_width() // frame_width
frame_index = 0

for row in range(rows):
    for col in range(columns):
        frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        frame.blit(CONFETTI_SCALED, (0, 0), (col * frame_width, row * frame_height, frame_width, frame_height))
        confetti.append(frame)

def confetti_animation(screen, x, y):
    global frame_index
    CHA_CHING_SOUND.play()
    while frame_index < len(confetti):
        WIN.blit(ROULETTE, (0, 0))
        screen.blit(confetti[frame_index], (x, y))
        if 0 <= frame_index < 16 or 32 <= frame_index < 48:
            PLAYER_WINS_BLUE.blit_text(WIN)
        elif 16 <= frame_index < 32 or 48 <= frame_index < 64:
            PLAYER_WINS_PINK.blit_text(WIN)
        pygame.display.update()
        pygame.time.delay(40)  # Adjust the delay to control the speed of the animation
        frame_index += 1

    frame_index = 0

# Breaking down the fireworks spritesheet into a list of images (adding blank images to stagger the animation)
# should probably make this into a class now that i've used it twice
fireworks = []
fireworks_frame_width = 192 * fireworks_scale
fireworks_frame_height = 192 * fireworks_scale
fireworks_rows = FIREWORKS_SCALED.get_height() // fireworks_frame_height
fireworks_columns = FIREWORKS_SCALED.get_width() // fireworks_frame_width
fireworks_frame_index = 0

for i in range(40):
    frame = pygame.Surface((fireworks_frame_width, fireworks_frame_height), pygame.SRCALPHA)
    fireworks.append(frame)

for row in range(fireworks_rows):
    for col in range(fireworks_columns):
        frame = pygame.Surface((fireworks_frame_width, fireworks_frame_height), pygame.SRCALPHA)
        frame.blit(FIREWORKS_SCALED, (0, 0), (col * fireworks_frame_width, row * fireworks_frame_height, fireworks_frame_width, fireworks_frame_height))
        fireworks.append(frame)

# small fireworks
fireworks_small_1 = []
fireworks_small_2 = []
fireworks_small_3 = []
fireworks_small_4 = []
fireworks_frame_width_small = 192 * fireworks_scale_small
fireworks_frame_height_small = 192 * fireworks_scale_small
fireworks_rows_small = FIREWORKS_SCALED_SMALL.get_height() // fireworks_frame_height_small
fireworks_columns_small = FIREWORKS_SCALED_SMALL.get_width() // fireworks_frame_width_small
fireworks_frame_index = 0 # do i need to change this one or delete it?

for i in range(10):
    frame = pygame.Surface((fireworks_frame_width_small, fireworks_frame_height_small), pygame.SRCALPHA)
    fireworks_small_2.append(frame)

for i in range(20):
    frame = pygame.Surface((fireworks_frame_width_small, fireworks_frame_height_small), pygame.SRCALPHA)
    fireworks_small_3.append(frame)

for i in range(30):
    frame = pygame.Surface((fireworks_frame_width_small, fireworks_frame_height_small), pygame.SRCALPHA)
    fireworks_small_4.append(frame)

for row in range(fireworks_rows_small):
    for col in range(fireworks_columns_small):
        frame = pygame.Surface((fireworks_frame_width_small, fireworks_frame_height_small), pygame.SRCALPHA)
        frame.blit(FIREWORKS_SCALED_SMALL, (0, 0), (col * fireworks_frame_width_small, row * fireworks_frame_height_small, fireworks_frame_width_small, fireworks_frame_height_small))
        fireworks_small_1.append(frame)
        fireworks_small_2.append(frame)
        fireworks_small_3.append(frame)
        fireworks_small_4.append(frame)

for i in range(40):
    frame = pygame.Surface((fireworks_frame_width_small, fireworks_frame_height_small), pygame.SRCALPHA)
    fireworks_small_1.append(frame)

for i in range(30):
    frame = pygame.Surface((fireworks_frame_width_small, fireworks_frame_height_small), pygame.SRCALPHA)
    fireworks_small_2.append(frame)

for i in range(20):
    frame = pygame.Surface((fireworks_frame_width_small, fireworks_frame_height_small), pygame.SRCALPHA)
    fireworks_small_3.append(frame)

for i in range(10):
    frame = pygame.Surface((fireworks_frame_width_small, fireworks_frame_height_small), pygame.SRCALPHA)
    fireworks_small_4.append(frame)

def fireworks_animation(screen):
    global fireworks_frame_index
    FIREWORKS_SOUND.play()
    while fireworks_frame_index < 80:
        WIN.blit(ROULETTE, (0, 0))
        screen.blit(fireworks_small_1[fireworks_frame_index], (WIN_WIDTH//4 - fireworks_frame_width_small//2, WIN_HEIGHT//4 - fireworks_frame_height_small//2))
        screen.blit(fireworks_small_2[fireworks_frame_index], (WIN_WIDTH*3//4 - fireworks_frame_width_small//2, WIN_HEIGHT*3//4 - fireworks_frame_height_small//2))
        screen.blit(fireworks_small_3[fireworks_frame_index], (WIN_WIDTH//4 - fireworks_frame_width_small//2, WIN_HEIGHT*3//4 - fireworks_frame_height_small//2))
        screen.blit(fireworks_small_4[fireworks_frame_index], (WIN_WIDTH*3//4 - fireworks_frame_width_small//2, WIN_HEIGHT//4 - fireworks_frame_height_small//2))
        screen.blit(fireworks[fireworks_frame_index], (WIN_WIDTH//2 - fireworks_frame_width//2, WIN_HEIGHT//2 - fireworks_frame_height//2))
        if 0 <= fireworks_frame_index < 20 or 40 <= fireworks_frame_index < 60:
            BLACKJACK_BLACK.blit_text(WIN)
        elif 20 <= fireworks_frame_index < 40 or 60 <= fireworks_frame_index < 80:
            BLACKJACK_WHITE.blit_text(WIN)
        pygame.display.update()
        pygame.time.delay(60)  # Adjust the delay to control the speed of the animation
        fireworks_frame_index += 1

    fireworks_frame_index = 0

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

# Text
PLAYER_WINS_BLUE = Text(WIN_WIDTH/2, WIN_HEIGHT/2, 0, 0, 'Player Wins!!!', LIGHT_BLUE, 120)
PLAYER_WINS_PINK = Text(WIN_WIDTH/2, WIN_HEIGHT/2, 0, 0, 'Player Wins!!!', PINK, 120)
DEALER_WINS = Text(WIN_WIDTH/2, WIN_HEIGHT/2, 0, 0, 'Dealer Wins!', WHITE, 100)
BLACKJACK_BLACK = Text(WIN_WIDTH/2, WIN_HEIGHT/2, 0, 0, 'B L A C K J A C K', BLACK, 150)
BLACKJACK_WHITE = Text(WIN_WIDTH/2, WIN_HEIGHT/2, 0, 0, 'B L A C K J A C K', WHITE, 150)
PLAYER_STICK = Text(WIN_WIDTH/2, WIN_HEIGHT*9/10, 0, 0, 'Stick', WHITE, 64)
DEALER_STICK = Text(WIN_WIDTH/2, WIN_HEIGHT/10, 0, 0, 'Stick', WHITE, 64)
PLAYER_BUST = Text(WIN_WIDTH/2, WIN_HEIGHT*9/10, 0, 0, 'Bust', WHITE, 64)

def player_wins(): # don´t need this anymore now that iǘe combined it with the confetti
    for i in range(2):
        PLAYER_WINS_BLUE.blit_text(WIN)
        pygame.display.update()
        pygame.time.delay(1000)
        PLAYER_WINS_PINK.blit_text(WIN)
        pygame.display.update()
        pygame.time.delay(1000)
    PLAYER_WINS_BLUE.blit_text(WIN)
    pygame.display.update()
    pygame.time.delay(1000)

def dealer_wins():
    DEALER_WINS.blit_text(WIN)
    pygame.display.update()
    pygame.time.delay(3000)

def blackjack(): # not needed anymore now that i've merged it with fireworks
    for i in range(2):
        BLACKJACK_WHITE.blit_text(WIN)
        pygame.display.update()
        pygame.time.delay(1000)
        BLACKJACK_BLACK.blit_text(WIN)
        pygame.display.update()
        pygame.time.delay(1000)
    BLACKJACK_WHITE.blit_text(WIN)
    pygame.display.update()
    pygame.time.delay(1000)

class Button:
    def __init__(self, x, y, button_width, button_height, text, colour=WHITE, hover_colour=(200, 200, 200), text_colour=BLACK):
        self.rect = pygame.Rect(x, y, button_width, button_height)
        self.text = text
        self.colour = colour
        self.hover_colour = hover_colour
        self.text_colour = text_colour
        self.font = pygame.font.Font(None, 36)  # customize the font and size

    def draw_button(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)
        pygame.draw.rect(screen, self.hover_colour, self.rect, 4)  # Border
        self.draw_text(screen)

    def draw_text(self, screen):
        text_surface = self.font.render(self.text, True, self.text_colour)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Buttons
DRAW_CARD_BUTTON = Button(100, 100, BUTTON_WIDTH, BUTTON_HEIGHT, 'Draw Card')
STICK_BUTTON = Button(100, 300, BUTTON_WIDTH, BUTTON_HEIGHT, 'Stick')
STOP_PLAYING_BUTTON = Button(100, 500, BUTTON_WIDTH, BUTTON_HEIGHT, 'Stop Playing')

class Card:
    def __init__(self, suit, num, score):
        self.suit = suit
        self.num = num
        self.score = score
        self.img = pygame.transform.scale(pygame.image.load(os.path.join(PATH, 'images', str(self.num) + '_of_' + str(self.suit) + '.png')), (CARD_WIDTH, CARD_HEIGHT))

    def show_card(self):
        print(f'{self.num} of {self.suit}')

    def get_score(self):
        return self.score
    
    def blit_card(self, screen, x, y):
        screen.blit(self.img, (x, y))

class DeckOfCards:
    def __init__(self):
        self.deck = []
        self.build()
    
    def build(self):
        for suit in ['clubs', 'diamonds', 'hearts', 'spades']:
            for val in range(1, 14):
                if val == 1:
                    num = 'a'
                    score = 11
                elif val == 13:
                    num = 'k'
                    score = 10
                elif val == 12:
                    num = 'q'
                    score = 10
                elif val == 11:
                    num = 'j'
                    score = 10
                else:
                    num = val
                    score = val
                self.deck.append(Card(suit, num, score))

    def show_deck(self):
        for c in self.deck:
            c.show_card()

    def shuffle(self):
        random.shuffle(self.deck)

    def draw_card(self):
        return self.deck.pop()

class BlackjackPlayer:
    def __init__(self):
        self.hand = []
        self.wins = 0

    def draw(self, deck):
        self.hand.append(deck.draw_card())

    def total(self):
        self.total_val = 0
        self.ace11 = 0
        for card in self.hand:
            self.total_val += card.score
            if card.score == 11:
                self.ace11 += 1
        while self.total_val > 21:
            if self.ace11 > 0:
                self.total_val -= 10
                self.ace11 -= 1
            else:
                break
        return self.total_val
    
    def show_hand(self):
        for card in self.hand:
            card.show_card()
    
    def winner(self):
        self.wins += 1
    
class Dealer(BlackjackPlayer):
    def __init__(self):
        super().__init__()

class Player(BlackjackPlayer):
    def __init__(self, name):
        super().__init__()
        self.name = name

# Blackjack game
def main():

    clock = pygame.time.Clock()
    clock.tick(FPS)
    deck = DeckOfCards()
    deck.shuffle()
    dealer = Dealer()
    nacho = Player('Nacho')
    global dealer_win_count
    global player_win_count
    player_drawn = 0 # could swap this to be len of player.hand
    stop_clicks = 0
    playerIn = True
    dealerIn = True
    # blitted = []

    # Draw background and buttons
    WIN.blit(ROULETTE, (0, 0))
    DRAW_CARD_BUTTON.draw_button(WIN)
    STICK_BUTTON.draw_button(WIN)
    STOP_PLAYING_BUTTON.draw_button(WIN)
    pygame.display.update()
    # blitted.append(WIN.blit(ROULETTE, (0, 0)), DRAW_CARD_BUTTON.draw_button(WIN), STICK_BUTTON.draw_button(WIN), STOP_PLAYING_BUTTON.draw_button(WIN))

    # Draw 2 cards for player and dealer (dealer's first card is face down)
    for i in range(2):
        if i == 0:
            nacho.draw(deck)
            nacho.hand[i].blit_card(WIN, WIN_WIDTH/2 - CARD_WIDTH/2 - CARD_WIDTH, WIN_HEIGHT - CARD_HEIGHT - CARD_HEIGHT/2)
            pygame.display.update()
            # blitted.append(nacho.hand[0].blit_card(WIN, WIN_WIDTH/2 - CARD_WIDTH/2 - CARD_WIDTH, WIN_HEIGHT - CARD_HEIGHT - CARD_HEIGHT/2))
            DRAW_CARD_SOUND.play()
            pygame.time.delay(800)
            dealer.draw(deck)
            WIN.blit(CARD_BACK, (WIN_WIDTH/2 - CARD_WIDTH/2 - CARD_WIDTH, CARD_HEIGHT/2))
            pygame.display.update(WIN.blit(CARD_BACK, (WIN_WIDTH/2 - CARD_WIDTH/2 - CARD_WIDTH, CARD_HEIGHT/2)))
            DRAW_CARD_SOUND.play()
            pygame.time.delay(800)
        else:
            nacho.draw(deck)
            WIN.blit(nacho.hand[i].img, (WIN_WIDTH/2 - CARD_WIDTH, WIN_HEIGHT - CARD_HEIGHT - CARD_HEIGHT/2))
            pygame.display.update()
            DRAW_CARD_SOUND.play()
            pygame.time.delay(800)
            dealer.draw(deck)
            WIN.blit(dealer.hand[i].img, (WIN_WIDTH/2 - CARD_WIDTH, CARD_HEIGHT/2))
            pygame.display.update()
            DRAW_CARD_SOUND.play()
            pygame.time.delay(800)
    
    run = True
    while run:

        # if dealer has blackjack it stops the game
        if len(dealer.hand) == 2 and dealer.total() == 21:
            dealerIn = False
            playerIn = False
        # if either dealer or player gets 21 or over it stops them from drawing more cards
        if nacho.total() == 21:
            if len(nacho.hand) == 2: # if player has blackjack it stops the game
                dealerIn = False
                # playerIn = False # already happens regardless of if statement
            elif len(nacho.hand) > 2:
                PLAYER_STICK.blit_text(WIN)
                pygame.display.update()
            playerIn = False
        if nacho.total() > 21:
            PLAYER_BUST.blit_text(WIN)
            FART_SOUND.play()
            pygame.display.update()
            playerIn = False
        # if dealer.total() >= 21: # this might be a problem of dealer sticking too early when bust
        #     dealerIn = False

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # logic for when the buttons are clicked
                if DRAW_CARD_BUTTON.is_clicked(pygame.mouse.get_pos()):
                    if playerIn and player_drawn < 3:
                        nacho.draw(deck)
                        DRAW_CARD_SOUND.play()
                        player_drawn += 1

                if STICK_BUTTON.is_clicked(pygame.mouse.get_pos()):
                    playerIn = False
                    PLAYER_STICK.blit_text(WIN)
                    pygame.display.update()
                
                if STOP_PLAYING_BUTTON.is_clicked(pygame.mouse.get_pos()):
                    if stop_clicks == 0:
                        WIN.blit(ROULETTE, (0, 0))
                        Text(WIN_WIDTH/2, WIN_HEIGHT/3, 0, 0, 'Dealer wins: ' + str(dealer_win_count), WHITE, 120).blit_text(WIN)
                        Text(WIN_WIDTH/2, WIN_HEIGHT*2/3, 0, 0, 'Player wins: ' + str(player_win_count), WHITE, 120).blit_text(WIN)
                        pygame.display.update()
                        stop_clicks += 1
                        break
                    # this doesn´t really work because the button isn´t there anymore but can still be clicked (leave in until i've done the button hover colour change in case that makes a difference)
                    elif stop_clicks > 0:
                        run = False
                        exit()

        # logic for when the dealer draws/sticks and positioning for blit-ing drawn cards
        if playerIn and player_drawn == 1:
            nacho.hand[-1].blit_card(WIN, WIN_WIDTH/2 - CARD_WIDTH/2, WIN_HEIGHT - CARD_HEIGHT - CARD_HEIGHT/2)
            pygame.display.update()
            pygame.time.delay(1000)

        if (player_drawn == 1 or playerIn == False) and len(dealer.hand) == 2:  # makes the dealer go after the player, says if player has had their go...
            if dealer.total() >= 21 or nacho.total() > 21:  # if player or dealer is bust then dealer sticks
                dealerIn = False
                DEALER_STICK.blit_text(WIN)
                pygame.display.update()
            else:
                if dealerIn:  # if dealer is in and has 2 cards
                    if dealer.total() > 16 and dealer.total() >= nacho.total():  # dealer chooses to stick or twist
                        dealerIn = False
                        DEALER_STICK.blit_text(WIN)
                        pygame.display.update()
                    else:
                        dealer.draw(deck)
                        dealer.hand[-1].blit_card(WIN, WIN_WIDTH/2 - CARD_WIDTH/2, CARD_HEIGHT/2)
                        pygame.display.update()
                        DRAW_CARD_SOUND.play()
                        pygame.time.delay(1000)

        if playerIn and player_drawn == 2:
            nacho.hand[-1].blit_card(WIN, WIN_WIDTH/2, WIN_HEIGHT - CARD_HEIGHT - CARD_HEIGHT/2)
            pygame.display.update()
            pygame.time.delay(1000)

        if (player_drawn == 2 or playerIn == False) and len(dealer.hand) == 3:  # makes the dealer go after the player
            if dealer.total() >= 21 or nacho.total() > 21:  # if bust dealer is out (or if 21 they stick)
                dealerIn = False
                DEALER_STICK.blit_text(WIN)
                pygame.display.update()
            else:
                if dealerIn:  # if dealer is in and has 3 cards
                    if dealer.total() > 16 and dealer.total() >= nacho.total():  # dealer chooses to stick or twist
                        dealerIn = False
                        DEALER_STICK.blit_text(WIN)
                        pygame.display.update()
                    else:
                        dealer.draw(deck)
                        dealer.hand[-1].blit_card(WIN, WIN_WIDTH/2, CARD_HEIGHT/2)
                        pygame.display.update()
                        DRAW_CARD_SOUND.play()
                        pygame.time.delay(1000)

        if playerIn and player_drawn == 3:
            nacho.hand[-1].blit_card(WIN, WIN_WIDTH/2 + CARD_WIDTH/2, WIN_HEIGHT - CARD_HEIGHT - CARD_HEIGHT/2)
            pygame.display.update()
            pygame.time.delay(1000)
            playerIn = False  # after having 5 cards can´t draw more

        if (player_drawn == 3 or playerIn == False) and len(dealer.hand) == 4:  # makes the dealer go after the player
            if dealer.total() >= 21 or nacho.total() > 21:  # if bust dealer is out (or if 21 they stick)
                dealerIn = False
                DEALER_STICK.blit_text(WIN)
                pygame.display.update()
            else:
                if dealerIn:  # if dealer is in and has 4 cards
                    if dealer.total() > 16 and dealer.total() >= nacho.total():  # dealer chooses to stick or twist
                        dealerIn = False
                        DEALER_STICK.blit_text(WIN)
                        pygame.display.update()
                    else:
                        dealer.draw(deck)
                        dealer.hand[-1].blit_card(WIN, WIN_WIDTH/2 + CARD_WIDTH/2, CARD_HEIGHT/2)
                        pygame.display.update()
                        DRAW_CARD_SOUND.play()
                        pygame.time.delay(1000)
                        dealerIn = False  # after having 5 cards can´t draw more
                        DEALER_STICK.blit_text(WIN)
                        pygame.display.update()
        
        # both player and dealer have stuck/bust and so reveals the dealers full hand and the totals
        if playerIn == False and dealerIn == False:
            dealer.hand[0].blit_card(WIN, WIN_WIDTH/2 - CARD_WIDTH/2 - CARD_WIDTH, CARD_HEIGHT/2)
            dealer.hand[1].blit_card(WIN, WIN_WIDTH/2 - CARD_WIDTH, CARD_HEIGHT/2)
            pygame.display.update()
            if len(dealer.hand) >= 3:
                dealer.hand[2].blit_card(WIN, WIN_WIDTH/2 - CARD_WIDTH/2, CARD_HEIGHT/2)
                pygame.display.update()
                if len(dealer.hand) >= 4:
                    dealer.hand[3].blit_card(WIN, WIN_WIDTH/2, CARD_HEIGHT/2)
                    pygame.display.update()
                    if len(dealer.hand) >= 5:
                        dealer.hand[4].blit_card(WIN, WIN_WIDTH/2 + CARD_WIDTH/2 - CARD_WIDTH, CARD_HEIGHT/2)
                        pygame.display.update()
            # could probably do one update here rather than the 4 done above
            pygame.time.delay(1000)
            player_score = Text(1000, 600, 0, 0, "Player\'s Total: " + str(nacho.total()))
            player_score.blit_text(WIN)
            dealer_score = Text(1000, 200, 0, 0, "Dealer\'s Total: " + str(dealer.total()))
            dealer_score.blit_text(WIN)
            pygame.display.update()

            # works out who wins the game, does winning/losing messages
            if dealer.total() == 21:
                if len(dealer.hand) == 2:
                    print('Dealer has Blackjack! You lose :(')
                    dealer_win_count += 1
                    Text(WIN_WIDTH/2, WIN_HEIGHT/2, 0, 0, 'Dealer has Blackjack', WHITE, 120).blit_text(WIN)
                    pygame.display.update()
                    pygame.time.delay(5000)
            elif len(nacho.hand) == 5 and nacho.total() <= 21:
                print(f'Five-Card Charlie! You drew 5 cards and your total of {nacho.total()} is less than or equal to 21. You win :D')
                player_win_count += 1
                confetti_animation(WIN, WIN_WIDTH//2 - frame_width//2, WIN_HEIGHT//2 - frame_height//2)
            elif dealer.total() == 21:
                if len(dealer.hand) > 2:
                    print('Dealer has 21. You lose :(')
                    dealer_win_count += 1
                    dealer_wins()
            elif nacho.total() == 21:
                if len(nacho.hand) == 2:
                    print('Blackjack!!! You win :D')
                    player_win_count += 1
                    fireworks_animation(WIN)
                else:
                    print(f'Your total of {nacho.total()} beats the dealers {dealer.total()}. You win :D')
                    player_win_count += 1
                    confetti_animation(WIN, WIN_WIDTH//2 - frame_width//2, WIN_HEIGHT//2 - frame_height//2)
            elif nacho.total() > 21:
                print('You\'ve gone bust. You lose! :(')
                dealer_win_count += 1
                dealer_wins()
            elif dealer.total() > 21:
                print('Dealer is bust! You win :D')
                player_win_count += 1
                confetti_animation(WIN, WIN_WIDTH//2 - frame_width//2, WIN_HEIGHT//2 - frame_height//2)
            elif nacho.total() > dealer.total():
                print(f'Your total of {nacho.total()} beats the dealers {dealer.total()}. You win :D')
                player_win_count += 1
                confetti_animation(WIN, WIN_WIDTH//2 - frame_width//2, WIN_HEIGHT//2 - frame_height//2)
            elif nacho.total() == dealer.total():
                print(f'You both have a total of {nacho.total()}. You lose :(')
                dealer_win_count += 1
                dealer_wins()
            elif nacho.total() < dealer.total():
                print(f'Your total of {nacho.total()} is less than the dealers {dealer.total()}. You lose :(')
                dealer_win_count += 1
                dealer_wins()
            else:
                print('error deciding who won')

            # plays the game again (need to change this so there's a button to start a new game instead)
            main()

# Start game
main()


# notes
# can double click on draw card to fuck it up
# add in a confetti animation and a 21 image when someone gets 21
# write in who the player/dealer are
# write in your own name
# do a play again button
# change the colour of the buttons when you hover over them
# get a sound for the hidden dealer card reveal
# get a sound of money falling when you win
# add in the blackjack logic for 5 cards
# add in blackjack functionality of burning a 13, splitting a double etc
# make it so that the player wins confetti screen still shows all the cards/totals/buttons etc
# 5 card rule - Regardless of whether the dealer has a stronger hand or not, the player will win because they have reached the five-card goal without going bust. However, if a player manages to achieve a Five-Card Charlie, but the dealer has blackjack (a 10 and an ace,) the dealer will still win
# 5 card charlie doesn´t apply to the dealer, only the player benefits from it. So need to figure out logic for dealer (currently they'll stop after 5 cards no matter what)
# check if the dealer gets 21 with 3+ cards if it stops the player from playing or not