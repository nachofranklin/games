what it needs to do
- get valid moves (includes checking it's within the board, if it can take a piece, if it's blocked by a piece, if moving would result in your king getting checked - this will be overwritten for each piece) - this will need to be done in [[Game State]], instead get raw moves
- checking if it's within the board
- checking if moving would result in your king getting checked - [[Game State]]
- have a piece colour black/white
- enum PieceColour {white, black}
- have a score value
- a way to check if an other piece is an enemy
- have a grid pos
- name
- sprite
- directions (if the piece can move infinitely then just do 1 vector2 for 1 square in that direction)
- if it's never moved before - should this be piece not piece resource - no


for getting raw moves
- each piece will have an array of possible directions
	- pawns also have an attacking/taking direction
	- knights don't really have a direction just possible moves
- the board size could vary
- a piece could be blocking
- we don't check for if moving leaves the piece in check, instead we'll get a list of all the raw moves and game logic can check each of those for if it leaves us in check or not
- 
- raw moves = []
- so we loop through each direction
	- get the difference between current pos and top/bottom/left/right of the board depending on what direction we're going (while loop)
	- multiplier = 0
	- loop through that difference
		- multiplier += 1
		- new pos = grid pos + direction * multiplier
		- occupier = board state[current pos]
		- if occupier == null then append new pos
		- if occupier != null
			- if is enemy(occupier)
				- append new pos
				- break
			- if is enemy == false
				- break

need to add in something for castling - need a var for if already moved (for king and rook but also a way to differentiate between rooks so the king knows which way to castle - can differentiate from their grid_pos as if they've not already moved then it can work out which is which)
need to add in something for en passent
need to add in something for pawns moving up 2 (or down 2 if black) - need a var for if already moved - done

i'll also have to change grid pos as that shouldn't be saved in the resource, that's another one for [[Game State]]