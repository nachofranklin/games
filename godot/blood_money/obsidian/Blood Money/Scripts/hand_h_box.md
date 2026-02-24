---
Extends: HBoxContainer
Class Name: Hand
---
#### What it needs to do

- hold and display all the cards
- fan out the cards
- if cards get picked up and put back they need to go to the same position as they were before
- be able to draw new cards into the hand

#### How to do it

- loop through each child (Card_UI) and set the card_ui.parent to self and connect the reparent_requested signal
- create a func for what the reparent signal should do
	- take the child as a parameter
	- add the card as a child - reparent
	- if the card was already in the hand it needs a way to go back to the same pos - move_child