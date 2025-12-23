What is the simplest version of this game that is still “a game”?

#### Battle Scene

##### Initialise
- Random group of enemies based on the act you're in
- Player/enemies applies any start of combat effects

##### Loop
- Player applies start of turn effects from relics and statuses
- Player draws 5 cards and gets 3 energy
- Player plays cards and ends their turn
- Player applies end of turn effects from relics and statuses
- Remaining cards in hand get discarded
- Enemies applies start of turn effects from statuses
- Enemy does a conditional (higher priority) or random (lower priority) pre-defined move
- Enemies apply end of turn effects from statuses
- Loop repeats until either player dies, all enemies die, player runs away, or enemies run away

##### Player wins
- Player applies end of combat effects
- Goes to a reward scene where a player gets:
	- gold
	- choice of adding one/zero of three random cards to their deck
	- a possible potion
- Then back to the map