---
Extends: Resource
Class Name: CardPile
---
Linked to [[CardPile]] scene.

#### What it needs to do

- Check if card pile is empty - pointless, .is_empty() already exists
- Draw a card
- Add a card
- Remove a card
- Remove all cards (clear) - not pointless as while .clear() already exists, we need to emit the change in size signal after
- Shuffle - pointless as .shuffle() already exists
- Every time the card pile size changes it needs to emit a signal so that we can update the visuals

#### How to do it

- create a signal card_pile_size_changed(new_amount) - maybe work out the cards.size() in the functions connecting to the signal instead of passing it to the signal
- have an export var for cards: Array[Card]
- create funcs for all the above needs