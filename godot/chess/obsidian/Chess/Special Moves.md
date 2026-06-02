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

if white/black pawn reaches the top/bottom of the board (y=0 or y=len(board_state)?) then i emit the pawn promotion selection signal - probably want this to happen at the end of the move piece func
on pawn promotion selection, make the selection scene visible
get the pawn's colour
add the button options with the correct colour to choose from
on button being pressed, set the board state of the pawns pos to now be a new instance of whatever piece was selected (piece manager's spawn piece)
also need to remove the pawn first (piece manager's on piece taken - although this could have unintended consequences of counting it as being taken for scoring when it's not)

summary - 2 new signals, 1 at the end of move piece in game state that emits if the pawn reaches the end. This connects to promotion selection where the scene becomes visible and the button images are updated to be black/white depending on the pawn colour. If you click one of the 4 button options it hides the scene and emits the second signal with the pawn and the chosen piece (as a resource). Piece manager connects to this signal, saves the pos of the pawn then deletes it and spawns the new piece which was selected

- Need to change it so that i can't click on anything else other than selecting the new piece - done
- Also maybe add in a hide/show button so the player can look at the board to decide what piece they want - STILL NEED TO DO THIS!!!!!!!!
- Still need to fix the centring issues - done
- Might need to slightly adjust the turn ending to allow for the player to choose their new piece before the opp can take their go - done added a var to check if awaiting promotion