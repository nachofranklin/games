extends Node2D
class_name Game

@export var board: Board
@export var piece_manager: PieceManager
@export var game_state: GameState


func _ready() -> void:
	position = get_viewport_rect().size/2 # centres everything
	_initialise_game()


func _initialise_game() -> void:
	board.initialise_board()
	var layout: Array = BoardSetup.get_standard_layout()
	piece_manager.initialise_pieces(layout)
	game_state.initialise_game_state()
