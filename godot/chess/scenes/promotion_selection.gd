extends Control
class_name PromotionSelection

#const WHITE_KNIGHT: CompressedTexture2D = preload('res://art/white_knight.png')
#const WHITE_BISHOP: CompressedTexture2D = preload('res://art/white_bishop.png')
#const WHITE_ROOK: CompressedTexture2D = preload('res://art/white_rook.png')
#const WHITE_QUEEN: CompressedTexture2D = preload('res://art/white_queen.png')
#const BLACK_KNIGHT: CompressedTexture2D = preload('res://art/black_knight.png')
#const BLACK_BISHOP: CompressedTexture2D = preload('res://art/black_bishop.png')
#const BLACK_ROOK: CompressedTexture2D = preload('res://art/black_rook.png')
#const BLACK_QUEEN: CompressedTexture2D = preload('res://art/black_queen.png')

const WHITE_KNIGHT: Resource = preload('res://pieces/white_knight.tres')
const WHITE_BISHOP: Resource = preload('res://pieces/white_bishop.tres')
const WHITE_ROOK: Resource = preload('res://pieces/white_rook.tres')
const WHITE_QUEEN: Resource = preload('res://pieces/white_queen.tres')
const BLACK_KNIGHT: Resource = preload('res://pieces/black_knight.tres')
const BLACK_BISHOP: Resource = preload('res://pieces/black_bishop.tres')
const BLACK_ROOK: Resource = preload('res://pieces/black_rook.tres')
const BLACK_QUEEN: Resource = preload('res://pieces/black_queen.tres')

@onready var button_knight: Button = %ButtonKnight
@onready var button_bishop: Button = %ButtonBishop
@onready var button_rook: Button = %ButtonRook
@onready var button_queen: Button = %ButtonQueen

var pawn: Piece


func _ready() -> void:
	hide()
	Events.pawn_promotion_selection.connect(_on_pawn_promotion_selection)


func _on_pawn_promotion_selection(piece: Piece) -> void:
	pawn = piece
	
	var colour: PieceResource.PieceColour = piece.piece_resource.piece_colour
	match colour:
		PieceResource.PieceColour.WHITE:
			button_knight.icon = WHITE_KNIGHT.sprite
			button_bishop.icon = WHITE_BISHOP.sprite
			button_rook.icon = WHITE_ROOK.sprite
			button_queen.icon = WHITE_QUEEN.sprite
		PieceResource.PieceColour.BLACK:
			button_knight.icon = BLACK_KNIGHT.sprite
			button_bishop.icon = BLACK_BISHOP.sprite
			button_rook.icon = BLACK_ROOK.sprite
			button_queen.icon = BLACK_QUEEN.sprite
	
	show()


func _button_pressed(chosen_piece: Resource) -> void:
	hide()
	Events.pawn_promoted.emit(pawn, chosen_piece)


func _on_button_knight_pressed() -> void:
	var new_piece: Resource
	if pawn.piece_resource.piece_colour == PieceResource.PieceColour.WHITE:
		new_piece = WHITE_KNIGHT
	elif pawn.piece_resource.piece_colour == PieceResource.PieceColour.BLACK:
		new_piece = BLACK_KNIGHT
	
	_button_pressed(new_piece)


func _on_button_bishop_pressed() -> void:
	var new_piece: Resource
	if pawn.piece_resource.piece_colour == PieceResource.PieceColour.WHITE:
		new_piece = WHITE_BISHOP
	elif pawn.piece_resource.piece_colour == PieceResource.PieceColour.BLACK:
		new_piece = BLACK_BISHOP
	
	_button_pressed(new_piece)


func _on_button_rook_pressed() -> void:
	var new_piece: Resource
	if pawn.piece_resource.piece_colour == PieceResource.PieceColour.WHITE:
		new_piece = WHITE_ROOK
	elif pawn.piece_resource.piece_colour == PieceResource.PieceColour.BLACK:
		new_piece = BLACK_ROOK
	
	_button_pressed(new_piece)


func _on_button_queen_pressed() -> void:
	var new_piece: Resource
	if pawn.piece_resource.piece_colour == PieceResource.PieceColour.WHITE:
		new_piece = WHITE_QUEEN
	elif pawn.piece_resource.piece_colour == PieceResource.PieceColour.BLACK:
		new_piece = BLACK_QUEEN
	
	_button_pressed(new_piece)
