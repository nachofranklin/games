# make a script that inherits from this and a resource for each piece, remember to link the script to the resource
extends Resource
class_name PieceResource

enum PieceColour {WHITE, BLACK}

@export var name: String
@export var directions: Array[Vector2i]
@export var score_value: int
@export var piece_colour: PieceColour
@export var sprite: Texture2D

var grid_pos: Vector2i
var has_never_moved: bool = true


func get_raw_moves(board_state: Array) -> Array[Vector2i]:
	# this works for infinitely sliding pieces (bishop, rook, queen)
	# needs to be over written for pawn, knight, king
	var moves: Array[Vector2i] = []
	
	for dir in directions:
		var multiplier: int = 1
		while true:
			var new_pos = grid_pos + dir * multiplier
			if not is_in_bounds(new_pos, board_state):
				break
			
			var occupier = board_state[new_pos.y][new_pos.x]
			if occupier == null:
				moves.append(new_pos)
			elif is_enemy(occupier):
				moves.append(new_pos)
				break
			else:
				break
			multiplier += 1
	
	return moves


func is_enemy(other_piece: PieceResource) -> bool:
	return other_piece.piece_colour != piece_colour


func is_in_bounds(new_pos: Vector2i, board_state: Array) -> bool:
	return new_pos.y >= 0 and new_pos.y < board_state.size() and new_pos.x >= 0 and new_pos.x < board_state.size()


func is_king_safe(new_pos:Vector2i, board_state: Array) -> bool:
	# this probably needs to be in game state rather than piece
	# 1. Simulate the move on a temporary board copy
	# 2. Check if our king is in check on that copy
	# 3. Undo / discard the copy
	# 4. Return true only if king is safe
	return true
