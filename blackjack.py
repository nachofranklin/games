import random
import time

# draw a card
def dealCard(turn):
    card = random.choice(deck)
    turn.append(card)
    deck.remove(card)

# calculate total of each hand
def total(turn):
    total = 0
    ace11 = 0
    face = ['Jack', 'Queen', 'King']
    for card in turn:
        if card in face:
            total += 10
        elif card in range(2, 11):
            total += card
        elif card == 'Ace':
            total += 11
            ace11 += 1
        else:
            print('error totaling cards')
    while total > 21:
        if ace11 > 0:
            total -= 10
            ace11 -= 1
        else:
            break
    return total

# seeing dealers hand
def revealDealerHand():
    if len(dealerHand) == 2:
        return dealerHand[0]
    elif len(dealerHand) > 2:
        revealed = [dealerHand[0]]
        for i in range(2, len(dealerHand)):
            revealed.append(dealerHand[i])
        return revealed

playAgain = True
playerWins = 0
dealerWins = 0
while playAgain == True:

    # deck of cards and player/dealer hands
    deck = []
    for i in range(4):
        for v in range(1, 14):
            if v == 1:
                v = 'Ace'
            elif v == 13:
                v = 'King'
            elif v == 12:
                v = 'Queen'
            elif v == 11:
                v = 'Jack'
            deck.append(v)
    playerHand = []
    dealerHand = []

    # game loop
    for i in range(2):
        dealCard(dealerHand)
        dealCard(playerHand)

    playerIn = True
    dealerIn = True

    while playerIn or dealerIn:
        print(f'Dealer has {revealDealerHand()} and X')
        time.sleep(1)
        print(f'You have {playerHand} for a total of {total(playerHand)}')
        time.sleep(1)

        if total(dealerHand) == 21:
            break
        if total(playerHand) == 21:
            break

        if playerIn:
            stickOrTwist = input('1) Stick or 2) Draw - ')
            if stickOrTwist == '1':
                playerIn = False
            elif stickOrTwist == '2':
                dealCard(playerHand)
                print(f'You\'ve drawn a {playerHand[-1]}')
            else:
                print('Enter only "1" or "2"')
       
        if total(dealerHand) > 16:
            dealerIn = False
        else:
            dealCard(dealerHand)
       
        if total(playerHand) > 21:
            break

    time.sleep(1)
    print('')
    print(f'Your final hand is {playerHand}')
    print(f'Dealer\'s final hand is {dealerHand}')
    print('')

    time.sleep(1)
    if total(dealerHand) == 21:
        if len(dealerHand) == 2:
            print('Dealer has Blackjack! You lose :(')
            dealerWins += 1
        else:
            print('Dealer has 21. You lose :(')
            dealerWins += 1
    elif total(playerHand) == 21:
        if len(playerHand) == 2:
            print('Blackjack!!! You win :D')
            playerWins += 1
        else:
            print(f'Your total of {total(playerHand)} beats the dealers {total(dealerHand)}. You win :D')
            playerWins += 1
    elif total(playerHand) > 21:
        print('You\'ve gone bust. You lose! :(')
        dealerWins += 1
    elif total(dealerHand) > 21:
        print('Dealer is bust! You win :D')
        playerWins += 1
    elif total(playerHand) > total(dealerHand):
        print(f'Your total of {total(playerHand)} beats the dealers {total(dealerHand)}. You win :D')
        playerWins += 1
    elif total(playerHand) == total(dealerHand):
        print(f'You both have a total of {total(playerHand)}. You lose :(')
        dealerWins += 1
    elif total(playerHand) < total(dealerHand):
        print(f'Your total of {total(playerHand)} is less than the dealers {total(dealerHand)}. You lose :(')
        dealerWins += 1
    else:
        print('error deciding who won')

    time.sleep(1)
    print('')
    oneMoreGame = input('Play again? Y/N - ').lower()
    print('')
    if oneMoreGame == 'y':
        continue
    elif oneMoreGame == 'n':
        break
    else:
        print('Enter "y" or "n"')
print(f'''You won {playerWins} times
The dealer won {dealerWins} times''')