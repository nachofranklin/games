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
- keep track of if the card is playable and if it's disabled
- have an original_index var for when a card gets put back into the hand it can go to it's previous position
- set char stats and connect to the stats changed signal
- set playable and make visual changes depending on whether there's enough mana to play the card or not

#### How to do it

- attached to [[CardUI]]
- signal for reparent_requested
- setter func for card: Card
- onready var for state machine, card area, card visuals so that we can run funcs from their scripts
- var for targets: Array[Node] (should be an array of the top parent node of an enemy or i guess CardDropArea), tween, parent, playable, disabled, original_index
- funcs
	- ready
		- connect to all the card drag/aim started/ended signals
		- card_state_machine.init(self)
	- setter for card (value: Card)
		- await ready
		- card = value
		- update visuals
	- set char stats
		- await ready
		- char_stats = value
		- connect to stats_changed
	- set playable
		- playable = value
		- if not playable make the energy label text red
		- if playable undo that
	- play
		- card.play(targets, char_stats)
		- queue_free
	- animate to pos (new_pos, duration)
		- tween
	- all the state machine funcs
	- on char stats changed
		- update playable
	- on card drag or aiming started(dragged_card)
		- if the dragged_card == self then return
		- else set disabled = true
	- on card drag or aiming ended
		- disabled = false
		- update playable
	- connect to the on area entered and exited signals
		- append or remove the area to target_areas