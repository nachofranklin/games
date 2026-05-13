extends Node2D
class_name GameState

#const SLIDING_PIECES: Array = [PieceResource.PieceName.ROOK, PieceResource.PieceName.BISHOP, PieceResource.PieceName.QUEEN]

@export var board: Board
@export var player_white: PlayerResource
@export var player_black: PlayerResource

var current_player: PlayerResource
var board_state: Array = []
var last_selected_piece: Piece = null
var highlighted_tiles: Array[Vector2i] = []


func _ready() -> void:
	Events.tile_clicked.connect(_on_tile_clicked)
	Events.turn_ended.connect(_on_turn_ended)
	#initialise_game_state() # testing purposes


func initialise_game_state() -> void:
	current_player = player_white
	Events.turn_started.emit(current_player)


func setup_board(initial_board_state: Array) -> void:
	board_state = initial_board_state


func _on_tile_clicked(grid_pos: Vector2i) -> void:
	var clicked_piece: Piece = board_state[grid_pos.y][grid_pos.x]
	
	if last_selected_piece == null:
		_try_select(clicked_piece)
	elif last_selected_piece.grid_pos == grid_pos:
		_deselect()
	else:
		if grid_pos in highlighted_tiles:
			_move_piece(last_selected_piece, grid_pos)
			_deselect()
			Events.turn_ended.emit()
		else:
			_deselect()
			_try_select(clicked_piece)


func _move_piece(piece: Piece, new_grid_pos: Vector2i) -> void:
	var current_occupant: Piece = board_state[new_grid_pos.y][new_grid_pos.x]
	if current_occupant != null:
		Events.piece_taken.emit(current_occupant)
	board_state[piece.grid_pos.y][piece.grid_pos.x] = null
	board_state[new_grid_pos.y][new_grid_pos.x] = piece
	piece.move_to(new_grid_pos, board.grid_to_world(new_grid_pos))
	board.last_tile_selected.tile_unselected()
	board.last_tile_selected = null
	# need to end turn and switch to the other player to have their go


func _try_select(piece: Piece) -> void:
	if piece == null:
		return
	elif piece.piece_resource.piece_colour != current_player.piece_colour:
		return
	# else if you've clicked one of your pieces...
	last_selected_piece = piece
	highlighted_tiles = _get_valid_moves(piece)
	
	for move in highlighted_tiles:
		var tile: Tile = board.grid[move.y][move.x]
		var is_empty: bool = board_state[move.y][move.x] == null
		tile.highlight_tile(is_empty)


func _deselect() -> void:
	for move in highlighted_tiles:
		var tile: Tile = board.grid[move.y][move.x]
		tile.reset_highlighted_tile()
	highlighted_tiles.clear()
	last_selected_piece = null


func _get_valid_moves(piece: Piece) -> Array[Vector2i]:
	var valid_moves: Array[Vector2i] = []
	var raw_moves: Array[Vector2i] = piece.piece_resource.get_raw_moves(board_state, piece.grid_pos)
	
	# need to check two things...
	# 1) what moves can be made if currently in check
	# 2) if moving a piece leaves you in check afterwards
	# update - both things are, move piece, is my king now in check or not, so it's the same func, no need to over complicate it by essentially writing it out twice
	
	for move: Vector2i in raw_moves:
		if _is_own_king_safe(piece, move):
			valid_moves.append(move)
	
	return valid_moves


func _is_own_king_safe(piece: Piece, new_pos: Vector2i) -> bool:
	# create a copy of the board
	var sim_board: Array = board_state.duplicate(true)
	# move the piece to it's new move pos
	sim_board[piece.grid_pos.y][piece.grid_pos.x] = null
	sim_board[new_pos.y][new_pos.x] = piece
	# get own kings pos
	var own_kings_pos: Vector2i = _get_own_kings_pos(sim_board)
	# iterate through every opp piece and get their raw moves
	# if own kings pos in their raw moves return false
	for row in sim_board:
		for opp_piece: Piece in row:
			if opp_piece == null:
				continue
			if opp_piece.piece_resource.piece_colour != piece.piece_resource.piece_colour:
				var raw_moves = opp_piece.piece_resource.get_raw_moves(sim_board, opp_piece.grid_pos)
				if own_kings_pos in raw_moves:
					return false
	
	return true


func _get_own_kings_pos(sim_board_state: Array) -> Vector2i:
	var y: int = 0
	for row in sim_board_state:
		var x: int = 0
		for piece: Piece in row:
			if piece == null:
				x += 1
				continue
			if piece.piece_resource.piece_name == PieceResource.PieceName.KING and piece.piece_resource.piece_colour == current_player.piece_colour:
				return Vector2i(x, y)
			x += 1
		y += 1
	
	print('no king on the board?')
	return Vector2i(-1, -1) # there should always be a king on the board so this should never happen


func _on_turn_ended() -> void:
	if current_player == player_white:
		current_player = player_black
	else:
		current_player = player_white
	Events.turn_started.emit(current_player)
