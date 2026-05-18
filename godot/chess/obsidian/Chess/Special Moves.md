#### Castling

if king has never moved
	iterate through the board state to find rooks
		if rook hasn't moved
			find out if rook is king/queens rook
			make sure there are no pieces in between
			make sure not currently in check
			make sure when the king moves that it wouldn't be in check in the square it moves through or ends up in
			if kings rook
				move king two to the right
				move rook one to the right (of the kings original pos)
			elif queens rook
				move king two to the left
				move rook one to the left (of the kings original pos)

for get valid moves it just needs a vector2i, so i guess that would be just the kings 2 movement

in move piece i'll probably have to do an if statement to add in the rooks movement

#### En Passant

I think en passant only triggers if their pawn moves two spaces and ends up next to your pawn to the left/right ie they've tried to use the 2 space move to dodge your pawn.
So, maybe when pawns move two forward there could be some sort of check to see if an opp pawn is to the left/right of it and then an en_passant_available var could turn true? But that would require pawn res to know the board state, so not ideal. Maybe send out an en passant check signal when a pawn moves two up