#### What needs to happen at the start of a battle?

a lot of this will go to the player handler. I'll tick off what is done by the player handler

- [ ] when the battle is supposed to start the battle scene will get loaded up
- [ ] in the ready func we can temporarily set the char_stats as the place where everything else will take it's stats from (this should be in run when that gets built)
- [ ] and we can also call a start battle func where...
- [ ] turn number = 0
- [ ] enemies you face are randomly selected based off of what path option was chosen (regular enemy, mini boss, boss) and what act you're in - currently this just uses the same two enemies in the battle scene, will implement this later
- [x] the draw pile should equal a duplication of your deck
- [x] need to shuffle the draw pile
- [x] discard and exhaust piles should be new CardPile
- [x] check if the hand is empty?
- [ ] selected enemies get loaded into the fight
- [ ] player gets loaded into the fight
- [ ] should probably initialise win/loss conditions to check for when the battle ends
- [x] apply the effects of the start of battle relics (anything that effects the base values)
- [ ] ~~apply the effects of the start of battle statuses - don't think this can be a thing~~
- [x] start the turn
	- [ ] turn number += 1 
	- [x] reset block
	- [x] reset mana
	- [x] reset the number of cards you should draw
	- [x] emit stats changed signal
	- [x] apply start of turn relics
	- [x] apply start of turn statuses
	- [x] emit the stats changed signal again?
	- [x] draw x cards from the draw pile
	- [x] make the cards and end turn button be available


So, how do we deal with a start of battle relic that does something like +1 energy at the start of the battle (not +1 each turn, just a one off)? - this would actually be a start of turn relic which only applies if turn_number == 1
	Would i make it a start of turn relic instead but have an if statement that says if it's the first turn then +1, else do nothing - YES
	~~Or do i create another variable that is a start of battle mana += 1 but then i'd still have to only play that if it's the first turn~~
	~~Or do i make it so that the reset of stats happens at battle start and then happens at the end of the enemies turn rather than the start of players turn~~