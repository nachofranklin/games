# make a script that inherits from this and a resource for each piece, remember to link the script to the resource
extends Resource
class_name PieceResource

enum PieceName {PAWN, ROOK, BISHOP, KNIGHT, QUEEN, KING}
enum PieceColour {WHITE, BLACK}

@export var piece_name: PieceName
@export var directions: Array[Vector2i]
@export var score_value: int
@export var piece_colour: PieceColour
@export var sprite: CompressedTexture2D

#var grid_pos: Vector2i # piece res shouldn't know it's pos but it can be passed that info
var has_never_moved: bool = true


func get_raw_moves(board_state: Array, grid_pos: Vector2i) -> Array[Vector2i]:
	# this works for infinitely sliding pieces (bishop, rook, queen)
	# needs to be over written for pawn, knight, king
	var moves: Array[Vector2i] = []
	
	for dir in directions:
		var multiplier: int = 1
		while true:
			var new_pos = grid_pos + dir * multiplier
			if not _is_in_bounds(new_pos, board_state):
				break
			
			var occupier: Piece = board_state[new_pos.y][new_pos.x]
			if occupier == null:
				moves.append(new_pos)
			elif _is_enemy(occupier):
				moves.append(new_pos)
				break
			else:
				break
			multiplier += 1
	
	return moves


func _is_enemy(other_piece: Piece) -> bool:
	return other_piece.piece_resource.piece_colour != piece_colour


func _is_in_bounds(new_pos: Vector2i, board_state: Array) -> bool:
	return new_pos.y >= 0 and new_pos.y < board_state.size() and new_pos.x >= 0 and new_pos.x < board_state.size()
