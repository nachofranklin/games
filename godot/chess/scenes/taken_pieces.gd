extends HBoxContainer
class_name TakenPieces

const PIECE_ORDER = {
	PieceResource.PieceName.PAWN: 0,
	PieceResource.PieceName.KNIGHT: 1,
	PieceResource.PieceName.BISHOP: 2,
	PieceResource.PieceName.ROOK: 3,
	PieceResource.PieceName.QUEEN: 4
}

@export var colour_of_taken_pieces: PieceResource.PieceColour
@export var board: Board
@export var overlap_offset: float = 12.0
@export var group_gap: float = 20.0
@export var scale_ratio: float = 0.7

var piece_size: Vector2
var taken_pieces: Array[PieceResource] = []

@onready var margin_container: MarginContainer = %MarginContainer
@onready var pieces: Control = %Pieces
@onready var score_label: Label = %ScoreLabel


func _ready() -> void:
	_clear_display()
	Events.game_initialised.connect(_on_game_initialised)
	Events.piece_taken.connect(_on_piece_taken)


func _clear_display() -> void:
	for child: TextureRect in pieces.get_children():
		child.queue_free()
	score_label.text = ""


func _on_game_initialised(tile_size: float, board_width: int) -> void:
	_get_piece_size()
	var board_pixel_width: float = tile_size * board_width
	var left_margin: float = (get_viewport_rect().size.x - board_pixel_width) / 2
	margin_container.add_theme_constant_override('margin_left', int(left_margin))


func _get_piece_size() -> void:
	piece_size = Vector2(board.tile_size * scale_ratio, board.tile_size * scale_ratio)


func _on_piece_taken(piece: Piece) -> void:
	if colour_of_taken_pieces == piece.piece_resource.piece_colour:
		taken_pieces.append(piece.piece_resource)
		_sort_taken_pieces()
		_rebuild_display()
		# update score
		score_label.text = '+10'


func _sort_taken_pieces() -> void:
	taken_pieces.sort_custom(func(a: PieceResource, b: PieceResource):
		if a.score_value != b.score_value:
			return a.score_value < b.score_value
		return PIECE_ORDER[a.piece_name] < PIECE_ORDER[b.piece_name])


func _rebuild_display() -> void: # ideally make the y pos better too
	_clear_display()
	
	if taken_pieces.is_empty():
		return
	
	var x_pos: float = 0.0
	var current_type: PieceResource.PieceName = taken_pieces[0].piece_name
	
	for i in taken_pieces.size():
		var resource: Resource = taken_pieces[i]
		
		if i > 0 and resource.piece_name != current_type:
			x_pos += group_gap
			current_type = resource.piece_name
		
		var text_rect: TextureRect = TextureRect.new()
		text_rect.texture = resource.sprite
		text_rect.custom_minimum_size = piece_size
		text_rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		text_rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		text_rect.position = Vector2(x_pos, 0)
		pieces.add_child(text_rect)
		
		x_pos += overlap_offset  # pieces overlap within the same group
	
	pieces.custom_minimum_size = Vector2(x_pos, 0) + piece_size


#func _update_score() -> void:
	# this should probably be done in piece manager or game state and then emit the score every move
	# will need to iterate through every piece on the board to get the score as pawn promotion could mess up score of just taken pieces
