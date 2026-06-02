extends Node2D
class_name Board

const TILE_SCENE = preload('res://scenes/tile.tscn')

@export var board_width: int = 8
@export var board_height: int = 8
@export var available_size: Vector2 = Vector2(600, 600)
@export var light_square_colour: Color = Color(0.792, 1.0, 0.843)
@export var dark_square_colour: Color = Color(0.392, 0.753, 0.4)
@export var selected_colour: Color = Color(0.498, 0.659, 1.0, 0.843)

var grid: Array = []
var tile_size: float
var last_tile_selected: Tile = null


func _ready() -> void:
	#initialise_board() # testing purposes
	Events.tile_clicked.connect(_on_tile_clicked)
	last_tile_selected = null


func initialise_board() -> void:
	_calculate_tile_size()
	_generate_board()
	_centre_board() # how best to centre the node?


func get_available_size(available_space: Vector2) -> void:
	available_size = available_space


func _calculate_tile_size() -> void:
	var max_tile_width = available_size.x / board_width
	var max_tile_height = available_size.y / board_height
	tile_size = min(max_tile_width, max_tile_height)


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


func _centre_board() -> void: # assumes the node is centred rather than at 0,0
	var total_width = board_width * tile_size
	var total_height = board_height * tile_size
	position -=Vector2(total_width / 2.0, total_height / 2.0)


func _on_tile_clicked(grid_pos) -> void:
	var tile: Tile = grid[grid_pos.y][grid_pos.x]
	# for showing possible moves when tile is clicked happens in piece_manager. This is just to show the selected tile
	# 1) select a tile and the last tile was null
	# 2) select a tile and the last tile == selected tile
	# 3) select a tile and the last tile != selected tile
	if last_tile_selected == null: # if there was no previously selected tile
		tile.tile_selected()
		last_tile_selected = tile
	elif last_tile_selected == tile: # if you click the same tile again
		tile.tile_unselected()
		last_tile_selected = null
	elif last_tile_selected != tile: # if the new tile is different to the old tile
		tile.tile_selected()
		last_tile_selected.tile_unselected()
		last_tile_selected = tile


func grid_to_world(grid_pos: Vector2i) -> Vector2:
	return position + Vector2(grid_pos.x + 0.5, grid_pos.y + 0.5) * tile_size # + 0.5 centres the grid pos
