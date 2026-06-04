extends Node2D
class_name Game

@export var board: Board
@export var piece_manager: PieceManager
@export var game_state: GameState

@onready var board_space: Control = %BoardSpace


func _ready() -> void:
	position = get_viewport_rect().size/2 # centres everything
	await get_tree().process_frame # without this the control node doesn't know it's size
	board.get_available_size(board_space.size)
	_initialise_game()


func _initialise_game() -> void:
	board.initialise_board()
	var layout: Array = BoardSetup.get_standard_layout()
	piece_manager.initialise_pieces(layout)
	game_state.initialise_game_state()
	Events.game_initialised.emit(board.tile_size, board.board_width, board.board_height)
