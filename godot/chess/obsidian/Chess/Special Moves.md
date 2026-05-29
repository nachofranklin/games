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
So, maybe when pawns move two forward there could be some sort of check to see if an opp pawn is to the left/right of it and then an en_passant_available var could turn true? But that would require pawn res to know the board state, so not ideal. Maybe send out an en passant check signal when a pawn moves two up. But would also have to send out something that iterates through every opp pawn after a move to say that en passant is no longer available

in game state i need a var pawn_just_moved_2_up: Piece = null
that var can be changed in the move piece func so that whenever you move a piece that var gets updated to either the piece that just moved or to null

in get valid moves for pawns it will return all possible +1 or +2 moves but not en passant, so we need to add en passant move to that list then it can check if king is safe and potentially remove it if need be

get en passant moves(piece we've just clicked on: piece) -> array[vector2i]
var en passant moves = []
first check that the piece is a pawn (don't need to check correct colour as that's already done by try select i think)
then check if pawn just moved 2 up is not null
then check that the y level is the same for both the piece and pawn just moved 2 up
then check if the x pos is +/- 1 for the two pieces
append a move to en passant moves that is pawn just moved 2 up.pos + piece's dir (might have to do a for dir in directions even though it's only one but it's in an array)
return en passant moves

this will likely work for en passant but i don't think it will take the piece - correct

now back in move piece i need to say if en passant happened then events.piece taken.emit(pawn just moved 2 up)
so if piece name == pawn
if pawn just moved 2 up is not null
if current y level is the same
if new grid pos.x = pawn just moved 2 up.x
then trigger piece taken

#### Pawn Promotion

