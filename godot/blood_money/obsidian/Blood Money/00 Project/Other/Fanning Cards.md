what we'll have is:
- an array[Card]

what we want is:
- the cards to be equally spread out between a leftmost and rightmost point (hand_h_box)
- the central card to be higher than the rest and with 0 rotation
- cards left of centre to gradually decrease in height and to increase rotation anti-clockwise
- cards right of centre to gradually decrease in height and to increase rotation clockwise

what we need is:
- card's index in the array
- hand_ratio between 0 - 1 (leftmost - rightmost) = index / (number of cards - 1) (float) (need a separate if for having one card as the formula will try to divide by 0)
- max height the centre card should go to
- max rotation the leftmost/rightmost card should be
- ~~max number of cards in the hand = 10 (this would be in the drawing cards func not here)~~
- width of hand_h_box (- card width)
- use curves for the x, y, rotations and .sample in the hand_ratios * max amounts

to make it better:
- if i can work out the number of cards that can fit in the hand before overlapping then i could adjust the hand ratio of each card below that so that the cards don't stretch out on the x-axis all the way to the ends, leaving big gaps in between the cards (it looks silly if you have two cards in your hand and the cards are as far away from each other as possible). So, i'd need a new way of working out what the hand ratio is for those cards and can do the normal hand ratio formula for cards above the limit before overlap
- number_of_cards_before_overlap = hand.size.x / card.size.x * buffer (rounded down)
- x_gap = card.size.x * buffer / hand.size.x - card.size.x (i've honestly gone insane trying to figure out if it's correct to have the - card.size.x at the end or not. I didn't think it was but testing different gap values seemed to like having it, so i've kept it)
- hand ratio for a few cards = 0.5 - (number of cards in hand - 1) / 2 * x_gap + index * x_gap
- hand ratio for lots of cards = index / (number of cards - 1) 
- tried the mathematically correct (i think) formula for working out the gap but visually i thought it was too big, so i'll just stick with 10% for a gap