---
Extends: Stats
Class Name: CharacterStats
---
#### What it needs to do

- have all stats i can think of
	- art - [[stats]]
	- health - [[stats]]
	- max health - [[stats]]
	- block - [[stats]]
	- name
	- ~~gold~~
	- primary colour
	- card piles
		- starting deck
		- deck
		- hand
		- draw
		- discard
		- exhaust
	- list of relics
	- list of potions
	- base cards per turn - export
	- base mana per turn - export
	- cards per turn - setter
	- mana per turn - setter

#### How to do it

- setter func for mana and cards per turn
- reset func to set the mana and cards per turn back to the base amount (for the end of the turns)
- func that returns a bool for if a card can be played or not, mana >= card cost
- an instantiate func to create a var that duplicates character stats, set health and block, calls the reset funcs above, sets deck to starter deck, draw, discard, exhaust to new card piles, then returns the var