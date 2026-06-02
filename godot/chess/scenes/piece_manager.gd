extends Node2D
class_name PieceManager

const PIECE_SCENE: PackedScene = preload("res://scenes/piece.tscn")

@export var board: Board # board needs to be initialised before piece manager
@export var game_state: GameState

var board_state: Array = []


func _ready() -> void:
	#initialise_pieces(BoardSetup.get_standard_layout()) # testing purposes
	Events.piece_taken.connect(_on_piece_taken)
	Events.pawn_promoted.connect(_on_pawn_promoted)


func initialise_pieces(layout: Array) -> void:
	_create_empty_board_state()
	for dict in layout:
		_spawn_piece(dict.resource, dict.pos)
	game_state.setup_board(board_state)


func _create_empty_board_state() -> void:
	board_state.clear()
	for row in board.board_height:
		var r = []
		for col in board.board_width:
			r.append(null)
		board_state.append(r)


func _spawn_piece(resource: PieceResource, pos: Vector2i) -> void:
	var piece: Piece = PIECE_SCENE.instantiate()
	add_child(piece)
	piece.setup_piece(resource.duplicate(), pos, board.grid_to_world(pos), board.tile_size)
	board_state[pos.y][pos.x] = piece


func _on_piece_taken(piece: Piece) -> void:
	board_state[piece.grid_pos.y][piece.grid_pos.x] = null
	piece.queue_free()
	# add the piece to the taken pieces area above/below the board
	# adjust the players score


func _on_pawn_promoted(pawn: Piece, new_piece: Resource) -> void:
	var pos: Vector2i = pawn.grid_pos
	_on_piece_taken(pawn)
	_spawn_piece(new_piece, pos)
