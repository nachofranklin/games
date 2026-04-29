extends Node2D
class_name Board

const TILE_SCENE = preload('res://scenes/tile.tscn')
const WHITE_ROOK = preload('res://pieces/white_rook.tres')
const WHITE_KING = preload('res://pieces/white_king.tres')
const WHITE_PAWN = preload('res://pieces/white_pawn.tres')

@export var board_width: int = 8
@export var board_height: int = 8
@export var tile_size: float = 40.0 # i'll want to work this out dynamically when i know where i'll place the board in game scene so that it calculates the sizes needed for height available/rows and width/cols and then takes the smallest of the two to be the tile size
@export var light_square_colour: Color = Color(1.0, 1.0, 1.0, 1.0)
@export var dark_square_colour: Color = Color(0.0, 0.0, 0.0, 1.0)
@export var selected_colour: Color = Color(0.498, 0.659, 1.0, 0.843)

var grid: Array = []
var last_tile_selected: Tile = null


func _ready() -> void:
	_generate_board()
	Events.tile_clicked.connect(_on_tile_clicked)
	last_tile_selected = null
	_test_piece_moves()


func _generate_board() -> void:
	grid.clear()
	
	var colour: Color
	for row in board_height:
		var row_array: Array = []
		for col in board_width:
			var tile: Tile = TILE_SCENE.instantiate()
			if (row + col) % 2 == 0:
				colour = light_square_colour
			else:
				colour = dark_square_colour
			tile.set_tile_values(Vector2i(col, row), tile_size, colour, selected_colour)
			tile.name = 'Tile_%d_%d' % [col, row]
			tile.position = Vector2(col * tile_size, row * tile_size)
			
			row_array.append(tile)
			add_child(tile)
		grid.append(row_array)


func _on_tile_clicked(pos) -> void:
	var tile: Tile = grid[pos.y][pos.x]
	
	# 1) select a tile and the last tile was null
	# 2) select a tile and the last tile == selected tile
	# 3) select a tile and the last tile != selected tile
	if last_tile_selected == null:
		tile.tile_selected()
		last_tile_selected = tile
	elif last_tile_selected == tile:
		tile.tile_unselected()
		last_tile_selected = null
	elif last_tile_selected != tile:
		tile.tile_selected()
		last_tile_selected.tile_unselected()
		last_tile_selected = tile


func _test_piece_moves() -> void:
	var board_state = []
	for row in board_height:
		var r = []
		for col in board_width:
			r.append(null)
		board_state.append(r)
	
	var test_piece = WHITE_PAWN.duplicate()
	test_piece.grid_pos = Vector2i(2, 2) # middle of board
	board_state[2][2] = test_piece
	var rook2 = WHITE_ROOK.duplicate()
	rook2.piece_colour = PieceResource.PieceColour.BLACK
	rook2.grid_pos = Vector2i(1, 1) # (x, y)
	board_state[1][1] = rook2 # [y][x]
	
	# Print raw moves
	var moves = test_piece.get_raw_moves(board_state)
	print("test_piece moves: ", moves)
	print("Move count: ", moves.size())
