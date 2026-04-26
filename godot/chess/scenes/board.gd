extends Node2D
class_name Board

const TILE_SCENE = preload('res://scenes/tile.tscn')

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
	print(last_tile_selected)
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
	print(last_tile_selected)
