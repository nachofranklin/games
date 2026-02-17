---
Extends: Resource
Class Name: Card
---
#### What it needs to do

- have all the card info to be filled in in the inspector
- have a check if it's single targeted
- have a func to play the card
	- emit a signal to say a card is played
	- do characters mana -= cost of the card
	- apply effects (this will be an empty function, but each card will have a script attached that overwrites the func with whatever that specific card should do). It will take an argument of targets: Array[Node] which will loop through and apply the effect to each node in the array
- have a func that gets the targets for apply affects
- a func that gets the decription (so that if the value changes eg from 5 block to 6 block, it'll automatically reflect that in the description without needing to manually change it there too)

#### How to do it

- enums and export var which match what is in [[Card Template]]
- funcs
	- is_single_targeted
	- play(targets: Array[Node], char_stats: [[character_stats]])
	- apply_effects(targets: Array[Node]) -> void: pass
	- get_targets
	- get_description (another one that can get overwritten in the cards script)