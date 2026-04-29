extends Node
class_name BoardSetup

const WHITE_PAWN: Resource = preload('res://pieces/white_pawn.tres')
const BLACK_PAWN: Resource = preload('res://pieces/black_pawn.tres')
const WHITE_KNIGHT: Resource = preload('res://pieces/white_knight.tres')
const BLACK_KNIGHT: Resource = preload('res://pieces/black_knight.tres')
const WHITE_BISHOP: Resource = preload('res://pieces/white_bishop.tres')
const BLACK_BISHOP: Resource = preload('res://pieces/black_bishop.tres')
const WHITE_ROOK: Resource = preload('res://pieces/white_rook.tres')
const BLACK_ROOK: Resource = preload('res://pieces/black_rook.tres')
const WHITE_QUEEN: Resource = preload('res://pieces/white_queen.tres')
const BLACK_QUEEN: Resource = preload('res://pieces/black_queen.tres')
const WHITE_KING: Resource = preload('res://pieces/white_king.tres')
const BLACK_KING: Resource = preload('res://pieces/black_king.tres')


func get_standard_layout() -> Array[Dictionary]:
	var layout = []
	
	# pawns
	for col in range(8):
		layout.append({resource = WHITE_PAWN, pos = Vector2i(col, 6)})
		layout.append({resource = BLACK_PAWN, pos = Vector2i(col, 1)})
	
	# knights
	layout.append({resource = WHITE_KNIGHT, pos = Vector2i(2, 7)})
	layout.append({resource = WHITE_KNIGHT, pos = Vector2i(5, 7)})
	layout.append({resource = BLACK_KNIGHT, pos = Vector2i(2, 0)})
	layout.append({resource = BLACK_KNIGHT, pos = Vector2i(5, 0)})
	
	# bishops
	layout.append({resource = WHITE_BISHOP, pos = Vector2i(1, 7)})
	layout.append({resource = WHITE_BISHOP, pos = Vector2i(6, 7)})
	layout.append({resource = BLACK_BISHOP, pos = Vector2i(1, 0)})
	layout.append({resource = BLACK_BISHOP, pos = Vector2i(6, 0)})
	
	# rooks
	layout.append({resource = WHITE_ROOK, pos = Vector2i(0, 7)})
	layout.append({resource = WHITE_ROOK, pos = Vector2i(7, 7)})
	layout.append({resource = BLACK_ROOK, pos = Vector2i(0, 0)})
	layout.append({resource = BLACK_ROOK, pos = Vector2i(7, 0)})
	
	# queens
	layout.append({resource = WHITE_QUEEN, pos = Vector2i(3, 7)})
	layout.append({resource = BLACK_QUEEN, pos = Vector2i(3, 0)})
	
	# kings
	layout.append({resource = WHITE_KING, pos = Vector2i(4, 7)})
	layout.append({resource = BLACK_KING, pos = Vector2i(4, 0)})
	
	return layout
