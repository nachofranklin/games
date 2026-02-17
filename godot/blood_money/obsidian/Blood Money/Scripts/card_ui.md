---
Extends: Control
Class Name: CardUI
---
#### What it needs to do

- get the state machine up and running
- identify when the card is hovered over an enemy or CardDropArea
- update the visuals (call func from [[card_visuals]])
- have a func that plays the card and queue frees it once played (called in the released state)
	- i need to make the play card func in [[card]] to actually do whatever the card tells it to
- have a func that tweens a card (called in aiming state)

#### How to do it

- attached to [[CardUI]]
- signal for reparent_requested
- setter func for card: Card
- onready var for state machine, card area, card visuals so that we can run funcs from their scripts
- var for targets: Array[Node] (should be an array of the top parent node of an enemy or i guess CardDropArea), tween, parent
- funcs
	- ready
		- card_state_machine.init(self)
	- setter for card (value: Card)
		- await ready
		- card = value
		- update visuals
	- animate to pos (new_pos, duration)
		- tween
	- all the state machine funcs
	- connect to the on area entered and exited signals
		- append or remove the area to target_areas